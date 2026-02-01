exeperionEntContainer = Product.GetContainerByName('Experion_Enterprise_Cont')
#Product.Attr('MIB Exp Ent Grp').AssignValue(Product.Attr('MIB Configuration Required?').GetValue())
if exeperionEntContainer.Rows.Count > 0:
    i=1
    for row in exeperionEntContainer.Rows:
        Sys_Group_Name = row.Product.Attr('Experion Enterprise Group Name').GetValue()
        if str(row["Experion Enterprise Group Name"]) != Sys_Group_Name:
            row.Product.Attr('Experion Enterprise Group Name').AssignValue(str(row["Experion Enterprise Group Name"]))
        row.Product.Attr('Experion Enterprise Group Number').AssignValue(str(i))
        row.Product.Attr('PERF_ExecuteScripts').AssignValue('SCRIPT_RUN')
#        row.Product.Attr('MIB Configuration Required?').AssignValue(Product.Attr('MIB Configuration Required?').GetValue())
        i = i + 1
        row.ApplyProductChanges()
        row.Calculate()