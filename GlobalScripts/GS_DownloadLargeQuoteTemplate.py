templates = {'PL':'PL_Discount_Download', 'PLSG':'PLSG_Discount_Download'}
if Param.scenario in templates.Keys:
    Quote.GenerateDocument(templates[Param.scenario], GenDocFormat.EXCEL)
    jsonObject = {}
    jsonObject['href'] = TagParserQuote.ParseString('<*CTX( Quote.LastGeneratedDocument.Link )*>').replace('http','https')
    ApiResponse = ApiResponseFactory.JsonResponse(jsonObject)