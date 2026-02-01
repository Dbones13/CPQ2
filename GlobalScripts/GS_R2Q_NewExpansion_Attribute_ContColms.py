class R2QNewExpansionControlEdgePLC:
     products = {
        'ControlEdge PLC System' : {
            'hideContainerColumnDict' : {
                'PLC_Software_Question_Cont':['PLC_Media_Delivery','PLC_CE_Builder_Client', 'PLC_Migration_Tool_User_License', 'PLC_Subsea_MDIS_Interface'],
                'PLC_Common_Questions_Cont' :['PLC_Shielded_Terminal_Strip','PLC_IO_Filler_Module'],
                'PLC_Labour_Details' :['PLC_Ges_Location','PLC_Marshalling_Cabinet_Cont','PLC_Enter_Total_Cont'],
                'CE_PLC_System_Hardware' :['PLC_Engineering_Station_Model']
            }
        },
        'R2Q ControlEdge PLC System' : {
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
                'PLC_CG_UIO_Cont':['PLC_AO_100_250', 'PLC_AO_250_499', 'PLC_AO_HART_100_250', 'PLC_AO_HART_250_499', 'PLC_DO_250_500'],
                'PLC_CG_Other_IO_Cont' :['PLC_Analog_Output8_Internal', 'PLC_Analog_Output8_External', 'PLC_Digital_Input16_120240VAC', 'PLC_Digital_Input16_125VDC', 'PLC_Digital_Output8'],
                'PLC_CG_Controller_Rack_Cont' :['PLC_IO_Rack_Type','PLC_Power_Supply','PLC_Power_Input','PLC_Power_Status_Mod_Redudant_Supply','PLC_Field_Wiring_DIDOAOAI_Channel_Mod',
                                                'PLC_Field_Wiring_PIFII_Channel_Mod','PLC_Field_Wiring_Other_Mod','PLC_Remote_Terminal_Cable_Length','PLC_Network_Topology',
                                                'PLC_Ethernet_Switch_Supplier','PLC_Ethernet_Switch_Type','PLC_G3_Option_Ethernet_Switch','PLC_Power_Status_Mod_Redudant_Supply',
                                                'PLC_Ethernet_Switch_Type']
            }
        },
        'CE PLC Remote Group' : {
            'hideContainerColumnDict' : {
                'PLC_RG_UIO_Cont':['PLC_AO_100_250','PLC_AO_250_499', 'PLC_AO_HART_100_250', 'PLC_AO_HART_250_499', 'PLC_DO_250_500'],
                'PLC_RG_Cabinet_Cont':['PLC_Cabinet_Type','PLC_Cabinet_Door_Type', 'PLC_Cabinet_Door_Keylock', 'PLC_Cabinet_Power_Entry', 'PLC_Cabinet_Base_Size', 'PLC_Cabinet_Thermostat', 'PLC_Cabinet_Light'],
                'PLC_RG_Other_IO_Cont' :['PLC_Analog_Output8_Internal', 'PLC_Analog_Output8_External', 'PLC_Digital_Input16_120240VAC', 'PLC_Digital_Input16_125VDC', 'PLC_Digital_Output8']
            }
        },
        'HC900 Group' : {
            'hideAttrList' : ["HC900_Rack_Size_Quantity_Cont","HC900_Additional_IO_Details_of_SIL2","HC900_900_Control_Station_4","HC900_900_Control_Station_7","HC900_900_Control_Station_10","HC900_900_Control_Station_15","HC900_24_VDC_Power_Supply_for_900CR","HC900_Shield_Grounding_Strip_(Package of 2)","HC900_TerminalBoardJumpers_10_2_position_jumpers","HC900_TerminalBoardJumpers_10_10_position_jumpers","HC900 Ethernet Switching Hub","HC900_250_Ohm_Shunt_Resistor_Kit_(8/pkg.)","HC900 24 VDC Power Supply (2.5A)"],
            'hideContainerColumnDict' : {
            "HC900_IO_Details_of_SIL2": ["Barrier_TB", "Model_Number", "Required_Qty","Selected_Qty",
            "Message","IO_Point_Quantity_With_InputVoting","Total_IO_Point_Quantity"],"HC900_IO_Details_of_Non-SIL":["Barrier_TB","RTP_1_Pt_0M","RTP_2_Pt_5M","RTP_5_Pt_0M","Model_Number","Required_Qty","Selected_Qty","Message","Redun_UIO_Multiplier","Channel_Num"]
            }
        },
        'Terminal Manager' : {
            'hideAttrList' : ['Terminal_TM_Test_System_required?', 'Terminal_Media_kit_required', 'Terminal_Experion_Client_PC', 'Terminal_FTE_Switch', 'Terminal_Blank_Experion_Server_(ESV)', 'Terminal_Experion_Server_Hardware', 'Terminal_Additional_Hard_Drive', 'Terminal_Additional_Memory', 'Terminal_Optional_DVD', 'Terminal_Display_Required', 'Terminal_Trackball', 'Terminal_Cabinet_Mounting_Type','Terminal_Ges_Location_Labour', 'Terminal_TM_System_Complexity', 'Terminal_Feature_Type', 'Terminal_Number_of_Days_per_Design_Review', 'Terminal_Number_of_Reviews', 'Terminal_Number_of_Days_for_TM_FAT', 'Terminal_Number_of_Engineer_for_FAT', 'Terminal_Number_of_Days_for_TM_SAT', 'Terminal_Number_of_Engineer_for_SAT', 'Terminal_No_of_Reports_with_Simple_Changes', 'Terminal_No_of_Reports_with_Complex_Changes', 'Terminal_Number_of_New_Simple_Reports', 'Terminal_Number_of_New_Moderate_Reports', 'Terminal_Number_of_New_Complex_Reports', 'Terminal_Number_of_Simple_Screens_for_new_UI', 'Terminal_Number_of_Moderate_Screens_for_new_UI', 'Terminal_Number_of_Complex_Screens_for_new_UI','Terminal_Experion_Server_(ESV)_Type','Calculation_Button'], 
            'displayValueDict' : {
                "Terminal_Web_Portal_required?" : "No", "Terminal_Experion_Client_PC" : "Tower", "Terminal_FTE_Switch" : "EightPortCISCOSwitch", "Terminal_Blank_Experion_Server_(ESV)" : "Desk", "Terminal_Experion_Server_Hardware" : "DELL T550 STD TPM", "Terminal_Additional_Hard_Drive" : "No", "Terminal_Ges_Location_Labour" : "GES China", "Terminal_TM_System_Complexity" : "Moderate", "Terminal_Feature_Type" : "New Features (upto 5)", "Terminal_Additional_Memory" : "None", "Terminal_Optional_DVD" : "No", "Terminal_Display_Required" : "27 Inch", "Terminal_Trackball" : "No", "Terminal_Cabinet_Mounting_Type" : "None","Terminal_Weighbridge_Interface_required?" : "No","Terminal_SAP_ERP_BSI_Interface_required?":"No","Terminal_Card_Reader_Interface_required?":"No"},
            'defaultText' : {"Terminal_Number_of_Days_per_Design_Review" : "3", "Terminal_Number_of_Reviews" : "2", "Terminal_Number_of_Days_for_TM_FAT" : "5", "Terminal_Number_of_Engineer_for_FAT" : "1", "Terminal_Number_of_Days_for_TM_SAT" : "0", "Terminal_Number_of_Engineer_for_SAT" : "0", "Terminal_No_of_Reports_with_Simple_Changes" : "5", "Terminal_No_of_Reports_with_Complex_Changes" : "3", "Terminal_Number_of_New_Simple_Reports" : "2", "Terminal_Number_of_New_Moderate_Reports" : "3", "Terminal_Number_of_New_Complex_Reports" : "2", "Terminal_Number_of_Simple_Screens_for_new_UI" : "5", "Terminal_Number_of_Moderate_Screens_for_new_UI" : "3", "Terminal_Number_of_Complex_Screens_for_new_UI" : "2"
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
         'Fire Detection & Alarm Engineering' : {
            'hideAttrList' : ['FDA Implementation Methodology','FDA Graphics Required','FDA Interface Required','FDA IP scheme Required','FDA Functional Description Required','FDA XLS Software Configuration Document Required','FDA EBI Software Configuration Document Required','FDA Panels Networked','FDA Rudundant EBI Servers','FDA Wire List Required','FDA Number of Reviews (add Asbuilts) (2-5)','FDA Number of Title Page Sheet Index (1-20)','FDA Number of Symbols Notes and Legend (0-2)','FDA Number of Architecture Diagrams (1-10)','FDA Number of Overall Site Plans','FDA Number of Enlarged Site Plans','FDA Number of Building Plans','FDA Number of Room Plans','FDA Number of XLS Panels','FDA Number of SLC Loops','FDA Number of Additional Power Supply Boxes','FDA Number of XLS Interfaces','FDA Number of Standard Detectors','FDA Number of Specialty Detectors','FDA Number of Monitor Module points','FDA Number of 4-20mA monitor module points','FDA Number of Control module points','FDA Number of Isolation modules','FDA Number of pull stations','FDA Number of horns','FDA Number of strobes','FDA Number of combination units','FDA Number of FNAs','FDA Number of UL/nonUL Switches','FDA Number of Fiber to copper converters','FDA Number of EBI Servers','FDA Number of EBI Workstations','FDA Number of EBI interfaces to other systems','FDA Number of Graphics','FDA GES Location'],
            'displayValueDict' : {
                "FDA GES Location":"GES China", "FDA Interface Required" : "Yes", "FDA Functional Description Required" : "Yes", "FDA XLS Software Configuration Document Required" : "Yes", "FDA Panels Networked" : "Yes", "FDA Wire List Required" : "Yes"
            },
            'defaultText' : {
                "FDA Number of XLS Panels" : "1", "FDA Number of XLS Interfaces" : "1", "FDA Number of Control module points" : "10", "FDA Number of FNAs" : "1", "FDA Number of UL/nonUL Switches" : "1", "FDA Number of Fiber to copper converters" : "2", "FDA Number of Graphics" : "10"
            }
            }
     }