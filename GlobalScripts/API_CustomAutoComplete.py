import GS_CommonUtil as cm

container = Product.GetContainerByName('Migration_MSID_Selection_Container')
container.Calculate()
selectedMSID = set()

for row in container.Rows:
    for col in filter(lambda x : x.Name == 'MSID' , row.Columns):
        selectedMSID.add(col.ReferencingAttribute.GetValue())

accountName = cm.getCFValue(Quote , "Account Name")
entitlementType = cm.getCFValue(Quote , "Entitlement")

query = "select Top 10 msid , CpqTableEntryId as Id from MSID as ms where Account_Name = '{}' and coalesce(EntitlementType , '') = '{}'"
if RequestContext.QueryString.Get('SearchValue'):
    query += " and msid like '%{}%'".format(RequestContext.QueryString.Get('SearchValue'))
query = query.format(accountName , entitlementType)
selectedMSID.discard('')
selectedMSID.discard(None)
if selectedMSID:
     query = "{} and MSID not in ('{}')".format(query , "','".join(selectedMSID))
query = "{} order by CpqTableEntryId".format(query)

res = SqlHelper.GetList(query)
response = cm.queryToDict(res , "Items")

ApiResponse = ApiResponseFactory.JsonResponse(response)