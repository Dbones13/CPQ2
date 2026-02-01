validPartsCon = Product.GetContainerByName("PU_Valid_Parts")
RecommVCPartsCon = Product.GetContainerByName("Recommended_VC_PartCont")
#CXCPQ-46818 and CXCPQ-46819 : PMC VFD Changes
cyberPartCon = Product.GetContainerByName("Cyber_Parts_Container")
addcyberPartCon = Product.GetContainerByName("Add_Cyber_Parts_Container")
vfdRecommVCPartsCon = Product.GetContainerByName("VFD_Recommended_VC_PartCont")
vfdaddRecommendedVCpart = Product.GetContainerByName("VFD_Add_Recommended_VC_PartCont")

if validPartsCon:
    if Product.Attr('PU_SelectValidParts').SelectedValue:
        #validPartsCon.MakeAllRowsSelected()
        #We must select each row individually and set the ItemQuantity attribute, or the quanity will get reset upon further action on the line item
        for row in validPartsCon.Rows:
            row.IsSelected = True
            if row.Product and row.Product.Attributes.GetByName("ItemQuantity"):
                row.Product.Attr("ItemQuantity").AssignValue(row["Quantity"])
                row.ApplyProductChanges()
    else:
        for row in validPartsCon.Rows:
            row.IsSelected = False
    validPartsCon.Calculate()

elif RecommVCPartsCon:
    if Product.Attr('PU_SelectValidParts').SelectedValue:
        RecommVCPartsCon.MakeAllRowsSelected()
    else:
        for row in RecommVCPartsCon.Rows:
            row.IsSelected = False
    RecommVCPartsCon.Calculate()
#CXCPQ-46818 and CXCPQ-46819 : PMC VFD Changes
elif cyberPartCon:
    if Product.Attr('PU_SelectValidParts').SelectedValue:
        cyberPartCon.MakeAllRowsSelected()
    else:
        for row in cyberPartCon.Rows:
            row.IsSelected = False
    cyberPartCon.Calculate()

    for row in cyberPartCon.Rows:
        for Row in addcyberPartCon.Rows:
            if row["Product"] == Row["Product"]:
                Row.IsSelected = row.IsSelected
                break
        else:
            addNewRow = addcyberPartCon.AddNewRow()
            addNewRow["Select"] = row["Select"]
            addNewRow["Product"] = row["Product"]
            addNewRow["Description"] = row["Description"]
            addNewRow["Quantity"] = row["Quantity"]
            addNewRow.IsSelected = True

elif vfdRecommVCPartsCon:
    if Product.Attr('VFD_PU_SelectValidParts').SelectedValue:
        vfdRecommVCPartsCon.MakeAllRowsSelected()
    else:
        for row in vfdRecommVCPartsCon.Rows:
            row.IsSelected = False
    vfdRecommVCPartsCon.Calculate()
    
    for row in vfdRecommVCPartsCon.Rows:
        for Row in vfdaddRecommendedVCpart.Rows:
            if row["VC Model Number"] == Row["VC Model Number"] and row["Recommended Spare Part"] == Row["Recommended Spare Part"]:
                Row.IsSelected = row.IsSelected
                break
        else:
            addNewRow = vfdaddRecommendedVCpart.AddNewRow()
            addNewRow["Select"] = row["Select"]
            addNewRow["VC Model Number"] = row["VC Model Number"]
            addNewRow["Selected Variant"] = row["Selected Variant"]
            addNewRow["Recommended Spare Part"] = row["Recommended Spare Part"]
            addNewRow["Spare Part Description"] = row["Spare Part Description"]
            addNewRow["Spare Parts Type"] = row["Spare Parts Type"]
            addNewRow["Quantity"] = row["Quantity"]
            addNewRow.IsSelected = True