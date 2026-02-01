FDMCont = Product.GetContainerByName('FDM_System_Group_Cont')
if FDMCont.Rows.Count > 0:
    for row in FDMCont.Rows:
        Sys_Group_Name = row.Product.Attr('FDM_System_Group_Name').GetValue()
        if str(row["FDM_System_Group_Name"]) != Sys_Group_Name:
            row.Product.Attr('FDM_System_Group_Name').AssignValue(str(row["FDM_System_Group_Name"]))
        row.ApplyProductChanges()
        row.Calculate()