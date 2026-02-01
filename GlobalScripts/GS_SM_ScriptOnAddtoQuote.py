if Product.Attr('PERF_ExecuteScripts').GetValue() == 'SCRIPT_RUN':
    Trace.Write('SM Control Group addtoquote_start')

    cont = Product.GetContainerByName('SM_ControlGroup_Cont')
    for r in cont.Rows:
        product = r.Product
        contRG = product.GetContainerByName('SM_RemoteGroup_Cont')
        for rr in contRG.Rows:
            if rr.Product.Attributes.GetByName('PERF_ExecuteScripts'):
                rr.Product.Attr('PERF_ExecuteScripts').AssignValue('SCRIPT_RUN')
                rr.Product.ApplyRules()
                rr.ApplyProductChanges()
        if product.Attributes.GetByName('PERF_ExecuteScripts'):
            product.Attr('PERF_ExecuteScripts').AssignValue('SCRIPT_RUN')
            product.ApplyRules()
            r.ApplyProductChanges()

    for r in cont.Rows:
        product = r.Product
        contRG = product.GetContainerByName('SM_RemoteGroup_Cont')
        for rr in contRG.Rows:
            rr.Product.Attr('PERF_ExecuteScripts').AssignValue('')
            rr.Product.ApplyRules()
            rr.ApplyProductChanges()
            rr.Calculate()
        contRG.Calculate()
        product.Attr('PERF_ExecuteScripts').AssignValue('')
        product.ApplyRules()
        r.ApplyProductChanges()
        r.Calculate()
    cont.Calculate()
    Product.Attr('PERF_ExecuteScripts').AssignValue('')
    Trace.Write('SM Control Group addtoquote_Complete')
    Product.ApplyRules()