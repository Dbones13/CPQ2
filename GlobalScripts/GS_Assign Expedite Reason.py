def getCFValue(quote,field):
    return Quote.GetCustomField(field).Content

def setCFValue(field, value):
    Quote.GetCustomField(field).Content = value

def calculateExpediteFee(quote, item):
    if item['QI_Customer_Requested_Date'].Value :
        isValid = DateTime.Compare(item['QI_LT_Delivery_Date'].Value, item['QI_Customer_Requested_Date'].Value) > 0
    else:
        isValid = False
    if item['QI_Expedite_Reason'].Value and isValid and getCFValue(quote,"Expedite Fee Waiver") != 'True' and not(getCFValue(quote,"Expedite Fee Waiver Reason")) :
        Trace.Write("here 1")
        exchangeRate	= getCFValue(quote,'Exchange Rate') if getCFValue(quote,'Exchange Rate').strip() !='' else 1.0
        expedite_fee	= 0
        unitSellPrice	= float(item.NetPrice)/ float(exchangeRate)
        value			= 0.1 * unitSellPrice
        if value < 500:
            expedite_fee= 500 * float(exchangeRate) * item.Quantity
            item['QI_Expedite_Fees'].Value = round(expedite_fee,2)
        else:
            expedite_fee = value * item.Quantity
            item['QI_Expedite_Fees'].Value = round(expedite_fee,2)
    else:
        item['QI_Expedite_Fees'].Value = 0

if getCFValue(Quote, "Quote Tab Booking LOB") == 'LSS' and getCFValue(Quote,"Quote Type") == 'Parts and Spot':
    expReason = getCFValue(Quote,"Expedite Reason")
    totalExpedite = 0.0
    for item in Quote.Items :
        item["QI_Expedite_Reason"].Value = expReason
        calculateExpediteFee(Quote, item)
        totalExpedite = float(totalExpedite) + float(item['QI_Expedite_Fees'].Value)
    setCFValue('Expedite Fee', str(totalExpedite))