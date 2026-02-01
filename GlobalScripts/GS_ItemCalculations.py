from GS_CommonConfig import CL_CommonSettings as CS
from GS_GetPriceFromCPS import getPrice
from GS_Add_NP_Parts import getKENonPrcPart_standalone
import re
def getCFValue(quote , field):
	return quote.GetCustomField(field).Content
def getItemField(item , field):
	if field == 'ListPrice': return item.ListPrice
	if field == 'Cost': return item.Cost
	if field == 'ExtendedListPrice':return item.ExtendedListPrice
	if field == 'ExtendedCost': return item.ExtendedCost
	return item[field].Value
def setItemField(item , field , value):
	if field == 'cost':
		item.Cost = value
		return
	if field == 'discountPercent':
		item.DiscountPercent = value
		return
	if field == 'discountAmount':
		item.DiscountAmount = value
		return
	if field == 'extCost':
		item.ExtendedCost = value
		return
	item[field].Value = value
def getThresold(quote , pricePlan , ref , quoteType):
	mpa = quote.GetCustomField('AccountId').Content
	sf_agg_id = SqlHelper.GetFirst("SELECT Salesforce_Agreement_ID FROM MPA_ACCOUNT_MAPPING(nolock) WHERE Salesforce_ID='{}'".format(mpa))
	if sf_agg_id:
		res = SqlHelper.GetFirst("Select Order_Threshold_Parts,Order_Threshold_Systems from MPA_PRICE_PLAN_MAPPING(nolock) where Salesforce_Agreement_ID='{}' and Price_Plan_Name='{}'".format(sf_agg_id.Salesforce_Agreement_ID,pricePlan))
	else:
		res = SqlHelper.GetFirst("Select Order_Threshold_Parts,Order_Threshold_Systems from MPA_PRICE_PLAN_MAPPING(nolock) where (Honeywell_Ref='{}' and Honeywell_Ref != '') and Price_Plan_Name='{}'".format(ref , pricePlan))
	if res:
		thresold = res.Order_Threshold_Parts if quoteType == 'Parts and Spot' else res.Order_Threshold_Systems
		return float(thresold) if thresold else 0
	return 0
def getFromUSSGPricebook(quote,part):
	effectiveDate = quote.EffectiveDate.ToString('MM/dd/yyyy')
	table = "HPS_USSG_COST_DATA"
	bookingLOB = quote.GetCustomField('Booking LOB').Content
	if getCFValue(quote , "Quote Type") == "Projects":
		table = "HPS_USSC_COST_DATA"
	res = SqlHelper.GetFirst("Select Cost from {} where PartNumber = '{}' and Valid_from <= '{}' and Valid_to >= '{}'".format(table , part,effectiveDate,effectiveDate))
	if res is None and table == "HPS_USSC_COST_DATA" and bookingLOB in ['PAS','LSS']:
		res = SqlHelper.GetFirst("Select Cost from HPS_USSG_COST_DATA where PartNumber = '{}' and Valid_from <= '{}' and Valid_to >= '{}'".format(part, effectiveDate, effectiveDate))
	return res.Cost if res else 0
def getSumFromUSSGPricebook(quote,parts,qty):
	effectiveDate = quote.EffectiveDate.ToString('MM/dd/yyyy')
	table = "HPS_USSG_COST_DATA"
	bookingLOB = quote.GetCustomField('Booking LOB').Content
	if getCFValue(quote , "Quote Type") == "Projects":
		table = "HPS_USSC_COST_DATA"
	sumCost = 0
	for prd in parts:
		res = SqlHelper.GetFirst("Select Cost, PartNumber from {} where PartNumber = '{}' and Valid_from <= '{}' and Valid_to >= '{}'".format(table,prd,effectiveDate,effectiveDate))
		if res is None and table == "HPS_USSC_COST_DATA" and bookingLOB in ['PAS','LSS']:
			res = SqlHelper.GetFirst("Select Cost, PartNumber from HPS_USSG_COST_DATA where PartNumber = '{}' and Valid_from <= '{}' and Valid_to >= '{}'".format(prd,effectiveDate,effectiveDate))
		sumCost += (float(res.Cost) * float(qty.get(res.PartNumber,0)) if res else 0)
	return sumCost
def getWTWFactor(partNumber , isWriteIn):
	query = "SELECT WTW_FACTOR from HPS_PLSG_WTW_FACTOR wtw JOIN HPS_PRODUCTS_MASTER hpm on hpm.PLSG = wtw.PL_PLSG where hpm.PartNumber = '{}'".format(partNumber)
	if isWriteIn:
		query = "SELECT WTW_FACTOR from HPS_PLSG_WTW_FACTOR wtw JOIN WriteInProducts wrt on wrt.ProductLineSubGroup = wtw.PL_PLSG where wrt.Product = '{}'".format(partNumber)
	res = SqlHelper.GetFirst(query)
	return res.WTW_FACTOR if res else 0
def getGesWTWFactor(partNumber):
	query = "SELECT WTWMarkupFactorEstimated from Labor_GES_WTW_Markup_Factor where GES_Service_Material = '{}'".format(partNumber)
	res = SqlHelper.GetFirst(query)
	return res.WTWMarkupFactorEstimated if res else 0
def getTPFactor(quoteType , productType):
	res = SqlHelper.GetFirst("SELECT FACTOR from HPS_LABOR_FACTORS where QUOTE_TYPE='{}' and PRODUCT_TYPE='{}'".format(quoteType , productType))
	return res.FACTOR if res else 0
def getMpaDiscountPercent(quote,item , pricePlan , honeywellRef):
	if item.Training_QI_Gst_KP.Value != 0:
		return item.Training_QI_Gst_KP.Value
	if quote.GetCustomField("Quote Tab Booking LOB").Content=='PMC':
		return getItemField(item , "QI_MPA_Discount_Percent")
	if item.QI_MPA_Price.Value and item.ListPrice:
		discount = ((item.ListPrice - item.QI_MPA_Price.Value) / item.ListPrice) * 100
		return round(discount,2)
	result=None
	if quote.GetCustomField("Quote Type").Content in ['Projects','Parts and Spot']:
		if quote.GetCustomField("Quote Type").Content == "Projects":
			Type = "System Discount"
		else:
			Type = "Parts Discount"
		if quote.GetCustomField("Quote Tab Booking LOB").Content in ['LSS','PAS']:
			if quote.GetCustomField("MPA Honeywell Ref").Content:
				result = SqlHelper.GetFirst("SELECT Discount FROM MPA_DISCOUNTS(nolock) md JOIN HPS_PRODUCTS_MASTER(nolock) hpm on hpm.PLSG = md.Product_Line where hpm.PartNumber = '{}' and Price_Plan='{}' and Honeywell_Ref = '{}' and Type = '{}'".format(item.PartNumber , pricePlan , honeywellRef,Type))
				if not result:
					result = SqlHelper.GetFirst("SELECT Discount FROM MPA_DISCOUNTS(nolock) md JOIN HPS_PRODUCTS_MASTER(nolock) hpm on hpm.PLSG = md.Product_Line where hpm.PartNumber = '{}' and Price_Plan='{}' and Honeywell_Ref = '{}'".format(item.PartNumber , pricePlan , honeywellRef))
			elif quote.GetCustomField("MPA").Content:
				val = quote.GetCustomField('MPA').Content
				ctval = SqlHelper.GetFirst("SELECT Salesforce_Agreement_ID FROM MPA_PRICE_PLAN_MAPPING(nolock) WHERE Agreement_Name='"+str(val)+"'")
				result = SqlHelper.GetFirst("SELECT Discount FROM MPA_DISCOUNTS md JOIN HPS_PRODUCTS_MASTER(nolock) hpm on hpm.PLSG = md.Product_Line where hpm.PartNumber = '{}' and Price_Plan='{}' and Salesforce_Agreement_ID = '{}' and Type = '{}'".format(item.PartNumber, pricePlan , ctval.Salesforce_Agreement_ID,Type))
				if not result:
					result = SqlHelper.GetFirst("SELECT Discount FROM MPA_DISCOUNTS md JOIN HPS_PRODUCTS_MASTER(nolock) hpm on hpm.PLSG = md.Product_Line where hpm.PartNumber = '{}' and Price_Plan='{}' and Salesforce_Agreement_ID = '{}'".format(item.PartNumber, pricePlan , ctval.Salesforce_Agreement_ID))
			if result:
				return result.Discount
	return 0

def getMarketScheduleDiscount(quote,item,marketScheduleLookup,bookingLOB):
	discount = 0
	minMargin = 0
	effectiveDate = quote.EffectiveDate.ToString('MM/dd/yyyy')
	result = SqlHelper.GetFirst("select Discount,Minimum_Margin from MARKETDISCOUNT_SCHEDULE_PERCENTAGE(nolock) md join HPS_PRODUCTS_MASTER(nolock) hpm on hpm.PLSG = md.PL_PLSG where hpm.PartNumber = '{0}' and md.Market_Schedule = '{1}' and md.LOB = '{2}' and ISNULL(NULLIF(md.Valid_From,''),CONVERT(DATE,'{3}')) <= '{3}' and ISNULL(NULLIF(md.Valid_To,''),GETDATE()) >= '{3}' ".format(item.PartNumber,marketScheduleLookup,bookingLOB,effectiveDate))
	
	if result:
		discount,minMargin  =  result.Discount,result.Minimum_Margin
	return discount,minMargin
def checkMPAPricePlanValidty(quote):
	validcheckForMarketSchedule = False
	mpaValidity = quote.GetCustomField('MPA Validity').Content
	if mpaValidity:
		mpaValidityDate = UserPersonalizationHelper.CovertToDate(mpaValidity).Date
		if quote.DateModified.Date > mpaValidityDate:
			validcheckForMarketSchedule = True
	return validcheckForMarketSchedule
def applyMPA(quote , item):
	pricePlan = quote.GetCustomField('MPA Price Plan').Content
	honeywellRef = quote.GetCustomField('MPA Honeywell Ref').Content
	orderTotal = quote.GetCustomField('Total List Price').Content
	quoteType = quote.GetCustomField('Quote Type').Content
	sfid = quote.GetCustomField('AccountId').Content
	sfan = SqlHelper.GetFirst("SELECT Agreement_Name  FROM MPA_ACCOUNT_MAPPING WHERE Salesforce_ID  ='"+str(sfid)+"'")
	quote.GetCustomField('MPA').Content = sfan.Agreement_Name if sfan is not None else ''
	MPA = getCFValue(quote , "MPA")
	exchangeRate = quote.GetCustomField('Exchange Rate').Content
	bookingLOB = quote.GetCustomField('Booking LOB').Content
	marketScheduleLookup = quote.GetCustomField('Selected Discount Plan').Content
	mpaValidity = quote.GetCustomField('MPA Validity').Content
	PROS_Guidance = quote.GetCustomField('PROS Guidance Recommendation').Content
	validcheck = checkMPAPricePlanValidty(quote)
	scheduleDiscount,minMargin = getMarketScheduleDiscount(quote,item,marketScheduleLookup,bookingLOB)
	minMarginTargetPrice = (getItemField(item , "ExtendedCost") * 100) / (100 - float(minMargin))
	PROSDiscPerc = getItemField(item , "QI_Guidance_Discount_Percent")
	PROSDiscAmt = getItemField(item , "QI_PROS_Guidance_Recommended_Price")
	
	if quoteType == "Projects" and bookingLOB in ('LSS','PAS'):
		if item.Description == 'Write-In Standard Warranty System':
			setItemField(item , 'QI_Min_Margin_Target_Price' , 0)
		else:
			setItemField(item , 'QI_Min_Margin_Target_Price' , minMarginTargetPrice)
	thresold = getThresold(quote , pricePlan , honeywellRef , quoteType) * float(exchangeRate)
	quote.GetCustomField("MPA Threshold").Content = str(thresold or 0)
	if pricePlan and thresold <= float(orderTotal) and not validcheck:
		discount = getMpaDiscountPercent(quote,item , pricePlan ,honeywellRef)
		setItemField(item , 'QI_MPA_Discount_Percent' , discount)
		if discount > 0:
			discountAmount = getItemField(item , "ExtendedListPrice") * (discount / 100)
			setItemField(item , "QI_MPA_Discount_Amount" , discountAmount)
	elif (validcheck or mpaValidity == '') and quoteType == "Projects" and marketScheduleLookup != "List Price" and marketScheduleLookup != '':
		if quote.GetCustomField('Quote Tab Booking LOB').Content=='PMC':
			discount = getMpaDiscountPercent(quote,item , pricePlan ,honeywellRef)
			setItemField(item , 'QI_MPA_Discount_Percent' , discount)
			if discount > 0:
				discountAmount = getItemField(item , "ExtendedListPrice") * (discount / 100)
				setItemField(item , "QI_MPA_Discount_Amount" , discountAmount)
		elif quote.GetCustomField('Selected Discount Plan').Visible==True:
			setItemField(item , 'QI_MPA_Discount_Percent' , scheduleDiscount)
			if scheduleDiscount:
				discountAmount = getItemField(item , "ExtendedListPrice") * (float(scheduleDiscount) / 100)
				setItemField(item , "QI_MPA_Discount_Amount" , discountAmount)
		else:
			setItemField(item , 'QI_MPA_Discount_Percent' , 0)
			setItemField(item , "QI_MPA_Discount_Amount" , 0)
	else:
		if quote.GetCustomField('Quote Tab Booking LOB').Content:
			discount = getMpaDiscountPercent(quote,item , pricePlan ,honeywellRef)
			setItemField(item , 'QI_MPA_Discount_Percent' , discount)
			if discount > 0:
				discountAmount = getItemField(item , "ExtendedListPrice") * (discount / 100)
				setItemField(item , "QI_MPA_Discount_Amount" , discountAmount)
		else:
			setItemField(item , 'QI_MPA_Discount_Percent' , 0)
			setItemField(item , "QI_MPA_Discount_Amount" , 0)
def getFloat(Var):
	if Var or Var is not None:
		return float(Var)
	return 0
def laborCostWithoutConversion(quote,item):
	salesOrg = quote.GetCustomField("Sales Area").Content
	laborCost = ''
	currencyCode = ''
	query = "Select Cost_CurrentMonth_Year1,Cost_Currency_Code from HPS_LABOR_COST_DATA(NOLOCK) where Sales_Org = '{0}' and Part_Number = '{1}'".format(salesOrg,item.PartNumber)
	res = SqlHelper.GetFirst(query)
	if res is not None and res.Cost_CurrentMonth_Year1:
		laborCost = res.Cost_CurrentMonth_Year1
		currencyCode = res.Cost_Currency_Code
	else:
		laborCost = item.QI_Manual_labor_Regional_Cost.Value
	return laborCost,currencyCode
def laborCostWithCOnversion(quote,item):
	costWithConversion = ''
	quoteCurrency = quote.SelectedMarket.CurrencyCode
	laborCost,currencyCode = laborCostWithoutConversion(quote,item)
	query = SqlHelper.GetFirst("select Exchange_Rate from Currency_ExchangeRate_Mapping where From_Currency = '{}' and To_Currency = '{}'".format(currencyCode,quoteCurrency))
	if query is not None:
		costWithConversion = getFloat(laborCost) * getFloat(query.Exchange_Rate)
	else:
		costWithConversion = laborCost
	return getFloat(costWithConversion)
def getNonPriceCont(quote, item,nonpricecont, type):
	if not nonpricecont :
		res = SqlHelper.GetFirst("select Child_Part from MIGRATION_PART_MAPPING (NOLOCK) JOIN KE_Package_Part_Qty_Mapping (NOLOCK) ON Package_Model_Number = Child_Part and IS_Model_name = 'Y' WHERE Child_Part = '"+str(item.PartNumber)+"'")
	else :
		res = 1 if nonpricecont and nonpricecont.get(item.PartNumber, False)  == True else 0
	nonPricingParts = set()
	nonPricingQty = dict()
	is_KE = False
	ctrl_kePrd = ['MC-ZEHPR4','MC-ZEHPR9','MC-ZEHPS4','MC-ZEHPS9','MC-ZEXPR2','MC-ZEXPR7','MC-ZEXPS2','MC-ZEXPS7','MC-ZH2EXR','MC-ZH2EXS','MC-ZH4EHR','MC-ZH4EHS','MC-ZH4EXR','MC-ZH4EXS','MC-ZH6EHR','MC-ZH6EHS','MC-ZH6EXR','MC-ZH6EXS']
	if res:
		is_KE = True
		if type == 'C':
			if '.' in item.RolledUpQuoteItem:
				parentItem = quote.GetItemByQuoteItem(item.ParentRolledUpQuoteItem)
				p_parentItem = quote.GetItemByQuoteItem(parentItem.ParentRolledUpQuoteItem)
				if parentItem.ProductName in ('Experion Station Upgrade', 'Experion Server Upgrade', 'Experion Controller Upgrade'):
					nonPricingContainer = parentItem.SelectedAttributes.GetContainerByName("Non Pricing Parts")
					if nonPricingContainer:
						for row in nonPricingContainer.Rows:
							nonPricingParts.add(row["Part_Number"])
							nonPricingQty[row["Part_Number"]] = row['ItemQuantity']
				elif p_parentItem.ProductName == 'MSID_New':
					nonPricingContainer = p_parentItem.SelectedAttributes.GetContainerByName("Non Pricing Parts")
					if nonPricingContainer:
						for row in nonPricingContainer.Rows:
							if row["KE_Part_Number"] == item.PartNumber:
								nonPricingParts.add(row["Part_Number"])
								nonPricingQty[row["Part_Number"]] = row['ItemQuantity']
			else:
				nonPricingParts, nonPricingQty = getKENonPrcPart_standalone(item.PartNumber)
			if nonPricingParts and item.PartNumber in ctrl_kePrd:
				for prd in nonPricingParts:
					if prd not in ("EP-EHPMSP", "TC-SWCS30"):
						nonPricingQty[prd] = 0
	if type == 'C':
		return is_KE, nonPricingParts, nonPricingQty
	else:
		return is_KE
def getRegionalCost(quote, item , quoteType , exchangeRate, nonpricecont, tagParserQuote):
	lob = quote.GetCustomField('Booking LOB').Content
	first_part = item.RolledUpQuoteItem.split('.')[0]
	is_KE, nonPricingParts, nonPricingQty = getNonPriceCont(quote, item, nonpricecont, 'C')
	if CS.setdefaultvalue.get("rolled_up",'')!='' and item.PartNumber !='CYBER' and ((len(item.RolledUpQuoteItem)>=2 and str(item.RolledUpQuoteItem)[:len(first_part) + 1] != CS.setdefaultvalue.get("rolled_up",'')) or len(item.RolledUpQuoteItem)<2):
		CS.setdefaultvalue["rolled_up"]=''
	if CS.setdefaultvalue.get("LaborConfigParentGuid",'')!='' and item.PartNumber !='HCI_Labor_config' and ((len(item.RolledUpQuoteItem)>=2 and str(item.RolledUpQuoteItem)[:2] != CS.setdefaultvalue.get("LaborConfigParentGuid",'')) or len(item.RolledUpQuoteItem)<2):
		CS.setdefaultvalue["LaborConfigParentGuid"]=''
	if item.ProductTypeName.lower() == "honeywell labor" and quoteType != "Projects" and  lob != 'HCP' and not is_KE and CS.setdefaultvalue.get("rolled_up",'')=='':
		factor = getTPFactor(quoteType , item.ProductTypeName)
		return item.ListPrice * factor
	elif is_KE:
		licenceQty, migEhpmAdded = getKeLicQty(quote, item, is_KE)
		nonPricingParts , nonPricingQty = getNonPrcDtls(quote, item, licenceQty, migEhpmAdded, nonPricingParts, nonPricingQty)
		if licenceQty:
			nonPricingQty["EP-EHPMSP"] = 0
		nonPricingCost = getSumFromUSSGPricebook(quote, nonPricingParts , nonPricingQty) * exchangeRate
		if licenceQty and "EP-EHPMSP" in nonPricingParts:
			cost = (getFromUSSGPricebook(quote, "EP-EHPMSP") * exchangeRate * licenceQty)
			nonPricingCost = ((nonPricingCost*item.Quantity) + float(cost))
		checkECU = "Select Parent_Model_Name from KE_PACKAGE_PART_QTY_MAPPING (NOLOCK) where Parent_Model_Name='Experion Controller Upgrade' and Package_Model_Number='{}'".format(item.PartNumber)
		res=SqlHelper.GetList(checkECU)
		if len(res) > 0:
			basePrice = getFromUSSGPricebook(quote,item.PartNumber) * exchangeRate
			if licenceQty and "EP-EHPMSP" in nonPricingParts:
				basePrice = basePrice * item.Quantity
				extCost = basePrice + nonPricingCost
				unitCost = extCost/item.Quantity
			else:
				unitCost = basePrice + nonPricingCost
			return unitCost
		return nonPricingCost
	elif item.ProductTypeName.lower() == "honeywell labor" and (quoteType == "Projects" or (lob == 'HCP') or (CS.setdefaultvalue.get("rolled_up",'')!='' and len(item.RolledUpQuoteItem)>=2 and str(item.RolledUpQuoteItem)[:len(first_part) + 1] == CS.setdefaultvalue.get("rolled_up",''))):
		if item.QI_GESRegionalCost.Value not in ('',0):
			return item.QI_GESRegionalCost.Value
		return laborCostWithCOnversion(quote,item)
	else:
		return getFromUSSGPricebook(quote,item.PartNumber) * exchangeRate
def getStdWarrantyCost(quote): 
	warrantyCost = 0
	bookingCountry = quote.GetCustomField('Booking Country').Content
	getWarranty = SqlHelper.GetFirst("Select Warranty_Percentage From Standard_Warranty_Percentages Where Country = '{}'".format(bookingCountry))
	if getWarranty:
		sellPrice = float(quote.GetCustomField('Total Sell Price').Content.replace(',',''))
		warrantyCost = (sellPrice * getWarranty.Warranty_Percentage) / 100
	return warrantyCost
def getWTWCost(item , cost , quoteType,wtwcostfactor_dict,nonpricecont, quote= None):
	lob = quote.GetCustomField('Booking LOB').Content
	first_part = item.RolledUpQuoteItem.split('.')[0]
	is_KE, nonPricingParts, nonPricingQty = getNonPriceCont(quote, item, nonpricecont, 'C')
	licenceQty, migEhpmAdded = getKeLicQty(quote, item, is_KE)
	nonPricingParts , nonPricingQty = getNonPrcDtls(quote, item, licenceQty, migEhpmAdded, nonPricingParts, nonPricingQty)
	if item.ProductTypeName.lower() == "honeywell labor" and quoteType == "Parts and Spot" and not is_KE and (CS.setdefaultvalue.get("rolled_up",'')=='' and CS.setdefaultvalue.get("LaborConfigParentGuid",'')== ''):
		return cost
	elif is_KE:
		total=0
		exchangeRate    = float(getCFValue(quote , "Exchange Rate") if getCFValue(quote , "Exchange Rate") else 1)
		for part in nonPricingParts:
			wtwFactor=getWTWFactor(part,part == "Write-In")
			nonPricingCost = 0
			if licenceQty and "EP-EHPMSP" in nonPricingParts and part == "EP-EHPMSP":
				regionalCost = (getFromUSSGPricebook(quote, "EP-EHPMSP") * exchangeRate * licenceQty)
				nonPricingCost = float(regionalCost)/(float(1)+float(wtwFactor))
			elif licenceQty and "TC-SWCS30" in nonPricingParts and part == "TC-SWCS30":
				regionalCost=getFromUSSGPricebook(quote, "TC-SWCS30") * exchangeRate *item.Quantity
				nonPricingCost = float(regionalCost)/(float(1)+float(wtwFactor))
			else:
				regionalCost=getFromUSSGPricebook(quote,part) * exchangeRate
				nonPricingCost = (float(regionalCost) * float(nonPricingQty.get(part,0)))/(float(1)+float(wtwFactor))
			total+=nonPricingCost
		checkECU = "Select Parent_Model_Name from KE_PACKAGE_PART_QTY_MAPPING where Parent_Model_Name='Experion Controller Upgrade' and Package_Model_Number='{}'".format(item.PartNumber)
		res=SqlHelper.GetList(checkECU)
		if len(res) > 0:
			basecost = getFromUSSGPricebook(quote,item.PartNumber) * exchangeRate
			wtwFactor =wtwcostfactor_dict.get(item.QI_PLSG.Value,0)
			if licenceQty and "EP-EHPMSP" in nonPricingParts:
				basecost = basecost * item.Quantity
				total+=(float(basecost))/(float(1)+float(wtwFactor))
				total = total/item.Quantity
			else:
				total+=(float(basecost))/(float(1)+float(wtwFactor))

		return total
	elif item.ProductTypeName.lower() == "honeywell labor" and (quoteType == "Projects" or (CS.setdefaultvalue.get("rolled_up",'')!='' and len(item.RolledUpQuoteItem)>2 and str(item.RolledUpQuoteItem)[:len(first_part) + 1] == CS.setdefaultvalue.get("rolled_up",'')) or (lob != 'HCP')):
		if item.QI_FoWTWCost.Value not in ('',0):
			return item.QI_FoWTWCost.Value
		elif (item.PartNumber.startswith("SVC_GES") or item.PartNumber.startswith("HPS_GES")) and item.QI_GESRegionalCost.Value not in ('',0):
			return cost / (1 + float(getGesWTWFactor(item.PartNumber)))
	return cost / (1 + float(wtwcostfactor_dict.get(item.QI_PLSG.Value,0))) if cost else 0.0
def calculateCosts(quote , bookingLob, quoteType, item, wtwcostfactor_dict, nonpricecont,  tagParserQuote):
	if item.ProductName == 'TPC_Product':
		retrun
	exchangeRate    = float(getCFValue(quote , "Exchange Rate") if getCFValue(quote , "Exchange Rate") else 1)
	oppType         = getCFValue(quote , "Opportunity Type")
	cost            = item.Cost
	listPrice       = item.ExtendedListPrice
	wtwCost         = 0
	if item.PartNumber != "Write-In Standard Warranty" and item.PartNumber != "Write-In Tariff" and item.ProductName not in ['Write-In Entitlement-Hardening Services','Write-In Entitlement-Hardening Cyber Care','Write-In Entitlement-Cyber App Control','Write-In Entitlement-Cyber App Control Care','WriteIn']:
		if (bookingLob == "PMC" and quoteType == "Parts and Spot"):
			if item["QI_Adder_LP"].Value == 'Adder':
				setItemField(item , 'cost' , cost + item.MrcCost)
				setItemField(item , 'QI_UnitWTWCost' , cost + item.MrcCost)
			elif item["QI_Adder_LP"].Value == 'Total LP':
				setItemField(item , 'cost' , item.MrcCost)
				setItemField(item , 'QI_UnitWTWCost' , item.MrcCost)
			else:
				setItemField(item , 'QI_UnitWTWCost' , cost)
		else:
			cost = getRegionalCost(quote, item , quoteType , exchangeRate,nonpricecont, tagParserQuote)
			setItemField(item , 'cost' , cost)
	if item.PartNumber in ["Write-In Standard Warranty"]:
		cost = getStdWarrantyCost(quote)
		wtwCost = getWTWCost(item , cost , quoteType,wtwcostfactor_dict,nonpricecont,quote)
		setItemField(item , 'cost' , cost)
		setItemField(item , 'QI_UnitWTWCost' , wtwCost)
		setItemField(item , 'QI_ExtendedWTWCost' , wtwCost * item.Quantity)
		setItemField(item , 'QI_ExtendedWTWCost_1' , wtwCost * item.Quantity)
		setItemField(item , 'QI_RegionalMargin' , (item.ExtendedAmount - (cost * item.Quantity)))
		setItemField(item , 'QI_WTWMargin' , (item.ExtendedListPrice - (wtwCost * item.Quantity)))
		if item.ExtendedAmount != 0:
			setItemField(item , 'QI_RegionalMarginPercent' , (item.ExtendedAmount - (cost * item.Quantity))/item.ExtendedAmount * 100)
			setItemField(item , 'QI_WTWMarginPercent' , (item.ExtendedListPrice - (wtwCost * item.Quantity))/item.ExtendedListPrice * 100)
	if bookingLob != "PMC" and not (item.ProductName== 'WriteIn' and item.ProductName == "HCI Labor Config" and bookingLob == "HCP" and item.QI_PLSG.Value == '7243-7992' and str(item.ParentRolledUpQuoteItem)!=''):
		wtwCost = getWTWCost(item , item.Cost , quoteType,wtwcostfactor_dict,nonpricecont,quote)
		setItemField(item , 'QI_UnitWTWCost' , wtwCost)
		setItemField(item , 'QI_ExtendedWTWCost' , wtwCost * item.Quantity)
	#CXCPQ-34929- Added this condition to make labor WTW cost appear at quote level for PMC LOB
	if bookingLob == "PMC" and quoteType == "Projects":
		wtwCost = getWTWCost(item , item.Cost , quoteType,wtwcostfactor_dict,nonpricecont,quote)
		setItemField(item , 'QI_UnitWTWCost' , wtwCost)
		setItemField(item , 'QI_ExtendedWTWCost' , wtwCost * item.Quantity)
		setItemField(item , 'QI_ExtendedWTWCost_1' , wtwCost * item.Quantity)
	if bookingLob == "HCP" and item.ProductName == "HCI Labor Config":
		wtwCost = float(item["QI_UnitWTWCost"].Value or 0)
		setItemField(item, "QI_UnitWTWCost", wtwCost)
		setItemField(item, "QI_ExtendedWTWCost", wtwCost * item.Quantity)
	if bookingLob == "CCC":
		# wtwCost = item.MrcCost*exchangeRate
		wtwCost = item.MrcCost
		#setItemField(item , 'cost' , wtwCost)
		setItemField(item , 'QI_UnitWTWCost' , wtwCost)
		setItemField(item , 'QI_ExtendedWTWCost' , wtwCost * item.Quantity)
		setItemField(item , 'QI_ExtendedWTWCost_1' , wtwCost * item.Quantity)
	#CCEECOMMBR-6136
	if item.QI_PLSG.Value in ('7061-Y963', '7061-Y964', '7061-Y992'):
		listPrice = item.ListPrice
		cost = listPrice * float(0.55)
		setItemField(item , 'cost' , cost)
		setItemField(item , 'QI_UnitWTWCost' , cost)
		setItemField(item , 'QI_ExtendedWTWCost' , cost * item.Quantity)
		setItemField(item , 'QI_ExtendedWTWCost_1' , cost * item.Quantity)
		setItemField(item , 'QI_WTWMargin' , (item.ExtendedListPrice - (cost * item.Quantity)))
		if item.ExtendedListPrice != 0:
			setItemField(item , 'QI_WTWMarginPercent' , (item.ExtendedListPrice - (cost * item.Quantity))/item.ExtendedListPrice * 100)
		setItemField(item , 'QI_No_Discount_Allowed' , '1')
		setItemField(item , 'QI_RegionalMargin' , (item.ExtendedAmount - item.QI_TOTAL_EXTENDED_COST.Value))
		if item.ExtendedAmount != 0:
			setItemField(item , 'QI_RegionalMarginPercent' , (item.ExtendedAmount - item.QI_TOTAL_EXTENDED_COST.Value)/item.ExtendedAmount * 100)
	#CCEECOMMBR-CXCPQ-83757
	if item.PartNumber in ('SM-MLF-FSC2SM01','SM-MLF-FSC2SM02','SM-MLF-FSC2SM03','SM-MLF-FSC2SM04','SM-MLF-FSC2SM05','SM-MLF-FSC2SM06'):
		lp=item.ListPrice
		cost = (lp*50)/100
		setItemField(item , 'cost' , cost)
		setItemField(item , 'QI_UnitWTWCost' , cost)
		setItemField(item , 'QI_ExtendedWTWCost' , cost * item.Quantity)
		setItemField(item , 'QI_ExtendedWTWCost_1' , cost * item.Quantity)
		setItemField(item , 'QI_WTWMargin' , lp)
	#CCEECOMMBR-6136  
	if item.QI_PLSG.Value == '7061-7239' and item.PartNumber != 'Write-In Training Automation College':
		listPrice = item.ListPrice
		cost = listPrice * float(0.70)
		wtwCost = getWTWCost(item , cost , quoteType,wtwcostfactor_dict,nonpricecont,quote)
		setItemField(item , 'cost' , cost)
		setItemField(item , 'QI_UnitWTWCost' ,wtwCost)
		setItemField(item , 'QI_ExtendedWTWCost' , wtwCost * item.Quantity)
		setItemField(item , 'QI_WTWMargin' , (item.ExtendedListPrice - (wtwCost * item.Quantity)))
		setItemField(item , 'QI_WTWMarginPercent' , (item.ExtendedListPrice - (wtwCost * item.Quantity))/item.ExtendedListPrice * 100)
		setItemField(item , 'QI_RegionalMargin' , (item.ExtendedAmount - item.QI_TOTAL_EXTENDED_COST.Value))
		setItemField(item , 'QI_RegionalMarginPercent' , (item.ExtendedAmount - item.QI_TOTAL_EXTENDED_COST.Value)/item.ExtendedAmount * 100)
	if item.PartNumber == 'Write-In InterCo Margin':
		item.ListPrice = 0
		setItemField(item,'QI_UnitWTWCost',0)
		setItemField(item,'QI_ExtendedWTWCost',0)
def CalculateListPrice(quote , item,nonpricecont, tagParserQuote, Session=dict()):
	quoteType = getCFValue(quote , "Quote Type")
	first_part = item.RolledUpQuoteItem.split('.')[0]
	# MPA= getCFValue(quote , "MPA")
	if quoteType == "Projects" and item.PartNumber in ("PRJT", "Migration", "R2Q-PRJT", "IAA", "IAA -Project", "Trace Software", "Cyber Products"):
		process_project_items(item.AsMainItem)
		WTWCostUpdate(quote)
	if item.PartNumber == 'CYBER':
		WTWCostUpdate(quote)
	if item.ProductName == "Winest Labor Import":
		WTWCostUpdate(quote)
	if item.ProductTypeName.lower() == "honeywell labor" and (quoteType == "Projects" or (CS.setdefaultvalue.get("rolled_up",'')!='' and len(item.RolledUpQuoteItem)>2 and str(item.RolledUpQuoteItem)[:len(first_part) + 1] == CS.setdefaultvalue.get("rolled_up",''))):
		if item.QI_LaorPartsListPrice.Value not in ('',0):
			item.ListPrice = item.QI_LaorPartsListPrice.Value
		return
	salesOrg = getCFValue(quote , "Sales Area")
	entitlement = getCFValue(quote , "Entitlement")
	is_KE = getNonPriceCont(quote, item,nonpricecont,  '')
	licenceQty, migEhpmAdded = getKeLicQty(quote, item, is_KE)
	licensePrice = 0
	licensePriceFound = False
	flag = True
	if entitlement:
		entitlementType = 'SF' if 'flex' in entitlement.lower() else 'SP'
		currencyCode = quote.SelectedMarket.CurrencyCode
		effectiveDate = quote.EffectiveDate.ToString('MM/dd/yyyy')
		if licenceQty:
			query = (
			"select Amount from HPS_SESP_DATA(NOLOCK) where PartNumber = '{0}' "
			"and Price_Type = '{1}' and Sales_Org = '{2}' and Currency = '{3}' "
			"and Valid_from <= '{4}' and Valid_to >= '{4}' and coalesce(Deletion_Indicator,'') <> 'X'"
			).format("EP-EHPMSP", entitlementType, salesOrg, currencyCode, effectiveDate)
			rs = SqlHelper.GetFirst(query)
			if rs:
				licensePriceFound = True
				licensePrice = rs.Amount
		query = ("select Amount from HPS_SESP_DATA(nolock) where PartNumber = '{0}' and Price_Type = '{1}' and Sales_Org = '{2}' and Currency = '{3}' and Valid_from <= '{4}' and Valid_to >= '{4}' and coalesce(Deletion_Indicator,'') <> 'X'"
		).format(item.PartNumber, entitlementType, salesOrg, currencyCode, effectiveDate)
		rs = SqlHelper.GetFirst(query)
		if rs:
			item.ListPrice = rs.Amount
			flag = False
	if is_KE:
		if flag:
			priceDict = getPrice(quote, {}, [item.PartNumber, "EP-EHPMSP"], tagParserQuote, Session)
			if not licensePriceFound:
				licensePriceFound = True
				licensePrice = float(priceDict.get("EP-EHPMSP", 0))
			item.ListPrice = float(priceDict.get(item.PartNumber, 0))
		if not flag and not licensePriceFound:
			priceDict = getPrice(quote, {}, ["EP-EHPMSP"], tagParserQuote, Session)
			licensePrice = float(priceDict.get("EP-EHPMSP", 0))
		if licenceQty:
			extLP = ((item.ListPrice * item.Quantity) + (licensePrice * licenceQty))
			item.ListPrice = extLP / item.Quantity
def calculateItemDiscountFromAmount(quote , item):
	mpaDiscount = getItemField(item , "QI_MPA_Discount_Amount")
	additionalDiscount = getItemField(item , "QI_Additional_Discount_Amount")
	totalDiscount = mpaDiscount + additionalDiscount
	if totalDiscount > item.ExtendedListPrice:
		additionalDiscountpercent = getItemField(item , "QI_Additional_Discount_Percent")
		if quote.GetCustomField("Booking LOB").Content == "PMC":
			additionalDiscount = (item.ExtendedListPrice * additionalDiscountpercent) / 100
		else:
			additionalDiscount = ((item.ExtendedListPrice - mpaDiscount) * additionalDiscountpercent) / 100
		setItemField(item , "QI_Additional_Discount_Amount" , additionalDiscount)
		quote.Messages.Add('Discount limit exceeded!!')
		return
	if item.ExtendedListPrice:
		if quote.GetCustomField("Booking LOB").Content == "PMC":
			setItemField(item , "QI_Additional_Discount_Percent" , (100 * additionalDiscount) / item.ExtendedListPrice)
		else:
			setItemField(item , "QI_Additional_Discount_Percent" , (100 * additionalDiscount) / (item.ExtendedListPrice-mpaDiscount))
		item.DiscountAmount = totalDiscount
		item.DiscountPercent = (100 * item.DiscountAmount) / item.ExtendedListPrice
	else:
		setItemField(item , "QI_Additional_Discount_Amount" , 0)
def calculateItemDiscountFromPercent(quote, item):
	mpaDiscountPercent = getItemField(item, "QI_MPA_Discount_Percent")
	if getCFValue(quote, "Booking LOB") == "PMC" and getCFValue(quote, "Quote Type") == "Parts and Spot":
		childItem = item.AsMainItem
		if childItem and childItem.VCItemPricingPayload.Conditions:
			for condition in childItem.VCItemPricingPayload.Conditions:
				if str(condition.ConditionType) in ('ZD08', 'ZD00'):
					conditionRate = re.sub('-', '', str(condition.ConditionRate))
					enableMPA = getCFValue(quote, 'Enable MPA') == 'true'
					if enableMPA:
 						childItem.QI_MPA_Discount_Percent.Value = conditionRate
					else:
 						childItem.QI_MPA_Discount_Percent.Value = 0.00
					break
 			mpaDiscountPercent=childItem.QI_MPA_Discount_Percent.Value
	mpaDiscount = (item.ExtendedListPrice * float(mpaDiscountPercent)) / 100
	additionalDiscountpercent = getItemField(item , "QI_Additional_Discount_Percent")
	additionalDiscount = ((item.ExtendedListPrice - mpaDiscount) * additionalDiscountpercent) / 100
	totalDiscount = mpaDiscount + additionalDiscount
	if totalDiscount > item.ExtendedListPrice:
		additionalDiscount = getItemField(item , "QI_Additional_Discount_Amount")
		setItemField(item , "QI_Additional_Discount_Percent" , (100 * additionalDiscount) / (item.ExtendedListPrice-mpaDiscount))
		quote.Messages.Add('Discount limit exceeded!!')
		return
	setItemField(item , "QI_Additional_Discount_Amount" , additionalDiscount)
	setItemField(item , "QI_MPA_Discount_Amount" , mpaDiscount)
	item.DiscountAmount = totalDiscount
	if item.ExtendedListPrice:
		item.DiscountPercent = (100 * item.DiscountAmount) / item.ExtendedListPrice
def calculateExpediteFee(quote, item):
	if item['QI_Customer_Requested_Date'].Value !='' and item['QI_LT_Delivery_Date'].Value != '':
		isValid = DateTime.Compare(item['QI_LT_Delivery_Date'].Value, item['QI_Customer_Requested_Date'].Value) > 0
	else:
		isValid = False
	if item['QI_Expedite_Reason'].Value and isValid and getCFValue(quote,"Expedite Fee Waiver") != 'True' and not(getCFValue(quote,"Expedite Fee Waiver Reason")):
		exchangeRate    = getCFValue(quote,'Exchange Rate') if getCFValue(quote,'Exchange Rate').strip() !='' else 1.0
		expedite_fee    = 0
		unitSellPrice   = float(item.NetPrice)/ float(exchangeRate)
		value           = 0.1 * unitSellPrice
		if value < 500:
			expedite_fee= 500* float(exchangeRate) * item.Quantity
			item['QI_Expedite_Fees'].Value = round(expedite_fee,2)
		else:
			expedite_fee = value * item.Quantity
			item['QI_Expedite_Fees'].Value = round(expedite_fee,2)
	else:
		item['QI_Expedite_Fees'].Value = 0
def calculatePublishedLeadTime(quote, item):
	publishedLeadTime = UserPersonalizationHelper.ConvertToNumber(getCFValue(quote,'Published Lead Time')) if getCFValue(quote,'Published Lead Time') else 0
	itemLeadTime = item['QI_LeadTime'].Value if item['QI_LeadTime'].Value else 0
	if itemLeadTime  <= publishedLeadTime:
		pass
	else:
		publishedLeadTime = itemLeadTime
		quote.GetCustomField('Published Lead Time').Content = str(int(publishedLeadTime))
def calculateLTDevileryDate(quote, item):
    leadTime =item['QI_LeadTime'].Value
    quoteRepriceDate = getCFValue(quote , 'Quote Reprice Date')
    if quoteRepriceDate != '':
        convertedQuoteRepriceDate =UserPersonalizationHelper.CovertToDate(quoteRepriceDate)
        deliveryDate = convertedQuoteRepriceDate.AddDays(leadTime)
        item['QI_LT_Delivery_Date'].Value = deliveryDate
def assignLeadTime(quote, item):
	salesArea = getCFValue(quote,'Sales Area')
	transitTime,serviceDays = 0, 0
	query = SqlHelper.GetFirst("Select SERVICE_DAYS from LEAD_TIME where SALES_ORG = '{0}' and MATERIAL = '{1}'".format(salesArea, item.PartNumber))
	if query and query.SERVICE_DAYS:
		serviceDays = query.SERVICE_DAYS
		query = SqlHelper.GetFirst("Select TRANSIT_TIME from TRANSIT_TIME where SALES_ORG = '{0}'".format(salesArea))
		if query and query.TRANSIT_TIME:
			transitTime = query.TRANSIT_TIME
		else:
			transitTime = 0
		totalDays = int(serviceDays) + int(transitTime)
		item['QI_LeadTime'].Value = totalDays
	else:
		item['QI_LeadTime'].Value = 0

def getKeLicQty(quote, item, is_KE):
	licenceQty = 0
	migEhpmAdded = 0
	reqPart = item.PartNumber
	if reqPart in ('MC-ZH6EHR', 'MC-ZH6EHS', 'MC-ZH4EXR', 'MC-ZH4EXS'):
		if '.' in item.RolledUpQuoteItem and is_KE:
			if '.' in item.ParentRolledUpQuoteItem:
				parentItem = quote.GetItemByQuoteItem(item.ParentRolledUpQuoteItem)
				p_parentItem = quote.GetItemByQuoteItem(parentItem.ParentRolledUpQuoteItem)
				parPrdNm = parentItem.ProductName
				if parPrdNm == 'EHPM/EHPMX/ C300PM':
					migEhpmAdded = 1
					cnfgCont = parentItem.SelectedAttributes.GetContainerByName('xPM_Migration_Config_Cont')
					mig_new = parentItem.SelectedAttributes.GetContainerByName('xPM_Migration_Config_Cont')
					mig_old = p_parentItem.SelectedAttributes.GetContainerByName('xPM_Migration_Config_Cont')
					cnfgCont = cnfgCont if mig_new else mig_old
					if cnfgCont:
						for i in cnfgCont.Rows:
							if reqPart in ('MC-ZH6EHR') and i['xPM_Migration_Scenario'] == 'Redundant EHPM to C300PM':
								licenceQty += int(i['xPM_Controller_need_Experion_peer_to_peer_connectivity']) if i['xPM_Controller_need_Experion_peer_to_peer_connectivity'] else 0
							elif reqPart in ('MC-ZH6EHS') and i['xPM_Migration_Scenario'] == 'Non-redundant EHPM to C300PM':
								licenceQty += int(i['xPM_Controller_need_Experion_peer_to_peer_connectivity']) if i['xPM_Controller_need_Experion_peer_to_peer_connectivity'] else 0
							elif reqPart in ('MC-ZH4EXR') and i['xPM_Migration_Scenario'] == 'Redundant EHPM to EHPMX':
								licenceQty += int(i['xPM_EHPMX_need_Experion_peer_to_peer_connectivity']) if i['xPM_EHPMX_need_Experion_peer_to_peer_connectivity'] else 0
							elif reqPart in ('MC-ZH4EXS') and i['xPM_Migration_Scenario'] == 'Non-redundant EHPM to EHPMX':
								licenceQty += int(i['xPM_EHPMX_need_Experion_peer_to_peer_connectivity']) if i['xPM_EHPMX_need_Experion_peer_to_peer_connectivity'] else 0
			else:
				parentItem = quote.GetItemByQuoteItem(item.ParentRolledUpQuoteItem)
				for attr in filter(lambda x: x.Name == "KE_Controller P2P Connectivity Licenses", parentItem.SelectedAttributes):
					for val in attr.Values:
						licenceQty = float(val.Display)
						break
	return licenceQty, migEhpmAdded

def getNonPrcDtls(quote, item, licenceQty, migEhpmAdded, nonPricingParts, nonPricingQty):
	hw_sel = ''
	if '.' in item.RolledUpQuoteItem:
		if '.' in item.ParentRolledUpQuoteItem:
			if item.PartNumber in ('TP-ZWDTA2'):
				parentItem = quote.GetItemByQuoteItem(item.ParentRolledUpQuoteItem)
				parPrdNm = parentItem.ProductName
				if parPrdNm == 'TPS to Experion':
					mig_new = parentItem.SelectedAttributes.GetContainerByName('TPS_EX_Station_Conversion_EST')
					if mig_new:
						for i in mig_new.Rows:
							if i['TPS_EX_Station_Conversion_Type'] == 'US_AM to ES-T' and int(i['TPS_EX_Quantity']) > 0:
								hw_sel = i['TPS_EX_Hardware']
	if hw_sel != '':
		futRelPrd_qry = "Select Package_Model_Number, Child_Products, Quantity from KE_PACKAGE_PART_QTY_MAPPING where Attribute_Name = 'KE_Hardware_Selection' and Attribute_Value_Code = '{}' and Package_Model_Number='{}'".format(hw_sel, item.PartNumber)
		futRelPrd=SqlHelper.GetList(futRelPrd_qry)
		for parts in futRelPrd:
			if parts.Child_Products not in nonPricingParts:
				nonPricingParts.add(parts.Child_Products)
				nonPricingQty[parts.Child_Products] = parts.Quantity
	if licenceQty>0 and migEhpmAdded == 1 and "EP-EHPMSP" not in nonPricingParts:
		nonPricingParts.add("EP-EHPMSP")
		nonPricingQty["EP-EHPMSP"] = 1
	elif licenceQty==0 and migEhpmAdded == 1 and "EP-EHPMSP" in nonPricingParts and item.PartNumber in ('MC-ZH6EHR', 'MC-ZH6EHS', 'MC-ZH4EXR', 'MC-ZH4EXS'):
		nonPricingParts.remove("EP-EHPMSP")
		nonPricingQty["EP-EHPMSP"] = 0
	return nonPricingParts, nonPricingQty

def WTWCostUpdate(quote):
	wtw_qt = quote.QuoteTables["WTW_Prices_Calculation"]
	for quoteitem in quote.Items:
		for row in wtw_qt.Rows:
			if quoteitem.QuoteItemGuid == row["GUID"]:
				quoteitem.QI_GESRegionalCost.Value = row["QI_GESRegionalCost"]
				quoteitem.QI_LaorPartsListPrice.Value = row["QI_LaorPartsListPrice"]
				quoteitem.QI_FoWTWCost.Value = row["QI_FoWTWCost"]
				break
		
def populate_years(item, year):
	item["QI_Year"].Value = year
	item["QI_Year_Visibility"].Value = "0"
	for citem in item.Children:
		citem["QI_Year"].Value = year
		citem["QI_Year_Visibility"].Value = "0"

def process_project_items(item):
	yearVal = next((sAtt.Values[0].ValueCode for sAtt in item.SelectedAttributes if sAtt.Name == "LCM_Multiyear_Selection"), '')
	populate_years(item, yearVal)