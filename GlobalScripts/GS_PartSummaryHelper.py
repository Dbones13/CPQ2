import math
def getFloat(var):
	if var:
		return float(var)
	return 0

def getContainer(product, containerName):
	return product.GetContainerByName(containerName)

def addFinalHours(totalDict, key, value):
	totalDict[key] = getFloat(totalDict.get(key, 0)) + getFloat(value)

def setAtvQty(Product,AttrName,sv,qty):
	pvs=Product.Attr(AttrName).Values
	for av in pvs:
		if av.Display == sv:
			av.Quantity = 0
			av.IsSelected=False
			if int(qty) > 0:
				av.IsSelected=True
				av.Quantity=qty
				break

def productAttrMatchingNames():
	return {
			'OPM': {
				'ATT_OPMNUMRESS': 'OPM_No_of_RESS_Remote_Users',
				'ATT_OPMQTYSWTS': 'OPM_Quantity_of_L1_L2_Switches',
				'ATT_OPMQTYBBON': 'OPM_Qty_of_Backbone_or_Agg_Fiber_Optic_Switch',
				'ATT_OPMADNLHRS': 'OPM_Additional_hrs_for_Document_Customization'
			},
			'EBR': {
				'Attr_New/AdditionalServer': 'EBR_Qty_of_EBR_New_Additional_for_Server',
				'Attr_NewAddWorkstation': 'EBR_Qty_of_EBR_New_Additional_for_Workstation',
				'Attr_NewAddVirtual_Node': 'EBR_Qty_of_EBR_New_Additional_for_Virtual_Node',
				'EBR_If_hardware_desired_select_host_type': 'EBR_If_hardware_desired_select_host_type',
				'EBR_Additional_Hard_Drive_required': 'EBR_Additional_Hard_Drive_required',
				'EBR_Additional_Network_Storage_Device_NAS_required': 'EBR_Additional_Network_Storage_Device_NAS_required',
				'EBR_Site_Acceptance_Test_required': 'EBR_Site_Acceptance_Test_required'
			},
			'XP10 Actuator Upgrade': {
				'ATT_XP10ACTUPG': 'XP10_Actuator_Number_of_actuators_to_be_upgraded',
				'XP10_Actuator_current_actuator_model': 'XP10_Actuator_Select_current_actuator_model',
				'XP10_Actuator_current_valve_plug_model': 'XP10_Actuator_Select_current_valve_plug_model',
				'XP10_Actuator_Will_a_seat_removal_tool_be_needed': 'XP10_Actuator_Will_a_seat_removal_tool_be_needed',
				'XP10_Actuator_Will_an_A7_actuator_tool_be_needed': 'XP10_Actuator_Will_an_A7_actuator_tool_be_needed',
				'XP10_Actuator_XP10_seat_adapter_tool_be_needed': 'XP10_Actuator_XP10_seat_adapter_tool_be_needed',
				'XP10_Actuator_XP10_adapter_tool_be_needed': 'XP10_Actuator_XP10_adapter_tool_be_needed'
			},
			'xPM to C300 Migration': {
				'xPM_C300_Cabinet_Doors': 'xPM_C300_Cabinet_Doors',
				'xPM_C300_Cabinet_Hinge_Type': 'xPM_C300_Cabinet_Hinge_Type',
				'xPM_C300_Cabinet_Light_Required': 'xPM_C300_Cabinet_Light_Required',
				'xPM_C300_Cabinet_Thermostat_Required': 'xPM_C300_Cabinet_Thermostat_Required',
				'xPM_C300_Cabinet_Keylock_Type': 'xPM_C300_Cabinet_Keylock_Type',
				'xPM_C300_TDI_Power_Supply_Cable_Length': 'xPM_C300_Power_Entry',
				'xPM_C300_Cabinet_Color': 'xPM_C300_Cabinet_Color',
				'C200_C300_Fan_Voltage': 'C200_C300_Fan_Voltage',
				'C200_C300_Cabinet_Base_Required': 'C200_C300_Cabinet_Base_Required',
				'Power System Vendor': 'Power System Vendor','Power System Type': 'Power System Type'},
				'C200 Migration': {'C200_Select_Migration_Scenario': 'C200_Select_the_Migration_Scenario'},
				'FSC to SM': {'ATT_FSC_to_SM_Number_of_configurations': 'FSC_to_SM_Number_of_configurations_to_be_migrated'
			},
			'FDM Upgrade 1': {
				'FDM_Upgrade_What_is_the_current_release': 'FDM_Upgrade_What_is_the_current_release_of_the_system_to_be_upgraded',
				'FDM_Upgrade_Select_desired_FDM_release': 'FDM_Upgrade_Select_desired_FDM_release',
				'FDM_Upgrade_FDM_Media_Delivery': 'FDM_Upgrade_FDM_Media_Delivery',
				'Attr_FDM_Upg_FDMsUpgraded': 'FDM_Upgrade_Number_of_FDMs_to_be_Upgraded',
				'FDM_Upgrade_Additional_Components': 'FDM_Upgrade_Additional_Components_to_be_offered_for_number_of_FDMs_?',
				'Attr_FDM_Upg1ServerDevicePoints': 'FDM_Upgrade_Total_number_of_Server_Device_Points',
				'Attr_FDMUpg1_AuditTrailDev': 'FDM_Upgrade_Total_number_of_Audit_Trail_Devices',
				'Attr_FDMUpg1_RCIs_excExperion': 'FDM_Upgrade_Total_RCIs_excluding_Experion_PKS_Server_Interfaces',
				'Attr_FDMUpg1_RCIs_incExperion': 'FDM_Upgrade_Total_RCIs_including_Experion_PKS_Server_Interfaces',
				'Attr_FDM_Upg1_TotalFDMClients': 'FDM_Upgrade_Total_FDM_Clients',
				'Attr_FDM_Upg_HdwareMultiplexer': 'FDM_Upgrade_Total_Server_Hardware_Multiplexer_Licenses',
				'Attr_FDM_Upg_Multiplexer': 'FDM_Upgrade_Total_Multiplexer_Monitoring_Network_Licenses',
				'Attr_FDM_Upg_Dummy': 'FDM_Upgrade_Dummy',
				'Attr_FDMClientStation': 'FDM_Upgrade_Number_of_FDM_Client_Station_PCs',
				'Attr_FDMRCIPCs': 'FDM_Upgrade_Number_of_FDM_RCI_PCs',
				'Attr_FDMGatewayPCs': 'FDM_Upgrade_Number_of_FDM_Gateway_PCs',
				'Attr_FDM_Upg_devmanaged': 'FDM_Upgrade_How_many_devices_will_be_managed',
				'Attr_FDM_Upg_AuditTrailDev': 'FDM_Upgrade_Number_of_Audit_Trail_Devices',
				'Attr_FDM_Upg_HARTdevvendors': 'FDM_Upgrade_Number_of_HART_devices_from_device_vendors',
				'Attr_FDMUpg_FDMClients': 'FDM_Upgrade_Number_of_FDM_Clients',
				'Attr_Experion/TPS_Servers_FDMInt': 'FDM_Upgrade_Number_of_Experion_TPS_Servers_for_FDM_Integration',
				'Attr_ServerNetInterfaceLic': 'FDM_Upgrade_Number_of_Server_Network_Interface_Licenses_Add',
				'Attr_HWMUX_Net_MonitoringLic': 'FDM_Upgrade_Number_of_HART_Hardware_MUX_Network_Monitoring_Licenses',
				'Attr_ExpServer_processI/Opoint': 'FDM_Upgrade_Number_of_Experion_Server_process_IO_point_licenses',
				'Attr_remPCs_FDMServerviaLAN': 'FDM_Upgrade_Number_of_remote_PCs_connecting_to_FDM_Serve_ via_LAN',
				'Attr_PVST_HARTESD': 'FDM_Upgrade_Number_of_PVST_Planner_Licenses_for_supported_HART_ESD_Devices'
			},
			'FDM Upgrade 2': {
				'FDM_Upgrade_What_is_the_current_release': 'FDM_Upgrade_2_What_is_the_current_release_of_the_system_to_be_upgraded',
				'FDM_Upgrade_Select_desired_FDM_release': 'FDM_Upgrade_2_Select_desired_FDM_release',
				'FDM_Upgrade_FDM_Media_Delivery': 'FDM_Upgrade_2_FDM_Media_Delivery',
				'Attr_FDM_Upg_FDMsUpgraded': 'FDM_Upgrade_2_Number_of_FDMs_to_be_Upgraded',
				'FDM_Upgrade_Additional_Components': 'FDM_Upgrade_2_Additional_Components_to_be_offered_for_number_of_FDMs_?',
				'Attr_FDM_Upg_devmanaged': 'FDM_Upgrade_How_many_devices_will_be_managed',
				'Attr_FDM_Upg_AuditTrailDev': 'FDM_Upgrade_Number_of_Audit_Trail_Devices',
				'Attr_FDM_Upg_HARTdevvendors': 'FDM_Upgrade_Number_of_HART_devices_from_device_vendors',
				'Attr_FDMUpg_FDMClients': 'FDM_Upgrade_Number_of_FDM_Clients',
				'Attr_Experion/TPS_Servers_FDMInt': 'FDM_Upgrade_Number_of_Experion_TPS_Servers_for_FDM_Integration',
				'Attr_ServerNetInterfaceLic': 'FDM_Upgrade_Number_of_Server_Network_Interface_Licenses_Add',
				'Attr_HWMUX_Net_MonitoringLic': 'FDM_Upgrade_Number_of_HART_Hardware_MUX_Network_Monitoring_Licenses',
				'Attr_ExpServer_processI/Opoint': 'FDM_Upgrade_Number_of_Experion_Server_process_IO_point_licenses',
				'Attr_remPCs_FDMServerviaLAN': 'FDM_Upgrade_Number_of_remote_PCs_connecting_to_FDM_Serve_ via_LAN','Attr_PVST_HARTESD': 'FDM_Upgrade_Number_of_PVST_Planner_Licenses_for_supported_HART_ESD_Devices',
				'Attr_FDMClientStation': 'FDM_Upgrade_2_Number_of_FDM_Client_Station_PCs',
				'Attr_FDMRCIPCs': 'FDM_Upgrade_2_Number_of_FDM_RCI_PCs',
				'Attr_FDMGatewayPCs': 'FDM_Upgrade_2_Number_of_FDM_Gateway_PCs',
				'Attr_FDM_Upg1ServerDevicePoints': 'FDM_Upgrade_Total_number_of_Server_Device_Points',
				'Attr_FDMUpg1_AuditTrailDev': 'FDM_Upgrade_Total_number_of_Audit_Trail_Devices',
				'Attr_FDMUpg1_RCIs_excExperion': 'FDM_Upgrade_Total_RCIs_excluding_Experion_PKS_Server_Interfaces',
				'Attr_FDMUpg1_RCIs_incExperion': 'FDM_Upgrade_Total_RCIs_including_Experion_PKS_Server_Interfaces',
				'Attr_FDM_Upg1_TotalFDMClients': 'FDM_Upgrade_Total_FDM_Clients',
				'Attr_FDM_Upg_HdwareMultiplexer': 'FDM_Upgrade_Total_Server_Hardware_Multiplexer_Licenses',
				'Attr_FDM_Upg_Multiplexer': 'FDM_Upgrade_Total_Multiplexer_Monitoring_Network_Licenses',
				'Attr_FDM_Upg_Dummy': 'FDM_Upgrade_Dummy',
				'FDM_Upgrade_Will_Honeywell_provide_the_FDM_server':'FDM_Upgrade_2_Will_Honeywell_provide_the_FDM_server',
				'FDM_Upgrade_FDM_Gateway_PC_Hardware_Selection':'FDM_Upgrade_2_FDM_Gateway_PC_Hardware_Selection'
			},
			'FDM Upgrade 3': {
				'FDM_Upgrade_What_is_the_current_release': 'FDM_Upgrade_3_What_is_the_current_release_of_the_system_to_be_upgraded',
				'FDM_Upgrade_Select_desired_FDM_release': 'FDM_Upgrade_3_Select_desired_FDM_release',
				'FDM_Upgrade_FDM_Media_Delivery': 'FDM_Upgrade_3_FDM_Media_Delivery',
				'Attr_FDM_Upg_FDMsUpgraded': 'FDM_Upgrade_3_Number_of_FDMs_to_be_Upgraded',
				'FDM_Upgrade_Additional_Components': 'FDM_Upgrade_3_Additional_Components_to_be_offered_for_number_of_FDMs_?',
				'Attr_FDM_Upg_devmanaged': 'FDM_Upgrade_How_many_devices_will_be_managed',
				'Attr_FDM_Upg_AuditTrailDev': 'FDM_Upgrade_Number_of_Audit_Trail_Devices',
				'Attr_FDM_Upg_HARTdevvendors': 'FDM_Upgrade_Number_of_HART_devices_from_device_vendors',
				'Attr_FDMUpg_FDMClients': 'FDM_Upgrade_Number_of_FDM_Clients',
				'Attr_Experion/TPS_Servers_FDMInt': 'FDM_Upgrade_Number_of_Experion_TPS_Servers_for_FDM_Integration',
				'Attr_ServerNetInterfaceLic': 'FDM_Upgrade_Number_of_Server_Network_Interface_Licenses_Add',
				'Attr_HWMUX_Net_MonitoringLic': 'FDM_Upgrade_Number_of_HART_Hardware_MUX_Network_Monitoring_Licenses',
				'Attr_ExpServer_processI/Opoint': 'FDM_Upgrade_Number_of_Experion_Server_process_IO_point_licenses',
				'Attr_remPCs_FDMServerviaLAN': 'FDM_Upgrade_Number_of_remote_PCs_connecting_to_FDM_Serve_ via_LAN',
				'Attr_PVST_HARTESD': 'FDM_Upgrade_Number_of_PVST_Planner_Licenses_for_supported_HART_ESD_Devices',
				'Attr_FDMClientStation': 'FDM_Upgrade_3_Number_of_FDM_Client_Station_PCs',
				'Attr_FDMRCIPCs': 'FDM_Upgrade_3_Number_of_FDM_RCI_PCs',
				'Attr_FDMGatewayPCs': 'FDM_Upgrade_3_Number_of_FDM_Gateway_PCs',
				'Attr_FDM_Upg1ServerDevicePoints': 'FDM_Upgrade_Total_number_of_Server_Device_Points',
				'Attr_FDMUpg1_AuditTrailDev': 'FDM_Upgrade_Total_number_of_Audit_Trail_Devices',
				'Attr_FDMUpg1_RCIs_excExperion': 'FDM_Upgrade_Total_RCIs_excluding_Experion_PKS_Server_Interfaces',
				'Attr_FDMUpg1_RCIs_incExperion': 'FDM_Upgrade_Total_RCIs_including_Experion_PKS_Server_Interfaces',
				'Attr_FDM_Upg1_TotalFDMClients': 'FDM_Upgrade_Total_FDM_Clients',
				'Attr_FDM_Upg_HdwareMultiplexer': 'FDM_Upgrade_Total_Server_Hardware_Multiplexer_Licenses',
				'Attr_FDM_Upg_Multiplexer': 'FDM_Upgrade_Total_Multiplexer_Monitoring_Network_Licenses',
				'Attr_FDM_Upg_Dummy': 'FDM_Upgrade_Dummy',
				'FDM_Upgrade_Will_Honeywell_provide_the_FDM_server':'FDM_Upgrade_3_Will_Honeywell_provide_the_FDM_server',
				'FDM_Upgrade_FDM_Gateway_PC_Hardware_Selection':'FDM_Upgrade_3_FDM_Gateway_PC_Hardware_Selection'
			},
			'EHPM/EHPMX/ C300PM': {
				'xPM_Customer_requires_Fiber_Communication': 'xPM_Customer_requires_Fiber_Communication',
				'xPM_Distance_of_Fiber_Optic_Extenders': 'xPM_Distance_of_Fiber_Optic_Extenders',
				'ATT_QRPCF9IOTA': 'xPM_Qty_of_Red_pair_of_CF9_firewalls',
				'ATT_QARPCF9IOTA': 'xPM_Qty_Additional_Red_pair_of_CF9_firewalls',
				'ATT_QFTENK': 'xPM_Qty_of_FTE_Networks_kits',
				'xPM_NIMsconf': 'xPM_Number_of_NIMs_configurations_to_be_migrated',
				'xPM_DNCFLPCN': 'xPM_Number_of_DNCF_long_power_cable_needed',
				'xPM_NUMDNCF': 'xPM_Number_of_DNCF_needed'
			},
			'TCMI': {
				'TCMI_Is_Triconex_SMM_being_migrated_with_xPM_in': 'TCMI_Is_Triconex_SMM_being_migrated_with_xPM_in'
			},
			'TPS to Experion': {
				'ATT_IS_Migration_Part_Of_ELCN_Migration': 'IS_Migration_Part_Of_ELCN_Migration',
				'TPS_EX_Setup_FTE_Network_Infrastructure': 'Setup_FTE_Network_Infrastructure',
				'TPS_EX_FTE_Switch_Type': 'FTE_Switch_Type',
				'TPS_EX_Additional_Switches': 'Additional_Switches',
				'TPS_EX_QTY_New_Cabinates': 'QTY_New_Cabinates',
				'TPS_EX_Media_Kit_Type': 'TPS_EX_Media_Kit_Type',
				'TPS_EX_Additional_Server_Stations_Required': 'Additional_Server_ESV_Stations_ESF_ESC_ESF_Required',
				'TPS_EX_Cabinet_Depth_Size': 'TPS_EX_Cabinet_Depth_Size',
				'TPS_EX_Power_Supply_Voltage': 'TPS_EX_Power_Supply_Voltage',
				'TPS_EX_Cabinet_Door_Type': 'TPS_EX_Cabinet_Door_Type',
				'TPS_EX_Cabinet_Keylock_Type': 'TPS_EX_Cabinet_Keylock_Type',
				'TPS_EX_Cabinet_Hinge_Type': 'TPS_EX_Cabinet_Hinge_Type',
				'TPS_EX_Cabinet_Thermostat_Required': 'TPS_EX_Cabinet_Thermostat_Required',
				'TPS_EX_Cabinet_Base_Required': 'TPS_EX_Cabinet_Base_Required',
				'TPS_EX_Cabinet_Color': 'TPS_EX_Cabinet_Color',
				'TPS_EX_TDC_US_ESVT': 'TPS_EX_TDC_US_ESVT',
				'TPS_EX_TDC_AM_ESVT': 'TPS_EX_TDC_AM_ESVT',
				'TPS_EX_TDC_APP_ESVT': 'TPS_EX_TDC_APP_ESVT',
				'TPS_EX_TDC_GUS_ESVT': 'TPS_EX_TDC_GUS_ESVT',
				'TPS_EX_ESVT_WO_Trade_Ins': 'TPS_EX_ESVT_WO_Trade_Ins',
				'TPS_EX_ESVT_Redundant': 'TPS_EX_ESVT_Redundant',
				'TPS_EX_ESVT_Server_Hardware': 'TPS_EX_ESVT_Server_Hardware',
				'TPS_EX_Additional_Hard_Drives': 'TPS_EX_Additional_Hard_Drives',
				'TPS_EX_Qty_Of_Cabinet_Slide_Mounting_For_Servers': 'TPS_EX_Qty_Of_Cabinet_Slide_Mounting_For_Servers',
				'TPS_EX_Qty_Of_Cabinet_Fix_Mounting_For_Servers': 'TPS_EX_Qty_Of_Cabinet_Fix_Mounting_For_Servers'
			},
			'LM to ELMM ControlEdge PLC': {
				'LM_to_ELMM_FTE_Switch_To_Connect_ControlEdge_PLC': 'LM_FTE_Switch_To_Connect_ControlEdge_PLC',
				'LM_to_ELMM_Experion_Release': 'LM_Current_Experion_Release',
				'ATT_LM_ELMM_DOES_THE_CUSTOMERTPN_RELEASE': 'LM_Does_The_Customer_Have_TPN_Release_R688.1_Or_Later',
				'ATT_LM_ADDITIONALSWITCHES': 'LM_Number_Of_Additional_Switches',
				'ATT_LM_ELMM_ADDITIONAL_SWITCH': 'LM_Additional_Switch_Selection',
				'ATT_LM_ELMM_HONEYWELL_PROVIDE_FTE': 'Is_Honeywell_Providing_FTE_Cables',
				'LM_to_ELMM Cable Length': 'Average_Cable_Length_For_PLC_Uplink',
				'ATT_LM_QTY_OF_LMPAIR_TOBE_MIGRATED': 'LM_Qty_Of_LM_Pair_To_Be_Migrated',
				'LM_to_ELMM_ControlEdge_PLC_Operating_temperature': 'LM_to_ELMM_ControlEdge_PLC_Operating_temperature'
			}
		}

def cal16k (value):
	list1 = ["16k","8k","4k","2k","1k","512","256","128","064","032","016"]
	partDict = {}
	for x in list1:
		partDict[x]=0

	if 15984 < value <= 16000:
		partDict["16k"] = 1
	else:
		if 8176<value <=8192:
			partDict["8k"] =1
		else:
			partDict["8k"] +=  math.floor(value/8192)
			if  4080<value <=4096 or 4080<(value-partDict["8k"]*8192) <=4096:
				partDict["4k"] =1
			else:
				partDict["4k"] =math.floor((value-partDict["8k"]*8192)/4096)
				if 2032<value<=2048 or 2032<(value-partDict["8k"]*8192 -partDict["4k"]*4096)<=2048:
					partDict["2k"] =1
				else:
					partDict["2k"] =math.floor((value-partDict["8k"]*8192 -partDict["4k"]*4096)/2048)
					if 1008< value<=1024 or 1008< (value-partDict["8k"]*8192 -partDict["4k"]*4096 - partDict["2k"]*2048)<=1024:
						partDict["1k"] =1
					else:
						partDict["1k"] =math.floor((value-partDict["8k"]*8192 -partDict["4k"]*4096 - partDict["2k"]*2048)/1024)
						if 496< value<=512 or 496<(value-partDict["8k"]*8192 -partDict["4k"]*4096 - partDict["2k"]*2048 -partDict["1k"]*1024)<=512 :
							partDict["512"] =1
						else:
							partDict["512"] =math.floor((value-partDict["8k"]*8192 -partDict["4k"]*4096 - partDict["2k"]*2048 -partDict["1k"]*1024)/512)
							if 240 <value<=256 or 240 <(value-partDict["8k"]*8192 -partDict["4k"]*4096 - partDict["2k"]*2048 -partDict["1k"]*1024- partDict["512"]*512)<=256: 
								partDict["256"] =1
							else:
								partDict["256"] =math.floor((value-partDict["8k"]*8192 -partDict["4k"]*4096 - partDict["2k"]*2048 -partDict["1k"]*1024- partDict["512"]*512)/256)
								if 112<value<=128 or 112<(value-partDict["8k"]*8192 -partDict["4k"]*4096 - partDict["2k"]*2048 -partDict["1k"]*1024- partDict["512"]*512-partDict["256"]*256)<=128:
									partDict["128"] =1
								else:
									partDict["128"] =math.floor((value-partDict["8k"]*8192 -partDict["4k"]*4096 - partDict["2k"]*2048 -partDict["1k"]*1024- partDict["512"]*512-partDict["256"]*256)/128)
									if  48<value<=64 or 48<(value-partDict["8k"]*8192 -partDict["4k"]*4096 - partDict["2k"]*2048 -partDict["1k"]*1024- partDict["512"]*512-partDict["256"]*256-partDict["128"]*128)<=64:
										partDict["064"] =1
									else:
										partDict["064"] =math.floor((value-partDict["8k"]*8192 -partDict["4k"]*4096 - partDict["2k"]*2048 -partDict["1k"]*1024- partDict["512"]*512-partDict["256"]*256-partDict["128"]*128)/64)
										if 16< value<=32 or 16< (value-partDict["8k"]*8192 -partDict["4k"]*4096 - partDict["2k"]*2048 -partDict["1k"]*1024- partDict["512"]*512-partDict["256"]*256-partDict["128"]*128-partDict["064"]*64)<=32:
											partDict["032"] =1
										else:
											partDict["032"] =math.floor((value-partDict["8k"]*8192 -partDict["4k"]*4096 - partDict["2k"]*2048 -partDict["1k"]*1024- partDict["512"]*512-partDict["256"]*256-partDict["128"]*128-partDict["064"]*64)/32)
											partDict["016"] =math.ceil((value-partDict["8k"]*8192 -partDict["4k"]*4096 - partDict["2k"]*2048 -partDict["1k"]*1024- partDict["512"]*512-partDict["256"]*256-partDict["128"]*128-partDict["064"]*64-partDict["032"]*32)/16)
	return partDict

def cal10k(value):
	list1 = ["10k","5k","2k","1k","100"]
	partDict = {}
	for x in list1:
		partDict[x]=0
	if 9900<value<= 10000:
		partDict["10k"] = 1
	else:
		partDict["10k"] =  math.floor(value/10000)
		if 4900 < value<=5000 or 4900 < (value -partDict["10k"]*10000)<=5000:
			partDict["5k"] =1
		else:
			partDict["5k"] = math.floor((value -partDict["10k"]*10000)/5000)
			if 3900 < value<=4000 or 3900 < (value-partDict["10k"]*10000-partDict["5k"]*5000)<=4000:
				partDict["2k"] =2
			elif 1900 < value<=2000 or 1900 < (value-partDict["10k"]*10000-partDict["5k"]*5000)<=2000:
				partDict["2k"] =1
			else:
				partDict["2k"] =math.floor((value-partDict["10k"]*10000-partDict["5k"]*5000)/2000)
				if 900 < value<=1000 or 900 < (value-partDict["10k"]*10000-partDict["5k"]*5000-partDict["2k"]*2000)<=1000:
					partDict["1k"] =1
				else:
					partDict["1k"] =math.floor((value-partDict["10k"]*10000-partDict["5k"]*5000-partDict["2k"]*2000)/1000)
					partDict["100"] =math.ceil((value-partDict["10k"]*10000-partDict["5k"]*5000-partDict["2k"]*2000-partDict["1k"]*1000)/100)
	return partDict

def getLaborContainerData(container, productDictKey, partNumbersToBeAdded, partsList):
	for row in container.Rows:
		if row["Deliverable"] not in ('Total','Off-Site','On-Site'):
			if row["FO_Eng"]:
				foQty = round((getFloat(row["Final_Hrs"]) * getFloat(row["FO_Eng_Percentage_Split"]) / 100))
				addFinalHours(partNumbersToBeAdded[productDictKey],row["FO_Eng"],foQty)
			if row["FO_Eng"] not in partsList:
				partsList.add(row["FO_Eng"])
			if row["GES_Eng"] != '' and row["GES_Eng_Percentage_Split"] != '0':
				gesQty = round((getFloat(row["Final_Hrs"]) * getFloat(row["GES_Eng_Percentage_Split"]) / 100))
				addFinalHours(partNumbersToBeAdded[productDictKey],row["GES_Eng"],gesQty)
			if row["GES_Eng"] not in partsList:
				partsList.add(row["GES_Eng"])

def getProductLaborDeliverablesContainer(productName, partNumbersToBeAdded, partsList, product):
	selectedProducts = str(product.Attr('MSID_Selected_Products').GetValue().split('<br>'))
	if productName == 'OPM':
		opmEngineeringCon = getContainer(product,"MSID_Labor_OPM_Engineering")
		getLaborContainerData(opmEngineeringCon, "OPM", partNumbersToBeAdded, partsList)
	elif productName == 'LCN One Time Upgrade':
		lcnOneTimeUpgradeCon = getContainer(product,"MSID_Labor_LCN_One_Time_Upgrade_Engineering")
		getLaborContainerData(lcnOneTimeUpgradeCon, "LCN", partNumbersToBeAdded, partsList)
	elif productName == 'CD Actuator I-F Upgrade':
		CDActuatorCon = getContainer(product, "MSID_Labor_CD_Actuator_con")
		getLaborContainerData(CDActuatorCon,"CD_Actuator_IF_Upgrade", partNumbersToBeAdded, partsList)
	elif productName == 'EBR':
		ebrCon = getContainer(product,"MSID_Labor_EBR_Con")
		getLaborContainerData(ebrCon,"EBR", partNumbersToBeAdded, partsList)
	elif productName == 'ELCN':
		elcnCon = getContainer(product, "MSID_Labor_ELCN_Con")
		getLaborContainerData(elcnCon,"ELCN", partNumbersToBeAdded, partsList)
	elif productName == 'Orion Console':
		orionConsoleCon = getContainer(product,"MSID_Labor_Orion_Console_Con")
		getLaborContainerData(orionConsoleCon,"Orion_Console", partNumbersToBeAdded, partsList)
	elif productName == 'EHPM/EHPMX/ C300PM':
		ehpmCon = getContainer(product, "MSID_Labor_EHPM_C300PM_Con")
		getLaborContainerData(ehpmCon,"EHPM/EHPMX/ C300PM", partNumbersToBeAdded, partsList)
	elif productName == 'TPS to Experion':
		tpsCon = getContainer(product, "MSID_Labor_TPS_TO_EXPERION_Con")
		getLaborContainerData(tpsCon,"TPS_EXP", partNumbersToBeAdded, partsList)
	elif productName == 'TCMI':
		tcmiCon = getContainer(product, "MSID_Labor_TCMI_Con")
		getLaborContainerData(tcmiCon,"TCMI", partNumbersToBeAdded, partsList)
	elif productName == 'EHPM HART IO':
		ehpmhartioCon = getContainer(product, "MSID_Labor_EHPM_HART_IO_Con")
		getLaborContainerData(ehpmhartioCon,"EHPMHART", partNumbersToBeAdded, partsList)
	elif productName == 'C200 Migration':
		c200MigrationCon = getContainer(product, "MSID_Labor_C200_Migration_Con")
		getLaborContainerData(c200MigrationCon,"C200 Migration", partNumbersToBeAdded, partsList)
	elif productName == 'CB-EC Upgrade to C300-UHIO':
		cbCEtoC300UHIOCon = getContainer(product, "MSID_Labor_CB-EC_Upgrade_to_C300-UHIO_con")
		getLaborContainerData(cbCEtoC300UHIOCon,"CBEC", partNumbersToBeAdded, partsList)
	elif productName == 'xPM to C300 Migration':
		xPMCon = getContainer(product, "MSID_Labor_xPM_to_C300_Migration_Con")
		getLaborContainerData(xPMCon,"XPM C300", partNumbersToBeAdded, partsList)
	elif productName == 'FSC to SM':
		fscCon = getContainer(product, "MSID_Labor_FSC_to_SM_con")
		getLaborContainerData(fscCon,"FSC_to_SM", partNumbersToBeAdded, partsList)
		fscauditCon = getContainer(product, "MSID_Labor_FSC_to_SM_audit_Con")
		getLaborContainerData(fscauditCon,"FSC_to_SM_audit", partNumbersToBeAdded, partsList)
		
	elif productName == 'LM to ELMM ControlEdge PLC':
		LMCon = getContainer(product, "MSID_Labor_LM_to_ELMM_Con")
		getLaborContainerData(LMCon,"LMTOELMM", partNumbersToBeAdded, partsList)
	elif productName == 'XP10 Actuator Upgrade':
		XP10con = getContainer(product, "MSID_Labor_XP10_Actuator_Upgrade_con")
		getLaborContainerData(XP10con,"XP10_Actuator", partNumbersToBeAdded, partsList)
	elif productName == 'Graphics Migration':
		GraphicsCon = getContainer(product, "MSID_Labor_Graphics_Migration_con")
		getLaborContainerData(GraphicsCon,"Graphics_Migration", partNumbersToBeAdded, partsList)
	elif productName == 'CWS RAE Upgrade':
		CWSRAECon = getContainer(product, "MSID_Labor_CWS_RAE_Upgrade_con")
		getLaborContainerData(CWSRAECon,"CWS_RAE_Upgrade", partNumbersToBeAdded, partsList)
	elif productName == 'FSC to SM IO Migration':
		fscsmioCon = getContainer(product, "MSID_Labor_FSCtoSM_IO_con")
		getLaborContainerData(fscsmioCon,"FSCtoSM_IO", partNumbersToBeAdded, partsList)
		fscsmioauditCon = getContainer(product, "MSID_Labor_FSC_to_SM_IO_Audit_Con")
		getLaborContainerData(fscsmioauditCon,"FSCtoSM_IO_AUDIT", partNumbersToBeAdded, partsList)
	elif productName == 'Generic System Migration':
		gs1Con = getContainer(product, "MSID_Labor_Generic_System1_Cont")
		getLaborContainerData(gs1Con,"GS_Migration_1", partNumbersToBeAdded, partsList)
		gs2Con = getContainer(product, "MSID_Labor_Generic_System2_Cont")
		getLaborContainerData(gs2Con,"GS_Migration_2", partNumbersToBeAdded, partsList)
		gs3Con = getContainer(product, "MSID_Labor_Generic_System3_Cont")
		getLaborContainerData(gs3Con,"GS_Migration_3", partNumbersToBeAdded, partsList)
		gs4Con = getContainer(product, "MSID_Labor_Generic_System4_Cont")
		getLaborContainerData(gs4Con,"GS_Migration_4", partNumbersToBeAdded, partsList)
		gs5Con = getContainer(product, "MSID_Labor_Generic_System5_Cont")
		getLaborContainerData(gs5Con,"GS_Migration_5", partNumbersToBeAdded, partsList)
	elif productName == 'Virtualization System Migration':
		VirtCon = getContainer(product, "MSID_Labor_Virtualization_con")
		getLaborContainerData(VirtCon,"Virtualization_System_Migration", partNumbersToBeAdded, partsList)
	elif productName == 'QCS RAE Upgrade':
		QCSCon = getContainer(product, "MSID_Labor_QCS_RAE_Upgrade_con")
		getLaborContainerData(QCSCon,"QCS_RAE_Upgrade", partNumbersToBeAdded, partsList)
	elif productName == 'TPA/PMD Migration':
		TPACon = getContainer(product, "MSID_Labor_TPA_con")
		getLaborContainerData(TPACon,"TPA/PMD_Migration", partNumbersToBeAdded, partsList)
										 
																				 
	elif productName == 'ELEPIU ControlEdge RTU Migration Engineering':
		ELEPIUCon = getContainer(product, "MSID_Labor_ELEPIU_con")
		getLaborContainerData(ELEPIUCon,"ELEPIU_ControlEdge_RTU_Migration_Engineering", partNumbersToBeAdded, partsList)
	elif productName == '3rd Party PLC to ControlEdge PLC/UOC':
		thirdpartyplc = getContainer(product, "3rd_Party_PLC_UOC_Labor")
		getLaborContainerData(thirdpartyplc,"3rd_Party_PLC_to_ControlEdge_PLC/UOC", partNumbersToBeAdded, partsList)
	elif 'FDM Upgrade 1' in selectedProducts and (('FDM Ugrade 2' not in selectedProducts) and ('FDM Ugrade 3' not in selectedProducts)) :
		fdmCon = getContainer(product, "MSID_Labor_FDM_Upgrade_Con")
		getLaborContainerData(fdmCon,"FDM_Upgrade",partNumbersToBeAdded,partsList)
	elif 'FDM Upgrade 2' in selectedProducts and (('FDM Ugrade 1' not in selectedProducts) and ('FDM Ugrade 3' not in selectedProducts)) :
		fdmCon = getContainer(product, "MSID_Labor_FDM_Upgrade_Con")
		getLaborContainerData(fdmCon,"FDM_Upgrade_2",partNumbersToBeAdded,partsList)
	elif 'FDM Upgrade 3' in selectedProducts and (('FDM Ugrade 2' not in selectedProducts) and ('FDM Ugrade 1' not in selectedProducts)) :
		fdmCon = getContainer(product, "MSID_Labor_FDM_Upgrade_Con")
		getLaborContainerData(fdmCon,"FDM_Upgrade_3",partNumbersToBeAdded,partsList)
	projectManagementCon = getContainer(product, "MSID_Labor_Project_Management")
	for row in projectManagementCon.Rows:
		if row["Deliverable"] not in ('Total','Off-Site','On-Site'):
			if row["FO_Eng"]:
				foQty = round((getFloat(row["Final_Hrs"]) * getFloat(row["FO_Eng_Percentage_Split"]) / 100))
				addFinalHours(partNumbersToBeAdded["PM"],row["FO_Eng"],foQty)
			if row["FO_Eng"] not in partsList:
				partsList.add(row["FO_Eng"])
			if row["GES_Eng"] != '' and row["GES_Eng_Percentage_Split"] != '0':
				gesQty = round((getFloat(row["Final_Hrs"]) * getFloat(row["GES_Eng_Percentage_Split"]) / 100))
				addFinalHours(partNumbersToBeAdded["PM"],row["GES_Eng"],gesQty)
			if row["GES_Eng"] not in partsList:
				partsList.add(row["GES_Eng"])

'''def popthirdPartSummary(prod, partNumbersToBeAdded, partsList):
	parts_to_update = {}
	partNumToBeAdded = {}
	if prod.Name == '3rd Party PLC to ControlEdge PLC/UOC' and prod.GetContainerByName('LSS_Configuration_for_Rockwell_transpose') != None:
		base_media_delivery = prod.Attr('LSS_PLC_Base_Media_Delivery').GetValue()
		for row in prod.GetContainerByName('LSS_Configuration_for_Rockwell_transpose').Rows:
			controller_migrated = row['LSS_PLC_controllers_intend_to_migrate']
			sql_res = SqlHelper.GetList("Select * from LSS_3RD_PARTY_CONTROLEDGE_PLC_BOM where ('{}' = isPLC or '{}' = isUOC or '{}' = isvUOC) and (Operating_Temperature = '{}' or Operating_Temperature = '') and (Controller_Type = '{}' or Controller_Type = '') and (Power_Input_Type = '{}' or Power_Input_Type = '') and (Power_Supply_Type='{}' or Power_Supply_Type = '') and (Power_Status_Module_for_Redundant_Power_Supply='{}' or Power_Status_Module_for_Redundant_Power_Supply = '') and (Redundant_Controller_Physical_Separation_Required='{}' or Redundant_Controller_Physical_Separation_Required = '') and (IO_Rack_Type='{}'  or IO_Rack_Type = '') and (ControlEdge_PLC_System_Software_Release='{}' or ControlEdge_PLC_System_Software_Release = '') and (Base_Media_Delivery='{}' or Base_Media_Delivery = '') and (Ethernet_Switch_Type='{}' or Ethernet_Switch_Type = '') and (Ethernet_Switch_Ports='{}' or Ethernet_Switch_Ports = '') and (Network_Topology='{}' or Network_Topology = '') and (G3_Option_Ethernet_Switch='{}' or G3_Option_Ethernet_Switch = '')".format(row['LSS_PLC_ControlEdge_PLC_UOC_or_vUOC'],row['LSS_PLC_ControlEdge_PLC_UOC_or_vUOC'],row['LSS_PLC_ControlEdge_PLC_UOC_or_vUOC'],row['LSS_PLC_Operating_temp_for_Controller_Module'], row['LSS_PLC_Controller_Type'], row['LSS_PLC_Power_Input_Type'], row['LSS_PLC_Power_Supply_Type'], row['LSS_PLC_Power_Status_Module_for_Redundant_Pwr_Sply'], row['LSS_PLC_Redundant_Controller_Phy_Sep_Req'], row['LSS_PLC_IO_Rack_Type'], row['LSS_PLC_ControlEdge_PLC_System_Software_Release'], base_media_delivery,row['LSS_PLC_Ethernet_Switch_Type'], row['LSS_Ethernet_Switch_Ports'], row['LSS_PLC_Network_Topology'], "No" if row['LSS_PLC_G3_Option_Ethernet_Switch']=="" else row['LSS_PLC_G3_Option_Ethernet_Switch']))
			for i in sql_res:
				if i.Part_Number in ['SP-EMD170-ESD','SP-EMD171-ESD','SP-EMD172-ESD','SP-EMD174-ESD','SP-EMD170','SP-EMD171','SP-EMD172','SP-EMD174']:
					part_number1_sum=sum(parts_to_update.get('900CP1-0200',list()))
					part_number2_sum=sum(parts_to_update.get('900CP1-0300',list()))
					if part_number1_sum <= 0 and part_number2_sum <= 0:
						continue
				part_number = parts_to_update.get(i.Part_Number,list())
				try:
					part_number.append(int(i.Qty) * int(controller_migrated))
				except:
					if row[i.Qty] =='':
						part_number.append(0)
					else:
						part_number.append(int(row[i.Qty]) * int(controller_migrated))
				parts_to_update[i.Part_Number]= part_number
		partNumToBeAdded=  {key: sum(value_list) for key, value_list in parts_to_update.items()}
		partNumbersToBeAdded["3rd_Party_PLC_to_ControlEdge_PLC/UOC"].update(partNumToBeAdded)
	if len(parts_to_update)>0:
		part_numbers_keys=[]
		for i in parts_to_update:
			partsList.add(i)
			if sum(parts_to_update[i]) != '0':
				part_numbers_keys.append(i)
		for r in part_numbers_keys:
			setAtvQty(prod, "PLC_UOC_BOM_Items", r, sum(parts_to_update[r]))'''

def popthirdPartSummary(prod, partNumbersToBeAdded, partsList, Product):
	parts_to_update = {}
	partNumToBeAdded = {}
	pvs=Product.Attr('PLC_UOC_BOM_Items').Values
	for av in pvs:
		if av.IsSelected:
			partNumToBeAdded[av.Display] = av.Quantity
			#CXCPQ-94283 :Start
			partsList.add(av.Display)
			#CXCPQ-94283 :End
	partNumbersToBeAdded["3rd_Party_PLC_to_ControlEdge_PLC/UOC"].update(partNumToBeAdded)