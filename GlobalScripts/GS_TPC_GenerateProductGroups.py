def getMarketScheduleDiscount(Quote,prdPLSGs,marketScheduleLookup,bookingLOB):
	disPLSGs = {}
	effectiveDate = Quote.EffectiveDate.ToString('MM/dd/yyyy')
	result = SqlHelper.GetList("select PL_PLSG, Discount, Minimum_Margin from MARKETDISCOUNT_SCHEDULE_PERCENTAGE(nolock) md where md.PL_PLSG IN {0} and md.Market_Schedule = '{1}' and md.LOB = '{2}' and ISNULL(NULLIF(md.Valid_From,''),CONVERT(DATE,'{3}')) <= '{3}' and ISNULL(NULLIF(md.Valid_To,''),GETDATE()) >= '{3}' ".format(str(tuple(prdPLSGs)).replace(',)',')'),marketScheduleLookup,bookingLOB,effectiveDate))
	for row in result:
		#{'Discount': row.Discount, 'MinimumMargin': row.Minimum_Margin}
		disPLSGs[row.PL_PLSG] = row.Discount
	return disPLSGs

def checkMPAPricePlanValidty(Quote):
	validcheckForMarketSchedule = False
	mpaValidity = Quote.GetCustomField('MPA Validity').Content
	if mpaValidity:
		mpaValidityDate = UserPersonalizationHelper.CovertToDate(mpaValidity).Date
		if Quote.DateModified.Date > mpaValidityDate:
			validcheckForMarketSchedule = True
	return validcheckForMarketSchedule

def getMpaDiscountPercent(prdPLSGs, pricePlan, honeywellRef, mpaVal):
	disPLSGs = {}
	result = None
	if honeywellRef:
		result = SqlHelper.GetList("SELECT Product_Line, Discount FROM MPA_DISCOUNTS(nolock) where Product_Line IN {} and Price_Plan='{}' and Honeywell_Ref = '{}'".format(str(tuple(prdPLSGs)).replace(',)',')'), pricePlan , honeywellRef))
	elif mpaVal:
		ctval = SqlHelper.GetFirst("SELECT Salesforce_Agreement_ID FROM MPA_PRICE_PLAN_MAPPING(nolock) WHERE Agreement_Name='{}'".format(mpaVal))
		result = SqlHelper.GetList("SELECT Product_Line, Discount FROM MPA_DISCOUNTS where Product_Line IN {} and Price_Plan='{}' and Salesforce_Agreement_ID = '{}'".format(str(tuple(prdPLSGs)).replace(',)',')'), pricePlan , ctval.Salesforce_Agreement_ID))
	if result:
		for row in result:
			disPLSGs[row.Product_Line] = row.Discount
	return disPLSGs


def getThresold(Quote, pricePlan , ref, QuoteType):
	mpa = Quote.GetCustomField('AccountId').Content
	sf_agg_id = SqlHelper.GetFirst("SELECT Salesforce_Agreement_ID FROM MPA_ACCOUNT_MAPPING(nolock) WHERE Salesforce_ID='{}'".format(mpa))
	if sf_agg_id:
		res = SqlHelper.GetFirst("Select Order_Threshold_Parts,Order_Threshold_Systems from MPA_PRICE_PLAN_MAPPING(nolock) where Salesforce_Agreement_ID='{}' and Price_Plan_Name='{}'".format(sf_agg_id.Salesforce_Agreement_ID,pricePlan))
	else:
		res = SqlHelper.GetFirst("Select Order_Threshold_Parts,Order_Threshold_Systems from MPA_PRICE_PLAN_MAPPING(nolock) where (Honeywell_Ref='{}' and Honeywell_Ref != '') and Price_Plan_Name='{}'".format(ref , pricePlan))
	if res:
		thresold = res.Order_Threshold_Parts if QuoteType == 'Parts and Spot' else res.Order_Threshold_Systems
		return float(thresold) if thresold else 0
	return 0

def getMPA(product):
	disPLSGs = {}
	pricePlan = Quote.GetCustomField('MPA Price Plan').Content
	honeywellRef = Quote.GetCustomField('MPA Honeywell Ref').Content
	prdTotal = product.ParseString('<*CTX( Container(TPC_PartsContainer).Sum(ExtendedListPrice) )*>')
	prdPLSGs = product.ParseString('<*CTX( Container(TPC_PartsContainer).UniqueValues(QI_PLSG).Separator(,) )*>').split(',')
	orderTotal = float(prdTotal) if prdTotal else 0
	QuoteType = Quote.GetCustomField('Quote Type').Content
	sfid = Quote.GetCustomField('AccountId').Content
	sfan = SqlHelper.GetFirst("SELECT Agreement_Name  FROM MPA_ACCOUNT_MAPPING WHERE Salesforce_ID  ='"+str(sfid)+"'")
	Quote.GetCustomField('MPA').Content = sfan.Agreement_Name if sfan is not None else ''
	MPA = Quote.GetCustomField('MPA').Content
	exchangeRate = Quote.GetCustomField('Exchange Rate').Content
	bookingLOB = Quote.GetCustomField('Booking LOB').Content
	marketScheduleLookup = Quote.GetCustomField('Selected Discount Plan').Content
	mpaValidity = Quote.GetCustomField('MPA Validity').Content
	validcheck = checkMPAPricePlanValidty(Quote)

	thresold = getThresold(Quote , pricePlan , honeywellRef , QuoteType) * float(exchangeRate)
	Quote.GetCustomField("MPA Threshold").Content = str(thresold or 0)
	if pricePlan and thresold <= float(orderTotal) and not validcheck:
		disPLSGs = getMpaDiscountPercent( prdPLSGs , pricePlan ,honeywellRef, MPA)
	elif QuoteType == "Projects" and marketScheduleLookup != "List Price" and marketScheduleLookup != '':
		if Quote.GetCustomField('Selected Discount Plan').Visible==True:
			disPLSGs = getMarketScheduleDiscount(Quote,prdPLSGs,marketScheduleLookup,bookingLOB)
	else:
		if Quote.GetCustomField('Quote Tab Booking LOB').Content:
			disPLSGs = getMpaDiscountPercent(prdPLSGs , pricePlan ,honeywellRef, MPA)
	return disPLSGs #{'7025-7166': '43.00', '7025-7841': '44.00', '7021-7146': '44.00', '7023-7291': '30.00', '7023-7159': '30.00'}


def GeneratePLSGs(cProduct, partsContainer):
	disPLSGs = getMPA(cProduct)
	plsgDict = {}
	for trow in partsContainer.Rows:
		if trow["PartNumber"].strip() == '':
			continue
		RQUP_partList.append(trow["PartNumber"]) if trow['QI_CrossDistributionStatus'] == '05 PreRelease' else None
		ERP_partList.append(trow["PartNumber"]) if trow['QI_SalesText'] else None
		zoroPrice_partList.append(trow["PartNumber"]) if trow['isPriced'] == '1' and (float(trow['ExtendedListPrice']) if trow['ExtendedListPrice'] else 0) == 0 else None
		if trow['QI_PLSG'] in disPLSGs:
			trow['QI_MPA_Discount_Percent'] = str(disPLSGs[trow['QI_PLSG']])
			trow['QI_MPA_Discount_Amount'] = str(float(trow['ExtendedListPrice']) * float(trow['QI_MPA_Discount_Percent']) / 100) if trow['QI_MPA_Discount_Percent'] else  '0'
			trow['QI_Additional_Discount_Amount'] = str((float(trow['ExtendedListPrice']) - float(trow['QI_MPA_Discount_Amount']))* float(trow['QI_Additional_Discount_Percent']) / 100)  if trow['QI_Additional_Discount_Percent'] else 0
			trow["ExtendedAmount"] = str(float(trow["ExtendedListPrice"]) - float(trow["QI_Additional_Discount_Amount"]) - float(trow["QI_MPA_Discount_Amount"]))
			trow["QI_UnitSellPrice"] = str((float(trow["ExtendedAmount"]) / int(trow["Quantity"])) if trow["Quantity"] not in ['0', '', None] else 0)
			trow.Calculate()
		uKey = trow['OriginalItemNumber'] + '<*>' + trow['QI_PLSG'] + '<*>' + trow['QI_Year'] + '<*>' + trow['QI_No_Discount_Allowed']
		if uKey in plsgDict:
			plsgDict[uKey]['ListPrice'] = plsgDict[uKey]['ListPrice'] + float(trow['ExtendedListPrice']) if trow['ExtendedListPrice'] else 0
			plsgDict[uKey]['ExtendedCost'] = plsgDict[uKey]['ExtendedCost'] + float(trow['ExtendedCost']) if trow['ExtendedCost'] else 0
			plsgDict[uKey]['QI_ExtendedWTWCost'] = plsgDict[uKey]['QI_ExtendedWTWCost'] + float(trow['QI_ExtendedWTWCost']) if trow['QI_ExtendedWTWCost'] else 0
			plsgDict[uKey]['ExtendedAmount'] = plsgDict[uKey]['ExtendedAmount'] + float(trow['ExtendedAmount']) if trow['ExtendedAmount'] else 0
			plsgDict[uKey]['QI_Additional_Discount_Amount'] = plsgDict[uKey]['QI_Additional_Discount_Amount'] + float(trow['QI_Additional_Discount_Amount']) if trow['QI_Additional_Discount_Amount'] else 0
			plsgDict[uKey]['QI_MPA_Discount_Amount'] = plsgDict[uKey]['QI_MPA_Discount_Amount'] + float(trow['QI_MPA_Discount_Amount']) if trow['QI_MPA_Discount_Amount'] else 0
			plsgDict[uKey]['QI_Cost_Tariff_Amount'] = plsgDict[uKey]['QI_Cost_Tariff_Amount'] + float(trow['QI_Cost_Tariff_Amount']) if trow['QI_Cost_Tariff_Amount'] else 0
			plsgDict[uKey]['QI_Tariff_Amount'] = plsgDict[uKey]['QI_Tariff_Amount'] + float(trow['QI_Tariff_Amount']) if trow['QI_Tariff_Amount'] else 0
			plsgDict[uKey]['QI_CrossDistributionStatus'] = '05 PreRelease' if plsgDict[uKey]['QI_CrossDistributionStatus'] == '05 PreRelease' or trow['QI_CrossDistributionStatus'] == '05 PreRelease' else trow['QI_CrossDistributionStatus']
		else:
			plsgDict[uKey] = {'ProductName':trow['ParentProductName'],
					 'OriginalItemNumber': trow['OriginalItemNumber'],
					 'QI_PLSG': trow['QI_PLSG'],
					 'PLSGDesc': trow['QI_PLSGDesc'],
					 'ListPrice': float(trow['ExtendedListPrice']) if trow['ExtendedListPrice'] else 0,
					 'ExtendedCost': float(trow['ExtendedCost']) if trow['ExtendedCost'] else 0,
					 'QI_ExtendedWTWCost': float(trow['QI_ExtendedWTWCost']) if trow['QI_ExtendedWTWCost'] else 0,
					 'ExtendedAmount': float(trow['ExtendedAmount']) if trow['ExtendedAmount'] else 0,
					 'QI_Additional_Discount_Amount': float(trow['QI_Additional_Discount_Amount']) if trow['QI_Additional_Discount_Amount'] else 0,
					 'QI_MPA_Discount_Amount': float(trow['QI_MPA_Discount_Amount']) if trow['QI_MPA_Discount_Amount'] else 0,
					 'Year': trow['QI_Year'],
					 'ProductLine': trow['QI_ProductLine'],
					 'ProductLineDesc': trow['QI_ProductLineDesc'],
					 'QI_No_Discount_Allowed': trow['QI_No_Discount_Allowed'],
					 'QI_CrossDistributionStatus': trow['QI_CrossDistributionStatus'],
					 'QI_ProductCostCategory': trow['QI_ProductCostCategory'],
					 'QI_Tariff_Amount': float(trow['QI_Tariff_Amount']) if trow['QI_Tariff_Amount'] else 0,
					 'QI_Cost_Tariff_Amount': float(trow['QI_Cost_Tariff_Amount']) if trow['QI_Cost_Tariff_Amount'] else 0}
	partsContainer.Calculate()
	ttPrice, ttCost = 0, 0

	PrdContainer_Parts = cProduct.GetContainerByName("TPC_PRDContainer")
	PrdContainer_Parts.Rows.Clear()
	tPrice, tCost, twtwCost, tMPADiscount, tSellDiscount, tSellPrice = 0, 0, 0, 0, 0, 0
	for key in plsgDict:
		Prd = PrdContainer_Parts.AddNewRow()
		Prd.Product.Attr('PRD_PartNumber').AssignValue(plsgDict[key]['QI_PLSG'])
		Prd.Product.Attr('PRD_Name').AssignValue(plsgDict[key]['QI_PLSG'])
		Prd.Product.Attr('PRD_Description').AssignValue(plsgDict[key]['PLSGDesc'])
		Prd.Product.Attr('ItemQuantity').AssignValue('1')
		Prd.Product.Attr('PRD_Quantity').AssignValue('1')
		Prd.Product.Attr('PRD_Price').AssignValue(str(plsgDict[key]['ListPrice']))
		Prd.Product.Attr('PRD_Cost').AssignValue(str(plsgDict[key]['ExtendedCost']))

		Prd.Product.Attr('PRD_WTWCost').AssignValue(str(plsgDict[key]['QI_ExtendedWTWCost']))
		Prd.Product.Attr('PRD_SellPrice').AssignValue(str(plsgDict[key]['ExtendedAmount']))
		Prd.Product.Attr('PRD_SellDiscount').AssignValue(str(plsgDict[key]['QI_Additional_Discount_Amount']))
		Prd.Product.Attr('PRD_MPADiscount').AssignValue(str(plsgDict[key]['QI_MPA_Discount_Amount']))
		Prd.Product.Attr('PRD_SellDiscountPercentage').AssignValue(str(((plsgDict[key]['QI_Additional_Discount_Amount']) /(plsgDict[key]['ListPrice'] - plsgDict[key]['QI_MPA_Discount_Amount']))* 100 if plsgDict[key]['ListPrice'] - plsgDict[key]['QI_MPA_Discount_Amount'] != 0 else 0))
		Prd.Product.Attr('PRD_MPADiscountPercentage').AssignValue(str(((plsgDict[key]['QI_MPA_Discount_Amount']) /(plsgDict[key]['ListPrice']))* 100 if plsgDict[key]['ListPrice'] != 0 else 0))
		Prd.Product.Attr('PRD_No_Discount_Allowed').AssignValue(str(plsgDict[key]['QI_No_Discount_Allowed']))
		Prd.Product.Attr('PRD_Year').AssignValue(str(plsgDict[key]['Year']))
		Prd.Product.Attr('PRD_ProductLine').AssignValue(str(plsgDict[key]['ProductLine']))
		Prd.Product.Attr('PRD_ProductLineDesc').AssignValue(str(plsgDict[key]['ProductLineDesc']))
		Prd.Product.Attr('PRD_CrossDistributionStatus').AssignValue(str(plsgDict[key]['QI_CrossDistributionStatus']))
		Prd.Product.Attr('PRD_ProductCostCategory').AssignValue(str(plsgDict[key]['QI_ProductCostCategory']))
		Prd.Product.Attr('PRD_TariffAmount').AssignValue(str(plsgDict[key]['QI_Tariff_Amount']))
		Prd.Product.Attr('PRD_TariffCost').AssignValue(str(plsgDict[key]['QI_Cost_Tariff_Amount']))

		Prd["ProductName"] = str(plsgDict[key]['QI_PLSG'])
		Prd["Description"] = str(plsgDict[key]['PLSGDesc'])
		Prd["Quantity"] = "1"
		#Prd["PRD_Quantity"] = "10"
		Prd["ListPrice"] = str(plsgDict[key]['ListPrice'])
		Prd["Cost"] = str(plsgDict[key]['ExtendedCost'])

		Prd["Year"] = str(plsgDict[key]['Year'])
		Prd["WTWCost"] = str(plsgDict[key]['QI_ExtendedWTWCost'])
		Prd["SellPrice"] = str(plsgDict[key]['ExtendedAmount'])
		Prd["MPADiscountPercentage"] = str(((plsgDict[key]['QI_MPA_Discount_Amount']) /(plsgDict[key]['ListPrice']))* 100 if plsgDict[key]['ListPrice'] != 0 else 0)
		Prd["SellDiscountPercentage"] = str(((plsgDict[key]['QI_Additional_Discount_Amount']) /(plsgDict[key]['ListPrice'] - plsgDict[key]['QI_MPA_Discount_Amount']))* 100 if plsgDict[key]['ListPrice'] - plsgDict[key]['QI_MPA_Discount_Amount'] != 0 else 0)
		Prd["MPADiscount"] = str(plsgDict[key]['QI_MPA_Discount_Amount'])
		Prd["SellDiscount"] = str(plsgDict[key]['QI_Additional_Discount_Amount'])
		Prd["ProductLine"] = str(plsgDict[key]['ProductLine'])
		Prd["ProductLineDesc"] = str(plsgDict[key]['ProductLineDesc'])
		Prd["No_Discount_Allowed"] = str(plsgDict[key]['QI_No_Discount_Allowed'])
		Prd["OriginalItemNumber"] = '1'

		Prd.IsSelected = True
		tPrice += plsgDict[key]['ListPrice']
		tCost += plsgDict[key]['ExtendedCost']
		twtwCost += plsgDict[key]['QI_ExtendedWTWCost']
		tMPADiscount += plsgDict[key]['QI_MPA_Discount_Amount']
		tSellDiscount += plsgDict[key]['QI_Additional_Discount_Amount']
		tSellPrice += plsgDict[key]['ExtendedAmount']
		Prd.Calculate()
		Prd.ApplyProductChanges()
	PrdContainer_Parts.Calculate()
	ttPrice += tPrice
	ttCost += tCost
	cProduct.ApplyRules()
	return ttPrice, ttCost

RQUP_partList = []
ERP_partList = []
zoroPrice_partList = []
sysContainer = Product.GetContainerByName("TPS_PRDContainerSys")
if sysContainer:
	for sysProd in sysContainer.Rows:
		sysProd.Product.Attr('PRD_Error').AssignValue('')
		partsContainer = sysProd.Product.GetContainerByName("TPC_PartsContainer")
		tPrice, tCost = GeneratePLSGs(sysProd.Product, partsContainer)
		sysProd.Product.Attr('PRD_Price').AssignValue(str(tPrice))
		sysProd.Product.Attr('PRD_Cost').AssignValue(str(tCost))
		sysProd["ListPrice"] = str(tPrice)
		sysProd["Cost"] = str(tCost)
		sysProd.ApplyProductChanges()
		if zoroPrice_partList:
			sysProd.Product.Attr('PRD_Error').AssignValue(', '.join(zoroPrice_partList))
		if sysProd.Product.GetContainerByName("TPC_PRDContainer").Rows.Count > 0:
			sysProd.Product.Attr('Calculation Button Trigger').AssignValue('')
		else:
			sysProd.Product.Attr('Calculation Button Trigger').AssignValue('Yes')
	sysContainer.Calculate
else:
	sysContainer = Product.GetContainerByName("TPC_PRDContainer")
	if sysContainer:
		Product.Attr('PRD_Error').AssignValue('')
		partsContainer = Product.GetContainerByName("TPC_PartsContainer")
		GeneratePLSGs(Product, partsContainer)
		sysContainer.Calculate
		#if zoroPrice_partList:
		#	Product.Attr('PRD_Error').AssignValue(', '.join(zoroPrice_partList))
	if Product.GetContainerByName("TPC_PRDContainer").Rows.Count > 0:
		Product.Attr('Calculation Button Trigger').AssignValue('')
	else:
		Product.Attr('Calculation Button Trigger').AssignValue('Yes')
Product.ApplyRules()
if RQUP_partList:
	Product.Messages.Add('Upload file contains Unreleased Product ({}). User should answer the RQUP question RAFR1 as "Yes" in the functional review question tab.'.format(', '.join(set(RQUP_partList))))
if ERP_partList:
	Product.Messages.Add('Your Quote may have ERP texts in one or more-line items. Please check before submitting for approval.')
	#Product.Messages.Add('Upload file has ERP texts in Product ({}). Please check before submitting for approval'.format(', '.join(ERP_partList)))
#if zoroPrice_partList:
#	Product.Messages.Add('Upload file has zero price in Product ({}). Please check before submitting for approval'.format(', '.join(zoroPrice_partList)))