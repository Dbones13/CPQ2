Product.Attr('PERF_ExecuteScripts').AssignValue('SCRIPT_RUN')
Series_RCont = Product.GetContainerByName('Series_C_Remote_Groups_Cont')
for item in Series_RCont.Rows:
    if item['RemoteGroupCheck']:
        item['RemoteGroupCheck'] = ''
        item.Product.Attr("RemoteGroupCheck").AssignValue('')