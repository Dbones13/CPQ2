partsQty = dict()
addRecommendedVCpart = Product.GetContainerByName("VFD_Add_Recommended_VC_PartCont")

if addRecommendedVCpart.Rows.Count > 0:
    for row in addRecommendedVCpart.Rows:
        partsQty[row.UniqueIdentifier] = [int(row["Quantity"]),row["VC Model Number"]]

for item in arg.QuoteItemCollection:
    if partsQty[item.QuoteItemGuid]:
        item.Quantity = partsQty[item.QuoteItemGuid][0]
        item.QI_SparePartsFlag.Value = "Spare Part"
        item.QI_ParentVcModel.Value = partsQty[item.QuoteItemGuid][1]
Quote.Calculate(1)