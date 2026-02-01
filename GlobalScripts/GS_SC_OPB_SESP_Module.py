#GS_SC_OPB_SESP_Module
from CPQ_SF_SC_Modules import CL_SC_Modules
def getModelDetails(partNumbers):
	descDict = dict()
	platformDict = dict()
	moduleDict = dict()
	lst = SqlHelper.GetList("select p.PartNumber, p.Platform, p.Description, m.ModuleName from SC_PRICING_SESP p JOIN CT_SC_PLATFORM_MODULE_MAPPING m ON p.Platform=m.PlatformName where p.PartNumber in {}".format(str(tuple(partNumbers)).replace(',)',')')))
	for row in lst:
		descDict[row.PartNumber] = row.Description
		platformDict[row.PartNumber] = row.Platform
		moduleDict[row.PartNumber] = row.ModuleName
	return descDict, platformDict, moduleDict

def getPreviousQuoteInfo(Quote):
	qtyDict = dict()
	unitPriceDict = dict()
	listPriceDict = dict()
	sellPriceDict = dict()
	systemNameDict = dict()
	systemNumberDict = dict()
	descriptionDict = dict()
	pyPartNumbers = []
	product_name = 'Solution Enhancement Support Program'
	reference_number = Quote.GetCustomField("SC_CF_PREVIOUS_QUOTE_NO").Content.strip()
	if reference_number != '':
		query = SqlHelper.GetFirst("Select Product,ProductDetails from SC_RENEWAL_TABLE where Product = '{0}' and QuoteID = '{1}' UNION ALL Select Product,ProductDetails from SC_RENEWAL_TABLE where Product = '{0}' and QuoteID = '{2}' AND NOT EXISTS (SELECT 1 FROM SC_RENEWAL_TABLE WHERE QuoteID = '{1}')".format(product_name, reference_number, reference_number.split('-')[0]))
		Trace.Write("Select Product,ProductDetails from SC_RENEWAL_TABLE where Product = '{}' and QuoteID = '{}'".format(product_name,reference_number))
		if query is not None:
			var = eval(query.ProductDetails)
			for i in var:
				if i['Type'] == 'Container' and i['Name'] == 'SC_SESP Models Hidden':
					contRows = i['Value']
					for row in contRows:
						MSID	 = str(row['MSID']).strip()
						Platform = str(row['Platform']).strip()
						Model	 = str(row['Model#']).strip()
						Qty		 = int(row['Qty']) if str(row['Qty']).strip() != ''	 else 0
						System_Name = str(row['System_Name']).strip()
						System_Number = str(row['System_Number']).strip()
						Description = row['Description'].strip().replace('‐' , '-')
						#key = "{}|{}|{}|{}|{}|{}".format(MSID, Platform, Model, System_Name, System_Number,Description)
						key = "{}|{}|{}".format(MSID, System_Number, Model)
						qtyDict[key] = Qty
						unitPriceDict[key] = float(row['UnitPrice']) if str(row['UnitPrice']).strip() != ''	 else 0
						listPriceDict[key] = float(row['Price']) if str(row['Price']).strip() != ''	 else 0
						sellPriceDict[key] = 0
						systemNameDict[key] = System_Name
						systemNumberDict[key] = System_Number
						descriptionDict[key] = Description
						pyPartNumbers.append(Model)
						if 'Final Sell Price' in row.keys():
							sellPriceDict[key] = float(row['Final Sell Price']) if row['Final Sell Price'].strip() != '' else 0
	return qtyDict, unitPriceDict, listPriceDict, sellPriceDict, systemNameDict, systemNumberDict, descriptionDict, pyPartNumbers

def updateInvalidModelCont(validModelCont, validModelCont_Hidden, validModelDict, qtyDict, systemNameDict, systemNumberDict, descriptionDict, unitPriceDict, listPriceDict, sellPriceDict, outOfScopeCont, moduleDict):
	for key in qtyDict.keys():
		if key not in validModelDict:
			MSID, Platform, Model = key.split('|')
			if moduleDict.get(Model, '') != "Solution Enhancement Support Program":
				outRow = outOfScopeCont.AddNewRow(False)
				outRow['MSIDs'] = str(MSID)
				outRow['ServiceProduct_Model'] = str(Model)
				outRow['System_Name'] = systemNameDict.get(key, '')
				outRow['System_Number'] = systemNumberDict.get(key, '')
				outRow['Platform'] = Platform
				outRow['Description'] = descriptionDict.get(key, '')
				outRow['Previous Year Quantity'] = str(qtyDict[key])
				outRow['Asset Validation Line Item Number'] = 'New'
				outRow['Renewal Quantity'] = '0'
				outRow['ServiceProduct'] = moduleDict.get(Model, '')
				outRow['PY_UnitPrice'] = str(unitPriceDict.get(key, 0))
				outRow['PY_ListPrice'] = str(listPriceDict.get(key, 0))
				outRow['PY_SellPrice'] = str(sellPriceDict.get(key, 0))
				continue

			row1 = validModelCont.AddNewRow(False)
			row2 = validModelCont_Hidden.AddNewRow(False)
			row2["Asset Validation Line Item Number"]= row1["Asset Validation Line Item Number"] = 'New'
			row2["MSIDs"] = row1["MSIDs"] = MSID
			row2["System_Name"] = row1["System_Name"] = systemNameDict.get(key, '')
			row2["System_Number"] = row1["System_Number"] = systemNumberDict.get(key, '')
			row2["SESP_Models"] = row1["SESP_Models"] = Model
			row2["Platform"] = row1["Platform"] = Platform
			row2["Description"] = row1["Description"] = descriptionDict.get(key, '')
			row2["Quantity"] = row1["Quantity"] = str(qtyDict[key])
			row2["Renewal Quantity"] = row1["Renewal Quantity"] = '0'
			row2["Difference"] =  row1["Difference"] =  str(int(row1['Renewal Quantity'])-int(row1['Quantity']))
			row2["Comments"] = "Scope Addition" if int(row1['Difference'])>0 else "Scope Reduction" if	int(row1['Difference'])<0 else "No Scope Change"
			row2["Previous Year Unit Price"] = row1["Previous Year Unit Price"] = str(unitPriceDict.get(key, 0))
			row2["Previous Year List Price"] = row1["Previous Year List Price"] = str(listPriceDict.get(key, 0))
			row2["PY_SellPrice"] = row1["PY_SellPrice"] = str(sellPriceDict.get(key, 0))
			row1['HiddenRowIndex'] = str(row2.RowIndex)

def assetValidationHeaderData(Product, Quote, TagParserQuote, Session):
	localRef=Quote.GetCustomField("SC_CF_LOCAL_REF").Content
	accountSite=Quote.GetCustomField("Account Site").Content
	assetData = CL_SC_Modules(Quote, TagParserQuote, None,Session)
	#res = assetData.get_AssetValidationHeader_Data1(localRef,accountSite)
	res = assetData.get_AssetValidationHeader_Data_With_HeaderID(localRef,accountSite, Product.Attr('SC_SESP_AVH_Data').SelectedValue.Display if Product.Attr('SC_SESP_AVH_Data').SelectedValue != None else '', Quote.GetCustomField('AccountId').Content)
	return res

def assetValidationHeaderDetails(Product, Quote, TagParserQuote, Session):
	localRef=Quote.GetCustomField("SC_CF_LOCAL_REF").Content
	accountSite=Quote.GetCustomField("Account Site").Content
	assetData = CL_SC_Modules(Quote, TagParserQuote, None,Session)
	apiResponse = assetData.get_AssetValidationHeader_Details(localRef,accountSite)
	if apiResponse and str(apiResponse).Contains('totalSize') and apiResponse.totalSize > 0:
		SCPDD=Quote.QuoteTables['SC_Product_Dynamic_Data']
		SCPDD.Rows.Clear()
		for hrow in apiResponse.records:
			row = SCPDD.AddNewRow()
			row['Product']='SESP'
			row['DisplayValue'] = str(hrow.Name)
			row['DisplayCode'] = str(hrow.Id)
			row['DisplayFilter'] = localRef
		SCPDD.Save()

def insertVRWInfo(Product, Quote, TagParserQuote, Session):
	Exchange_Rate = float(Quote.GetCustomField('SC_CF_PRVYR_EXCH_RATE').Content) if Quote.GetCustomField('SC_CF_PRVYR_EXCH_RATE').Content else 1
	assetDict = dict()
	VRWList = []
	validModelCont1 = Product.GetContainerByName("SC_Models_Scope_Renewal")
	validModelCont2 = Product.GetContainerByName("SC_Models_Scope_Renewal_Hidden")
	outOfScopeCont = Product.GetContainerByName("SC_SESP_OutOfScope_Models")
	Product.Attr("SC_VRW_Error_Msg").AssignValue('')
	res = assetValidationHeaderData(Product, Quote, TagParserQuote, Session)
	if res:
		if res.totalSize > 0:
			partNumbers = []
			qtyDict, unitPriceDict, listPriceDict, sellPriceDict, systemNameDict, systemNumberDict, descriptionDict, partNumbers = getPreviousQuoteInfo(Quote)
			preDateRange = ''
			for asset in res.records:
				assetStatus = str(asset["ContractRenewalHeaderId__r"]["Status__c"])
				dateRange = str(asset["ContractRenewalHeaderId__r"]["StartDate__c"])+'||'+str(asset["ContractRenewalHeaderId__r"]["EndDate__c"])
				if preDateRange != '' and preDateRange != dateRange:
					break
				else:
					preDateRange = dateRange
				if assetStatus.lower() in ['asset validation completed', 'amendment completed']:
					nestDict = dict()
					nestDict["Asset Validation Line Item Number"] = str(asset["Name"])
					nestDict["System_Name"] = str(asset["SysName__c"])
					nestDict["System_Number"] = str(asset["SystemNumber__c"])
					nestDict["Platform"] = str(asset["Platform__c"])
					partNumbers.append(str(asset['SESP_Model_Num__c']))
					nestDict["SESP_Models"] = str(asset["SESP_Model_Num__c"])
					nestDict["Quantity"] = '0' #str(asset["Quantity__c"]) if str(asset["Quantity__c"]).strip() != '' else '0'
					nestDict["Renewal Quantity"] = str(asset["Renewal_Quantity__c"]) if str(asset["Renewal_Quantity__c"]).strip() != '' else '0'
					MSID = str(asset["MSID__r"]["Name"])
					nestDict["Description"] = ''
					key = "{}|{}|{}".format(MSID, nestDict["System_Number"], nestDict["SESP_Models"])
					assetDict[key] = nestDict
				else:
					Product.Attr("SC_VRW_Error_Msg").AssignValue('Asset Validation is in progress')
					break

			if len(partNumbers):
				descDict, platformDict, moduleDict = getModelDetails(partNumbers)
				#update quantiy, platform, and description
				for key in assetDict.keys():
					MSID = key.split('|')[0]
					Model = key.split('|')[2]
					nestDict = assetDict[key]
					platform = str(nestDict["Platform"])
					System_Name = str(nestDict["System_Name"])
					System_Number = str(nestDict["System_Number"])
					if platform.strip() == '':
						nestDict['Platform'] = platformDict.get(Model, '')
					if nestDict['Description'] == '':
						nestDict['Description'] = descDict.get(Model, '')
					dictKey = "{}|{}|{}".format(str(MSID).strip(), str(nestDict["System_Number"]).strip(), str(Model).strip())
					if moduleDict.get(Model, '') != "Solution Enhancement Support Program":
						outRow = outOfScopeCont.AddNewRow(False)
						outRow['MSIDs'] = str(MSID)
						outRow['ServiceProduct_Model'] = str(Model)
						outRow['System_Name'] = System_Name
						outRow['System_Number'] = System_Number
						outRow['Platform'] = nestDict['Platform']
						outRow['Description'] = nestDict['Description']
						outRow['Previous Year Quantity'] = nestDict["Quantity"]
						outRow['Asset Validation Line Item Number'] = nestDict["Asset Validation Line Item Number"]
						outRow['Renewal Quantity'] = nestDict["Renewal Quantity"]
						outRow['ServiceProduct'] = moduleDict.get(Model, '')
						outRow['PY_UnitPrice'] = str(unitPriceDict.get(dictKey, 0))
						outRow['PY_ListPrice'] = str(listPriceDict.get(dictKey, 0))
						outRow['PY_SellPrice'] = str(sellPriceDict.get(dictKey, 0))
						continue
					#dictKey = "{}|{}|{}|{}|{}|{}".format(str(MSID).strip(), str(nestDict['Platform']).strip(), str(Model).strip(), str(System_Name).strip(), str(System_Number).strip(), nestDict['Description'])
					
					preQuoteQty = qtyDict.get(dictKey, 0)
					if preQuoteQty > 0:
						nestDict["Quantity"] = str(qtyDict.get(dictKey, 0))
					nestDict["Previous Year Unit Price"] = str(unitPriceDict.get(dictKey, 0))
					nestDict["Previous Year List Price"] = str(listPriceDict.get(dictKey, 0))
					nestDict["PY_SellPrice"] = str(sellPriceDict.get(dictKey, 0))
					row1 = validModelCont1.AddNewRow(False)
					row2 = validModelCont2.AddNewRow(False)
					row1['MSIDs'] = row2['MSIDs'] = str(MSID)
					for col in nestDict.keys():
						if col not in ['Quantity', 'Renewal Quantity', 'Previous Year Unit Price', 'Previous Year List Price', 'PY_SellPrice']:
							row1[col] = row2[col] = nestDict.get(col, '')
						elif col in	 ['Quantity', 'Renewal Quantity']:
							qty = nestDict.get(col, '0')
							qty = 0 if str(qty).strip() == '' else int(float(qty))
							row1[col] = row2[col] = str(qty)
						else:
							price = float(nestDict.get(col, '0')) * Exchange_Rate
							row1[col] = row2[col] = str(price)
					row1['Difference'] = str(int(row1['Renewal Quantity'])-int(row1['Quantity']))
					row2['Difference'] =  row1['Difference']
					row1["Comments"] = "Scope Addition" if int(row1['Difference'])>0 else "Scope Reduction" if	int(row1['Difference'])<0 else "No Scope Change"
					row2["Comments"] = row1["Comments"]
					row1['HiddenRowIndex'] = str(row2.RowIndex)
					VRWList.append(dictKey)
				#Available in Previous Year Quote but not available in VRW
				if len(qtyDict) > 0:
					updateInvalidModelCont(validModelCont1, validModelCont2, VRWList, qtyDict, systemNameDict, systemNumberDict, descriptionDict, unitPriceDict, listPriceDict, sellPriceDict, outOfScopeCont, moduleDict)

def updateVRWInfo(Product, Quote, assetDict, partNumbers):
	validModelCont1 = Product.GetContainerByName("SC_Models_Scope_Renewal")
	validModelCont2 = Product.GetContainerByName("SC_Models_Scope_Renewal_Hidden")
	outOfScopeCont = Product.GetContainerByName("SC_SESP_OutOfScope_Models")
	deleteOutOfScopeRecord(outOfScopeCont)
	Slevel = ''
	Coverage = ''
	SC_Configured_PY_Sell_Price = 0
	descDict, platformDict, moduleDict = getModelDetails(partNumbers)
	for asset in assetDict.keys():
		rowDict = assetDict[asset]
		MSID = asset.split('|')[0]
		SysNumber = asset.split('|')[1]
		SESP_Models = asset.split('|')[2]
		isAssetModelAlreadyExists = False
		Slevel = rowDict['Slevel']
		Coverage = rowDict['Coverage7_24']
		platform = str(rowDict["Platform"])
		SC_Configured_PY_Sell_Price += float(rowDict['PY_SellPrice']) if str(rowDict['PY_SellPrice']).strip() != '' else 0
		for row in validModelCont1.Rows:
			if MSID == row['MSIDs'] and SESP_Models == row['SESP_Models'] and SysNumber == row['System_Number']:
				row['Quantity'] = rowDict.get('Quantity', '0')
				if str(row['Renewal Quantity']).strip() == '':
					row['Renewal Quantity'] = '0'
				row['Previous Year Unit Price'] = str(rowDict.get('Previous Year Unit Price', '0'))
				row['Previous Year List Price'] = str(rowDict.get('Previous Year List Price', '0'))
				row['PY_SellPrice'] = str(rowDict.get('PY_SellPrice', '0'))
				row['Difference'] = str(int(row['Renewal Quantity'])-int(rowDict.get('Quantity', '0')))
				row["Comments"] = "Scope Addition" if int(row['Difference'])>0 else "Scope Reduction" if  int(row['Difference'])<0 else "No Scope Change"
				isAssetModelAlreadyExists = True
				row.Calculate()
				break
		for row in validModelCont2.Rows:
			if MSID == row['MSIDs'] and SESP_Models == row['SESP_Models'] and SysNumber == row['System_Number']:
				row['Quantity'] = rowDict.get('Quantity', '0')
				if str(row['Renewal Quantity']).strip() == '':
					row['Renewal Quantity'] = '0'
				row['Previous Year Unit Price'] = str(rowDict.get('Previous Year Unit Price', '0'))
				row['Previous Year List Price'] = str(rowDict.get('Previous Year List Price', '0'))
				row['PY_SellPrice'] = str(rowDict.get('PY_SellPrice', '0'))
				row['Difference'] = str(int(row['Renewal Quantity'])-int(rowDict.get('Quantity', '0')))
				row["Comments"] = "Scope Addition" if int(row['Difference'])>0 else "Scope Reduction" if  int(row['Difference'])<0 else "No Scope Change"
				isAssetModelAlreadyExists = True
				row.Calculate()
				break
		if not isAssetModelAlreadyExists:
			if moduleDict.get(SESP_Models, '') != "Solution Enhancement Support Program":
				outRow = None
				for row in outOfScopeCont.Rows:
					if MSID == row['MSIDs'] and SESP_Models == row['ServiceProduct_Model'] and SysNumber == row['System_Number']:
						outRow = row
				if not outRow:
					outRow = outOfScopeCont.AddNewRow(False)
				outRow['MSIDs'] = str(MSID)
				outRow['ServiceProduct_Model'] = str(SESP_Models)
				outRow['System_Name'] = outRow['System_Name'] if outRow['System_Name'] else str(rowDict.get('System_Name', '0'))
				outRow['System_Number'] = outRow['System_Number'] if outRow['System_Number'] else str(rowDict.get('System_Number', '0'))
				outRow['Platform'] = outRow['Platform'] if outRow['Platform'] else platformDict.get(SESP_Models, '')
				outRow['Description'] = outRow['Description'] if outRow['Description'] else descDict.get(SESP_Models, '')
				outRow['Previous Year Quantity'] = str(rowDict.get('Quantity', '0'))
				outRow['Asset Validation Line Item Number'] = outRow['Asset Validation Line Item Number'] if outRow['Asset Validation Line Item Number'] else 'New'
				outRow['Renewal Quantity'] = outRow['Renewal Quantity'] if outRow['Renewal Quantity'] else str(rowDict.get('Renewal Quantity', '0'))
				outRow['ServiceProduct'] = moduleDict.get(SESP_Models, '')
				outRow['PY_UnitPrice'] = str(rowDict.get('Previous Year Unit Price', '0'))
				outRow['PY_ListPrice'] = str(rowDict.get('Previous Year List Price', '0'))
				outRow['PY_SellPrice'] = str(rowDict.get('PY_SellPrice', '0'))
				continue
			row1 = validModelCont1.AddNewRow(False)
			row2 = validModelCont2.AddNewRow(False)
			row1["Asset Validation Line Item Number"] = 'New'
			row2["Asset Validation Line Item Number"] = 'New'
			row1['Quantity'] = '0'
			row2['Quantity'] = row1['Quantity']
			for col in rowDict.keys():
				if col not in ['Quantity', 'Renewal Quantity', 'Slevel', 'Previous Year Unit Price', 'Previous Year List Price', 'PY_SellPrice', 'Coverage7_24']:
					row1[col] = row2[col] = rowDict.get(col, '')
				elif col in ['Quantity', 'Renewal Quantity', 'Previous Year Unit Price', 'Previous Year List Price', 'PY_SellPrice']:
					row1[col] = row2[col] = str(rowDict.get(col, '0'))
			diff = int(row1['Renewal Quantity'])-int(row1['Quantity'])
			row1['Difference'] = row2['Difference'] = str(diff)
			row1["Comments"] = "Scope Addition" if int(diff)>0 else "Scope Reduction" if  int(diff)<0 else "No Scope Change"
			row2["Comments"] = row1["Comments"]
			row1['HiddenRowIndex'] = str(row2.RowIndex)
			row1.Calculate()
	validModelCont1.Calculate()
	Product.Attr('SC_Service_Product').SelectDisplayValue(Slevel, False)
	PY_Coverage = '24x7' if Coverage == 'Yes' else '8x5'
	Product.Attr('SC_Coverage').SelectDisplayValue(PY_Coverage, False)
	Product.Attr('PY_SC_Coverage').AssignValue(PY_Coverage)

def deleteExistingRecords(contList):
	for cont in contList:
		rows_to_delete = []
		for row in cont.Rows:
			avlin = str(row['Asset Validation Line Item Number']).strip()
			if avlin != 'New':
				rows_to_delete.append(row.RowIndex)
		rows_to_delete.sort(reverse=True)
		for x in rows_to_delete:
			cont.DeleteRow(x)

def deleteExistingRecord(ModelCont, ModelContHidden, SearchText):
	rows_to_delete = []
	for row in ModelContHidden.Rows:
		avlin = str(row['Asset Validation Line Item Number']).strip()
		if avlin != 'New':
			rows_to_delete.append(row.RowIndex)
	rows_to_delete.sort(reverse=True)
	for x in rows_to_delete:
		ModelContHidden.DeleteRow(x)
	ModelCont.Clear()
	for row in ModelContHidden.Rows:
		if SearchText == "" or SearchText == None or SearchText.lower() in row['MSIDs'].lower():
			i = ModelCont.AddNewRow(False)
			i['Asset Validation Line Item Number']=row['Asset Validation Line Item Number']
			i['MSIDs'] = row['MSIDs']
			i['System_Name'] = row['System_Name']
			i['System_Number'] = row['System_Number']
			i['Platform'] = row['Platform']
			i['SESP_Models'] = row['SESP_Models']
			i['Description'] = row['Description']
			i['Quantity'] = row['Quantity']
			i['Previous Year Unit Price'] = row['Previous Year Unit Price']
			i['Previous Year List Price'] = row['Previous Year List Price']
			i['Renewal Quantity']=row['Renewal Quantity']
			i['Comments']=row['Comments']
			i['Difference']=row['Difference']
			i['HiddenRowIndex'] = str(row.RowIndex)

def deleteOutOfScopeRecord(cont, deleteNew = True):
	rows_to_delete = []
	for row in cont.Rows:
		avlin = str(row['Asset Validation Line Item Number']).strip()
		if deleteNew:
			if avlin == 'New':
				rows_to_delete.append(row.RowIndex)
		else:
			if avlin != 'New':
				rows_to_delete.append(row.RowIndex)
	rows_to_delete.sort(reverse=True)
	for x in rows_to_delete:
		cont.DeleteRow(x)

def refreshVRWInfo(Product, Quote, TagParserQuote, Session):
	SC_VRW_Error_Msg = Product.Attr("SC_VRW_Error_Msg").GetValue()
	validModelCont1 = Product.GetContainerByName("SC_Models_Scope_Renewal")
	validModelCont2 = Product.GetContainerByName("SC_Models_Scope_Renewal_Hidden")
	outOfScopeCont = Product.GetContainerByName("SC_SESP_OutOfScope_Models")
	deleteExistingRecord(validModelCont1,validModelCont2, Product.Attr('SC_MSID_Search_Sope_Selection').GetValue())
	deleteOutOfScopeRecord(outOfScopeCont, False)
	insertVRWInfo(Product, Quote, TagParserQuote, Session)

def readExcelData(Workbook, SheetName, Product, PriceMultiplier):
	Sheet = Workbook.GetSheet(str(SheetName)).Cells
	LastCellPosition = Sheet.GetLastColumnPosition + str(Sheet.GetRowCount)
	Models = Sheet.GetRange("A1",LastCellPosition)
	Trace.Write("count:{} pos:{}".format(Sheet.GetRowCount, LastCellPosition))
	ModelsCount = Sheet.GetRowCount
	assetDict = dict()
	partNumbers = []
	discount = 0
	comparisonCont = Product.GetContainerByName('ComparisonSummary')
	if comparisonCont.Rows.Count:
		row = comparisonCont.Rows[0]
		discount = float(row['PY_Discount_SFDC']) if row['PY_Discount_SFDC'].strip() != '' else 0
	for i in range(1,ModelsCount):
		nestDict = dict()
		nestDict["MSIDs"]			= str(Models[i,0].encode("ascii", "replace").replace('?','')).strip()
		"""Lst = str(Models[i,1]).strip().split('#')
		nestDict["System_Name"]		= Lst[0]
		nestDict["System_Number"]	= ''
		if len(Lst) == 2:
			nestDict["System_Number"]	= Lst[1]"""
		nestDict["System_Name"]		= str(Models[i,1].encode("ascii", "replace").replace('?','')).strip()
		nestDict["System_Number"]	= str(Models[i,2].encode("ascii", "replace").replace('?','')).strip()
		nestDict["Platform"]		= str(Models[i,3].encode("ascii", "replace").replace('?','')).strip()
		nestDict["SESP_Models"]		= str(Models[i,4].encode("ascii", "replace").replace('?','')).strip()
		nestDict["Description"]		= str(Models[i,5].encode("ascii", "replace").replace('?','')).strip()
		nestDict["Quantity"]		= str(Models[i,6].encode("ascii", "replace").replace('?','')).strip() if str(Models[i,6].encode("ascii", "replace").replace('?','')).strip() != '' else 0
		nestDict["Renewal Quantity"]= '0'
		nestDict["Slevel"]			= str(Models[i,7].encode("ascii", "replace").replace('?','')).strip()
		PY_ListPrice = str(Models[i,9].encode("ascii", "replace").replace('?','')).strip() if str(Models[i,9].encode("ascii", "replace").replace('?','')).strip() != '' else 0
		nestDict["Previous Year List Price"] = str((float(PY_ListPrice) * PriceMultiplier))
		nestDict["Previous Year Unit Price"] = '0'
		if float(nestDict["Previous Year List Price"]) > 0 and float(nestDict["Quantity"]) > 0:
			nestDict["Previous Year Unit Price"] = str((float(nestDict["Previous Year List Price"])/float(nestDict["Quantity"])))
		##Trace.Write(str(nestDict["Previous Year Unit Price"]))
		##pyListPrice = float(nestDict["Previous Year List Price"])
		##pySellPrice = pyListPrice-(pyListPrice*discount)
		PY_SellPrice = str(Models[i,10].encode("ascii", "replace").replace('?','')).strip() if str(Models[i,10].encode("ascii", "replace").replace('?','')).strip() != '' else 0
		nestDict["PY_SellPrice"] = str((float(PY_SellPrice) * PriceMultiplier))
		nestDict["Coverage7_24"]	= str(Models[i,13].encode("ascii", "replace").replace('?','')).strip()
		key = "{}|{}|{}".format(nestDict["MSIDs"], nestDict["System_Number"], nestDict["SESP_Models"])
		assetDict[key] = nestDict
		partNumbers.append(str(nestDict["SESP_Models"]))
	return assetDict, partNumbers