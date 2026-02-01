searchValue = Param.searchValue
query = "select distinct Country_of_Origin from COUNTRY_OF_ORIGIN_PLSG_MAPPING where PLSG = '{}'".format(searchValue)
res = SqlHelper.GetList(query)
r = set()
for row in res:
    r.add(row.Country_of_Origin)
ApiResponse = ApiResponseFactory.JsonResponse(r)