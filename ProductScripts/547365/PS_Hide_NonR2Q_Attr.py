isR2Qquote = True if Quote.GetCustomField("isR2QRequest").Content else False
checkproduct= Product.ParseString('<*CTX(Product.RootProduct.PartNumber)*>')
if isR2Qquote and checkproduct == 'Migration':
    Product.Attr('R2QRequest').AssignValue('Yes')
    Product.Attr("R2Q_QuoteNumber").AssignValue(str(Quote.CompositeNumber))
    uoc_attributes_to_hide = [
        'UOC_Exp_PKS_software_release',
        'UOC_Shielded_Terminal_Strip',
        'UOC_IO_Filler_Module',
        'UOC_IO_Spare',
        'UOC_IO_Slot_Spare',
        'UOC_Cluster',
        'UOC_Starter_Kit'
    ]

    for attr in uoc_attributes_to_hide:
        Product.ParseString('<*CTX( Container({}).Column("{}").SetPermission({}) )*>'.format('UOC_Common_Questions_Cont', attr, 'Hidden'))