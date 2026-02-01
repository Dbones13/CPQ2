isValid = False
itemsWithoutExpediteReason = []
totalExpedite = 0.0
if Quote.GetCustomField('Booking Lob').Content == "LSS" and Quote.GetCustomField('Quote Type').Content == 'Parts and Spot':
    for item in Quote.Items:
        if item['QI_Customer_Requested_Date'].Value and item['QI_LT_Delivery_Date'].Value:
            isValid = DateTime.Compare(item['QI_LT_Delivery_Date'].Value, item['QI_Customer_Requested_Date'].Value) > 0
            if isValid and not(item['QI_Expedite_Reason'].Value):
                itemsWithoutExpediteReason.Add(item.RolledUpQuoteItem)
        totalExpedite = float(totalExpedite) + float(item['QI_Expedite_Fees'].Value)
    if itemsWithoutExpediteReason:
        itemReasonString  = (',').join(itemsWithoutExpediteReason)
        if Quote.GetCustomField('Quote Type').Content !='Projects':
            if not Quote.Messages.Contains('Kindly enter Expedite Reason for the items: {0}'.format(itemReasonString)):
                Quote.Messages.Add('Kindly enter Expedite Reason for the items: {0}'.format(itemReasonString))
Quote.GetCustomField('Expedite Fee').Content = str(totalExpedite)