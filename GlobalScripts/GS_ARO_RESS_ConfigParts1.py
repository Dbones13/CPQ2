#CXCPQ-49175
def getpart_EPCOAS16(Product):
	var43=var40=var41=var42=0
	ARO_System_Required=Product.Attr('ARO_System_Required').GetValue()
	RESS_System_Required=Product.Attr('RESS_System_Required').GetValue()
	if Product.Name == "Experion ARO, RESS & ERG Group":
		Aro_Software=Product.Attr('ARO_Experion_Software_Release').GetValue()
		#Aro_Software1=Product.Attr('ARO_Experion_Software_Release').GetValue()
		#Trace.Write(Aro_Software1)
		Aro_Software2=Product.Attr('RESS_Experion_Software_Release').GetValue()
		#Trace.Write(ARO_Software2)
		Node_Supplier=Product.Attr('ARO_Node_Supplier').GetValue()
		Node_Supplier2=Product.Attr('ARO_Node_Supplier_GW').GetValue()
		#Trace.Write(Node_Supplier2)
		Node_Supplier3=Product.Attr('RESS_Node_Supplier_(Server)').GetValue()
		#Trace.Write(Node_Supplier3)
		Server_Node_Type=Product.Attr('ARO_Server_Node_Type').GetValue()
		Server_Node_Type2=Product.Attr('ARO_Server_Node_Type_GW').GetValue()
		#Trace.Write(Server_Node_Type2)
		Server_Node_Type3=Product.Attr('RESS_Server_Node_Type').GetValue()
		#Trace.Write(Server_Node_Type3)
		if ARO_System_Required =="Yes" and (Aro_Software=="R510" or Aro_Software=="R511") and Node_Supplier=="Honeywell" and (Server_Node_Type=="SVR_PER_HP_Rack_RAID5" or Server_Node_Type=="SVR_PER_DELL_Rack_RAID1_RUG" or Server_Node_Type=="SVR_PER_DELL_Tower_RAID1" or Server_Node_Type=="SVR_PER_DELL_Rack_RAID1" or Server_Node_Type=="SVR_STD_DELL_Tower_RAID1" or Server_Node_Type=="SVR_STD_DELL_Rack_RAID1" or Server_Node_Type=="SVR_PER_DELL_Rack_RAID5") :
			var40=1
		#Trace.Write(var40)
		if ARO_System_Required =="Yes" and (Aro_Software=="R510" or Aro_Software=="R511") and Node_Supplier2=="Honeywell" and (Server_Node_Type2=="SVR_PER_HP_Rack_RAID5" or Server_Node_Type2=="SVR_PER_DELL_Rack_RAID1_RUG" or Server_Node_Type2=="SVR_PER_DELL_Tower_RAID1" or Server_Node_Type2=="SVR_PER_DELL_Rack_RAID1" or Server_Node_Type2=="SVR_STD_DELL_Tower_RAID1" or Server_Node_Type2=="SVR_STD_DELL_Rack_RAID1" or Server_Node_Type2=="SVR_PER_DELL_Rack_RAID5"):
			var41=1
		#Trace.Write(var41)
		if RESS_System_Required == "Yes" and (Aro_Software2=="R510" or Aro_Software2=="R511") and Node_Supplier3=="Honeywell" and (Server_Node_Type3=="SVR_PER_HP_Rack_RAID5" or Server_Node_Type3=="SVR_PER_DELL_Rack_RAID1_RUG" or Server_Node_Type3=="SVR_PER_DELL_Tower_RAID1" or Server_Node_Type3=="SVR_PER_DELL_Rack_RAID1" or Server_Node_Type3=="SVR_STD_DELL_Tower_RAID1" or Server_Node_Type3=="SVR_STD_DELL_Rack_RAID1" or Server_Node_Type3=="SVR_PER_DELL_Rack_RAID5"):
			var42=1
		#Trace.Write(var42)
		var43=var40+var41+var42
	return(var43)
#Trace.Write(getpart_EPCOAS16(Product))
#49185

#CXCPQ-112914 new function
def getpart_EPCOAW21(Product):
	Qty = 0
	RESS_System_Required=Product.Attr('RESS_System_Required').GetValue()
	RESS_Sw_Rel=Product.Attr('RESS_Experion_Software_Release').GetValue()
	RESS_remote_client_stn_hw=Product.Attr('Remote_client_station_hardware').GetValue()
	RESS_Client_Qty = Product.Attr("Client_Qty").GetValue()
	RESS_Client_Node_Type=Product.Attr('Client_Node_Type').GetValue()
	RESS_Client_Node_Supplier=Product.Attr('Client_Node_Supplier').GetValue()
	if RESS_System_Required=="Yes" and RESS_Sw_Rel=="R530" and RESS_remote_client_stn_hw =="Yes" and int(RESS_Client_Qty)>0 and RESS_Client_Node_Supplier =="Honeywell" and RESS_Client_Node_Type:
		Qty = int(float(RESS_Client_Qty))
	return Qty
#CXCPQ-112914

def getpart_MZSQLCL4(Product):
	server_qnt = station_qnt = 0
	QNT = 0
	# server
	erg_required = Product.Attr('Experion Remote Gateway (ERG) System Required').GetValue()
	aro_node_type = Product.Attr('ARO_Server_Node_Type').GetValue()
	Trace.Write(aro_node_type)
	aro_gw_node_type = Product.Attr('ARO_Server_Node_Type_GW').GetValue()
	Trace.Write(aro_gw_node_type)
	ress_node_type = Product.Attr('RESS_Server_Node_Type').GetValue()
	Trace.Write(ress_node_type)
	erg_node_type = Product.Attr('ERG_Server_Node_Type').GetValue()
	Trace.Write(erg_node_type)
	erg_cb_node_type = Product.Attr('ERG CB Server Node Type').GetValue()
	Trace.Write(erg_cb_node_type)
	aro_release=Product.Attr('ARO_Experion_Software_Release').GetValue()
	ARO_server_req_Phy_hw=Product.Attr('ARO_server_require_Physical_hardware').GetValue()
	ARO_Gateway_req_Phy_hw=Product.Attr('ARO_Gateway_require_Physical_hardware').GetValue()

	# Hardware
	stations_hardware = ["STN_PER_DELL_Tower_RAID1","STN_PER_DELL_Rack_RAID1","STN_PER_HP_Tower_RAID1","STN_STD_DELL_Tower_NonRAID"]
	erg_hardware = ["SVR_STD_DELL_Tower_RAID1","SVR_STD_DELL_Rack_RAID1","SVR_PER_DELL_Tower_RAID1","SVR_PER_DELL_Rack_RAID1_XE"]

	if ress_node_type: #if ress_node_type in server_hardware #CXCPQ-112914
		server_qnt += 1
		Trace.Write("server quantity3"+str(server_qnt))
	if erg_required == 'Yes' and erg_node_type in erg_hardware:
		server_qnt += 1
		Trace.Write("server quantity4"+str(server_qnt))
	if erg_required == 'Yes' and erg_cb_node_type in erg_hardware:
		server_qnt += 1
		Trace.Write("server quantity5"+str(server_qnt))

	if aro_release=="R520" or aro_release=="R530":
		if ARO_server_req_Phy_hw=="Yes" and aro_node_type:
			server_qnt += 1
		if ARO_Gateway_req_Phy_hw=="Yes" and aro_gw_node_type:
			server_qnt += 1
	# station
	additional_server_Aro = Product.Attr("Additional_Stations_for_ARO_WS").GetValue()
	additional_server_RESS = Product.Attr("RESS_Additional_Stations").GetValue()
	ARO_Station_Node_WS =  Product.Attr('ARO_Station_Node_WS').GetValue()
	RESS_Server_Node_Type = Product.Attr('RESS_Staton_Node').GetValue()
	RESS_Client_Qty = Product.Attr("Client_Qty").GetValue() #CXCPQ-112914
	Trace.Write(RESS_Server_Node_Type)
	if ARO_Station_Node_WS in stations_hardware:
		station_qnt += int(additional_server_Aro)
		Trace.Write("station1"+str(station_qnt))
	if RESS_Client_Qty: #RESS_Server_Node_Type in stations_hardware CXCPQ-112914
		station_qnt += int(float(RESS_Client_Qty)) #additional_server_RESS CXCPQ-112914
		Trace.Write("station2"+str(station_qnt))

	QNT = int(station_qnt) + int(server_qnt)
	return (QNT)
def getpart_EP(Product):
	ERG_Sys_Req=Product.Attr('Experion Remote Gateway (ERG) System Required').GetValue()
	EP_PKS530_ESD=EP_PKS530=EP_BRM520_ESD=EP_BRM520=0
	if ERG_Sys_Req=="Yes":
		ERG_Sft_Rel=Product.Attr('ERG_Software_Release').GetValue()
		ERG_BMed_Del=Product.Attr('ERG_Experion_Base_Media_Delivery').GetValue()
		ERG_BkpRes_Rel=Product.Attr('ERG_Experion_Backup_and_Restore_Release').GetValue()
		ERG_BkpRMed_Del=Product.Attr('ERG_Experion_Backup_and_Restore_Media_Delivery').GetValue()
		EBR_Req_ERG_CB=Product.Attr('EBR_Required_ERG(CB Server)').GetValue()
		EBR_Req_ERG_Ser=Product.Attr('EBR_Required_ERG(Server)').GetValue()
		if ERG_Sft_Rel=="R530" and ERG_BMed_Del=="Electronic Download":
			EP_PKS530_ESD=1
		elif ERG_Sft_Rel=="R530" and ERG_BMed_Del=="Physical Delivery":
			EP_PKS530=1
		if ERG_BkpRes_Rel=="R520" and ERG_BkpRMed_Del=="Electronic Download" and (EBR_Req_ERG_CB=="Yes" or EBR_Req_ERG_Ser=="Yes"):
			EP_BRM520_ESD=1
		elif ERG_BkpRes_Rel=="R520" and ERG_BkpRMed_Del=="Physical Delivery" and (EBR_Req_ERG_CB=="Yes" or EBR_Req_ERG_Ser=="Yes"):
			EP_BRM520=1
	return EP_PKS530_ESD,EP_PKS530,EP_BRM520_ESD,EP_BRM520
#Trace.Write(getpart_MZSQLCL4(Product))
def getpart_MZ_PCSR01_PCSR81(Product):
	ERG_Sys_Req=Product.Attr('Experion Remote Gateway (ERG) System Required').GetValue()
	MZ_PCSR01=MZ_PCSR81=0
	if ERG_Sys_Req=="Yes":
		ERG_Sft_Rel=Product.Attr('ERG_Software_Release').GetValue()
		erg_cb_node_type = Product.Attr('ERG CB Server Node Type').GetValue()
		node_supp_ergcb = Product.Attr('Node Supplier (ERG CB Server)').GetValue()
		tru_pla_Mod = Product.Attr('Trusted Platform Module (TPM)').GetValue()
		erg_node_type = Product.Attr('ERG_Server_Node_Type').GetValue()
		node_supp_erg = Product.Attr('Node_Suplier(ERG Server)').GetValue()
		tru_pla_Mod_eg = Product.Attr('Trusted_Platform_Module(TPM)').GetValue()
		if ERG_Sft_Rel=='R530' and erg_cb_node_type=='SVR_STD_DELL_Rack_RAID1' and node_supp_ergcb=='Honeywell' and tru_pla_Mod=='Yes':
			MZ_PCSR01+=1
		elif ERG_Sft_Rel=='R530' and erg_cb_node_type=='SVR_STD_DELL_Rack_RAID1' and node_supp_ergcb=='Honeywell' and tru_pla_Mod=='No':
			MZ_PCSR81+=1
		if ERG_Sft_Rel=='R530' and erg_node_type=='SVR_STD_DELL_Rack_RAID1' and node_supp_erg=='Honeywell' and tru_pla_Mod_eg=='Yes':
			MZ_PCSR01+=1
		elif ERG_Sft_Rel=='R530' and erg_node_type=='SVR_STD_DELL_Rack_RAID1' and node_supp_erg=='Honeywell' and tru_pla_Mod_eg=='No':
			MZ_PCSR81+=1
	return MZ_PCSR01,MZ_PCSR81

def getpart_TPFPW272(Product):
	server_qnt = cb_server_qnt = 0
	QNT = 0
	erg_required = Product.Attr('Experion Remote Gateway (ERG) System Required').GetValue()
	Trace.Write(erg_required)
	server_qnt = Product.Attr('Displays(ERG Server)(0-1)').GetValue()
	Trace.Write(server_qnt)
	erg_size = Product.Attr('Display_Size(ERG Server)').GetValue()
	Trace.Write(erg_size)
	erg_supplier = Product.Attr('Display_Supplier(ERG Server)').GetValue()
	Trace.Write(erg_supplier)
	cb_server_qnt = Product.Attr('Displays (ERG CB Server) (0-1)').GetValue()
	Trace.Write(cb_server_qnt)
	cb_erg_size = Product.Attr('Display Size (ERG CB Server)').GetValue()
	Trace.Write(cb_erg_size)
	cb_erg_supplier = Product.Attr('Display Supplier (ERG CB Server)').GetValue()
	Trace.Write(cb_erg_supplier)
	if erg_required == 'Yes' and int(server_qnt) > 0 and erg_size == '27 inch NTS DELL' and erg_supplier == 'Honeywell':
		QNT += int(server_qnt)
	if erg_required == 'Yes' and int(cb_server_qnt) > 0 and cb_erg_size == '27 inch NTS DELL' and cb_erg_supplier == 'Honeywell':
		QNT += int(cb_server_qnt)
	RESS_System_Required = Product.Attr('RESS_System_Required').GetValue()
	RESS_server_display_size = Product.Attr('RESS_Display_Size').GetValue()
	RESS_server_display_supplier = Product.Attr('RESS_Display_Supplier').GetValue()
	RESS_client_display_size = Product.Attr('Display_Size').GetValue()
	RESS_client_display_supplier = Product.Attr('Display_Supplier_RESS').GetValue()
	total_qty = 0
	client_qty = 0
	final_qty = 0
	if RESS_System_Required == 'Yes' :
		server_qty = 1 if RESS_server_display_size == '27 inch NTS DELL' and RESS_server_display_supplier == 'Honeywell' else 0
		if RESS_client_display_size == '27 inch NTS DELL' and RESS_client_display_supplier == 'Honeywell':
			client_qty = (int(Product.Attr('Client_Qty').GetValue()) * int(Product.Attr('Display_Qty_4').GetValue())) if Product.Attr('Multiwindow_support').GetValue() == 'Yes' else (int(Product.Attr('Client_Qty').GetValue()) * int(Product.Attr('Display_Qty').GetValue()))
		total_qty = server_qty + client_qty
	final_qty = QNT + total_qty
	return(final_qty)

def getpart_TPFPW242(Product):
	server_qnt = cb_server_qnt = 0
	QNT = 0
	erg_required = Product.Attr('Experion Remote Gateway (ERG) System Required').GetValue()
	Trace.Write(erg_required)
	server_qnt = Product.Attr('Displays(ERG Server)(0-1)').GetValue()
	Trace.Write(server_qnt)
	erg_size = Product.Attr('Display_Size(ERG Server)').GetValue()
	Trace.Write(erg_size)
	erg_supplier = Product.Attr('Display_Supplier(ERG Server)').GetValue()
	Trace.Write(erg_supplier)
	cb_server_qnt = Product.Attr('Displays (ERG CB Server) (0-1)').GetValue()
	Trace.Write(cb_server_qnt)
	cb_erg_size = Product.Attr('Display Size (ERG CB Server)').GetValue()
	Trace.Write(cb_erg_size)
	cb_erg_supplier = Product.Attr('Display Supplier (ERG CB Server)').GetValue()
	Trace.Write(cb_erg_supplier)
	if erg_required == 'Yes' and int(server_qnt) > 0 and erg_size == '24 inch NTS DELL' and erg_supplier == 'Honeywell':
		QNT += int(server_qnt)
	if erg_required == 'Yes' and int(cb_server_qnt) > 0 and cb_erg_size == '24 inch NTS DELL' and cb_erg_supplier == 'Honeywell':
		QNT += int(cb_server_qnt)
	RESS_System_Required = Product.Attr('RESS_System_Required').GetValue()
	RESS_server_display_size = Product.Attr('RESS_Display_Size').GetValue()
	RESS_server_display_supplier = Product.Attr('RESS_Display_Supplier').GetValue()
	RESS_client_display_size = Product.Attr('Display_Size').GetValue()
	RESS_client_display_supplier = Product.Attr('Display_Supplier_RESS').GetValue()
	total_qty = 0
	client_qty = 0
	final_qty = 0
	if RESS_System_Required == 'Yes' :
		server_qty = 1 if RESS_server_display_size == '24 inch NTS DELL' and RESS_server_display_supplier == 'Honeywell' else 0
		if RESS_client_display_size == '24 inch NTS DELL' and RESS_client_display_supplier == 'Honeywell':
			client_qty = (int(Product.Attr('Client_Qty').GetValue()) * int(Product.Attr('Display_Qty_4').GetValue())) if Product.Attr('Multiwindow_support').GetValue() == 'Yes' else (int(Product.Attr('Client_Qty').GetValue()) * int(Product.Attr('Display_Qty').GetValue()))
		total_qty = server_qty + client_qty
	final_qty = QNT + total_qty
	return(final_qty)

def getpart_EPBRSE06(Product):
	QNT = 0
	erg_required = Product.Attr('Experion Remote Gateway (ERG) System Required').GetValue()
	erg_backup_restore_rel = Product.Attr('ERG_Experion_Backup_and_Restore_Release').GetValue()
	Trace.Write(erg_backup_restore_rel)
	ebr_required_erg = Product.Attr('EBR_Required_ERG(Server)').GetValue()
	Trace.Write(ebr_required_erg)
	cb_ebr_required_erg = Product.Attr('EBR_Required_ERG(CB Server)').GetValue()
	Trace.Write(cb_ebr_required_erg)

	if erg_required == 'Yes' and erg_backup_restore_rel == 'R520':
		if ebr_required_erg == 'Yes':
			QNT += 1
			Trace.Write("QNT1-->>"+str(QNT))
		if cb_ebr_required_erg == 'Yes':
			QNT += 1
			Trace.Write("QNT2-->>"+str(QNT))

	return QNT

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
	#CXCPQ-112913
	ARO_System_Required=Product.Attr('ARO_System_Required').GetValue()
	if part in ('TPFPW241','TPFPD211200','TPFPD211100'):
		erg_cb_count=int(Product.Attr('Displays (ERG CB Server) (0-1)').GetValue()) if Product.Attr('Displays (ERG CB Server) (0-1)').GetValue() not in (None,'') else 0
		erg_count=int(Product.Attr('Displays(ERG Server)(0-1)').GetValue()) if Product.Attr('Displays(ERG Server)(0-1)').GetValue() not in (None,'') else 0
		erg_cb_size=Product.Attr('Display Size (ERG CB Server)').GetValue()
		erg_size=Product.Attr('Display_Size(ERG Server)').GetValue()
		erg_cb_supl=Product.Attr('Display Supplier (ERG CB Server)').GetValue()
		return ERG_Sys_Req, erg_cb_count, erg_count, erg_cb_size, erg_size, erg_cb_supl, erg_supl
	elif part in ('EPCOAS22'):
		erg_cb_nodeTyp=Product.Attr('ERG CB Server Node Type').GetValue()
		erg_cb_supl=Product.Attr('Node Supplier (ERG CB Server)').GetValue()
		erg_cb_trstPltf=Product.Attr('Trusted Platform Module (TPM)').GetValue()
		return RESS_System_Required,RESS_Sw_Rel,RESS_server_req_Phy_hw,RESS_Tpm,RESS_Node_Supplier,RESS_Server_Node_Type,ERG_Sys_Req,erg_swRel,erg_cb_nodeTyp,erg_nodeTyp,erg_cb_supl,erg_supl,erg_cb_trstPltf,erg_trstPltf
	elif part == 'MZPCSR03': #CXCPQ-112913
		return ARO_System_Required,RESS_System_Required,RESS_Sw_Rel,RESS_server_req_Phy_hw,RESS_Tpm,RESS_Node_Supplier,RESS_Server_Node_Type,ERG_Sys_Req,erg_swRel,erg_nodeTyp,erg_supl,erg_trstPltf #CXCPQ-112913
	elif part in ('MZPCST02','MZPCST82'): #CXCPQ-112913 removed MZPCSR03 from this elif
		return ERG_Sys_Req,erg_swRel,erg_nodeTyp,erg_supl,erg_trstPltf

def getpart_MZPCSR03(Product):
	var=var1=var2=var3=var4=0 #CXCPQ-112913
	if Product.Name == "Experion ARO, RESS & ERG Group":
		ARO_System_Required,RESS_System_Required,RESS_Sw_Rel,RESS_server_req_Phy_hw,RESS_Tpm,RESS_Node_Supplier,RESS_Server_Node_Type,ERG_Sys_Req,erg_swRel,erg_nodeTyp,erg_supl,erg_trstPltf=getERGAttrVal(Product, 'MZPCSR03') #CXCPQ-112913
		if ERG_Sys_Req=='Yes' and erg_swRel=='R530' and erg_nodeTyp in ('SVR_PER_DELL_Rack_RAID1_XE') and erg_supl=='Honeywell' and erg_trstPltf=='Yes':
			var1=1
		if RESS_System_Required == "Yes" and RESS_Sw_Rel in ('R520','R530') and RESS_server_req_Phy_hw == "Yes" and RESS_Tpm == "Yes" and RESS_Node_Supplier == "Honeywell" and RESS_Server_Node_Type == "SVR_PER_DELL_Rack_RAID1_XE": #CXCPQ-112913
			var2=1
		if ARO_System_Required == 'Yes': # CXCPQ-112861
			ARO_server_req_Phy_hw=Product.Attr('ARO_server_require_Physical_hardware').GetValue()
			Server_Node_Type=Product.Attr('ARO_Server_Node_Type').GetValue()
			Node_Supplier=Product.Attr('ARO_Node_Supplier').GetValue()
			Aro_Tpm=Product.Attr('ARO_Trusted_Platform_Module').GetValue()
			ARO_Gateway_req_Phy_hw=Product.Attr('ARO_Gateway_require_Physical_hardware').GetValue()
			Server_Node_Type2=Product.Attr('ARO_Server_Node_Type_GW').GetValue()
			Node_Supplier2=Product.Attr('ARO_Node_Supplier_GW').GetValue()
			Aro_Tpm1=Product.Attr('ARO_Trusted_Platform_Module_GW').GetValue()
			if Node_Supplier == 'Honeywell' and ARO_server_req_Phy_hw == 'Yes' and Server_Node_Type == 'SVR_PER_DELL_Rack_RAID1_XE' and Aro_Tpm == 'Yes':
				var4=1
				Trace.Write("---PCSR03---var4--->"+str(var4))
			if Node_Supplier2 == 'Honeywell' and ARO_Gateway_req_Phy_hw == 'Yes' and Server_Node_Type2 =='SVR_PER_DELL_Rack_RAID1_XE' and Aro_Tpm1 == 'Yes':
				var3=1
		var=var1+var2+var3+var4
	return(var) # CXCPQ-112913

#CXCPQ-104062
def getpart_server(Product):#MZ-PCSR05,MZ-PCSR06,MZ-PCST03,MZ-PCST04,MZ_PCSR04,MZ_PCSV85
	MZ_PCSR05=MZ_PCSR06=MZ_PCST03=MZ_PCST04=MZ_PCSR04=MZ_PCSV85=0 #CXCPQ-112913
	ARO_System_Required=Product.Attr('ARO_System_Required').GetValue()
	RESS_System_Required=Product.Attr('RESS_System_Required').GetValue()
	ERG_System_Required=Product.Attr('Experion Remote Gateway (ERG) System Required').GetValue()
	if ARO_System_Required == "Yes":
		ARO_Sw_Rel=Product.Attr('ARO_Experion_Software_Release').GetValue()
		ARO_server_req_Phy_hw=Product.Attr('ARO_server_require_Physical_hardware').GetValue()
		Server_Node_Type=Product.Attr('ARO_Server_Node_Type').GetValue()
		Node_Supplier=Product.Attr('ARO_Node_Supplier').GetValue()
		Aro_Tpm=Product.Attr('ARO_Trusted_Platform_Module').GetValue()

		ARO_Gateway_req_Phy_hw=Product.Attr('ARO_Gateway_require_Physical_hardware').GetValue()
		Server_Node_Type2=Product.Attr('ARO_Server_Node_Type_GW').GetValue()
		Node_Supplier2=Product.Attr('ARO_Node_Supplier_GW').GetValue()
		Aro_Tpm1=Product.Attr('ARO_Trusted_Platform_Module_GW').GetValue()

		if Node_Supplier == 'Honeywell' and ARO_server_req_Phy_hw == 'Yes' and Server_Node_Type == 'SVR_PER_DELL_Tower_RAID1':
			MZ_PCST04 += 1
		if Node_Supplier2 == 'Honeywell' and ARO_Gateway_req_Phy_hw == 'Yes' and Server_Node_Type2 == 'SVR_PER_DELL_Tower_RAID1':
			MZ_PCST04 += 1
		if Node_Supplier == 'Honeywell' and ARO_server_req_Phy_hw == 'Yes' and Server_Node_Type == 'SVR_PER_DELL_Rack_RAID1':
			MZ_PCSR06 += 1
		if Node_Supplier2 == 'Honeywell' and ARO_Gateway_req_Phy_hw == 'Yes' and Server_Node_Type2 == 'SVR_PER_DELL_Rack_RAID1':
			MZ_PCSR06 += 1
		if Node_Supplier == 'Honeywell' and ARO_server_req_Phy_hw == 'Yes' and Server_Node_Type == 'SVR_PER_DELL_Rack_RAID5' and Aro_Tpm == 'Yes':
			MZ_PCSR04 += 1
		if Node_Supplier2 == 'Honeywell' and ARO_Gateway_req_Phy_hw == 'Yes' and Server_Node_Type2 == 'SVR_PER_DELL_Rack_RAID5' and Aro_Tpm1 == 'Yes':
			MZ_PCSR04 += 1
		if Node_Supplier == 'Honeywell' and ARO_server_req_Phy_hw == 'Yes' and Server_Node_Type == 'SVR_PER_HP_Rack_RAID5' and Aro_Tpm == 'Yes':
			MZ_PCSV85 += 1
		if Node_Supplier2 == 'Honeywell' and ARO_Gateway_req_Phy_hw == 'Yes' and Server_Node_Type2 == 'SVR_PER_HP_Rack_RAID5' and Aro_Tpm1 == 'Yes':
			MZ_PCSV85 += 1
		if Node_Supplier2 == 'Honeywell' and ARO_Gateway_req_Phy_hw == 'Yes' and Server_Node_Type2 == 'SVR_STD_DELL_Rack_RAID1':
			MZ_PCSR05 += 1
		if Node_Supplier2 == 'Honeywell' and ARO_Gateway_req_Phy_hw == 'Yes' and Server_Node_Type2 == 'SVR_STD_DELL_Tower_RAID1':
			MZ_PCST03 += 1

		'''if ARO_Sw_Rel in ('R520','R530') and ARO_server_req_Phy_hw=="Yes" and Aro_Tpm and Node_Supplier=="Honeywell":
			if Server_Node_Type=="SVR_STD_DELL_Rack_RAID1" :
				MZ_PCSR05+=1
			elif Server_Node_Type=="SVR_PER_DELL_Rack_RAID1" :
				MZ_PCSR06+=1
			elif Server_Node_Type=="SVR_STD_DELL_Tower_RAID1" :
				MZ_PCST03+=1
			elif Server_Node_Type=="SVR_PER_DELL_Tower_RAID1" :
				MZ_PCST04+=1
		if ARO_Sw_Rel in ('R520','R530') and ARO_Gateway_req_Phy_hw=="Yes" and Aro_Tpm1 and Node_Supplier2=="Honeywell":
			if Server_Node_Type2=="SVR_STD_DELL_Rack_RAID1" :
				MZ_PCSR05+=1
			elif Server_Node_Type2=="SVR_PER_DELL_Rack_RAID1" :
				MZ_PCSR06+=1
			elif Server_Node_Type2=="SVR_STD_DELL_Tower_RAID1" :
				MZ_PCST03+=1
			elif Server_Node_Type2=="SVR_PER_DELL_Tower_RAID1" :
				MZ_PCST04+=1 '''
	if RESS_System_Required == "Yes":
		RESS_server_req_Phy_hw=Product.Attr('RESS_server_require_Physical_hardware').GetValue()
		RESS_Sw_Rel=Product.Attr('RESS_Experion_Software_Release').GetValue()

		RESS_Server_Node_Type=Product.Attr('RESS_Server_Node_Type').GetValue()
		Node_Supplier3=Product.Attr('RESS_Node_Supplier_(Server)').GetValue()
		RESS_Tpm2=Product.Attr('RESS_Trusted_Platform_Module').GetValue()
		if RESS_Sw_Rel in ('R520','R530') and RESS_server_req_Phy_hw=="Yes" and RESS_Tpm2 and Node_Supplier3=="Honeywell":
			if RESS_Server_Node_Type=="SVR_STD_DELL_Rack_RAID1" :
				MZ_PCSR05+=1
			elif RESS_Server_Node_Type=="SVR_PER_DELL_Rack_RAID1" :
				MZ_PCSR06+=1
			elif RESS_Server_Node_Type=="SVR_STD_DELL_Tower_RAID1" :
				MZ_PCST03+=1
			elif RESS_Server_Node_Type=="SVR_PER_DELL_Tower_RAID1" :
				MZ_PCST04+=1
			#CXCPQ-112913
			elif RESS_Server_Node_Type=="SVR_PER_DELL_Rack_RAID5" and RESS_Tpm2=="Yes":
				MZ_PCSR04+=1
			elif RESS_Server_Node_Type=="SVR_PER_HP_Rack_RAID5" and RESS_Tpm2=="Yes":
				MZ_PCSV85+=1
			#CXCPQ-112913
	if ERG_System_Required == "Yes":
		ERG_Sw_Rel=Product.Attr('ERG_Software_Release').GetValue()

		ERG_CB_Ser_Red=Product.Attr('ERG CB Server Redundancy').GetValue()
		ERG_CB_Server_Node_Type=Product.Attr('ERG CB Server Node Type').GetValue()
		ERG_Node_Supplier=Product.Attr('Node Supplier (ERG CB Server)').GetValue()
		ERG_TPM=Product.Attr('Trusted Platform Module (TPM)').GetValue()

		ERG_Server_Red=Product.Attr('ERG_Server_Redundancy').GetValue()
		ERG_Server_Node_Type=Product.Attr('ERG_Server_Node_Type').GetValue()
		ERG_Server_Node_Supplier=Product.Attr('Node_Suplier(ERG Server)').GetValue()
		ERG_Server_Tpm=Product.Attr('Trusted_Platform_Module(TPM)').GetValue()

		if ERG_Sw_Rel =='R530' and ERG_TPM and ERG_Node_Supplier=="Honeywell":
			if ERG_CB_Server_Node_Type=="SVR_STD_DELL_Rack_RAID1" :
				MZ_PCSR05+=1
			#elif ERG_CB_Server_Node_Type=="SVR_PER_DELL_Rack_RAID1" :
				#MZ_PCSR06+=1
			elif ERG_CB_Server_Node_Type=="SVR_STD_DELL_Tower_RAID1" :
				MZ_PCST03+=1
			elif ERG_CB_Server_Node_Type=="SVR_PER_DELL_Tower_RAID1" :
				MZ_PCST04+=1
		if ERG_Sw_Rel == 'R530' and ERG_Server_Tpm and ERG_Server_Node_Supplier=="Honeywell":
			if ERG_Server_Node_Type=="SVR_STD_DELL_Rack_RAID1" :
				MZ_PCSR05+=1
			#elif ERG_Server_Node_Type=="SVR_PER_DELL_Rack_RAID1" :
				#MZ_PCSR06+=1
			elif ERG_Server_Node_Type=="SVR_STD_DELL_Tower_RAID1" :
				MZ_PCST03+=1
			elif ERG_Server_Node_Type=="SVR_PER_DELL_Tower_RAID1" :
				MZ_PCST04+=1

	return MZ_PCSR05,MZ_PCSR06,MZ_PCST03,MZ_PCST04,MZ_PCSR04,MZ_PCSV85 #CXCPQ-112913

def getpart_AROClients(Product):
    RESS_System_Required=Product.Attr('RESS_System_Required').GetValue()
    RESS_Experion_release=Product.Attr('RESS_Experion_Software_Release').GetValue()
    RESS_Qty_Thin_clients=Product.Attr('RESS_Qty_of_Thin_clients').GetValue()
    RESS_Qty_OperatorTouchPanel=Product.Attr('RESS_OTP_hardware_&_software_required').GetValue()
    ARO_Qty_OperatorTouchPanel=Product.Attr('ARO_OTP_hardware_&_software_required').GetValue()
    ARO_System_Required=Product.Attr('ARO_System_Required').GetValue()
    Node_Supplier=Product.Attr('ARO_Client_Node_Supplier').GetValue()
    ARO_client_20 = int(Product.Attr('ARO_Client_Qty_20').GetValue() or 0)
    ARO_client_15 = int(Product.Attr('ARO_Client_Qty_15').GetValue() or 0)
    ARO_client_40 = int(Product.Attr('ARO_Client_Qty_40').GetValue() or 0)
    ARO_WindOW_Client = int(Product.Attr('ARO_Multi_Window_Client_Qty').GetValue() or 0)
    ARO_Multi_Window_Support = Product.Attr('AR0_Multi_Window_support').GetValue()
    ARO_Experion_release = Product.Attr('ARO_Experion_Software_Release').GetValue()
    ARO_client_peripherals = int(Product.Attr('ARO_Client_Peripherals').GetValue() or 0)
    client_node_type = Product.Attr('ARO_Client_Node_Type').GetValue()
    remote_client_connection = Product.Attr('ARO_Remote_Client_Connection').GetValue()
    Aro_flex_station_license_required=int(Product.Attr('ARO_new_Flex_Station_licenses_required').GetValue() or 0)
    ARO_new_Console_Station_Extension_License =int(Product.Attr('ARO_new_Console_Station_Extension_License').GetValue() or 0)
    ARO_Native_Window_Client_Experion=int(Product.Attr('ARO_Native_Window_Client_Experion').GetValue() or 0)
    RESS_concurrent_remote_access_device_nodes=int(Product.Attr('RESS_Concurrent_Remote_Access_device_nodes').GetValue() or 0)
    RESS_Native_Window_Client_Experion = Product.Attr('Native_window_accessibility_through_ARO').GetValue()
    RESS_exp_server_type = Product.Attr('Experion_server_type_at_location').GetValue()
    RESS_flex_station_license_required = int(Product.Attr('RESS_new_Flex_Station_licenses_required').GetValue() or 0)
    RESS_new_Console_Station_Extension_License=int(Product.Attr('RESS_new_Console_Station_Extension_License').GetValue() or 0)
    ARO_Experion_Server_Location=Product.Attr('ARO_Experion_Server_Location').GetValue()
    TPTHNR01_100,TPTHNR02_100,TPTHNCL9_100 = 0,0,0
    part_qty, EP_SMWIN1, TPTHNCL5_400 , TP_OTP231, EP_OCOTP1,Total_Console_station_license,Total_Native_Window_Client_Experion,EP_STAT10,EP_STAT05,EP_STAT01,EP_STACEX,EP_RNW000 = 0,0,0,0,0,0,0,0,0,0,0,0
    if ARO_System_Required == "Yes" and Node_Supplier == 'Honeywell':
        if ARO_client_20>0:
            part_qty = ARO_client_20
        if ARO_client_40>0:
            part_qty = ARO_client_40
        if ARO_client_15 > 0 or ARO_WindOW_Client>0:
            part_qty = ARO_client_15+ARO_WindOW_Client
        if client_node_type =='Pepperl+Fuchs BTC22':
            TPTHNR01_100 = part_qty
        elif client_node_type =='Pepperl+Fuchs BTC24':
            TPTHNR02_100 = part_qty
        elif client_node_type =='Wyse 5070 Optiplex 3000':
            TPTHNCL9_100 = part_qty
        if remote_client_connection =='Microsoft Remote Desktop client' and ARO_Multi_Window_Support == 'Yes' and  int(ARO_WindOW_Client) > 0:
            EP_SMWIN1 = ARO_WindOW_Client
        if ARO_Experion_release in ('R530', 'R520') and ARO_client_peripherals>0:
            TPTHNCL5_400 , TP_OTP231 = ARO_client_peripherals, ARO_client_peripherals
    if RESS_System_Required == "Yes" and RESS_Experion_release in ('R530', 'R520'):
        if RESS_Qty_Thin_clients>0:
            TPTHNCL5_400 += int(RESS_Qty_Thin_clients)
        if RESS_Qty_OperatorTouchPanel>0:
            TP_OTP231 += int(RESS_Qty_OperatorTouchPanel)
            EP_OCOTP1 += int(RESS_Qty_OperatorTouchPanel)
        if RESS_concurrent_remote_access_device_nodes >0:
            Total_Native_Window_Client_Experion += int(RESS_concurrent_remote_access_device_nodes)
        if RESS_Native_Window_Client_Experion == 'Yes':
            Total_Native_Window_Client_Experion += 1
        if RESS_new_Console_Station_Extension_License>0:
            Total_Console_station_license += int(RESS_new_Console_Station_Extension_License)
        if RESS_flex_station_license_required > 0:
            #Total_Flex_station_license += int(RESS_flex_station_license_required)
            EP_STAT05,rem2=divmod(RESS_flex_station_license_required,5)
            EP_STAT01=rem2

    if ARO_System_Required == "Yes" and ARO_Experion_release in ('R530', 'R520'):
        if ARO_Qty_OperatorTouchPanel>0:
            EP_OCOTP1 += int(ARO_Qty_OperatorTouchPanel)
        if Aro_flex_station_license_required>0 and ARO_Experion_Server_Location =="Experion PKS Server":
            #Total_Flex_station_license += int(Aro_flex_station_license_required)
            EP_STAT10,rem=divmod(Aro_flex_station_license_required,10)
            EP_STAT05_1,rem1=divmod(rem,5)
            EP_STAT05+=EP_STAT05_1
            EP_STAT01+=rem1
        if ARO_new_Console_Station_Extension_License>0 and ARO_Experion_Server_Location =="Server TPS":
            Total_Console_station_license += int(ARO_new_Console_Station_Extension_License)
        if ARO_Native_Window_Client_Experion>0:
            Total_Native_Window_Client_Experion += int(ARO_Native_Window_Client_Experion)
    if Total_Console_station_license>0:
        EP_STACEX=Total_Console_station_license
    if Total_Native_Window_Client_Experion>0:
        EP_RNW000=Total_Native_Window_Client_Experion
    Trace.Write("Before return")
    return TPTHNR01_100,TPTHNR02_100,TPTHNCL9_100, EP_SMWIN1,TPTHNCL5_400 ,TP_OTP231, EP_OCOTP1,EP_STAT10,EP_STAT05,EP_STAT01,EP_STACEX,EP_RNW000

#CXCPQ-112863
def Aro_Display_Parts(Product):
	AroSystem=Product.Attr('ARO_System_Required').GetValue()
	#initilizing all qnt zero
	qty24dell=qty27dell=qty24NEC=qty27NEC=0
	#Size Mapiing with verible
	size_map={
		"24 inch NTS DELL":"qty24dell",
		"27 inch NTS DELL":"qty27dell",
		"24 inch NTS NEC":"qty24NEC",
		"27 inch NTS NEC":"qty27NEC"
	}
	if AroSystem=="Yes":
		##Arrs value Collection
		if Product.Attr('ARO_Client_Harware_Req').GetValue()== "Yes":
			ClientSize=Product.Attr('ARO_Client_Display_Size').GetValue()
			ClientSupplie=Product.Attr('ARO_Client_Display_Supplier').GetValue()
			if ClientSupplie=="Honeywell" and ClientSize in size_map and Product.Attr('ARO_Multi_Window_Client_4').GetValue()!="" and Product.Attr('ARO_Multi_Window_Client_Qty').GetValue()!="":
				locals()[size_map[ClientSize]]=int(Product.Attr('ARO_Multi_Window_Client_4').GetValue())*int(Product.Attr('ARO_Multi_Window_Client_Qty').GetValue())
		if Product.Attr('ARO_server_require_Physical_hardware').GetValue()=="Yes":
			Ser_size=Product.Attr('ARO_Display_Size').GetValue()
			if Product.Attr('ARO_Display_Supplier').GetValue()=="Honeywell" and Ser_size in size_map:
				locals()[size_map[Ser_size]]=locals().get(size_map[Ser_size],0)+1

		if Product.Attr('ARO_Gateway_require_Physical_hardware').GetValue()=="Yes":
			GWSize=Product.Attr('ARO_Display_Size_GW').GetValue()
			if Product.Attr('ARO_Display_Supplier_GW').GetValue()=="Honeywell" and GWSize in size_map:
				locals()[size_map[GWSize]]=locals().get(size_map[GWSize],0)+1

	return qty24dell,qty27dell,qty24NEC,qty27NEC

# CXCPQ-112916 Start
def getpart_RESSClients(Product):
	MZ_PCWT01 = MZ_PCWR01 = MZ_PCWS86 = MZ_PCWS15 = 0
	RESS_System_Required=Product.Attr('RESS_System_Required').GetValue()
	RESS_Sw_Rel=Product.Attr('RESS_Experion_Software_Release').GetValue()
	RESS_remote_client_stn_hw=Product.Attr('Remote_client_station_hardware').GetValue()
	RESS_Client_Qty = Product.Attr("Client_Qty").GetValue()
	RESS_Client_Node_Type=Product.Attr('Client_Node_Type').GetValue()
	RESS_Client_Node_Supplier=Product.Attr('Client_Node_Supplier').GetValue()
	if RESS_System_Required=="Yes" and RESS_Sw_Rel=="R530" and RESS_remote_client_stn_hw =="Yes" and int(RESS_Client_Qty)>0 and RESS_Client_Node_Supplier =="Honeywell" and RESS_Client_Node_Type:
		if RESS_Client_Node_Type == 'STN_PER_DELL_Tower_RAID1':
			MZ_PCWT01 = int(float(RESS_Client_Qty))
		elif RESS_Client_Node_Type == 'STN_PER_DELL_Rack_RAID1':
			MZ_PCWR01 = int(float(RESS_Client_Qty))
		elif RESS_Client_Node_Type == 'STN_PER_HP_Tower_RAID1':
			MZ_PCWS86 = int(float(RESS_Client_Qty))
		elif RESS_Client_Node_Type == 'STN_STD_DELL_Tower_NonRAID':
			MZ_PCWS15 = int(float(RESS_Client_Qty))
	return MZ_PCWT01, MZ_PCWR01, MZ_PCWS86, MZ_PCWS15

def getpart_RESSDisplays(Product):
	EP_SMWIN1 = 0
	RESS_Client_Qty = Product.Attr("Client_Qty").GetValue()
	RESS_Displays = Product.Attr('Display_Qty_4').GetValue()
	if RESS_Displays and int(RESS_Displays) > 0:
		EP_SMWIN1 = int(RESS_Client_Qty)
	return EP_SMWIN1
# CXCPQ-112916 End