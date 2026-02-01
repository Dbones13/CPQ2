if Product.Attr('PERF_ExecuteScripts').GetValue() == 'SCRIPT_RUN':
    Trace.Write('Experion Enterprise Group addtoquote_start')

    cont = Product.GetContainerByName('List of Locations/Clusters/Network Groups')
    for r in cont.Rows:
        if r.Product.Attr('PERF_ExecuteScripts') is not None:
            r.Product.Attr('PERF_ExecuteScripts').AssignValue('SCRIPT_RUN')
            r.ApplyProductChanges()
            r.Product.ApplyRules()
    Product.Attr('PERF_ExecuteScripts').AssignValue('')
    Trace.Write('Experion Enterprise Group addtoquote_Complete')