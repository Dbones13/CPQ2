import time
from GS_GetPriceFromCPS import getPrice

def GetQueryData(QueryStr):
	data, offset, limit = [], 0, 999
	while True:
		query = SqlHelper.GetList("{} OFFSET {} ROWS FETCH NEXT {} ROWS ONLY".format(QueryStr, offset, limit))
		if not query:
			break
		data.extend(query)
		offset += limit
	return data

def GetQueryDataDict(data):
	dataDict = {}
	partsCode = []
	for drow in data:
		dataDict[drow.PartNumber] = drow
		partsCode.append(drow.PRODUCT_CATALOG_CODE)
	return dataDict, partsCode

def isDiscountAllowed(qI_ProductLine, qI_PLSG, partNumber):
	partsList = ['CEPS_CAD','CEPS_PE','CEPS_PM','D4418111','D4418113','SVC-PER-DIEM','SVC-PMC-TRAV-AIR','SVC-PMC-TRAV-CAR','SVC-PMC-TRAV-PVT','ECSA-1001','ECSP-1001']
	plsgList = ['7725-7D38','7029-7179','7076-7000','7066-7000','7066-7729','7066-7730','7066-7731','7061-Y963','7061-Y964']
	return ('1' if not qI_ProductLine or qI_PLSG in plsgList or partNumber in partsList else '0')

def splitPartsList(pList, chunkSize = 1000):
	return [pList[i:i + chunkSize] for i in range(0, len(pList), chunkSize)]

def getPartsPrice(partsCatalogCode, quote, tagParserQuote):
	partsList = splitPartsList(partsCatalogCode)
	priceData = {}
	for pList in partsList:
		pData = {}
		pData = getPrice(quote, pData, set(partsCatalogCode), tagParserQuote)
		priceData.update(pData)
	return priceData

def GetQueryDataToDict(data):
	dataDict = {}
	for drow in data:
		dataDict[drow.colKey] = drow
	return dataDict

def isValidQty(value):
	return isinstance(value, str) and value.isdigit()

def getSESPprice(PartNumber, entitlementType, salesOrg, currencyCode, effectiveDate):
	return GetQueryDataToDict(GetQueryData("select PartNumber as colKey, Amount from HPS_SESP_DATA(nolock) where PartNumber IN ('{0}') and Price_Type = '{1}' and Sales_Org = '{2}' and Currency = '{3}' and Valid_from <= '{4}' and Valid_to >= '{4}' and coalesce(Deletion_Indicator,'') <> 'X' ORDER BY CpqTableEntryId".format(PartNumber, entitlementType, salesOrg, currencyCode, effectiveDate)))

def uploadTPSData(Quote, Product, data, TotalRows, headers, tagParserQuote):
	Product.Attr("Download_Flag").AssignValue('')
	#Trace.Write('{}'.format(str(data)))
	start = time.time()
	start1 = time.time()
	PrdContainer = Product.GetContainerByName("TPS_PRDContainerSys")
	PrdContainer.Rows.Clear()
	PrdContainer_Invalid = Product.GetContainerByName("Siebel_Invalid_Parts")
	PrdContainer_Invalid.Rows.Clear()
	gPrdDeleteIndex = []
	inValidPartNumberMsg = Translation.Get('message.uploadExcel.catalog')
	notSimpleProductMsg = Translation.Get('message.uploadExcel.configurable')
	priceBookMsg = Translation.Get('message.uploadExcel.pricebook')
	exchangeRate    = float(Quote.GetCustomField('Exchange Rate').Content if Quote.GetCustomField('Exchange Rate').Content else 1)
	booking_country = Quote.GetCustomField('Booking Country').Content
	effectiveDate = Quote.EffectiveDate.ToString('MM/dd/yyyy')
	salesOrg = Quote.GetCustomField('Sales Area').Content
	currencyCode = Quote.SelectedMarket.CurrencyCode
	entitlement = Quote.GetCustomField('Entitlement').Content
	entitlementType = ''
	if entitlement:
		entitlementType = 'SF' if 'flex' in entitlement.lower() else 'SP'
	PrdDict=[]
	partList = []
	KnEpartsList = {}
	sysName=''
	for i in range(1,TotalRows):
		validRow = False
		for x in headers.Values:
			if data[i,x] != '':
				validRow = True
		if validRow == False:
			break
		if i==1: #not sysName and data[i,headers['SystemName']]:
			sysName = data[i,headers['SystemName']].strip();
		PrdDict.append({"PartNumber": data[i,headers['Part']], "Quantity": data[i,headers['PartQuantity']].strip() if isValidQty(data[i,headers['PartQuantity']].strip()) else "-1", "Area": data[i,headers['Area']] if headers.get('Area', '') else '', "WBS": data[i,headers['WBS']] if headers.get('WBS', '') else '', "UserComments": data[i,headers['UserComments']] if headers.get('UserComments', '') else '', "Year": data[i,headers['Year']] if headers.get('Year', '') else '', "Discount": data[i,headers['SellPriceDiscount']] if data[i,headers['SellPriceDiscount']] else '0' if headers.get('SellPriceDiscount', '') else '0', "DoNotPriceFlag": data[i,headers['DoNotPriceFlag']] if headers.get('DoNotPriceFlag', None) else None, "PackageName": data[i,headers['PackageName']] if headers.get('PackageName', None) else None, "ParentFlag": data[i,headers['ParentFlag']] if headers.get('ParentFlag', None) else None, "FileName": data[i,headers['FileName']] if headers.get('FileName', None) else None, "TPCFileExportDate": data[i,headers['TPCFileExportDate']] if headers.get('TPCFileExportDate', None) else None})
		pkgName= data[i,headers['PackageName']] if headers.get('PackageName', None) else None
		if pkgName is not None and pkgName.strip().lower() not in ('', 'project'):
			KnEpartsList.setdefault(pkgName, []).append(data[i,headers['Part']])
		partList.append(data[i,headers['Part']])
	#Trace.Write(str(PrdDict))
	if not sysName:
		Product.Messages.Add('Upload file has blank/empty System Name')
		return
	#Productdetails = GetQueryDataDict(GetQueryData("select h.PartNumber, h.MindeliveryQuantity, h.MinOrderQuantity, h.ProductLine, h.ProductLineDesc,h.SalesText,h.PLSGDesc,h.PLSG,sp.LOB,sp.Cost_Category, ps.IsSimple from HPS_PRODUCTS_MASTER h JOIN SAP_PLSG_LOB_Mapping sp ON h.PLSG = sp.SAP_PL_PLSG JOIN Products ps on h.PartNumber = ps.PRODUCT_CATALOG_CODE JOIN product_versions(nolock) pv on ps.Product_ID = pv.Product_ID WHERE pv.Is_Active = 1 and ps.PRODUCT_ACTIVE = 'True' and h.PartNumber IN ('{0}') ORDER BY h.CpqTableEntryId".format("', '".join(set(partList)))))
	Productdetails, partsCatalogCode = GetQueryDataDict(GetQueryData("select h.PartNumber, ps.PRODUCT_NAME, h.MindeliveryQuantity, h.MinOrderQuantity, h.ProductLine, h.ProductLineDesc,h.SalesText,h.PLSGDesc,h.PLSG,sp.LOB,sp.Cost_Category, ps.IsSimple, ps.PRODUCT_CATALOG_CODE, ps.UnitOfMeasure, COALESCE(SC.Cost, SG.Cost, -1) as Cost, COALESCE(WtW.WTW_FACTOR, '0.0') as WTWFactor, prt.PRODUCTTYPE_NAME, h.CrossDistributionStatus from HPS_PRODUCTS_MASTER h JOIN SAP_PLSG_LOB_Mapping sp ON h.PLSG = sp.SAP_PL_PLSG JOIN Products ps on h.PartNumber = ps.PRODUCT_CATALOG_CODE JOIN product_versions(nolock) pv on ps.Product_ID = pv.Product_ID LEFT JOIN PRODUCT_TYPES_DEFN prt on ps.PRODUCTTYPE_CD = prt.PRODUCTTYPE_CD LEFT JOIN HPS_USSC_COST_DATA SC on h.PartNumber = SC.PartNumber and SC.Valid_from <= '{eDate}' and SC.Valid_to >= '{eDate}' LEFT JOIN HPS_USSG_COST_DATA SG on h.PartNumber = SG.PartNumber and SG.Valid_from <= '{eDate}' and SG.Valid_to >= '{eDate}' LEFT JOIN HPS_PLSG_WTW_FACTOR WTW on  h.PLSG = WTW.PL_PLSG WHERE pv.Is_Active = 1 and ps.PRODUCT_ACTIVE = 'True' and h.PartNumber IN ('{0}') ORDER BY h.CpqTableEntryId".format("', '".join(set(partList)), eDate = effectiveDate)))
	tariffProducts = GetQueryDataToDict(GetQueryData("SELECT CO.PART_NUMBER as colKey, CO.PART_NUMBER as PartNumber, TD.COO,TD.TARIFF_COST_PER,TD.TARIFF_LIST_PER FROM HPS_TARIFF_DETAILS TD left JOIN HPS_TARIFF_PRODUCTS_COO CO on CO.COO = TD.COO WHERE SHIP_TO = '{}' and CO.PART_NUMBER IN ('{}') ORDER BY CO.CpqTableEntryId".format(booking_country, "', '".join(set(partList)))))
	tariffMarkUps = GetQueryDataToDict(GetQueryData("SELECT PLSG as colKey, PLSG, MARKUP_RATE FROM HPS_TARIFF_PLSG_MARKUP_RATE ORDER BY CpqTableEntryId"))
	PriceData = getPartsPrice(list(set(partsCatalogCode)), Quote, tagParserQuote)
	SESPpriceData = {}
	if entitlementType:
		SESPpriceData = getSESPprice("', '".join(set(partList)), entitlementType, salesOrg, currencyCode, effectiveDate)
	InvalidPartsDict = {}
	KnEPrdDict = {}
	KnEPrdDictPricenCost = {}
	RQUP_partList = []
	ERP_partList = []
	zoroPrice_partList = []
	PrdContainer_Sys = Product.GetContainerByName("TPS_PRDContainerSys")
	PrdSys = PrdContainer_Sys.AddNewRow()
	PrdSys.Product.Attr('PRD_Name').AssignValue(sysName)
	PrdSys.Product.Attr('PRD_Description').AssignValue(sysName)
	PrdSys.Product.Attr('ItemQuantity').AssignValue('1')
	PrdSys.Product.Attr('PRD_Quantity').AssignValue('1')
	PrdSys.Product.Attr('PRD_Price').AssignValue('0')
	PrdSys.Product.Attr('PRD_Cost').AssignValue('0')

	PrdSys["ProductName"] = sysName
	PrdSys["Description"] = sysName
	PrdSys["Quantity"] = "1"
	PrdSys["ListPrice"] = "0"
	PrdSys["Cost"] = "0"
	PrdSys.IsSelected = True
	gPrdContainer = PrdSys.Product.GetContainerByName("TPC_PartsContainer")
	gPrdKnEContainer = PrdSys.Product.GetContainerByName("TPC_KnEPartsContainer")
	for pindex, gprd in enumerate(PrdDict):
		prdRow = Productdetails.get(gprd["PartNumber"], None)
		if prdRow and gprd['ParentFlag'] == 'Y' and prdRow.Cost < 0:
			prdRow.Cost = 0
		if gprd["PartNumber"] in Productdetails and prdRow and prdRow.IsSimple and prdRow.PRODUCT_CATALOG_CODE in PriceData and gprd['Year'] in ('', 'Year 1', 'Year 2', 'Year 3', 'Year 4', 'Year 5', 'Year 6', 'Year 7', 'Year 8', 'Year 9', 'Year 10') and gprd['Quantity'] != "-1" and prdRow.Cost >= 0:
			if gprd.get('PackageName', '') and gprd.get('PackageName', '').strip().lower() not in ('', 'project'):
				gKnEProd = gPrdKnEContainer.AddNewRow()
				if any(x in set(KnEpartsList[gprd.get('PackageName', '').strip()]) for x in ('EP-EHPMSP', 'TC-SWCS30')) and gprd["PartNumber"] not in ('EP-EHPMSP', 'TC-SWCS30') and gprd['ParentFlag'] != 'Y':
					gKnEProd["setQtyZero"] = '0'
				else:
					gKnEProd["setQtyZero"] = '1'
				gKnEProd["PartNumber"] = gprd["PartNumber"]
				gKnEProd["Quantity"] = gprd['Quantity']
				gKnEProd["ProductName"] = prdRow.PRODUCT_NAME
				gKnEProd["PackageName"] = gprd['PackageName']
				gKnEProd["ParentFlag"] = gprd['ParentFlag']
				gKnEProd["isPriced"] = '0' if gprd['DoNotPriceFlag'] else '1'
				gKnEProd["DoNotPriceFlag"] = gprd['DoNotPriceFlag']
				gKnEProd["QI_Area"] = gprd['Area']
				gKnEProd["WBS"] = gprd['WBS']
				gKnEProd["QI_Year"] = gprd['Year'] if gprd['Year'] != '' else 'None'
				gKnEProd["QI_Additional_Discount_Percent"] = gprd['Discount']
				gKnEProd["QI_UserComments"] =  gprd['UserComments']
				gKnEProd["FileName"] = gprd['FileName']
				gKnEProd["TPCFileExportDate"] = gprd['TPCFileExportDate']
				if gKnEProd['DoNotPriceFlag'] =='Y' or gKnEProd['ParentFlag'] == 'Y':
					gKnEProd["Cost"] = str(prdRow.Cost * exchangeRate)
					gKnEProd["ExtendedCost"] = str(prdRow.Cost * exchangeRate * int(gKnEProd["setQtyZero"])  * (int(gKnEProd["Quantity"]) if gKnEProd["Quantity"] else 0))
					gKnEProd["QI_UnitWTWCost"] = str(float(gKnEProd["Cost"]) / (1 + (float(prdRow.WTWFactor) if prdRow.WTWFactor else 0)) if gKnEProd["Cost"] else 0)
					gKnEProd["QI_ExtendedWTWCost"] = str(float(gKnEProd["QI_UnitWTWCost"]) * int(gKnEProd["setQtyZero"]) * (int(gKnEProd["Quantity"]) if gKnEProd["Quantity"] else 0))
					if gKnEProd['PackageName'] in KnEPrdDictPricenCost:
						KnEPrdDictPricenCost[gKnEProd['PackageName']]["ExtendedCost"] = KnEPrdDictPricenCost[gKnEProd['PackageName']]["ExtendedCost"] + float(gKnEProd["ExtendedCost"])
						KnEPrdDictPricenCost[gKnEProd['PackageName']]["QI_ExtendedWTWCost"] = KnEPrdDictPricenCost[gKnEProd['PackageName']]["QI_ExtendedWTWCost"] + float(gKnEProd["QI_ExtendedWTWCost"])
					else:
						KnEPrdDictPricenCost[gKnEProd['PackageName']] = {"ExtendedCost": float(gKnEProd["ExtendedCost"]), "QI_ExtendedWTWCost": float(gKnEProd["QI_ExtendedWTWCost"])}
				if gKnEProd['ParentFlag'] != 'Y' and gKnEProd['DoNotPriceFlag'] =='Y':
					continue

			gProd = gPrdContainer.AddNewRow()
			gProd["PartNumber"] = gprd["PartNumber"]
			gProd["UploadQuantity"] = gprd['Quantity']
			gProd["AdjQty"] = '0'
			gProd["Quantity"] = gprd['Quantity']
			gProd["SystemNumber"] = sysName
			gProd["SystemName"] = sysName
			gProd["SysQuantity"] = "1"
			gProd["OriginalItemNumber"] = "1"
			gProd["ParentProductName"] = sysName
			gProd["ParentProductDescription"] = sysName
			gProd["ParentQuantity"] = "1"
			gProd["ATOItemNumber"] = str(pindex)
			gProd["QI_Area"] = gprd['Area']
			gProd["QI_UserComments"] = gprd['UserComments']
			gProd["LeadTime"] = '1'
			gProd["QI_Year"] = gprd['Year'] if gprd['Year'] != '' else 'None'
			gProd.GetColumnByName('QI_Year').SetAttributeValue(gprd['Year'] if gprd['Year'] != '' else 'None')
			gProd["WBS"] = gprd['WBS']
			gProd["isPriced"] = '0' if gprd['DoNotPriceFlag'] == 'Y' else '1'
			gProd["FileName"] = gprd['FileName']
			gProd["TPCFileExportDate"] = gprd['TPCFileExportDate']
			gProd["QI_Additional_Discount_Percent"] = gprd['Discount']
			gProd["QI_MPA_Discount_Percent"] = '0'
			gProd["QI_MPA_Discount_Amount"] = '0'
			gProd["QI_Tariff_Amount"] = '0'
			gProd["QI_Cost_Tariff_Amount"] = '0'
			gProd["PackageName"] = gprd['PackageName']
			gProd["ParentFlag"] = gprd['ParentFlag']

			if gprd['ParentFlag'] == 'Y':
				KnEPrdDict[gprd['PackageName']] = gProd.RowIndex

			gProd["ProductName"] = prdRow.PRODUCT_NAME
			if entitlementType and SESPpriceData.get(prdRow.PRODUCT_CATALOG_CODE, None):
				gProd["ListPrice"] = str(float(SESPpriceData[prdRow.PRODUCT_CATALOG_CODE].Amount) * int(gProd["isPriced"]))
			else:
				gProd["ListPrice"] = str(float(PriceData.get(prdRow.PRODUCT_CATALOG_CODE, 0)) * int(gProd["isPriced"])) #<*CTX ( MyContainer.CurrentRow.ProductTotalPrice )*>
			gProd["ExtendedListPrice"] = str(float(gProd["ListPrice"]) * (int(gProd["Quantity"]) if gProd["Quantity"] else 0))
			gProd["LOB"] = prdRow.LOB
			gProd["QI_MinOrderQty"] = prdRow.MinOrderQuantity
			gProd["QI_ProductLine"] = prdRow.ProductLine
			gProd["QI_ProductLineDesc"] = prdRow.ProductLineDesc
			gProd["QI_PLSG"] = prdRow.PLSG
			gProd["QI_PLSGDesc"] = prdRow.PLSGDesc
			gProd["Cost"] = str(prdRow.Cost * exchangeRate)
			gProd["ExtendedCost"] = str(prdRow.Cost * exchangeRate  * (int(gProd["Quantity"]) if gProd["Quantity"] else 0))
			gProd["QI_No_Discount_Allowed"] = '1' if gProd["isPriced"] == '0' else isDiscountAllowed(gProd["QI_ProductLine"], gProd["QI_PLSG"], gProd["PartNumber"])
			gProd["QI_Additional_Discount_Percent"] = '0' if gProd["QI_No_Discount_Allowed"] == '1' else gProd["QI_Additional_Discount_Percent"]
			gProd["QI_Additional_Discount_Amount"] = str(float(gProd["ExtendedListPrice"]) * float(gProd["QI_Additional_Discount_Percent"]) / 100)
			gProd["ExtendedAmount"] = str(float(gProd["ExtendedListPrice"]) - float(gProd["QI_Additional_Discount_Amount"]))
			gProd["QI_UnitSellPrice"] = str((float(gProd["ExtendedAmount"]) / int(gProd["Quantity"])) if gProd["Quantity"] not in ['0', '', None] else 0)
			gProd["QI_UnitWTWCost"] = str(float(gProd["Cost"]) / (1 + (float(prdRow.WTWFactor) if prdRow.WTWFactor else 0)) if gProd["Cost"] else 0)
			gProd["QI_ExtendedWTWCost"] = str(float(gProd["QI_UnitWTWCost"])  * (int(gProd["Quantity"]) if gProd["Quantity"] else 0))
			gProd["QI_RegionalMargin"] = str(float(gProd["ExtendedAmount"]) - float(gProd["ExtendedCost"]))
			gProd["QI_RegionalMarginPercent"] = str(float(gProd["QI_RegionalMargin"])/float(gProd["ExtendedAmount"]) * 100) if float(gProd["ExtendedAmount"]) != 0 else '0'
			gProd["QI_WTWMargin"] = str(float(gProd["ExtendedListPrice"]) - float(gProd["QI_ExtendedWTWCost"]))
			gProd["QI_WTWMarginPercent"] = str(float(gProd["QI_WTWMargin"])/float(gProd["ExtendedListPrice"]) * 100) if float(gProd["ExtendedListPrice"]) != 0 else '0'
			gProd["QI_UoM"] = prdRow.UnitOfMeasure
			gProd["QI_SalesText"] = prdRow.SalesText
			gProd["QI_ProductCostCategory"] = prdRow.Cost_Category
			gProd["QI_ProjectType"] = prdRow.PRODUCTTYPE_NAME
			gProd["QI_CrossDistributionStatus"] = prdRow.CrossDistributionStatus

			if gprd["PartNumber"] in tariffProducts:
				gProd["QI_Cost_Tariff_Amount"] = str(float(gProd["QI_ExtendedWTWCost"]) * (tariffProducts[gprd["PartNumber"]].TARIFF_COST_PER if tariffProducts.get(gprd["PartNumber"], None) else 0) / 100)
				base_value = float(gProd["QI_ExtendedWTWCost"]) * (1 + (tariffMarkUps[prdRow.PLSG].MARKUP_RATE if tariffMarkUps.get(prdRow.PLSG, None) else 0) / 100)
				gProd["QI_Tariff_Amount"] = str(base_value * (tariffProducts[gprd["PartNumber"]].TARIFF_LIST_PER if tariffProducts.get(gprd["PartNumber"], None) else 0) / 100)

			RQUP_partList.append(gprd["PartNumber"]) if prdRow.CrossDistributionStatus == '05 PreRelease' else None
			ERP_partList.append(gprd["PartNumber"]) if prdRow.SalesText else None
			zoroPrice_partList.append(gprd["PartNumber"]) if float(PriceData.get(prdRow.PRODUCT_CATALOG_CODE, 0)) == 0 else None

		else:
			inRow=PrdContainer_Invalid.AddNewRow()
			inRow['Part Number']= gprd["PartNumber"]
			inRow['Item Id']= str(pindex+1)
			if not prdRow:
				inRow['Message']= inValidPartNumberMsg
			elif prdRow.IsSimple != True:
				inRow['Message']= notSimpleProductMsg
			elif prdRow.PRODUCT_CATALOG_CODE not in PriceData:
				inRow['Message']= priceBookMsg
			elif prdRow.Cost < 0:
				inRow['Message']= "No Cost available in Pricebook"
			elif gprd['Year'] not in ('', 'Year 1', 'Year 2', 'Year 3', 'Year 4', 'Year 5', 'Year 6', 'Year 7', 'Year 8', 'Year 9', 'Year 10'):
				inRow['Message']= 'Year value - "{}"  is not Valid'.format(gprd['Year'])
			elif gprd['Quantity'] == '-1':
				inRow['Message']= 'Invalid Quantity'
			# elif gProd.Product.Attributes.GetByName('ItemQuantity') == None:
			# 	inRow['Message']= "Default Quantity is 1, not allowed to change"
			elif float(PriceData.get(prdRow.PRODUCT_CATALOG_CODE, 0))==0 and prdRow.Cost == 0:
				inRow['Message']= 'Both List Price & Cost have zero value'
			else:
				inRow['Message']= "Unknown Error";
	for keyPackage in KnEPrdDict:
		KnERow = gPrdContainer.Rows[KnEPrdDict[keyPackage]]
		KnERow["Cost"] = str(KnEPrdDictPricenCost[keyPackage]["ExtendedCost"])
		KnERow["ExtendedCost"] = str(KnEPrdDictPricenCost[keyPackage]["ExtendedCost"])
		KnERow["QI_UnitWTWCost"] = str(KnEPrdDictPricenCost[keyPackage]["QI_ExtendedWTWCost"])
		KnERow["QI_ExtendedWTWCost"] = str(KnEPrdDictPricenCost[keyPackage]["QI_ExtendedWTWCost"])
		KnERow["QI_RegionalMargin"] = str(float(KnERow["ExtendedAmount"]) - float(KnERow["ExtendedCost"]))
		KnERow["QI_RegionalMarginPercent"] = str(float(KnERow["QI_RegionalMargin"])/float(KnERow["ExtendedAmount"]) * 100) if float(KnERow["ExtendedAmount"]) != 0 else '0'
		KnERow["QI_WTWMargin"] = str(float(KnERow["ExtendedListPrice"]) - float(KnERow["QI_ExtendedWTWCost"]))
		KnERow["QI_WTWMarginPercent"] = str(float(KnERow["QI_WTWMargin"])/float(KnERow["ExtendedListPrice"]) * 100) if float(KnERow["ExtendedListPrice"]) != 0 else '0'
	if RQUP_partList:
		Product.Messages.Add('Upload file contains Unreleased Product ({}). User should answer the RQUP question RAFR1 as "Yes" in the functional review question tab.'.format(', '.join(set(RQUP_partList))))
	if ERP_partList:
		#Product.Messages.Add('Upload file has ERP texts in Product ({}). Please check before submitting for approval'.format(', '.join(ERP_partList)))
		Product.Messages.Add('Your Quote may have ERP texts in one or more-line items. Please check before submitting for approval.')
	#if zoroPrice_partList:
	#	Product.Messages.Add('Upload file has zero price in Product ({}). Please check before submitting for approval'.format(', '.join(zoroPrice_partList)))
	end = time.time()
	Log.Info("TPC Upload Execution Time: {}".format(float(end - start1)))