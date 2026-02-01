quoteStatus = ""
if Quote and Quote.GetCustomField('Quote Type').Content in ['Contract New','Contract Renewal']:
    quoteStatus = True if Quote and Quote.OrderStatus.Name == 'Preparing' else False
ApiResponse = ApiResponseFactory.JsonResponse(quoteStatus)