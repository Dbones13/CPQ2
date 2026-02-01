selectedprd = Product.Attr('AR_CyberPrdChoices').GetValue().split(', ')
ApiResponse = ApiResponseFactory.JsonResponse(selectedprd)