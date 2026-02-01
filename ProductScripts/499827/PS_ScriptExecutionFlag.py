cont = Product.GetContainerByName('CE_SystemGroup_Cont')
for r in cont.Rows:
    if r.Product.Attr('PERF_ExecuteScripts') is not None:
        r.Product.Attr('PERF_ExecuteScripts').AssignValue('SCRIPT_RUN')
        r.Product.ApplyRules()
        r.ApplyProductChanges()