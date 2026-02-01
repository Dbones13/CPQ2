isR2Qquote = True if Quote.GetCustomField("isR2QRequest").Content else False
if isR2Qquote:
	from System import DateTime
	from GS_GetPriceFromCPS import getPrice

	def getContainer(Product, Name):
		return Product.GetContainerByName(Name)

	def getCfValue(Name):
		return Quote.GetCustomField(Name).Content

	def getFloat(Var):
		if Var:
			return float(Var)
		return 0

	def checkForMPACustomer():
		PricePlanPresent = False
		query = TagParserQuote.ParseString("select * from MPA_PRICE_PLAN_MAPPING where Honeywell_Ref = '<*CTX(Quote.CustomField(MPA Honeywell Ref))*>' and Honeywell_Ref ! = '' and Price_Plan_Status= 'Active' and Price_Plan_Parts_Discount = 'Y' and Price_Plan_Start_Date < '<*CTX( Date.Format(MM/dd/yyyy) )*>' and Price_Plan_End_Date > '<*CTX( Date.Format(MM/dd/yyyy) )*>'")
		res = SqlHelper.GetList(query)
		if res and len(res) > 0:
			PricePlanPresent = True
		return PricePlanPresent

	def getDefaultExecutionYear():
		executionYear = str(DateTime.Now.Year )
		yearsList = []
		currentYear = DateTime.Now.Year
		i = 0
		while i < 4:
			year = currentYear + i
			yearsList.append(year)
			i += 1

		if getCfValue("EGAP_Contract_Start_Date") != '':
			year = UserPersonalizationHelper.CovertToDate(getCfValue("EGAP_Contract_Start_Date")).Year
			if year in yearsList:
				executionYear = year
			else:
				executionYear = yearsList[-1] if len(yearsList) > 0 else str(DateTime.Now.Year )
		return executionYear

	def GetPrice(partsList):
		PriceData = dict()
		remainingParts = []
		effectiveDate = Quote.EffectiveDate.Date.ToString("MM/dd/yyyy")
		if entitlement:
			priceType = 'SF' if 'Flex' in entitlement else 'SP'
			query = ("Select Amount, PartNumber from HPS_SESP_DATA where PartNumber In ('{0}') and Price_Type = '{1}' and Sales_Org = '{2}' and Currency = '{3}' and Valid_from <= '{4}' and Valid_to >= '{4}'").format("','".join(partsList),priceType,salesOrg,currency,effectiveDate)
			PriceOfParts = SqlHelper.GetList(query)
			if PriceOfParts:
				for part in PriceOfParts:
					PriceData[part.PartNumber] = part.Amount if part.Amount else ''
			for part in partsList:
				if part not in PriceData.keys():
					remainingParts.append(part)
			if len(remainingParts) > 0:
				PriceData = getPrice(Quote,PriceData,remainingParts,TagParserQuote,Session)
		else:
			PriceData = getPrice(Quote,PriceData,partsList,TagParserQuote,Session)
		return PriceData

	def laborCostWithoutConversion(partsList,executionYear):
		salesOrg = getExecutionCountrySalesOrg()
		laborcostParts = dict()
		query = "Select * from HPS_LABOR_COST_DATA where Sales_Org = '{0}' and Part_Number in ('{1}')".format(salesOrg, "','".join(partsList))
		res = SqlHelper.GetList(query)
		if res is not None:
			for i in res:
				#laborcostParts[i.Part_Number] = {"cost":i.Cost_CurrentMonth_Year1,"stdcurrency":i.Cost_Currency_Code}
				if executionYear == str(DateTime.Now.Year ):
					laborcostParts[i.Part_Number] = {"cost":i.Cost_CurrentMonth_Year1,"stdcurrency":i.Cost_Currency_Code}
				elif executionYear == str(DateTime.Now.Year  + 1):
					laborcostParts[i.Part_Number] = {"cost":i.Cost_CurrentMonth_Year2,"stdcurrency":i.Cost_Currency_Code}
				elif executionYear == str(DateTime.Now.Year  + 2):
					laborcostParts[i.Part_Number] = {"cost":i.Cost_CurrentMonth_Year3,"stdcurrency":i.Cost_Currency_Code}
				elif executionYear == str(DateTime.Now.Year  + 3):
					laborcostParts[i.Part_Number] = {"cost":i.Cost_CurrentMonth_Year4,"stdcurrency":i.Cost_Currency_Code}
		return laborcostParts

	def laborCostWithCOnversion(laborcostParts):
		quoteCurrency = Quote.SelectedMarket.CurrencyCode
		costWithConversion = dict()
		if laborcostParts:
			for key in laborcostParts:
				if quoteCurrency == "USD" or laborcostParts[key]["stdcurrency"] == "USD":
					query = SqlHelper.GetFirst("select Exchange_Rate from Currency_ExchangeRate_Mapping where From_Currency = '{}' and To_Currency = '{}'".format(laborcostParts[key]["stdcurrency"],quoteCurrency))
					costWithConversion[key] = getFloat(laborcostParts[key]["cost"]) * getFloat(query.Exchange_Rate)
				else:
					factor = 1.00
					query1 = SqlHelper.GetFirst("select Exchange_Rate from Currency_ExchangeRate_Mapping where From_Currency = '{}' and To_Currency = '{}'".format(laborcostParts[key]["stdcurrency"],'USD'))
					if query1 is not None:
						factor = factor * getFloat(query1.Exchange_Rate)
						queryUSD = SqlHelper.GetFirst("select Exchange_Rate from Currency_ExchangeRate_Mapping where From_Currency = '{}' and To_Currency = '{}'".format('USD',quoteCurrency))
						if queryUSD is not None:
							factor = factor * getFloat(queryUSD.Exchange_Rate)
						else:
							factor = 1.00
					costWithConversion[key] = getFloat(laborcostParts[key]["cost"]) * factor
		return costWithConversion
	def getExecutionCountrySalesOrg():
		#marketCode = Quote.SelectedMarket.MarketCode
		
		salesOrg = Quote.GetCustomField('Sales Area').Content
		currency = Quote.GetCustomField('Currency').Content
		query = SqlHelper.GetFirst("select Execution_Country_Sales_Org from NEW_EXECUTION_COUNTRY_SALES_ORG_MAPPING where Sales_Area = '{}' and Currency = '{}'".format(salesOrg,currency))
		if query is not None:
			return query.Execution_Country_Sales_Org

	def getTPandEACValueSapParts(gesParts,executionYear):
		salesOrg = getExecutionCountrySalesOrg()
		query = "Select lc.*,eac.EAC_Value,eac.Currency from HPS_LABOR_COST_DATA lc join Labor_GES_EAC_Value eac on lc.Part_Number = eac.GES_Service_Material where Sales_Org = '{0}' and Part_Number in ('{1}')".format(salesOrg, "','".join(gesParts))
		res = SqlHelper.GetList(query)
		gesTP = dict()
		gesEAC = dict()
		for i in res:
			#gesTP[i.Part_Number] = {"cost":i.Cost_CurrentMonth_Year1,"stdcurrency":i.Cost_Currency_Code}
			#gesEAC[i.Part_Number] = {"cost":i.EAC_Value,"stdcurrency":i.Currency}
			if executionYear == str(DateTime.Now.Year ):
				gesTP[i.Part_Number] = {"cost":i.Cost_CurrentMonth_Year1,"stdcurrency":i.Cost_Currency_Code}
				gesEAC[i.Part_Number] = {"cost":i.EAC_Value,"stdcurrency":i.Currency}
			elif executionYear == str(DateTime.Now.Year  + 1):
				gesTP[i.Part_Number] = {"cost":i.Cost_CurrentMonth_Year2,"stdcurrency":i.Cost_Currency_Code}
				gesEAC[i.Part_Number] = {"cost":i.EAC_Value,"stdcurrency":i.Currency}
			elif executionYear == str(DateTime.Now.Year  + 2):
				gesTP[i.Part_Number] = {"cost":i.Cost_CurrentMonth_Year3,"stdcurrency":i.Cost_Currency_Code}
				gesEAC[i.Part_Number] = {"cost":i.EAC_Value,"stdcurrency":i.Currency}
			elif executionYear == str(DateTime.Now.Year  + 3):
				gesTP[i.Part_Number] = {"cost":i.Cost_CurrentMonth_Year4,"stdcurrency":i.Cost_Currency_Code}
				gesEAC[i.Part_Number] = {"cost":i.EAC_Value,"stdcurrency":i.Currency}
		tpWithConversion = laborCostWithCOnversion(gesTP)
		eacWithConversion = laborCostWithCOnversion(gesEAC)
		return tpWithConversion,eacWithConversion

	def getTPandEACValueNonSapParts(gesParts,executionYear):
		salesOrg = getExecutionCountrySalesOrg()
		query = "Select lc.*,eac.EAC_Value,eac.Currency from HPS_LABOR_COST_DATA lc join Labor_GES_EAC_Value eac on lc.Part_Number = eac.GES_Service_Material where Sales_Org = '' and Part_Number in ('{}')".format("','".join(gesParts))
		res = SqlHelper.GetList(query)
		gesTP = dict()
		gesEAC = dict()
		for i in res:
			#gesTP[i.Part_Number] = {"cost":i.Cost_CurrentMonth_Year1,"stdcurrency":i.Cost_Currency_Code}
			#gesEAC[i.Part_Number] = {"cost":i.EAC_Value,"stdcurrency":i.Currency}
			if executionYear == str(DateTime.Now.Year ):
				gesTP[i.Part_Number] = {"cost":i.Cost_CurrentMonth_Year1,"stdcurrency":i.Cost_Currency_Code}
				gesEAC[i.Part_Number] = {"cost":i.EAC_Value,"stdcurrency":i.Currency}
			elif executionYear == str(DateTime.Now.Year  + 1):
				gesTP[i.Part_Number] = {"cost":i.Cost_CurrentMonth_Year2,"stdcurrency":i.Cost_Currency_Code}
				gesEAC[i.Part_Number] = {"cost":i.EAC_Value,"stdcurrency":i.Currency}
			elif executionYear == str(DateTime.Now.Year  + 2):
				gesTP[i.Part_Number] = {"cost":i.Cost_CurrentMonth_Year3,"stdcurrency":i.Cost_Currency_Code}
				gesEAC[i.Part_Number] = {"cost":i.EAC_Value,"stdcurrency":i.Currency}
			elif executionYear == str(DateTime.Now.Year  + 3):
				gesTP[i.Part_Number] = {"cost":i.Cost_CurrentMonth_Year4,"stdcurrency":i.Cost_Currency_Code}
				gesEAC[i.Part_Number] = {"cost":i.EAC_Value,"stdcurrency":i.Currency}
		tpWithConversion = laborCostWithCOnversion(gesTP)
		eacWithConversion = laborCostWithCOnversion(gesEAC)
		return tpWithConversion,eacWithConversion

	def populateCotainer(foPartNumberCon,entry,costWithConversion,PriceData):
		row = foPartNumberCon.AddNewRow(False)
		row["Product_Module"] = entry.Product_Module
		row["Contract_Type"] = entry.Contract_Type
		row["FO_Part_Number"] = entry.FO_Part_Number
		row["Part_Description"] = entry.PRODUCT_NAME
		row["Cost"] = str(costWithConversion.get(entry.FO_Part_Number,''))
		row["ListPrice"] = str((PriceData.get(entry.FO_Part_Number,'')))
		if row["Cost"] in ('',"0.00",'0.00'):
			row["Manual_Entry"] = "Yes"

	def populateGesMaterials(foPartNumberCon,entry,gesRegionalCost,PriceData):
		row = foPartNumberCon.AddNewRow(False)
		row["Product_Module"] = entry.Product_Module
		row["Part_Description"] = entry.PRODUCT_NAME
		row["GES_Part_Number"] = entry.GES_Part_Number
		row["Deliverable_Type"] = entry.Deliverable_Type
		row["Cost"] = str(gesRegionalCost.get(entry.GES_Part_Number,''))
		row["ListPrice"] = str((PriceData.get(entry.GES_Part_Number,'')))


	def populateFOPartNumberCon(Product, foPartNumberCon,mpaAvailable,activeServiceContract,executionYear,SelectedProducts):
		partsList = []
		foPartNumberCon.Rows.Clear()
		LOB = Quote.GetCustomField("Booking LOB").Content #Get Quote Booking LOB
		queryData = SqlHelper.GetList("select TOP 2000 fo.*,p.PRODUCT_NAME from Labor_FO_Part_Number fo join products p on p.PRODUCT_CATALOG_CODE = fo.FO_Part_Number where fo.LOB = '"+LOB+"' and fo.GES_Part_Number = '' and fo.Product_Module IN ("+SelectedProducts+")")
		if queryData is not None:
			if mpaAvailable or activeServiceContract == "Yes":
				for entry in queryData:
					if entry.Contract_Type == "Contract":
						if entry.FO_Part_Number not in partsList:
							partsList.append(entry.FO_Part_Number)
				PriceData = GetPrice(partsList)
				laborcostParts =laborCostWithoutConversion(partsList,executionYear)
				costWithConversion = laborCostWithCOnversion(laborcostParts)

				for entry in queryData:
					if entry.Contract_Type == "Contract":
						populateCotainer(foPartNumberCon,entry,costWithConversion,PriceData)
			else:
				for entry in queryData:
					if entry.Contract_Type == "Non-Contract":
						if entry.FO_Part_Number not in partsList:
							partsList.append(entry.FO_Part_Number)
				PriceData = GetPrice(partsList)
				laborcostParts =laborCostWithoutConversion(partsList,executionYear)
				costWithConversion = laborCostWithCOnversion(laborcostParts)
				for entry in queryData:
					if entry.Contract_Type == "Non-Contract":
						populateCotainer(foPartNumberCon,entry,costWithConversion,PriceData)

		sapCountriesparts = []
		nonsapCountriesparts = []
		gesParts = []

		queryData1 = SqlHelper.GetList("select fo.*,p.PRODUCT_NAME from Labor_FO_Part_Number fo join products p on p.PRODUCT_CATALOG_CODE = fo.GES_Part_Number where fo.GES_Part_Number != '' and fo.LOB = '"+LOB+"'and fo.Product_Module IN ("+SelectedProducts+") and fo.GES_Location = '{}'".format(Product.ParseString('<*ValueCode(MSID_GES_Location)*>')))
		if queryData1 is not None:
			for entry in queryData1:
				if entry.GES_Part_Number not in gesParts:
					gesParts.append(entry.GES_Part_Number)
				if (entry.GES_Part_Number.endswith("_IN") or entry.GES_Part_Number.endswith("_RO")) and entry.GES_Part_Number not in sapCountriesparts:
					sapCountriesparts.append(entry.GES_Part_Number)
				elif (entry.GES_Part_Number.endswith("_CN") or entry.GES_Part_Number.endswith("_UZ") or entry.GES_Part_Number.endswith("_EG")) and entry.GES_Part_Number not in nonsapCountriesparts:
					nonsapCountriesparts.append(entry.GES_Part_Number)
			
			if Product.Attr('MSID_Selected_Products').GetValue() in ('QCS RAE Upgrade','CWS RAE Upgrade')   and Product.Attr('MSID_GES_Location').GetValue() not in ('GES China', 'None'):
				nonsapCountriesparts.append("SVC_GES_P350B_CN")
				gesParts.append("SVC_GES_P350B_CN")
			gesTPSap,gesEAC1Sap = getTPandEACValueSapParts(sapCountriesparts,executionYear)
			gesTPNonSap,gesEACNonSap = getTPandEACValueNonSapParts(nonsapCountriesparts,executionYear)

			gesRegionalCost = dict()
			for part in sapCountriesparts:
				if part in gesTPSap and gesTPSap[part]:
					gesRegionalCost[part] = getFloat(gesTPSap.get(part,0)) + getFloat(gesEAC1Sap.get(part,0))
			for part in nonsapCountriesparts:
				if part in gesTPNonSap and gesTPNonSap[part]:
					gesRegionalCost[part] = getFloat(gesTPNonSap.get(part,0)) + getFloat(gesEACNonSap.get(part,0))
			if gesParts:
				PriceData1 = GetPrice(gesParts)
		
			if Product.Attr('MSID_Selected_Products').GetValue() in ('QCS RAE Upgrade','CWS RAE Upgrade')   and Product.Attr('MSID_GES_Location').GetValue() not in ('GES China', 'None'):
				Product.Attr("QCS_CWS_Labor_del_china_part_regional_cost_price").AssignValue(str(gesRegionalCost.get("SVC_GES_P350B_CN",'')))
				Product.Attr("QCS_CWS_Labor_del_china_part_list_price").AssignValue(str(PriceData1.get("SVC_GES_P350B_CN",'')))
			for entry in queryData1:
				populateGesMaterials(foPartNumberCon,entry,gesRegionalCost,PriceData1)

	migration_new_cont = Product.GetContainerByName('CONT_Migration_MSID_Selection')
	for MigrationNew in migration_new_cont.Rows:
		foPartNumberCon = getContainer(MigrationNew.Product, "MSID_Labor_FO_Part_Number")
		mpaAvailable = checkForMPACustomer()
		entitlement = Quote.GetCustomField("Entitlement").Content
		#salesOrg,currency = Quote.SelectedMarket.MarketCode.split('_')
		salesOrg = Quote.GetCustomField('Sales Area').Content
		currency = Quote.GetCustomField('Currency').Content
		activeServiceContract = MigrationNew.Product.Attr("MSID_Active_Service_Contract").GetValue()
		executionYear = str(getDefaultExecutionYear())
		MSID_Selected_Products=MigrationNew.Product.Attr("MSID_Selected_Products").GetValue()
		MSID_Selected_Products = MSID_Selected_Products.replace('Virtualization System Migration', 'Virtualization System')
		#MSID_Selected_Products ='Virtualization System' if MSID_Selected_Products == 'Virtualization System Migration' else MSID_Selected_Products
		SelectedProducts = "'"+ MSID_Selected_Products.replace("<br>","','").replace("LCN One Time Upgrade","LCN").replace("FDM Upgrade 1","FDM Upgrade").replace("FDM Upgrade 2","FDM Upgrade").replace("FDM Upgrade 3","FDM Upgrade") + "','PM','PA'"
		if 'FSC to SM' in SelectedProducts:
			SelectedProducts = SelectedProducts + ",'FSC to SM Audit'"
		if 'FSC to SM IO Migration' in SelectedProducts:
			SelectedProducts = SelectedProducts + ",'FSC to SM IO Audit'"
		'''if 'Generic System' in SelectedProducts:
			for i in Product.GetContainerByName('MSID_Product_Container_Generic_hidden').Rows:
				SelectedProducts = SelectedProducts + ",'"+i["Product Name"]+"'"'''
		populateFOPartNumberCon(MigrationNew.Product, foPartNumberCon,mpaAvailable,activeServiceContract,executionYear,SelectedProducts)
		if MigrationNew.Product.ParseString('[LIKE](<*VALUE(MSID_Selected_Products)*>,3rd Party PLC to ControlEdge PLC/UOC)'):
			MigrationNew.Product.ApplyRules()