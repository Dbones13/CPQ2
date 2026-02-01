#pn = Product.PartNumber
#query = SqlHelper.GetFirst("SELECT 1 as flag FROM DISPLAY_VALUECODE WHERE PARTNUMBER = '{}'".format(pn))
try:
    query = SqlHelper.GetList("SELECT PARTNUMBER FROM DISPLAY_VALUECODE ")
    if 1==1:#query is not None:
        #ApiResponse = ApiResponseFactory.JsonResponse(True)
        ApiResponse = ApiResponseFactory.JsonResponse([i.PARTNUMBER for i in query])
    else:
        ApiResponse = ApiResponseFactory.JsonResponse(False)
except:
    pass