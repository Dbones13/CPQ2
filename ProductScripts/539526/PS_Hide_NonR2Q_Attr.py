isR2Qquote = True if Quote.GetCustomField("isR2QRequest").Content else False
Checkproduct = Product.ParseString('<*CTX(Product.RootProduct.PartNumber)*>')
if isR2Qquote or (Quote.GetCustomField('R2QFlag').Content == 'Yes'):
    Product.Attr('R2QRequest').AssignValue('Yes')
    Product.Attr("R2Q_QuoteNumber").AssignValue(str(Quote.CompositeNumber))
    columns = [
    ('PLC_RG_Controller_Rack_Cont', 'PLC_Field_Wiring_DIDOAOAI_Channel_Mod'),
    ('PLC_RG_Controller_Rack_Cont', 'PLC_Field_Wiring_PIFII_Channel_Mod'),
    ('PLC_RG_Controller_Rack_Cont', 'PLC_Field_Wiring_Other_Mod'),
    ('PLC_RG_Controller_Rack_Cont', 'PLC_Remote_Terminal_Cable_Length')
    ]
    Product.GetContainerByName('PLC_RG_Controller_Rack_Cont').Rows[0].GetColumnByName('PLC_Power_Status_Mod_Redudant_Supply').SetAttributeValue('No')
    if Checkproduct == 'PRJT R2Q' or Checkproduct == 'PRJT' :
        Product.GetContainerByName('PLC_RG_Controller_Rack_Cont').Rows[0].GetColumnByName('PLC_IO_Rack_Type').SetAttributeValue('Optimum Mixed I/O Rack')
    else:
        Product.GetContainerByName('PLC_RG_Controller_Rack_Cont').Rows[0].GetColumnByName('PLC_IO_Rack_Type').SetAttributeValue('12 I/O Rack')
for container, column in columns:
    Product.ParseString('<*CTX( Container({}).Column("{}").SetPermission({}) )*>'.format(container, column, 'Hidden'))