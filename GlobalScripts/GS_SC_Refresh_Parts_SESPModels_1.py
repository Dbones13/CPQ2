from CPQ_SF_SC_Modules import CL_SC_Modules
a= Product.Attr('SC_Product_Type').GetValue()
errorList=[err for err in Product.Attr('Error_Message').GetValue().split(',') if err and not err.Trim().startswith('Error in Dynamic price calculation for Model: ')]
Product.Attr('Error_Message').AssignValue('')

quoteCurrency = Quote.SelectedMarket.CurrencyCode
#query = SqlHelper.GetFirst("select Exchange_Rate from Currency_ExchangeRate_Mapping where From_Currency = 'USD' and To_Currency = '{}'".format(quoteCurrency))
#Exchange_Rate = float(query.Exchange_Rate)
exRate = float(Quote.GetCustomField('SC_CF_EXCHANGE_RATE').Content)
pexRate = float(Quote.GetCustomField('SC_CF_PRVYR_EXCHANGE_RATE').Content) if Quote.GetCustomField('SC_CF_PRVYR_EXCHANGE_RATE').Content not in (None, "") else exRate
fxFactor = 1 if (Product.Attr('SESP_FxRate').GetValue() if Product.Attributes.GetByName('SESP_FxRate') else '') else exRate/pexRate if pexRate>0 else 1
def getPartNumberQty(dypartNumber, partNumber, pQty):
	if not (pQty and partNumber):
		return pQty
	pData = SqlHelper.GetFirst("select PartNumber, BaseQuantity from SC_PRICING_SESP where SC_DYNAMIC_MODEL <> '{0}' and PartNumber='{0}' and PriceDate <= GETDATE()".format(partNumber))
	rQty=1
	if pData:
		rQty = pData.BaseQuantity
	return rQty * pQty

def GetDynamicPrice(partNumber, pQty):
	try:
		if not (pQty and partNumber):
			return 0, 'True'
		pPrice = 0
		gQty = pQty
		if partNumber:
			pData = SqlHelper.GetList("select PartNumber,Platform,BasePrice,Description, PriceType, BaseQuantity, MinQuantity, MaxQuantity from SC_PRICING_SESP where SC_DYNAMIC_MODEL = '{0}' and PartNumber<>'{0}' and PriceDate <= GETDATE()".format(partNumber))
			pDict={}
			for trow in pData:
				pDict[trow.BaseQuantity] = float(trow.BasePrice)
			minQty = min(pDict, key=pDict.get)
			kCnt=0
			while gQty>0 and kCnt<pQty:
				mQty = max(filter(lambda val: val <= gQty, pDict.keys()))
				if minQty == mQty:
					pPrice = pPrice + pDict[mQty] * gQty/minQty
					gQty = 0
				else:
					pPrice += pDict[mQty]
					gQty = gQty-mQty
				kCnt+=1
		pStatus = 'True'
		return pPrice/pQty, 'True'
	except:
		pStatus = 'Error in Dynamic price calculation for Model: ' + partNumber
	return 0, pStatus

#if a=="New":
contract_duration = Quote.GetCustomField('SC_CF_CONTRACTDURYR').Content.split('.')[0] if Quote.GetCustomField('SC_CF_CONTRACTDURYR').Content !='' else '0'
if a != "Renewal":
# Dynamic Price calculation method
	class_contact_modules = CL_SC_Modules(Quote, TagParserQuote, None, Session)
	AccountName = Quote.GetCustomField('Account Name').Content
	AccountId = Quote.GetCustomField('AccountId').Content
	#AccountSite = Quote.GetCustomField('Account Site').Content
	pAccountName = Quote.GetCustomField('SC_CF_PARENT_ACCOUNT_NAME').Content
	isParent = False
	selectedSites = Product.Attr('SC_MultiSites_Selected').GetValue()
	AccountSite = selectedSites.split('<,>')
	if not pAccountName:
		isParent = True
	MSID_Cont = Product.GetContainerByName('SC_Select_MSID_Cont_Hidden')
	SESP_Models_Cont = Product.GetContainerByName('SC_SESP Models')
	SESP_Models_Cont.Clear()
	SESP_Models_Hid_Cont = Product.GetContainerByName('SC_SESP Models Hidden')
	SESP_Models_Hid_Cont.Clear()

	Selected_MSID = []
	Models_Summary = []
	#MSIDTable=class_contact_modules.get_site_assets(AccountName, AccountSite)
	bundlePricingDict = {'sesp value plus':0.91, 'sesp value remote plus':1, 'value shield': 0.64, 'system evolution program': 0.3, 'unlimited migrations support service': 0.085}
	bundlePricingDict['system evolution program'] = 0.2 if int(contract_duration) >=5 else 0.3
	for row in MSID_Cont.Rows:
		if row.IsSelected == True:
			Selected_MSID.append(row['MSIDs'])
	if Selected_MSID:
		SummaryTable=class_contact_modules.get_siteID_assets(AccountId, AccountSite, Selected_MSID, isParent)
		for models in SummaryTable.records:
			msid_name  = models.Parent['Name']
			sys_name = models.Parent['ProductCode']
			i = SESP_Models_Cont.AddNewRow(False)
			hRow = SESP_Models_Hid_Cont.AddNewRow(False)
			hRow['MSID'] = i['MSID']  = msid_name.ToString()
			hRow['MSID_SFDC_ID'] = i['MSID_SFDC_ID']  = models.Parent['Id'].ToString()
			hRow['Model_SFDC_ID'] = i['Model_SFDC_ID']	= str(models.Id)
			hRow['Model#'] = i['Model#'] = str(models.ProductCode)
			hRow['System_Name'] = i['System_Name'] = sys_name.ToString()
			hRow['System_Number'] = i['System_Number'] = str(models.SiteLicSeqSys__c)
			hRow['Description'] = i['Description'] = str(models.Name)
			hRow['Qty'] = i['Qty'] = str(models.Quantity)
			hRow['UnitPrice'] = i['UnitPrice'] = '0'
			hRow['Price'] = i['Price'] = '0'
			Models_Summary.append(str(models.ProductCode))

	# to load Model summary container from Models scope container:
	mc = Product.GetContainerByName('SC_Models_Scope')
	for i in mc.Rows:
		#if i.IsSelected == True:
		j = SESP_Models_Cont.AddNewRow(False)
		hRow = SESP_Models_Hid_Cont.AddNewRow(False)
		hRow['MSID'] = j['MSID'] = i['MSIDs']
		hRow['System_Name'] = j['System_Name'] = i['System_Name']
		hRow['System_Number'] = j['System_Number'] = i['System_Number']
		hRow['Platform'] = j['Platform'] = i['Platform']
		hRow['Model#'] = j['Model#'] = i['SESP_Models']
		hRow['Description'] = j['Description'] = i['Description']
		hRow['Qty'] = j['Qty'] = i['Quantity']
		hRow['UnitPrice'] = j['UnitPrice'] = '0'
		hRow['Price'] = j['Price'] = '0'
		Models_Summary.append(str(i['SESP_Models']))

	if Models_Summary:
		pData = SqlHelper.GetList("select PartNumber, Description, SC_DYNAMIC_MODEL from SC_PRICING_SESP where PartNumber IN {} and PriceDate <= GETDATE() and SC_DYNAMIC_MODEL <> ''".format(str(tuple(Models_Summary)).replace(',)',')')))
		dyModel = {}
		dyModelDescription = {}
		dyModelList = []
		#Trace.Write("SC_DYNAMIC_MODEL " +str(trow.SC_DYNAMIC_MODEL))
		for trow in pData:
			dyModel[trow.PartNumber] = trow.SC_DYNAMIC_MODEL
			dyModel[trow.SC_DYNAMIC_MODEL] = trow.SC_DYNAMIC_MODEL
			dyModelList.append(trow.SC_DYNAMIC_MODEL)
		if dyModelList:
			pData = SqlHelper.GetList('select PartNumber, Description, SC_DYNAMIC_MODEL from SC_PRICING_SESP where PartNumber IN {} and PriceDate <= GETDATE()'.format(str(tuple(dyModelList)).replace(",)",")")))
			for trow in pData:
				dyModelDescription[trow.PartNumber] = trow.Description
			dyModelIndex = {}
			dyModelValues = {}
			for cRow in SESP_Models_Cont.Rows:
				if cRow['Model#'] in dyModel:
					if cRow['MSID'] + '<->' + dyModel[cRow['Model#']] in dyModelIndex:
						dyModelIndex[cRow['MSID'] + '<->' + dyModel[cRow['Model#']]].append(cRow.RowIndex)
					else:
						dyModelIndex[cRow['MSID'] + '<->' + dyModel[cRow['Model#']]] = [cRow.RowIndex]

			deleteIndexList = []
			dfpg=str(dyModelIndex)
			for mkey in dyModelIndex:
				if len(dyModelIndex[mkey])>0:
					for mIndex in dyModelIndex[mkey]:
						mData = SESP_Models_Cont.Rows[mIndex]
						if mkey in dyModelValues:
							dyModelValues[mkey]['Qty'] = getPartNumberQty(dyModel[mData['Model#']], mData['Model#'], int(mData['Qty'])) + dyModelValues[mkey]['Qty']
							dyModelValues[mkey]['UnitPrice'] = round((float(mData['UnitPrice']) + dyModelValues[mkey]['UnitPrice'])/2, 2)
							dyModelValues[mkey]['Price'] = round(float(mData['Price']) + dyModelValues[mkey]['Price'], 2)
						else:
							dyModelValues[mkey] = {'MSID': mData['MSID'], 'MSID_SFDC_ID': mData['MSID_SFDC_ID'], 'Model_SFDC_ID': mData['Model_SFDC_ID'], 'Platform': mData['Platform'], 'Model#': dyModel[mData['Model#']], 'System_Name': mData['System_Name'], 'System_Number': mData['System_Number'], 'Description': dyModelDescription[dyModel[mData['Model#']]], 'Qty': getPartNumberQty(dyModel[mData['Model#']], mData['Model#'], int(mData['Qty'])), 'UnitPrice': float(mData['UnitPrice']), 'Price': float(mData['Price'])}
						deleteIndexList.append(mIndex)
			if deleteIndexList:
				deleteIndexList.sort(reverse=True)
			for i in deleteIndexList:
				SESP_Models_Cont.DeleteRow(i)
				SESP_Models_Hid_Cont.DeleteRow(i)
			for kval in dyModelValues:
				cRow = SESP_Models_Cont.AddNewRow(False)
				hRow = SESP_Models_Hid_Cont.AddNewRow(False)
				hRow['MSID'] = cRow['MSID'] = dyModelValues[kval]['MSID']
				hRow['System_Name'] = cRow['System_Name'] = dyModelValues[kval]['System_Name']
				hRow['System_Number'] = cRow['System_Number'] = dyModelValues[kval]['System_Number']
				hRow['Platform'] = cRow['Platform'] = dyModelValues[kval]['Platform']
				hRow['Model#'] = cRow['Model#'] = dyModelValues[kval]['Model#']
				hRow['Description'] = cRow['Description'] = dyModelValues[kval]['Description']
				hRow['Qty'] = cRow['Qty'] = str(dyModelValues[kval]['Qty'])
				hRow['UnitPrice'] = cRow['UnitPrice'] = str(dyModelValues[kval]['UnitPrice'])
				hRow['Price'] = cRow['Price'] = str(dyModelValues[kval]['Price'])
				Models_Summary.append(str(dyModelValues[kval]['Model#']))

	if Models_Summary:
		cFactor = 1.1 if Product.Attr('SC_Coverage').GetValue().lower() == '24x7' else 1
		bFactor = bundlePricingDict[Product.Attr('SC_Service_Product').GetValue().lower()] if Product.Attr('SC_Service_Product').GetValue().lower()in bundlePricingDict else 1
		pData = SqlHelper.GetList("select PartNumber, Platform, BasePrice, Description, PriceType from SC_PRICING_SESP where PartNumber IN {} and PriceDate <= GETDATE()".format(str(tuple(Models_Summary)).replace(',)',')')))
		for val in pData:
			BasePrice = val.BasePrice
			for j in SESP_Models_Cont.Rows:
				if j['Model#'] == val.PartNumber:
					if val.PriceType == 'Dynamic':
						BasePrice, pStatus = GetDynamicPrice(val.PartNumber, int(j['Qty']))
						if pStatus != 'True':
							errorList.append(pStatus)
					j['Platform'] = str(val.Platform)
					j['UnitPrice'] = str(round(((BasePrice *bFactor) * cFactor * exRate),2))
					j['Price'] = str(round((((BasePrice *bFactor) * cFactor * exRate)* int(j['Qty'])),2))
					SESP_Models_Hid_Cont.Rows[j.RowIndex]['Platform'] = j['Platform']
					SESP_Models_Hid_Cont.Rows[j.RowIndex]['UnitPrice'] = j['UnitPrice']
					SESP_Models_Hid_Cont.Rows[j.RowIndex]['Price'] = j['Price']
	SESP_Models_Cont.Calculate()
	SESP_Models_Hid_Cont.Calculate()
	if errorList:
		Product.Attr('Error_Message').AssignValue(Product.Attr('Error_Message').GetValue() + ', ' + ', '.join(errorList) if Product.Attr('Error_Message').GetValue() else ', '.join(errorList))


else:
	Product.Attributes.GetByName('SC_SESP Models').Allowed=False
	class_contact_modules = CL_SC_Modules(Quote, TagParserQuote, None, Session)
	AccountName = Quote.GetCustomField('Account Name').Content
	AccountId = Quote.GetCustomField('AccountId').Content
	#AccountSite = Quote.GetCustomField('Account Site').Content
	pAccountName = Quote.GetCustomField('SC_CF_PARENT_ACCOUNT_NAME').Content
	isParent = False
	selectedSites = Product.Attr('SC_MultiSites_Selected').GetValue()
	AccountSite = selectedSites.split('<,>')
	if not pAccountName:
		isParent = True
	MSID_Cont = Product.GetContainerByName('SC_Select_MSID_Cont_Hidden')
	Selected_MSID = []
	Models_Summary = []
	bundlePricingDict = {'sesp value plus':0.91, 'sesp value remote plus':1, 'value shield': 0.64,'sesp software flex':0.77,'sesp support flex':0.64, 'system evolution program': 0.3, 'unlimited migrations support service': 0.085}
	bundlePricingDict['system evolution program'] = 0.2 if int(contract_duration) >=5 else 0.3
	validModelCont1 = Product.GetContainerByName("SC_Models_Scope_Renewal_Hidden")
	summary= Product.GetContainerByName("SC_SESP Models_Renewal")
	SC_Coverage=Product.Attr('SC_Coverage').GetValue()
	Product.Attr('SC_Coverage_Model').AssignValue(SC_Coverage)
	Product.Attr('SC_Service_Product_Model').Access = AttributeAccess.ReadOnly
	Product.Attr('SC_Service_Product_Model').AssignValue(Product.Attr('SC_Service_Product').GetValue())
	Product.Attr('SC_Coverage_Model').Access = AttributeAccess.ReadOnly
	SC_Service_Product = Product.Attr('SC_Service_Product').GetValue().lower()
	CY_Service_Product = ''
	Pre_Service_Product = ''

	comparisonCont = Product.GetContainerByName('ComparisonSummary')
	compDict = {}
	if comparisonCont.Rows.Count:
		for compRow in comparisonCont.Rows:
			compDict[compRow["Service_Product"]] = compRow["PY_Discount_SFDC"] if compRow["PY_Discount_SFDC"] else '0'
			CY_Service_Product = compRow["CY_Service_Product"].lower() if compRow["CY_Service_Product"] else SC_Service_Product
			Pre_Service_Product = compRow["Service_Product"].lower() if compRow["Service_Product"] else ''
			PY_Coverage = compRow["PY_Coverage"] if compRow["PY_Coverage"] else SC_Coverage

	for row in MSID_Cont.Rows:
		if row.IsSelected == True:
			Selected_MSID.append(row['MSIDs'])
	#To be confirm 
	'''if Selected_MSID:
		SummaryTable=class_contact_modules.get_siteID_assets(AccountId, AccountSite, Selected_MSID, isParent)
		for models in SummaryTable.records:
			msid_name  = models.Parent['Name']
			sys_name = models.Parent['ProductCode']
			summ=summary.AddNewRow(False)
			Trace.Write("test"+str(msid_name))'''
	# to load Model summary container from Models scope container:	 
	SESP_Models_Hid_Cont = Product.GetContainerByName('SC_SESP Models Hidden')
	summary.Clear()
	SESP_Models_Hid_Cont.Clear()
	outOfScopeCont = Product.GetContainerByName("SC_SESP_OutOfScope_Models")

	for row in validModelCont1.Rows:
		if row['MSIDs'] == '':
			continue
		summ=summary.AddNewRow(False)
		summ_hide=SESP_Models_Hid_Cont.AddNewRow(False)
		summ['MSID']=summ_hide['MSID']=row['MSIDs']
		''' Nilesh added code to fetch asset validation line item number in summary container - dt 19082024 '''
		summ['Asset Validation Line Item Number']= summ_hide['Asset Validation Line Item Number'] =  row['Asset Validation Line Item Number']
		Models_Summary.append(str(row['SESP_Models']))
		summ['System_Name']=summ_hide['System_Name']=row['System_Name']
		summ['System_Number']=summ_hide['System_Number']=row['System_Number']
		summ['Platform']=summ_hide['Platform']=row['Platform']
		summ['SESP Model']=summ_hide['Model#']=row['SESP_Models']
		summ['Previous Year Quantity']=summ_hide['Qty']=row['Quantity']
		summ['Renewal Quantity']=summ_hide['Renewal Quantity']=row['Renewal Quantity']
		summ['Previous Year Unit Price']=summ_hide['Previous Year Unit Price']=row['Previous Year Unit Price'] if row['Previous Year Unit Price'] else '0'
		summ['Description']=summ_hide['Description']=row['Description']
		summ['Previous Year List Price']=summ_hide['Previous Year List Price']=row['Previous Year List Price'] if row['Previous Year List Price'] else '0'
		#diff=int(row['Renewal Quantity'])-int(summ['Previous Year Quantity'])
		renewalQty = int(row['Renewal Quantity']) if row['Renewal Quantity'].strip() != '' else 0
		preQty = int(summ['Previous Year Quantity']) if summ['Previous Year Quantity'].strip() != '' else 0
		diff = renewalQty - preQty
		summ['Scope Reduction Quantity']=summ_hide['Scope Reduction Quantity']=str(diff if diff <0 else 0)
		#summ['Scope Reduction Price']=summ_hide['Scope Reduction Price']='-' if diff==0 else str(int(diff)*-1*(float(row['Previous Year List Price'])/int(row['Quantity'])))
		#summ['Escalation %']=summ_hide['Escalation %']=str(10)
		#summ['Escalation Value']=summ_hide['Escalation Value']=str(int(summ['Escalation %']) *float(row['Previous Year Unit Price'])*int(row['Renewal Quantity'])) if row['Comments']=="Scope Addition" else str(int(summ['Escalation %']) *float(row['Previous Year Unit Price'])*int(row['Quantity']))
		summ['Scope Addition Quantity']=summ_hide['Scope Addition Quantity']=str(diff if diff >0 else 0)
		summ['Honeywell List Price Per Unit']=summ_hide['Honeywell List Price Per Unit']='0'
		summ['Comments']=summ_hide['Comments']= row['Comments']

	for row in outOfScopeCont.Rows:
		if row['Platform'].lower() != 'vmware software_001':
			continue
		summ=summary.AddNewRow(False)
		summ_hide=SESP_Models_Hid_Cont.AddNewRow(False)
		summ['MSID']=summ_hide['MSID']=row['MSIDs']
		summ['Asset Validation Line Item Number']= summ_hide['Asset Validation Line Item Number'] =  row['Asset Validation Line Item Number']
		Models_Summary.append(str(row['ServiceProduct_Model']))
		summ['System_Name']=summ_hide['System_Name']=row['System_Name']
		summ['System_Number']=summ_hide['System_Number']=row['System_Number']
		summ['Platform']=summ_hide['Platform']=row['Platform']
		summ['SESP Model']=summ_hide['Model#']=row['ServiceProduct_Model']
		summ['Previous Year Quantity']=summ_hide['Qty']=row['Previous Year Quantity']
		summ['Renewal Quantity']=summ_hide['Renewal Quantity']= '0'
		summ['Previous Year Unit Price']=summ_hide['Previous Year Unit Price']=row['PY_UnitPrice'] if row['PY_UnitPrice'] else '0'
		summ['Description']=summ_hide['Description']=row['Description']
		summ['Previous Year List Price']=summ_hide['Previous Year List Price']=row['PY_ListPrice'] if row['PY_ListPrice'] else '0'
		#diff=int(row['Renewal Quantity'])-int(summ['Previous Year Quantity'])
		renewalQty = 0
		preQty = int(summ['Previous Year Quantity']) if summ['Previous Year Quantity'].strip() != '' else 0
		diff = renewalQty - preQty
		summ['Scope Reduction Quantity']=summ_hide['Scope Reduction Quantity']=str(diff if diff <0 else 0)
		#summ['Scope Reduction Price']=summ_hide['Scope Reduction Price']='-' if diff==0 else str(int(diff)*-1*(float(row['Previous Year List Price'])/int(row['Quantity'])))
		#summ['Escalation %']=summ_hide['Escalation %']=str(10)
		#summ['Escalation Value']=summ_hide['Escalation Value']=str(int(summ['Escalation %']) *float(row['Previous Year Unit Price'])*int(row['Renewal Quantity'])) if row['Comments']=="Scope Addition" else str(int(summ['Escalation %']) *float(row['Previous Year Unit Price'])*int(row['Quantity']))
		summ['Scope Addition Quantity']=summ_hide['Scope Addition Quantity']=str(diff if diff >0 else 0)
		summ['Honeywell List Price Per Unit']=summ_hide['Honeywell List Price Per Unit']='0'
		summ['Comments']=summ_hide['Comments']= "Scope Reduction"

		
	if Models_Summary:
		pData = SqlHelper.GetList("select PartNumber, Description, SC_DYNAMIC_MODEL from SC_PRICING_SESP where PartNumber IN {} and PriceDate <= GETDATE() and SC_DYNAMIC_MODEL <> ''".format(str(tuple(Models_Summary)).replace(',)',')')))
		dyModel = {}
		dyModelDescription = {}
		dyModelList = []
		#Trace.Write("SC_DYNAMIC_MODEL " +str(trow.SC_DYNAMIC_MODEL))
		for trow in pData:
			dyModel[trow.PartNumber] = trow.SC_DYNAMIC_MODEL
			dyModel[trow.SC_DYNAMIC_MODEL] = trow.SC_DYNAMIC_MODEL
			dyModelList.append(trow.SC_DYNAMIC_MODEL)
		if dyModelList:
			pData = SqlHelper.GetList('select PartNumber, Description, SC_DYNAMIC_MODEL from SC_PRICING_SESP where PartNumber IN {} and PriceDate <= GETDATE()'.format(str(tuple(dyModelList)).replace(",)",")")))
			for trow in pData:
				dyModelDescription[trow.PartNumber] = trow.Description
			dyModelIndex = {}
			dyModelValues = {}
			for cRow in summary.Rows:
				if cRow['SESP Model'] in dyModel:
					if cRow['MSID'] + '<->' + dyModel[cRow['SESP Model']] in dyModelIndex:
						dyModelIndex[cRow['MSID'] + '<->' + dyModel[cRow['SESP Model']]].append(cRow.RowIndex)
					else:
						dyModelIndex[cRow['MSID'] + '<->' + dyModel[cRow['SESP Model']]] = [cRow.RowIndex]

			deleteIndexList = []
			dfpg=str(dyModelIndex)
			for mkey in dyModelIndex:
				if len(dyModelIndex[mkey])>0:
					for mIndex in dyModelIndex[mkey]:
						mData = summary.Rows[mIndex]
						if mkey in dyModelValues:
							dyModelValues[mkey]['Renewal Quantity'] = getPartNumberQty(dyModel[mData['SESP Model']], mData['SESP Model'], int(mData['Renewal Quantity'])) + dyModelValues[mkey]['Renewal Quantity']
							dyModelValues[mkey]['Honeywell List Price Per Unit'] = (float(mData['Honeywell List Price Per Unit']) + dyModelValues[mkey]['Honeywell List Price Per Unit'])/2
							dyModelValues[mkey]['Previous Year Quantity'] =	  dyModelValues[mkey]['Previous Year Quantity'] + (getPartNumberQty(dyModel[mData['SESP Model']], mData['SESP Model'], int(mData['Previous Year Quantity'])) if mData['SESP Model'] in dyModelList else 0)
							dyModelValues[mkey]['Previous Year Unit Price'] = (float(mData['Previous Year Unit Price'] if mData['Previous Year Unit Price'] else 0) + dyModelValues[mkey]['Previous Year Unit Price'])/2
							dyModelValues[mkey]['Previous Year List Price'] = (float(mData['Previous Year List Price'] if mData['Previous Year List Price'] else 0) + dyModelValues[mkey]['Previous Year List Price'])
							#dyModelValues[mkey]['Price'] = float(mData['Price']) + dyModelValues[mkey]['Price']
						else:
							dyModelValues[mkey] = {'Previous Year Quantity': getPartNumberQty(dyModel[mData['SESP Model']], mData['SESP Model'], int(mData['Previous Year Quantity'])) if mData['SESP Model'] in dyModelList else 0, 'MSID': mData['MSID'], 'Platform': mData['Platform'], 'SESP Model': dyModel[mData['SESP Model']], 'System_Name': mData['System_Name'], 'System_Number': mData['System_Number'], 'Description': dyModelDescription[dyModel[mData['SESP Model']]], 'Renewal Quantity': getPartNumberQty(dyModel[mData['SESP Model']], mData['SESP Model'], int(mData['Renewal Quantity'])), 'Honeywell List Price Per Unit': float(mData['Honeywell List Price Per Unit']), 'Previous Year Unit Price': float(mData['Previous Year Unit Price']) if mData['Previous Year Unit Price'] else 0, 'Previous Year List Price': float(mData['Previous Year List Price']) if mData['Previous Year List Price'] else 0}
						deleteIndexList.append(mIndex)
			if deleteIndexList:
				deleteIndexList.sort(reverse=True)
			for i in deleteIndexList:
				if summary.Rows[i]['SESP Model'] not in dyModelList:
					summary.Rows[i]['Renewal Quantity'] = SESP_Models_Hid_Cont.Rows[i]['Renewal Quantity'] = '0'
					diff=int(summary.Rows[i]['Renewal Quantity'])-int(summary.Rows[i]['Previous Year Quantity'])
					summary.Rows[i]['Scope Reduction Quantity']=SESP_Models_Hid_Cont.Rows[i]['Scope Reduction Quantity']=str(diff if diff <0 else 0)
					summary.Rows[i]['Scope Addition Quantity']=SESP_Models_Hid_Cont.Rows[i]['Scope Addition Quantity']= '0'
					comm="Scope Addition" if int(diff)>0 else "Scope Reduction" if	int(diff)<0 else "No Scope Change"
					summary.Rows[i]['Comments']=SESP_Models_Hid_Cont.Rows[i]['Comments']=comm
				else:
					summary.DeleteRow(i)
					SESP_Models_Hid_Cont.DeleteRow(i)
			ksdk=str(dyModelValues)
			for kval in dyModelValues:
				summ=summary.AddNewRow(False)
				summ_hide=SESP_Models_Hid_Cont.AddNewRow(False)
				summ['MSID']=summ_hide['MSID']=dyModelValues[kval]['MSID']
				Models_Summary.append(str(dyModelValues[kval]['SESP Model']))
				summ['System_Name']=summ_hide['System_Name']=dyModelValues[kval]['System_Name']
				summ['System_Number']=summ_hide['System_Number']=dyModelValues[kval]['System_Number']
				summ['Platform']=summ_hide['Platform']=dyModelValues[kval]['Platform']
				summ['SESP Model']=summ_hide['Model#']=dyModelValues[kval]['SESP Model']
				summ['Previous Year Quantity']=summ_hide['Qty']=str(dyModelValues[kval]['Previous Year Quantity'])
				summ['Renewal Quantity']=summ_hide['Renewal Quantity']=str(dyModelValues[kval]['Renewal Quantity'])
				summ['Previous Year Unit Price']=summ_hide['Previous Year Unit Price']=str(dyModelValues[kval]['Previous Year Unit Price'] if dyModelValues[kval]['Previous Year Unit Price'] else 0)
				summ['Description']=summ_hide['Description']=dyModelValues[kval]['Description']
				summ['Previous Year List Price']=summ_hide['Previous Year List Price']=str(dyModelValues[kval]['Previous Year List Price'])
				diff=int(str(dyModelValues[kval]['Renewal Quantity'])) 
				##summ['Scope Reduction Quantity']=summ_hide['Scope Reduction Quantity']=str(diff if diff <0 else 0)
				#summ['Scope Reduction Price']=summ_hide['Scope Reduction Price']='-' if diff==0 else str(int(diff)*-1*(float(row['Previous Year List Price'])/int(row['Quantity'])))
				#summ['Escalation %']=summ_hide['Escalation %']=str(10)
				#summ['Escalation Value']=summ_hide['Escalation Value']=str(int(summ['Escalation %']) *float(row['Previous Year Unit Price'])*int(row['Renewal Quantity'])) if row['Comments']=="Scope Addition" else str(int(summ['Escalation %']) *float(row['Previous Year Unit Price'])*int(row['Quantity']))
				##summ['Scope Addition Quantity']=summ_hide['Scope Addition Quantity']=str(diff if diff >0 else 0)
				summ['Honeywell List Price Per Unit']=summ_hide['Honeywell List Price Per Unit']='0'
				diff=int(summ['Renewal Quantity'])-int(summ['Previous Year Quantity'])
				comm="Scope Addition" if int(diff)>0 else "Scope Reduction" if	int(diff)<0 else "No Scope Change"
				summ['Scope Addition Quantity']=summ_hide['Scope Addition Quantity']=str(diff if diff >0 else 0)
				summ['Scope Reduction Quantity']=summ_hide['Scope Reduction Quantity']=str(diff if diff <0 else 0)
				summ['Comments']=summ_hide['Comments']=comm

	py_discount = float(compDict.get(Product.Attr('SC_Service_Product').GetValue(),next(iter(compDict.values())) if compDict.values() else 0))

	if Models_Summary:
		xcFactor = 1
		if PY_Coverage.lower() != SC_Coverage.lower():
			if PY_Coverage.lower() == '24x7':
				xcFactor = 1.0/1.1
			elif SC_Coverage.lower() == '24x7':
				xcFactor = 1.1/1.0
		cFactor = 1.1 if Product.Attr('SC_Coverage').GetValue().lower() == '24x7' else 1
		xFactor = bundlePricingDict[Pre_Service_Product] if Pre_Service_Product in bundlePricingDict else 1
		cyFactor = bundlePricingDict[CY_Service_Product] if CY_Service_Product in bundlePricingDict else 1
		bFactor = bundlePricingDict[Product.Attr('SC_Service_Product').GetValue().lower()] if Product.Attr('SC_Service_Product').GetValue().lower()in bundlePricingDict else 1
		xbFactor = cyFactor/xFactor
		#Trace.Write("Pre_Service_Product:{}, CY_Service_Product:{},PY_Coverage:{},  SC_Coverage:{}, cyFactor:{},xcFactor:{}, xFactor:{},bFactor:{} cFactor:{}".format(Pre_Service_Product, CY_Service_Product,PY_Coverage.lower(), SC_Coverage.lower(),cyFactor,xcFactor, xFactor,bFactor,cFactor))
		pData = SqlHelper.GetList("select PartNumber, Platform, BasePrice, Description, PriceType from SC_PRICING_SESP where PartNumber IN {} and PriceDate <= GETDATE()".format(str(tuple(Models_Summary)).replace(',)',')')))
		for val in pData:
			BasePrice = val.BasePrice
			for j in summary.Rows:
				if j['SESP Model'] == val.PartNumber:
					j['Platform'] = str(val.Platform)
					j['Description']=str(val.Description)
					if val.PriceType == 'Dynamic':
						BasePrice, pStatus = GetDynamicPrice(val.PartNumber, int(j['Renewal Quantity']))
						if pStatus != 'True':
							errorList.append(pStatus)
					if Product.Attr('SC_Pricing_Escalation').GetValue() == "Yes":
						if int(j['Renewal Quantity']) > int(j['Previous Year Quantity']):
							qtyDiff = int(j['Renewal Quantity']) - int(j['Previous Year Quantity'])
							prePrice = ((float(j['Previous Year Unit Price']) *xbFactor) * xcFactor) * int(j['Previous Year Quantity']) * fxFactor
							cyPrice = ((BasePrice *cyFactor) * cFactor * exRate) * qtyDiff
							SESP_Models_Hid_Cont.Rows[j.RowIndex]['Price'] = str(prePrice+cyPrice)
						else:
							prePrice = ((float(j['Previous Year Unit Price']) *xbFactor) * xcFactor) * int(j['Renewal Quantity']) * fxFactor
							SESP_Models_Hid_Cont.Rows[j.RowIndex]['Price'] = str(prePrice)
					else:
						SESP_Models_Hid_Cont.Rows[j.RowIndex]['Price'] = str((((BasePrice *bFactor) * cFactor * exRate)* int(j['Renewal Quantity'])))
					j['Honeywell List Price Per Unit'] = str(((BasePrice *bFactor) * cFactor * exRate))
					#j['Price'] = str((((BasePrice *bFactor) * cFactor * exRate)* int(j['Renewal Quantity'])))
					SESP_Models_Hid_Cont.Rows[j.RowIndex]['Platform'] = j['Platform']
					SESP_Models_Hid_Cont.Rows[j.RowIndex]['Honeywell List Price Per Unit'] = j['Honeywell List Price Per Unit']
					SESP_Models_Hid_Cont.Rows[j.RowIndex]['Honeywell List Price'] = str((((BasePrice *bFactor) * cFactor * exRate)* int(j['Renewal Quantity'])))
					##SESP_Models_Hid_Cont.Rows[j.RowIndex]['Price'] = str((((BasePrice *bFactor) * cFactor * exRate)* int(j['Renewal Quantity'])))
					#Trace.Write("XXXXXXX Price: {}, Qty: {}, Price: {}, HW: {}".format(j['Previous Year Unit Price'], j['Renewal Quantity'], SESP_Models_Hid_Cont.Rows[j.RowIndex]['Price'], SESP_Models_Hid_Cont.Rows[j.RowIndex]['Honeywell List Price Per Unit'] ))
					SESP_Models_Hid_Cont.Rows[j.RowIndex]['SR_Price'] = str(float(j['Previous Year Unit Price'])*float(j['Scope Reduction Quantity']))
					SESP_Models_Hid_Cont.Rows[j.RowIndex]['SA_Price'] = str(float(j['Honeywell List Price Per Unit'])*float(j['Scope Addition Quantity']))
					SESP_Models_Hid_Cont.Rows[j.RowIndex]['PY_ListPrice'] = str(float(j['Previous Year List Price'])) if j['Previous Year List Price'] else '0'
					SESP_Models_Hid_Cont.Rows[j.RowIndex]['PY_SellPrice'] = str(float(SESP_Models_Hid_Cont.Rows[j.RowIndex]['PY_ListPrice']) - (float(SESP_Models_Hid_Cont.Rows[j.RowIndex]['PY_ListPrice']) * py_discount))
					if Product.Attr('SC_Pricing_Escalation').GetValue() == "Yes":
						if int(j['Renewal Quantity']) > int(j['Previous Year Quantity']):
							SESP_Models_Hid_Cont.Rows[j.RowIndex]['Escalation_Price'] = str(float(j['Previous Year Quantity'])*float(j['Previous Year Unit Price'])*xbFactor*fxFactor)
							#summ['List Price'] = str((float(summ['Previous Year Quantity'])*float(summ['PY_UnitPrice'])) + ((int(summ['Renewal Quantity']) - int(summ['Previous Year Quantity']))*float(summ['Honeywell List Price Per Unit'])))
						else:
							SESP_Models_Hid_Cont.Rows[j.RowIndex]['Escalation_Price'] = str(float(j['Renewal Quantity'])*float(j['Previous Year Unit Price'])*xbFactor*fxFactor)
							#summ['List Price'] = str(float(summ['Renewal Quantity'])*float(summ['PY_UnitPrice']))
					else:
						SESP_Models_Hid_Cont.Rows[j.RowIndex]['Escalation_Price'] = '0'
						#summ['List Price'] = summ['HW_ListPrice']