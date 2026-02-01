def getFloat(v):
	if v:
		return float(v)
	return 0

def getContainer(prod, conName):
	return prod.GetContainerByName(conName)

def updateAttrDictWithCustomXpm(product, attrValDict,Quote, sespType):
	con = getContainer(product, "ENB_Migration_Config_Cont")
	ENB_K4_processor_boards_Non_Redundant_config = 0
	ENB_K4_processor_boards_Redundant_config = 0
	for row in con.Rows:
		if row["xPM_Does_the_customer_have_K4_processor_boards"] == "No" and row["xPM_What_is_the_NIM_migration_scenario"] == "Non Redundant NIM to ENB":
			ENB_K4_processor_boards_Non_Redundant_config += getFloat(row["xPM_Number_of_NIMs_in_this_config"])
		if row["xPM_Does_the_customer_have_K4_processor_boards"] == "No" and row["xPM_What_is_the_NIM_migration_scenario"] == "Redundant NIM to ENB":
			ENB_K4_processor_boards_Redundant_config += getFloat(row["xPM_Number_of_NIMs_in_this_config"]) * 2
	attrValDict["ENB_K4_processor_boards_Non_Redundant_config"] = ENB_K4_processor_boards_Non_Redundant_config
	attrValDict["ENB_K4_processor_boards_Redundant_config"] = ENB_K4_processor_boards_Redundant_config

	if getContainer(product, "xPM_Migration_Scenario_Cont"):
		isC300Mig = getContainer(product, "xPM_Migration_Scenario_Cont").Rows[0]["xPM_Select_the_migration_scenario"] == "xPM to C300PM"
	else:
		isC300Mig = product.Attr("xPM_Select_the_migration_scenario").GetValue() == "xPM to C300PM"
	total_xpm_points = 0
	total_exp_conn = 0
	migCon = getContainer(product, "xPM_Migration_Config_Cont")
	if isC300Mig and sespType in ("No", ""):
		for row in migCon.Rows:
			xPM_config = getFloat(row["xPM_Number_of_xPMs_in_this_config"])
			total_xpm_points += (getFloat(row["xPM_Number_of_xPM_Points_including_SI"]) * xPM_config)
	if isC300Mig and sespType in ("Yes") :
		scenarioList = ['HPM', 'EHPM']
		for row in migCon.Rows:
			xPM_config = getFloat(row["xPM_Number_of_xPMs_in_this_config"])
			multiplier = 2200 if any(scenario in row["xPM_Migration_Scenario"] for scenario in scenarioList) else 1000
			if ((getFloat(row["xPM_Number_of_xPM_Points_including_SI"] ) * xPM_config) - (xPM_config * multiplier)) > 0:
				total_xpm_points += ((getFloat(row["xPM_Number_of_xPM_Points_including_SI"] ) * xPM_config) - (xPM_config * multiplier))
	if not isC300Mig:
		for row in migCon.Rows:
			total_exp_conn += getFloat(row["xPM_How_many_EHPMs_will_require_Exp_conn"])
	attrValDict["xPM_Total_xPM_require_exp_conn"] = total_exp_conn
	attrValDict["xPM_Total_xPM_Points_Including_SI"] = total_xpm_points
	attrValDict["SESP_TYPE"] = sespType

	con = getContainer(product, "xPM_Network_Upgrade_Cont")
	res = 0
	if con:
		for row in con.Rows:
			res += getFloat(row["xPM_Qty_of_Red_pair_of_CF9_firewalls"])
			res += getFloat(row["xPM_Qty_Additional_Red_pair_of_CF9_firewalls"])
	else:
		res += getFloat(product.Attr("ATT_QRPCF9IOTA").GetValue())
		res += getFloat(product.Attr("ATT_QARPCF9IOTA").GetValue())
	attrValDict["xpm_Optic_Extender_needed"] = "true" if res > 0 else "false"

def populateWriteInsTPAPMD(product):
	writeInData = dict()
	msid= product.Attr('MSID').GetValue()
	sysNumber= product.Attr('System Number').GetValue()
	area = str(msid) +" - "+ str(sysNumber)
	third_party =getContainer(product,'TPA_Third_Party_Items_Cont')
	for x in third_party.Rows:
		if x["WriteIn"] not in ['Extended warranty for servers']:
			if x["Display_Flag"]  in [0, "0"] and getFloat(x["Unit_Price"]) >0 and getFloat(x["Unit_Cost"])>0 and getFloat(x["Final_Qty"])>0:
				writeInData[x["WriteIn"]] = [x["Unit_Price"],x["Unit_Cost"],x["WriteIn_Type"],x["Final_Qty"], area]
		else:
			if getFloat(x["Final_Qty"])>0:
					writeInData[x["WriteIn"]] = [x["Unit_Price"],x["Unit_Cost"],x["WriteIn_Type"],x["Final_Qty"], area]

	if product.Attr("MIgration_Scope_Choices").GetValue() not in ["LABOR"]:
		'''productContainer = product.GetContainerByName("MSID_Product_Container")
		productRow = productContainer.Rows.GetByColumnName("Product Name", "TPA/PMD Migration")
		prod = productRow.Product'''
		con = product.GetContainerByName("WriteInProduct")
		if con.Rows.Count > 0:
			con.Clear()
		for wi, wiData in writeInData.items():
			row = con.AddNewRow()
			row.Product.Attr("Selected_WriteIn").AssignValue(wiData[2])
			row.Product.Attr("Price").AssignValue(str(wiData[0]))
			row.Product.Attr("Cost").AssignValue(str(wiData[1]))
			row.Product.Attr("QI_Area").AssignValue(wiData[4])
			row.Product.Attr("ItemQuantity").AssignValue(wiData[3])
			row.Product.Attr("Extended Description").AssignValue(str(wi))
			row.Product.ApplyRules()
			row.ApplyProductChanges()
			row.Calculate()
	else:
		'''productContainer = product.GetContainerByName("MSID_Product_Container")
		productRow = productContainer.Rows.GetByColumnName("Product Name", "TPA/PMD Migration")
		prod = productRow.Product'''
		con = product.GetContainerByName("WriteInProduct")
		if con.Rows.Count > 0:
			con.Clear()
	con.Calculate()

def populateCBECwritein(product):
	writeInData = dict()
	msid= product.Attr('MSID').GetValue()
	sysNumber= product.Attr('System Number').GetValue()
	area = str(msid) +" - "+ str(sysNumber)
	thirdPartyCost = '0'
	thirdPartyPrice = '0'
	ext_des=''
	#writeInData["Write-in Third Party Hardware Misc"] = [str(thirdPartyPrice), str(thirdPartyCost), ""]
	con = getContainer(product, "CB_EC_Third_party_items_Cont")
	for row in con.Rows:
		thirdPartyCost=row["CB_EC_Cost"] if row["CB_EC_Cost"] is None or str(row["CB_EC_Cost"]) != '' else '0'
		thirdPartyPrice=row["CB_EC_Price"] if row["CB_EC_Price"] is None or str(row["CB_EC_Price"]) != '' else '0'
		ext_des=row["CB_EC_Extended_Description"]
		break

	writeInData["Write-in Third Party Hardware Misc"]=[thirdPartyPrice,thirdPartyCost,ext_des, area]
	if float(thirdPartyPrice) > 0  and float(thirdPartyCost)> 0:
		'''productContainer = product.GetContainerByName("MSID_Product_Container")
		productRow = productContainer.Rows.GetByColumnName("Product Name", "CB-EC Upgrade to C300-UHIO")
		prod = productRow.Product'''
		con1 = product.GetContainerByName("WriteInProduct")
		con1.Rows.Clear()
		for wi, wiData in writeInData.items():
			if con1.Rows.Count == 0:
				row = con1.AddNewRow()
				row.Product.Attr("Selected_WriteIn").AssignValue(wi)
				row.Product.Attr("Price").AssignValue(wiData[0])
				row.Product.Attr("Cost").AssignValue(wiData[1])
				row.Product.Attr("QI_Area").AssignValue(wiData[3])
				row.Product.Attr("ItemQuantity").AssignValue("1")
				row.Product.Attr("Extended Description").AssignValue(wiData[2])
				row.Product.ApplyRules()
				row.ApplyProductChanges()
				row.Calculate()
		con1.Calculate()