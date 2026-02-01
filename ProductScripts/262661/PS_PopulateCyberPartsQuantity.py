partsQty = dict()
addcyberPartCon = Product.GetContainerByName("Add_Cyber_Parts_Container")

if addcyberPartCon.Rows.Count > 0:
    for row in addcyberPartCon.Rows:
        partsQty[row.UniqueIdentifier] = [int(row["Quantity"]),row["Product"]]

for item in arg.QuoteItemCollection:
    if partsQty.get(item.QuoteItemGuid):
        item.Quantity = partsQty[item.QuoteItemGuid][0]
        item.QI_CyberProductFlag.Value = "Cyber Product"
Quote.Calculate(1)