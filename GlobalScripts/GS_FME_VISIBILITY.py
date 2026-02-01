pn = Product.PartNumber
query = SqlHelper.GetFirst("SELECT 1 as flag FROM FME_PARTS WHERE PARTNUMBER = '{}'".format(pn))
if query is not None:
    ApiResponse = ApiResponseFactory.JsonResponse(True)
else:
    ApiResponse = ApiResponseFactory.JsonResponse(False)