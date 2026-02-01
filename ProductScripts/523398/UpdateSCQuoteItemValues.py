from GS_SC_QuoteLinesHelper import CL_SC_QuoteLinesHelper
from GS_SC_UpdateProducts import sc_yearlist
pfList = [] # will have item description
itemDict = {} #key will be description and value will be the item object
guidDict = {} #key will be guid and value will be description
#optionalFlag = False
if Quote.GetCustomField('Quote Type').Content in ('Contract New','Contract Renewal'):
	SC_CF_ContractEndDate = Quote.GetGlobal('SC_CF_ContractEndDate')
	SC_CF_ContractEndDate = DateTime.Parse(SC_CF_ContractEndDate) if (SC_CF_ContractEndDate !='' and SC_CF_ContractEndDate!= None) else None
	Contract_Ed_Dt = UserPersonalizationHelper.CovertToDate(Quote.GetCustomField('EGAP_Contract_End_Date').Content) if Quote.GetCustomField('EGAP_Contract_End_Date').Content else ''
	if Contract_Ed_Dt =='' and Quote.GetCustomField("SC_CF_IS_CONTRACT_EXTENSION").Content =='True':
		Contract_Ed_Dt= SC_CF_ContractEndDate 
	if Quote.GetCustomField("Quote Type").Content == 'Contract Renewal' and ((SC_CF_ContractEndDate and SC_CF_ContractEndDate == Contract_Ed_Dt) or Quote.GetCustomField("SC_CF_IS_CONTRACT_EXTENSION").Content =='True'):
		yearList, dtDict = sc_yearlist(UserPersonalizationHelper.CovertToDate(Quote.GetCustomField('SC_CF_CURANNDELSTDT').Content),  UserPersonalizationHelper.CovertToDate(Quote.GetCustomField('SC_CF_CURANNDELENDT').Content), True)
	else:
		yearList, dtDict = sc_yearlist(UserPersonalizationHelper.CovertToDate(Quote.GetCustomField('EGAP_Contract_Start_Date').Content),  UserPersonalizationHelper.CovertToDate(Quote.GetCustomField('EGAP_Contract_End_Date').Content), True)
	yKey = None
	for item in Quote.Items:
		if item.ProductName == "Year":
			yKey = item.PartNumber
		if yKey:
			item.QI_SC_StartDate.Value = DateTime.Parse(dtDict[yKey]['StartDate'])
			item.QI_SC_EndDate.Value = DateTime.Parse(dtDict[yKey]['EndDate'])
		item.QI_SC_Product_ListPrice.Value = item.ListPrice
		if item.QI_PartNumber.Value.strip():
			Entitlements_InfoIcon = Quote.GetItemByUniqueIdentifier(item.QI_PartNumber.Value.strip()).Description
			Entitlements_InfoIcon = Entitlements_InfoIcon.replace('Entitlements: ','')
			item.QI_SC_Product_Entitlements.Value=Entitlements_InfoIcon.replace(',','
')
		if item.RolledUpQuoteItem.count('.') == 2 and item.QI_SC_Product_Entitlements.Value.strip() == '':
			cst_Category = SqlHelper.GetFirst("SELECT Cost_Category FROM SAP_PLSG_LOB_MAPPING WHERE SC_Module = '{}'".format(item.PartNumber))
			item.QI_SC_Product_Entitlements.Value = 'Cost Category: ' + (cst_Category.Cost_Category if cst_Category else '')
		#if item.PartNumber == 'Year-2' or optionalFlag:
			#item.ItemType = 3
			#optionalFlag = True
		if item.PartNumber == 'Platform':
			guidDict[item.QuoteItemGuid] = item.Description
			if item.Description not in itemDict:
				  itemDict[item.Description] = []
			itemDict[item.Description].append(item)
			pfList.append(item.Description)
		elif item.ParentItemGuid in guidDict:
			if guidDict[item.ParentItemGuid] + '_u*k#e*y_' + item.Description not in itemDict:
				  itemDict[guidDict[item.ParentItemGuid] + '_u*k#e*y_' + item.Description] = []
			itemDict[guidDict[item.ParentItemGuid] + '_u*k#e*y_' + item.Description].append(item)
		#so that margin will be 0 for hardware warranty and hardware refresh models.
if pfList:
	pData = SqlHelper.GetList("select Escalation, Platform, Year  from SC_ESCALATION_PLATFORM where Platform in {} and ServiceBundleType = '{}'".format(str(tuple(pfList)).replace(',)',')'), "VRP"))
	EsDict = {}
	maxEsDict = {}
	for row in pData:
		EsDict[row.Platform + '_' + str(row.Year)] = row.Escalation
		if maxEsDict.get(row.Platform, 0) < row.Year:
			maxEsDict[row.Platform] = row.Year
			EsDict[row.Platform + '_max'] = row.Escalation
	for key in itemDict:
		val = itemDict[key]
		i=1
		iListPrice = 0
		for vVal in val:
			if iListPrice == 0:
				iListPrice = vVal.ListPrice
			pkey = vVal.Description if '_u*k#e*y_' not in key else key.replace('_u*k#e*y_' + vVal.Description, '')
			vVal['QI_SC_Escalation_Percent'].Value = EsDict[pkey + '_' + str(i)] if pkey + '_' + str(i) in EsDict else EsDict[pkey + '_max'] if pkey + '_max' in EsDict else 0
			iListPrice = vVal.ListPrice =  iListPrice + (iListPrice *  vVal['QI_SC_Escalation_Percent'].Value/100)
			i+=1
qCurrency = Quote.GetCustomField('SC_CF_CURRENCY').Content if Quote.GetCustomField('SC_CF_PRICE_TOGGLE').Content != 'USD' else 'USD'
exRate = 1 if qCurrency == 'USD' else float(Quote.GetCustomField('SC_CF_EXCHANGE_RATE').Content)
otuData = {}
QCS_Rollup = []
Parts_Rollup = []
ThirdParty_Rollup = []
qListPrice = {}
SESPEscaltion = []
SC_ProductsType = eval(Quote.GetGlobal('SC_ProductsType')) if Quote.GetGlobal('SC_ProductsType') else {}
if 'Solution Enhancement Support Program' in SC_ProductsType:
	SC_ProductsType['SESP'] = SC_ProductsType['Solution Enhancement Support Program']
for item in Quote.MainItems:
	itemValues = dict([(val.Name, val.Values[0].Display) for val in item.SelectedAttributes if val.Name in ('SC_ItemEditFlag','SC_Item_MarginPercent','SC_Item_BlockDiscount','SC_Item_Cost','SC_Item_CostStatus','SC_PrevYr_ListPrice_RWL','SC_PrevYr_SellPrice_RWL','SC_HWListPrice_RWL','SC_ScopeChange_RWl','SC_PriceImpact_RWL','SC_Escalation_Price','SC_PY_Price','SC_PY_SellPrice','SC_SA_Price','SC_SR_Price','SC_Scope_Manual','SC_Honeywell_List_Price')])
	item.QI_SC_Honeywell_List_Price.Value = float(itemValues.get('SC_Honeywell_List_Price', '0')) if itemValues.get('SC_Honeywell_List_Price', '') != '' else item.ListPrice
	item.QI_SC_EscalationPrice.Value = float(itemValues.get('SC_Escalation_Price', '0') if itemValues.get('SC_Escalation_Price', '0') != '' else  '0')
	item.QI_SC_Previous_Year_List_Price.Value = float(itemValues.get('SC_PY_Price', '0') if itemValues.get('SC_PY_Price', '0') != '' else  '0')
	item.QI_SC_Previous_Year_Sell_Price.Value = float(itemValues.get('SC_PY_SellPrice', '0') if itemValues.get('SC_PY_SellPrice', '0') != '' else  '0')
	item.QI_SC_ScopeAdditionPrice.Value = float(itemValues.get('SC_SA_Price', '0') if itemValues.get('SC_SA_Price', '0') != '' else  '0')
	item.QI_SC_ScopeReductionPrice.Value = float(itemValues.get('SC_SR_Price', '0') if itemValues.get('SC_SR_Price', '0') != '' else  '0')
	if Quote.GetCustomField('Quote Type').Content in ('Contract New') and item.RolledUpQuoteItem.startswith('1.1') and len(list(item.Children)) == 0 and item.QI_SC_ItemFlag.Value != "Hidden":
		item.QI_SC_EscalationPrice.Value = item.ListPrice
	if item.Description in ('Parts Replacement','Parts Management') or (Parts_Rollup and item.RolledUpQuoteItem.startswith(tuple(Parts_Rollup))):
		if item.Description == 'Parts Replacement':
			item.QI_SC_Scope_Change.Value = float(itemValues.get('SC_Scope_Manual', '0') if itemValues.get('SC_Scope_Manual', '0') != '' else  '0')
		item.QI_SC_Honeywell_List_Price.Value = 0
		if item.Description in ('Parts Replacement','Parts Management'):
			Parts_Rollup.append(item.RolledUpQuoteItem)
	if itemValues.get('SC_ItemEditFlag', 0):
		if itemValues.get('SC_ItemEditFlag', 0) == 'Hidden':
			item.QI_SC_ItemFlag.Value = 'Hidden'
		else:
			if Quote.GetCustomField('Quote Type').Content in ('Contract New') and (item.RolledUpQuoteItem.startswith('1.1') or item.PartNumber == 'Service Contract'):
				item.QI_SC_ItemFlag.Value = '1' if (item.PartNumber == 'Resource Type' and (item.PartNumber == 'A360 Contract Management' or item.PartNumber == 'Service Contract Management')) else itemValues.get('SC_ItemEditFlag', '000')[0] + itemValues.get('SC_ItemEditFlag', '000')
			else:
				item.QI_SC_ItemFlag.Value = ('1' if (item.PartNumber == 'Other cost details' or (item.PartNumber == 'Resource Type' and (item.PartNumber == 'A360 Contract Management' or item.PartNumber == 'Service Contract Management'))) else itemValues.get('SC_ItemEditFlag', '000')[0]) + itemValues.get('SC_ItemEditFlag', '000')
				if 'Solution Enhancement Support Program' in SC_ProductsType and SC_ProductsType.get('Solution Enhancement Support Program', '') != 'Renewal' and item.RolledUpQuoteItem.startswith('1.1'):
					item.QI_SC_ItemFlag.Value = itemValues.get('SC_ItemEditFlag', '000')[0] + itemValues.get('SC_ItemEditFlag', '000')
	if item.PartNumber == 'Platform':
		isEscalation = False
		for citem in item.Children:
			citemValues = dict([(val.Name, val.Values[0].Display) for val in citem.SelectedAttributes if val.Name in ('SC_ItemEditFlag','SC_Item_MarginPercent','SC_Item_BlockDiscount','SC_Item_Cost','SC_Item_CostStatus')])
			citem.QI_SC_Margin_Percent.Value = item.QI_SC_Margin_Percent.Value
			citem['QI_SC_Margin_Percent'].Value = citemValues.get('SC_Item_MarginPercent', 0)
			citem['QI_SC_Cost'].Value = (1-item['QI_SC_Margin_Percent'].Value/100)*item.ListPrice
			item['QI_SC_Cost'].Value += citem['QI_SC_Cost'].Value
			if citem.QI_SC_EscalationPrice.Value>0 and isEscalation == False:
				isEscalation = True
		if (isEscalation and item.RolledUpQuoteItem.startswith('1.1')) or Quote.GetCustomField('Quote Type').Content == 'Contract New':
			item.QI_SC_ItemFlag.Value = '1' + item.QI_SC_ItemFlag.Value[1:]
			SESPEscaltion.append(item.RolledUpQuoteItem)
		item['QI_SC_Margin_Percent'].Value = 45
	elif item.PartNumber == 'Other cost details' and (not item.RolledUpQuoteItem.startswith('1.1') or SC_ProductsType.get('Solution Enhancement Support Program', '') == 'Renewal'):
		item['QI_SC_Escalation_Percent'].Value = 5
	#elif item.PartNumber == 'Service Product' and item.Description == 'Local Support Standby' and (not item.RolledUpQuoteItem.startswith('1.1') or SC_ProductsType.get('Local Support Standby', '') == 'Renewal'):
		#item['QI_SC_Escalation_Percent'].Value = 5
	elif item.PartNumber == 'Service Product' and item.Description == 'Trace Subscription Service' and not item.RolledUpQuoteItem.startswith('1.1'):
		item['QI_SC_Escalation_Percent'].Value = 5
	elif item.PartNumber in ('Enabled Services - Enhanced', 'Enabled Services - Essential') and (SC_ProductsType.get('Enabled Services' , '') == 'Renewal' or SC_ProductsType.get('Solution Enhancement Support Program' , '') == 'Renewal'):
		item['QI_SC_Escalation_Percent'].Value = 5
	elif item.PartNumber == 'Service Product' and item.Description in ['Honeywell Digital Prime Base','Digital Prime Twin']:
		if item.RolledUpQuoteItem.startswith('1.1'):
			if Quote.GetCustomField('Quote Type').Content in ('Contract New'):
				escPrice = item.ListPrice
			else:
				item['QI_SC_Escalation_Percent'].Value = 5
				escPrice = item.ListPrice = item.ListPrice + (item.ListPrice*5/100)
		else:
			if Quote.GetCustomField('Quote Type').Content in ('Contract New'):
				item['QI_SC_Escalation_Percent'].Value = 3
				item.ListPrice = escPrice = escPrice + (escPrice*3/100)
			else:
				item['QI_SC_Escalation_Percent'].Value = 5
				item.ListPrice = escPrice = escPrice + (escPrice*5/100)
		item['QI_SC_Margin_Percent'].Value = itemValues.get('SC_Item_MarginPercent', 0)
		item['QI_SC_Cost'].Value = (1-item['QI_SC_Margin_Percent'].Value/100)*item.ListPrice
	elif 'QCS 4.0' in SC_ProductsType and SC_ProductsType['QCS 4.0'] == 'Renewal' and ((item.PartNumber == 'Service Product' and item.Description in ['QCS 4.0', 'QCS Support Center']) or (QCS_Rollup and item.RolledUpQuoteItem.startswith(tuple(QCS_Rollup)))):
		if item.Description in ['QCS 4.0', 'QCS Support Center']:
			QCS_Rollup.append(item.RolledUpQuoteItem)
		else:
			if item.RolledUpQuoteItem.startswith(tuple(QCS_Rollup)):
				if item.RolledUpQuoteItem.startswith('1.1'):
					item['QI_SC_Escalation_Percent'].Value = 5
					rolledupNum = item.RolledUpQuoteItem.split('.')
					rolledupNum[1] = str(int(rolledupNum[1])+1)
					rolledupKey = '.'.join(rolledupNum)
					qListPrice[rolledupKey] = item.ListPrice = item.ListPrice + (item.ListPrice*5/100)
				else:
					item['QI_SC_Escalation_Percent'].Value = 5
					rolledupNum = item.RolledUpQuoteItem.split('.')
					rolledupNum[1] = str(int(rolledupNum[1])+1)
					rolledupKey = '.'.join(rolledupNum)
					qListPrice[rolledupKey] = item.ListPrice = qListPrice[item.RolledUpQuoteItem] + (qListPrice[item.RolledUpQuoteItem]*5/100)
		item['QI_SC_Margin_Percent'].Value = itemValues.get('SC_Item_MarginPercent', 0)
		item['QI_SC_Cost'].Value = (1-item['QI_SC_Margin_Percent'].Value/100)*item.ListPrice
	elif item.PartNumber == 'One Time Upgrade' and item.Description == 'Software Upgrades':
		if item.RolledUpQuoteItem.startswith('1.1'):
			for citem in item.Children:
				otuData[citem.PartNumber] = citem.ListPrice
		else:
			for citem in item.Children:
				citem['QI_SC_Escalation_Percent'].Value = '7'
				citem.ListPrice = otuData[citem.PartNumber]  = otuData[citem.PartNumber]  + (otuData[citem.PartNumber] * 7/100)
				citem['QI_SC_Margin_Percent'].Value = itemValues.get('SC_Item_MarginPercent', 0)
				citem['QI_SC_Cost'].Value = (1-item['QI_SC_Margin_Percent'].Value/100)*item.ListPrice
	else:
		item['QI_SC_Margin_Percent'].Value = itemValues.get('SC_Item_MarginPercent', 0)
		item['QI_SC_Cost'].Value = (1-item['QI_SC_Margin_Percent'].Value/100)*item.ListPrice
		#item['QI_SC_Previous_Year_List_Price'].Value = float(itemValues.get('SC_PrevYr_ListPrice_RWL',0))
		#item['QI_SC_Previous_Year_Sell_Price'].Value = float(itemValues.get('SC_PrevYr_SellPrice_RWL',0))
		#item['QI_SC_Honeywell_List_Price'].Value = float(itemValues.get('SC_HWListPrice_RWL',0))
		#item['QI_SC_Scope_Change'].Value = float(itemValues.get('SC_ScopeChange_RWl',0))
		#item['QI_SC_Price_Impact'].Value = float(itemValues.get('SC_PriceImpact_RWL',0))

	if item.RolledUpQuoteItem.startswith('1.1') and item.QI_SC_EscalationPrice.Value>0 and not item.RolledUpQuoteItem.startswith(tuple(SESPEscaltion)):
		item.QI_SC_ItemFlag.Value = '1' + item.QI_SC_ItemFlag.Value[1:]

	if not item.RolledUpQuoteItem.startswith('1.1'):
		if (item.Description == 'Third Party Services' and item.PartNumber == 'Third Party Services') or (item.PartNumber == 'Local Support Standby'):
			ThirdParty_Rollup.append(item.RolledUpQuoteItem)
		else:
			if item.RolledUpQuoteItem.startswith(tuple(ThirdParty_Rollup)):
				item.QI_SC_ItemFlag.Value = '1' + item.QI_SC_ItemFlag.Value[1:]
	item.QI_SC_ListPrice.Value = qCurrency + ' ' +  (str(round(item.ExtendedListPrice/exRate,2)) if qCurrency == 'USD' else str(round(item.ExtendedListPrice,2)))
	item.QI_SC_SellPrice.Value = qCurrency + ' ' +  (str(round(item.ExtendedAmount/exRate,2)) if qCurrency == 'USD' else str(round(item.ExtendedAmount,2)))
	item.QI_SC_CostPrice.Value = qCurrency + ' ' +  (str(round(item.QI_SC_Cost.Value/exRate,2)) if qCurrency == 'USD' else str(round(item.QI_SC_Cost.Value,2)))
	item.QI_SC_Target_Sell_Price.Value = (item.ExtendedListPrice + item.QI_MPA_Discount_Amount.Value)/exRate
	#item.QI_SC_Scope_Change.Value = ((item.QI_SC_ScopeAdditionPrice.Value * (item.ExtendedAmount/item.ListPrice)) if item.ListPrice > 0 else 0) + ((item.QI_SC_ScopeReductionPrice.Value * (item.QI_SC_Previous_Year_Sell_Price.Value/item.QI_SC_Previous_Year_List_Price.Value)) if item.QI_SC_Previous_Year_List_Price.Value > 0 else 0)
	#item.QI_SC_Scope_Impact.Value = qCurrency + ' ' +  (str(round((item.ExtendedAmount - (item.QI_SC_Scope_Change.Value + item.QI_SC_Previous_Year_Sell_Price.Value))/exRate,2)) if qCurrency == 'USD' else str(round((item.ExtendedAmount - (item.QI_SC_Scope_Change.Value + item.QI_SC_Previous_Year_Sell_Price.Value)),2)))

def assignValues(pDict,lineItem, mKey, Parts_Rollup):
	for cItem in lineItem.Children:
		if len(list(cItem.Children))>0:
			assignValues(pDict,cItem, mKey + '|' + lineItem.Description, Parts_Rollup)
		if pDict.get("{}|{}|{}".format(mKey, lineItem.Description, cItem.Description), ''):
			cItem.QI_SC_Previous_Year_List_Price.Value = float(pDict["{}|{}|{}".format(mKey, lineItem.Description, cItem.Description)]["ListPrice"])
			cItem.QI_SC_Previous_Year_Sell_Price.Value = float(pDict["{}|{}|{}".format(mKey, lineItem.Description, cItem.Description)]["SellPrice"])
			cItem.QI_MPA_Discount_Percent.Value = float(pDict["{}|{}|{}".format(mKey, lineItem.Description, cItem.Description)]["MPADiscount"])
			cItem.QI_Additional_Discount_Percent.Value = float(pDict["{}|{}|{}".format(mKey, lineItem.Description, cItem.Description)]["OtherDiscount"])
		else:
			if cItem.RolledUpQuoteItem.startswith('1.1'):
				cItem.QI_SC_ItemFlag.Value = '0' + cItem.QI_SC_ItemFlag.Value[1:]
				cItem.QI_SC_Escalation_Percent.Value = 0
		if not(Parts_Rollup and cItem.RolledUpQuoteItem.startswith(tuple(Parts_Rollup))):
			cItem.QI_SC_Honeywell_List_Price.Value = cItem.ListPrice
"""
if Quote.GetCustomField('Quote Type').Content == 'Contract Renewal':
	reference_number = Quote.GetCustomField("SC_CF_PREVIOUS_QUOTE_NO").Content
	if reference_number:
		for item in Quote.MainItems:
			if item.ProductName == "Year":
				#query = SqlHelper.GetList("Select distinct(Product), QuoteDetails from CT_SC_RENEWAL_QUOTE_TABLE where QuoteID = '{}'".format(reference_number))
				for citem in item.Children:
					if citem.RolledUpQuoteItem.count('.') == 2:
						query = SqlHelper.GetFirst("Select Product, QuoteDetails from CT_SC_RENEWAL_QUOTE_TABLE where QuoteID = '{}' and Product = '{}'".format(reference_number,citem.PartNumber))
						assignValues(eval(query.QuoteDetails) if query != None else {}, citem, item.PartNumber, Parts_Rollup)
					#Trace.Write(citem.PartNumber)
"""

def setEscalationValue(prdType,lineItem, Parts_Rollup):
	for cItem in lineItem.Children:
		cItem.QI_ContractType.Value = prdType
		if len(list(cItem.Children))>0:
			setEscalationValue(prdType,cItem, Parts_Rollup)
		if cItem.RolledUpQuoteItem.startswith('1.1') and (prdType != 'Renewal' or cItem.RolledUpQuoteItem.startswith(tuple(SESPEscaltion))):
			cItem.QI_SC_ItemFlag.Value = '0' + cItem.QI_SC_ItemFlag.Value[1:]
			cItem.QI_SC_Escalation_Percent.Value = 0
		if cItem.RolledUpQuoteItem in SESPEscaltion:
			cItem.QI_SC_ItemFlag.Value = '1' + cItem.QI_SC_ItemFlag.Value[1:]
		if not(Parts_Rollup and cItem.RolledUpQuoteItem.startswith(tuple(Parts_Rollup))):
			cItem.QI_SC_Honeywell_List_Price.Value = cItem.ListPrice
		if Quote.GetCustomField('SC_CF_IS_CONTRACT_EXTENSION').Content == 'True' and cItem.QI_SC_ItemFlag.Value[0] == '1' and cItem.Description not in ('Parts Replacement'):
			cItem.QI_SC_Escalation_Percent.Value = 5
			Trace.Write("Extention Value: {}, Part: {}, Desc: {}".format(item.QI_SC_ItemFlag.Value, item.PartNumber, item.Description))

def setItemType(prdType,lineItem):
	for cItem in lineItem.Children:
		cItem.QI_ContractType.Value = prdType
		if len(list(cItem.Children))>0:
			setItemType(prdType, cItem)

if Quote.GetCustomField('Quote Type').Content == 'Contract Renewal':
	for item in Quote.MainItems:
		if item.ProductName == "Year" and item.RolledUpQuoteItem == "1.1":
			for citem in item.Children:
				if citem.RolledUpQuoteItem.count('.') == 2:
					if citem.PartNumber in SC_ProductsType:
						prdType = SC_ProductsType[citem.PartNumber]
					elif citem.Description in SC_ProductsType:
						prdType = SC_ProductsType[citem.Description]
					else:
						prdType = ''
					citem.QI_ContractType.Value = prdType
					setEscalationValue(prdType, citem, Parts_Rollup)
		elif item.ProductName == "Year":
			for citem in item.Children:
				if citem.RolledUpQuoteItem.count('.') == 2:
					if citem.PartNumber in SC_ProductsType:
						prdType = SC_ProductsType[citem.PartNumber]
					elif citem.Description in SC_ProductsType:
						prdType = SC_ProductsType[citem.Description]
					else:
						prdType = ''
					citem.QI_ContractType.Value = prdType
					setItemType(prdType, citem)

qLineHelper = CL_SC_QuoteLinesHelper(Quote, TagParserQuote, None, Session)
qLineData = qLineHelper.getSCLineItemsData()

if qLineData:
	keysDict = {}
	for item in Quote.MainItems:
		if item.RolledUpQuoteItem.count('.') >= 1:
			keysDict[item.RolledUpQuoteItem] = (keysDict.get(item.RolledUpQuoteItem[:-2], '#') + '|' + item.PartNumber + '|' + item.Description).replace('#|', '')
			if keysDict[item.RolledUpQuoteItem] in qLineData:
				#Trace.Write(kDict[item.RolledUpQuoteItem])
				iData = qLineData[keysDict[item.RolledUpQuoteItem]]
				Trace.Write("Rank: {}, Escalation: {}, MPADiscount: {}, OtherDiscount: {}, Margin: {}".format(item.RolledUpQuoteItem, iData['Escalation'], iData['MPADiscount'], iData['OtherDiscount'], iData['Margin']))
				if len(item.QI_SC_ItemFlag.Value)>3 and  item.QI_SC_ItemFlag.Value[0] == '1':
					item.QI_SC_Escalation_Percent.Value = float(iData['Escalation'])
				if len(item.QI_SC_ItemFlag.Value)>3 and  item.QI_SC_ItemFlag.Value[1] == '1':
					item.QI_MPA_Discount_Percent.Value = float(iData['MPADiscount'])
				if len(item.QI_SC_ItemFlag.Value)>3 and  item.QI_SC_ItemFlag.Value[2] == '1':
					item.QI_Additional_Discount_Percent.Value = float(iData['OtherDiscount'])
				if len(item.QI_SC_ItemFlag.Value)>3 and  item.QI_SC_ItemFlag.Value[3] == '1':
					item.QI_SC_Margin_Percent.Value = float(iData['Margin'])
	qLineHelper.clearSCLineItemsData()
if SC_ProductsType:
	Quote.SetGlobal('SC_ProductsType', '')

if Quote.GetCustomField("SC_CF_IS_CONTRACT_EXTENSION").Content == 'True' and Quote.GetCustomField("SC_CF_Parent_Quote_Number_Link").Content:
	from GS_SC_GetQuoteData import CL_QuoteHandler
	QuoteHandler = CL_QuoteHandler(Quote.GetCustomField("SC_CF_Parent_Quote_Number_Link").Content)
	pQuoteDisc=QuoteHandler.GetQuoteLineItemDiscounts()
	for item in Quote.MainItems:
		if item.RolledUpQuoteItem.startswith('1.1') and pQuoteDisc.get(item.PartNumber + '-#-' + item.Description, None) != None:
			item.QI_MPA_Discount_Percent.Value = float(pQuoteDisc[item.PartNumber + '-#-' + item.Description]['QI_MPA_Discount_Percent'])
			item.QI_Additional_Discount_Percent.Value = float(pQuoteDisc[item.PartNumber + '-#-' + item.Description]['QI_Additional_Discount_Percent'])
#Start: Added below change to set the parent product quantity to zero if all the child items quantity is zero #CXCPQ-82629
def checkchildItemsqty(item): #checks if any child item qty is non-zero
	for child in item.Children:
		if child.ParentItemGuid==item.QuoteItemGuid:
			if child.Quantity!=0:
				return 1
	return 0
def ret_parentId(item):
	pItem= Quote.GetItemByUniqueIdentifier(item.ParentItemGuid)
	if pItem is not None:
		if item.Quantity==0 and checkchildItemsqty(pItem)==0: #update parent item qty only when all child items qty is zero
			pItem.Quantity=item.Quantity
		ret_parentId(pItem)
for item in Quote.MainItems:
	if item.QI_SC_EscalationPrice.Value == 0 and item.RolledUpQuoteItem.startswith('1.1') and len(item.QI_SC_ItemFlag.Value)>3 and  item.QI_SC_ItemFlag.Value[0] == '1' and item.RolledUpQuoteItem not in SESPEscaltion:
		item.QI_SC_Escalation_Percent.Value = 0
		item.QI_SC_ItemFlag.Value = '0' + item.QI_SC_ItemFlag.Value[1:]
	if len(list(item.Children)) == 0 and item.QI_SC_ItemFlag.Value != "Hidden":
		ret_parentId(item)
#End: Added below change to set the parent product quantity to zero if all the child items quantity is zero #CXCPQ-82629
Quote.Save(False)
Quote.Calculate(1)
Quote.Calculate(2)