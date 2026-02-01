isR2Qquote = True if Quote.GetCustomField("isR2QRequest").Content else False
Checkproduct = Product.ParseString('<*CTX(Product.RootProduct.PartNumber)*>')
container_software = Product.GetContainerByName('PLC_Software_Question_Cont')
container_labour = Product.GetContainerByName('PLC_Labour_Details')
if isR2Qquote:
    Product.Attr('R2QRequest').AssignValue('Yes')
    Product.Attr("R2Q_QuoteNumber").AssignValue(str(Quote.CompositeNumber))
    container_software = Product.GetContainerByName('PLC_Software_Question_Cont')
    if container_software.Rows:
        container_software.Rows[0].GetColumnByName('PLC_Cabinet_Required_Racks_Mounting').SetAttributeValue('Yes')
    container_labour = Product.GetContainerByName('PLC_Labour_Details')
    if container_labour.Rows and Quote.GetCustomField('R2QFlag').Content == "Yes" and Checkproduct == "Migration":
        container_labour.Rows[0].GetColumnByName('PLC_Process_Type').SetAttributeValue('Continuous')
        container_labour.Rows[0].GetColumnByName('PLC_Process_Type').Value='Continuous'