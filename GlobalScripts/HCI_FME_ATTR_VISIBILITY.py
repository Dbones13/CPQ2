pn = Product.PartNumber
query = SqlHelper.GetFirst("SELECT 1 as flag FROM FME_PARTS WHERE PARTNUMBER = '{}'".format(pn))
if query is not None and Quote.GetCustomField('Booking LOB').Content=="HCP":
	for att in Product.Attributes:
		att.Access = AttributeAccess.ReadOnly
	ApiResponse = ApiResponseFactory.JsonResponse(True)
else:
    ApiResponse = ApiResponseFactory.JsonResponse(False)