isR2Qquote = True if Quote.GetCustomField("isR2QRequest").Content else False
Checkproduct = Product.ParseString('<*CTX(Product.RootProduct.PartNumber)*>')
if isR2Qquote and Checkproduct == 'PRJT R2Q':
    if Product.GetContainerByName('PLC_CG_Controller_Rack_Cont').Rows.Count:
        Product.GetContainerByName('PLC_CG_Controller_Rack_Cont').Rows[0].GetColumnByName('PLC_IO_Rack_Type').SetAttributeValue('Optimum Mixed I/O Rack')
        containername = Product.GetContainerByName('PLC_CG_Controller_Rack_Cont')
        for row in containername.Rows:
            row['PLC_IO_Rack_Type'] = 'Optimum Mixed I/O Rack'

if isR2Qquote and Checkproduct == 'Migration':
    Product.Attr('R2QRequest').AssignValue('Yes')
    Product.Attr("R2Q_QuoteNumber").AssignValue(str(Quote.CompositeNumber))

    columns_to_hide = [
        'PLC_Field_Wiring_DIDOAOAI_Channel_Mod',
        'PLC_G3_Option_Ethernet_Switch',
        'PLC_Field_Wiring_PIFII_Channel_Mod',
        'PLC_Field_Wiring_Other_Mod',
        'PLC_Remote_Terminal_Cable_Length',
        'PLC_Ethernet_Switch_Supplier'
    ]
    

    for column in columns_to_hide:
        Product.ParseString('<*CTX( Container({}).Column("{}").SetPermission({}) )*>'.format('PLC_CG_Controller_Rack_Cont', column, 'Hidden'))
