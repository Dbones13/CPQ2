if Product.Attr('PERF_ExecuteScripts').GetValue() == 'SCRIPT_RUN':
    Trace.Write('C300 System addtoquote_start')

    cont = Product.GetContainerByName('Series_C_Control_Groups_Cont')
    Trace.Write('C300 Control groups:{}'.format(cont.Rows.Count))
    for r in cont.Rows:
        if r.Product.Attr('PERF_ExecuteScripts') is not None:
            r.Product.Attr('PERF_ExecuteScripts').AssignValue('SCRIPT_RUN')
            r.ApplyProductChanges()
            r.Product.ApplyRules()
    Product.Attr('PERF_ExecuteScripts').AssignValue('')
    Trace.Write('C300 System addtoquote_Complete')