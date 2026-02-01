RecommendedVCpart = Product.GetContainerByName("Recommended_VC_PartCont")
SparePartsList = []
for row in RecommendedVCpart.Rows:
    if row["Recommended Spare Part"] not in SparePartsList:
        SparePartsList.append(row["Recommended Spare Part"])
for item in Quote.MainItems:
    if item.PartNumber in SparePartsList:
        item.Delete()
        break