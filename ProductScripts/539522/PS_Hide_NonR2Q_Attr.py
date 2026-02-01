isR2Qquote = True if Quote.GetCustomField("isR2QRequest").Content else False
checkproduct = Product.ParseString('<*CTX(Product.RootProduct.PartNumber)*>')

if isR2Qquote and checkproduct == 'Migration':
    container = Product.GetContainerByName('UOC_RG_Controller_Rack_Cont')
    if container and container.Rows.Count > 0:
        containerRow = container.Rows[0]
        containerRow.Product.Attr('UOC_IO_Rack_Type').SelectValue('12Rack')
        containerRow.Product.Attr('UOC_Power_Supply').SelectDisplayValue('Non Redundant')
        containerRow.Product.ApplyRules()
        containerRow.ApplyProductChanges()
        containerRow.Calculate()
else:
    container = Product.GetContainerByName('UOC_RG_Controller_Rack_Cont')
    if container and container.Rows.Count > 0:
        containerRow = container.Rows[0]
        if containerRow.GetColumnByName('UOC_IO_Rack_Type').Value == '':
            containerRow.Product.Attr('UOC_IO_Rack_Type').SelectValue('4Rack')
            containerRow.Product.ApplyRules()
            containerRow.ApplyProductChanges()
            containerRow.Calculate()