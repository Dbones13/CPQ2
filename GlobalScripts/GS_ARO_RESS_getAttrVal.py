def getERGAttrVal(Product, part):
	ERG_Sys_Req=Product.Attr('Experion Remote Gateway (ERG) System Required').GetValue()
	erg_swRel=Product.Attr('ERG_Software_Release').GetValue()
	#CXCPQ-112913
	RESS_System_Required=Product.Attr('RESS_System_Required').GetValue()
	RESS_Sw_Rel=Product.Attr('RESS_Experion_Software_Release').GetValue()
	RESS_server_req_Phy_hw=Product.Attr('RESS_server_require_Physical_hardware').GetValue()
	RESS_Tpm=Product.Attr('RESS_Trusted_Platform_Module').GetValue()
	RESS_Node_Supplier=Product.Attr('RESS_Node_Supplier_(Server)').GetValue()
	RESS_Server_Node_Type=Product.Attr('RESS_Server_Node_Type').GetValue()
	erg_nodeTyp=Product.Attr('ERG_Server_Node_Type').GetValue()
	erg_supl=Product.Attr('Node_Suplier(ERG Server)').GetValue()
	erg_trstPltf=Product.Attr('Trusted_Platform_Module(TPM)').GetValue()
	aro_release=Product.Attr('ARO_Experion_Software_Release').GetValue()
	ARO_server_req_Phy_hw=Product.Attr('ARO_server_require_Physical_hardware').GetValue()
	Server_Node_Type=Product.Attr('ARO_Server_Node_Type').GetValue()
	Node_Supplier=Product.Attr('ARO_Node_Supplier').GetValue()
	ARO_Gateway_req_Phy_hw=Product.Attr('ARO_Gateway_require_Physical_hardware').GetValue()
	Server_Node_Type2=Product.Attr('ARO_Server_Node_Type_GW').GetValue()
	Node_Supplier2=Product.Attr('ARO_Node_Supplier_GW').GetValue()
	RESS_server_display_size = Product.Attr('RESS_Display_Size').GetValue()
	RESS_server_display_supplier = Product.Attr('RESS_Display_Supplier').GetValue()
	RESS_client_display_size = Product.Attr('Display_Size').GetValue()
	RESS_client_display_supplier = Product.Attr('Display_Supplier_RESS').GetValue()
	#CXCPQ-112913
	if part in ('TPFPW241', 'TPFPD211200','TPFPD211100'):
		erg_cb_count=int(Product.Attr('Displays (ERG CB Server) (0-1)').GetValue()) if Product.Attr('Displays (ERG CB Server) (0-1)').GetValue() not in (None,'') else 0
		erg_count=int(Product.Attr('Displays(ERG Server)(0-1)').GetValue()) if Product.Attr('Displays(ERG Server)(0-1)').GetValue() not in (None,'') else 0
		erg_cb_size=Product.Attr('Display Size (ERG CB Server)').GetValue()
		erg_size=Product.Attr('Display_Size(ERG Server)').GetValue()
		erg_cb_supl=Product.Attr('Display Supplier (ERG CB Server)').GetValue()
		total_qty = 0
		client_qty = 0
		server_qty = 1 if RESS_server_display_size == '24 inch NTS NEC' and RESS_server_display_supplier == 'Honeywell' else 0
		if RESS_client_display_size == '24 inch NTS NEC' and RESS_client_display_supplier == 'Honeywell':
			client_qty = (int(Product.Attr('Client_Qty').GetValue()) * int(Product.Attr('Display_Qty_4').GetValue())) if Product.Attr('Multiwindow_support').GetValue() == 'Yes' else (int(Product.Attr('Client_Qty').GetValue()) * int(Product.Attr('Display_Qty').GetValue()))
		total_qty = server_qty + client_qty
		if part == 'TPFPW241':
			return ERG_Sys_Req, erg_cb_count, erg_count, erg_cb_size, erg_size, erg_cb_supl, erg_supl, total_qty
		return ERG_Sys_Req, erg_cb_count, erg_count, erg_cb_size, erg_size, erg_cb_supl, erg_supl
	elif part in ('EPCOAS22'):
		erg_cb_nodeTyp=Product.Attr('ERG CB Server Node Type').GetValue()
		erg_cb_supl=Product.Attr('Node Supplier (ERG CB Server)').GetValue()
		erg_cb_trstPltf=Product.Attr('Trusted Platform Module (TPM)').GetValue()
		return RESS_System_Required,RESS_Sw_Rel,RESS_server_req_Phy_hw,RESS_Tpm,RESS_Node_Supplier,RESS_Server_Node_Type,ERG_Sys_Req,erg_swRel,erg_cb_nodeTyp,erg_nodeTyp,erg_cb_supl,erg_supl,erg_cb_trstPltf,erg_trstPltf,aro_release,ARO_server_req_Phy_hw,Server_Node_Type,Node_Supplier,ARO_Gateway_req_Phy_hw,Server_Node_Type2,Node_Supplier2
	elif part == 'MZPCSR03': #CXCPQ-112913
		return RESS_System_Required,RESS_Sw_Rel,RESS_server_req_Phy_hw,RESS_Tpm,RESS_Node_Supplier,RESS_Server_Node_Type,ERG_Sys_Req,erg_swRel,erg_nodeTyp,erg_supl,erg_trstPltf #CXCPQ-112913
	elif part in ('MZPCST02','MZPCST82'): #CXCPQ-112913 removed MZPCSR03 from this elif
		return ERG_Sys_Req,erg_swRel,erg_nodeTyp,erg_supl,erg_trstPltf