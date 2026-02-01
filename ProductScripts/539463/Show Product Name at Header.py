PCD_Group_Cont = Product.GetContainerByName('PCD_Cont')
if PCD_Group_Cont.Rows.Count > 0:
    for row in PCD_Group_Cont.Rows:
        PCD_Grp_Name = row.Product.Attr('PCD_Group_Name').GetValue()
        if str(row["ControlEdge PCD Group Name"]) != PCD_Grp_Name:
            row.Product.Attr('PCD_Group_Name').AssignValue(str(row["ControlEdge PCD Group Name"]))
            row.ApplyProductChanges()
PCD_Group_Cont.Calculate()