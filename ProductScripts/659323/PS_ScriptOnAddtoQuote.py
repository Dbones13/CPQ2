if Product.Attr('PERF_ExecuteScripts').GetValue() == 'SCRIPT_RUN':
    Trace.Write('ARO RESS addtoquote_start')
    Product.Attr('PERF_ExecuteScripts').AssignValue('')
    Trace.Write('ARO RESS addtoquote_Complete')