if Product.Attr('PERF_ExecuteScripts').GetValue() == 'SCRIPT_RUN':
    Trace.Write('Series-C Remote Group addtoquote_start')
    Product.Attr('PERF_ExecuteScripts').AssignValue('')
    Trace.Write('Series-C Remote Group addtoquote_Complete')