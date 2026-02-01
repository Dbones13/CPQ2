###############################################################################################
#       Class CL_SC_QuoteLinesHelper:
#       Helper Class for SC Quote Lines
###############################################################################################
class CL_SC_QuoteLinesHelper:

	def __init__(self, Quote, TagParserQuote, WorkflowContext, Session):
		self.Quote = Quote
		self.TagParserQuote = TagParserQuote
		self.WorkflowContext = WorkflowContext
		self.Session = Session

	def getParentKey(self, item, xkey):
		pItem = self.Quote.GetItemByUniqueIdentifier(item.ParentItemGuid)
		if pItem.ProductName == "Year":
			xkey = pItem.PartNumber + '|' + xkey
			return xkey,item.PartNumber
		else:
			xkey = pItem.PartNumber + '|' + pItem.Description + '|' + xkey
			return self.getParentKey(pItem, xkey)

	def getSCLineItemsDataToSave(self):
		SCLineItemsData = {}
		for item in self.Quote.MainItems:
			if len(list(item.Children)) == 0 and item.QI_SC_ItemFlag.Value != "Hidden":
				value = {"Escalation": item.QI_SC_Escalation_Percent.Value,
							"MPADiscount": item.QI_MPA_Discount_Percent.Value,
							"OtherDiscount": item.QI_Additional_Discount_Percent.Value,
							"Margin": item.QI_SC_Margin_Percent.Value}
				key,product = self.getParentKey(item, item.PartNumber + '|' + item.Description)
				if product not in SCLineItemsData.keys():
					SCLineItemsData[product] = {key:value}
				else:
					SCLineItemsData[product][key] = value
		return str(SCLineItemsData)

	def setSCLineItemsData(self):
		SCLineItemsData = {}
		kDict = {}
		for item in self.Quote.MainItems:
			if len(item.RolledUpQuoteItem)>=3 and item.QI_SC_ItemFlag.Value != "Hidden":
				kDict[item.RolledUpQuoteItem] = (kDict.get(item.RolledUpQuoteItem[:-2], '#') + '|' + item.PartNumber + '|' + item.Description).replace('#|', '')
				SCLineItemsData[kDict[item.RolledUpQuoteItem]] = {"Escalation": str(item.QI_SC_Escalation_Percent.Value),
																  "MPADiscount": str(item.QI_MPA_Discount_Percent.Value),
																  "OtherDiscount": str(item.QI_Additional_Discount_Percent.Value),
																  "Margin": str(item.QI_SC_Margin_Percent.Value)}
		self.Quote.SetGlobal('SCLineItemsData', str(SCLineItemsData))

	def getSCLineItemsData(self):
		return eval(self.Quote.GetGlobal('SCLineItemsData')) if self.Quote.GetGlobal('SCLineItemsData') else ''

	def clearSCLineItemsData(self):
		self.Quote.SetGlobal('SCLineItemsData', '')
		return True

	def updateToggleCurrency(self):
		qCurrency = self.Quote.GetCustomField('SC_CF_CURRENCY').Content if self.Quote.GetCustomField('SC_CF_PRICE_TOGGLE').Content != 'USD' else 'USD'
		exRate = float(self.Quote.GetCustomField('SC_CF_EXCHANGE_RATE').Content)
		for item in self.Quote.Items:
			item.QI_SC_ListPrice.Value = qCurrency + ' ' +  '{0:.2f}'.format(round(item.ExtendedListPrice/exRate,2) if qCurrency == 'USD' else round(item.ExtendedListPrice,2))
			item.QI_SC_SellPrice.Value = qCurrency + ' ' +  '{0:.2f}'.format(round(item.ExtendedAmount/exRate,2) if qCurrency == 'USD' else round(item.ExtendedAmount,2))
			item.QI_SC_CostPrice.Value = qCurrency + ' ' +  '{0:.2f}'.format(round(item.QI_SC_Cost.Value/exRate,2) if qCurrency == 'USD' else round(item.QI_SC_Cost.Value,2))
			item.QI_SC_Target_Sell_Price.Value = (item.ExtendedListPrice + item.QI_MPA_Discount_Amount.Value)/exRate
			item.QI_SC_Scope_Impact.Value = item.QI_SC_SellPrice.Value

	def AddMatrikonLicense(self, QLine, qitem):
		pItem = self.Quote.GetItemByUniqueIdentifier(qitem.ParentItemGuid)
		for item in pItem.Children:
			if item.PartNumber == 'Matrikon License':
				mpaAmount = QLine['CPQ_Unti_List_Price__c'] * QLine['MPA__c']/100
				otherAmount = QLine['CPQ_Unti_List_Price__c'] * QLine['Other_Discount__c']/100
				QLine['UnitPrice'] = QLine['UnitPrice'] + item.QI_SC_Cost.Value
				QLine['CPQ_Unti_List_Price__c'] = QLine['CPQ_Unti_List_Price__c'] + item.ListPrice
				QLine['Requested_Unit_Sell_Price__c'] = QLine['Requested_Unit_Sell_Price__c'] + item.ExtendedAmount
				QLine['Target_Price__c'] = QLine['Target_Price__c'] + item.QI_SC_Target_Sell_Price.Value
				item.QI_SC_Scope_Impact.Value = item.QI_SC_Scope_Impact.Value if item.QI_SC_Scope_Impact.Value !='' else str(0)
				QLine['Scope_Impact__c'] = float(item.QI_SC_Scope_Impact.Value.replace(self.Quote.SelectedMarket.CurrencyCode, '').replace(self.Quote.SelectedMarket.CurrencySign, '').replace(',', '').strip()) + float(QLine['Scope_Impact__c'])
				QLine['SC_Price_Impact__c'] = QLine['SC_Price_Impact__c'] + item.QI_SC_Price_Impact.Value
				QLine['Booked_Margin__c'] = round((1 - QLine['UnitPrice'] / QLine['Requested_Unit_Sell_Price__c']) * 100, 6) if QLine['Requested_Unit_Sell_Price__c'] > 0 else 0.00
				QLine['Gross_Margin__c'] = QLine['Booked_Margin__c']
				QLine['Previous_Year_List_Price__c'] = QLine['Previous_Year_List_Price__c'] + item.QI_SC_Previous_Year_List_Price.Value
				QLine['SC_Previous_Year_Sell_Price__c'] = QLine['SC_Previous_Year_Sell_Price__c'] + item.QI_SC_Previous_Year_Sell_Price.Value
				QLine['Scope_Change__c'] = QLine['Scope_Change__c'] + item.QI_SC_Scope_Change.Value
				QLine['Variable_Invoice_Amount__c'] = QLine['Variable_Invoice_Amount__c'] + item.ExtendedAmount
				QLine['Recurring_Invoice_Amount__c'] = QLine['Variable_Invoice_Amount__c'] + item.ExtendedAmount
				QLine['MPA__c'] = round(mpaAmount/QLine['CPQ_Unti_List_Price__c'] * 100, 6) if QLine['CPQ_Unti_List_Price__c']> 0 else 0.00
				QLine['Other_Discount__c'] = round(otherAmount/QLine['CPQ_Unti_List_Price__c'] * 100, 6) if QLine['CPQ_Unti_List_Price__c']> 0 else 0.00
				QLine['SC_DiscountAmout'] = QLine['CPQ_Unti_List_Price__c'] - QLine['Requested_Unit_Sell_Price__c']
				QLine['SC_EscalationAmount'] = item.ListPrice - item.QI_SC_Product_ListPrice.Value
				QLine['SC_EscalationValue'] = QLine['SC_EscalationAmount']/QLine['CPQ_Unti_List_Price__c'] * 100 if QLine['CPQ_Unti_List_Price__c']> 0 else 0.00
		return QLine

	def getTrainingMatch_SellPrice(self, itemGuid):
		pItem = self.Quote.GetItemByUniqueIdentifier(itemGuid)
		for item in pItem.Children:
			if item.PartNumber == 'Training Match':
				return item.ExtendedAmount
		return 0

	def generateSFDCQuoteLines(self):
		UniqueIDList = []
		UniqueIDItems = {}
		QuoteLines = []
		child_des = {}
		entitlement = ''
		ParentUniqueID = ''
		for item in self.Quote.Items:
			if item.QI_PartNumber.Value.strip():
				Trace.Write('Rank: {}, PartNumber: {}, Description: {},  UniqueID: {}'.format(item.RolledUpQuoteItem, item.PartNumber, item.Description, item.QI_PartNumber.Value))
				QLine={}
				ParentUniqueID = item.QI_PartNumber.Value.strip()
				QLine['UniqueID'] = item.QuoteItemGuid
				QLine['RolledUpQuoteItem'] = item.RolledUpQuoteItem
				QLine['PartNumber'] = item.PartNumber
				QLine['Description'] = item.Description
				QLine['Quantity'] = item.Quantity
				QLine['UnitPrice'] = item.QI_SC_Cost.Value
				QLine['CPQ_Unti_List_Price__c'] = item.ListPrice
				QLine['MPA__c'] = item.QI_MPA_Discount_Percent.Value
				QLine['Other_Discount__c'] = item.QI_Additional_Discount_Percent.Value
				QLine['Requested_Unit_Sell_Price__c'] = item.ExtendedAmount
				QLine['Target_Price__c'] = item.QI_SC_Target_Sell_Price.Value
				item.QI_SC_Scope_Impact.Value = item.QI_SC_Scope_Impact.Value if item.QI_SC_Scope_Impact.Value !='' else str(0)
				QLine['Scope_Impact__c'] = item.QI_SC_Scope_Impact.Value.replace(self.Quote.SelectedMarket.CurrencyCode, '').replace(self.Quote.SelectedMarket.CurrencySign, '').replace(',', '').strip()
				QLine['SC_Price_Impact__c'] = item.QI_SC_Price_Impact.Value
				QLine['Booked_Margin__c'] = item.QI_SC_Margin_Percent.Value
				QLine['Gross_Margin__c'] = item.QI_SC_Margin_Percent.Value
				QLine['Previous_Year_List_Price__c'] = item.QI_SC_Previous_Year_List_Price.Value
				QLine['SC_Previous_Year_Sell_Price__c'] = item.QI_SC_Previous_Year_Sell_Price.Value
				QLine['Scope_Change__c'] = item.QI_SC_Scope_Change.Value
				QLine['Start_Date__c'] = item.QI_SC_StartDate.Value.ToString('yyyy-MM-dd')
				QLine['End_Date__c'] = item.QI_SC_EndDate.Value.ToString('yyyy-MM-dd')
				QLine['Variable_Invoice_Amount__c'] = item.ExtendedAmount
				QLine['Recurring_Invoice_Amount__c'] = item.ExtendedAmount
				QLine['SC_ModuleName'] = self.Quote.GetItemByUniqueIdentifier(item.QI_PartNumber.Value.strip()).PartNumber
				QLine['SC_DiscountAmout'] = item.DiscountAmount
				QLine['SC_EscalationAmount'] = item.ListPrice - item.QI_SC_Product_ListPrice.Value
				QLine['SC_EscalationValue'] = item.QI_SC_EscalationPrice.Value
				QLine['Product2Id'] = ""
				QLine['PriceBookEntryId'] = ""
				QLine['Royalty_Excluded_Amount__c'] = self.getTrainingMatch_SellPrice(item.QuoteItemGuid) if item.PartNumber == "SESP" else 0
				QLine['TrainingMatch_SellPrice'] = QLine['Royalty_Excluded_Amount__c'] * 2 
				QLine['ParentUniqueID'] = ParentUniqueID
				QLine['PSCLines'] = []
				QLine['SFDCLineID'] = ''
				if item.Description in ('Enabled Services - Enhanced', 'Enabled Services - Essential') and item.Quantity > 0:
					QLine['PartNumber'] = item.Description
					QLine = self.AddMatrikonLicense(QLine, item)
				QuoteLines.append(QLine)
				UniqueIDList.append(item.QI_PartNumber.Value.strip())
			elif item.PartNumber == 'Entitlement' and ParentUniqueID:
				entitlement = item.Description
			elif item.PartNumber == 'Resource Type' and ParentUniqueID and entitlement:
				#Trace.Write('iddd -->'+str(ParentUniqueID))
				start_date = QLine['Start_Date__c']
				key = '{}{}'.format(ParentUniqueID, start_date)
				resource_entry = [item.Description, item.ListPrice, item.ExtendedAmount]
				if key not in child_des:
						#Trace.Write('key added-if->'+str(key))
						child_des[key] = {entitlement: [resource_entry]}
				else:
						if entitlement in child_des[key]:
							#Trace.Write('key added-if2->'+str(key))
							child_des[key][entitlement].append(resource_entry)
						else:
							#Trace.Write('key added-else->'+str(key))
							child_des[key][entitlement] = [resource_entry]
			if item.QuoteItemGuid in UniqueIDList:
				#Trace.Write('************: {}'.format(item.PartNumber))
				UniqueIDItems[item.QuoteItemGuid] = {'Qitem' : item, 'PartNumber': item.PartNumber, 'Desc': item.DescriptionLong, 'pscList': []}
			for lines in QuoteLines:
				if str(lines['ParentUniqueID']+str(lines['Start_Date__c'])) in child_des.keys():
					#Trace.Write("child_des----1"+str(child_des[lines['ParentUniqueID']+str(lines['Start_Date__c'])]))
					lines['Contract_ResourceType__c'] = {lines['ParentUniqueID']+str(lines['Start_Date__c']):child_des[lines['ParentUniqueID']+str(lines['Start_Date__c'])]}
		return QuoteLines, UniqueIDList, UniqueIDItems