parts = dict(Param.Parts)

query = "SELECT PartNumber, SalesText FROM HPS_PRODUCTS_MASTER where PartNumber in ('{}')"
query = query.format("','".join(parts.keys()))

res = SqlHelper.GetList(query)
response = dict()
for r in res:
    response[str(parts[r.PartNumber])] = r.SalesText
ApiResponse = ApiResponseFactory.JsonResponse(response)