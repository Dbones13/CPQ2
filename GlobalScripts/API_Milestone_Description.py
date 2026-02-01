searchValue = Param.searchValue
mileStoneCategory = Quote.GetCustomField("Payment Milestones Category").Content
query = "select distinct Description from MILESTONE_DESCRIPTION where Billing_Milestone = '{}' and Milestone_Category = '{}'".format(searchValue,mileStoneCategory)
res = SqlHelper.GetList(query)

r = set()
for row in res:
    r.add(row.Description)

ApiResponse = ApiResponseFactory.JsonResponse(r)