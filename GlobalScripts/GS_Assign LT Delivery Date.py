def getCFValue(quote , field):
    return quote.GetCustomField(field).Content

def calculateLTDevileryDate(quote, item):
    leadTime =item['QI_LeadTime'].Value
    quoteRepriceDate = getCFValue(quote , 'Quote Reprice Date')
    convertedQuoteRepriceDate =UserPersonalizationHelper.CovertToDate(quoteRepriceDate)
    deliveryDate = convertedQuoteRepriceDate.AddDays(leadTime)
    item['QI_LT_Delivery_Date'].Value = deliveryDate

for item in Quote.Items:
    calculateLTDevileryDate(Quote, item)