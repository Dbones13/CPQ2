def getobsoletePartList(Quote):
    partsList = []
    obsoletePartList = []
    

    partsList = [item.PartNumber for item in Quote.Items if item.PartNumber not in partsList]

    daystoCompare = DateTime.Now.Subtract(DateTime(1899 , 12 , 31)).Days
    query = ("select p.D1, p.D2, p.PRODUCT_CATALOG_CODE from Products(nolock) p join product_versions(nolock) pv on p.Product_ID = pv.Product_ID where System_ID in ('{}') and pv.Is_Active = 1 ").format("','".join(partsList))
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
if len(obsoletePartList) >= 1 and (not Quote.Messages.Contains(Translation.Get('error.message.obsoleteParts').format("','".join(obsoletePartList)))):
    Quote.Messages.Add(Translation.Get('error.message.obsoleteParts').format("','".join(obsoletePartList)))