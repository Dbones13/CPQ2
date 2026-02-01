sys_groups = Product.GetContainerByName("CE_SystemGroup_Cont").Rows
for row in sys_groups:
    sys_group = row.Product
    Sys_Group_Name = sys_group.Attr('Sys_Group_Name').GetValue()
    Trace.Write("Sys_Group_Name:{}".format(Sys_Group_Name))
    for each in sys_group.GetContainerByName("CE_System_Cont").Rows:
        system = each.Product
        system.Attr('Sys_Group_Name').AssignValue(Sys_Group_Name)
        each.ApplyProductChanges()