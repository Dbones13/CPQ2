CE_SystemGroup_Cont = Product.GetContainerByName('CN900_ControlGroup_Cont')
if CE_SystemGroup_Cont.Rows.Count == 0:
    newRow = CE_SystemGroup_Cont.AddNewRow('CN900_Control_Group_cpq', False)
    newRow.ApplyProductChanges()

if CE_SystemGroup_Cont.Rows.Count > 0:
    for row in CE_SystemGroup_Cont.Rows:
        CN900_CG_Name = row.Product.Attr('CN900_CG_Name').GetValue()
        if str(row["Control Group Name"]) != CN900_CG_Name:
            row.Product.Attr('CN900_CG_Name').AssignValue(str(row["Control Group Name"]))
            row.ApplyProductChanges()
CE_SystemGroup_Cont.Calculate()