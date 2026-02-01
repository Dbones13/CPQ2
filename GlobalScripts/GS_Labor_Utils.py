#GS_Labor_Utils
from System import DateTime
import GS_GetPriceFromCPS as cps
def getFloat(Var):
	if Var:
		return float(Var)
	return 0.00

def getDefaultExecutionYear(Quote): #Finds the default execution year
	yearsList = []
	currentYear = executionYear = DateTime.Now.Year
	if not Quote:
		return currentYear
	i = 0
	while i < 4:
		year = currentYear + i
		yearsList.append(year)
		i += 1
	if Quote.GetCustomField("EGAP_Contract_Start_Date").Content != '':
		year = UserPersonalizationHelper.CovertToDate(Quote.GetCustomField("EGAP_Contract_Start_Date").Content).Year
		if year in yearsList:
			executionYear = year
		elif len(yearsList) > 0:
			executionYear = yearsList[-1] #If the start date is more than 4 years out, select the highest year in the list
	return str(executionYear)

def getPriceBookName(Quote): #Finds the pricebook names (first parent, then child)
	pricebookId = str(Quote.PricebookId)
	pricebookData = SqlHelper.GetFirst("SELECT ab.Id as childId, cd.Code as PriceBook2, ab.Code as PriceBook1 from PriceBookTableDefn ab left join PriceBookTableDefn cd on ab.ParentId = cd.Id where ab.Id = '"+pricebookId+"'")
	if pricebookData:
		return pricebookData.PriceBook1,pricebookData.PriceBook2

def getSalesOrg(country): #Not sure that we will need this. Would be used to calculate GES_Regional_Cost and LaborCost
	query = SqlHelper.GetFirst("select Execution_Country_Sales_Org from EXECUTION_COUNTRY_SALES_ORG_MAPPING where Execution_County = '{}'".format(country))
	if query is not None:
		return query.Execution_Country_Sales_Org
	else:
		return ''

def checkForMPACustomer(Quote, TagParserQuote): #Checks to see if the customer has an MPA 
	PricePlanPresent = False
	query = TagParserQuote.ParseString("select * from MPA_PRICE_PLAN_MAPPING where Honeywell_Ref = '<*CTX(Quote.CustomField(MPA Honeywell Ref))*>' and Price_Plan_Status= 'Active' and Price_Plan_Parts_Discount = 'Y' and Price_Plan_Start_Date <= '<*CTX( Date.Format(MM/dd/yyyy) )*>' and Price_Plan_End_Date >= '<*CTX( Date.Format(MM/dd/yyyy) )*>'")
	res = SqlHelper.GetList(query)
	if res and len(res) > 0:
		PricePlanPresent = True
	return PricePlanPresent


def getExecutionCountry(Quote):
	#marketCode = Quote.SelectedMarket.MarketCode
	#salesOrg = marketCode.partition('_')[0]
	#currency = marketCode.partition('_')[2]
	salesOrg = Quote.GetCustomField('Sales Area').Content
	currency = Quote.GetCustomField('Currency').Content
	if Quote.GetCustomField('R2QFlag').Content == "Yes":
		salesOrg = Quote.GetCustomField('Sales Area').Content
		currency = Quote.GetCustomField('Currency').Content
	query = SqlHelper.GetFirst("select Execution_County from NEW_EXECUTION_COUNTRY_SALES_ORG_MAPPING where Sales_Area = '{}' and Currency = '{}'".format(salesOrg,currency))
	#query = SqlHelper.GetFirst("select Execution_County from EXECUTION_COUNTRY_SALES_ORG_MAPPING where Execution_Country_Sales_Org = '{}'".format(salesOrg))
	if query is not None:
		return query.Execution_County

def laborCostWithDoubleConversion(laborcostParts, key, quoteCurrency):
	costInQuoteCurrency = laborcostParts[key]["amount"]
	#Convert cost from local currency to USD
	query = SqlHelper.GetFirst("select Exchange_Rate from Currency_ExchangeRate_Mapping where From_Currency = '{}' and To_Currency = '{}'".format(laborcostParts[key]["currency"], 'USD'))
	if query is not None:
		costInUSD = getFloat(laborcostParts[key]["amount"]) * getFloat(query.Exchange_Rate)
		#Convert cost from USD to Quote Currency
		query = SqlHelper.GetFirst("select Exchange_Rate from Currency_ExchangeRate_Mapping where From_Currency = '{}' and To_Currency = '{}'".format('USD', quoteCurrency))
		if query is not None:
			costInQuoteCurrency = getFloat(costInUSD) * getFloat(query.Exchange_Rate)
	return costInQuoteCurrency

def laborCostWithConversion(Quote, laborcostParts):
	quoteCurrency = Quote.SelectedMarket.CurrencyCode
	costWithConversion = dict()
	if laborcostParts:
		for key in laborcostParts:
			if laborcostParts[key]["currency"] != quoteCurrency:
				#Direct Conversion - if anyone of the currency is USD
				if laborcostParts[key]["currency"] == 'USD' or quoteCurrency == 'USD':
					query = SqlHelper.GetFirst("select Exchange_Rate from Currency_ExchangeRate_Mapping where From_Currency = '{}' and To_Currency = '{}'".format(laborcostParts[key]["currency"],quoteCurrency))
					costWithConversion[key] = laborcostParts[key]["amount"]
					if query is not None:
						costWithConversion[key] = getFloat(laborcostParts[key]["amount"]) * getFloat(query.Exchange_Rate)
				else:
					#Indirect Conversion - if none of the currency is USD
					costWithConversion[key] = laborCostWithDoubleConversion(laborcostParts, key, quoteCurrency)
			else:
				costWithConversion[key] = laborcostParts[key]["amount"]
	return costWithConversion

def getFopartsCost(Quote, salesOrg,partNumber,executionYear):
	executionYear = getFloat(executionYear)
	currentYear = DateTime.Now.Year
	Trace.Write("ebr--6--"+str([salesOrg,partNumber]))
	query = "Select * from HPS_LABOR_COST_DATA where Sales_Org = '{0}' and Part_Number in ('{1}')".format(salesOrg,partNumber)
	res = SqlHelper.GetFirst(query)
	if res is None and Quote.GetCustomField('R2QFlag').Content == 'Yes':
		alternate_execution_country = Quote.GetCustomField('R2Q_Alternate_Execution_Country').Content
		salesOrgr2q = getSalesOrg(alternate_execution_country)
		query = "Select * from HPS_LABOR_COST_DATA where Sales_Org = '{0}' and Part_Number in ('{1}')".format(salesOrgr2q,partNumber)
		res = SqlHelper.GetFirst(query)
	foCost = dict()
	if res is not None:
		if int(executionYear) == currentYear:
			foCost[res.Part_Number] = {"amount":res.Cost_CurrentMonth_Year1,"currency":res.Cost_Currency_Code}
		elif int(executionYear) == currentYear + 1:
			foCost[res.Part_Number] = {"amount":res.Cost_CurrentMonth_Year2,"currency":res.Cost_Currency_Code}
		elif int(executionYear) == currentYear + 2:
			foCost[res.Part_Number] = {"amount":res.Cost_CurrentMonth_Year3,"currency":res.Cost_Currency_Code}
		elif int(executionYear) == currentYear + 3:
			foCost[res.Part_Number] = {"amount":res.Cost_CurrentMonth_Year4,"currency":res.Cost_Currency_Code}
	foCostWithConversion = laborCostWithConversion(Quote, foCost)
	return foCostWithConversion


def getTPandEACValueParts(Quote, salesOrg, partNumber, executionYear):
	executionYear = getFloat(executionYear)
	currentYear = DateTime.Now.Year
	query = "Select lc.*,eac.EAC_Value,eac.Currency from HPS_LABOR_COST_DATA lc join Labor_GES_EAC_Value eac on lc.Part_Number = eac.GES_Service_Material where Sales_Org = '{0}' and Part_Number in ('{1}')".format(salesOrg, partNumber)
	res = SqlHelper.GetFirst(query)
	gesTP = dict()
	gesEAC = dict()
	if res is not None:
		#Trace.Write("-----------executionYear-----res is not None"+str(type(executionYear))+"---------currentYear:----"+str(query))
		if int(executionYear) == currentYear:
			gesTP[res.Part_Number] = {"amount":res.Cost_CurrentMonth_Year1,"currency":res.Cost_Currency_Code}
			gesEAC[res.Part_Number] = {"amount":res.EAC_Value,"currency":res.Currency}
		elif int(executionYear) == currentYear + 1:
			gesTP[res.Part_Number] = {"amount":res.Cost_CurrentMonth_Year2,"currency":res.Cost_Currency_Code}
			gesEAC[res.Part_Number] = {"amount":res.EAC_Value,"currency":res.Currency}
		elif int(executionYear) == currentYear + 2:
			gesTP[res.Part_Number] = {"amount":res.Cost_CurrentMonth_Year3,"currency":res.Cost_Currency_Code}
			gesEAC[res.Part_Number] = {"amount":res.EAC_Value,"currency":res.Currency}
		elif int(executionYear) == currentYear + 3:
			gesTP[res.Part_Number] = {"amount":res.Cost_CurrentMonth_Year4,"currency":res.Cost_Currency_Code}
			gesEAC[res.Part_Number] = {"amount":res.EAC_Value,"currency":res.Currency}

	tpWithConversion = laborCostWithConversion(Quote, gesTP)
	eacWithConversion = laborCostWithConversion(Quote, gesEAC)
	return tpWithConversion,eacWithConversion

def populateCost(Quote, row, parts_dict):
	error_flag = True
	different_salesOrg = False
	FO_Eng_1_Unit_WTW_Cost = FO_Eng_2_Unit_WTW_Cost = WTW_Markup_Factor = 0.00
	try: #For custom deliverables
		fo1_split = getFloat(row["FO Eng % Split"]) * 0.01
		fo2_split = 0.0
		#fo1_eng = row.GetColumnByName('FO Eng').DisplayValue
		fo1_eng = row.GetColumnByName('FO Eng').Value
		fo2_eng = 'None'
	except: #For standard labor deliverables
		fo1_split = getFloat(row["FO Eng 1 % Split"]) * 0.01
		fo2_split = getFloat(row["FO Eng 2 % Split"]) * 0.01
		#fo1_eng = row.GetColumnByName('FO Eng 1').DisplayValue
		fo1_eng = row.GetColumnByName('FO Eng 1').Value
		#fo2_eng = row.GetColumnByName('FO Eng 2').DisplayValue
		fo2_eng = row.GetColumnByName('FO Eng 2').Value

	gesFinalHours = round(getFloat(row["Final Hrs"]) * getFloat(row["GES Eng % Split"]) / 100)
	fo_ENG1_FinalHours = round(getFloat(row["Final Hrs"]) * fo1_split)
	fO_ENG2_FinalHours = round(getFloat(row["Final Hrs"]) * fo2_split)

	salesOrgCountry = getExecutionCountry(Quote)
	salesOrg = getSalesOrg(row["Execution Country"])

	if row["Execution Country"] != salesOrgCountry:
		different_salesOrg = True
		WTW_Markup_Factor = 0.1

	if row["GES Eng % Split"] not in ('0','') and row["Final Hrs"] not in ('','0') and row["GES Eng"] and row["GES Eng"] not in ('None', ''):
		parts_dict = add_to_dict(parts_dict, row["GES Eng"], 'Qty', gesFinalHours)
		non_salesOrg = ""
		if row["GES Eng"].endswith("_IN") or row["GES Eng"].endswith("_RO"):
			non_salesOrg = salesOrg

		gesTPSap,gesEAC1Sap = getTPandEACValueParts(Quote, non_salesOrg, row["GES Eng"],row["Execution Year"])
		if row["GES Eng"] in gesTPSap and gesTPSap[row["GES Eng"]]:
			unit_regionalCost = getFloat(gesTPSap.get(row["GES Eng"],0)) + getFloat(gesEAC1Sap.get(row["GES Eng"],0))
			total_cost = getFloat(round(unit_regionalCost,2) * gesFinalHours)
			GES_Eng_Unit_WTW_Cost = unit_regionalCost / (1 + getFloat(row["GES_WTW_MarkupFactor"]))
			total_wtw_cost = gesFinalHours * GES_Eng_Unit_WTW_Cost
			row["GES_Unit_Regional_Cost"] = str(unit_regionalCost)
			row["GES_Regional_Cost"] = str(total_cost)
			row["GES_WTW_Cost"] = str(total_wtw_cost)
			parts_dict = add_to_dict(parts_dict, row["GES Eng"], 'Cost', total_cost)
			parts_dict = add_to_dict(parts_dict, row["GES Eng"], 'WTWCost', total_wtw_cost)
		else:
			row["GES_Unit_Regional_Cost"] = row["GES_Regional_Cost"] = row["GES_WTW_Cost"] = "0"
			error_flag = ""
	else:
		row["GES_Unit_Regional_Cost"] = row["GES_Regional_Cost"] = row["GES_WTW_Cost"] = "0"

	if fo1_split not in ('0','',0) and row["Final Hrs"] not in ('','0') and fo1_eng not in ('None', ''):
		parts_dict = add_to_dict(parts_dict, fo1_eng, 'Qty', fo_ENG1_FinalHours)
		add_10_percent = 0.00
		foPartsCost = getFopartsCost(Quote, salesOrg,fo1_eng,row["Execution Year"])
		if fo1_eng in foPartsCost and foPartsCost[fo1_eng]:
			unit_regionalCost = round(getFloat(foPartsCost.get(fo1_eng,0)),2)

			if different_salesOrg: #Add 10% if execution country is different from sales org country
				add_10_percent = unit_regionalCost * 0.1

			row["FO_Eng_1_Unit_Regional_Cost"] = str(unit_regionalCost + add_10_percent)
			FO_Eng_1_Unit_WTW_Cost = getFloat(row["FO_Eng_1_Unit_Regional_Cost"]) / (1 + WTW_Markup_Factor)
			fo1_total_cost = fo_ENG1_FinalHours * getFloat(row["FO_Eng_1_Unit_Regional_Cost"])
			fo1_total_wtw_cost = fo_ENG1_FinalHours * getFloat(FO_Eng_1_Unit_WTW_Cost)
			parts_dict = add_to_dict(parts_dict, fo1_eng, 'Cost', fo1_total_cost)
			parts_dict = add_to_dict(parts_dict, fo1_eng, 'WTWCost', fo1_total_wtw_cost)

		else:
			row["FO_Eng_1_Unit_Regional_Cost"] = "0"
			fo1_total_cost = fo1_total_wtw_cost = 0.0
			error_flag = ""
	else:
		fo1_total_cost = fo1_total_wtw_cost = 0.0
		row["FO_Eng_1_Unit_Regional_Cost"] = "0"

	if fo2_split not in ('0','', 0) and row["Final Hrs"] not in ('','0') and fo2_eng not in ('None', ''):
		parts_dict = add_to_dict(parts_dict, fo2_eng, 'Qty', fO_ENG2_FinalHours)
		add_10_percent = 0.00
		foPartsCost = getFopartsCost(Quote, salesOrg,fo2_eng,row["Execution Year"])
		if fo2_eng in foPartsCost and foPartsCost[fo2_eng]:
			unit_regionalCost = round(getFloat(foPartsCost.get(fo2_eng,0)),2)

			if different_salesOrg: #Add 10% if execution country is different from sales org country
				add_10_percent = unit_regionalCost * 0.1

			row["FO_Eng_2_Unit_Regional_Cost"] = str(unit_regionalCost + add_10_percent)
			FO_Eng_2_Unit_WTW_Cost = getFloat(row["FO_Eng_2_Unit_Regional_Cost"]) / (1 + WTW_Markup_Factor)
			fo2_total_cost = fO_ENG2_FinalHours * getFloat(row["FO_Eng_2_Unit_Regional_Cost"])
			fo2_total_wtw_cost = fO_ENG2_FinalHours * getFloat(FO_Eng_2_Unit_WTW_Cost)
			parts_dict = add_to_dict(parts_dict, fo2_eng, 'Cost', fo2_total_cost)
			parts_dict = add_to_dict(parts_dict, fo2_eng, 'WTWCost', fo2_total_wtw_cost)
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

def populateListPrice(Quote,row, salesOrg, LOB, parts_dict,TagParserQuote, Session=dict()): #sets List Price
	final_hours = getFloat(row["Final Hrs"])
	ges_split = getFloat(row["GES Eng % Split"]) * 0.01
	ges_eng = row.GetColumnByName('GES Eng').DisplayValue
	try: #For custom deliverables
		fo1_split = getFloat(row["FO Eng % Split"]) * 0.01
		fo2_split = 0.0
		#fo1_eng = row.GetColumnByName('FO Eng').DisplayValue
		fo1_eng = row.GetColumnByName('FO Eng').Value
		fo2_eng = 'None'
	except: #For standard labor deliverables
		fo1_split = getFloat(row["FO Eng 1 % Split"]) * 0.01
		fo2_split = getFloat(row["FO Eng 2 % Split"]) * 0.01
		#fo1_eng = row.GetColumnByName('FO Eng 1').DisplayValue
		fo1_eng = row.GetColumnByName('FO Eng 1').Value
		#fo2_eng = row.GetColumnByName('FO Eng 2').DisplayValue
		fo2_eng = row.GetColumnByName('FO Eng 2').Value
	currentYear = DateTime.Now.Year
	year_diff = int(row["Execution Year"]) - currentYear
	gesFinalHours = round(getFloat(row["Final Hrs"]) * ges_split)
	fo_ENG1_FinalHours = round(getFloat(row["Final Hrs"]) * fo1_split)
	fo_ENG2_FinalHours = round(getFloat(row["Final Hrs"]) * fo2_split)

	#Calcuates and sets GES List Price
	if final_hours != 0 and ges_split != 0 and ges_eng != "None":
		ges_unit_price = getYearPrice(Quote,year_diff, row["GES Eng"], salesOrg, LOB,TagParserQuote,Session)
		ges_total_price = round((gesFinalHours * ges_unit_price), 2)
		row["GES_ListPrice"] = str(ges_total_price)
		parts_dict = add_to_dict(parts_dict, ges_eng, 'ListPrice', ges_total_price)
	else: ges_total_price = 0.0

	#Calculates and sets FO List Price
	if final_hours != 0 and fo1_split != 0 and fo1_eng != "None":
		fo1_unit_price = getYearPrice(Quote,year_diff, fo1_eng, salesOrg, LOB,TagParserQuote,Session)
		fo1_total_price = round((fo_ENG1_FinalHours * fo1_unit_price), 2)
		parts_dict = add_to_dict(parts_dict, fo1_eng, 'ListPrice', fo1_total_price)
	else: fo1_total_price = 0.0

	if final_hours != 0 and fo2_split != 0 and fo2_eng != "None":
		fo2_unit_price = getYearPrice(Quote,year_diff, fo2_eng, salesOrg, LOB,TagParserQuote,Session)
		fo2_total_price = round((fo_ENG2_FinalHours * fo2_unit_price), 2)
		parts_dict = add_to_dict(parts_dict, fo2_eng, 'ListPrice', fo2_total_price) #add_to_dict is run two separate times because the service materials might be different
	else: fo2_total_price = 0.0

	fo_total_price =  fo1_total_price + fo2_total_price
	row["FO_ListPrice"] = str(fo_total_price)
	return parts_dict

def convertToQuoteCurrency(Quote, value): #Converts given price/cost into the current quote currency.
	#'value' is assumed to be a dict, with at least 3 keys: 'part', 'currency', and 'amount'.
	quoteCurrency = Quote.SelectedMarket.CurrencyCode
	exchange_rate = SqlHelper.GetFirst("select Exchange_Rate from Currency_ExchangeRate_Mapping where From_Currency = '{0}' and To_Currency = '{1}'".format(value["currency"],quoteCurrency))
	if exchange_rate is not None:
		converted_value = getFloat(value["amount"]) * getFloat(exchange_rate.Exchange_Rate)
	else:
		converted_value = value["amount"]
	Trace.Write("original_currency: {0}, original_value: {1}, converted_value: {2}, Part Number: {3}".format(value["currency"], exchange_rate.Exchange_Rate, converted_value, value["part"]))
	return converted_value

def getPrice(Quote,part_num,TagParserQuote, Session=dict()): #Looks up the price in the pricebook
	remainingParts = []
	effectiveDate = Quote.EffectiveDate.Date.ToString("MM/dd/yyyy")
	entitlement = Quote.GetCustomField("Entitlement").Content
	salesOrg = Quote.GetCustomField('Sales Area').Content
	currency = Quote.GetCustomField('Currency').Content
	priceType = 'SF' if 'Flex' in entitlement else 'SP'
	if entitlement:
		Trace.Write("PriceBook Present")
		query = ("Select Amount, PartNumber from HPS_SESP_DATA where PartNumber = '{0}' and Price_Type = '{1}' and Sales_Org = '{2}' and Currency = '{3}' and Valid_from <= '{4}' and Valid_to >= '{4}'").format(part_num,priceType,salesOrg,currency,effectiveDate)
		price = SqlHelper.GetFirst(query)
		if price: 
			return price.Amount
	res = cps.getPrice(Quote,{},[part_num],TagParserQuote,Session)
	if res.get(part_num) is not None:
		return res[part_num]
	return '' #Only returns blank string if no price is found earlier

def getYearPrice(Quote,power, partnumber, salesOrg, LOB,TagParserQuote, Session=dict()): #Needs the quote for the pricebook call
	query = "Select * from YOY_INFLATION_RATE where salesOrg = '{0}' and LOB = '{1}'".format(salesOrg,LOB)
	res = SqlHelper.GetFirst(query)
	listPrice = getPrice(Quote, partnumber,TagParserQuote, Session)
	if power == 1 and res is not None:
		inflationRate1 = float(res.Inflation_Rate)
		price = getFloat(listPrice) * getFloat(1 + inflationRate1 )
	elif power==2 and res is not None:
		inflationRate1 = float(res.Inflation_Rate)
		inflationRate2 = float(res.Inflation_Rate_Year2)
		price = getFloat(listPrice) * getFloat(1 + inflationRate1 ) * getFloat(1 + inflationRate2 )
	elif power==3 and res is not None:
		inflationRate1 = float(res.Inflation_Rate)
		inflationRate2 = float(res.Inflation_Rate_Year2)
		inflationRate3 = float(res.Inflation_Rate_Year3)
		price = getFloat(listPrice) * getFloat(1 + inflationRate1 ) * getFloat(1 + inflationRate2 ) * getFloat(1 + inflationRate3 )
	else:
		price =  getFloat(listPrice)
	if price:
		#Trace.Write(price)
		return price
	if listPrice:
		 return getFloat(listPrice)
	return 0.0

def getLaborCost(part_num, Quote): #Gets the labor cost - no currency conversion
	salesOrg = Quote.GetCustomField("Sales Area").Content #Does this need to change to dynamic based on row's execution country?
	executionYear = getDefaultExecutionYear(Quote)
	currentYear = DateTime.Now.Year
	cost = {"part": part_num, "amount":0,"currency":"USD"} #default to 0
	query = "Select * from HPS_LABOR_COST_DATA where Sales_Org = '{0}' and Part_Number = '{1}' ".format(salesOrg, part_num)
	res = SqlHelper.GetFirst(query)
	if res is not None:
		if executionYear == currentYear:
			cost = {"part": part_num, "amount":res.Cost_CurrentMonth_Year1,"currency":res.Cost_Currency_Code}
		elif executionYear == currentYear + 1:
			cost = {"part": part_num, "amount":res.Cost_CurrentMonth_Year2,"currency":res.Cost_Currency_Code}
		elif executionYear == currentYear + 2:
			cost = {"part": part_num, "amount":res.Cost_CurrentMonth_Year3,"currency":res.Cost_Currency_Code}
		elif executionYear == currentYear + 3:
			cost = {"part": part_num, "amount":res.Cost_CurrentMonth_Year4,"currency":res.Cost_Currency_Code}
	return cost

def getTPandEACCost(part_num, executionYear): #Gets the TP and EAC Cost for the part number    
	currentYear = DateTime.Now.Year
	tp_cost = {"part": part_num, "amount":0,"currency":"USD"} #default to 0
	eac_cost = {"part": part_num, "amount":0,"currency":"USD"} #default to 0

	if part_num.endswith("_IN") or part_num.endswith("_RO"):
		salesOrg = Quote.GetCustomField("Sales Area").Content
	elif part_num.endswith("_CN") or part_num.endswith("_UZ"):
		salesOrg = ''

	query = "Select lc.*,eac.EAC_Value,eac.Currency from HPS_LABOR_COST_DATA lc join Labor_GES_EAC_Value eac on lc.Part_Number = eac.GES_Service_Material where Sales_Org = '{0}' and Part_Number = '{1}')".format(salesOrg, part_num)
	res = SqlHelper.GetList(query)

	if res is not None:
		if executionYear == currentYear:
			tp_cost = {"part": part_num, "amount":res.Cost_CurrentMonth_Year1, "currency":res.Cost_Currency_Code}
		elif executionYear == currentYear + 1:
			tp_cost = {"part": part_num, "amount":res.Cost_CurrentMonth_Year2, "currency":res.Cost_Currency_Code}
		elif executionYear == currentYear + 2:
			tp_cost = {"part": part_num, "amount":res.Cost_CurrentMonth_Year3, "currency":res.Cost_Currency_Code}
		elif executionYear == currentYear + 3:
			tp_cost = {"part": part_num, "amount":res.Cost_CurrentMonth_Year4, "currency":res.Cost_Currency_Code}
		eac_cost = {"part": part_num, "amount":res.EAC_Value, "currency":res.Currency}

	return tp_cost, eac_cost



def getMPAPrice(row, part_num, Product, Quote): #Gets the MPA price
	LaborHrs_Products=["PRMS Skid Engineering","Public Address General Alarm System","Tank Gauging Engineering","Metering Skid Engineering","Gas MeterSuite Engineering - C300 Functions","Industrial Security (Access Control)","Fire Detection & Alarm Engineering","MS Analyser System Engineering","MeterSuite Engineering - MSC Functions","One Wireless System","Fire and Gas Consultancy Service","Liquid MeterSuite Engineering - C300 Functions","Process Safety Workbench Engineering"]
	getMPA = dict()
	booking_country = Quote.GetCustomField('Booking Country').Content #row["Execution Country"]
	honeywellRef = Quote.GetCustomField('MPA Honeywell Ref').Content #"1-CUN51UZ"#We believe this shouldn't be hardcoded <*CTX(Quote.CustomField(MPA Honeywell Ref))*><*CTX( Quote.CustomField(Booking Country) )*>
	#totalManHours = round(float(Product.GetContainerByName(row.ParentContainer.Name).TotalRow['Final Hrs']))
	#try:
	if Product.PartNumber in LaborHrs_Products:
		totalManHours = (int(Product.Attr('Total_Labor_Hrs').GetValue())+int(Product.Attr('Final_Hrs').GetValue())) if Product.Attr('Final_Hrs').GetValue() not in ('0', 0, '') else "-1"
	else:
		totalManHours = int(Product.Attr('Total_Project_Hrs').GetValue()) if Product.Attr('Total_Project_Hrs').GetValue() not in ('0', 0, '') else "-1"
	#except:
		#totalManHours = ""

	query = "SELECT Unit_MPA_Price,Currency,Service_Material FROM GES_MPA_PRICE WHERE Booking_Country = '{0}' and cast(Minimum_MH as float) <= {1} and cast(Maximum_MH as float)> {1} and Service_Material = '{2}' and HoneywellRef = '{3}' ".format(booking_country,totalManHours,part_num,honeywellRef)

	res = SqlHelper.GetFirst(query)

	if res is not None and res.Unit_MPA_Price:
		getMPA[res.Service_Material] = {"amount":res.Unit_MPA_Price,"currency":res.Currency}

	MPAWithConversion = laborCostWithConversion(Quote, getMPA)

	return MPAWithConversion

def populate_MPA_Price(row, Product, Quote, parts_dict):
	if row["Final Hrs"] not in ('','0'):
		FO_ENG1_MPA = FO_ENG2_MPA = 0
		gesFinalHours = round(getFloat(row["Final Hrs"]) * getFloat(row["GES Eng % Split"]) / 100)
		try: #For custom deliverables
			fo1_split = getFloat(row["FO Eng % Split"]) * 0.01
			fo2_split = 0.0
			#fo1_eng = row.GetColumnByName('FO Eng').DisplayValue
			fo1_eng = row.GetColumnByName('FO Eng').Value
			fo2_eng = 'None'
		except: #For standard labor deliverables
			fo1_split = getFloat(row["FO Eng 1 % Split"]) * 0.01
			fo2_split = getFloat(row["FO Eng 2 % Split"]) * 0.01
			#fo1_eng = row.GetColumnByName('FO Eng 1').DisplayValue
			fo1_eng = row.GetColumnByName('FO Eng 1').Value
			#fo2_eng = row.GetColumnByName('FO Eng 2').DisplayValue
			fo2_eng = row.GetColumnByName('FO Eng 2').Value
		fo_ENG1_FinalHours = round(getFloat(row["Final Hrs"]) * fo1_split)
		fo_ENG2_FinalHours = round(getFloat(row["Final Hrs"]) * fo2_split)

		if row["GES Eng % Split"] not in ('0',''):
			GES_Eng = row.GetColumnByName('GES Eng').DisplayValue
			ges_mpaprice = getMPAPrice(row, GES_Eng, Product, Quote)
			if GES_Eng in ges_mpaprice and ges_mpaprice[GES_Eng]:
				unit_mpaPrice = round(getFloat(ges_mpaprice.get(GES_Eng,0)),2)
				total_mpaPrice = gesFinalHours * unit_mpaPrice
				row["GES_MPA_Price"] = str(total_mpaPrice)
				parts_dict = add_to_dict(parts_dict, row["GES Eng"], 'MPA', total_mpaPrice)
			else:
				row["GES_MPA_Price"] = "0"
		else:
			row["GES_MPA_Price"] = "0"

		if fo1_split not in ('0',''): #FO_MPA_Price
			foeng1_mpa = getMPAPrice(row, fo1_eng, Product, Quote)
			if fo1_eng in foeng1_mpa and foeng1_mpa[fo1_eng]:
				unit_mpaPrice = round(getFloat(foeng1_mpa.get(fo1_eng,0)),2)
				FO_ENG1_MPA = unit_mpaPrice * fo_ENG1_FinalHours
				parts_dict = add_to_dict(parts_dict, fo1_eng, 'MPA', FO_ENG1_MPA)

		if fo2_split not in ('0',''):
			foeng2_mpa = getMPAPrice(row, fo2_eng, Product, Quote)
			if fo2_eng in foeng2_mpa and foeng2_mpa[fo2_eng]:
				unit_mpaPrice = round(getFloat(foeng2_mpa.get(fo2_eng,0)),2)
				FO_ENG2_MPA = unit_mpaPrice * fo_ENG2_FinalHours
				parts_dict = add_to_dict(parts_dict, fo2_eng, 'MPA', FO_ENG2_MPA)

		row["FO_MPA_Price"] = str(FO_ENG1_MPA + FO_ENG2_MPA)
	else:
		row["GES_MPA_Price"] = "0"
		row["FO_MPA_Price"] = "0"
	return parts_dict

def calcLaborPriceCost(Quote, Product): #Not sure if we'll use this yet. It would run all the calculations, and return the values to be loaded into the container.
	return dict()

def add_to_dict(parts_dict, part_num, column_name, unit_value): #Column name doesn't differiate between FO/GES. Valid names are Qty, Cost, ListPrice, WTWCost, and MPA.
	#Sample of the dictionary layout:
	#parts_dict = {"HPS_SYS_LE1_P305": {"GES_ListPrice": 3214, "GES_Cost": 45}, 
	#              "HPS_SYS_LE1_P300": { "GES_Cost": 45} }

	if part_num in parts_dict:
		part_info = parts_dict[part_num]
		if column_name in part_info:
			part_info[column_name] += unit_value
		else:
			part_info[column_name] = unit_value
	else:
		parts_dict[part_num] = {column_name: unit_value}
	return parts_dict

def populatePriceCost(Product, parts_dict): #Populates the pricing and costing container from the dictionary. This container will be used to add line items to cart
	cont = Product.GetContainerByName('Labor_PriceCost_Cont')
	cont.Clear()
	for part in parts_dict:
		part_info = parts_dict[part]
		if part and getFloat(part_info.get("Qty",0)) != 0.0:
			new_row = cont.AddNewRow(part,False)
			if new_row is not None:
				Trace.Write("--new_row-"+str(new_row))
				new_row['Part Number'] = part
				Qty=part_info.get("Qty",0)
				Qty_ref=(new_row.GetColumnByName("Qty").ReferencingAttribute.AssignValue(str(Qty)))
				new_row['Total Cost'] = (str(part_info['Cost'])) if 'Cost' in part_info else '0.0'
				new_row['Total List Price'] = (str(part_info['ListPrice'])) if 'ListPrice' in part_info else '0.0'
				new_row['Total WTW Cost'] = (str(part_info['WTWCost'])) if 'WTWCost' in part_info else '0.0'
				new_row['Total MPA Price'] = (str(part_info['MPA'])) if 'MPA' in part_info else '0.0'
				new_row.Calculate()