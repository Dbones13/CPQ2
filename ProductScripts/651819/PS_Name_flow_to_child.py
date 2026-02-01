CGCont = Product.GetContainerByName('ES_Group')
esGroup = Product.Attr('ES_Count').GetValue()
if esGroup == '':
    Product.Attr('ES_Count').AssignValue('1')
if CGCont.Rows.Count > 0:
    for row in CGCont.Rows:
        Sys_Group_Name = row.Product.Attr('eServer_name').GetValue()
        if str(row["eServer_System_Group_Name"]) != Sys_Group_Name:
            row.Product.Attr('eServer_name').AssignValue(str(row["eServer_System_Group_Name"]))
        row.ApplyProductChanges()
        row.Calculate()