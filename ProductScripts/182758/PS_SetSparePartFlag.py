RecommendedVCpart = Product.GetContainerByName("Recommended_VC_PartCont")
SpareParts = dict()
if RecommendedVCpart.HasSelectedRow:
    for row in RecommendedVCpart.Rows:
        SpareParts[row["Recommended Spare Part"]] = row["VC Model Number"]

if SpareParts:
    for item in arg.QuoteItemCollection:
        if item.PartNumber in SpareParts:
            item.QI_SparePartsFlag.Value = "Spare Part"
            item.QI_ParentVcModel.Value = SpareParts[item.PartNumber]
    Quote.Save(False)