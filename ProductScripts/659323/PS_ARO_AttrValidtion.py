#Trace.Write("-PS_ARO_AttrValidtion-")
if Product.Name == 'Experion ARO, RESS & ERG Group' and Product.Attr('ARO_System_Required').GetValue() == 'Yes':
	#Trace.Write(str(Product.Attr('ARO_Remote_Client_Connection').GetValue())+"--test--111--PS_ARO_AttrValidtion--->"+str(Product.Attr('ARO_Multi_Window_Client_Qty').GetValue()))
	if str(Product.Attr('ARO_Experion_Server_Location').GetValue())=='Experion PKS Server':
		Product.Attr("ARO_new_Flex_Station_licenses_required").Access = AttributeAccess.Editable
	else:
		Product.Attr("ARO_new_Flex_Station_licenses_required").Access = AttributeAccess.Hidden
	if str(Product.Attr('ARO_Experion_Server_Location').GetValue())=='Server TPS':
		Product.Attr("ARO_new_Console_Station_Extension_License").Access = AttributeAccess.Editable
	else:
		Product.Attr("ARO_new_Console_Station_Extension_License").Access = AttributeAccess.Hidden
	if str(Product.Attr('ARO_Remote_Client_Connection').GetValue())=='Microsoft Remote Desktop client':
		Product.AllowAttr("AR0_Multi_Window_support")
		if str(Product.Attr('AR0_Multi_Window_support').GetValue()) == '':
			Product.Attr('AR0_Multi_Window_support').SelectDisplayValue('No')
			Product.Attr('AR0_Multi_Window_support').AssignValue('No')
		#Product.Attr("AR0_Multi_Window_support").Access = AttributeAccess.Editable
		#Product.AllowAttr("ARO_Client_Qty_20")
	else:
		Product.DisallowAttr("AR0_Multi_Window_support")
		#Product.Attr("AR0_Multi_Window_support").Access = AttributeAccess.Hidden
		#Product.DisallowAttr("ARO_Client_Qty_20")
		#Product.Attr("AR0_Multi_Window_support").Access = AttributeAccess.Hidden'''
	if str(Product.Attr('ARO_Remote_Client_Connection').GetValue())=='Remote Desktop Web client':
		Product.AllowAttr("ARO_Client_Qty_40")
		Product.DisallowAttr("ARO_Client_Qty_20")
		Product.DisallowAttr("ARO_Client_Qty_15")
		Product.DisallowAttr("ARO_Multi_Window_Client_Qty")
	else:
		Product.DisallowAttr("ARO_Client_Qty_40")
	if str(Product.Attr('ARO_Remote_Client_Connection').GetValue())=='Remote App client':
		Product.AllowAttr("ARO_Client_Qty_100")
		Product.DisallowAttr("ARO_Client_Qty_20")
		Product.DisallowAttr("ARO_Client_Qty_15")
		Product.DisallowAttr("ARO_Multi_Window_Client_Qty")
	else:
		Product.DisallowAttr("ARO_Client_Qty_100")
	if str(Product.Attr('AR0_Multi_Window_support').GetValue())=='Yes':
		Product.AllowAttr("ARO_Multi_Window_Client_4")
	else:
		Product.DisallowAttr("ARO_Multi_Window_Client_4")
	if str(Product.Attr('ARO_Remote_Client_Connection').GetValue())=='Microsoft Remote Desktop client' and str(Product.Attr('AR0_Multi_Window_support').GetValue())=='No':
		Product.AllowAttr("ARO_Client_Qty_20")
		Product.DisallowAttr("ARO_Multi_Window_Client_Qty")
		Product.DisallowAttr("ARO_Client_Qty_15")

	if str(Product.Attr('ARO_Remote_Client_Connection').GetValue())=='Microsoft Remote Desktop client' and str(Product.Attr('AR0_Multi_Window_support').GetValue())=='Yes':
		Product.AllowAttr("ARO_Multi_Window_Client_Qty")
		Product.AllowAttr("ARO_Client_Qty_15")
		Product.DisallowAttr("ARO_Client_Qty_20")
	#if str(Product.Attr('ARO_Remote_Client_Connection').GetValue())=='Microsoft Remote Desktop client' and str(Product.Attr('ARO_Multi_Window_Client_Qty').GetValue()) > '0':
	#    Product.Attr("AR0_Multi_Window_support").Access = AttributeAccess.Editable
	#else:
	#    Product.Attr("AR0_Multi_Window_support").Access = AttributeAccess.Hidden