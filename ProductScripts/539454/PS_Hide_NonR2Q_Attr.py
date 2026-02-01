isR2Qquote = True if Quote.GetCustomField("isR2QRequest").Content else False
if isR2Qquote:
    Product.Attr("OPM_RESS_Server_configuration").SelectDisplayValue("Physical")
    Product.Attr("ATT_OPMNUMRESS").AssignValue('0')
    