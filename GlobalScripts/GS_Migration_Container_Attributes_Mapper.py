def getSingleLineMapperDict():
    return {
        'OPM': {
			'OPM_Migration_platforms': {
				'OPM_Experion_Server_Hardware_Selection':'OPM_Experion_Server_Hardware_Selection',
                'OPM_ACET_EAPP_Server_Hardware_Selection':'OPM_ACET_EAPP_Server_Hardware_Selection',
                'OPM_Other_Servers_Hardware_Selection':'OPM_Other_Servers_Hardware_Selection',
                'OPM_Type_of_RPS_and_Thin_Client_for_EST':'OPM_Type_of_RPS_and_Thin_Client_for_EST',
				'OPM_EST_Tower_Hardware_Selection':'OPM_EST_Tower_Hardware_Selection',
                'OPM_Type_of_RPS_and_Thin_Client_for_ESC_ESF_ESCE':'OPM_Type_of_RPS_and_Thin_Client_for_ESC_ESF_ESCE',
                'OPM_ESC_ESF_or_ESCE_Tower_Hardware_Selection':'OPM_ESC_ESF_or_ESCE_Tower_Hardware_Selection',
                'OPM_RESS_Server_configuration':'OPM_RESS_Server_configuration',
                'OPM_Select_RESS_platform_configuration':'OPM_Select_RESS_platform_configuration',
                'OPM_Additional_Memory_for_RESS_Server':'OPM_Additional_Memory_for_RESS_Server',
                'OPM_Additional_Memory_for_RESS_Server':'OPM_Additional_Memory_for_RESS_Server',
                'ATT_OPMNUMRESS':'OPM_No_of_RESS_Remote_Users'},
			'OPM_FTE_Switches_migration_info': {
				'OPM_Is_L1_L2_Switch_HW_refresh_required':'OPM_Is_L1_L2_Switch_HW_refresh_required',
				'ATT_OPMQTYSWTS':'OPM_Quantity_of_L1_L2_Switches',
				'OPM_Is_Backbone_or_Agg_Switch_HW_refresh_required':'OPM_Is_Backbone_or_Agg_Switch_HW_refresh_required',
                'ATT_OPMQTYBBON':'OPM_Qty_of_Backbone_or_Agg_Fiber_Optic_Switch'},
			'OPM_Services': {
				'OPM_Acceptance_Test_Required':'OPM_Acceptance_Test_Required',
				'OPM_is_system_required_Domain_controller_upgrade':'OPM_is_system_required_Domain_controller_upgrade',
				'ATT_OPMADNLHRS':'OPM_Additional_hrs_for_Document_Customization'}
		},
        'EBR': {
			'EBR_New_Additional_EBR': {
				'Attr_New/AdditionalServer': 'EBR_Qty_of_EBR_New_Additional_for_Server',
				'Attr_NewAddWorkstation': 'EBR_Qty_of_EBR_New_Additional_for_Workstation',
				'Attr_NewAddVirtual_Node': 'EBR_Qty_of_EBR_New_Additional_for_Virtual_Node'},
			'EBR_Hardware_to_Host_EBR_Physical_Node_Only':{
				'EBR_If_hardware_desired_select_host_type': 'EBR_If_hardware_desired_select_host_type',
				'EBR_Additional_Hard_Drive_required': 'EBR_Additional_Hard_Drive_required',
				'EBR_Additional_Network_Storage_Device_NAS_required': 'EBR_Additional_Network_Storage_Device_NAS_required'},
			'EBR_Services': {
				'EBR_Site_Acceptance_Test_required': 'EBR_Site_Acceptance_Test_required'}
		},
        'XP10 Actuator Upgrade': {
			'XP10_Actuator_General_Information': {
				'ATT_XP10ACTUPG': 'XP10_Actuator_Number_of_actuators_to_be_upgraded',
				'XP10_Actuator_current_actuator_model': 'XP10_Actuator_Select_current_actuator_model',
				'XP10_Actuator_current_valve_plug_model': 'XP10_Actuator_Select_current_valve_plug_model',
				'XP10_Actuator_Will_a_seat_removal_tool_be_needed': 'XP10_Actuator_Will_a_seat_removal_tool_be_needed',
				'XP10_Actuator_Will_an_A7_actuator_tool_be_needed': 'XP10_Actuator_Will_an_A7_actuator_tool_be_needed',
				'XP10_Actuator_XP10_seat_adapter_tool_be_needed': 'XP10_Actuator_XP10_seat_adapter_tool_be_needed',
				'XP10_Actuator_XP10_adapter_tool_be_needed': 'XP10_Actuator_XP10_adapter_tool_be_needed'}
		},
        'ELCN': {
			'ELCN_Server_Cabinet_Configuration': {
				'ELCN_Cabinet_Depth_Size': 'ELCN_Cabinet_Depth_Size',
				'ELCN_Power_Supply_Voltage': 'ELCN_Power_Supply_Voltage',
				'ELCN_Cabinet_Door_Type': 'ELCN_Cabinet_Door_Type',
				'ELCN_Cabinet_Keylock_Type': 'ELCN_Cabinet_Keylock_Type',
				'ELCN_Cabinet_Hinge_Type': 'ELCN_Cabinet_Hinge_Type',
				'ELCN_Cabinet_Thermostat_Required': 'ELCN_Cabinet_Thermostat_Required',
				'ELCN_Cabinet_Base_Required': 'ELCN_Cabinet_Base_Required',
				'ELCN_Cabinet_Color': 'ELCN_Cabinet_Color'},
			'ELCN_Network_Gateway_Upgrade': {
				'ELCN_Select_Switch_configuration_required': 'ELCN_Select_Switch_configuration_required',
				'ATT_ELCN_Qty_of_NGs_more_than_100mts': 'ELCN_Qty_of_NGs_more_than_100mts_from_existing_fiber_concentrators',
				'ELCN_Select_type_of_fiber_optic_switch': 'ELCN_Select_type_of_fiber_optic_switch'},
			'ELCN_Services': {
				'ELCN_Off_Process_Setup_Validation_Required': 'ELCN_Off_Process_Setup_Validation_Required',
				'ELCN_Site_Acceptance_Test_required': 'ELCN_Site_Acceptance_Test_required',
				'ELCN_Will_OPM_or_TPS_to_Experion_be_performed': 'ELCN_Will_OPM_or_TPS_to_Experion_be_performed',
				'ATT_ELCN_Additional_hours': 'ELCN_Additional_hours_for_FTE_setup',
				'ELCN_Services_for_NG_Switch_Configuration': 'ELCN_Services_for_NG_Switch_Configuration'}
		},
        'FDM Upgrade 1': {
			'FDM_Upgrade_General_questions': {
				'Attr_Fdmupg1_generalques':'General questions - Field Device Manager (FDM) Upgrade',
				'FDM_Upgrade_What_is_the_current_release': 'What is the current release of the system to be upgraded ?',
				'FDM_Upgrade_Select_desired_FDM_release': 'Select desired FDM release ?',
				'FDM_Upgrade_FDM_Media_Delivery':'FDM Media Delivery',
				'Attr_FDM_Upg_FDMsUpgraded': 'Number of FDMs to be Upgraded?',
				'FDM_Upgrade_Additional_Components': 'Are Additional Components being offered?'},
			'FDM_Upgrade_Services':{
				'Attr_Servicesheader':'Services',
				'Attr_Experion/TPSSer':'Number of Experion/TPS Server interfaces (if integrated)',
				'Attr_FDMGateways':'Number of FDM Gateways',
				'Attr_NetworkInterf_Lic':'Number of Server Network Interface Licenses',
				'Attr_ExpStationsFDM':'Number of Exp Stations w/FDM Maintenance Station View features?',
				'FDM_Upgrade_Site_Acceptance_Test':'Site Acceptance Test',
				'Attr_DMPVST_Planner':'Number of PVST Planner Licenses / Devices supported by HART ESD devices?'}
		},
        'FDM Upgrade 2': {
			'FDM_Upgrade_2_General_questions':{
				'Attr_Fdmupg1_generalques':'General questions - Field Device Manager (FDM) Upgrade',
				'FDM_Upgrade_What_is_the_current_release':'What is the current release of the system to be upgraded ?',
				'FDM_Upgrade_Select_desired_FDM_release':'Select desired FDM release ?',
				'FDM_Upgrade_FDM_Media_Delivery':'FDM Media Delivery',
				'Attr_FDM_Upg_FDMsUpgraded':'Number of FDMs to be Upgraded?',
				'FDM_Upgrade_Additional_Components':'Are Additional Components being offered?'},
			'FDM_Upgrade_2_Services':{
				'Attr_Servicesheader':'Services',
				'Attr_Experion/TPSSer':'Number of Experion/TPS Server interfaces (if integrated)',
				'Attr_FDMGateways':'Number of FDM Gateways',
				'Attr_NetworkInterf_Lic':'Number of Server Network Interface Licenses',
				'Attr_ExpStationsFDM':'Number of Exp Stations w/FDM Maintenance Station View features?',
				'FDM_Upgrade_Site_Acceptance_Test':'Site Acceptance Test',
				'Attr_DMPVST_Planner':'Number of PVST Planner Licenses / Devices supported by HART ESD devices?'}
        },
        'FDM Upgrade 3': {
			'FDM_Upgrade_3_General_questions':{
				'Attr_Fdmupg1_generalques':'General questions - Field Device Manager (FDM) Upgrade',
				'FDM_Upgrade_What_is_the_current_release':'What is the current release of the system to be upgraded ?',
				'FDM_Upgrade_Select_desired_FDM_release':'Select desired FDM release ?',
				'FDM_Upgrade_FDM_Media_Delivery':'FDM Media Delivery',
				'Attr_FDM_Upg_FDMsUpgraded':'Number of FDMs to be Upgraded?',
				'FDM_Upgrade_Additional_Components':'Are Additional Components being offered?'},
			'FDM_Upgrade_3_Services':{
				'Attr_Servicesheader':'Services',
				'Attr_Experion/TPSSer':'Number of Experion/TPS Server interfaces (if integrated)',
				'Attr_FDMGateways':'Number of FDM Gateways',
				'Attr_NetworkInterf_Lic':'Number of Server Network Interface Licenses',
				'Attr_ExpStationsFDM':'Number of Exp Stations w/FDM Maintenance Station View features?',
				'FDM_Upgrade_Site_Acceptance_Test':'Site Acceptance Test',
				'Attr_DMPVST_Planner':'Number of PVST Planner Licenses / Devices supported by HART ESD devices?'}
        },
        'xPM to C300 Migration': {
            'xPM_C300_General_Qns_Cont': {
                'xPM_C300_FTE_System_already_installed_on_Site':'xPM_C300_FTE_System_already_installed_on_Site', 'xPM_C300_FTE_switch':'xPM_C300_FTE_switch',
                'ATT_NUMADSWT':'xPM_C300_Number_of_additional_switches', 'xPM_C300_Is_Honeywell_Providing_FTE_cables':'xPM_C300_Is_Honeywell_Providing_FTE_cables', 
                'xPM_C300_Average_Cable_Length':'PM_C300_Average_Cable_Length', 'ATT_NUMXPMC300':'xPM_C300_Number_of_xPMs_to_be_Migrated_to_C300_with_PMIO', 
                'xPM_C300_General_redundancy':'xPM_C300_General_redundancy'},
            'xPM_C300_Services_Cont': {
                'ATT_NUMAMTOACE':'xPM_C300_Number_of_AM_migrating_to_ACE',
                'ATT_NUMAMPTS':'xPM_C300_Number_of_AM_points',
                'xPM_C300_Data_Gathering_required':'xPM_C300_Data_Gathering_required',
                'xPM_C300_Will_Honeywell_perform_equipment_installa':'xPM_C300_Will_Honeywell_perform_equipment_installa'}
        },
        'C200 Migration': {
            'C200_Migration_Scenario_Cont': {
                'C200_Select_Migration_Scenario': 'C200_Select_the_Migration_Scenario'},
            'C200_Services_2_Cont': {
                'C200_Factory_Acceptance_Test_Required':'C200_Factory_Acceptance_Test_Required', 'C200_Will_Honeywell_perform_equipment_installation':'C200_Will_Honeywell_Perform_Equipment_Installation_Activities'},
            'C200_Services_1_Cont': {
                'C200_Data_Gathering_Required':'C200_Data_Gathering_Required',
                'C200_Documentation_Required':'C200_Documentation_Required',
                'C200_additional_hrs_ins':'C200_additional_hours_for_UOC_installation'}
        },
        'EHPM/EHPMX/ C300PM': {
            'xPM_Migration_Scenario_Cont': {
                'xPM_Select_the_migration_scenario':'xPM_Select_the_migration_scenario'},
            'xPM_Network_Upgrade_Cont': {
                'xPM_Customer_requires_Fiber_Communication': 'xPM_Customer_requires_Fiber_Communication',
                'xPM_Distance_of_Fiber_Optic_Extenders': 'xPM_Distance_of_Fiber_Optic_Extenders',
                'ATT_QRPCF9IOTA': 'xPM_Qty_of_Red_pair_of_CF9_firewalls',
                'ATT_QARPCF9IOTA': 'xPM_Qty_Additional_Red_pair_of_CF9_firewalls',
                'ATT_QFTENK': 'xPM_Qty_of_FTE_Networks_kits'},
            'xPM_Services_Cont': {
                'xPM_Factory_Acceptance_Test_Required':'xPM_Factory_Acceptance_Test_Required',
                'MSID_Will_Honeywell_perform_equipment_installation':'MSID_Will_Honeywell_perform_equipment_installation'},
            'ENB_Migration_General_Qns_Cont': {
                'xPM_NIMsconf': 'xPM_Number_of_NIMs_configurations_to_be_migrated',
                'xPM_DNCFLPCN': 'xPM_Number_of_DNCF_long_power_cable_needed',
                'xPM_NUMDNCF': 'xPM_Number_of_DNCF_needed'}
        },
        'TPS to Experion': {
            'TPS_EX_General_Questions': {
                'ATT_IS_Migration_Part_Of_ELCN_Migration': 'IS_Migration_Part_Of_ELCN_Migration',
                'TPS_EX_Setup_FTE_Network_Infrastructure': 'Setup_FTE_Network_Infrastructure',
                'TPS_EX_FTE_Switch_Type': 'FTE_Switch_Type',
                'TPS_EX_Additional_Switches': 'Additional_Switches',
                'FTE_Switch_Type':'Additional_Switches_Type',
                'TPS_EX_QTY_New_Cabinates': 'QTY_New_Cabinates',
                'TPS_EX_Media_Kit_Type': 'TPS_EX_Media_Kit_Type',
                'TPS_EX_Additional_Server_Stations_Required': 'Additional_Server_ESV_Stations_ESF_ESC_ESF_Required'},
            'TPS_EX_Bundle_Conversion_Server_Stations': {
                'TPS_EX_Non_Reduntant_Conversion_ESVT': 'TPS_EX_Non_Reduntant_Conversion_ESVT',
                'TPS_EX_Redundant_Conversion_ESVT': 'TPS_EX_Redundant_Conversion_ESVT',
                'TPS_EX_Bundle_Conversion_Existing_Node': 'TPS_EX_Bundle_Conversion_Existing_Node',
                'TPS_EX_Bundle_Conversion_ESVT_Server_Hardware': 'TPS_EX_Bundle_Conversion_ESVT_Server_Hardware',
                'TPS_EX_Bundle_Conversion_EST_Station_Hardware': 'TPS_EX_Bundle_Conversion_EST_Station_Hardware',
                'TPS_EX_Bundle_Conversion_EST_Station_Mounting_Furn': 'TPS_EX_Bundle_Conversion_EST_Station_Mounting_Furn'},
            'TPS_EX_Service': {
                'TPS_EX_Service_Switch_Config_Honeywell_Scope': 'TPS_EX_Service_Switch_Config_Honeywell_Scope',
                'TPS_EX_Service_Acceptance_Test_Required': 'TPS_EX_Service_Acceptance_Test_Required',
                'ATT_TPS_Qty_Existing_Cabinets':'Qty_Existing_Cabinets_Server_Switches_Stations',
                'TPS_EX_Will_System_be_migrated_virtual_system':'TPS_EX_Will_System_be_migrated_virtual_system',
                'TPS_Will_Honeywell_perform_equipment_installation':'TPS_Will_Honeywell_perform_equipment_installation'},
            'TPS_EX_Conversion_ESVT_Server': {
                'TPS_EX_TDC_US_ESVT': 'TPS_EX_TDC_US_ESVT',
                'TPS_EX_TDC_AM_ESVT': 'TPS_EX_TDC_AM_ESVT',
                'TPS_EX_TDC_APP_ESVT': 'TPS_EX_TDC_APP_ESVT',
                'TPS_EX_TDC_GUS_ESVT': 'TPS_EX_TDC_GUS_ESVT',
                'TPS_EX_ESVT_WO_Trade_Ins': 'TPS_EX_ESVT_WO_Trade_Ins',
                'TPS_EX_ESVT_Redundant': 'TPS_EX_ESVT_Redundant',
                'TPS_EX_ESVT_Server_Hardware': 'TPS_EX_ESVT_Server_Hardware',
                'TPS_EX_Additional_Hard_Drives': 'TPS_EX_Additional_Hard_Drives',
                'TPS_EX_Qty_Of_Cabinet_Slide_Mounting_For_Servers': 'TPS_EX_Qty_Of_Cabinet_Slide_Mounting_For_Servers',
                'TPS_EX_Qty_Of_Cabinet_Fix_Mounting_For_Servers': 'TPS_EX_Qty_Of_Cabinet_Fix_Mounting_For_Servers'}
        },
        'LM to ELMM ControlEdge PLC': {
            'LM_to_ELMM_ControlEdge_PLC_Migration_Gen_Cont': {
                'LM_to_ELMM_Experion_Release': 'LM_Current_Experion_Release',
                'ATT_LM_ELMM_DOES_THE_CUSTOMERTPN_RELEASE': 'LM_Does_The_Customer_Have_TPN_Release_R688.1_Or_Later',
                'LM_to_ELMM_FTE_Switch_To_Connect_ControlEdge_PLC': 'LM_FTE_Switch_To_Connect_ControlEdge_PLC',
                'ATT_LM_ADDITIONALSWITCHES': 'LM_Number_Of_Additional_Switches',
                'ATT_LM_ELMM_ADDITIONAL_SWITCH': 'LM_Additional_Switch_Selection',
                'ATT_LM_ELMM_HONEYWELL_PROVIDE_FTE': 'Is_Honeywell_Providing_FTE_Cables',
                'LM_to_ELMM Cable Length': 'Average_Cable_Length_For_PLC_Uplink',
                'ATT_LM_QTY_OF_LMPAIR_TOBE_MIGRATED': 'LM_Qty_Of_LM_Pair_To_Be_Migrated',
                'LM_to_ELMM_ControlEdge_PLC_Operating_temperature': 'LM_to_ELMM_ControlEdge_PLC_Operating_temperature'},
            'LM_to_ELMM_Services': {
                'AT_LM_ELMM_FELDATA_REQUIRED': 'LM_to_ELMM_FEL_Data_gathering_required',
                'ATT_LM_ELMM_FACTORY_ACCEPTANCE': 'LM_to_ELMM_Factory_Acceptance_Test_requested',
                'ATT_LT_ELMM_HONEYWELL_INSTALLATION': 'LM_to_ELMM_Will_Honeywell_perform_equipment_installation_activities'}
        },
        'CD Actuator I-F Upgrade': {
            'CD_Actuator_IF_Upgrade_General_Info_Cont': {
                'ATT_CD_ACTUATOR_NOZONES': 'CD_Actuator_Number_of_Actuators_Zones',
                'CD_Actuator_Actuator_Type': 'CD_Actuator_Actuator_Type',
                'CD_Actuator_IF_Actuator_Model': 'CD_Actuator_Actuator_Model',
                'CD_Actuator_Processor_Type': 'CD_Actuator_Processor_Type',
                'CD_Actuator_Interlocks': 'CD_Actuator_Interlocks',
                'CD_Actuator_QCS_Type': 'CD_Actuator_QCS_Type',
                'ATT_CD_EXISTING_SETSOF_EXTRA_EDGEACTUATORS': 'CD_Actuator_Existing_sets_of_extra_edge_actuators',
                'CD_Actuator_Will_the_current_Interlocks_be': 'CD_Actuator_Will_the_current_Interlocks_be',
                'CD_Actuator_Interlock_Voltage': 'CD_Actuator_Interlock_Voltage',
                'ATT_CD_ACTUATOR_LINE_SINGLE_PHASE': 'CD_Actuator_Line_Voltage_Single_Phase_Supply_Voltage',
                'ATT_CD_ACTUATOR_LINE_THREE_PHASE': 'CD_Actuator_Line_Voltage_Three_Phase_Supply_Voltage',
                'ATT_CD_IF_OTHERS_PROVIDE_INFO': 'CD_Actuator_If_other_please_provide_information',
                'CD_Actuator_Lynk_Type': 'CD_Actuator_Lynk_Type',
                'CD_Actuator_For_Aquatrol_what_is_solenoid_voltage': 'CD_Actuator_For_Aquatrol_what_is_solenoid_voltage',
                'CD_Actuator_For_Caltrol_or_Thermatrol_Is_feedback': 'CD_Actuator_For_Caltrol_or_Thermatrol_Is_feedback'},
            'CD_Actuator_IF_Upgrade_Services_Cont': {
                'CD_Actuator_HSE_and_Quality_Plan': 'CD_Actuator_HSE_and_Quality_Plan_required',
                'CD_Actuator_Update_existing_documents': 'CD_Actuator_Update_existing_documents',
                'CD_Actuator_SAT_required': 'CD_Actuator_SAT_required'}
        },
        'EHPM HART IO': {
            'EHPM_HART_IO_Services_Cont': {
                'EHPM_HART_IO_NES': 'Number_of_Experion_Systems',
                'EHPM_HART_IO_WBI': 'Number_of_EHPM_where_HART_IO_will_be_installed',
                'EHPM_HART_IO_Wiring_termination_type': 'Wiring_termination_type',
                'EHPM_HART_IO_Commissioning_required?': 'Commissioning_required',
                'EHPM_HART_IO_Will_Honeywell_equipment_activities': 'EHPM_HART_IO_Will_Honeywell_perform_equipment_installation_activities'}
        },
        'Orion Console': {
            'Orion_General_Information_Container2': {
                'Attr_NoOfOrion Console': 'Orion_Number_of_Orion_Console_configurations_needed'},
            'Orion_Services': {
                'Orion_How_is_this_Orion_Console_Installation': 'Orion_How_is_this_Orion_Console_Installation_performed',
                'Attr_NoOfexistingstations': 'Orion_Number_of_existing_stations_that_will_be_migrated_to_Orion_Console',
                'Attr_OrionStationsInstalled': 'Orion_Number_of_new_Orion_stations_that_will_be_installed',
                'Attr_HMIGraphics': 'Orion_Number_of_existing_HMI_Graphics',
                'Attr_installationControl Room': 'Orion_Honeywell_hours_for_Orion_Console_unboxing_and_installation_in_Control_Room',
                'Orion_Is_Graphics_Scaling_needed': 'Orion_Is_Graphics_Scaling_needed',
                'MSID_Will_Honeywell_perform_equipment_installation': 'MSID_Will_Honeywell_perform_equipment_installation'}
        },
        'FSC to SM':{ 
            'FSC_to_SM_Services': {
                'FSC_SM_Are_the_system_drawings_currently_on_site':'FSC_to_SM_Are_the_system_drawings_currently_on_site_up_to_date',
                'FSC_to_SM_ACAD':'FSC_to_SM_ACAD',
                'FSC_to_SM_Factory_Acceptance_Test_required':'FSC_to_SM_Factory_Acceptance_Test_required',
                'FSC_to_SM_Has_the_System_Audit_been_performed':'FSC_to_SM_Has_the_System_Audit_been_performed',
                'ATT_FSC_to_SM_On_Site_Eng_hours':'FSC_to_SM_On_Site_Eng_hours_per_Audit_Report',
                'ATT_FSC_to_SM_In_Office_Eng_hours':'FSC_to_SM_In_Office_Eng_hours_per_Audit_Report'},
            'FSC_to_SM_General_Information':{
                'ATT_FSC_to_SM_Number_of_configurations':'FSC_to_SM_Number_of_configurations_to_be_migrated'}
        },
        'TCMI':{
            'TCMI_Services':{
                'TCMI_Is_Triconex_SMM_being_migrated_with_xPM_in':'TCMI_Is_Triconex_SMM_being_migrated_with_xPM_in'}
        },
        'FSC to SM IO Migration':{
            'FSC_to_SM_IO_New_SM_Cabinet_Configuration':{
                'FSC_to_SM_IO_Cabinet_IP_Rating':'FSC_to_SM_IO_Cabinet_IP_Rating',
                'FSC_to_SM_IO_Cabinet_Base_Plinth':'FSC_to_SM_IO_Cabinet_Base_Plinth',
                'FSC_to_SM_IO_Cabinet_Front_Door':'FSC_to_SM_IO_Cabinet_Front_Door',
                'FSC_to_SM_IO_Cabinet_Rear_Door':' FSC_to_SM_IO_Cabinet_Front_Door',
                'FSC_to_SM_IO_Cabinet_Light':' FSC_to_SM_IO_Cabinet_Front_Door',
                'FSC_to_SM_IO_Swing_Frame':'FSC_to_SM_IO_Swing_Frame',
                'FSC_to_SM_IO_Cabinet_Depth':'FSC_to_SM_IO_Cabinet_Depth',
                'FSC_to_SM_IO_Cabinet_Access':'FSC_to_SM_IO_Cabinet_Access'},
            'FSC_to_SM_IO_Services':{
                'FSC_to_SM_IO_Is_Honeywell_executing_the_field_cros':'FSC_to_SM_IO_Is_Honeywell_executing_the_field_cros',
                'FSC_to_SM_IO_Software_Factory_Acceptance_Test_Requ':'FSC_to_SM_IO_Software_Factory_Acceptance_Test_Requ',
                'FSC_to_SM_IO_Has_the_FSC_IO_Audit_been_performed':'FSC_to_SM_IO_Has_the_FSC_IO_Audit_been_performed'},
            'FSC_to_SM_IO_Migration_General_Information':{
                'ATT_FSCtoSMIOMigrationTotalFSC':'FSC_to_SM_IO_Migration_Total_FSC_SM_Systems',
                'FSC_to_SM_IO_Migration_Where_will_IO_be_installed':'FSC_to_SM_IO_Migration_Where_will_the_IOs_be_installed'}
        },
        'CB-EC Upgrade to C300-UHIO': {
            'CB_EC_Services_1_Cont': {
                'CB_EC_Is_CB/EC_interfacing_with_DHEB_on_the_system': 'CB_EC_Is_CB_EC_interfacing_with_DHEB_on_the_system',
                'CB_EC_Does_the_customer_have_all_updated_ILDs': 'CB_EC_Does_the_Customer_have_all_updated_ILDs',
                'CB_EC_Does_the_Customer_validate_ILDs_by_Honeywell': 'CB_EC_Does_Customer_want _to_validate_ILDs_by_Honeywell',
                'ATT_CBECPSNEDR': 'CB_EC_Number_of_CB_EC_Power_Supplies_that_need_to_be_replaced',
                'CB_EC_Do_u_know_no.of_AI_AO_Regulatory': 'CB_EC_Do_you_know_the_number_of AI_AO_Regulatory_points_DI_DO_and_Digital_Composite_points',
                'ATT_CBECHGAIN': 'CB_EC_Total_Number_of_Analog_Input_points_HGAIN',
                'ATT_CBECHGOAT': 'CB_EC_Total_Number_of_Analog_Output_points_HGAOT',
                'ATT_CBECHGREG': 'CB_EC_Total_Number_of_Regulatory_points_HGREG',
                'ATT_CBECHGDIN': 'CB_EC_Total_Number_of_Digital_Input_points_HGDIN',
                'ATT_CBECHGDOT': 'CB_EC_Total_Number_of_Digital_Output_points_HGDOT',
                'ATT_CBECHGDCP': 'CB_EC_Total_Number_of_Digital_Composite_points_HGDCP',
                'ATT_CBECASLOOP': 'CB_EC_Total_Number_of_Cascade_Loop',
                'ATT_CBECOMLOOP': 'CB_EC_Total_Number_of_Complex_Loop',
                'ATT_CBECAUXFUN': 'CB_EC_Total_Number_of_Aux_function'},
            'CB_EC_Services_2_Cont': {
                'CB_EC_IsCommonPVsharingtwoormorethantwoCB/EC': 'CB_EC_Is_common_PV_sharing_between_two_or_more_than_two_CB_EC',
                'CB_EC_Detailed_DDS_required': 'CB_EC_Detailed_DDS_required',
                'CB_EC_Is_HotCutover_required': 'CB_EC_Is_HotCutover_required',
                'CB_ECWillHoneywellperforminstallationactivities': 'CB_EC_Will_Honeywell_perform_equipment_installation_activities',
                'CB_EC_Data_Gathering_required': 'CB_EC_Data_Gathering_required'}
        },
        'Graphics Migration':{
            'Graphics_Migration_Additional_Questions':{
                'Graphics_Migration_Gap_Analysis_done?':'Gap Analysis done?',
                'Graphics_Migration_For_GAP_Analysis_project_com':'For GAP Analysis - project complexity/language adds',
                'Graphics_Migration_DCA_IRA_done?':'DCA / IRA done?',
                'Graphics_Migration_New_Safeview_Configuration':'New Safeview Configuration',
                'Graphics_Migration_Alarm_groups_configured?':'Alarm groups configured?',
                'ATT_GMNUMSL':'Number of station licenses (0 - 64)',
                'ATT_GMOBJSI':'Number of object scripts to be implemented (0 - 10,000)',
                'ATT_GMADGAPAN':'Additional hours for customized graphics after GAP analysis'},
            'Graphics_Migration_Training_Testing_Documentation':{
                'Graphics_Migration_FAT_required?':'FAT required?',
                'Graphics_Migration_Does_the_customer_require_SAT?':'Does the customer require SAT?',
                'Graphics_Migration_Does_require_Operator_Training?':'Does the customer require Operator Training (Basic)?',
                'ATT_GMTRNSESREQ':'How many training sessions are required?',
                'Graphics_Migration_FDS_Required?':'FDS Required?',
                'Graphics_Migration_DDS_Required?':'DDS Required?'},
            'Graphics_Migration_Migration_Scenario':{
                'Graphics_Migration_Select_Vertical_Market':'Select Vertical Market',
                'Graphics_Migration_Type_of_Existing_Displays':'Type of Existing Displays',
                'Migration_Configuration_Is_Standard_Builds_used':'Is Standard Builds used for EXP to EXP?',
                'ATT_GMPERUSD':'For existing US/GUS/DSP what percentage of Standard Builds will be used? (0% - 100%)',
                'Migration_Graphics_Using_device_control_digital':'Using device control/digital composite block for all digital equipment?',
                'Migration_Graphics_Have_multiple_DI_or_DO':'Have multiple DI or DO parameters that must be combined in one shape?',
                'Graphics_Migration_Is_the_system_connected_to':'Is the system connected to Hiway Gateway Controllers?',
                'Graphics_Migration_Require_multi_tag_shapes':'Require multi tag shapes?',
                'Graphics_Migration_Have_process_module_point':'Have process module point (AM custom Data points) as part of the point configuration?',
                'Graphics_Migration_Require_an_HMI_interface_for_AM':'Require an HMI interface for AM or HPM CL applications?',
                'Migration_Graphics_Have_array_point_that_requires':'Have array point that requires a HMIWeb interface?',
                'Migration_Graphics_Willing_to_accept_alternative':'Willing to accept alternative visualization solution for specific functions?',
                'Graphics_Migration_Have_specific_native_or_GUS':'Have specific native or GUS displays that support a specific application?'},
        'Common Questions':{ 
            'MSID_CommonQuestions': {
                'MSID_Is_Site_Acceptance_Test_Required':'Is Site Acceptance Test Required?'}
        }
                }
    }
def getMultiLineMapperDict():
    return {}