nonR2QAttr = ["FSC_SM_IO_SIC_Cable"]

isR2QProduct = True if Quote.GetCustomField("isR2QRequest").Content == "Yes" else False

if isR2QProduct:
    Product.Attr('R2QRequest').AssignValue('Yes')
    Product.Attr("R2Q_QuoteNumber").AssignValue(str(Quote.CompositeNumber))
    Trace.Write(Product.Attr('FSC_SM_IO_SIC_Cable').Access)
    for contColumn in nonR2QAttr:
        Product.Attr('FSC_SM_IO_SIC_Cable').Access = AttributeAccess.Hidden