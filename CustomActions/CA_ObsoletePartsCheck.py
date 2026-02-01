from datetime import datetime

def getobsoletePartList(Quote):
    partsList = []
    obsoleteParts = dict()
    obsoletePartList = []
    parts = SqlHelper.GetList("SELECT DISTINCT(CATALOGCODE) from CART_ITEM where CART_ID = '"+str(Quote.QuoteId)+"' and USERID  = '"+str(Quote.UserId)+"'")

    daystoCompare = DateTime.Now.Subtract(DateTime(1899 , 12 , 31)).Days
    query = ("select p.* from Products p join product_versions pv on p.Product_ID = pv.Product_ID where System_ID in ('{}') and pv.Is_Active = 1 ").format("','".join(i.CATALOGCODE for i in parts))
    res = SqlHelper.GetList(query)
    for i in res:
        d1 = i.D1 if i.D1 else 0
        d2 = i.D2 if i.D2 else 99999999999999999999999999
        if d1 <= daystoCompare <= d2:
            pass
        else:
            obsoletePartList.append(i.PRODUCT_CATALOG_CODE)
    return obsoletePartList

obsoletePartList = getobsoletePartList(Quote)
if len(obsoletePartList) >= 1:
    WorkflowContext.BreakWorkflowExecution = True
    if not Quote.Messages.Contains(Translation.Get('error.message.obsoleteParts').format("','".join(obsoletePartList))):
        Quote.Messages.Add(Translation.Get('error.message.obsoleteParts').format("','".join(obsoletePartList)))