import GS_Add_To_Quote
if Product.Attr('PERF_ExecuteScripts').GetValue() == 'SCRIPT_RUN':
    Log.Info('Experion Enterprise System addtoquote_start')
    GS_Add_To_Quote.addToQuote(Product, Quote, TagParserQuote)
    cont = Product.GetContainerByName('Experion_Enterprise_Cont')
    for r in cont.Rows:
        if r.Product.Attr('PERF_ExecuteScripts') is not None:
            r.Product.Attr('PERF_ExecuteScripts').AssignValue('SCRIPT_RUN')
            r.ApplyProductChanges()
            r.Product.ApplyRules()
    Product.Attr('PERF_ExecuteScripts').AssignValue('')
    Log.Info('Experion Enterprise System addtoquote_Complete')