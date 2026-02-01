CE_SystemGroup_Cont = Product.GetContainerByName('SM_ControlGroup_Cont')
if CE_SystemGroup_Cont.Rows.Count == 0:
    newRow = CE_SystemGroup_Cont.AddNewRow('SM_Control_Group_cpq', False)
    newRow.ApplyProductChanges()

SM_ControlGroup_Cont = Product.GetContainerByName('SM_ControlGroup_Cont')
if SM_ControlGroup_Cont.Rows.Count > 0:
    contCal = False
    for row in SM_ControlGroup_Cont.Rows:
        SM_CG_Name = row.Product.Attr('SM_CG_Name').GetValue()
        if str(row["Control Group Name"]) != SM_CG_Name:
            row.Product.Attr('SM_CG_Name').AssignValue(str(row["Control Group Name"]))
            row.ApplyProductChanges()
            contCal = True
        if row.Product.Attr('SM_System_Scope').GetValue() != Product.Attr('SM_System_Scope').GetValue():
            row.Product.Attr('SM_System_Scope').AssignValue(Product.Attr('SM_System_Scope').GetValue())
            row.ApplyProductChanges()
            contCal = True
    if contCal:
        SM_ControlGroup_Cont.Calculate()