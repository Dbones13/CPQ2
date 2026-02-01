import System.Decimal as D
from GS_ARO_RESS_getAttrVal import getERGAttrVal
def getpart_TPFPW271(Product):
	var=var1=var2=var3=var4=var5=0
	ARO_System_Required=Product.Attr('ARO_System_Required').GetValue()
	RESS_System_Required=Product.Attr('RESS_System_Required').GetValue()
	ERG_System = Product.Attr('Experion Remote Gateway (ERG) System Required').GetValue()
	if Product.Name == "Experion ARO, RESS & ERG Group":
		Display_Size=Product.Attr('ARO_Display_Size').GetValue()
		Display_Size1=Product.Attr('ARO_Display_Size_GW').GetValue()
		Display_Supplier=Product.Attr('ARO_Display_Supplier').GetValue()
		Display_Supplier2=Product.Attr('ARO_Display_Supplier_GW').GetValue()
		Server_Node_Type=Product.Attr('ARO_Server_Node_Type').GetValue()
		Server_Node_Type2=Product.Attr('ARO_Server_Node_Type_GW').GetValue()
		server_qnt = Product.Attr('Displays(ERG Server)(0-1)').GetValue()
		erg_size = Product.Attr('Display_Size(ERG Server)').GetValue()
		erg_supplier = Product.Attr('Display_Supplier(ERG Server)').GetValue()
		cb_server_qnt = Product.Attr('Displays (ERG CB Server) (0-1)').GetValue()
		cb_erg_size = Product.Attr('Display Size (ERG CB Server)').GetValue()
		cb_erg_supplier = Product.Attr('Display Supplier (ERG CB Server)').GetValue()
		RESS_server_display_size = Product.Attr('RESS_Display_Size').GetValue()
		RESS_server_display_supplier = Product.Attr('RESS_Display_Supplier').GetValue()
		RESS_client_display_size = Product.Attr('Display_Size').GetValue()
		RESS_client_display_supplier = Product.Attr('Display_Supplier_RESS').GetValue()
		total_qty = 0
		client_qty = 0
		if ARO_System_Required =="Yes" and Display_Size=="27 inch" and Display_Supplier=="Honeywell" and (Server_Node_Type=="SVR_PER_HP_Rack_RAID5" or Server_Node_Type=="SVR_PER_DELL_Rack_RAID1_RUG" or Server_Node_Type=="SVR_PER_DELL_Tower_RAID1" or Server_Node_Type=="SVR_PER_DELL_Rack_RAID1" or Server_Node_Type=="SVR_STD_DELL_Tower_RAID1" or Server_Node_Type=="SVR_STD_DELL_Rack_RAID1" or Server_Node_Type=="SVR_PER_DELL_Rack_RAID5") :
			var1=1
		if ARO_System_Required =="Yes" and Display_Size1=="27 inch" and Display_Supplier2=="Honeywell" and (Server_Node_Type2=="SVR_PER_HP_Rack_RAID5" or Server_Node_Type2=="SVR_PER_DELL_Rack_RAID1_RUG" or Server_Node_Type2=="SVR_PER_DELL_Tower_RAID1" or Server_Node_Type2=="SVR_PER_DELL_Rack_RAID1" or Server_Node_Type2=="SVR_STD_DELL_Tower_RAID1" or Server_Node_Type2=="SVR_STD_DELL_Rack_RAID1" or Server_Node_Type2=="SVR_PER_DELL_Rack_RAID5"):
			var2=1
		if RESS_System_Required == 'Yes' :
			server_qty = 1 if RESS_server_display_size == '27 inch NTS NEC' and RESS_server_display_supplier == 'Honeywell' else 0
			if RESS_client_display_size == '27 inch NTS NEC' and RESS_client_display_supplier == 'Honeywell':
				client_qty = (int(Product.Attr('Client_Qty').GetValue()) * int(Product.Attr('Display_Qty_4').GetValue())) if Product.Attr('Multiwindow_support').GetValue() == 'Yes' else (int(Product.Attr('Client_Qty').GetValue()) * int(Product.Attr('Display_Qty').GetValue()))
			total_qty = server_qty + client_qty
			var3=total_qty
		if ERG_System == 'Yes' and int(server_qnt) > 0 and erg_size == '27 inch NTS NEC' and erg_supplier == 'Honeywell':
			var4 = 1
		if ERG_System == 'Yes' and int(cb_server_qnt) > 0 and cb_erg_size == '27 inch NTS NEC' and cb_erg_supplier == 'Honeywell':
			var5 = 1
	var=var1+var2+var3+var4+var5
	return(var)
#CXCPQ-49203
def getpart_MZPCWS94(Product):
	sum1=sum2=sum3=0
	ARO_System_Required=Product.Attr('ARO_System_Required').GetValue()
	RESS_System_Required=Product.Attr('RESS_System_Required').GetValue()
	if Product.Name == "Experion ARO, RESS & ERG Group":
		aro_release=Product.Attr('ARO_Experion_Software_Release').GetValue()
		ress_release=Product.Attr('RESS_Experion_Software_Release').GetValue()
		aro_station=Product.Attr('ARO_Station_Node_WS').GetValue()
		ress_station=Product.Attr('RESS_Staton_Node').GetValue()
		aro_node_supplier=Product.Attr('ARO_Node_Supplier_WB').GetValue()
		ress__node_supplier=Product.Attr('RESS_Node_Supplier').GetValue()
		aro_additional_station=Product.Attr('Additional_Stations_for_ARO_WS').GetValue()
		ress_additional_station=Product.Attr('RESS_Additional_Stations').GetValue()
		if ARO_System_Required =="Yes" and aro_release=="R520" and aro_node_supplier=="Honeywell" and aro_station=="STN_PER_DELL_Tower_RAID1" :
			sum2=int(Product.Attr('Additional_Stations_for_ARO_WS').GetValue()) if Product.Attr('Additional_Stations_for_ARO_WS').GetValue()!='' else 0
		if RESS_System_Required =="Yes" and ress_release=="R520" and ress__node_supplier=="Honeywell" and ress_station=="STN_PER_DELL_Tower_RAID1" :
			sum3=int(Product.Attr('RESS_Additional_Stations').GetValue()) if Product.Attr('RESS_Additional_Stations').GetValue()!='' else 0
		sum1= int(sum2)+int(sum3)
	return(sum1)
#CXCPQ-49202
def getpart_MZPCWS14(Product):
	sum4=sum5=sum6=0
	ARO_System_Required=Product.Attr('ARO_System_Required').GetValue()
	RESS_System_Required=Product.Attr('RESS_System_Required').GetValue()
	if Product.Name == "Experion ARO, RESS & ERG Group":
		aro_release=Product.Attr('ARO_Experion_Software_Release').GetValue()
		ress_release=Product.Attr('RESS_Experion_Software_Release').GetValue()
		aro_station=Product.Attr('ARO_Station_Node_WS').GetValue()
		ress_station=Product.Attr('RESS_Staton_Node').GetValue()
		aro_node_supplier=Product.Attr('ARO_Node_Supplier_WB').GetValue()
		ress__node_supplier=Product.Attr('RESS_Node_Supplier').GetValue()
		aro_additional_station=Product.Attr('Additional_Stations_for_ARO_WS').GetValue()
		ress_additional_station=Product.Attr('RESS_Additional_Stations').GetValue()
		if ARO_System_Required =="Yes" and aro_release=="R520" and aro_node_supplier=="Honeywell" and aro_station=="STN_STD_DELL_Tower_NonRAID" :
			sum5=int(Product.Attr('Additional_Stations_for_ARO_WS').GetValue()) if Product.Attr('Additional_Stations_for_ARO_WS').GetValue()!='' else 0
		if RESS_System_Required =="Yes" and ress_release=="R520" and ress__node_supplier=="Honeywell" and ress_station=="STN_STD_DELL_Tower_NonRAID" :
			sum6=int(Product.Attr('RESS_Additional_Stations').GetValue()) if Product.Attr('RESS_Additional_Stations').GetValue()!='' else 0
		sum4= int(sum5)+int(sum6)
	return(sum4)
#CXCPQ-49204
def getpart_MZPCWS84(Product):
	sum7=sum8=sum9=0
	ARO_System_Required=Product.Attr('ARO_System_Required').GetValue()
	RESS_System_Required=Product.Attr('RESS_System_Required').GetValue()
	if Product.Name == "Experion ARO, RESS & ERG Group":
		aro_release=Product.Attr('ARO_Experion_Software_Release').GetValue()
		ress_release=Product.Attr('RESS_Experion_Software_Release').GetValue()
		aro_station=Product.Attr('ARO_Station_Node_WS').GetValue()
		ress_station=Product.Attr('RESS_Staton_Node').GetValue()
		aro_node_supplier=Product.Attr('ARO_Node_Supplier_WB').GetValue()
		ress__node_supplier=Product.Attr('RESS_Node_Supplier').GetValue()
		aro_additional_station=Product.Attr('Additional_Stations_for_ARO_WS').GetValue()
		ress_additional_station=Product.Attr('RESS_Additional_Stations').GetValue()
		if ARO_System_Required =="Yes" and aro_node_supplier=="Honeywell" and aro_station=="STN_PER_HP_Tower_RAID1" :
			sum8=int(Product.Attr('Additional_Stations_for_ARO_WS').GetValue()) if Product.Attr('Additional_Stations_for_ARO_WS').GetValue()!='' else 0
		if RESS_System_Required =="Yes" and ress__node_supplier=="Honeywell" and ress_station=="STN_PER_HP_Tower_RAID1" :
			sum9=int(Product.Attr('RESS_Additional_Stations').GetValue()) if Product.Attr('RESS_Additional_Stations').GetValue()!='' else 0
		sum7= int(sum8)+int(sum9)
	return(sum7)
#CXCPQ-49198
def getpart_TPFPD211200(Product):
	var7=var4=var5=var6=var8=var9=0
	ARO_System_Required=Product.Attr('ARO_System_Required').GetValue()
	RESS_System_Required=Product.Attr('RESS_System_Required').GetValue()
	if Product.Name == "Experion ARO, RESS & ERG Group":
		Display_Size=Product.Attr('ARO_Display_Size').GetValue()
		Display_Size1=Product.Attr('ARO_Display_Size_GW').GetValue()
		Display_Size2=Product.Attr('RESS_Display_Size').GetValue()
		Display_Supplier=Product.Attr('ARO_Display_Supplier').GetValue()
		Display_Supplier2=Product.Attr('ARO_Display_Supplier_GW').GetValue()
		Display_Supplier3=Product.Attr('RESS_Display_Supplier').GetValue()
		Server_Node_Type=Product.Attr('ARO_Server_Node_Type').GetValue()
		Server_Node_Type2=Product.Attr('ARO_Server_Node_Type_GW').GetValue()
		Server_Node_Type3=Product.Attr('RESS_Server_Node_Type').GetValue()
		CE_Site_Voltage=Product.Attr('CE_Site_Voltage').GetValue()
		ERG_Sys_Req,erg_cb_count,erg_count,erg_cb_size,erg_size,erg_cb_supl,erg_supl=getERGAttrVal(Product, 'TPFPD211200')
		if ARO_System_Required =="Yes" and CE_Site_Voltage=="240V" and Display_Size=="21.33 inch" and Display_Supplier=="Honeywell" and (Server_Node_Type=="SVR_PER_HP_Rack_RAID5" or Server_Node_Type=="SVR_PER_DELL_Rack_RAID1_RUG" or Server_Node_Type=="SVR_PER_DELL_Tower_RAID1" or Server_Node_Type=="SVR_PER_DELL_Rack_RAID1" or Server_Node_Type=="SVR_STD_DELL_Tower_RAID1" or Server_Node_Type=="SVR_STD_DELL_Rack_RAID1" or Server_Node_Type=="SVR_PER_DELL_Rack_RAID5") :
			var4=1
		if CE_Site_Voltage=="240V" and ARO_System_Required =="Yes" and Display_Size1=="21.33 inch" and Display_Supplier2=="Honeywell" and (Server_Node_Type2=="SVR_PER_HP_Rack_RAID5" or Server_Node_Type2=="SVR_PER_DELL_Rack_RAID1_RUG" or Server_Node_Type2=="SVR_PER_DELL_Tower_RAID1" or Server_Node_Type2=="SVR_PER_DELL_Rack_RAID1" or Server_Node_Type2=="SVR_STD_DELL_Tower_RAID1" or Server_Node_Type2=="SVR_STD_DELL_Rack_RAID1" or Server_Node_Type2=="SVR_PER_DELL_Rack_RAID5"):
			var5=1
		if RESS_System_Required == "Yes" and CE_Site_Voltage=="240V" and Display_Size2=="21.33 inch" and Display_Supplier3=="Honeywell" and (Server_Node_Type3=="SVR_PER_HP_Rack_RAID5" or Server_Node_Type3=="SVR_PER_DELL_Rack_RAID1_RUG" or Server_Node_Type3=="SVR_PER_DELL_Tower_RAID1" or Server_Node_Type3=="SVR_PER_DELL_Rack_RAID1" or Server_Node_Type3=="SVR_STD_DELL_Tower_RAID1" or Server_Node_Type3=="SVR_STD_DELL_Rack_RAID1" or Server_Node_Type3=="SVR_PER_DELL_Rack_RAID5"):
			var6=1
		if CE_Site_Voltage=="240V" and ERG_Sys_Req=='Yes' and erg_cb_count>0 and erg_cb_size=='21.33 inch NTS' and erg_cb_supl=='Honeywell':
			var8=erg_cb_count
		if CE_Site_Voltage=="240V" and ERG_Sys_Req=='Yes' and erg_count>0 and erg_size=='21.33 inch NTS' and erg_supl=='Honeywell':
			var9=erg_count
		var7=var4+var5+var6+var8+var9
	return(var7)
#CXCPQ-49206
def getpart_EPCOAW10(Product):
	sum7=sum8=sum9=0
	ARO_System_Required=Product.Attr('ARO_System_Required').GetValue()
	RESS_System_Required=Product.Attr('RESS_System_Required').GetValue()
	if Product.Name == "Experion ARO, RESS & ERG Group":
		aro_release=Product.Attr('ARO_Experion_Software_Release').GetValue()
		ress_release=Product.Attr('RESS_Experion_Software_Release').GetValue()
		aro_station=Product.Attr('ARO_Station_Node_WS').GetValue()
		ress_station=Product.Attr('RESS_Staton_Node').GetValue()
		aro_node_supplier=Product.Attr('ARO_Node_Supplier_WB').GetValue()
		ress__node_supplier=Product.Attr('RESS_Node_Supplier').GetValue()
		aro_additional_station=Product.Attr('Additional_Stations_for_ARO_WS').GetValue()
		ress_additional_station=Product.Attr('RESS_Additional_Stations').GetValue()
		release=["R510","R511"]
		hardware=["STN_PER_DELL_Tower_RAID1","STN_PER_DELL_Rack_RAID1","STN_PER_HP_Tower_RAID1"]
		if ARO_System_Required =="Yes" and aro_release in release and aro_node_supplier=="Honeywell" and aro_station in hardware :
			sum8=int(Product.Attr('Additional_Stations_for_ARO_WS').GetValue()) if Product.Attr('Additional_Stations_for_ARO_WS').GetValue()!='' else 0
		if RESS_System_Required =="Yes" and ress_release in release and ress__node_supplier=="Honeywell" and ress_station in hardware  :
			sum9=int(Product.Attr('RESS_Additional_Stations').GetValue()) if Product.Attr('RESS_Additional_Stations').GetValue()!='' else 0
		sum7= int(sum9)+int(sum8)
	return(sum7)
#CXCPQ-49197
def getpart_TPFPD211100(Product):
	var11=var8=var9=var10=var12=var13=0
	ARO_System_Required=Product.Attr('ARO_System_Required').GetValue()
	RESS_System_Required=Product.Attr('RESS_System_Required').GetValue()
	if Product.Name == "Experion ARO, RESS & ERG Group":
		Display_Size=Product.Attr('ARO_Display_Size').GetValue()
		Display_Size1=Product.Attr('ARO_Display_Size_GW').GetValue()
		Display_Size2=Product.Attr('RESS_Display_Size').GetValue()
		Display_Supplier=Product.Attr('ARO_Display_Supplier').GetValue()
		Display_Supplier2=Product.Attr('ARO_Display_Supplier_GW').GetValue()
		Display_Supplier3=Product.Attr('RESS_Display_Supplier').GetValue()
		Server_Node_Type=Product.Attr('ARO_Server_Node_Type').GetValue()
		Server_Node_Type2=Product.Attr('ARO_Server_Node_Type_GW').GetValue()
		Server_Node_Type3=Product.Attr('RESS_Server_Node_Type').GetValue()
		CE_Site_Voltage=Product.Attr('CE_Site_Voltage').GetValue()
		ERG_Sys_Req,erg_cb_count,erg_count,erg_cb_size,erg_size,erg_cb_supl,erg_supl=getERGAttrVal(Product, 'TPFPD211100')
		if ARO_System_Required =="Yes" and CE_Site_Voltage=="120V" and Display_Size=="21.33 inch" and Display_Supplier=="Honeywell" and (Server_Node_Type=="SVR_PER_HP_Rack_RAID5" or Server_Node_Type=="SVR_PER_DELL_Rack_RAID1_RUG" or Server_Node_Type=="SVR_PER_DELL_Tower_RAID1" or Server_Node_Type=="SVR_PER_DELL_Rack_RAID1" or Server_Node_Type=="SVR_STD_DELL_Tower_RAID1" or Server_Node_Type=="SVR_STD_DELL_Rack_RAID1" or Server_Node_Type=="SVR_PER_DELL_Rack_RAID5") :
			var8=1
		if CE_Site_Voltage=="120V" and ARO_System_Required =="Yes" and Display_Size1=="21.33 inch" and Display_Supplier2=="Honeywell" and (Server_Node_Type2=="SVR_PER_HP_Rack_RAID5" or Server_Node_Type2=="SVR_PER_DELL_Rack_RAID1_RUG" or Server_Node_Type2=="SVR_PER_DELL_Tower_RAID1" or Server_Node_Type2=="SVR_PER_DELL_Rack_RAID1" or Server_Node_Type2=="SVR_STD_DELL_Tower_RAID1" or Server_Node_Type2=="SVR_STD_DELL_Rack_RAID1" or Server_Node_Type2=="SVR_PER_DELL_Rack_RAID5"):
			var9=1
		if RESS_System_Required == "Yes" and CE_Site_Voltage=="120V" and Display_Size2=="21.33 inch" and Display_Supplier3=="Honeywell" and (Server_Node_Type3=="SVR_PER_HP_Rack_RAID5" or Server_Node_Type3=="SVR_PER_DELL_Rack_RAID1_RUG" or Server_Node_Type3=="SVR_PER_DELL_Tower_RAID1" or Server_Node_Type3=="SVR_PER_DELL_Rack_RAID1" or Server_Node_Type3=="SVR_STD_DELL_Tower_RAID1" or Server_Node_Type3=="SVR_STD_DELL_Rack_RAID1" or Server_Node_Type3=="SVR_PER_DELL_Rack_RAID5"):
			var10=1
		if CE_Site_Voltage=="120V" and ERG_Sys_Req=='Yes' and erg_cb_count>0 and erg_cb_size=='21.33 inch NTS' and erg_cb_supl=='Honeywell':
			var12=erg_cb_count
		if CE_Site_Voltage=="120V" and ERG_Sys_Req=='Yes' and erg_count>0 and erg_size=='21.33 inch NTS' and erg_supl=='Honeywell':
			var13=erg_count
		var11=var8+var9+var10+var12+var13
	return(var11)
#CXCPQ-49199
def getpart_TPFPW231(Product):
	sum15=sum13=sum14=0
	ARO_System_Required=Product.Attr('ARO_System_Required').GetValue()
	RESS_System_Required=Product.Attr('RESS_System_Required').GetValue()
	if Product.Name == "Experion ARO, RESS & ERG Group":
		aro_Display=Product.Attr('ARO_Display_size_WB').GetValue()
		ress_Display=Product.Attr('RESS_Display_size_WS').GetValue()
		aro_node_supplier=Product.Attr('ARO_Node_Supplier_WB').GetValue()
		ress__node_supplier=Product.Attr('RESS_Node_Supplier').GetValue()
		aro_additional_station=Product.Attr('Additional_Stations_for_ARO_WS').GetValue()
		ress_additional_station=Product.Attr('RESS_Additional_Stations').GetValue()
		if ARO_System_Required =="Yes" and aro_Display=="23 inch" and aro_node_supplier=="Honeywell" :
			sum13=int(Product.Attr('Additional_Stations_for_ARO_WS').GetValue()) if Product.Attr('Additional_Stations_for_ARO_WS').GetValue()!='' else 0
		if RESS_System_Required =="Yes" and ress_Display=="23 inch" and ress__node_supplier=="Honeywell" :
			sum14=int(Product.Attr('RESS_Additional_Stations').GetValue()) if Product.Attr('RESS_Additional_Stations').GetValue()!='' else 0
		sum15= int(sum13)+int(sum14)
	return(sum15)
#CXCPQ-49201
def getpart_TPFPW241(Product):
	var19=var16=var17=var18=var20=var21=0
	ARO_System_Required=Product.Attr('ARO_System_Required').GetValue()
	RESS_System_Required=Product.Attr('RESS_System_Required').GetValue()
	if Product.Name == "Experion ARO, RESS & ERG Group":
		Display_Size=Product.Attr('ARO_Display_Size').GetValue()
		Display_Size1=Product.Attr('ARO_Display_Size_GW').GetValue()
		Display_Supplier=Product.Attr('ARO_Display_Supplier').GetValue()
		Display_Supplier2=Product.Attr('ARO_Display_Supplier_GW').GetValue()
		Server_Node_Type=Product.Attr('ARO_Server_Node_Type').GetValue()
		Server_Node_Type2=Product.Attr('ARO_Server_Node_Type_GW').GetValue()
		ERG_Sys_Req,erg_cb_count,erg_count,erg_cb_size,erg_size,erg_cb_supl,erg_supl,total_qty=getERGAttrVal(Product, 'TPFPW241')
		if ARO_System_Required =="Yes" and Display_Size=="24 inch" and Display_Supplier=="Honeywell" and (Server_Node_Type=="SVR_PER_HP_Rack_RAID5" or Server_Node_Type=="SVR_PER_DELL_Rack_RAID1_RUG" or Server_Node_Type=="SVR_PER_DELL_Tower_RAID1" or Server_Node_Type=="SVR_PER_DELL_Rack_RAID1" or Server_Node_Type=="SVR_STD_DELL_Tower_RAID1" or Server_Node_Type=="SVR_STD_DELL_Rack_RAID1" or Server_Node_Type=="SVR_PER_DELL_Rack_RAID5") :
			var16=1
		if ARO_System_Required =="Yes" and Display_Size1=="24 inch" and Display_Supplier2=="Honeywell" and (Server_Node_Type2=="SVR_PER_HP_Rack_RAID5" or Server_Node_Type2=="SVR_PER_DELL_Rack_RAID1_RUG" or Server_Node_Type2=="SVR_PER_DELL_Tower_RAID1" or Server_Node_Type2=="SVR_PER_DELL_Rack_RAID1" or Server_Node_Type2=="SVR_STD_DELL_Tower_RAID1" or Server_Node_Type2=="SVR_STD_DELL_Rack_RAID1" or Server_Node_Type2=="SVR_PER_DELL_Rack_RAID5"):
			var17=1
		if RESS_System_Required == "Yes" :
			var18=total_qty
		if ERG_Sys_Req=='Yes' and erg_cb_count>0 and erg_cb_size=='24 inch NTS NEC' and erg_cb_supl=='Honeywell':
			var20=erg_cb_count
		if ERG_Sys_Req=='Yes' and erg_count>0 and erg_size=='24 inch NTS NEC' and erg_supl=='Honeywell':
			var21=erg_count
		var19=var16+var17+var18+var20+var21
	return(var19)
#CXCPQ-49191
def getpart_MZPCSR02(Product):
	var15=var12=var13=var14=0
	ARO_System_Required=Product.Attr('ARO_System_Required').GetValue()
	RESS_System_Required=Product.Attr('RESS_System_Required').GetValue()
	if Product.Name == "Experion ARO, RESS & ERG Group":
		Aro_Tpm=Product.Attr('ARO_Trusted_Platform_Module').GetValue()
		Aro_Tpm1=Product.Attr('ARO_Trusted_Platform_Module_GW').GetValue()
		Aro_Tpm2=Product.Attr('RESS_Trusted_Platform_Module').GetValue()
		Node_Supplier=Product.Attr('ARO_Node_Supplier').GetValue()
		Node_Supplier2=Product.Attr('ARO_Node_Supplier_GW').GetValue()
		Node_Supplier3=Product.Attr('RESS_Node_Supplier_(Server)').GetValue()
		Server_Node_Type=Product.Attr('ARO_Server_Node_Type').GetValue()
		Server_Node_Type2=Product.Attr('ARO_Server_Node_Type_GW').GetValue()
		Server_Node_Type3=Product.Attr('RESS_Server_Node_Type').GetValue()
		if ARO_System_Required =="Yes" and Aro_Tpm=="Yes" and Node_Supplier=="Honeywell" and (Server_Node_Type=="SVR_PER_DELL_Rack_RAID1") :
			var12=1
		if ARO_System_Required =="Yes" and Aro_Tpm1=="Yes" and Node_Supplier2=="Honeywell" and (Server_Node_Type2=="SVR_PER_DELL_Rack_RAID1"):
			var13=1
		if RESS_System_Required == "Yes" and Aro_Tpm2=="Yes" and Node_Supplier3=="Honeywell" and (Server_Node_Type3=="SVR_PER_DELL_Rack_RAID1"):
			var14=1
		var15=var12+var13+var14
	return(var15)
#CXCPQ-49192
def getpart_MZPCST01(Product):
	var23=var20=var21=var22=var200=var201=0
	ARO_System_Required=Product.Attr('ARO_System_Required').GetValue()
	RESS_System_Required=Product.Attr('RESS_System_Required').GetValue()
	ERG_System_Required=Product.Attr('Experion Remote Gateway (ERG) System Required').GetValue()
	if Product.Name == "Experion ARO, RESS & ERG Group":
		Aro_Tpm=Product.Attr('ARO_Trusted_Platform_Module').GetValue()
		Aro_Tpm1=Product.Attr('ARO_Trusted_Platform_Module_GW').GetValue()
		ERG_Tpm=Product.Attr('Trusted Platform Module (TPM)').GetValue()
		Aro_Tpm2=Product.Attr('RESS_Trusted_Platform_Module').GetValue()
		Node_Supplier=Product.Attr('ARO_Node_Supplier').GetValue()
		Node_Supplier2=Product.Attr('ARO_Node_Supplier_GW').GetValue()
		Node_Supplier3=Product.Attr('RESS_Node_Supplier_(Server)').GetValue()
		ERG_Node_Supplier=Product.Attr('Node Supplier (ERG CB Server)').GetValue()
		Server_Node_Type=Product.Attr('ARO_Server_Node_Type').GetValue()
		Server_Node_Type2=Product.Attr('ARO_Server_Node_Type_GW').GetValue()
		ERG_CB_Server_Node_Type=Product.Attr('ERG CB Server Node Type').GetValue()
        
		ERG_Server_Node_Type=Product.Attr('ERG_Server_Node_Type').GetValue()
		ERG_Server_Node_Supplier=Product.Attr('Node_Suplier(ERG Server)').GetValue()
		ERG_Server_Tpm=Product.Attr('Trusted_Platform_Module(TPM)').GetValue()
        
		if ARO_System_Required =="Yes" and Aro_Tpm=="Yes" and Node_Supplier=="Honeywell" and (Server_Node_Type=="SVR_STD_DELL_Tower_RAID1") :
			var20=1
		if ARO_System_Required =="Yes" and Aro_Tpm1=="Yes" and Node_Supplier2=="Honeywell" and (Server_Node_Type2=="SVR_STD_DELL_Tower_RAID1"):
			var21=1
		if RESS_System_Required == "Yes" and Aro_Tpm2=="Yes" and Node_Supplier3=="Honeywell" and (Server_Node_Type3=="SVR_STD_DELL_Tower_RAID1"):
			var22=1
		if ERG_System_Required == "Yes" and ERG_Tpm=="Yes" and ERG_Node_Supplier=="Honeywell" and (ERG_CB_Server_Node_Type=="SVR_STD_DELL_Tower_RAID1"):
			var200=1
		if ERG_System_Required == "Yes" and ERG_Server_Tpm=="Yes" and ERG_Server_Node_Supplier=="Honeywell" and (ERG_Server_Node_Type=="SVR_STD_DELL_Tower_RAID1"):
			var201=1
		var23=var20+var21+var22+var200+var201
	return(var23)
def getpart_MZPCST81(Product):
	var23=var20=var21=0
	
	ERG_System_Required=Product.Attr('Experion Remote Gateway (ERG) System Required').GetValue()
	if Product.Name == "Experion ARO, RESS & ERG Group":
		
		ERG_Tpm=Product.Attr('Trusted Platform Module (TPM)').GetValue()
		ERG_Node_Supplier=Product.Attr('Node Supplier (ERG CB Server)').GetValue()
		ERG_CB_Server_Node_Type=Product.Attr('ERG CB Server Node Type').GetValue()
        
		ERG_Server_Node_Type=Product.Attr('ERG_Server_Node_Type').GetValue()
		ERG_Server_Node_Supplier=Product.Attr('Node_Suplier(ERG Server)').GetValue()
		ERG_Server_Tpm=Product.Attr('Trusted_Platform_Module(TPM)').GetValue()
        
		if ERG_System_Required == "Yes" and ERG_Tpm=="No" and ERG_Node_Supplier=="Honeywell" and (ERG_CB_Server_Node_Type=="SVR_STD_DELL_Tower_RAID1"):
			var20=1
		if ERG_System_Required == "Yes" and ERG_Server_Tpm=="No" and ERG_Server_Node_Supplier=="Honeywell" and (ERG_Server_Node_Type=="SVR_STD_DELL_Tower_RAID1"):
			var21=1
		var23=var20+var21
	return(var23)


#CXCPQ-49207
def getpart_EPCOAW19(Product):
	sum7=sum8=sum9=0
	ARO_System_Required=Product.Attr('ARO_System_Required').GetValue()
	RESS_System_Required=Product.Attr('RESS_System_Required').GetValue()
	if Product.Name == "Experion ARO, RESS & ERG Group":
		aro_release=Product.Attr('ARO_Experion_Software_Release').GetValue()
		ress_release=Product.Attr('RESS_Experion_Software_Release').GetValue()
		aro_station=Product.Attr('ARO_Station_Node_WS').GetValue()
		ress_station=Product.Attr('RESS_Staton_Node').GetValue()
		aro_node_supplier=Product.Attr('ARO_Node_Supplier_WB').GetValue()
		ress__node_supplier=Product.Attr('RESS_Node_Supplier').GetValue()
		aro_additional_station=Product.Attr('Additional_Stations_for_ARO_WS').GetValue()
		Trace.Write(aro_additional_station)
		ress_additional_station=Product.Attr('RESS_Additional_Stations').GetValue()
		release=["R520"]
		hardware=["STN_PER_DELL_Tower_RAID1","STN_PER_DELL_Rack_RAID1","STN_PER_HP_Tower_RAID1"]
		if ARO_System_Required =="Yes" and aro_release in release and aro_node_supplier=="Honeywell" and aro_station in hardware :
			sum8=int(Product.Attr('Additional_Stations_for_ARO_WS').GetValue()) if Product.Attr('Additional_Stations_for_ARO_WS').GetValue()!='' else 0
		if RESS_System_Required =="Yes" and ress_release in release and ress__node_supplier=="Honeywell" and ress_station in hardware  :
			sum9=int(Product.Attr('RESS_Additional_Stations').GetValue()) if Product.Attr('RESS_Additional_Stations').GetValue()!='' else 0
		sum7= int(sum8)+int(sum9)
	return(sum7)
#CXCPQ-49196
def getpart_MZPCSV65(Product):
	var27=var24=var25=var26=0
	ARO_System_Required=Product.Attr('ARO_System_Required').GetValue()
	RESS_System_Required=Product.Attr('RESS_System_Required').GetValue()
	if Product.Name == "Experion ARO, RESS & ERG Group":
		Aro_Tpm=Product.Attr('ARO_Trusted_Platform_Module').GetValue()
		Aro_Tpm1=Product.Attr('ARO_Trusted_Platform_Module_GW').GetValue()
		Aro_Tpm2=Product.Attr('RESS_Trusted_Platform_Module').GetValue()
		Node_Supplier=Product.Attr('ARO_Node_Supplier').GetValue()
		Node_Supplier2=Product.Attr('ARO_Node_Supplier_GW').GetValue()
		Node_Supplier3=Product.Attr('RESS_Node_Supplier_(Server)').GetValue()
		Server_Node_Type=Product.Attr('ARO_Server_Node_Type').GetValue()
		Server_Node_Type2=Product.Attr('ARO_Server_Node_Type_GW').GetValue()
		Server_Node_Type3=Product.Attr('RESS_Server_Node_Type').GetValue()
		if ARO_System_Required =="Yes" and Aro_Tpm=="Yes" and Node_Supplier=="Honeywell" and (Server_Node_Type=="SVR_PER_DELL_Rack_RAID5") :
			var24=1
		if ARO_System_Required =="Yes" and Aro_Tpm1=="Yes" and Node_Supplier2=="Honeywell" and (Server_Node_Type2=="SVR_PER_DELL_Rack_RAID5"):
			var25=1
		if RESS_System_Required == "Yes" and Aro_Tpm2=="Yes" and Node_Supplier3=="Honeywell" and (Server_Node_Type3=="SVR_PER_DELL_Rack_RAID5"):
			var26=1
		var27=var24+var25+var26
	return(var27)
#CXCPQ-49195
def getpart_MZPCST82(Product):
	var31=var28=var29=var30=var32=0
	ARO_System_Required=Product.Attr('ARO_System_Required').GetValue()
	RESS_System_Required=Product.Attr('RESS_System_Required').GetValue()
	if Product.Name == "Experion ARO, RESS & ERG Group":
		Aro_Tpm=Product.Attr('ARO_Trusted_Platform_Module').GetValue()
		Aro_Tpm1=Product.Attr('ARO_Trusted_Platform_Module_GW').GetValue()
		Aro_Tpm2=Product.Attr('RESS_Trusted_Platform_Module').GetValue()
		Node_Supplier=Product.Attr('ARO_Node_Supplier').GetValue()
		Node_Supplier2=Product.Attr('ARO_Node_Supplier_GW').GetValue()
		Node_Supplier3=Product.Attr('RESS_Node_Supplier_(Server)').GetValue()
		Server_Node_Type=Product.Attr('ARO_Server_Node_Type').GetValue()
		Server_Node_Type2=Product.Attr('ARO_Server_Node_Type_GW').GetValue()
		Server_Node_Type3=Product.Attr('RESS_Server_Node_Type').GetValue()
		if ARO_System_Required =="Yes" and Aro_Tpm=="No" and Node_Supplier=="Honeywell" and (Server_Node_Type=="SVR_PER_DELL_Tower_RAID1") :
			var28=1
		if ARO_System_Required =="Yes" and Aro_Tpm1=="No" and Node_Supplier2=="Honeywell" and (Server_Node_Type2=="SVR_PER_DELL_Tower_RAID1"):
			var29=1
		if RESS_System_Required == "Yes" and Aro_Tpm2=="No" and Node_Supplier3=="Honeywell" and (Server_Node_Type3=="SVR_PER_DELL_Tower_RAID1"):
			var30=1
		ERG_Sys_Req,erg_swRel,erg_nodeTyp,erg_supl,erg_trstPltf=getERGAttrVal(Product, 'MZPCST82')
		if ERG_Sys_Req=='Yes' and erg_swRel=='R530' and erg_nodeTyp=='SVR_PER_DELL_Tower_RAID1' and erg_supl=='Honeywell' and erg_trstPltf=='No':
			var32=1
		var31=var28+var29+var30+var32
	return(var31)
#CXCPQ-49205
def getpart_MZPCWS77(Product):
	sum1=sum2=sum3=0
	ARO_System_Required=Product.Attr('ARO_System_Required').GetValue()
	RESS_System_Required=Product.Attr('RESS_System_Required').GetValue()
	if Product.Name == "Experion ARO, RESS & ERG Group":
		aro_release=Product.Attr('ARO_Experion_Software_Release').GetValue()
		ress_release=Product.Attr('RESS_Experion_Software_Release').GetValue()
		aro_station=Product.Attr('ARO_Station_Node_WS').GetValue()
		ress_station=Product.Attr('RESS_Staton_Node').GetValue()
		aro_node_supplier=Product.Attr('ARO_Node_Supplier_WB').GetValue()
		ress__node_supplier=Product.Attr('RESS_Node_Supplier').GetValue()
		aro_additional_station=Product.Attr('Additional_Stations_for_ARO_WS').GetValue()
		ress_additional_station=Product.Attr('RESS_Additional_Stations').GetValue()
		if ARO_System_Required =="Yes" and aro_release=="R520" and aro_node_supplier=="Honeywell" and aro_station=="STN_PER_DELL_Rack_RAID1" :
			sum2=int(Product.Attr('Additional_Stations_for_ARO_WS').GetValue()) if Product.Attr('Additional_Stations_for_ARO_WS').GetValue()!='' else 0
		if RESS_System_Required =="Yes" and ress_release=="R520" and ress__node_supplier=="Honeywell" and ress_station=="STN_PER_DELL_Rack_RAID1" :
			sum3=int(Product.Attr('RESS_Additional_Stations').GetValue()) if Product.Attr('RESS_Additional_Stations').GetValue()!='' else 0
		sum1= int(sum2)+int(sum3)
	return(sum1)
#CXCPQ-50323
def getpart_MZPCSR82(Product):
	var57=var54=var55=var56=0
	ARO_System_Required=Product.Attr('ARO_System_Required').GetValue()
	RESS_System_Required=Product.Attr('RESS_System_Required').GetValue()
	if Product.Name == "Experion ARO, RESS & ERG Group":
		Aro_Tpm=Product.Attr('ARO_Trusted_Platform_Module').GetValue()
		Aro_Tpm1=Product.Attr('ARO_Trusted_Platform_Module_GW').GetValue()
		Aro_Tpm2=Product.Attr('RESS_Trusted_Platform_Module').GetValue()
		Node_Supplier=Product.Attr('ARO_Node_Supplier').GetValue()
		Node_Supplier2=Product.Attr('ARO_Node_Supplier_GW').GetValue()
		Node_Supplier3=Product.Attr('RESS_Node_Supplier_(Server)').GetValue()
		Server_Node_Type=Product.Attr('ARO_Server_Node_Type').GetValue()
		Server_Node_Type2=Product.Attr('ARO_Server_Node_Type_GW').GetValue()
		Server_Node_Type3=Product.Attr('RESS_Server_Node_Type').GetValue()
		if ARO_System_Required =="Yes" and Aro_Tpm=="No" and Node_Supplier=="Honeywell" and (Server_Node_Type=="SVR_PER_DELL_Rack_RAID1") :
			var54=1
		if ARO_System_Required =="Yes" and Aro_Tpm1=="No" and Node_Supplier2=="Honeywell" and (Server_Node_Type2=="SVR_PER_DELL_Rack_RAID1"):
			var55=1
		if RESS_System_Required == "Yes" and Aro_Tpm2=="No" and Node_Supplier3=="Honeywell" and (Server_Node_Type3=="SVR_PER_DELL_Rack_RAID1"):
			var56=1
		var57=var54+var55+var56
	return(var57)
#CXCPQ-49181
def getpart_MZPCSV84(Product):
	var47=var44=var45=var46=0
	ARO_System_Required=Product.Attr('ARO_System_Required').GetValue()
	RESS_System_Required=Product.Attr('RESS_System_Required').GetValue()
	if Product.Name == "Experion ARO, RESS & ERG Group":
		Aro_Tpm=Product.Attr('ARO_Trusted_Platform_Module').GetValue()
		Aro_Tpm1=Product.Attr('ARO_Trusted_Platform_Module_GW').GetValue()
		Aro_Tpm2=Product.Attr('RESS_Trusted_Platform_Module').GetValue()
		Node_Supplier=Product.Attr('ARO_Node_Supplier').GetValue()
		Node_Supplier2=Product.Attr('ARO_Node_Supplier_GW').GetValue()
		Node_Supplier3=Product.Attr('RESS_Node_Supplier_(Server)').GetValue()
		Server_Node_Type=Product.Attr('ARO_Server_Node_Type').GetValue()
		Server_Node_Type2=Product.Attr('ARO_Server_Node_Type_GW').GetValue()
		Server_Node_Type3=Product.Attr('RESS_Server_Node_Type').GetValue()
		if ARO_System_Required =="Yes" and Aro_Tpm=="Yes" and Node_Supplier=="Honeywell" and (Server_Node_Type=="SVR_PER_HP_Rack_RAID5") :
			var44=1
		if ARO_System_Required =="Yes" and Aro_Tpm1=="Yes" and Node_Supplier2=="Honeywell" and (Server_Node_Type2=="SVR_PER_HP_Rack_RAID5"):
			var45=1
		if RESS_System_Required == "Yes" and Aro_Tpm2=="Yes" and Node_Supplier3=="Honeywell" and (Server_Node_Type3=="SVR_PER_HP_Rack_RAID5"):
			var46=1
		var47=var44+var45+var46
	return(var47)
#CXCPQ-49190
def getpart_MZPCIS02(Product):
	var35=var32=var33=var34=0
	ARO_System_Required=Product.Attr('ARO_System_Required').GetValue()
	RESS_System_Required=Product.Attr('RESS_System_Required').GetValue()
	if Product.Name == "Experion ARO, RESS & ERG Group":
		Aro_Tpm=Product.Attr('ARO_Trusted_Platform_Module').GetValue()
		Aro_Tpm1=Product.Attr('ARO_Trusted_Platform_Module_GW').GetValue()
		Aro_Tpm2=Product.Attr('RESS_Trusted_Platform_Module').GetValue()
		RESS_server_req_Phy_hw=Product.Attr('RESS_server_require_Physical_hardware').GetValue() #CXCPQ-112913
		RESS_Sw_Rel=Product.Attr('RESS_Experion_Software_Release').GetValue() #CXCPQ-112913
		Node_Supplier=Product.Attr('ARO_Node_Supplier').GetValue()
		Node_Supplier2=Product.Attr('ARO_Node_Supplier_GW').GetValue()
		Node_Supplier3=Product.Attr('RESS_Node_Supplier_(Server)').GetValue()
		Server_Node_Type=Product.Attr('ARO_Server_Node_Type').GetValue()
		Server_Node_Type2=Product.Attr('ARO_Server_Node_Type_GW').GetValue()
		Server_Node_Type3=Product.Attr('RESS_Server_Node_Type').GetValue()
        #CXCPQ-112861 Start
        ARO_server_req_Phy_hw=Product.Attr('ARO_server_require_Physical_hardware').GetValue()
        ARO_Gateway_req_Phy_hw=Product.Attr('ARO_Gateway_require_Physical_hardware').GetValue()
        if ARO_System_Required =="Yes" and Node_Supplier == 'Honeywell' and ARO_server_req_Phy_hw == 'Yes' and Server_Node_Type == 'SVR_PER_DELL_Rack_RAID1_RUG' and Aro_Tpm == 'Yes':
			var32 = 1
        if ARO_System_Required =="Yes" and Node_Supplier2 == 'Honeywell' and ARO_Gateway_req_Phy_hw == 'Yes' and Server_Node_Type2 == 'SVR_PER_DELL_Rack_RAID1_RUG' and Aro_Tpm1 == 'Yes':
			var33 = 1
		#CXCPQ-112861 End
        if RESS_System_Required == "Yes" and RESS_Sw_Rel in ('R520','R530') and RESS_server_req_Phy_hw=="Yes" and Aro_Tpm2=="Yes" and Node_Supplier3=="Honeywell" and Server_Node_Type3=="SVR_PER_DELL_Rack_RAID1_RUG": #if RESS_System_Required == "Yes" and Aro_Tpm2=="Yes" and Node_Supplier3=="Honeywell" and (Server_Node_Type3=="SVR_PER_DELL_Rack_RAID1_RUG") #CXCPQ-112913
			var34=1
        var35=var32+var33+var34
	return(var35)
#CXCPQ-49178
def getpart_EPCOAS19(Product):
	var39=var36=var37=var38=0
	ARO_System_Required=Product.Attr('ARO_System_Required').GetValue()
	RESS_System_Required=Product.Attr('RESS_System_Required').GetValue()
	if Product.Name == "Experion ARO, RESS & ERG Group":
		Aro_Software=Product.Attr('ARO_Experion_Software_Release').GetValue()
		Aro_Software1=Product.Attr('ARO_Experion_Software_Release').GetValue()
		Aro_Software2=Product.Attr('RESS_Experion_Software_Release').GetValue()
		Node_Supplier=Product.Attr('ARO_Node_Supplier').GetValue()
		Node_Supplier2=Product.Attr('ARO_Node_Supplier_GW').GetValue()
		Node_Supplier3=Product.Attr('RESS_Node_Supplier_(Server)').GetValue()
		Server_Node_Type=Product.Attr('ARO_Server_Node_Type').GetValue()
		Server_Node_Type2=Product.Attr('ARO_Server_Node_Type_GW').GetValue()
		Server_Node_Type3=Product.Attr('RESS_Server_Node_Type').GetValue()
		if ARO_System_Required =="Yes" and Aro_Software=="R520" and Node_Supplier=="Honeywell" and Server_Node_Type :
			var36=1
		if ARO_System_Required =="Yes" and Aro_Software=="R520" and Node_Supplier2=="Honeywell" and Server_Node_Type2:
			var37=1
		if RESS_System_Required == "Yes" and Aro_Software2=="R520" and Node_Supplier3=="Honeywell" and Server_Node_Type3: #CXCPQ-112914
			var38=1
		var39=var36+var37+var38
	return(var39)
def getpart_EPCOAS22(Product):
	var4=var3=var1=var2=0 #CXCPQ-112914
	if Product.Name == "Experion ARO, RESS & ERG Group":
		RESS_System_Required,RESS_Sw_Rel,RESS_server_req_Phy_hw,RESS_Tpm,RESS_Node_Supplier,RESS_Server_Node_Type,ERG_Sys_Req,erg_swRel,erg_cb_nodeTyp,erg_nodeTyp,erg_cb_supl,erg_supl,erg_cb_trstPltf,erg_trstPltf,aro_release,ARO_server_req_Phy_hw,Server_Node_Type,Node_Supplier,ARO_Gateway_req_Phy_hw,Server_Node_Type2,Node_Supplier2=getERGAttrVal(Product, 'EPCOAS22')
		if ERG_Sys_Req=='Yes' and erg_swRel=='R530' and erg_cb_nodeTyp in ('SVR_STD_DELL_Tower_RAID1','SVR_STD_DELL_Rack_RAID1') and erg_cb_supl=='Honeywell' and erg_cb_trstPltf in ('Yes','No'):
			var1=1
		if ERG_Sys_Req=='Yes' and erg_swRel=='R530' and erg_nodeTyp in ('SVR_STD_DELL_Tower_RAID1','SVR_STD_DELL_Rack_RAID1','SVR_PER_DELL_Tower_RAID1','SVR_PER_DELL_Rack_RAID1_XE') and erg_supl=='Honeywell' and erg_trstPltf in ('Yes','No'):
			var2=1
		if RESS_System_Required == "Yes" and RESS_Sw_Rel == 'R530' and RESS_server_req_Phy_hw == "Yes" and RESS_Node_Supplier == "Honeywell" and RESS_Server_Node_Type: #CXCPQ-112914
			var3=1
		if aro_release == 'R530':
			if ARO_server_req_Phy_hw == "Yes" and Node_Supplier == "Honeywell" and Server_Node_Type:
				var3+=1
			if ARO_Gateway_req_Phy_hw == "Yes" and Node_Supplier2 == "Honeywell" and Server_Node_Type2:
				var3+=1
		var4=var1+var2+var3 #CXCPQ-112914
	return(var4)
def getpart_MZPCSR03(Product):
	var3=var1=var2=0 #CXCPQ-112913
	if Product.Name == "Experion ARO, RESS & ERG Group":
		RESS_System_Required,RESS_Sw_Rel,RESS_server_req_Phy_hw,RESS_Tpm,RESS_Node_Supplier,RESS_Server_Node_Type,ERG_Sys_Req,erg_swRel,erg_nodeTyp,erg_supl,erg_trstPltf=getERGAttrVal(Product, 'MZPCSR03') #CXCPQ-112913
		if ERG_Sys_Req=='Yes' and erg_swRel=='R530' and erg_nodeTyp in ('SVR_PER_DELL_Rack_RAID1_XE') and erg_supl=='Honeywell' and erg_trstPltf=='Yes':
			var1=1
		if RESS_System_Required == "Yes" and RESS_Sw_Rel in ('R520','R530') and RESS_server_req_Phy_hw == "Yes" and RESS_Tpm == "Yes" and RESS_Node_Supplier == "Honeywell" and RESS_Server_Node_Type == "SVR_PER_DELL_Rack_RAID1_XE": #CXCPQ-112913
			var2=1
		var3=var1+var2
	return(var3) # CXCPQ-112913
def getpart_MZPCST02(Product):
	var1=0
	if Product.Name == "Experion ARO, RESS & ERG Group":
		ERG_Sys_Req,erg_swRel,erg_nodeTyp,erg_supl,erg_trstPltf=getERGAttrVal(Product, 'MZPCST02')
		if ERG_Sys_Req=='Yes' and erg_swRel=='R530' and erg_nodeTyp in ('SVR_PER_DELL_Tower_RAID1') and erg_supl=='Honeywell' and erg_trstPltf=='Yes':
			var1=1
	return(var1)
