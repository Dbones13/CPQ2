priceData = ''
if Quote.GetCustomField('Quote Type').Content in ('Contract New','Contract Renewal'):
    priceData = {}
    cfList = ['Honeywell List Price(USD)', 'Honeywell List Price', 'Total Discount Percent(CW)', 'Total Sell Price(USD)', 'Total Sell Price(CW)']
    for cf in cfList:
        priceData[cf] = Quote.GetCustomField(cf).Content
ApiResponse = ApiResponseFactory.JsonResponse(priceData)