if Quote.GetCustomField('Quote Type').Content in ('Contract New','Contract Renewal'):
	listPrice = dict()
	py_listPrice = dict()
	py_sellPrice = dict()
	costPrice = dict()
	wtwFactor = dict()
	Parts_Rollup = []
	MPADisctList = dict()
	OtherDisctList = dict()
	exRate = float(Quote.GetCustomField('SC_CF_EXCHANGE_RATE').Content)
	pexRate = float(Quote.GetCustomField('SC_CF_PRVYR_EXCHANGE_RATE').Content) if Quote.GetCustomField('SC_CF_PRVYR_EXCHANGE_RATE').Content not in (None, "") else exRate
	qCurrency = Quote.GetCustomField('SC_CF_CURRENCY').Content if Quote.GetCustomField('SC_CF_PRICE_TOGGLE').Content != 'USD' else 'USD'
	dTable = SqlHelper.GetList("select distinct sp.SC_Module, sp.SAP_PL_PLSG as PLSG, sp.SAP_PLSG_Description as PLSGDesc, COALESCE(WtW.WTW_FACTOR, '0.0') as WTWFactor from HPS_PLSG_WTW_FACTOR WtW JOIN SAP_PLSG_LOB_Mapping sp ON WtW.PL_PLSG = sp.SAP_PL_PLSG Join Cart_Item c on  sp.SC_Module LIKE CONCAT('%', c.CATALOGCODE, '%')  Where sp.SC_Module != 'NULL' and c.CART_ID = '"+str(Quote.QuoteId)+"' and USERID = '"+str(Quote.UserId)+"'")
	RollupYear1, RollupYear2 = ({item.PartNumber: item.RolledUpQuoteItem for item in Quote.Items if item.RolledUpQuoteItem.startswith(prefix) and len(item.RolledUpQuoteItem) == 5} for prefix in ('1.1', '1.2'))
	RepRollupData = {RollupYear1[k]: RollupYear2[k] for k in RollupYear1 if k in RollupYear2}
	plsgDict = {}
	otuRolledUpQuoteItem = ''
	for row in dTable:
		if row.SC_Module not in plsgDict:
			plsgDict[row.SC_Module] = {'PLSG': row.PLSG, 'PLSGDesc': row.PLSGDesc, 'WTWFactor': row.WTWFactor}
	plsgDict_keyList = [pkeyval.strip() for pkey in plsgDict.keys() for pkeyval in pkey.split('|')]
	for item in Quote.MainItems:
		if item.QI_SC_Escalation_Percent.Value < 0:
			item.QI_SC_Escalation_Percent.Value = 0
		elif item.QI_SC_Escalation_Percent.Value > 100:
			item.QI_SC_Escalation_Percent.Value = 100
		if item['QI_SC_Product_ListPrice'].Value == 0 and item.RolledUpQuoteItem.startswith('1.1'):
			item['QI_SC_Product_ListPrice'].Value = item.ListPrice
		ItemValues = dict([(val.Name, val.Values[0].Display) for val in item.SelectedAttributes if val.Name in ('SC_ItemEditFlag','SC_Item_MarginPercent','SC_Item_BlockDiscount','SC_Item_Cost','SC_Item_CostStatus','SC_Escalation_Price','SC_PY_Price','SC_PY_SellPrice','SC_SA_Price','SC_SR_Price','SC_Honeywell_List_Price')])
		rolledupNum = item.RolledUpQuoteItem.split('.')
		if len(rolledupNum)>2:
			matched_Rolledup = next((rkey for rkey in RepRollupData if item.RolledUpQuoteItem.startswith(rkey)), None)
			if matched_Rolledup:
				rolledupKey = RepRollupData[matched_Rolledup] + item.RolledUpQuoteItem[len(matched_Rolledup):]
			else:
				rolledupNum[1] = str(int(rolledupNum[1])+1)
				rolledupKey = '.'.join(rolledupNum)
		else:
			rolledupKey = item.RolledUpQuoteItem
		if item.PartNumber == 'One Time Upgrade' or item.PartNumber == 'Experion':
			otuRolledUpQuoteItem = item.RolledUpQuoteItem if item.PartNumber == 'One Time Upgrade' else otuRolledUpQuoteItem
			pyListPrice = (listPrice.get(item.RolledUpQuoteItem, item['QI_SC_Product_ListPrice'].Value if item['QI_SC_Product_ListPrice'].Value else 0))

			item.ListPrice = pyListPrice + ((float(ItemValues.get('SC_Escalation_Price', 0) if ItemValues.get('SC_Escalation_Price', 0) else 0) * item.QI_SC_Escalation_Percent.Value/100) if item.RolledUpQuoteItem.startswith('1.1') and Quote.GetCustomField('Quote Type').Content == 'Contract Renewal' else (pyListPrice *  item.QI_SC_Escalation_Percent.Value/100))

			item.QI_SC_Honeywell_List_Price.Value = float(ItemValues.get('SC_Honeywell_List_Price', '0'))  if ItemValues.get('SC_Honeywell_List_Price', '') != '' else item.ListPrice
			Trace.Write('item.PartNumber-->{3}pyListPrice--->{0}	item.ListPrice--->{1}	item.QI_SC_Honeywell_List_Price.Value---->{2}'.format(pyListPrice,item.ListPrice,item.QI_SC_Honeywell_List_Price.Value,item.PartNumber))
		else:
			annualFactor = (1 if (item.QI_SC_EndDate.Value - item.QI_SC_StartDate.Value).Days >= 364 else float(float((item.QI_SC_EndDate.Value - item.QI_SC_StartDate.Value).Days + 1)/365)) if item.QI_SC_EndDate.Value and item.QI_SC_StartDate.Value else 1
			pyListPrice = (listPrice.get(item.RolledUpQuoteItem, item['QI_SC_Product_ListPrice'].Value if item['QI_SC_Product_ListPrice'].Value else 0)) * annualFactor
			item.ListPrice = pyListPrice + ((float(ItemValues.get('SC_Escalation_Price', 0) if ItemValues.get('SC_Escalation_Price', 0) else 0) * annualFactor * item.QI_SC_Escalation_Percent.Value/100) if item.RolledUpQuoteItem.startswith('1.1') and Quote.GetCustomField('Quote Type').Content == 'Contract Renewal' else (pyListPrice *  item.QI_SC_Escalation_Percent.Value/100))
			item.QI_SC_Honeywell_List_Price.Value = float(ItemValues.get('SC_Honeywell_List_Price', '0')) * annualFactor if ItemValues.get('SC_Honeywell_List_Price', '') != '' else item.ListPrice
			Trace.Write('item.PartNumber2-->{3}pyListPrice--->{0}	item.ListPrice--->{1}	item.QI_SC_Honeywell_List_Price.Value---->{2}'.format(pyListPrice,item.ListPrice,item.QI_SC_Honeywell_List_Price.Value,item.PartNumber))
		if item.Description in ('Parts Replacement','Parts Management') or (Parts_Rollup and item.RolledUpQuoteItem.startswith(tuple(Parts_Rollup))):
			item.QI_SC_Honeywell_List_Price.Value = 0
			if item.Description in ('Parts Replacement','Parts Management'):
				Parts_Rollup.append(item.RolledUpQuoteItem)
		if Quote.GetCustomField('Quote Type').Content in ('Contract New'):
			item['QI_SC_Price_Impact'].Value = item.ListPrice
			item.QI_SC_EscalationPrice.Value = 0
			item.QI_SC_Previous_Year_List_Price.Value = 0
			item.QI_SC_Previous_Year_Sell_Price.Value = 0
			item.QI_SC_ScopeAdditionPrice.Value = 0
			item.QI_SC_ScopeReductionPrice.Value = 0
		else:
			if item.RolledUpQuoteItem.startswith('1.1'):
				item['QI_SC_Price_Impact'].Value = 0
				item.QI_SC_EscalationPrice.Value = annualFactor * float(ItemValues.get('SC_Escalation_Price', 0) if ItemValues.get('SC_Escalation_Price', 0) else 0)
				item.QI_SC_Previous_Year_List_Price.Value = annualFactor * float(ItemValues.get('SC_PY_Price', 0) if ItemValues.get('SC_PY_Price', 0) else 0)
				item.QI_SC_Previous_Year_Sell_Price.Value = annualFactor * float(ItemValues.get('SC_PY_SellPrice', 0) if ItemValues.get('SC_PY_SellPrice', 0) else 0)
				item.QI_SC_ScopeAdditionPrice.Value = annualFactor * float(ItemValues.get('SC_SA_Price', 0) if ItemValues.get('SC_SA_Price', 0) else 0)
				item.QI_SC_ScopeReductionPrice.Value = annualFactor * float(ItemValues.get('SC_SR_Price', 0) if ItemValues.get('SC_SR_Price', 0) else 0)
			else:
				item['QI_SC_Price_Impact'].Value = 0
				item.QI_SC_EscalationPrice.Value = 0
				item.QI_SC_Previous_Year_List_Price.Value = py_listPrice.get(item.RolledUpQuoteItem,  0) * annualFactor
				item.QI_SC_Previous_Year_Sell_Price.Value = py_sellPrice.get(item.RolledUpQuoteItem,  0) * annualFactor
				item.QI_SC_ScopeAdditionPrice.Value = 0
				item.QI_SC_ScopeReductionPrice.Value = 0
		item.ExtendedListPrice = float(item.ListPrice * item.Quantity)
		listPrice[rolledupKey] = item.ListPrice

		if item.QI_MPA_Discount_Percent.Value < 0:
			item.QI_MPA_Discount_Percent.Value = 0
		if item.QI_Additional_Discount_Percent.Value < -25:
			item.QI_Additional_Discount_Percent.Value = 0
		if item.QI_Additional_Discount_Percent.Value + item.QI_MPA_Discount_Percent.Value > 100:
			item.QI_Additional_Discount_Percent.Value = 0
			item.QI_MPA_Discount_Percent.Value = 0
			Quote.Messages.Add("For item : '{}' Total Discount exceeds 100% ".format(item.RolledUpQuoteItem))
		if item.QI_SC_Escalation_Percent.Value < 5 and len(item.QI_SC_ItemFlag.Value)>0 and item.QI_SC_ItemFlag.Value[0] == '1' and item.PartNumber == 'Other cost details':
			Quote.Messages.Add("For item : '{}', Escalation % for Other cost details should not be less than 5%".format(item.RolledUpQuoteItem))
		if item.PartNumber == 'Platform' or item.PartNumber == 'Entitlement' or item.PartNumber == 'Other cost details':
			if item.PartNumber == 'Platform':
				item.QI_MPA_Discount_Percent.Value = MPADisctList.get(item.Description , item.QI_MPA_Discount_Percent.Value)
				item.QI_Additional_Discount_Percent.Value = OtherDisctList.get(item.Description , item.QI_Additional_Discount_Percent.Value)
				MPADisctList[item.Description] = item.QI_MPA_Discount_Percent.Value
				OtherDisctList[item.Description] = item.QI_Additional_Discount_Percent.Value
			for citem in item.Children:
				if citem.PartNumber == 'Total Expense' or citem.PartNumber == 'Resource Type':
					continue
				citem.QI_MPA_Discount_Percent.Value = item.QI_MPA_Discount_Percent.Value
				citem.QI_Additional_Discount_Percent.Value = item.QI_Additional_Discount_Percent.Value
				citem.QI_SC_Escalation_Percent.Value = item.QI_SC_Escalation_Percent.Value

		mpaDiscount = 0
		additionalDiscount = 0
		if item.ExtendedListPrice !=0:
			mpaDiscount = (item.ExtendedListPrice * item.QI_MPA_Discount_Percent.Value) / 100
			additionalDiscount = (item.ExtendedListPrice * item.QI_Additional_Discount_Percent.Value ) / 100

		totalDiscount = mpaDiscount + additionalDiscount + ((item.ExtendedListPrice * float(ItemValues.get('SC_Item_BlockDiscount', 0)))/100 if mpaDiscount + additionalDiscount == 0 else 0)
		item.QI_Additional_Discount_Amount.Value = additionalDiscount
		item.QI_MPA_Discount_Amount.Value = mpaDiscount
		item.DiscountAmount = totalDiscount
		if item.ExtendedListPrice:
			item.DiscountPercent = (100 * item.DiscountAmount) / item.ExtendedListPrice
		item.QI_SC_Total_Discount_Percent.Value = item.DiscountPercent
		item.QI_SC_Total_Discount_Price.Value = (Quote.SelectedMarket.CurrencySign if Quote.GetCustomField('SC_CF_PRICE_TOGGLE').Content != 'USD' else '$') + ' ' + (UserPersonalizationHelper.ToUserFormat(round(item.DiscountAmount/float(Quote.GetCustomField('SC_CF_EXCHANGE_RATE').Content),2)) if Quote.GetCustomField('SC_CF_PRICE_TOGGLE').Content == 'USD' else UserPersonalizationHelper.ToUserFormat(round(item.DiscountAmount,2)))

		pyCostPrice = float(costPrice.get(item.RolledUpQuoteItem, ItemValues.get('SC_Item_Cost', 0)))

		if 'SC_Item_CostStatus' in ItemValues and ItemValues['SC_Item_CostStatus'] == '1':
			item.QI_SC_Cost.Value = (pyCostPrice + float(pyCostPrice *  item['QI_SC_Escalation_Percent'].Value/100)) * annualFactor
			if item.ListPrice-item.DiscountAmount > 0:
				item.QI_SC_Margin_Percent.Value = (1-item.QI_SC_Cost.Value/(item.ListPrice-item.DiscountAmount))*100
			else:
				item.QI_SC_Margin_Percent.Value = 0
		else:
			Trace.Write("{} - {} - {} - {}".format(item.PartNumber,item.ListPrice-item.DiscountAmount, item.ParentRolledUpQuoteItem, otuRolledUpQuoteItem))
			if item.ListPrice-item.DiscountAmount == 0 and item.ParentRolledUpQuoteItem == otuRolledUpQuoteItem:
				item.QI_SC_Cost.Value = (1-item.QI_SC_Margin_Percent.Value/100)*(item.ListPrice)
			else:
				item.QI_SC_Cost.Value = (1-item.QI_SC_Margin_Percent.Value/100)*(item.ListPrice-item.DiscountAmount)
		costPrice[rolledupKey] = item.QI_SC_Cost.Value
		pwtwKey = None
		plsg_key = ''
		if str(item.PartNumber) in plsgDict_keyList:
			plsg_key  = item.PartNumber
			if str('|') in str(plsgDict.keys()):
				for key in plsgDict:
						if str(item.PartNumber) in str(key):
								plsg_key = key
								break
			item.QI_PLSG.Value 		= plsgDict[plsg_key]['PLSG'] if plsg_key else ''
			item.QI_PLSGDesc.Value 	= plsgDict[plsg_key]['PLSGDesc'] if plsg_key else ''
			wtwFactor[item.RolledUpQuoteItem] = float(plsgDict[plsg_key]['WTWFactor']) if plsg_key else ''
			pwtwKey = item.RolledUpQuoteItem
		elif wtwFactor:
			pwtwKeys = [skey for skey in wtwFactor if item.RolledUpQuoteItem.startswith(skey)]
			pwtwKey = max(pwtwKeys, key=len) if pwtwKeys else None

		item.QI_UnitWTWCost.Value = item.QI_ExtendedWTWCost.Value = item.QI_SC_Cost.Value / (1 + wtwFactor.get(pwtwKey, 0)) if item.QI_SC_Cost.Value else 0
		if len(list(item.Children)) == 0:
			item.QI_PLLOB.Value = 'LSS'


		#item.QI_SC_Total_Discount_Percent.Value = item.QI_MPA_Discount_Percent.Value + item.QI_Additional_Discount_Percent.Value + float(itemValues['SC_Item_BlockDiscount']) if 'SC_Item_BlockDiscount' in itemValues else 0
		# if (item.QI_MPA_Discount_Percent.Value + item.QI_Additional_Discount_Percent.Value + float(itemValues['SC_Item_BlockDiscount']) if 'SC_Item_BlockDiscount' in itemValues else 0) > 100:
		#     Quote.Messages.Add("For item : '{}' Total Discount exceeds 100% (Block Discount: {})".format(item.RolledUpQuoteItem, float(itemValues['SC_Item_BlockDiscount']) if 'SC_Item_BlockDiscount' in itemValues else 0))
		#     Trace.Write('********************Rank: {}, Discount : {}, BlockDiscount: {}'.format(item.Rank, item.QI_SC_Total_Discount_Percent.Value, itemValues.get('SC_Item_BlockDiscount',0)))
		#     item.QI_Additional_Discount_Percent.Value = 0
		#     item.QI_MPA_Discount_Percent.Value = 0
		#     item.QI_MPA_Discount_Percent.Value = 0
		if item.QI_ContractType.Value == 'Renewal':
			if item.Description != 'Parts Replacement':
				if item.Quantity > 0:
					item.QI_SC_Scope_Change.Value = ((item.QI_SC_ScopeAdditionPrice.Value * ((item.ListPrice-item.DiscountAmount)/item.ListPrice)) if item.ListPrice > 0 else 0) + ((item.QI_SC_ScopeReductionPrice.Value * (item.QI_SC_Previous_Year_Sell_Price.Value/item.QI_SC_Previous_Year_List_Price.Value)) if item.QI_SC_Previous_Year_List_Price.Value > 0 else 0)
					item.QI_SC_Price_Impact.Value = (item.ListPrice-item.DiscountAmount) - (item.QI_SC_Scope_Change.Value + item.QI_SC_Previous_Year_Sell_Price.Value)
				else:
					item.QI_SC_Scope_Change.Value = -1 * item.QI_SC_Previous_Year_Sell_Price.Value
					item.QI_SC_Price_Impact.Value = 0
			elif item.Description == 'Parts Replacement':
				if item.Quantity > 0:
					item.QI_SC_Scope_Change.Value = item.QI_SC_Scope_Change.Value
					item.QI_SC_Price_Impact.Value = (item.ListPrice-item.DiscountAmount) - (item.QI_SC_Scope_Change.Value + item.QI_SC_Previous_Year_Sell_Price.Value)
				else:
					item.QI_SC_Scope_Change.Value = -1 * item.QI_SC_Previous_Year_Sell_Price.Value
					item.QI_SC_Price_Impact.Value = 0
			py_listPrice[rolledupKey] = item.ListPrice
			py_sellPrice[rolledupKey] = item.ListPrice-item.DiscountAmount
		else:
			item.QI_SC_Scope_Change.Value = (item.ListPrice-item.DiscountAmount)
			item.QI_SC_Price_Impact.Value = 0
		if qCurrency == 'USD':
			item.QI_SC_Price_Impact.Value = item.QI_SC_Price_Impact.Value/exRate
			item.QI_SC_Previous_Year_List_Price.Value = item.QI_SC_Previous_Year_List_Price.Value/pexRate
			item.QI_SC_Previous_Year_Sell_Price.Value = item.QI_SC_Previous_Year_Sell_Price.Value/pexRate
			item.QI_SC_Honeywell_List_Price.Value = item.QI_SC_Honeywell_List_Price.Value/exRate
			item.QI_SC_Scope_Change.Value = item.QI_SC_Scope_Change.Value/exRate
			item.QI_SC_Price_Impact.Value = item.QI_SC_Price_Impact.Value/exRate
	if Quote.Items.Count == 1:
		Quote.MainItems[0].QI_MPA_Discount_Percent.Value = 0
		Quote.MainItems[0].QI_Additional_Discount_Percent.Value = 0
	Quote.CustomFields.AssignValue('SC_CF_RENEWAL_FLAG',"0")