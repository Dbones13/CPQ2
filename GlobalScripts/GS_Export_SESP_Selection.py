Quote.GenerateDocument('SC_SESP_Selection_Download_File', GenDocFormat.EXCEL)
jsonObject = {}
jsonObject['href'] = TagParserQuote.ParseString('<*CTX( Quote.LastGeneratedDocument.Link )*>').replace('http','https')
ApiResponse = ApiResponseFactory.JsonResponse(jsonObject)