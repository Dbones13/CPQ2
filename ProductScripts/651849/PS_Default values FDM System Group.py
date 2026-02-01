#Product.SelectAttrValues('FDM Server Device Adder Blocks (0-16000)', '0')
Product.Attr('R2QRequest').AssignValue('Yes')
Product.Attr("R2Q_QuoteNumber").AssignValue(str(Quote.CompositeNumber))
Product.Attr('FDM Server Device Adder Blocks (0-16000)').AssignValue('0')
Product.Attr('FDM Audit Trail Blocks (0-16000)').AssignValue('0')
Product.Attr('FDM Server Network Interface License (0-24)').AssignValue('0')
Product.Attr('FDM_Audit_Trail_Blocks(0-4000)').AssignValue('0')
Product.Attr('FDM_MUX_Monitoring_License(0-6)').AssignValue('0')
Product.Attr('FDM_Server_Device_Adder_Blocks(0-4000)').AssignValue('0')
Product.Attr('FDM_Server_Network_Interface_License(0-5)').AssignValue('0')
Product.Attr('FDM_Client_License(0-4)').AssignValue('0')
Product.Attr('FDM MUX Monitoring License (0-1)').AssignValue('0')
Product.Attr('FDM Client License (0-10)').AssignValue('0')
Product.Attr('FDM Client Station Qty (0-10)').AssignValue('0')
Product.Attr('FDM_Displays (Server) (0-1)').AssignValue('1')
Product.Attr('FDM Client Station Qty (0-10)').Access = AttributeAccess.Hidden