currency = ''
if Quote is not None:
    if Quote.GetCustomField('Quote Type').Content in ['Contract New','Contract Renewal']:
        currency = Quote.SelectedMarket.CurrencyCode
ApiResponse = ApiResponseFactory.JsonResponse(currency)