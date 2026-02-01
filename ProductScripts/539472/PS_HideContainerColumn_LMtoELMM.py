def getAttributeValue(Name):
	return Product.Attr(Name).GetValue()

def getContainer(Name):
	return Product.GetContainerByName(Name)

def hideColumn(container,Column):
	Product.ParseString('<*CTX( Container({}).Column({}).SetPermission(Hidden) )*>'.format(container,Column))
	Product.ParseString('<*CTX( Container({}).Row(1).Column({}).Set() )*>'.format(container,Column))

def setDefaultColumnForDropdown(container,Column, value):
	Product.ParseString('<*CTX( Container({}).Row(1).Column({}).Set({}) )*>'.format(container,Column, value))
	
def show_attribute(attributename):
	Product.AllowAttr(attributename)
	
def GetAttributePermission(name):
	return Product.Attr(name).Allowed
	
def hide_attribute(attributename):
	Product.DisallowAttr(attributename)

def visibleColumn(container,Column):
	Product.ParseString('<*CTX( Container({}).Column({}).SetPermission(Editable) )*>'.format(container,Column))

def isHidden(container,Column):
	return Product.ParseString('<*CTX( Container({}).Column({}).GetPermission )*>'.format(container,Column)) == 'Hidden'

def getContainer(Name):
	return Product.GetContainerByName(Name)

if Product.Name =="LM to ELMM ControlEdge PLC":
	if getAttributeValue("Scope") in ["LABOR"]:
		hide_attribute("LM_to_ELMM_Experion_Release")
		hide_attribute("ATT_LM_ELMM_DOES_THE_CUSTOMERTPN_RELEASE")
		hideColumn("LM_to_ELMM_ControlEdge_PLC_Cont", "LM_CE_Power_Input_Type")
		hideColumn("LM_to_ELMM_ControlEdge_PLC_Cont", "LM_select_IO_network_topology")
		hideColumn("LM_to_ELMM_ControlEdge_PLC_Cont", "LM_select_type_of_Switch_for_the_IO_network")
		container = Product.GetContainerByName('LM_to_ELMM_3rd_Party_Items')
		count = container.Rows.Count
		if count:
			for row in range(count,-1,-1):
				container.DeleteRow(row)
			container.Calculate()
	elif getAttributeValue("Scope") in ["HW/SW", "HW/SW/LABOR"]:
		if not GetAttributePermission("LM_to_ELMM_Experion_Release"):
			show_attribute("LM_to_ELMM_Experion_Release")
			#setDefaultColumnForDropdown("LM_to_ELMM_ControlEdge_PLC_Migration_Gen_Cont", "LM_Current_Experion_Release", "No Experion")
			Product.Attr("LM_to_ELMM_Experion_Release").SelectDisplayValue("No Experion")
		if not GetAttributePermission("ATT_LM_ELMM_DOES_THE_CUSTOMERTPN_RELEASE"):
			show_attribute("ATT_LM_ELMM_DOES_THE_CUSTOMERTPN_RELEASE")
			#setDefaultColumnForDropdown("LM_to_ELMM_ControlEdge_PLC_Migration_Gen_Cont", "LM_Does_The_Customer_Have_TPN_Release_R688.1_Or_Later", "No")
			Product.Attr("ATT_LM_ELMM_DOES_THE_CUSTOMERTPN_RELEASE").SelectDisplayValue("No")
		if isHidden("LM_to_ELMM_ControlEdge_PLC_Cont", "LM_CE_Power_Input_Type"):
			visibleColumn("LM_to_ELMM_ControlEdge_PLC_Cont", "LM_CE_Power_Input_Type")
			setDefaultColumnForDropdown("LM_to_ELMM_ControlEdge_PLC_Cont", "LM_CE_Power_Input_Type", "DC")
		if isHidden("LM_to_ELMM_ControlEdge_PLC_Cont", "LM_select_IO_network_topology"):
			visibleColumn("LM_to_ELMM_ControlEdge_PLC_Cont", "LM_select_IO_network_topology")
			setDefaultColumnForDropdown("LM_to_ELMM_ControlEdge_PLC_Cont", "LM_select_IO_network_topology", "Star")
		if isHidden("LM_to_ELMM_ControlEdge_PLC_Cont", "LM_select_type_of_Switch_for_the_IO_network"):
			visibleColumn("LM_to_ELMM_ControlEdge_PLC_Cont", "LM_select_type_of_Switch_for_the_IO_network")
			setDefaultColumnForDropdown("LM_to_ELMM_ControlEdge_PLC_Cont", "LM_select_type_of_Switch_for_the_IO_network", "Multimode Redundant")
		container = Product.GetContainerByName('LM_to_ELMM_3rd_Party_Items')
		count = container.Rows.Count
		if count == 0:
			for i in range(0,2):
				container.AddNewRow()
			container.Calculate()
	if getAttributeValue("Scope") in ["HW/SW"]:
		hideColumn("LM_to_ELMM_Migration_Additional_IO_Cont", "LM_any_unsupported_instruction_in_the_LM_ladder_logic")
		hideColumn("LM_to_ELMM_Migration_Additional_IO_Cont", "qty_3party_customized_ladder_used_in_the_LM_0_100")
		hideColumn("LM_to_ELMM_Migration_Additional_IO_Cont", "qty_IO_points_to_be_rewired_0_5000")
	else:
		visibleColumn("LM_to_ELMM_Migration_Additional_IO_Cont", "LM_any_unsupported_instruction_in_the_LM_ladder_logic")
		visibleColumn("LM_to_ELMM_Migration_Additional_IO_Cont", "qty_3party_customized_ladder_used_in_the_LM_0_100")
		visibleColumn("LM_to_ELMM_Migration_Additional_IO_Cont", "qty_IO_points_to_be_rewired_0_5000")
		
	if getAttributeValue("Scope") in ["HW/SW/LABOR", "LABOR"]:
		container = Product.GetContainerByName('LM_to_ELMM_Services')
		count = container.Rows.Count
		if count == 0:
			container.AddNewRow()
			container.Calculate()
	else:
		container = Product.GetContainerByName('LM_to_ELMM_Services')
		count = container.Rows.Count
		if count:
			container.DeleteRow(0)
		container.Calculate()
	#lMELMMGeneralCont=  getContainer('LM_to_ELMM_ControlEdge_PLC_Migration_Gen_Cont')
	#for row in lMELMMGeneralCont.Rows:
	if getAttributeValue('ATT_LM_ELMM_HONEYWELL_PROVIDE_FTE') == "No" or getAttributeValue('ATT_LM_ELMM_HONEYWELL_PROVIDE_FTE') == "":
		hideColumn('LM_to_ELMM_ControlEdge_PLC_Cont', 'LM_average_Cable_length_for_IO_network_connection')
		hide_attribute('LM_to_ELMM Cable Length')
	else:
		
		if isHidden('LM_to_ELMM_ControlEdge_PLC_Cont', 'LM_average_Cable_length_for_IO_network_connection'):
			visibleColumn('LM_to_ELMM_ControlEdge_PLC_Cont', 'LM_average_Cable_length_for_IO_network_connection')
			
			setDefaultColumnForDropdown('LM_to_ELMM_ControlEdge_PLC_Cont', 'LM_average_Cable_length_for_IO_network_connection', "10m")
		if not GetAttributePermission('LM_to_ELMM Cable Length'):
			show_attribute('LM_to_ELMM Cable Length')
			#setDefaultColumnForDropdown('LM_to_ELMM_ControlEdge_PLC_Migration_Gen_Cont', 'Average_Cable_Length_For_PLC_Uplink', "10m")
			Product.Attr("LM_to_ELMM Cable Length").SelectDisplayValue("10m")
	if getAttributeValue('ATT_LM_ADDITIONALSWITCHES') == "0" or getAttributeValue('ATT_LM_ADDITIONALSWITCHES') == "":
		hide_attribute('ATT_LM_ELMM_ADDITIONAL_SWITCH')
	else:
		if not GetAttributePermission('ATT_LM_ELMM_ADDITIONAL_SWITCH'):
			show_attribute('ATT_LM_ELMM_ADDITIONAL_SWITCH')