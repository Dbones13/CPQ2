if Quote.GetCustomField('IsR2QRequest').Content == "Yes":
    Product.Attr('HCI_PHD_BGP_SUPPORT').AssignValue('')
    Product.Attr("HCI_PHD_BGP_SUPPORT").Access = AttributeAccess.Hidden
    Product.Attr('SC_Central_Managed_SQL').SelectDisplayValue('No')
    Product.Attr("SC_Central_Managed_SQL").Access = AttributeAccess.Hidden
    Product.Attr('Trace_Software_Do_you_need_hardware').SelectDisplayValue('No')
    Product.Attr("Trace_Software_Do_you_need_hardware").Access = AttributeAccess.Hidden
else:
    Product.Attr("HCI_PHD_BGP_SUPPORT").Access = AttributeAccess.Editable
    Product.Attr('HCI_PHD_BGP_SUPPORT').AssignValue('1')
    Product.Attr("SC_Central_Managed_SQL").Access = AttributeAccess.Editable
    Product.Attr("Trace_Software_Do_you_need_hardware").Access = AttributeAccess.Editable
Trace.Write('last-hid--')