partsQty = dict()
validPartsCon = Product.GetContainerByName("PU_Valid_Parts")

if validPartsCon.Rows.Count > 0:
    for row in validPartsCon.Rows:
        partsQty[row.UniqueIdentifier] = int(row["Quantity"])
        partsQty[str(row.UniqueIdentifier)+"Area"] = row["Area"]
        partsQty[str(row.UniqueIdentifier)+"Year"] = row["Year"]
        #if row.Product and row.Product.Attributes.GetByName('ItemQuantity'):
            #row.Product.Attributes.GetByName('ItemQuantity').AssignValue(str(row["Quantity"]))

for item in arg.QuoteItemCollection:
    if partsQty.get(item.QuoteItemGuid):
        Trace.Write('TestingPart' + '   ' + str(partsQty.get(item.QuoteItemGuid)))
        item.Quantity = partsQty[item.QuoteItemGuid]
        #item.BaseQuantity = partsQty[item.QuoteItemGuid]
        item['QI_Area'].Value = partsQty[str(item.QuoteItemGuid)+"Area"]
        item['QI_Year'].Value = partsQty[str(item.QuoteItemGuid)+"Year"]
Quote.Calculate(1)