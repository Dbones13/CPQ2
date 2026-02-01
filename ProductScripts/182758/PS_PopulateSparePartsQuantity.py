partsQty = dict()
RecommVCPartsCon = Product.GetContainerByName("Recommended_VC_PartCont")

if RecommVCPartsCon.Rows.Count > 0:
    for row in RecommVCPartsCon.Rows:
        partsQty[row.UniqueIdentifier] = int(row["Quantity"])

for item in arg.QuoteItemCollection:
    if partsQty[item.QuoteItemGuid]:
        item.Quantity = partsQty[item.QuoteItemGuid]
Quote.Calculate(1)