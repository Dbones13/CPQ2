"""containerMapping={}
if Product.Name == 'EBR':
	containerMapping = {
						'EBR_Basic_Information': {
												  'EBR_Current_EBR_Release_only_for_EBR_Upgrade': 'R410 (Acronis)',
												  'EBR_Media_kit_type': 'Electronic delivery'
												  }
						}
elif Product.Name == 'Non-SESP Exp Upgrade':
	containerMapping = {
						'NONSESP_Design_Inputs_for_Experion_Upgrade_License': {
												  'NONSESP_Sever_Redundancy': 'No',
												  'NONSESP_Should_RSLinx_be_added': 'No'
												  }
						}
elif Product.Name == 'LCN One Time Upgrade':
	containerMapping = {
						'LCN_Design_Inputs_for_TPN_OTU_Upgrade': {
												  'LCN_Is_there_redundant_History_Module': 'No',
												  'LCN_Do_you_want_HG_Point_Bar_Trend_Display': 'No'
												  }
						}
elif Product.Name == 'LM to ELMM ControlEdge PLC':
	cont =  Product.Attr('ATT_LM_QTY_OF_LMPAIR_TOBE_MIGRATED').GetValue()
	col_name = []
	col_name.append(cont)
	value = int(col_name[0] or '0') if col_name else 0
	containerMapping = {
						'LM_to_ELMM_ControlEdge_PLC_Migration_Gen_Cont': {
												  'LM_Current_Experion_Release': 'No Experion',
												  'LM_Does_The_Customer_Have_TPN_Release_R688.1_Or_Later': 'No',
												  'LM_FTE_Switch_To_Connect_ControlEdge_PLC': 'None',
												  'Is_Honeywell_Providing_FTE_Cables': 'No',
												  'LM_to_ELMM_ControlEdge_PLC_Operating_temperature': '0 to 60 DegC or Marine application',
												  'LM_Additional_Switch_Selection': 'None'
												  },
						'LM_to_ELMM_ControlEdge_PLC_Cont': {
													'UPDATE_ROW_INDEXES': [i for i in range(0, value)],
												  'LM_do_you_have_additional_space_in_the_cabinet_room_to_mount_the_CE_System': 'No',
												  'LM_do_the_customer_wants_to_retain_the_wiring':'No',
												  'LM_CE_Power_Input_Type':'DC',
												  'LM_do_you_need_Redundant_PS_for_IO_Racks':'No',
												  'LM_type_of_IO_Rack_to_be_installed':'12 Slot Rack',
												  'LM_are_the_IO_Racks_remotely_located':'No',
												  'LM_select_IO_network_topology':'Star',
												  'LM_select_type_of_Switch_for_the_IO_network':'Multimode Redundant'
												  },
						'LM_to_ELMM_Migration_Additional_IO_Cont': {
												  'UPDATE_ROW_INDEXES': [i for i in range(0, value)],
												  'LM_any_unsupported_instruction_in_the_LM_ladder_logic': 'No'
												  }
						}
elif Product.Name == 'EHPM HART IO':
	containerMapping = {
						'EHPM_HART_IO_General_Qns_Cont': {
												  'Current_Experion_Release': 'Less_than_R511.4',
												  'Current_TPN_Release': 'Less_than_R688.5',
												  'Current_FDM_Release': 'None'
												  }
						}
elif Product.Name == 'TCMI':
	containerMapping = {
						'TCMI_General_Information ': {
												  'TCMI_Is_the_current_TPN_release_at_R687_or_greater': 'Yes',
												  'TCMI_Is_the_current_Experion_Release_at_R432.2': 'Yes',
												  'TCMI_Is_the_current_Triconex_Controller_HW_&_SW': 'Yes'
												  }
						}
elif Product.Name == 'ELCN':
	containerMapping = {
						'ELCN_Basic_Information ': {
												  'ELCN_If_ELCN_Bridge_is_not_present_in_LCN': 'Nothing - ELCN Bridge is present',
												  'ELCN_Type_of_Cabinet_where_the_ELCN_Bridge': 'None',
												  'ELCN_Type_of_Cabinet_to_Install_the_Physical_nodes': 'LCN Cabinet',
												  'ELCN_Additional_Switches_needed': 'EightPortCISCOSwitch'
												  }
						}    
elif Product.Name == 'C200 Migration':
	containerMapping = {
						'C200_Migration_General_Qns_Cont ': {
												  'C200_Connection _to_Experion_Server': 'FTE',
												  'C200_FTE_Switch_to_connect_required_exp_servers': 'None',
												  'C200_Is_Honeywell_Providing_FTE_cables': 'Yes',
												  'C200_Average_Cable_Length': '10m',
												  'C200_Type_of_UOC':'UOC',
												  'C200_Type_of_downlink_communication_UOC':'E/IP'

												  }
						}
elif Product.Name == 'CB-EC Upgrade to C300-UHIO':
	containerMapping = {
						'CB_EC_migration_to_C300_UHIO_Configuration_Cont ': {
												  'CB_EC_Do_you_want_IO_redundancy': 'No',
												  'CB_EC_Do_you_want_new_TCB_cables_or_just_the_Adapter_cables': 'Yes - New TCB cables 10m',
												  'CB_EC_Do_you_want_Series_C_RAM_Battery_Backup': 'No',
												  'CB_EC_Do_you_want_FTE_cables_to_run_between_the_C300_C9_Firewall_and_FTE_Switches': 'No'
												  }
						}
elif Product.Name == 'TPS to Experion':	
	containerMapping = {
						'TPS_EX_Station_Conversion_EST ': {
												  'UPDATE_ROW_INDEXES': [0,1,2],
												  'TPS_EX_Hardware': 'Dell T5860XL',
												  'TPS_EX_Future_Mounting_Furniture': 'Desktop',
												  'TPS_EX_Computer_Adapter_Kit': 'No',
												  'TPS_EX_RPS_Type': 'None',
												  'TPS_EX_Keyboard_Type': 'None'
												  },
						'TPS_EX_Conversion_ACET_EAPP': {
												   'UPDATE_ROW_INDEXES': [0,1],
												  'TPS_EX_Conversion_ACET_EAPP_Server_Hardware': 'DELL T550 STD TPM',
												  'TPS_EX_Conversion_ACET_EAPP_Does_App_Contains_Sol': 'No',
												  'TPS_EX_Conversion_ACET_EAPP_Additional_Hard_Drive': 'No'
												  },
						'TPS_EX_Additional_Servers':   {
													'UPDATE_ROW_INDEXES': [0,1],
													'TPS_EX_Additional_Server_Hardware':'DELL T150 STD TPM',
													'TPS_EX_Additional_Server_Additional_Memory':'None',
													'TPS_EX_Additional_Server_Optional_DVD':'No',
													'TPS_EX_Additional_Server_Display':'None',
													'TPS_EX_Additional_Server_Trackball': 'No',
													'TPS_EX_Additional_Server_Cabinet_Mounting_Type': 'None'
													},
						'TPS_EX_Additional_Stations':{
													'UPDATE_ROW_INDEXES': [0,1,2,3,4,5,6,7,8,9,10,11],
													'TPS_EX_Additional_Stations_Desk_Hardware':'Dell T5860XL',
													'TPS_EX_Additional_Stations_Cabinat_Hardware':'Dell T5860XL',
													'TPS_EX_Additional_Stations_RPS_Type':'None',
													'TPS_EX_Additional_Stations_RPS_Mounting_Furniture':'Desk',
													'TPS_EX_Additional_Stations_Multi_Window_Support':'No',
													'TPS_EX_Additional_Stations_Display_Size':'Wide',
													'TPS_EX_Additional_Stations_Touch_Screen':'No',
													'TPS_EX_Additional_Stations_Trackball':'No',
													'TPS_EX_Additional_Stations_IKB_OEP':'None',
													'TPS_EX_Additional_Stations_Interface_card':'FTE',
													'TPS_EX_Additional_Stations_Cabinet_Mounting_Type':'None',
													'TPS_EX_Additional_Stations_Station_License?':'No'
													}
						}
elif Product.Name == 'xPM to C300 Migration':
	containerMapping = {
						'xPM_C300_Migration_Configuration_Cont': {
												  'xPM_C300_Required_Modbus_Firewall': 'Read-Write'
												  }
						}
elif Product.Name == 'EHPM/EHPMX/ C300PM':
	containerMapping = {
						'xPM_Migration_General_Qns_Cont': {
												  'xPM_Is_FTE_Network_Infrastructure_Existing': 'Yes',
												  'xPM_On_Process_Red_HPMs_or_Off_Process_Migration': 'xPM to EHPM Off Process',
												  'xPM_Experion_Server_Redundancy':'Redundant',
												  'xPM_On_Process_Red_HPMs_EHPMs_only':'xPM to C300PM Off Process',
												  'xPM_On_Process_Red_HPMs_EHPMs_for_EHPMX_mig':'xPM to EHPMX Off Process'
												  },
						'ENB_Migration_Config_Cont': {
													'UPDATE_ROW_INDEXES': [i for i in range(0, int(Product.Attr('xPM_NIMsconf').GetValue() or '0'))],
													'xPM_ENB_CE_Mark_or_Not':'CE',
													'xPM_What_is_the_NIM_migration_scenario':'Non Redundant NIM to ENB',
													'xPM_Does_the_customer_have_K4_processor_boards':'Yes'
												}
						}
elif Product.Name == '3rd Party PLC to ControlEdge PLC/UOC':
	containerMapping = {
						'LSS_Configuration_for_Rockwell_transpose': {
												  'UPDATE_ROW_INDEXES': [i for i in range(0, int(Product.Attr('LSS_PLC_Number_of_ControlEdge_PLC_UOC_vUOC_confi').GetValue() or '0'))],
												  'LSS_PLC_Controller_Type': 'Redundant',
												  'LSS_PLC_Power_Supply_Type': 'Non Redundant',
												  'LSS_PLC_Ethernet_Switch_Supplier':'Honeywell',
												  'LSS_PLC_Need_Cabinet_for_the_controller_for_budget':'No'
												  }
						} 
elif Product.Name == 'OPM':
	containerMapping = {
						'OPM_Basic_Information': {
												  'OPM_RESS_Migration_in_scope': 'No',
												  'OPM_Does_the_customer_have_EBR_installed': 'No',
												  'OPM_If_AMT_Will_Not_Be_Used': 'No'
												  }
						} 
elif Product.Name == 'SM Control Group':
	containerMapping = {
						'SM_CG_Universal_Marshalling_Cabinet_Details': {
												  'Mounting Option': 'Bracket Mounting'
												  }
						}    
elif Product.Name == 'ControlEdge UOC System':
	containerMapping = {
						'UOC_Common_Questions_Cont': {
												  'UOC_Cabinet_Required_Racks_Mounting':'Yes',
												  'UOC_Starter_Kit':'No',
												  'UOC_Starter_ Kit_with_Experion_License':'No',
												  }
						}
elif Product.Name == 'UOC Control Group':
	containerMapping = {
						'UOC_CG_Cabinet_Cont': {
												  'UOC_Cabinet_Type': 'Dual Access',
												  'UOC_Cabinet_Door_Type': 'Standard',
												  'UOC_Cabinet_Base_Size':'100mm',
												  'UOC_Cabinet_Door_Keylock':'Standard',
												  'UOC_Cabinet_Power_Entry':'Double Pole',
												  'UOC_Cabinet_Thermostat':'Yes',
												  'UOC_Cabinet_Light':'Yes',
												  'UOC_Integrated_Marshalling_Cabinet':'No',
												  },
						'UOC_CG_Controller_Rack_Cont':{
												  'UOC_Controller_Type':'Redundant',
												  'UOC_Redundant_Controller_Physical_Seperation':'No',
												  'UOC_IO_Rack_Type':'4 I/O Rack',
												  'UOC_Power_Input':'AC',
												  'UOC_Field_Wiring_DIDOAOAI_Channel_Mod':'Terminal Block(Euro)',
												  'UOC_Power_Supply':'Non Redundant',
												  'UOC_Power_Status_Mod_Redundant_Supply':'No',
												  'UOC_Ethernet_Switch_Supplier':'Honeywell',
												  'UOC_Ethernet_Switch_Type':'Single Mode',
												  'UOC_Field_Wiring_Other_Mod':'Terminal Block(Euro)',
												  'UOC_Remote_Terminal_Cable_Length':'1M',
												  'UOC_Network_Topology':'Redundant Star-PRP',
												  'UOC_Remote_Terminal_Panel_Cable_Type':'High Voltage',
												  'UOC_Operating_Temprature':'0 to 60 DegC or Marine application',
												  }
						}
elif Product.Name == 'UOC Remote Group':
	containerMapping = {
						'UOC_RG_Cabinet_Cont': {
												  'UOC_Cabinet_Type': 'Dual Access',
												  'UOC_Cabinet_Door_Type': 'Standard',
												  'UOC_Cabinet_Base_Size':'100mm',
												  'UOC_Cabinet_Door_Keylock':'Standard',
												  'UOC_Cabinet_Power_Entry':'Double Pole',
												  'UOC_Cabinet_Thermostat':'Yes',
												  'UOC_Cabinet_Light':'Yes',
												  'UOC_Integrated_Marshalling_Cabinet':'No',
												  },
						'UOC_RG_Controller_Rack_Cont':{
												  'UOC_IO_Rack_Type':'4 I/O Rack',
												  'UOC_Power_Supply':'Non Redundant',
												  'UOC_Power_Input':'AC',
												  'UOC_Power_Status_Mod_Redundant_Supply':'No',
												  'UOC_Field_Wiring_DIDOAOAI_Channel_Mod':'Terminal Block(Euro)',
												  'UOC_Field_Wiring_Other_Mod':'Terminal Block(Euro)',
												  'UOC_Remote_Terminal_Cable_Length':'1M',
												  }
						}
elif Product.Name == 'ControlEdge PLC System':
	containerMapping = {
						'PLC_Software_Question_Cont': {
												  'PLC_Software_Release':'R180',
												  'PLC_Media_Delivery':'Electronic Download',
												  'PLC_Cabinet_Required_Racks_Mounting':'Yes'
												  },
						'PLC_Common_Questions_Cont': {
												  'PLC_Shielded_Terminal_Strip':'No',
												  'PLC_IO_Filler_Module':'No'
												  },
						'CE_PLC_System_Hardware': {
												  'PLC_Engineering_Station_Model':'STN_STD_DELL_Tower_NonRAID',
												  },
						'PLC_Labour_Details': {
												  'PLC_Process_Type':'None',
												  'PLC_Ges_Location':'None'
												  }
						}
elif Product.Name == 'CE PLC Control Group':
	containerMapping = {
						'PLC_CG_Cabinet_Cont': {
												  'PLC_Cabinet_Type': 'Dual Access',
												  'PLC_Cabinet_Door_Type': 'Standard',
												  'PLC_Cabinet_Base_Size':'200mm',
												  'PLC_Cabinet_Door_Keylock':'Standard',
												  'PLC_Cabinet_Power_Entry':'Double Pole',
												  'PLC_Cabinet_Thermostat':'Yes',
												  'PLC_Cabinet_Light':'Yes',
												  'PLC_Integrated_Marshalling_Cabinet':'No'
												  },
						'PLC_CG_Controller_Rack_Cont': {
												  'PLC_Controller_Type':'Redundant',
												  'PLC_IO_Rack_Type':'12 I/O Rack',
												  'PLC_Power_Supply':'Non Redundant',
												  'PLC_Power_Input':'AC',
												  'PLC_Power_Status_Mod_Redudant_Supply':'No',
												  'PLC_Field_Wiring_DIDOAOAI_Channel_Mod':'Terminal Block(Euro)',
												  'PLC_Field_Wiring_PIFII_Channel_Mod':'Terminal Block(Euro)',
												  'PLC_Field_Wiring_Other_Mod':'1M',
												  'PLC_Remote_Terminal_Cable_Length':'Redundant Star',
												  'PLC_Network_Topology':'Honeywell',
												  'PLC_Ethernet_Switch_Supplier':'No',
												  'PLC_Ethernet_Switch_Type':'Multi Mode',
												  'PLC_G3_Option_Ethernet_Switch':'No',
												  'PLC_Operating_Temperature':'0 to 60 DegC or Marine application'
												  }
						}
elif Product.Name == 'ControlEdge RTU System':
	containerMapping = {
						'RTU_Software_Labor_Container1': {
												  'RTU_Base_Media_delivery': 'Electronic Download',
												  'RTU_Cabinet_Required_Racks_Mounting': 'Yes'
												  }
						}
elif Product.Name == 'RTU Group':
	containerMapping = {
						'RTU_CG_Cabinet_Cntr_Cont': {
												  'Cabinet_Type': 'Full Size Dual Side Cabinet (800w*800d*2000h)',
												  'Cabinet_Access': 'Single Access',
												  'Cabinet_Base_Size': '100mm',
												  'Cabinet_Door_Keylock': 'Standard'
												  }
						}
for contName, colDetails in containerMapping.items():
	cont = Product.GetContainerByName(contName)
	rowIndexesList = colDetails.get('UPDATE_ROW_INDEXES', [0])
	for row in cont.Rows:
		if row.RowIndex in rowIndexesList:
			for key, val in colDetails.items():
				if key != 'UPDATE_ROW_INDEXES':
					rowColumn = row.GetColumnByName(key)
					if not rowColumn.DisplayValue:
						try:
							rowColumn.SetAttributeValue(val)
							valCodeData = SqlHelper.GetFirst("Select sav.STANDARD_ATTRIBUTE_VALUE from ContainerColumn cc " +
                                                             "inner join ATTRIBUTE_DEFN ad on ad.STANDARD_ATTRIBUTE_CODE = cc.AttributeId  " +
                                                             "inner join STANDARD_ATTRIBUTE_VALUES sav on sav.STANDARD_ATTRIBUTE_CODE = cc.RefAttribute " +
                                                             "where STANDARD_ATTRIBUTE_NAME = '{}' and Name = '{}' and sav.STANDARD_ATTRIBUTE_DISPLAY_VAL = '{}'".format(cont.Name, key, val))
							valCode = val
							if valCodeData:
								valCode = valCodeData.STANDARD_ATTRIBUTE_VALUE
								Trace.Write('Val:{}----ValCode:{}'.format(val, valCode))
							row[key] = valCode
						except Exception as e:
							Trace.Write('Error while defaulting: {}---{}'.format(key, val))
		#cont.Calculate()"""