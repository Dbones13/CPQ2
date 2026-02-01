if Product.Attr('PERF_ExecuteScripts').GetValue() == 'SCRIPT_RUN':
    Trace.Write('system group addtoquote_start')
    smProd = ['Safety Manager HIPPS', 'Safety Manager BMS', 'Safety Manager FGS']
    smProd.extend(['Safety Manager HIPPS', 'Safety Manager ESD','C300 System', 'ARO & RESS System'])
    cont = Product.GetContainerByName('CE_System_Cont')
    for r in cont.Rows:
        if r.Product.Attributes.GetByName('PERF_ExecuteScripts'):
            r.Product.Attr('PERF_ExecuteScripts').AssignValue('SCRIPT_RUN')
            r.ApplyProductChanges()
            r.Product.ApplyRules()
        if r.Product.Name in smProd and r.Product.Attributes.GetByName('PERF_ExecuteScriptsLabor'):
            r.Product.Attr('PERF_ExecuteScriptsLabor').AssignValue('SCRIPT_RUN')
            r.Product.ApplyRules()
            r.ApplyProductChanges()
    Product.Attr('PERF_ExecuteScripts').AssignValue('')
    Trace.Write('system group addtoquote_Complete')
