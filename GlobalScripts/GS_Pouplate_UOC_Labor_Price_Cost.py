import GS_Labor_Utils

#Create a Dictionary(value, valuecode) of a dropdown attribute
def buildDict(prodAttr):
	outDict = dict()
	for v in prodAttr.Values:
		if v.ValueCode != 'None':
			outDict[v.Display] = v.ValueCode
	return outDict

def populateCost(Quote, row, parts_dict, fo_dict):
	error_flag = True
	different_salesOrg = False
	FO_Eng_1_Unit_WTW_Cost = FO_Eng_2_Unit_WTW_Cost = WTW_Markup_Factor = 0.00
	try: #For custom deliverables
		fo1_split = GS_Labor_Utils.getFloat(row["FO Eng % Split"]) * 0.01
		fo2_split = 0.0
		fo1_eng = row.GetColumnByName('FO Eng').DisplayValue
		fo2_eng = 'None'
	except: #For standard labor deliverables
		fo1_split = GS_Labor_Utils.getFloat(row["FO Eng 1 % Split"]) * 0.01
		fo2_split = GS_Labor_Utils.getFloat(row["FO Eng 2 % Split"]) * 0.01
		fo1_eng = row.GetColumnByName('FO Eng 1').DisplayValue
		fo2_eng = row.GetColumnByName('FO Eng 2').DisplayValue
	if fo1_eng != 'None':
		fo1_eng = fo_dict.get(fo1_eng, '')
	if fo2_eng != 'None':
		fo2_eng = fo_dict.get(fo2_eng, '')
	Trace.Write("fo1_eng:{} fo2_eng:{}".format(fo1_eng, fo2_eng))
	Trace.Write("Ges eng partnumber:{}".format(row["GES Eng"]))
	Trace.Write('Final_Hrs = ' + str(row['Final Hrs']))
	gesFinalHours = round(GS_Labor_Utils.getFloat(row["Final Hrs"]) * GS_Labor_Utils.getFloat(row["GES Eng % Split"]) / 100)
	Trace.Write('gesFinalHours = ' + str(gesFinalHours))
	fo_ENG1_FinalHours = round(GS_Labor_Utils.getFloat(row["Final Hrs"]) * fo1_split)
	Trace.Write('fo_ENG1_FinalHours = ' + str(fo_ENG1_FinalHours))
	fO_ENG2_FinalHours = round(GS_Labor_Utils.getFloat(row["Final Hrs"]) * fo2_split)
	Trace.Write('fO_ENG2_FinalHours = ' + str(fO_ENG2_FinalHours))

	salesOrgCountry = GS_Labor_Utils.getExecutionCountry(Quote)
	salesOrg = GS_Labor_Utils.getSalesOrg(row["Execution Country"])
	alternate_execution_country = Quote.GetCustomField('R2Q_Alternate_Execution_Country').Content

	if row["Execution Country"] != salesOrgCountry:
		different_salesOrg = True
		WTW_Markup_Factor = 0.1

	if row["GES Eng % Split"] not in ('0','') and row["Final Hrs"] not in ('','0') and row["GES Eng"] and row["GES Eng"] not in ('None', ''):
		parts_dict = GS_Labor_Utils.add_to_dict(parts_dict, row["GES Eng"], 'Qty', gesFinalHours)
		non_salesOrg = ""
		if row["GES Eng"].endswith("_IN") or row["GES Eng"].endswith("_RO"):
			non_salesOrg = salesOrg

		gesTPSap,gesEAC1Sap = GS_Labor_Utils.getTPandEACValueParts(Quote, non_salesOrg, row["GES Eng"],row["Execution Year"])
		Trace.Write("gesTPSap: {0}".format(gesTPSap))
		if row["GES Eng"] in gesTPSap and gesTPSap[row["GES Eng"]]:
			unit_regionalCost = GS_Labor_Utils.getFloat(gesTPSap.get(row["GES Eng"],0)) + GS_Labor_Utils.getFloat(gesEAC1Sap.get(row["GES Eng"],0))
			total_cost = GS_Labor_Utils.getFloat(round(unit_regionalCost,2) * gesFinalHours)
			GES_Eng_Unit_WTW_Cost = unit_regionalCost / (1 + GS_Labor_Utils.getFloat(row["GES_WTW_MarkupFactor"]))
			total_wtw_cost = gesFinalHours * GES_Eng_Unit_WTW_Cost
			row["GES_Unit_Regional_Cost"] = str(unit_regionalCost)
			row["GES_Regional_Cost"] = str(total_cost)
			row["GES_WTW_Cost"] = str(total_wtw_cost)
			parts_dict = GS_Labor_Utils.add_to_dict(parts_dict, row["GES Eng"], 'Cost', total_cost)
			parts_dict = GS_Labor_Utils.add_to_dict(parts_dict, row["GES Eng"], 'WTWCost', total_wtw_cost)
		else:
			row["GES_Unit_Regional_Cost"] = row["GES_Regional_Cost"] = row["GES_WTW_Cost"] = "0"
			error_flag = ""
	else:
		row["GES_Unit_Regional_Cost"] = row["GES_Regional_Cost"] = row["GES_WTW_Cost"] = "0"
	
	if fo1_split not in ('0','') and row["Final Hrs"] not in ('','0') and fo1_eng not in ('None', ''):
		parts_dict = GS_Labor_Utils.add_to_dict(parts_dict, fo1_eng, 'Qty', fo_ENG1_FinalHours)
		add_10_percent = 0.00
		Trace.Write("ebr--4--"+str([salesOrg,fo1_eng,row["Execution Year"]]))
		foPartsCost = GS_Labor_Utils.getFopartsCost(Quote, salesOrg,fo1_eng,row["Execution Year"])
		if Quote.GetCustomField('R2QFlag').Content == 'Yes':
			if fo1_eng in foPartsCost:
				if (foPartsCost[fo1_eng] in (0.00,0.0,0,None,'')):
					row["Execution Country"] = alternate_execution_country
					salesOrg = GS_Labor_Utils.getSalesOrg(alternate_execution_country)
					foPartsCost = GS_Labor_Utils.getFopartsCost(Quote, salesOrg,fo1_eng,row["Execution Year"])
			elif fo1_eng not in foPartsCost:
				row["Execution Country"] = alternate_execution_country
				salesOrg = GS_Labor_Utils.getSalesOrg(alternate_execution_country)
				foPartsCost = GS_Labor_Utils.getFopartsCost(Quote, salesOrg,fo1_eng,row["Execution Year"])

		if fo1_eng in foPartsCost and foPartsCost[fo1_eng]:
			unit_regionalCost = round(GS_Labor_Utils.getFloat(foPartsCost.get(fo1_eng,0)),2)

			if different_salesOrg: #Add 10% if execution country is different from sales org country
				add_10_percent = unit_regionalCost * 0.1

			row["FO_Eng_1_Unit_Regional_Cost"] = str(unit_regionalCost + add_10_percent)
			FO_Eng_1_Unit_WTW_Cost = GS_Labor_Utils.getFloat(row["FO_Eng_1_Unit_Regional_Cost"]) / (1 + WTW_Markup_Factor)
			fo1_total_cost = fo_ENG1_FinalHours * round(GS_Labor_Utils.getFloat(row["FO_Eng_1_Unit_Regional_Cost"]),2)
			fo1_total_wtw_cost = fo_ENG1_FinalHours * GS_Labor_Utils.getFloat(FO_Eng_1_Unit_WTW_Cost)
			parts_dict = GS_Labor_Utils.add_to_dict(parts_dict, fo1_eng, 'Cost', fo1_total_cost)
			parts_dict = GS_Labor_Utils.add_to_dict(parts_dict, fo1_eng, 'WTWCost', fo1_total_wtw_cost)

		else:
			row["FO_Eng_1_Unit_Regional_Cost"] = "0"
			fo1_total_cost = fo1_total_wtw_cost = 0.0
			error_flag = ""
	else:
		fo1_total_cost = fo1_total_wtw_cost = 0.0
		row["FO_Eng_1_Unit_Regional_Cost"] = "0"

	if fo2_split not in ('0','') and row["Final Hrs"] not in ('','0') and fo2_eng not in ('None', ''):
		parts_dict = GS_Labor_Utils.add_to_dict(parts_dict, fo2_eng, 'Qty', fO_ENG2_FinalHours)
		add_10_percent = 0.00
		foPartsCost = GS_Labor_Utils.getFopartsCost(Quote, salesOrg,fo2_eng,row["Execution Year"])
		if Quote.GetCustomField('R2QFlag').Content == 'Yes':
			if fo2_eng in foPartsCost:
				if (foPartsCost[fo2_eng] in (0.00,0.0,0,None,'')):
					row["Execution Country"] = alternate_execution_country
					salesOrg = GS_Labor_Utils.getSalesOrg(alternate_execution_country)
					foPartsCost = GS_Labor_Utils.getFopartsCost(Quote, salesOrg,ffo2_engo1_eng,row["Execution Year"])
			elif fo2_eng not in foPartsCost:
				row["Execution Country"] = alternate_execution_country
				salesOrg = GS_Labor_Utils.getSalesOrg(alternate_execution_country)
				foPartsCost = GS_Labor_Utils.getFopartsCost(Quote, salesOrg,fo2_eng,row["Execution Year"])
				
		if fo2_eng in foPartsCost and foPartsCost[fo2_eng]:
			unit_regionalCost = round(GS_Labor_Utils.getFloat(foPartsCost.get(fo2_eng,0)),2)

			if different_salesOrg: #Add 10% if execution country is different from sales org country
				add_10_percent = unit_regionalCost * 0.1

			row["FO_Eng_2_Unit_Regional_Cost"] = str(unit_regionalCost + add_10_percent)
			FO_Eng_2_Unit_WTW_Cost = GS_Labor_Utils.getFloat(row["FO_Eng_2_Unit_Regional_Cost"]) / (1 + WTW_Markup_Factor)
			fo2_total_cost = fO_ENG2_FinalHours * GS_Labor_Utils.getFloat(row["FO_Eng_2_Unit_Regional_Cost"])
			fo2_total_wtw_cost = fO_ENG2_FinalHours * GS_Labor_Utils.getFloat(FO_Eng_2_Unit_WTW_Cost)
			parts_dict = GS_Labor_Utils.add_to_dict(parts_dict, fo2_eng, 'Cost', fo2_total_cost)
			parts_dict = GS_Labor_Utils.add_to_dict(parts_dict, fo2_eng, 'WTWCost', fo2_total_wtw_cost)
		else:
			row["FO_Eng_2_Unit_Regional_Cost"] = "0"
			fo2_total_cost = fo2_total_wtw_cost = 0.0
			error_flag = ""
	else:
		fo2_total_cost = fo2_total_wtw_cost = 0.0
		try:
			row["FO_Eng_2_Unit_Regional_Cost"] = "0"
		except:
			pass

	row["FO_Regional_Cost"] = str(fo1_total_cost + fo2_total_cost)
	row["FO_WTW_Cost"] = str(fo1_total_wtw_cost + fo2_total_wtw_cost)
	row["Error_Message"] = str(error_flag)
	return parts_dict

def populate_MPA_Price(row, Product, Quote, parts_dict, fo_dict):
	if row["Final Hrs"] not in ('','0'):
		FO_ENG1_MPA = FO_ENG2_MPA = 0
		gesFinalHours = round(GS_Labor_Utils.getFloat(row["Final Hrs"]) * GS_Labor_Utils.getFloat(row["GES Eng % Split"]) / 100)
		try: #For custom deliverables
			fo1_split = GS_Labor_Utils.getFloat(row["FO Eng % Split"]) * 0.01
			fo2_split = 0.0
			fo1_eng = row.GetColumnByName('FO Eng').DisplayValue
			fo2_eng = 'None'
		except: #For standard labor deliverables
			fo1_split = GS_Labor_Utils.getFloat(row["FO Eng 1 % Split"]) * 0.01
			fo2_split = GS_Labor_Utils.getFloat(row["FO Eng 2 % Split"]) * 0.01
			fo1_eng = row.GetColumnByName('FO Eng 1').DisplayValue
			fo2_eng = row.GetColumnByName('FO Eng 2').DisplayValue

		if fo1_eng != 'None':
			fo1_eng = fo_dict.get(fo1_eng, '')
		if fo2_eng != 'None':
			fo2_eng = fo_dict.get(fo2_eng, '')

		fo_ENG1_FinalHours = round(GS_Labor_Utils.getFloat(row["Final Hrs"]) * fo1_split)
		fo_ENG2_FinalHours = round(GS_Labor_Utils.getFloat(row["Final Hrs"]) * fo2_split)

		if row["GES Eng % Split"] not in ('0',''):
			GES_Eng = row["GES Eng"]
			ges_mpaprice = GS_Labor_Utils.getMPAPrice(row, GES_Eng, Product, Quote)
			if GES_Eng in ges_mpaprice and ges_mpaprice[GES_Eng]:
				unit_mpaPrice = round(GS_Labor_Utils.getFloat(ges_mpaprice.get(GES_Eng,0)),2)
				total_mpaPrice = gesFinalHours * unit_mpaPrice
				row["GES_MPA_Price"] = str(total_mpaPrice)
				parts_dict = GS_Labor_Utils.add_to_dict(parts_dict, row["GES Eng"], 'MPA', total_mpaPrice)
			else:
				row["GES_MPA_Price"] = "0"
		else:
			row["GES_MPA_Price"] = "0"

		if fo1_split not in ('0',''): #FO_MPA_Price
			foeng1_mpa = GS_Labor_Utils.getMPAPrice(row, fo1_eng, Product, Quote)
			if fo1_eng in foeng1_mpa and foeng1_mpa[fo1_eng]:
				unit_mpaPrice = round(GS_Labor_Utils.getFloat(foeng1_mpa.get(fo1_eng,0)),2)
				FO_ENG1_MPA = unit_mpaPrice * fo_ENG1_FinalHours
				parts_dict = GS_Labor_Utils.add_to_dict(parts_dict, fo1_eng, 'MPA', FO_ENG1_MPA)

		if fo2_split not in ('0',''):
			foeng2_mpa = GS_Labor_Utils.getMPAPrice(row, fo2_eng, Product, Quote)
			if fo2_eng in foeng2_mpa and foeng2_mpa[fo2_eng]:
				unit_mpaPrice = round(GS_Labor_Utils.getFloat(foeng2_mpa.get(fo2_eng,0)),2)
				FO_ENG2_MPA = unit_mpaPrice * fo_ENG2_FinalHours
				parts_dict = GS_Labor_Utils.add_to_dict(parts_dict, fo2_eng, 'MPA', FO_ENG2_MPA)

		row["FO_MPA_Price"] = str(FO_ENG1_MPA + FO_ENG2_MPA)
	else:
		row["GES_MPA_Price"] = "0"
		row["FO_MPA_Price"] = "0"
	return parts_dict

def populateListPrice(Quote,row, salesOrg, LOB, parts_dict,TagParserQuote, fo_dict, Session): #sets List Price
	final_hours = GS_Labor_Utils.getFloat(row["Final Hrs"])
	ges_split = GS_Labor_Utils.getFloat(row["GES Eng % Split"]) * 0.01
	ges_eng = row['GES Eng']
	try: #For custom deliverables
		fo1_split = GS_Labor_Utils.getFloat(row["FO Eng % Split"]) * 0.01
		fo2_split = 0.0
		fo1_eng = row.GetColumnByName('FO Eng').DisplayValue
		fo2_eng = 'None'
	except: #For standard labor deliverables
		fo1_split = GS_Labor_Utils.getFloat(row["FO Eng 1 % Split"]) * 0.01
		fo2_split = GS_Labor_Utils.getFloat(row["FO Eng 2 % Split"]) * 0.01
		fo1_eng = row.GetColumnByName('FO Eng 1').DisplayValue
		fo2_eng = row.GetColumnByName('FO Eng 2').DisplayValue

	if fo1_eng != 'None':
		fo1_eng = fo_dict.get(fo1_eng, '')
	if fo2_eng != 'None':
		fo2_eng = fo_dict.get(fo2_eng, '')

	currentYear = DateTime.Now.Year
	year_diff = int(row["Execution Year"]) - currentYear
	gesFinalHours = round(GS_Labor_Utils.getFloat(row["Final Hrs"]) * ges_split)
	fo_ENG1_FinalHours = round(GS_Labor_Utils.getFloat(row["Final Hrs"]) * fo1_split)
	fo_ENG2_FinalHours = round(GS_Labor_Utils.getFloat(row["Final Hrs"]) * fo2_split)

	#Calcuates and sets GES List Price
	Trace.Write("final_hours={} ges_split={} ges_eng={}".format(final_hours, ges_split, ges_eng))
	if final_hours != 0 and ges_split != 0 and ges_eng != "None":
		ges_unit_price = GS_Labor_Utils.getYearPrice(Quote,year_diff, row["GES Eng"], salesOrg, LOB,TagParserQuote, Session)
		ges_total_price = round((gesFinalHours * ges_unit_price), 2)
		parts_dict = GS_Labor_Utils.add_to_dict(parts_dict, ges_eng, 'ListPrice', ges_total_price)
	else: ges_total_price = 0.0

	#Calculates and sets FO List Price
	Trace.Write("final_hours={} fo1_split={} fo1_eng={}".format(final_hours, fo1_split, fo1_eng))
	if final_hours != 0 and fo1_split != 0 and fo1_eng != "None":
		fo1_unit_price = GS_Labor_Utils.getYearPrice(Quote,year_diff, fo1_eng, salesOrg, LOB,TagParserQuote, Session)
		fo1_total_price = round((fo_ENG1_FinalHours * fo1_unit_price), 2)
		parts_dict = GS_Labor_Utils.add_to_dict(parts_dict, fo1_eng, 'ListPrice', fo1_total_price)
	else: fo1_total_price = 0.0

	if final_hours != 0 and fo2_split != 0 and fo2_eng != "None":
		fo2_unit_price = GS_Labor_Utils.getYearPrice(Quote,year_diff, fo2_eng, salesOrg, LOB,TagParserQuote, Session)
		fo2_total_price = round((fo_ENG2_FinalHours * fo2_unit_price), 2)
		parts_dict = GS_Labor_Utils.add_to_dict(parts_dict, fo2_eng, 'ListPrice', fo2_total_price) #add_to_dict is run two separate times because the service materials might be different
	else: fo2_total_price = 0.0

	fo_total_price =  fo1_total_price + fo2_total_price
	Trace.Write("FO_ListPrice={}".format(fo_total_price))
	row["FO_ListPrice"] = str(fo_total_price)
	row["GES_ListPrice"] = str(ges_total_price)
	return parts_dict