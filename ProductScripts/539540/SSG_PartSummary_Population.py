def setAtvQty(Product,AttrName,PartNumber,qty):
	Cont=Product.Attr(AttrName).Values
	for Parts in Cont:
		if Parts.Display == PartNumber:
			Parts.IsSelected=False
			Parts.Quantity = 0
			if qty > 0:
				Parts.IsSelected=True
				Parts.Quantity=qty
				Trace.Write('Selected ' + PartNumber + ' in attribute ' + AttrName + ' at Qty ' + str(qty))
				break



SS_Release = Product.Attr('SS_Experion_PKS_Release').GetValue()
SS_Simulation_Server_required=Product.Attr('SS_Simulation_Server_required').GetValue()
Server_NodeType=Product.Attr('SS_Server_Node_Type').GetValue()
Server_NS = Product.Attr('SS_Node_Supplier').GetValue()
Server_TPM=Product.Attr('SS_Trusted_Platform_Module').GetValue()
SS_Server_Redundancy_Requirement=Product.Attr('SS_Server_Redundancy_Requirement').GetValue()
Server_Qty = 2 if SS_Server_Redundancy_Requirement == "Redundant" else 1

SS_Simulation_PC_Station_required=Product.Attr('SS_Simulation_PC_Station_required').GetValue()
Station_Qty = int(Product.Attr('SS_Number_of_Simulation_PCs_required').GetValue()) if Product.Attr('SS_Number_of_Simulation_PCs_required').GetValue() else 0
Station_NodeType=Product.Attr('SS_Server_Node_Type_Workstation').GetValue()
Station_NodeSupplier = Product.Attr('SS_Node_Supplier_Station').GetValue()
Station_TPM = Product.Attr('SS_Trusted_Platform_Module_Station').GetValue()


qty_MZ_PCSR05 = 0
qty_MZ_PCSR06 = 0
qty_MZ_PCST03 = 0
qty_MZ_PCST04 = 0
qty_TP_FPH552 = 0
qty_MZ_PCWT02 = 0
qty_EP_COAS19 = 0
#qty_MZ_SQLCL4 = 0

flex_stn_desk_qty=int(Product.Attr('SS_Flex_Station_Qty_Desk').GetValue()) if Product.Attr('SS_Flex_Station_Qty_Desk').GetValue() else 0
flex_stn_desk_display=Product.Attr('SS_Display_size_desk').GetValue()
flex_stn_desk_displaysupplier=Product.Attr('SS_Display_Supplier_desk').GetValue()
flex_stn_orion_qty=int(Product.Attr('SS_Flex_Station_Qty_Orion').GetValue()) if Product.Attr('SS_Flex_Station_Qty_Orion').GetValue() else 0
SS_No_of_Displays_desk=int(Product.Attr('SS_No_of_Displays_desk').GetValue()) if Product.Attr('SS_No_of_Displays_desk').GetValue() else 0
base2_total=int(Product.Attr('SS_Orion_Console_2_Position_Base_Unit_Total').GetValue()) if Product.Attr('SS_Orion_Console_2_Position_Base_Unit_Total').GetValue() else 0
base3_total=int(Product.Attr('SS_Orion_Console_3_Position_Base_Unit_Total').GetValue()) if Product.Attr('SS_Orion_Console_3_Position_Base_Unit_Total').GetValue() else 0
flex_orion_display_size=Product.Attr('SS_Orion_Console_Display_Size').GetValue()
flex_orion_node_supplier=Product.Attr('SS_Orion_Console_Display_Supplier').GetValue()
flex_orion_display_device=int(Product.Attr('SS_Orion_Console_Display_Devices').GetValue()) if Product.Attr('SS_Orion_Console_Display_Devices').GetValue() else 0
flex_node_supplier = Product.Attr('SS_Node_Supplier_Desk').GetValue()
flex_station_desk = Product.Attr('SS_Flex Staton  Desk Node_desk').GetValue()
orion_station_node = Product.Attr('SS_Flex_Staton _Orion_Node').GetValue()
orion_node_supplier = Product.Attr('SS_Node_Supplier_orion').GetValue()


if flex_stn_desk_qty > 0 and flex_stn_desk_display == '55 inch NTS' and SS_No_of_Displays_desk > 0 and flex_stn_desk_displaysupplier == 'Honeywell':
	qty_TP_FPH552 = flex_stn_desk_qty
if flex_stn_orion_qty > 0 and flex_orion_node_supplier == 'Honeywell' and flex_orion_display_size == '55 inch NTS':
	qty_TP_FPH552 += (((2*base2_total)+(3*base3_total))*flex_orion_display_device)


if SS_Release in ('R520','R530'):
	if SS_Simulation_Server_required=="Yes" and Server_TPM and Server_NS == 'Honeywell':
		if Server_NodeType == 'SVR_STD_DELL_Rack_RAID1':
			qty_MZ_PCSR05 = Server_Qty
		elif Server_NodeType == 'SVR_PER_DELL_Rack_RAID1':
			qty_MZ_PCSR06 = Server_Qty
		elif Server_NodeType == 'SVR_STD_DELL_Tower_RAID1':
			qty_MZ_PCST03 = Server_Qty
		elif Server_NodeType == 'SVR_PER_DELL_Tower_RAID1':
			qty_MZ_PCST04 = Server_Qty
	if SS_Simulation_PC_Station_required=="Yes" and Station_TPM and Station_NodeSupplier == 'Honeywell':
		if Station_NodeType == 'SVR_STD_DELL_Rack_RAID1':
			qty_MZ_PCSR05 += Station_Qty
		elif Station_NodeType == 'SVR_PER_DELL_Rack_RAID1':
			qty_MZ_PCSR06 += Station_Qty
		elif Station_NodeType == 'SVR_STD_DELL_Tower_RAID1':
			qty_MZ_PCST03 += Station_Qty
		elif Station_NodeType == 'SVR_PER_DELL_Tower_RAID1':
			qty_MZ_PCST04 += Station_Qty

	if SS_Release == 'R520':
		if flex_stn_desk_qty > 0 and flex_station_desk == 'STN_PER_DELL_Tower_RAID2' and flex_node_supplier == 'Honeywell':
			qty_MZ_PCWT02 += flex_stn_desk_qty
			qty_EP_COAS19 += flex_stn_desk_qty
			#qty_MZ_SQLCL4 += flex_stn_desk_qty

		if flex_stn_orion_qty >0 and orion_station_node == 'STN_PER_DELL_Tower_RAID2' and orion_node_supplier == 'Honeywell':
			qty_MZ_PCWT02 += flex_stn_orion_qty
			qty_EP_COAS19 += flex_stn_orion_qty
			#qty_MZ_SQLCL4 += flex_stn_orion_qty

setAtvQty(Product,"Simulation_Bom_parts","MZ-PCSR05",qty_MZ_PCSR05)
setAtvQty(Product,"Simulation_Bom_parts","MZ-PCSR06",qty_MZ_PCSR06)
setAtvQty(Product,"Simulation_Bom_parts","MZ-PCST03",qty_MZ_PCST03)
setAtvQty(Product,"Simulation_Bom_parts","MZ-PCST04",qty_MZ_PCST04)
setAtvQty(Product,"Simulation_Bom_parts","TP-FPH552",qty_TP_FPH552)
setAtvQty(Product,"Simulation_Bom_parts","MZ-PCWT02",qty_MZ_PCWT02)
setAtvQty(Product,"Simulation_Bom_parts","EP-COAS19",qty_EP_COAS19)
#setAtvQty(Product,"Simulation_Bom_parts","MZ-SQLCL4",qty_MZ_SQLCL4)