def hideContainerColumns(contColumnList, access):
    for contColumn in contColumnList:
        for col in contColumnList[contColumn]:
            TagParserProduct.ParseString('<*CTX( Container({0}).Column({1}).SetPermission({2}) )*>'.format(contColumn,col,access))
def hideAttr(attrList,access):
    for attr in attrList:
        if access =='hide':
            Product.Attr(attr).Access = AttributeAccess.Hidden
        else:
            Product.Attr(attr).Access = AttributeAccess.ReadOnly
Nonr2qattr = ["ATT_CBECASLOOP","ATT_CBECOMLOOP","ATT_CBECAUXFUN"]
Nonr2qcol = {"CB_EC_migration_to_C300_UHIO_Configuration_Cont":["CB_EC_If_terminal_blocks_are_required_for_spare_UIO_points"]}
isR2Qquote = True if Quote.GetCustomField("isR2QRequest").Content else False
if isR2Qquote:
    Product.Attr('R2QRequest').AssignValue('Yes')
    Product.Attr("R2Q_QuoteNumber").AssignValue(str(Quote.CompositeNumber))
    hideAttr(Nonr2qattr,"hide")
    hideContainerColumns(Nonr2qcol,'Hidden')
else:
    hideAttr(Nonr2qattr,"read")