'''if Quote.GetCustomField("Booking LOB").Content != 'CCC':
    import GS_ItemCalculations

    quoteStatus = True if Quote and Quote.OrderStatus.Name == 'Preparing' else False
    #ApiResponse = ApiResponseFactory.JsonResponse(quoteStatus)

    
    if Quote.OrderStatus.Name == 'Booked':
        ScriptExecutor.Execute('CA_CalculateCost')
    
    if Quote.OrderStatus.Name in ["Preparing","Approved","Submitted to Customer","Accepted by Customer","Pending Project Creation","Project Created","Pending Order Confirmation","Booked"] and Quote.GetCustomField('Quote Type').Content not in ('Contract New','Contract Renewal') :
        for Item in Quote.Items:
            GS_ItemCalculations.calculateCosts(Quote , Quote.GetCustomField("Booking LOB").Content,Quote.GetCustomField("Quote Type").Content,Item, TagParserQuote)
            Item.ExtendedCost = Item.Quantity * Item.Cost'''