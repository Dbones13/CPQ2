HONProductCon = Product.GetContainerByName("Generic_System_Part_Upload_Cont")
GS_FMeValid_Con = Product.GetContainerByName("Generic_System_Valid_FME_Cont")
GS_FMeValid_Con.Rows.Clear()

for Urow in HONProductCon.Rows:
    new_row = GS_FMeValid_Con.AddNewRow()
    #new_row.IsSelected = True
    new_row["ID"] = str(Urow["ID"])
    new_row["Part Number"] = str(Urow["Part Number"])
    new_row["Item Quantity"] = str(Urow["Quantity"])