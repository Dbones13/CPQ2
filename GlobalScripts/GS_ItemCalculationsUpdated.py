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
     
def getThreshold(quote , pricePlan , ref , quoteType):
    mpa = quote.GetCustomField('AccountId').Content
    sf_agg_id = SqlHelper.GetFirst("SELECT Salesforce_Agreement_ID FROM MPA_ACCOUNT_MAPPING(nolock) WHERE Salesforce_ID='{}' AND getdate() between Agreement_Start_Date and Agreement_End_Date".format(mpa))
    if sf_agg_id:
        res = SqlHelper.GetFirst("Select Order_Threshold_Parts,Order_Threshold_Systems from MPA_PRICE_PLAN_MAPPING(nolock) where Salesforce_Agreement_ID='{}' and Price_Plan_Name='{}'".format(sf_agg_id.Salesforce_Agreement_ID,pricePlan))
    else:
        res = SqlHelper.GetFirst("Select Order_Threshold_Parts,Order_Threshold_Systems from MPA_PRICE_PLAN_MAPPING(nolock) where (Honeywell_Ref='{}' and Honeywell_Ref != '') and Price_Plan_Name='{}'".format(ref , pricePlan))
    if res:
        threshold = res.Order_Threshold_Parts if quoteType == 'Parts and Spot' else res.Order_Threshold_Systems
        return float(threshold) if threshold else 0
    return 0

def checkMPAPricePlanValidty(quote):
    validcheckForMarketSchedule = False
    mpaValidity = quote.GetCustomField('MPA Validity').Content
    if mpaValidity:
        mpaValidityDate = UserPersonalizationHelper.CovertToDate(mpaValidity).Date
        if quote.DateModified.Date > mpaValidityDate:
            validcheckForMarketSchedule = True
	return validcheckForMarketSchedule

def getMpaDiscountPercent(quote, quoteItem, pricePlan , honeywellRef):
    if quote.GetCustomField("Quote Tab Booking LOB").Content=='PMC':#MD-PMC MPA bypass CXCPQ-75113
        return getItemField(quoteItem , "QI_MPA_Discount_Percent")#MD-PMC MPA bypass CXCPQ-75113
    if quoteItem.QI_MPA_Price.Value and quoteItem.ListPrice:
        discount = ((quoteItem.ListPrice - quoteItem.QI_MPA_Price.Value) / quoteItem.ListPrice) * 100
        return round(discount,2)
    result=None
    if quote.GetCustomField("Quote Type").Content in ['Projects','Parts and Spot']:
        if quote.GetCustomField("Quote Tab Booking LOB").Content in ['LSS','PAS','HCP']:
            if quote.GetCustomField("MPA Honeywell Ref").Content:
                if quoteItem.ProductTypeName != "Write-In":
                    if quoteItem.ProductName != "TPC_Product":
                        result = SqlHelper.GetFirst("SELECT Discount FROM MPA_DISCOUNTS(nolock) md JOIN HPS_PRODUCTS_MASTER(nolock) hpm on hpm.PLSG = md.Product_Line where hpm.PartNumber = '{}' and Price_Plan='{}' and Honeywell_Ref = '{}'".format(quoteItem.PartNumber , pricePlan , honeywellRef))
                    else:
                        result = SqlHelper.GetFirst("SELECT Discount FROM MPA_DISCOUNTS  where Product_Line = '{}' and Price_Plan='{}' and Honeywell_Ref = '{}'".format(quoteItem.PartNumber, pricePlan, honeywellRef))
                else:
                    writeInProduct = SqlHelper.GetFirst("SELECT WRITEINS FROM CT_SW_HW_WRITEINS(NOLOCK) WHERE WRITEINS_DESC = '{}'".format(' '.join(['Yr' if w.endswith('Yr') else w for w in quoteItem.PartNumber.split()])))
                    result = SqlHelper.GetFirst("SELECT Discount FROM MPA_DISCOUNTS(nolock) md JOIN WRITEINPRODUCTS(nolock) wp on wp.ProductLineSubGroup = md.Product_Line where wp.Product = '{}' and Price_Plan='{}' and Honeywell_Ref = '{}'".format(writeInProduct.WRITEINS if writeInProduct else quoteItem.PartNumber , pricePlan , honeywellRef))
            elif quote.GetCustomField("MPA").Content:
                val = quote.GetCustomField('MPA').Content
                ctval = SqlHelper.GetFirst("SELECT Salesforce_Agreement_ID FROM MPA_PRICE_PLAN_MAPPING(nolock) WHERE Agreement_Name='"+str(val)+"'")
                #result = SqlHelper.GetFirst("SELECT Discount FROM MPA_DISCOUNTS where Price_Plan='{}' and Salesforce_Agreement_ID = '{}'".format(pricePlan , ctval.Salesforce_Agreement_ID))
                if quoteItem.ProductTypeName != "Write-In":
                    if quoteItem.ProductName != "TPC_Product":
                        result = SqlHelper.GetFirst("SELECT Discount FROM MPA_DISCOUNTS md JOIN HPS_PRODUCTS_MASTER(nolock) hpm on hpm.PLSG = md.Product_Line where hpm.PartNumber = '{}' and Price_Plan='{}' and Salesforce_Agreement_ID = '{}'".format(quoteItem.PartNumber, pricePlan , ctval.Salesforce_Agreement_ID))
                    else:
                        result = SqlHelper.GetFirst("SELECT Discount FROM MPA_DISCOUNTS  where Product_Line = '{0}' and Price_Plan='{1}' and Salesforce_Agreement_ID = '{2}'".format(quoteItem.PartNumber, pricePlan , ctval.Salesforce_Agreement_ID))
                else:
                    writeInProduct = SqlHelper.GetFirst("SELECT WRITEINS FROM CT_SW_HW_WRITEINS(NOLOCK) WHERE WRITEINS_DESC = '{}'".format(' '.join(['Yr' if w.endswith('Yr') else w for w in quoteItem.PartNumber.split()])))
                    result = SqlHelper.GetFirst("SELECT Discount FROM MPA_DISCOUNTS md JOIN WRITEINPRODUCTS(nolock) wp on wp.ProductLineSubGroup = md.Product_Line where wp.Product= '{}' and Price_Plan='{}' and Salesforce_Agreement_ID = '{}'".format(writeInProduct.WRITEINS if writeInProduct else quoteItem.PartNumber, pricePlan , ctval.Salesforce_Agreement_ID))

            if result:
                return result.Discount
    return 0

def getMarketScheduleDiscount(quote,marketScheduleLookup,bookingLOB,productIN):
    discount = 0
    minMargin = 0
    effectiveDate = quote.EffectiveDate.ToString('MM/dd/yyyy')
    return SqlHelper.GetList("""select Discount,Minimum_Margin,hpm.PartNumber as PartNumber from MARKETDISCOUNT_SCHEDULE_PERCENTAGE(nolock) md join HPS_PRODUCTS_MASTER(nolock) hpm on hpm.PLSG = md.PL_PLSG where hpm.PartNumber {0} and md.Market_Schedule = '{1}' and md.LOB = '{2}' and ISNULL(NULLIF(md.Valid_From,''),CONVERT(DATE,'{3}')) <= '{3}' and ISNULL(NULLIF(md.Valid_To,''),GETDATE()) >= '{3}' union all SELECT Discount, Minimum_Margin, PL_PLSG as PartNumber from MARKETDISCOUNT_SCHEDULE_PERCENTAGE(nolock) where PL_PLSG {0} and Market_Schedule = '{1}' and LOB = '{2}' and ISNULL(NULLIF(Valid_From,''),CONVERT(DATE,'{3}')) <= '{3}' and ISNULL(NULLIF(Valid_To,''),GETDATE()) >= '{3}' """.format(productIN,marketScheduleLookup,bookingLOB,effectiveDate))

def applyMPA(quote):
    # Get Header Data  
    pricePlan = quote.GetCustomField('MPA Price Plan').Content
    honeywellRef = quote.GetCustomField('MPA Honeywell Ref').Content
    orderTotal = quote.GetCustomField('Total List Price').Content
    quoteType = quote.GetCustomField('Quote Type').Content
    # sfid = quote.GetCustomField('AccountId').Content
    # sfan = SqlHelper.GetFirst("SELECT Agreement_Name  FROM MPA_ACCOUNT_MAPPING WHERE Salesforce_ID  ='"+str(sfid)+"'")
    # quote.GetCustomField('MPA').Content = sfan.Agreement_Name if sfan is not None else ''
    MPA = getCFValue(quote , "MPA")
    exchangeRate = quote.GetCustomField('Exchange Rate').Content
    bookingLOB = quote.GetCustomField('Booking LOB').Content
    marketScheduleLookup = quote.GetCustomField('Selected Discount Plan').Content
    mpaValidity = quote.GetCustomField('MPA Validity').Content
    PROS_Guidance = '' #quote.GetCustomField('PROS Guidance Recommendation').Content
    validcheck = checkMPAPricePlanValidty(quote)
    threshold = float(getThreshold(quote , pricePlan , honeywellRef , quoteType) or 0) * float(exchangeRate)

    # Get Item Data
    productSet = set()
    for quoteitem in quote.Items:
        productSet.add(quoteitem.PartNumber)
    productIN = "IN ('{0}')".format("', '".join(productSet)) 
    marketData = getMarketScheduleDiscount(quote,marketScheduleLookup,bookingLOB,productIN)

    # Set Item Data
    for quoteItem in quote.Items:
        scheduleDiscount = 0
        minMargin = 0
        for dataRow in marketData:
            if quoteItem.PartNumber == dataRow.PartNumber:
                scheduleDiscount = dataRow.Discount
                minMargin = dataRow.Minimum_Margin
        minMarginTargetPrice = (getItemField(quoteItem , "ExtendedCost") * 100) / (100 - float(minMargin))
        PROSDiscPerc = getItemField(quoteItem , "QI_Guidance_Discount_Percent")
        PROSDiscAmt = getItemField(quoteItem , "QI_PROS_Guidance_Recommended_Price")
        if quoteType == "Projects" and bookingLOB in ('LSS','PAS'):
            if quoteItem.Description == 'Write-In Standard Warranty System':
                setItemField(quoteItem , 'QI_Min_Margin_Target_Price' , 0)
            else:
                setItemField(quoteItem , 'QI_Min_Margin_Target_Price' , minMarginTargetPrice)
        quote.GetCustomField("MPA Threshold").Content = str(threshold or 0)
        if pricePlan and threshold <= float(orderTotal) and not validcheck:
            discount = getMpaDiscountPercent(quote, quoteItem , pricePlan ,honeywellRef)
            setItemField(quoteItem , 'QI_MPA_Discount_Percent' , discount)
            if discount > 0:
                discountAmount = getItemField(quoteItem , "ExtendedListPrice") * (discount / 100)
                setItemField(quoteItem , "QI_MPA_Discount_Amount" , discountAmount)
        elif quoteType == "Projects" and marketScheduleLookup != "List Price" and marketScheduleLookup != '':
            if quote.GetCustomField('Quote Tab Booking LOB').Content=='PMC' and (validcheck or mpaValidity == ''):#MD-PMC MPA bypass CXCPQ-75113
                discount = getMpaDiscountPercent(quote, quoteItem , pricePlan ,honeywellRef)
                setItemField(quoteItem , 'QI_MPA_Discount_Percent' , discount)
                if discount > 0:
                    discountAmount = getItemField(quoteItem , "ExtendedListPrice") * (discount / 100)
                    setItemField(quoteItem , "QI_MPA_Discount_Amount" , discountAmount)
            elif quote.GetCustomField('Selected Discount Plan').Visible==True:
                setItemField(quoteItem , 'QI_MPA_Discount_Percent' , scheduleDiscount)
                if scheduleDiscount:
                    discountAmount = getItemField(quoteItem , "ExtendedListPrice") * (float(scheduleDiscount) / 100)
                    setItemField(quoteItem , "QI_MPA_Discount_Amount" , discountAmount)
            else:
                setItemField(quoteItem , 'QI_MPA_Discount_Percent' , 0)
                setItemField(quoteItem , "QI_MPA_Discount_Amount" , 0)
        else:
            if quote.GetCustomField('Quote Tab Booking LOB').Content == 'PMC':#MD-PMC MPA bypass CXCPQ-75113
                discount = getMpaDiscountPercent(quote, quoteItem , pricePlan ,honeywellRef)
                setItemField(quoteItem , 'QI_MPA_Discount_Percent' , discount)
                if discount > 0:
                    discountAmount = getItemField(quoteItem , "ExtendedListPrice") * (discount / 100)
                    setItemField(quoteItem , "QI_MPA_Discount_Amount" , discountAmount)
            else:
                setItemField(quoteItem , 'QI_MPA_Discount_Percent' , 0)
                setItemField(quoteItem , "QI_MPA_Discount_Amount" , 0)