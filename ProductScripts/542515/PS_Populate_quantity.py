partsQty = dict()
validPartsCon = Product.GetContainerByName("Generic_System_Part_Upload_Cont")

if validPartsCon.Rows.Count > 0:
    for row in validPartsCon.Rows:
        partsQty[row.UniqueIdentifier] = int(row["Quantity"])

for item in arg.QuoteItemCollection:
    if partsQty.get(item.QuoteItemGuid):
        item.Quantity = partsQty[item.QuoteItemGuid]