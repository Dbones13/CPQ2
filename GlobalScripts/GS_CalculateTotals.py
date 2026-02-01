def addToTotal(totalDict , key , value):
	totalDict[key] = totalDict.get(key , 0) + value

def calculateRolledUpValues(Item, quote):
	if Item.IsMainItem and len(list(Item.Children)):
		total = dict()
		for item in Item.Children:
			calculateRolledUpValues(item, quote)
			item.QI_RegionalMargin.Value    = item.ExtendedAmount - item.ExtendedCost
			item.QI_WTWMargin.Value = item.ExtendedAmount - item.QI_ExtendedWTWCost.Value
			if item.ExtendedAmount != 0:
				item.QI_RegionalMarginPercent.Value = (item.QI_RegionalMargin.Value * 100)/item.ExtendedAmount if item.ExtendedAmount > 0 else 0
				item.QI_WTWMarginPercent.Value = (item.QI_WTWMargin.Value / item.ExtendedAmount) * 100 if item.ExtendedAmount > 0 else 0
			else:
				item.QI_RegionalMarginPercent.Value = 0
				item.QI_WTWMarginPercent.Value = 0
			total["Cost"]                           = item.Cost + total.get("Cost" , 0)
			total["ListPrice"]                      = item.ListPrice + total.get("ListPrice" , 0)
			total["ExtendedCost"]                   = item.ExtendedCost + total.get("ExtendedCost" , 0)
			# total["QI_India_discounted_TP"]         = item.QI_India_discounted_TP.Value + total.get("QI_India_discounted_TP" , 0)
			total["ExtendedListPrice"]              = item.ExtendedListPrice + total.get("ExtendedListPrice" , 0)
			total["NetPrice"]                       = item.NetPrice + total.get("NetPrice" , 0)
			total["ExtendedAmount"]                 = item.ExtendedAmount + total.get("ExtendedAmount" , 0)
			total["QI_Tariff_Amount"]               = item.QI_Tariff_Amount.Value + total.get("QI_Tariff_Amount" , 0)
			total["QI_Sell_Price_Inc_Tariff"]		= item.QI_Sell_Price_Inc_Tariff.Value + total.get("QI_Sell_Price_Inc_Tariff", 0)

			total["QI_UnitSellPrice"]               = item.QI_UnitSellPrice.Value + total.get("QI_UnitSellPrice" , 0)
			total["wtwCost"]                        = item.QI_UnitWTWCost.Value + total.get("wtwCost" , 0)
			total["QI_ExtendedWTWCost"]             = item.QI_ExtendedWTWCost.Value + total.get("QI_ExtendedWTWCost" , 0)
			total["QI_MPA_Discount_Amount"]         = item.QI_MPA_Discount_Amount.Value + total.get("QI_MPA_Discount_Amount" , 0)
			total["QI_Additional_Discount_Amount"]  = item.QI_Additional_Discount_Amount.Value + total.get("QI_Additional_Discount_Amount",0)
			total["QI_Additional_Discount_Percent"] = item.QI_Additional_Discount_Percent.Value+ total.get("QI_Additional_Discount_Percent",0)
			total["QI_PROS_Guidance_Recommended_Price"]  = item.QI_PROS_Guidance_Recommended_Price.Value  + total.get("QI_PROS_Guidance_Recommended_Price" , 0)
			total["QI_SC_Cost"]                     = item.QI_SC_Cost.Value  + total.get("QI_SC_Cost" , 0)
			total["QI_SC_Honeywell_List_Price"]     = item.QI_SC_Honeywell_List_Price.Value  + total.get("QI_SC_Honeywell_List_Price" , 0)
			total["QI_SC_Scope_Change"]             = item.QI_SC_Scope_Change.Value  + total.get("QI_SC_Scope_Change" , 0)
			total["QI_SC_Price_Impact"]             = item.QI_SC_Price_Impact.Value  + total.get("QI_SC_Price_Impact" , 0)
			total["QI_SC_Previous_Year_List_Price"] = item.QI_SC_Previous_Year_List_Price.Value  + total.get("QI_SC_Previous_Year_List_Price" , 0)
			total["QI_SC_Previous_Year_Sell_Price"] = item.QI_SC_Previous_Year_Sell_Price.Value  + total.get("QI_SC_Previous_Year_Sell_Price" , 0)
			total["QI_SC_EscalationPrice"]          = item.QI_SC_EscalationPrice.Value  + total.get("QI_SC_EscalationPrice" , 0)
			total["QI_SC_Product_ListPrice"]        = item.QI_SC_Product_ListPrice.Value  + total.get("QI_SC_Product_ListPrice" , 0)
			
		Item.Cost                                   = total["ExtendedCost"] / Item.Quantity if Item.Quantity > 0 else 0
		Item.ListPrice                              = total["ExtendedListPrice"] / Item.Quantity if Item.Quantity > 0 else 0
		Item.ExtendedCost                           = total["ExtendedCost"]
		# Item.QI_India_discounted_TP.Value           = total["QI_India_discounted_TP"]
		Item.ExtendedAmount                         = total["ExtendedAmount"]
		Item.QI_Tariff_Amount.Value                 = total["QI_Tariff_Amount"]
		Item.QI_Sell_Price_Inc_Tariff.Value			= total["QI_Sell_Price_Inc_Tariff"]

		Item.ExtendedListPrice                      = total["ExtendedListPrice"]
		Item.NetPrice                               = total["NetPrice"] 
		Item.QI_UnitSellPrice.Value                 = total["ExtendedAmount"] / Item.Quantity if Item.Quantity > 0 else 0
		Item.QI_UnitWTWCost.Value                   = total["QI_ExtendedWTWCost"] / Item.Quantity if Item.Quantity > 0 else 0
		if quote.GetCustomField('Quote Type').Content in ['Contract New','Contract Renewal']:
			Item.QI_ExtendedWTWCost.Value               = total["QI_ExtendedWTWCost"]
			Item.ExtendedCost                           = total["QI_SC_Cost"]
		else:
			Item.QI_ExtendedWTWCost.Value               = total["QI_ExtendedWTWCost"]
		Item.QI_MPA_Discount_Amount.Value           = total["QI_MPA_Discount_Amount"]
		Item.QI_Additional_Discount_Amount.Value    = total["QI_Additional_Discount_Amount"]
		Item.QI_SC_Cost.Value                       = total["QI_SC_Cost"]
		Item.QI_SC_Honeywell_List_Price.Value       = total["QI_SC_Honeywell_List_Price"]
		Item.QI_SC_Scope_Change.Value               = total["QI_SC_Scope_Change"]
		Item.QI_SC_Price_Impact.Value               = total["QI_SC_Price_Impact"]
		Item.QI_SC_Previous_Year_List_Price.Value   = total["QI_SC_Previous_Year_List_Price"]
		Item.QI_SC_Previous_Year_Sell_Price.Value   = total["QI_SC_Previous_Year_Sell_Price"]
		Item.QI_SC_EscalationPrice.Value            = total["QI_SC_EscalationPrice"]
		Item.QI_SC_Product_ListPrice.Value          = total["QI_SC_Product_ListPrice"]
		Item.QI_Target_Sell_Price.Value 			= total["ExtendedListPrice"] - total["QI_MPA_Discount_Amount"]

		Item.QI_RegionalMargin.Value    = Item.ExtendedAmount - Item.ExtendedCost
		Item.QI_WTWMargin.Value = Item.ExtendedAmount - Item.QI_ExtendedWTWCost.Value
		Item.DiscountAmount             = total["ExtendedListPrice"] - total["ExtendedAmount"]
		if total["ExtendedListPrice"] != 0:
			Item.DiscountPercent = ((total["ExtendedListPrice"] - total["ExtendedAmount"]) * 100)/total["ExtendedListPrice"] if total["ExtendedListPrice"] > 0 else 0
			Item.QI_MPA_Discount_Percent.Value = (Item.QI_MPA_Discount_Amount.Value * 100)/total["ExtendedListPrice"] if total["ExtendedListPrice"] > 0 else 0
			Item.QI_Additional_Discount_Percent.Value = (Item.QI_Additional_Discount_Amount.Value * 100)/total["ExtendedListPrice"] if total["ExtendedListPrice"] > 0 else 0
		else:
			Item.DiscountPercent = 0
		if Item.ExtendedAmount != 0:
			Item.QI_RegionalMarginPercent.Value = (Item.QI_RegionalMargin.Value * 100)/Item.ExtendedAmount if Item.ExtendedAmount > 0 else 0
			Item.QI_WTWMarginPercent.Value = (Item.QI_WTWMargin.Value / Item.ExtendedAmount) * 100 if Item.ExtendedAmount > 0 else 0
		else:
			Item.QI_RegionalMarginPercent.Value = 0
			Item.QI_WTWMarginPercent.Value = 0
		if Item.QI_ProductLine.Value =='':
			Item.QI_PROS_Guidance_Recommended_Price.Value = total["QI_PROS_Guidance_Recommended_Price"]
		if quote.GetCustomField('Quote Type').Content in ('Contract New','Contract Renewal'):
			if total["QI_SC_Cost"] != 0:
				#Item.QI_ExtendedWTWCost.Value = total["QI_SC_Cost"]
				Item.QI_SC_Margin_Percent.Value = 100 - round((Item.QI_SC_Cost.Value/Item.ExtendedAmount)*100,2) if Item.ExtendedAmount else 0
			else:
				Item.QI_SC_Margin_Percent.Value = 0
			Item.QI_SC_Total_Discount_Percent.Value = Item.DiscountPercent
			Item.QI_SC_Total_Discount_Price.Value = (quote.SelectedMarket.CurrencySign if quote.GetCustomField('SC_CF_PRICE_TOGGLE').Content != 'USD' else '$') + ' ' + (UserPersonalizationHelper.ToUserFormat(round(Item.DiscountAmount/float(quote.GetCustomField('SC_CF_EXCHANGE_RATE').Content),2)) if quote.GetCustomField('SC_CF_PRICE_TOGGLE').Content == 'USD' else UserPersonalizationHelper.ToUserFormat(round(Item.DiscountAmount,2)))
	elif not(Item.IsSimple) and not Item.IsVariant and Item.ProductName not in ['Write-In Entitlement-Hardening Services','Write-In Entitlement-Hardening Cyber Care','Write-In Entitlement-Cyber App Control','Write-In Entitlement-Cyber App Control Care','WriteIn','Generic System Child Product'] and Item.CategoryName!='Kits & Enhancements' and Item.ProductTypeName!='Honeywell Material' and len(list(Item.Children))==0:
		Item.Cost                                   = 0
		Item.ListPrice                              = 0
		Item.ExtendedCost                           = 0
		Item.ExtendedAmount                         = 0
		Item.QI_Tariff_Amount.Value                 = 0
		Item.QI_Sell_Price_Inc_Tariff.Value			= 0
		Item.ExtendedListPrice                      = 0
		Item.NetPrice                               = 0
		Item.QI_UnitSellPrice.Value                 = 0
		Item.QI_UnitWTWCost.Value                   = 0
	elif Item.PartNumber in ('Write-In Standard Warranty'):
		totalSellPrice = sum(float(item.ExtendedAmount) if item.IsMainItem and item.ParentItemGuid == '' else 0 for item in quote.Items)
		Writein_std_wrnty = quote.GetCustomField('Writein_std_wrnty').Content.split(":")
		if len(Writein_std_wrnty) >= 2 and float(Writein_std_wrnty[0]) > 0:
			cost = float(float(totalSellPrice) * float(Writein_std_wrnty[1]) / 100)
			Item.Cost = cost
			query = SqlHelper.GetFirst("SELECT WTW_FACTOR from HPS_PLSG_WTW_FACTOR wtw JOIN WriteInProducts wrt on wrt.ProductLineSubGroup = wtw.PL_PLSG where wrt.Product = 'Write-In Standard Warranty'")
			wtwFac =  query.WTW_FACTOR if query else 0
			wtwCost = cost / (1 + float(wtwFac)) if cost else 0.0
			Item.ExtendedCost = cost * Item.Quantity
			Item['QI_UnitWTWCost'].Value = wtwCost
			Item['QI_ExtendedWTWCost'].Value = wtwCost * Item.Quantity
			Item['QI_RegionalMargin'].Value = (Item.ExtendedAmount - (cost * Item.Quantity))
			Item['QI_WTWMargin'].Value = (Item.ExtendedListPrice - (wtwCost * Item.Quantity))
			if Item.ExtendedAmount != 0:
				Item['QI_RegionalMarginPercent'].Value = (Item.ExtendedAmount - (cost * Item.Quantity))/Item.ExtendedAmount * 100
				Item['QI_WTWMarginPercent'].Value = (Item.ExtendedListPrice - (wtwCost * Item.Quantity))/Item.ExtendedListPrice * 100

def calculateParent(quote):
	fme_list = [i.PARTNUMBER for i in SqlHelper.GetList("Select PARTNUMBER from FME_PARTS")]
	for item in quote.Items:
		rolledUpItem = item.RolledUpQuoteItem
		if item.IsMainItem and item.ParentItemGuid == '' and item.PartNumber not in fme_list:
			calculateRolledUpValues(item.AsMainItem, quote)

def getWriteInProductType(quote):
	writeInProductType = dict()
	partNumberList = []
	for item in quote.Items:
		if item.IsOptional or (item.AsMainItem and len(list(item.AsMainItem.Children))):
			continue
		if item.ProductTypeName == 'Write-In':
			partNumberList.append(item.PartNumber)
	if len(partNumberList) > 0:
		strPartNubmers = ",".join(["'{0}'".format(x) for x in partNumberList])
		resProductType = SqlHelper.GetList("SELECT Product,ProductCategory FROM WriteInProducts WHERE Product in ({})".format(strPartNubmers))
		if resProductType:
			for row in resProductType:
				writeInProductType[row.Product] = row.ProductCategory
	return writeInProductType

def getRecommendedDiscount(quote,item,recommendedMarketlookup,bookingLOB):
	recommendedMpaDiscountAmount = 0
	effectiveDate = quote.EffectiveDate.ToString('MM/dd/yyyy')
	query = "select Discount from MARKETDISCOUNT_SCHEDULE_PERCENTAGE md join HPS_PRODUCTS_MASTER hpm on hpm.PLSG = md.PL_PLSG where hpm.PartNumber = '{0}' and md.Market_Schedule = '{1}' and md.LOB = '{2}' and ISNULL(NULLIF(md.Valid_From,''),CONVERT(DATE,'{3}')) <= '{3}' and ISNULL(NULLIF(md.Valid_To,''),GETDATE()) >= '{3}' ".format(item.PartNumber,recommendedMarketlookup,bookingLOB,effectiveDate)
	result = SqlHelper.GetFirst(query)
	if result:
		discount = result.Discount
		recommendedMpaDiscountAmount = item.ExtendedListPrice * (float(discount)/100)
	return recommendedMpaDiscountAmount

def calculateProductLines(quote):
	productLines = dict()
	PLSGroups    = dict()
	productTypes = dict()
	quoteTotal   = dict()
	writeInProductType = getWriteInProductType(quote)
	recommendedMarketlookup = quote.GetCustomField("Recommended Discount Plan").Content
	bookingLOB =  quote.GetCustomField("Booking LOB").Content
	nonDiscountableParts = ['CEPS_CAD','CEPS_PE','CEPS_PM','D4418111','D4418113','SVC-PER-DIEM','SVC-PMC-TRAV-AIR','SVC-PMC-TRAV-CAR','SVC-PMC-TRAV-PVT','ECSA-1001','ECSP-1001']
	nonDiscountablePLSG  = ['7725-7D38','7029-7179','7076-7000']
	ccc_regional_cost = float(0)

	for item in quote.Items:
		if item.PartNumber == 'Write-In Travel and Living':
			item['QI_ProductLine'].Value = str(7036)
			item['QI_ProductLineDesc'].Value = 'Administrative and General Expenditure - Travel and Living'
		if item.IsOptional or (item.AsMainItem and len(list(item.AsMainItem.Children))) or (not(item.QI_ProductLine.Value) and item.ProductTypeName != "Service Contract"):
			continue

		prodtuctLineDict = productLines.get(item.QI_ProductLine.Value , dict())
		lv_ETOTotal=float(item.Quantity * item['QI_GAS_ETO_PRICE_ADD'].Value)#CXCPQ-42168:06/13/2023 : Get ETO Price

		addToTotal(prodtuctLineDict , 'mpaDiscountAmount' , item['QI_MPA_Discount_Amount'].Value)
		addToTotal(prodtuctLineDict , 'additionalDiscountAmount' , item['QI_Additional_Discount_Amount'].Value)
		addToTotal(prodtuctLineDict , 'PROSRecommendedPrice' , item['QI_PROS_Guidance_Recommended_Price'].Value)
		addToTotal(prodtuctLineDict , 'totalListPrice' , item.ExtendedListPrice)
		addToTotal(prodtuctLineDict , 'totalCost' , item.ExtendedCost)
		addToTotal(prodtuctLineDict , 'totalWTWCost' , item['QI_ExtendedWTWCost'].Value)
		addToTotal(prodtuctLineDict , 'totalExtendedAmount' , item.ExtendedAmount)
		addToTotal(prodtuctLineDict , 'totalETOPrice' , lv_ETOTotal)#CXCPQ-42168:06/13/2023:Added totalETOPrice Key
		addToTotal(prodtuctLineDict , 'totalMPALabor' , item.Training_QI_Gst_KP.Value)
		#----Changed by Chirag for including non discountable PLSG
		if item.PartNumber not in nonDiscountableParts and item.QI_PLSG.Value not in nonDiscountablePLSG:
				addToTotal(prodtuctLineDict , 'maxDiscountLimit' , item['QI_Target_Sell_Price'].Value)
		if quote.GetCustomField('Booking LOB').Content == 'CCC':
			if quote.GetCustomField('Booking Country').Content.lower() == 'united states':
				ccc_regional_cost += float(item['QI_ExtendedWTWCost'].Value) if str(item.QI_ProductCostCategory.Value) in ('Honeywell Material','Honeywell Software') else float(item.ExtendedCost)
				addToTotal(prodtuctLineDict , 'totalCCCRegionalCost' , item['QI_ExtendedWTWCost'].Value if str(item.QI_ProductCostCategory.Value) in ('Honeywell Material','Honeywell Software') else item.ExtendedCost)
			elif quote.GetCustomField('Booking Country').Content.lower() == 'brazil':
				ccc_regional_cost += (float(item.ExtendedAmount)*float(0.80)) if str(item.QI_ProductCostCategory.Value) in ('Honeywell Material','Honeywell Software') else float(item.ExtendedCost)
				addToTotal(prodtuctLineDict , 'totalCCCRegionalCost' , (float(item.ExtendedAmount)*float(0.80)) if str(item.QI_ProductCostCategory.Value) in ('Honeywell Material','Honeywell Software') else float(item.ExtendedCost))
			else:
				ccc_regional_cost += (float(item.ExtendedAmount)*float(0.85)) if str(item.QI_ProductCostCategory.Value) in ('Honeywell Material','Honeywell Software') else float(item.ExtendedCost)
				addToTotal(prodtuctLineDict , 'totalCCCRegionalCost' , (float(item.ExtendedAmount)*float(0.85)) if str(item.QI_ProductCostCategory.Value) in ('Honeywell Material','Honeywell Software') else float(item.ExtendedCost))
		prodtuctLineDict['desc'] = item.QI_ProductLineDesc.Value
		productLines[item.QI_ProductLine.Value] = prodtuctLineDict

		#------------------------------------------------------------------

		PLSGroupDict = PLSGroups.get(item.QI_PLSG.Value , dict())

		addToTotal(PLSGroupDict , 'mpaDiscountAmount' , item['QI_MPA_Discount_Amount'].Value)
		addToTotal(PLSGroupDict , 'additionalDiscountAmount' , item['QI_Additional_Discount_Amount'].Value)
		addToTotal(PLSGroupDict , 'PROSRecommendedPrice' , item['QI_PROS_Guidance_Recommended_Price'].Value)
		addToTotal(PLSGroupDict , 'totalListPrice' , item.ExtendedListPrice)
		addToTotal(PLSGroupDict , 'totalCost' , item.ExtendedCost)
		addToTotal(PLSGroupDict , 'totalWTWCost' , item['QI_ExtendedWTWCost'].Value)
		addToTotal(PLSGroupDict , 'totalExtendedAmount' , item.ExtendedAmount)
		addToTotal(PLSGroupDict , 'totalETOPrice' , lv_ETOTotal)#CXCPQ-42168:06/13/2023:Added totalETOPrice Key
		addToTotal(PLSGroupDict , 'totalMPALabor' , item.Training_QI_Gst_KP.Value)


		if item.PartNumber not in nonDiscountableParts and item.QI_PLSG.Value not in nonDiscountablePLSG:
				addToTotal(PLSGroupDict , 'maxDiscountLimit' , item['QI_Target_Sell_Price'].Value)

		PLSGroupDict['desc'] = item.QI_PLSGDesc.Value
		PLSGroups[item.QI_PLSG.Value] = PLSGroupDict

		#-------------------------------------------------------------------
		itemProductTypeName = item.ProductTypeName if item.ProductName != 'TPC_Product' else item.QI_ProjectType.Value
		if itemProductTypeName == 'Write-In':
			itemProductTypeName = writeInProductType.get(str(item['QI_PLSG'].Value), item.ProductTypeName)

		productTypeDict = productTypes.get(itemProductTypeName , dict())

		addToTotal(productTypeDict , 'mpaDiscountAmount' , item['QI_MPA_Discount_Amount'].Value)
		addToTotal(productTypeDict , 'additionalDiscountAmount' , item['QI_Additional_Discount_Amount'].Value)
		addToTotal(productTypeDict , 'PROSRecommendedPrice' , item['QI_PROS_Guidance_Recommended_Price'].Value)
		addToTotal(productTypeDict , 'totalListPrice' , item.ExtendedListPrice)
		addToTotal(productTypeDict , 'totalCost' , item.ExtendedCost)
		addToTotal(productTypeDict , 'indiaDiscountedTP' , item['QI_India_discounted_TP'].Value) #CXCPQ-101295
		addToTotal(productTypeDict , 'totalWTWCost' , item['QI_ExtendedWTWCost'].Value)
		addToTotal(productTypeDict , 'totalExtendedAmount' , item.ExtendedAmount)
		addToTotal(productTypeDict , 'totalETOPrice' , lv_ETOTotal)#CXCPQ-42168:06/13/2023:Added totalETOPrice Key
		addToTotal(productTypeDict , 'totalMPALabor' , item.Training_QI_Gst_KP.Value)
		if item.PartNumber not in nonDiscountableParts and item.QI_PLSG.Value not in nonDiscountablePLSG:
			addToTotal(productTypeDict , 'maxDiscountLimit' , item['QI_Target_Sell_Price'].Value)
		productTypeDict['desc'] = itemProductTypeName
		productTypes[itemProductTypeName] = productTypeDict

		#--------------------------------------------------------------------

		addToTotal(quoteTotal , 'mpaDiscountAmount' , item['QI_MPA_Discount_Amount'].Value)
		addToTotal(quoteTotal , 'recommendedMpaDiscountAmount' , getRecommendedDiscount(quote,item,recommendedMarketlookup,bookingLOB))

		addToTotal(quoteTotal , 'additionalDiscountAmount' , item['QI_Additional_Discount_Amount'].Value)
		addToTotal(quoteTotal , 'PROSRecommendedPrice' , item['QI_PROS_Guidance_Recommended_Price'].Value)
		addToTotal(quoteTotal , 'totalListPrice' , item.ExtendedListPrice)
		addToTotal(quoteTotal , 'totalCost' , item.ExtendedCost)
		addToTotal(quoteTotal , 'indiaDiscountedTP' , item['QI_India_discounted_TP'].Value) #CXCPQ-101295
		addToTotal(quoteTotal , 'totalWTWCost' , item['QI_ExtendedWTWCost'].Value)
		addToTotal(quoteTotal , 'totalExtendedAmount' , item.ExtendedAmount)
		addToTotal(quoteTotal , 'totalTariffAmount' , item['QI_Tariff_Amount'].Value)
		addToTotal(quoteTotal , 'quoteSellPriceInclTariff' , item['QI_Sell_Price_Inc_Tariff'].Value)
		addToTotal(quoteTotal , 'totalRegionalMargin' , item['QI_RegionalMargin'].Value)
		addToTotal(quoteTotal , 'totalETOPrice' , lv_ETOTotal)#CXCPQ-42168:06/13/2023:Added totalETOPrice Key
		if item.PartNumber not in nonDiscountableParts and item.QI_PLSG.Value not in nonDiscountablePLSG:
			addToTotal(quoteTotal , 'maxDiscountLimit' , item['QI_Target_Sell_Price'].Value)
	addToTotal(quoteTotal , 'totalCCCRegionalCost' , ccc_regional_cost)
	return (productLines , PLSGroups , productTypes , quoteTotal)

def calculateQuoteTotals(quote):
	if quote.Items.Count == 0: return dict()
	totalDict = {}

	topLevelItems = filter(lambda item:item.ParentRolledUpQuoteItem == '' , quote.Items)
	for item in topLevelItems:
		lv_ETOTotal=float(item.Quantity * item['QI_GAS_ETO_PRICE_ADD'].Value)#CXCPQ-42168:06/13/2023 : Get ETO Price
		addToTotal(totalDict , 'unitListPrice' , item.ExtendedListPrice)
		addToTotal(totalDict , 'unitCost' , item.Cost)
		addToTotal(totalDict , 'unitWTWCost' , item['QI_UnitWTWCost'].Value)

		addToTotal(totalDict , 'mpaDiscountAmount' , item['QI_MPA_Discount_Amount'].Value)
		addToTotal(totalDict , 'additionalDiscountAmount' , item['QI_Additional_Discount_Amount'].Value)
		

		addToTotal(totalDict , 'totalListPrice' , item.ExtendedListPrice)
		addToTotal(totalDict , 'totalCost' , item.ExtendedCost)
		addToTotal(totalDict , 'totalWTWCost' , item['QI_ExtendedWTWCost'].Value)
		addToTotal(totalDict , 'totalNetPrice' , item.NetPrice)
		addToTotal(totalDict , 'totalExtendedAmount' , item.ExtendedAmount)
		addToTotal(totalDict , 'totalRegionalMargin' , item['QI_RegionalMargin'].Value)
		addToTotal(totalDict , 'totalETOPrice' , lv_ETOTotal)#CXCPQ-42168:06/13/2023:Added totalETOPrice Key
		
		addToTotal(totalDict , 'totalTariffAmount' , item['QI_Tariff_Amount'].Value)
		addToTotal(totalDict , 'totalSellPriceInclTariff' , item['QI_Sell_Price_Inc_Tariff'].Value)
	return totalDict

def calculateTotalListPrice(quote):
	listPrice = 0
	for item in quote.Items:
		if item.AsMainItem and len(list(item.AsMainItem.Children)):
			continue
		listPrice += item.ExtendedListPrice
	return listPrice