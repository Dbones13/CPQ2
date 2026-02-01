import GS_GetPriceFromCPS as cps
import GS_Labor_Utils
def updateLaborCostPrice(Product, Quote, TagParserQuote, conList, Session=dict()):
	salesOrg = Quote.SelectedMarket.MarketCode.split('_')[0]
	LOB = Quote.GetCustomField("Booking LOB").Content
	listPriceDict = dict()

	for cont in conList:
		laborCont = Product.GetContainerByName(cont)
		if laborCont.Rows.Count > 0:
			partList = getUniqueParts(laborCont)
			if len(partList) > 0:
				listPriceDict = cps.getPrice(Quote, {}, partList, TagParserQuote, Session)
				Trace.Write("listPriceDict --> "+str(listPriceDict))

			for row in laborCont.Rows:
				try:
					populateCost(Quote, row)
				except Exception,e:
					msg = "Error when Calculating Cost: {0}, Line Number: {1}".format(e, '82')
					Trace.Write(msg)
				try:
					populateListPrice(Quote, row, listPriceDict)
				except Exception,e:
					msg = "Error when Calculating ListPice: {0}, Line Number: {1}".format(e, '87')
					Trace.Write(msg)
			laborCont.Calculate()

		#Populate Price Cost Container
		#populatePriceCost(Product)

def getUniqueParts(laborCont, partList = []):
	for row in laborCont.Rows:
		if row['LaborResource'] != '':
			if row['LaborResource'] not in partList:
				partList.append(row['LaborResource'])

	return partList
def populateCost(Quote, row):
	different_salesOrg = False
	WTW_Markup_Factor = 0.00

	serviceMaterial = row["LaborResource"]
	finalHours = GS_Labor_Utils.getFloat(row["FinalHours"])
	salesOrg = GS_Labor_Utils.getSalesOrg(row["ExecutionCountry"])

	if finalHours != 0 and serviceMaterial != 'None':
		unitRegionalCost = unitWTWCost = 0
		if 'GES'in serviceMaterial:  #GES parts
			#Trace.Write("Running GES Part Logic")
			non_salesOrg = ""
			if serviceMaterial.endswith("_IN") or serviceMaterial.endswith("_RO"):
				non_salesOrg = salesOrg
			gesTPSap, gesEAC1Sap = GS_Labor_Utils.getTPandEACValueParts(Quote, non_salesOrg, serviceMaterial, row["ExecutionYear"])
			#Trace.Write("gesTPSap --> "+str(gesTPSap))
			#Trace.Write("gesEAC1Sap --> "+str(gesEAC1Sap))
			if serviceMaterial in gesTPSap and gesTPSap[serviceMaterial]:
				unitRegionalCost = round(GS_Labor_Utils.getFloat(gesTPSap.get(serviceMaterial,0)) + GS_Labor_Utils.getFloat(gesEAC1Sap.get(serviceMaterial,0)), 2)
				try:
					WTW_Markup_Factor = SqlHelper.GetFirst("SELECT WTWMarkupFactorEstimated FROM LABOR_GES_WTW_MARKUP_FACTOR WHERE GES_Service_Material = '{}'".format(serviceMaterial)).WTWMarkupFactorEstimated
				except:
					pass
				unitWTWCost = round(unitRegionalCost / (1 + GS_Labor_Utils.getFloat(WTW_Markup_Factor)), 2)
		else:  #FO parts
			#Trace.Write("Running FO Part Logic")
			salesOrgCountry = GS_Labor_Utils.getExecutionCountry(Quote)
			if row["ExecutionCountry"] != salesOrgCountry:
				different_salesOrg = True
				WTW_Markup_Factor = 0.1
			foPartsCost = GS_Labor_Utils.getFopartsCost(Quote, salesOrg, serviceMaterial, row["ExecutionYear"])
			#Trace.Write("foPartsCost --> "+str(foPartsCost))
			if serviceMaterial in foPartsCost and foPartsCost[serviceMaterial]:
				unitRegionalCost = round(GS_Labor_Utils.getFloat(foPartsCost.get(serviceMaterial,0)), 2)
				if different_salesOrg:
					add_10_percent = unitRegionalCost * 0.1
					unitRegionalCost = unitRegionalCost + add_10_percent
				unitWTWCost = round(unitRegionalCost / (1 + WTW_Markup_Factor), 2)

		totalCost = unitRegionalCost * finalHours
		totalWTWCost = unitWTWCost * finalHours
		row["TransferCost"] = str(unitRegionalCost)
		#row["Regional_Cost"] = str(totalCost)
		row["W2WCost"] = str(unitWTWCost)
		#row["WTW_Cost"] = str(totalWTWCost)
	else:
		row["TransferCost"] = "0" #row["Regional_Cost"] = "0" #row["WTW_Cost"] = "0"
	row.Calculate()
def getYearPrice(power, partNumber, salesOrg, LOB, listPriceDict): #Needs the quote for the pricebook call
	query = "Select * from YOY_INFLATION_RATE where salesOrg = '{0}' and LOB = '{1}'".format(salesOrg,LOB)
	res = SqlHelper.GetFirst(query)
	price = listPriceDict.get(partNumber, 0)
	if power ==1 and res is not None:
		inflationRate1 = GS_Labor_Utils.getFloat(res.Inflation_Rate)
		price = GS_Labor_Utils.getFloat(price) * GS_Labor_Utils.getFloat((1 + inflationRate1 ))
	elif power == 2 and res is not None :
		inflationRate1 = GS_Labor_Utils.getFloat(res.Inflation_Rate)
		inflationRate2 = GS_Labor_Utils.getFloat(res.Inflation_Rate_Year2)
		price = GS_Labor_Utils.getFloat(price) * GS_Labor_Utils.getFloat((1 + inflationRate1 ))*GS_Labor_Utils.getFloat((1 + inflationRate2))
	elif power == 3 and res is not None:
		inflationRate1 = GS_Labor_Utils.getFloat(res.Inflation_Rate)
		inflationRate2 = GS_Labor_Utils.getFloat(res.Inflation_Rate_Year2)
		inflationRate3 = GS_Labor_Utils.getFloat(res.Inflation_Rate_Year3)
		price = GS_Labor_Utils.getFloat(price) * GS_Labor_Utils.getFloat((1 + inflationRate1 ))*GS_Labor_Utils.getFloat((1 + inflationRate2))*GS_Labor_Utils.getFloat((1 + inflationRate3))
	if price:
		return GS_Labor_Utils.getFloat(price)
	return 0.0
def populateListPrice(Quote, row, listPriceDict): #sets List Price
	salesOrg = Quote.SelectedMarket.MarketCode.split('_')[0]
	LOB = Quote.GetCustomField("Booking LOB").Content
	serviceMaterial = row["LaborResource"]
	finalHours = GS_Labor_Utils.getFloat(row["FinalHours"])

	currentYear = DateTime.Now.Year
	year_diff = int(row["ExecutionYear"]) - currentYear

	if finalHours != 0 and serviceMaterial != "None":
		unitListPrice = getYearPrice(year_diff, serviceMaterial, salesOrg, LOB, listPriceDict)
		totalListPrice = round((finalHours * unitListPrice), 2)
		row["UnitListPrice"] = str(unitListPrice)
		row["TotalListPrice"] = str(totalListPrice)
conList = ['AR_HCI_LABOR_CONTAINER']
updateLaborCostPrice(Product, Quote, TagParserQuote, conList, Session=dict())
a = Session['LaborPricesDict']
Trace.Write("Session['LaborPricesDict']---->"+str(Session['LaborPricesDict']))