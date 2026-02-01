if Product.Attr('PERF_ExecuteScripts').GetValue() == 'SCRIPT_RUN':
    Trace.Write('List of Locations/Clusters/ Network Groups  addtoquote_start')
    Product.Attr('PERF_ExecuteScripts').AssignValue('')
    Trace.Write('List of Locations/Clusters/ Network Groups  addtoquote_Complete')