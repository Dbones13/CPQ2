partdet = Product.GetContainerByName("SC_P1P2_Parts_Details")
if partdet.Rows.Count>0:
    filename = 'SC_P1P2_Export_File_Renewal' if Product.Attr('SC_Product_Type').GetValue() == "Renewal" else 'SC_P1P2_Export_File_New'
    Quote.GenerateDocument(filename, GenDocFormat.EXCEL)
    jsonObject = {}
    jsonObject['href'] = TagParserQuote.ParseString('<*CTX( Quote.LastGeneratedDocument.Link )*>').replace('http','https')
    ApiResponse = ApiResponseFactory.JsonResponse(jsonObject)
else:
    Quote.GenerateDocument('SC_P1P2_Download_File', GenDocFormat.EXCEL)
    jsonObject = {}
    jsonObject['href'] = TagParserQuote.ParseString('<*CTX( Quote.LastGeneratedDocument.Link )*>').replace('http','https')
    ApiResponse = ApiResponseFactory.JsonResponse(jsonObject)