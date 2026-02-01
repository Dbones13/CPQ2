get_cf_isr2q=Quote.GetCustomField('IsR2QRequest').Content
if get_cf_isr2q == 'Yes':
	Trace.Write('PS- Hide_general_attr->')
	Product.Attr('HCI_PHD_BGP_SUPPORT').AssignValue('1')
	Product.Attr("HCI_PHD_BGP_SUPPORT").Access = AttributeAccess.Hidden
	Product.Attr('SC_Central_Managed_SQL').SelectDisplayValue('No')
	Product.Attr("SC_Central_Managed_SQL").Access = AttributeAccess.Hidden
	Product.Attr('Trace_Software_Do_you_need_hardware').SelectDisplayValue('No')
	Product.Attr("Trace_Software_Do_you_need_hardware").Access = AttributeAccess.Hidden
	#ScriptExecutor.ExecuteGlobal('R2Q_HCI_EDM_ATTRHIDE')