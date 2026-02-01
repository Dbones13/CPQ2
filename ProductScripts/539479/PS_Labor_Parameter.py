Product.Attr('PERF_ExecuteScripts').AssignValue('SCRIPT_RUN')
Product.ApplyRules()
for row in Product.GetContainerByName('Series_C_Control_Groups_Cont').Rows:
    for rowrg in row.Product.GetContainerByName('Series_C_Remote_Groups_Cont').Rows:
        rowrg.Calculate()
        rowrg.ApplyProductChanges()
    row.Product.GetContainerByName('Series_C_Remote_Groups_Cont').Calculate()
    row.Product.ApplyRules()
    row.Calculate()
    row.ApplyProductChanges()
Product.GetContainerByName('Series_C_Control_Groups_Cont').Calculate()
Product.ApplyRules()