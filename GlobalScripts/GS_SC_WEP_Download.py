#####Code Need to be added for download functionality of WEP####
''' restructed code Nilesh - 27082024 '''
filename = 'SC_WEP_Download_File_Renewal' if Product.Attr('SC_Product_Type').GetValue() == "Renewal" else 'SC_WEP_Download_File_New'
Quote.GenerateDocument(filename, GenDocFormat.EXCEL)
jsonObject = {}
jsonObject['href'] = TagParserQuote.ParseString('<*CTX( Quote.LastGeneratedDocument.Link )*>').replace('http','https')
ApiResponse = ApiResponseFactory.JsonResponse(jsonObject)