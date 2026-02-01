class MigrationProductsAttributesContainerColumns:
    products = {
        'OPM' : {
            'hideAttrList' : ["OPM_is_system_required_Domain_controller_upgrade","ATT_OPMADNLHRS"]
        },
        'FSC to SM IO Migration' : {
            'hideAttrList' : ['FSC_SM_IO_Total_ Calculated_SIC_cables','FSC_SM_IO_SIC_Cable']
        },
        'Orion Console' : {
            'hideAttrList' : ['Attr_installationControl Room'],
            'hideContainerColumnDict' : {
                'Orion_Station_Configuration': ['Orion_Number_of_Additional_23_monitors','Orion_Number_of_Additional_Monitor_Mounting_Arm_for_23','Orion_Console_Alarm_Light_Custom_Logo','Orion_Extended_Heigh_Alarm_Ligth_Panel','Orion_Alarm_Sounds']
            }
        },
        'C200 Migration' : {
            'hideAttrList' : ['C200_additional_hrs_ins'],
            'hideContainerColumnDict' : {
                'C200_Migration_Config_Cont' : ['C200_Required_Modbus_Firewall']
            },
        },
        'Graphics Migration' : {
            'hideAttrList' : ['ATT_GMPERUSD','Graphics_Migration_For_GAP_Analysis_project_com','Graphics_Migration_Gap_Analysis_done?','ATT_GMADGAPAN','ATT_GMOBJSI','Graphics_Migration_DCA_IRA_done?','Graphics_Migration_New_Safeview_Configuration'],
            'hideContainerColumnDict' : {
                'Graphics_Migration_Displays_Shapes_Faceplates': ['Number_of_Simple_Displays', 'Number_of_Medium_Displays','Number_of_Complex_Displays','Number_of_Very_Complex_Displays','Number_of_Repeats_Displays','Number_of_Simple_Custom_Shapes','Number_of_Medium_Custom_Shapes','Number_of_Complex_Custom_Shapes','Number_of_Very_Complex_Custom_Shapes','Number_of_Simple_Custom_Faceplates','Number_of_Medium_Custom_Faceplates','Number_of_Complex_Custom_Faceplates','Number_of_Very_Complex_Custom_Faceplates','Number_of_Repeats_Custom_Faceplates','Number_of_Custom_Context_Menus','Number_of_Repeats_Custom_Shapes','Experion_shapes_multiplier','Total_Number_of_Custom_Shapes','Total_Number_of_Custom_Faceplates']
            }
        },
        '3rd Party PLC to ControlEdge PLC/UOC' : {
            'hideAttrList' : ['LSS_Number_of_Soft_IO_for_CE_PLC','LSS_Number_of_Comm_IO_for_P2P','LSS_Number_of_Miscellaneous_Logic','LSS_Number_of_Simple_Close_Loop_Programming','LSS_Number_of_Complex_Close_Loop_Programming','LSS_Number_of_Sequence_Programming','LSS_Is_IO_details_database_available?','LSS_Is_PLC_Program_backup/Pdf_report_available?','LSS_Is_Input/Output_Loop_diagram_available','LSS_Existing_Cabinet_Drawing_available_dimensions','LSS_SCADA_Controntroller_Configuration','LSS_Third_party_items'],
            'hideContainerColumnDict' : {
                'LSS_Configuration_for_Rockwell_transpose': ['LSS_PLC_Ethernet_Switch_Supplier','LSS_PLC_G3_Option_Ethernet_Switch'],
            }
        },
        'CE PLC Remote Group':{
            'hideContainerColumnDict' : {
                'PLC_RG_Controller_Rack_Cont': ['PLC_Field_Wiring_DIDOAOAI_Channel_Mod','PLC_Field_Wiring_PIFII_Channel_Mod','PLC_Field_Wiring_Other_Mod','PLC_Remote_Terminal_Cable_Length']
            }
        },
        'UOC Control Group':{
            'hideContainerColumnDict' : {
                'UOC_CG_Controller_Rack_Cont': ['UOC_Field_Wiring_DIDOAOAI_Channel_Mod','UOC_Field_Wiring_Other_Mod','UOC_Remote_Terminal_Cable_Length','UOC_Ethernet_Switch_Supplier']
            }
        },
        'UOC Remote Group':{
            'hideContainerColumnDict' : {
                'UOC_RG_Controller_Rack_Cont': ['UOC_Field_Wiring_DIDOAOAI_Channel_Mod','UOC_Field_Wiring_Other_Mod','UOC_Remote_Terminal_Cable_Length']
            }
        },
        
        'xPM to C300 Migration' : {
            'hideAttrList' : ['ATT_NUMADSWT']},
        'Virtualization System' : {
            'hideAttrList' : ['VS_FTT_Level','VS_Distribute_Multi_Clusters','VS_24Port_Rack_Required','VS_48Port_Rack_Required']},
        'ControlEdge PLC System Migration' : {},
        'Terminal Manager' : {
            'hideAttrList' : ['Terminal_TM_Test_System_required?', 'Terminal_Media_kit_required', 'Terminal_Experion_Client_PC', 'Terminal_FTE_Switch', 'Terminal_Blank_Experion_Server_(ESV)', 'Terminal_Experion_Server_Hardware', 'Terminal_Additional_Hard_Drive', 'Terminal_Additional_Memory', 'Terminal_Optional_DVD', 'Terminal_Display_Required', 'Terminal_Trackball', 'Terminal_Cabinet_Mounting_Type','Terminal_Ges_Location_Labour', 'Terminal_TM_System_Complexity', 'Terminal_Feature_Type', 'Terminal_Number_of_Days_per_Design_Review', 'Terminal_Number_of_Reviews', 'Terminal_Number_of_Days_for_TM_FAT', 'Terminal_Number_of_Engineer_for_FAT', 'Terminal_Number_of_Days_for_TM_SAT', 'Terminal_Number_of_Engineer_for_SAT', 'Terminal_No_of_Reports_with_Simple_Changes', 'Terminal_No_of_Reports_with_Complex_Changes', 'Terminal_Number_of_New_Simple_Reports', 'Terminal_Number_of_New_Moderate_Reports', 'Terminal_Number_of_New_Complex_Reports', 'Terminal_Number_of_Simple_Screens_for_new_UI', 'Terminal_Number_of_Moderate_Screens_for_new_UI', 'Terminal_Number_of_Complex_Screens_for_new_UI','Terminal_Experion_Server_(ESV)_Type','Calculation_Button'], 
            'displayValueDict' : {
                "Terminal_Web_Portal_required?" : "No", "Terminal_Experion_Client_PC" : "Tower", "Terminal_FTE_Switch" : "EightPortCISCOSwitch", "Terminal_Blank_Experion_Server_(ESV)" : "Desk", "Terminal_Experion_Server_Hardware" : "DELL T550 STD TPM", "Terminal_Additional_Hard_Drive" : "No", "Terminal_Ges_Location_Labour" : "GES China", "Terminal_TM_System_Complexity" : "Moderate", "Terminal_Feature_Type" : "New Features (upto 5)", "Terminal_Additional_Memory" : "None", "Terminal_Optional_DVD" : "No", "Terminal_Display_Required" : "27 Inch", "Terminal_Trackball" : "No", "Terminal_Cabinet_Mounting_Type" : "None","Terminal_Weighbridge_Interface_required?" : "No","Terminal_SAP_ERP_BSI_Interface_required?":"No","Terminal_Card_Reader_Interface_required?":"No"},
            'defaultText' : {"Terminal_Number_of_Days_per_Design_Review" : "3", "Terminal_Number_of_Reviews" : "2", "Terminal_Number_of_Days_for_TM_FAT" : "5", "Terminal_Number_of_Engineer_for_FAT" : "1", "Terminal_Number_of_Days_for_TM_SAT" : "0", "Terminal_Number_of_Engineer_for_SAT" : "0", "Terminal_No_of_Reports_with_Simple_Changes" : "5", "Terminal_No_of_Reports_with_Complex_Changes" : "3", "Terminal_Number_of_New_Simple_Reports" : "2", "Terminal_Number_of_New_Moderate_Reports" : "3", "Terminal_Number_of_New_Complex_Reports" : "2", "Terminal_Number_of_Simple_Screens_for_new_UI" : "5", "Terminal_Number_of_Moderate_Screens_for_new_UI" : "3", "Terminal_Number_of_Complex_Screens_for_new_UI" : "2"
            }
            },
            
        'FDM Upgrade 1' : {
            'defaultText' : {
                "Attr_FDM_Upg_devmanaged" : "0", "Attr_FDM_Upg_AuditTrailDev" : "0", "Attr_FDM_Upg_HARTdevvendors" : "0", "Attr_FDMUpg_FDMClients" : "0", "Attr_Experion/TPS_Servers_FDMInt" : "0", "Attr_ServerNetInterfaceLic" : "0", "Attr_HWMUX_Net_MonitoringLic" : "0", "Attr_ExpServer_processI/Opoint" : "0","Attr_remPCs_FDMServerviaLAN" : "0", "Attr_PVST_HARTESD" : "0" }},
        'FDM Upgrade 2' : {
            'hideAttrList' : ['Attr_FDM_Upg_Dummy'],
            'defaultText' : {
                "Attr_FDM_Upg_devmanaged" : "0", "Attr_FDM_Upg_AuditTrailDev" : "0", "Attr_FDM_Upg_HARTdevvendors" : "0", "Attr_FDMUpg_FDMClients" : "0", "Attr_Experion/TPS_Servers_FDMInt" : "0", "Attr_ServerNetInterfaceLic" : "0", "Attr_HWMUX_Net_MonitoringLic" : "0", "Attr_ExpServer_processI/Opoint" : "0","Attr_remPCs_FDMServerviaLAN" : "0", "Attr_PVST_HARTESD" : "0" }},
        'FDM Upgrade 3' : {
            'defaultText' : {
                "Attr_FDM_Upg_devmanaged" : "0", "Attr_FDM_Upg_AuditTrailDev" : "0", "Attr_FDM_Upg_HARTdevvendors" : "0", "Attr_FDMUpg_FDMClients" : "0", "Attr_Experion/TPS_Servers_FDMInt" : "0", "Attr_ServerNetInterfaceLic" : "0", "Attr_HWMUX_Net_MonitoringLic" : "0", "Attr_ExpServer_processI/Opoint" : "0","Attr_remPCs_FDMServerviaLAN" : "0", "Attr_PVST_HARTESD" : "0" }},
        'Trace Software' : {
            'readAttrList' :['Trace_Software_What_is_the_scope'],
            'hideAttrList' :['Trace_Software_Select_desired_Release','Trace_Software_Additional_Media_Kits', 'LCM_Multiyear_Selection','Trace_Software_Scope_Choices','Trace_software_GES_Location','Trace_software_Active_Service_Contract'],
            'hideContainerColumnDict' : {
                "Trace_Software_License_Configuration_transpose": ["Trace_Software_Business_Level_Access"]
            }
        },
        'TPS to Experion' : {
            'showAttrList' : ['TPS_EX_Redundant_Conversion_ESVT','TPS_EX_Non_Reduntant_Conversion_ESVT'],
            'hideAttrList' : ['TPS_EX_Additional_Server_Stations_Required','TPS_EX_Media_Kit_Type'],
            'hideContainerColumnDict' : {
                'TPS_EX_Station_Conversion_EST': ['TPS_EX_Asset_DB', 'TPS_EX_Keyboard_Type'],'TPS_EX_Conversion_ACET_EAPP':['TPS_EX_Conversion_ACET_EAPP_Asset_DB','TPS_EX_Conversion_ACET_EAPP_Does_App_Contains_Sol','TPS_EX_Conversion_ACET_EAPP_Additional_Hard_Drive']
            }
        },
        'CB-EC Upgrade to C300-UHIO' : {
            'hideAttrList' : ['ATT_CBECASLOOP','ATT_CBECOMLOOP','ATT_CBECAUXFUN'],
            'hideContainerColumnDict' : {
                'CB_EC_migration_to_C300_UHIO_Configuration_Cont':['CB_EC_If_terminal_blocks_are_required_for_spare_UIO_points']
            }
        },
        'LM to ELMM ControlEdge PLC' : {
            'hideAttrList' : ['LM_to_ELMM_FTE_Switch_To_Connect_ControlEdge_PLC', 'ATT_LM_ADDITIONALSWITCHES'],
            'hideContainerColumnDict' : {
                'LM_to_ELMM_ControlEdge_PLC_Cont' : ['LM_CE_Power_Input_Type', 'LM_are_the_IO_Racks_remotely_located']
            },
            'showContainerColumnDict' : {
                'LM_to_ELMM_ControlEdge_PLC_Cont' : ['LM_average_Cable_length_for_IO_network_connection']
            }
        },
        'MSID_New' : {
            'hideAttrList' : ['Project_Execution_Year', 'R2Q_Alternate_Execution_Country', 'R2Q_PRJT_Proposal Language']
        },
        'Migration_New' : {
            'hideAttrList' : ['LCM_MultiYear_Project'],
            'nonR2QHideAttrList' : ['Project_Execution_Year', 'Sell Price Strategy', 'Customer_Budget_TextField', 'R2Q_Alternate_Execution_Country', 'R2Q_PRJT_Proposal Language', 'Order_Status'],
            'APAC' : ['India','None'],
            'EMEA' : ['Italy','Belgium','Netherlands','France','Spain','United Kingdom','Germany','South Africa','Croatia','Austria','Czech Republic','Egypt','United Arab Emirates','Norway','Portugal','Sweden','Switzerland','Turkey','Hungary','Poland','Bulgaria','Russia','Oman','Romania','Slovakia','Finland','Kazakhstan','Algeria','Angola','Qatar','Saudi Arabia','Iraq North','Iraq Center','None'],
            'AMER' : ['United States','Canada','Mexico','Argentina','Brazil','Chile','Colombia','Peru','None']
        },
        'ControlEdge PLC System' : {
            'hideContainerColumnDict' : {
                'PLC_Software_Question_Cont':['PLC_Media_Delivery','PLC_CE_Builder_Client', 'PLC_Migration_Tool_User_License', 'PLC_Subsea_MDIS_Interface'],
                'PLC_Common_Questions_Cont' :['PLC_Shielded_Terminal_Strip','PLC_IO_Filler_Module'],
                'PLC_Labour_Details' :['PLC_Ges_Location','PLC_Marshalling_Cabinet_Cont','PLC_Enter_Total_Cont'],
                'CE_PLC_System_Hardware' :['PLC_Engineering_Station_Model']
            }
        },
        'CE PLC Control Group' : {
            'hideContainerColumnDict' : {
                'PLC_CG_Cabinet_Cont':['PLC_Cabinet_Type','PLC_Cabinet_Door_Type', 'PLC_Cabinet_Door_Keylock', 'PLC_Cabinet_Power_Entry', 'PLC_Cabinet_Base_Size', 'PLC_Cabinet_Thermostat', 'PLC_Cabinet_Light'],
                'PLC_CG_Controller_Rack_Cont' :[ 'PLC_Power_Status_Mod_Redudant_Supply', 'PLC_Field_Wiring_DIDOAOAI_Channel_Mod', 'PLC_Field_Wiring_PIFII_Channel_Mod', 'PLC_Field_Wiring_Other_Mod', 'PLC_Remote_Terminal_Cable_Length',  'PLC_Ethernet_Switch_Type', 'PLC_G3_Option_Ethernet_Switch']
            }
        },
        'CE PLC Remote Group' : {
            'hideContainerColumnDict' : {
                'PLC_RG_Cabinet_Cont':['PLC_Cabinet_Type','PLC_Cabinet_Door_Type', 'PLC_Cabinet_Door_Keylock', 'PLC_Cabinet_Power_Entry', 'PLC_Cabinet_Base_Size', 'PLC_Cabinet_Thermostat', 'PLC_Cabinet_Light']
            }
        },
        'EHPM/EHPMX/ C300PM' : {
            'hideAttrList' : ["ATT_QRPCF9IOTA","ATT_QARPCF9IOTA"],
            'hideContainerColumnDict' : {
            "xPM_Config_Asset_DB_Cont": ["xPM_Number_of_xPMs_in_this_MSID", "xPM_7_slot_chassis", "xPM_15_slot_chassis", 			      "xPM_CE_Mark_or_Not"],"ENB_Config_Asset_DB_Cont":["xPM_Number_of_NIMs_in_this_MSID","xPM_CE_Mark_or_Not"]
            }
        },
        'Digital Video Manager' : {
            'hideAttrList' : ['DVM_Software_Release','DVM_Base_Media_Delivery','DVM_Implementation_Methodology','DVM_GES_Location','DVM_Number_of_Reviews','DVM_Number_of_Title_Page_Sheet','DVM_Number_of_Symbols','DVM_Number_of_Riser','DVM_Number_of_Overall_Site_Plans','DVM_Number_of_Enlarged_Site_Plans','DVM_Number_of_Building_Plans','DVM_Number_of_Room_Plans','DVM_Number_of_Camera_Details_Drawings','DVM_Number_of_Other_Details_Drawings','DVM_Number_of_Server_Rack_Configurations','DVM_Number_of_Workstation_Configurations','DVM_Number_of_Camera_field_wiring_types','DVM_Number_of_Other_Detail_field_wiring_types','DVM_Number_of_Server_Rack_Wiring_Diagrams','DVM_Number_of_Workstation_Wiring_Diagrams','DVM_Number_of_VSS_Control_Panel','DVM_Number_of_Camera_Panel','DVM_Number_of_Explosion_Proof_PTZ_Cameras','DVM_Number_of_Weather_Proof_PTZ_Cameras','DVM_Number_of_Interior_PTZ_Cameras','DVM_Number_of_Thermal_PTZ_cameras','DVM_Number_of_Explosion_Proof_Fixed_Cameras','DVM_Number_of_Weather_Proof_Fixed_Cameras','DVM_Number_of_Interior_Fixed_Cameras','DVM_Number_of_Thermal_Fixed_Cameras','DVM_Number_of_Streamers','DVM_Number_of_Converters','DVM_Number_of_DVM_DB_Servers','DVM_Number_of_DVM_CM_Servers','DVM_Number_of_Video_Analytic_Servers','DVM_Number_of_Cameras_with_Algorithms','DVM_Number_of_Graphics','DVM_Number_of_Network_Switches','DVM_FAT_Duration_in_Days_for_DVM','DVM_Number_of_DVM_Workstations','DVM_Redundant_DVM_Servers','Number_of_Experion_DVM_Group','Add_DVM_System_Group','Calculation_Button']
        ,'displayValueDict' : {
                "DVM_Implementation_Methodology": "Standard Build Estimate",
                "DVM_GES_Location":"GES China"
            },
        "defaultText":{"DVM_Number_of_Enlarged_Site_Plans":"0",
                             "DVM_Number_of_Building_Plans":"1",
                             "DVM_Number_of_Room_Plans":"2",
                             "DVM_Number_of_VSS_Control_Panel": "0",
                             "DVM_Number_of_Network_Switches":"2",
                             "DVM_FAT_Duration_in_Days_for_DVM":"5",
                             "DVM_Number_of_Thermal_PTZ_cameras":"0",
                             "DVM_Number_of_Thermal_Fixed_Cameras":"0",
                       		"DVM_Number_of_Video_Analytic_Servers":"0",
                       "DVM_Number_of_Thermal_PTZ_cameras":"0"
                      }
        },
        'Digital Video Manager Group':{
            'hideAttrList' : ['DVM_4_Camera_Interface','DVM_4_Camera_Camera_Server_Redundant_L','DVM_4_Camera_Database_Server_Redundant_L','DVM_Internet_Explorer/ Browser_Client','DVM_Video_Motion_Detection_Premium','DVM_Axis_MPEG-4_Adapter_License','DVM_Sony_Adapter_License','DVM_Honeywell_Series_Interface','DVM_Axis_and_Updated _M-JPEG_Adapter','DVM_HVA -Active_Alert_Base','DVM_HVA -Active_Alert_Standard_EP-DVMAAS','Alert_Standerd','DVM_HVA -People_Counting','DVM_HVA -Smart_Impressions','DVM_Encoder_I/O_Monitoring','DVM_Camera_Tamper_Detection','DVM_Bi-Directional_Audio','DVM_Ultrakeyboard_Integration','DVM_Additional_3rd Party_Client_L','DVM_Distributed_Video_Architecture','DVM_Authorized_Recording_Playback','DVM_Panasonic_Series_Interface','DVM_ONVIF_Device_Integration_License','DVM_Image_Blocking_License','DVM_Console_Client','DVM_PTZ_Activated_Recording_License','DVM_Mobile_Client_Connections','DVM_Same_Source_Video_Streaming','DVM_Edge_Device_Video_Storage_Support','DVM_Edge_Analytics_Support','DVM_AllGoVision_Analytics_Integration','DVM_BARCO_Video_Wall_Integration','DVM_Matrox_Video_Wall_Integration','DVM_High_Availability_Storage_Option','DVM_IPSOTEK_Analytics_Integration','DVM_AWIROS_Analytics_Integration','DVM_Honeywell_Maxpro_Integratio','DVM_Web_Portal','DVM_Video_Recording_Encryption','DVM_Public_Gateway','DVM_Occupancy_Compliance_Monitoring','DVM_Video_Wall_Output','Experion DVM Integration','Advanced Video Evidence Pack','RTSP_Video_Streaming_Interface','DVM_Matrox_Encoder_Adapter','DVM_Flare_Snapshot_Manager','Calculation_Button'],
            "displayValueDict":{
                "DVM_4_Camera_Database_Server_Redundant_L":"Yes",
                "DVM_4_Camera_Camera_Server_Redundant_L":"Yes",
                "DVM_PTZ_Activated_Recording_License":"Yes",
                "DVM_Axis_MPEG-4_Adapter_License":"Yes",
                "DVM_Honeywell_Series_Interface":"Yes",
                "DVM_Camera_Tamper_Detection":"Yes",
                "DVM_ONVIF_Device_Integration_License":"Yes",
                "Experion DVM Integration":"Yes",
                "DVM_Axis_MPEG-4_Adapter_License":"Yes",
                "Experion DVM Integration":"Yes"
            },
            "defaultText":{
                "DVM_Console_Client":"1",
                "DVM_Additional_3rd Party_Client_L":"1",
                "DVM_Internet_Explorer/ Browser_Client":"2"
            }
            },
        'Public Address General Alarm System' : {
            'hideAttrList' : ['PAGA_Implementation_Methodology','PAGA_GES_Location','PAGA_Is_Site_Study_with_Feasibility_Report_require','PAGA_Is_Civil_Scope_of_Work_(SOW)_required?','PAGA_Is_Electrical_Scope_of_Work_(SOW)_required?','PAGA_Are_Recorded_Messages_required_for_PAGA?','PAGA_Number_of_Reviews_(add Asbuilts)','PAGA_Number_of_PAGA_Cabinets','PAGA_Number_of_Digital_Output_Modules_(DOM)','PAGA_Number_of_Universal_Interface_Modules_(UIM)','PAGA_Number_of_Messages','PAGA_Number_of_Speakers']
        ,'displayValueDict' : {
                "PAGA_GES_Location":"GES China"
            }},
            'Tank Gauging Engineering' : {
            'hideAttrList' : ['TGE_GES Location','TGE_Number of Vertical Tanks with RADAR Gauge','TGE_Number of Vertical Tanks with SERVO Gauge','TGE_Number of Horizontal Tanks w RADAR(GWR) Gauges','TGE_Number of Horztal Tank w Other(Optilevel)Gauge']
        ,'displayValueDict' : {
                "TGE_GES Location":"GES China"
            }},
            'Fire Detection & Alarm Engineering' : {
            'hideAttrList' : ['FDA Implementation Methodology','FDA Graphics Required','FDA Interface Required','FDA IP scheme Required','FDA Functional Description Required','FDA XLS Software Configuration Document Required','FDA EBI Software Configuration Document Required','FDA Panels Networked','FDA Rudundant EBI Servers','FDA Wire List Required','FDA Number of Reviews (add Asbuilts) (2-5)','FDA Number of Title Page Sheet Index (1-20)','FDA Number of Symbols Notes and Legend (0-2)','FDA Number of Architecture Diagrams (1-10)','FDA Number of Overall Site Plans','FDA Number of Enlarged Site Plans','FDA Number of Building Plans','FDA Number of Room Plans','FDA Number of XLS Panels','FDA Number of SLC Loops','FDA Number of Additional Power Supply Boxes','FDA Number of XLS Interfaces','FDA Number of Standard Detectors','FDA Number of Specialty Detectors','FDA Number of Monitor Module points','FDA Number of 4-20mA monitor module points','FDA Number of Control module points','FDA Number of Isolation modules','FDA Number of pull stations','FDA Number of horns','FDA Number of strobes','FDA Number of combination units','FDA Number of FNAs','FDA Number of UL/nonUL Switches','FDA Number of Fiber to copper converters','FDA Number of EBI Servers','FDA Number of EBI Workstations','FDA Number of EBI interfaces to other systems','FDA Number of Graphics','FDA GES Location'],
            'displayValueDict' : {
                "FDA GES Location":"GES China", "FDA Interface Required" : "Yes", "FDA Functional Description Required" : "Yes", "FDA XLS Software Configuration Document Required" : "Yes", "FDA Panels Networked" : "Yes", "FDA Wire List Required" : "Yes"
            },
            'defaultText' : {
                "FDA Number of XLS Panels" : "1", "FDA Number of XLS Interfaces" : "1", "FDA Number of Control module points" : "10", "FDA Number of FNAs" : "1", "FDA Number of UL/nonUL Switches" : "1", "FDA Number of Fiber to copper converters" : "2", "FDA Number of Graphics" : "10"
            }
            },
        'Industrial Security (Access Control)' : {
            'hideAttrList' : ['IS_Implementation_Methodology','IS_GES_Location','IS_Informal_Cust_EIS_(EBI)/Photo_ID_Training_Req','IS_Informal_Customer_Tema_Training_Required','IS_Standard_Customer_Training_Required','IS_IP_Scheme_Required','IS_Wire_List_Required','IS_User_Requirement_Specification_Required','IS_Functional_Design_Specification_Required','IS_Detailed_Functional_Design_Specification_Req','IS_FAT_Documentation_Required','IS_SAT_Documentation_Required','IS_Updated_BOM_Required','IS_Updated_Cutsheets_Required','IS_Operations_Manual_Required','IS_Is_Muster_Report_Required','IS_Factory_Acceptance_Test_Required','IS_Site_Acceptance_Test_Required','IS_Is_TWIC_Server_Required_with_PIV_Check','IS_Redundant_EIS_(EBI)_Servers','IS_No_of_Reviews_(add_Asbuilts)_(2-5)','IS_No_of_Title_Page_Sheet_Index_(1-20)','IS_No_of_Symbols_Notes_and_Legend_(0-2)','IS_No_of_Riser_Diagrams_(0-250)','IS_No_of_Overall_Site_Plans_(0-20)','IS_No_of_Enlarged_Site_Plans_(0-100)','IS_No_of_Building_Plans_(0-100)','IS_No_of_Room_Plans_(0-100)','IS_No_of_Door_Details_Drawings_(0-250)','IS_No_of_Gate_Details_Drawings_(0-25)','IS_No_of_Turnstile_Details_Drawings_(0-25)','IS_No_of_IDS_Alarm_Details_Drawings_(0-25)','IS_No_of_Perimeter_Detection_Details_Drawings','IS_No_of_Other_Details_Drawings_(0-300)','IS_No_of_Muster_Reader_Detail_Drawings','IS_No_of_Door_Wiring_Detail_Drawings','IS_No_of_Gate_Wiring_Detail_Drawings','IS_No_of_Turnstile_Wiring_Detail_Drawings','IS_No_of_IDS_Wiring_Detail_Drawings','IS_No_of_Perimeter_Detec_Wiring_Details_Drawings','IS_No_of_TWIC_Wiring_Detail_Drawings','IS_No_of_TWIC_Reader_Installation_Details_Drawings','IS_No_of_Door_Configuration_Field_Wiring_Types','IS_No_of_Gate_Controller_Field_Wiring_Types_(0-20)','IS_No_of_Other_Detail_Field_Wiring_Types_(0-20)','IS_No_of_Server_Rack_Configurations_(0-10)','IS_No_of_Workstation_Configurations_(0-10)','IS_No_of_Access_Control_cabinet/JB_Layouts_(0-100)','IS_No_of_IDS_Control_cabinet/JB_Layouts_(0-100)','IS_No_of_Shared_cabinet/JB_Layouts_(0-100)','IS_No_of_Server_Rack_Wiring_Diagrams_(0-10)','IS_No_of_Workstation_Wiring_Diagrams_(0-10)','IS_No_of_Access_Control_cabinet/JB_Wiring_Diagrams','IS_No_of_VSS_Control_cabinet/JB_Wiring_Diagrams','IS_No_of_Shared_cabinet/JB_Wiring_Diagrams_(0-100)','IS_No_of_EIS_Points_(0-5000)','IS_FAT_Duration_in_Days','IS_SAT_Duration_in_Days','IS_No_of_RTUs_(0-10000)','IS_No_of_TemaServers_(0-200)','IS_No_of_Tema_Multis_(0-10)','IS_No_of_Digital_Inputs_(0-100)','IS_No_of_Digital_Outputs_(0-100)','IS_No_of_Zones_(0-100)','IS_No_of_Doors_(0-100)','IS_No_of_Gates_(0-100)','IS_No_of_Turnstiles_(0-100)','IS_No_of_Muster_Readers_(0-100)','IS_No_of_TWIC_Readers_(0-20)','IS_No_of_Custom_EIS_Report_Configurations_(0-100)','IS_No_of_Network_Switches_(0-100)','IS_No_of_EIS_(EBI)_Servers_(0-10)','IS_No_of_EIS_(EBI)_Workstations_(0-50)','IS_No_of_Dual_Use_Workstations_(0-20)','IS_No_of_Cardholders_(0-10000)','IS_No_of_Badging_Stations_(0-5)','IS_No_of_Interfaces_to_Other_Systems_(0-15)','IS_No_of_Graphics_(0-3000)','IS_No_of_EIS_(EBI)/Photo_ID_Training_Session','IS_No_of_Tema_Training_Session','IS_No_of_Safety_Training_Session','IS_No_of_Muster_Reader_Install_Details_Drawings','Labor_PriceCost_Cont'],
            'displayValueDict' : {"IS_GES_Location":"GES China","IS_Updated_Cutsheets_Required":"No","IS_Site_Acceptance_Test_Required":"No","IS_Informal_Cust_EIS_(EBI)/Photo_ID_Training_Req":"No","IS_Informal_Customer_Tema_Training_Required":"No","IS_Standard_Customer_Training_Required":"No","IS_Wire_List_Required":"Yes","IS_SAT_Documentation_Required":"No"},
            'defaultText' : {
                "IS_No_of_Symbols_Notes_and_Legend_(0-2)" : "2", "IS_No_of_Riser_Diagrams_(0-250)" : "5", "IS_FAT_Duration_in_Days" : "5", "IS_SAT_Duration_in_Days" : "0", "IS_No_of_Tema_Multis_(0-10)" : "0","IS_No_of_Zones_(0-100)":"3","IS_No_of_Door_Details_Drawings_(0-250)":"10","IS_No_of_Turnstile_Details_Drawings_(0-25)":"5","IS_No_of_Door_Wiring_Detail_Drawings":"5","IS_No_of_Turnstile_Wiring_Detail_Drawings":"5","IS_No_of_Gates_(0-100)":"0","IS_No_of_Muster_Readers_(0-100)":"1","IS_No_of_Custom_EIS_Report_Configurations_(0-100)":"5","IS_No_of_Network_Switches_(0-100)":"1","IS_No_of_EIS_(EBI)_Servers_(0-10)":"1","IS_No_of_EIS_(EBI)_Workstations_(0-50)":"1","IS_No_of_Interfaces_to_Other_Systems_(0-15)":"1","IS_No_of_Graphics_(0-3000)":"20","IS_No_of_EIS_(EBI)/Photo_ID_Training_Session":"0","IS_No_of_Tema_Training_Session":"0"
            }
            },
        'Virtualization System Migration' : {
        'hideAttrList' : ['VS_FTT_Level','VS_Distribute_Multi_Clusters','VS_24Port_Rack_Required','VS_48Port_Rack_Required']}
    }
    msidNewContainers = [
            'MSID_Labor_OPM_Engineering',
            'MSID_Labor_ELCN_Con',
            'MSID_Labor_FSC_to_SM_con',
            'MSID_Labor_FSC_to_SM_audit_Con',
            'MSID_Labor_EHPM_C300PM_Con',
            'MSID_Labor_LCN_One_Time_Upgrade_Engineering',
            'MSID_Labor_EBR_Con',
            'MSID_Labor_TPS_TO_EXPERION_Con',
            '3rd_Party_PLC_UOC_Labor',
            'MSID_Labor_LM_to_ELMM_Con',
            'MSID_Labor_TCMI_Con',
            'MSID_Labor_FSCtoSM_IO_con',
            'MSID_Labor_FSC_to_SM_IO_Audit_Con',
            'MSID_Labor_CB-EC_Upgrade_to_C300-UHIO_con',
            'MSID_Labor_C200_Migration_Con',
            'MSID_Labor_Orion_Console_Con',
            'MSID_Labor_xPM_to_C300_Migration_Con',
            'MSID_Labor_Graphics_Migration_con',
            'MSID_Labor_FDM_Upgrade_Con',
            'MSID_Labor_Project_Management',
            'MSID_Additional_Custom_Deliverables'
        ]

    ges_location = {'America' : 'IN', 'AMER': 'IN','APAC': 'CN','EMEA': 'RO'}
    contProductMap = {"OPM": "MSID_OPM_Added_Parts_Common_Container", "LCN One Time Upgrade": "MSID_LCN_Added_Parts_Common_Container", "Non-SESP Exp Upgrade": "MSID_NON_SESP_Added_Parts_Common_Container", "EBR": "MSID_EBR_Added_Parts_Common_Container", "ELCN": "MSID_ELCN_Added_Parts_Common_Container",'Orion Console': 'MSID_Orion_Console_Added_Parts_Common_Container','EHPM/EHPMX/ C300PM': 'MSID_EHPM_C300PM_Added_Parts_Common_Container','TPS to Experion': 'MSID_TPS_EXP_Added_Parts_Common_Container','TCMI': 'MSID_TCMI_Added_Parts_Common_Container','LM to ELMM ControlEdge PLC': 'MSID_LM_TO_ELMM_Added_Parts_Common_Container','Spare Parts': 'MSID_Spare_Parts_Added_Parts_Common_Container','EHPM HART IO': 'MSID_EHPM_HART_IO_Added_Parts_Common_Container','C200 Migration': 'MSID_C200_Migration_Added_Parts_Common_Container','CB-EC Upgrade to C300-UHIO': 'MSID_CB_EC_Added_Parts_Common_Container','xPM to C300 Migration': 'MSID_xPM_C300_Added_Parts_Common_Container','FDM Upgrade 1': 'MSID_FDM_Upgrade_1_Added_Parts_Common_Container','FDM Upgrade 2': 'MSID_FDM_Upgrade_2_Added_Parts_Common_Container','FDM Upgrade 3': 'MSID_FDM_Upgrade_3_Added_Parts_Common_Container','FSC to SM': 'MSID_FSC_to_SM_Added_Parts_Common_Container','FSC_to_SM_audit': 'MSID_FSC_to_SM_audit_Added_Parts_Common_Container','THIRD_PARTY' : 'MSID_Third_Party_Added_Parts_Common_Container','XP10 Actuator Upgrade': 'MSID_XP10_Actuator_Added_Parts_Common_Container','CWS RAE Upgrade': 'MSID_CWS_RAE_Upgrade_Added_Parts_Common_Container','Graphics Migration': 'MSID_Graphics_Added_Parts_Common_Container','FSC to SM IO Migration': 'MSID_FSCtoSM_IO_Added_Parts_Common_Container','CD Actuator I-F Upgrade': 'MSID_CD_Actuator_Added_Parts_Common_Container','Virtualization System': 'MSID_Virtualization_Added_Parts_Common_Container', 'Virtualization System Migration': 'MSID_Virtualization_Added_Parts_Common_Container','QCS RAE Upgrade': 'MSID_QCS_Added_Parts_Common_Container','Generic System 1': 'MSID_GS1_Added_Parts_Common_Container','Generic System 2': 'MSID_GS2_Added_Parts_Common_Container','Generic System 3': 'MSID_GS3_Added_Parts_Common_Container','Generic System 4': 'MSID_GS4_Added_Parts_Common_Container','Generic System 5': 'MSID_GS5_Added_Parts_Common_Container','FSCtoSM_IO_AUDIT': 'MSID_FSCtoSM_IO_audit_Added_Parts_Common_Container','TPA/PMD Migration': 'MSID_TPA_Added_Parts_Common_Container','ELEPIU ControlEdge RTU Migration Engineering': 'MSID_ELEPIU_Added_Parts_Common_Container','Trace Software': 'Trace_Software_Added_Parts_Common_Container'}
    product_containers = {"EBR": "MSID_Labor_EBR_Con", "ELCN": "MSID_Labor_ELCN_Con", "Orion Console": "MSID_Labor_Orion_Console_Con", "EHPM/EHPMX/ C300PM": "MSID_Labor_EHPM_C300PM_Con", "TPS to Experion": "MSID_Labor_TPS_TO_EXPERION_Con", "TCMI": "MSID_Labor_TCMI_Con", "C200 Migration": "MSID_Labor_C200_Migration_Con", "CB-EC Upgrade to C300-UHIO": "MSID_Labor_CB-EC_Upgrade_to_C300-UHIO_con", "FSC to SM": "MSID_Labor_FSC_to_SM_con", "FSC to SM Audit": "MSID_Labor_FSC_to_SM_audit_Con", "xPM to C300 Migration": "MSID_Labor_xPM_to_C300_Migration_Con", "LM to ELMM ControlEdge PLC": "MSID_Labor_LM_to_ELMM_Con", "EHPM HART IO": "MSID_Labor_EHPM_HART_IO_Con", "XP10 Actuator Upgrade": "MSID_Labor_XP10_Actuator_Upgrade_con", "Graphics Migration": "MSID_Labor_Graphics_Migration_con", "CD Actuator I-F Upgrade": "MSID_Labor_CD_Actuator_con", "FSC to SM IO Migration": "MSID_Labor_FSCtoSM_IO_con", "FSC to SM IO Audit": "MSID_Labor_FSC_to_SM_IO_Audit_Con", "3rd Party PLC to ControlEdge PLC/UOC": "3rd_Party_PLC_UOC_Labor","OPM": "MSID_Labor_OPM_Engineering", "LCN One Time Upgrade": "MSID_Labor_LCN_One_Time_Upgrade_Engineering", "CWS RAE Upgrade": "MSID_Labor_CWS_RAE_Upgrade_con", "Virtualization System": "MSID_Labor_Virtualization_con", "Virtualization System Migration": "MSID_Labor_Virtualization_con", "Generic System 1": "MSID_Labor_Generic_System1_Cont", "Generic System 2": "MSID_Labor_Generic_System2_Cont", "Generic System 3": "MSID_Labor_Generic_System3_Cont", "Generic System 4": "MSID_Labor_Generic_System4_Cont", "Generic System 5": "MSID_Labor_Generic_System5_Cont", "QCS RAE Upgrade": "MSID_Labor_QCS_RAE_Upgrade_con", "TPA/PMD Migration": "MSID_Labor_TPA_con", "ELEPIU ControlEdge RTU Migration Engineering": "MSID_Labor_ELEPIU_con","FDM Upgrade":"MSID_Labor_FDM_Upgrade_Con"}
    prdChoicesList = ['Spare_Parts', 'EHPM_HART_IO', 'Integrated_Automation_Assessment_IAA', 'XP10_Actuator_Upgrade', 'CWS_RAE_Upgrade', 'QCS_RAE_Upgrade', 'CD_Actuator_IF_Upgrade', 'TPA/PMD_Migration', 'Generic_System_Migration', 'ELEPIU_ControlEdge_RTU_Migration_Engineering']

    VS_Attr_values = {'Experion': ('Experion Server', 'Experion Server (EMDB only)', 'Experion Server (SCADA)', 'Experion LX Server', 'Experion PlantCruise Server', 'Experion Server (TPS)'),'ACEExperion': ('ACE', 'Experion Station - Console', 'Experion Station - Console (TPS)', 'ACE (TPS)'),'ACE': ('ACE', 'ACE (TPS)', 'EAPP (TPS)')}
    VS_Attr = {'Redundant': 'Experion','Fault_Tolerance': 'ACEExperion','Replicate': 'ACE'}
    VSproducts = {'Virtualization System' : {'essentials_show' : ["VS_Essential_Host_Type","Virtualization_Additional On Site Activities hours","Virtualization_Will_Honeywell_perform_equipment"], 'premium_show' : ["VS_FTT_Level","VS_Distribute_Multi_Clusters","VS_24Port_Rack_Required","VS_48Port_Rack_Required"], 'ownOS_attr' : ["VS_Use_Own_OS_License"]}, 'Virtualization System Migration' : {'essentials_show' : ["VS_Essential_Host_Type","Virtualization_Additional On Site Activities hours","Virtualization_Will_Honeywell_perform_equipment"], 'premium_show' : ["VS_FTT_Level","VS_Distribute_Multi_Clusters","VS_24Port_Rack_Required","VS_48Port_Rack_Required"], 'ownOS_attr' : ["VS_Use_Own_OS_License"]}}


class ExperionCalculationAttributesContainerColumns:
    cn_cont_with_fields = {
        "C300_CG_Universal_IO_cont_1": ["Red_IS", "Non_Red_IS", "Red_NIS", "Non_Red_NIS", "Red_ISLTR", "Non_Red_ISLTR"],
        "C300_CG_Universal_IO_cont_2": ["Red_IS", "Non_Red_IS", "Red_NIS", "Non_Red_NIS", "Red_ISLTR", "Non_Red_ISLTR", "Red_RLY", "Non_Red_RLY", "Red_HV_RLY", "Non_Red_HV_RLY"],
        "SerC_CG_Enhanced_Function_IO_Cont": ["Red_IS", "Non_Red_IS", "Red_NIS", "Non_Red_NIS", "Red_ISLTR", "Non_Red_ISLTR"],
        "SerC_CG_Enhanced_Function_IO_Cont2": ["Red_IS", "Non_Red_IS", "Red_NIS", "Non_Red_NIS", "Red_ISLTR", "Non_Red_ISLTR", "Red_RLY", "Non_Red_RLY", "Red_HV_RLY", "Non_Red_HV_RLY"],
        "SerC_CG_FIM_FF_IO_Cont": ["Red_wo_C300","Non_Red_wo_C300","Red_C300","Non_Red_C300"]
    }
    cn_cont_with_fields_mark = {
        "C300_CG_Universal_IO_Mark_1": ["Red_IS", "Non_Red_IS", "Red_NIS", "Non_Red_NIS", "Red_ISLTR", "Non_Red_ISLTR"],
        "C300_CG_Universal_IO_Mark_2": ["Red_IS", "Non_Red_IS", "Red_NIS", "Non_Red_NIS", "Red_ISLTR", "Non_Red_ISLTR", "Red_RLY", "Non_Red_RLY", "Red_HV_RLY", "Non_Red_HV_RLY"],
        "C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont": ["Red_IS", "Non_Red_IS", "Red_NIS", "Non_Red_NIS", "Red_ISLTR", "Non_Red_ISLTR"],
        "C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont1": ["Red_IS", "Non_Red_IS", "Red_NIS", "Non_Red_NIS", "Red_ISLTR", "Non_Red_ISLTR", "Red_RLY", "Non_Red_RLY", "Red_HV_RLY", "Non_Red_HV_RLY"],
        "SerC_CG_FIM_FF_IO_Cont": ["Red_wo_C300","Non_Red_wo_C300","Red_C300","Non_Red_C300"]
    }
    Fim_cont = {"SerC_CG_FIM_FF_IO_Cont": ["Red_wo_C300","Non_Red_wo_C300","Red_C300","Non_Red_C300"]}
    rm_cont_with_fields = {
        "SerC_RG_Enhanced_Function_IO_Cont": ["Red_IS", "Non_Red_IS", "Red_NIS", "Non_Red_NIS", "Red_ISLTR", "Non_Red_ISLTR"],
        "SerC_RG_Enhanced_Function_IO_Cont2": ["Red_IS", "Non_Red_IS", "Red_NIS", "Non_Red_NIS", "Red_ISLTR", "Non_Red_ISLTR", "Red_RLY", "Non_Red_RLY", "Red_HV_RLY", "Non_Red_HV_RLY"],
        "C300_RG_Universal_IO_cont_1": ["Red_IS", "Non_Red_IS", "Red_NIS", "Non_Red_NIS", "Red_ISLTR", "Non_Red_ISLTR"],
        "C300_RG_Universal_IO_cont_2": ["Red_IS", "Non_Red_IS", "Red_NIS", "Non_Red_NIS", "Red_ISLTR", "Non_Red_ISLTR", "Red_RLY", "Non_Red_RLY", "Red_HV_RLY", "Non_Red_HV_RLY"],
        "C300_UPC_Labor_IO_count_RG_1": ["Red_IS", "Non_Red_IS", "Red_NIS", "Non_Red_NIS"],
        "C300_UPC_Labor_IO_count_RG_2": ["Red_IS", "Non_Red_IS", "Red_NIS", "Non_Red_NIS"]
    }
    rm_cont_with_fields_mark = {
        "C300_CG_Universal_IO_Mark_1": ["Red_IS", "Non_Red_IS", "Red_NIS", "Non_Red_NIS", "Red_ISLTR", "Non_Red_ISLTR"],
        "C300_CG_Universal_IO_Mark_2": ["Red_IS", "Non_Red_IS", "Red_NIS", "Non_Red_NIS", "Red_ISLTR", "Non_Red_ISLTR", "Red_RLY", "Non_Red_RLY", "Red_HV_RLY", "Non_Red_HV_RLY"],
        "C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont": ["Red_IS", "Non_Red_IS", "Red_NIS", "Non_Red_NIS", "Red_ISLTR", "Non_Red_ISLTR"],
        "C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont1": ["Red_IS", "Non_Red_IS", "Red_NIS", "Non_Red_NIS", "Red_ISLTR", "Non_Red_ISLTR", "Red_RLY", "Non_Red_RLY", "Red_HV_RLY", "Non_Red_HV_RLY"]
    }
    con_UOC = [
        "UOC_CG_UIO_Cont",
        "UOC_CG_Other_IO_Cont",
        "UOC_CG_PF_IO_Cont"
    ]
    rem_UOC = [
        "UOC_RG_UIO_Cont",
        "UOC_RG_Other_IO_Cont",
        "UOC_RG_PF_IO_Cont"
    ]
    con_SM = {
        "SM_IO_Count_Digital_Input_Cont":"Total DI Point",
        "SM_IO_Count_Digital_Output_Cont":"Total DO Point",
        "SM_IO_Count_Analog_Input_Cont":"Total AI Point",
        "SM_IO_Count_Analog_Output_Cont":"Total AO Point"
    }
    rem_SM = {
        "SM_RG_IO_Count_Digital_Input_Cont":"Total_DI_Points",
        "SM_RG_IO_Count_Digital_Output_Cont":"Total_DO_Points",
        "SM_RG_IO_Count_Analog_Input_Cont":"Total_AI_Points",
        "SM_RG_IO_Count_Analog_Output_Cont":"Total_AO_Point",
        "SM_RG_IO_Count_Digital_Input_1.3_Cabinet_Cont":["Total_DI_Points","Total_DO_Points"],
        "SM_RG_IO_Count_Analog_Input_1.3_Cabinet_Cont":["Total AI Points","Total AO Points"]
    }
    scada_cont = {
        "Modbus/OPC Interfaces":"SCADA Points",
        "IEC/DNP3 Interfaces":"SCADA Points",
        "Leak Detection System Interfaces":"SCADA Points",
        "Allen-Bradley/Siemens Interfaces":"SCADA Points",
        "Flow Computer Interfaces":"SCADA Points"
    }
    selected_products = [
        "R2Q eServer System", 
        "R2Q Field Device Manager",
        "R2Q Experion Enterprise System",
        "R2Q 3rd Party Devices/Systems Interface (SCADA)"
    ]
    red_attr = [
        "SerC_Number of Redundant EIM for IEC61850",
        "SerC_Number of Redundant EIM for Profinet Devices",
        "SerC_Number of Redunt EIM for EIP Devices (0-300)",
        "SerC_Number_Redundant_EIM_for_Modbus"
    ]
    nonRed_attr = [
        "SerC_Number of Non Redundant EIM for IEC61850",
        "SerC_Number of Non Redund EIM for Profinet Devices",
        "SerC_Number of Non Redundant EIM for EIP Device",
        "SerC_Number_NonRedundant_EIM_for_Modbus"
    ]

class VSTriggerAttrHide:
    VSproducts = {'Virtualization System' : {'essentials_show' : ["VS_Essential_Host_Type","Virtualization_OnSite_Activities_hours","Virtualization_Will_Honeywell_perform_equipment"], 'premium_show' : ["VS_FTT_Level","VS_Distribute_Multi_Clusters","VS_24Port_Rack_Required","VS_48Port_Rack_Required"], 'ownOS_attr' : ["VS_Use_Own_OS_License"]}, 'Virtualization System Migration' : {'essentials_show' : ["VS_Essential_Host_Type","Virtualization_OnSite_Activities_hours","Virtualization_Will_Honeywell_perform_equipment"], 'premium_show' : ["VS_FTT_Level","VS_Distribute_Multi_Clusters","VS_24Port_Rack_Required","VS_48Port_Rack_Required"], 'ownOS_attr' : ["VS_Use_Own_OS_License"]}}