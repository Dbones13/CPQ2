Quote.GenerateDocument('Write In Part Upload Template', GenDocFormat.EXCEL)
jsonObject = {}
jsonObject['href'] = TagParserQuote.ParseString('<*CTX( Quote.LastGeneratedDocument.Link )*>').replace('http','https')
ApiResponse = ApiResponseFactory.JsonResponse(jsonObject)