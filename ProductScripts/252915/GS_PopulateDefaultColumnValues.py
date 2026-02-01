def getContainer(Name):
    return Product.GetContainerByName(Name)

commonQuestionCon = getContainer("MSID_CommonQuestions")
for row in commonQuestionCon.Rows:
    row.GetColumnByName("MSID_Current_Experion_Release").ReferencingAttribute.SelectDisplayValue('None')
    row.GetColumnByName("MSID_Future_Experion_Release").ReferencingAttribute.SelectDisplayValue('None')
    row.GetColumnByName('MSID_Future_TPN_Release').SetAttributeValue('None')
    row.GetColumnByName('MSID_Current_TPN_Release').SetAttributeValue('None')
    row.GetColumnByName('MSID_FEL_Data_Gathering_Required').SetAttributeValue('None')
    break
commonQuestionCon.Calculate()

opmBasicInfoCon = getContainer('OPM_Basic_Information')
for row in opmBasicInfoCon.Rows:
    row.GetColumnByName('OPM_RESS_Migration_in_scope').SetAttributeValue('No')
    row.GetColumnByName('OPM_Migration_Scenario').SetAttributeValue('Off-Process Migration')
    row.GetColumnByName("OPM_Is_the_Experion_System_LCN_Connected").ReferencingAttribute.SelectDisplayValue("No")
    row.GetColumnByName('OPM_Is_this_is_a_Remote_Migration_Service_RMS').SetAttributeValue('Yes')
    row.GetColumnByName('OPM_Does_the_customer_have_EBR_installed').SetAttributeValue('No')
    row.GetColumnByName('OPM_Is_this_is_migration_part_of_an_ELCN_migration').SetAttributeValue('No')
    row.GetColumnByName('OPM_Servers_and_Stations_HW_replace_needed').SetAttributeValue('No')
    row.GetColumnByName('OPM_If_AMT_Will_Not_Be_Used').SetAttributeValue('No')
    break
opmBasicInfoCon.Calculate()

nodeConfigurationCon = getContainer('OPM_Node_Configuration')
for row in nodeConfigurationCon.Rows:
    row.SetColumnValue("OPM_No_of_Experion_Servers",'0')
    row.SetColumnValue("OPM_No_of_ACET_Servers_LCN_Connected",'0')
    row.SetColumnValue("OPM_No_of_EAPP_Servers_LCN_Connected",'0')
    row.SetColumnValue("OPM_No_of_EST_Rack_mount",'0')
    row.SetColumnValue("OPM_No_of_EST_Tower",'0')
    row.SetColumnValue("OPM_No_of_Other_Servers_to_be_migrated",'0')
    row.SetColumnValue("OPM_Qty_of_ESC_Rack_Mount",'0')
    row.SetColumnValue("OPM_Qty_of_ESC_Tower",'0')
    row.SetColumnValue("OPM_Qty_of_ESF_and_ES-CE_Rack_Mount",'0')
    row.SetColumnValue("OPM_Qty_of_ESF_and_ESCE_Tower",'0')
    row.SetColumnValue("OPM_Qty_of_RPS_and_Thin_Clients",'0')
    row.SetColumnValue("OPM_Qty_of_Series_C_Controllers",'0')
    row.SetColumnValue("OPM_Qty_of_Control_Firewalls_CF9s",'0')
    row.SetColumnValue("OPM_Qty_of_Fieldbus_Interface_Modules",'0')
    row.SetColumnValue("OPM_Qty_of_Profibus_Modules",'0')
    row.SetColumnValue("OPM_Qty_of_Series_C_IO_Modules_excluding_UIO",'0')
    row.SetColumnValue("OPM_Qty_of_UIO_UIO2_Modules",'0')
    break
nodeConfigurationCon.Calculate()


migrationPlatform = getContainer("OPM_Migration_platforms")
for row in migrationPlatform.Rows:
    row.GetColumnByName("OPM_Experion_Server_Hardware_Selection").ReferencingAttribute.SelectDisplayValue("HP DL360 G10")
    row.GetColumnByName('OPM_ACET_EAPP_Server_Hardware_Selection').ReferencingAttribute.SelectDisplayValue('HP DL360 G10')
    row.GetColumnByName('OPM_Other_Servers_Hardware_Selection').ReferencingAttribute.SelectDisplayValue('HP DL360 G10')
    row.GetColumnByName('OPM_EST_Tower_Hardware_Selection').SetAttributeValue('HP Z4 G4')
    row.GetColumnByName('OPM_ESC_ESF_or_ESCE_Tower_Hardware_Selection').SetAttributeValue('HP Z4 G4')
    row.GetColumnByName('OPM_RESS_Server_configuration').SetAttributeValue('Physical')
    row.GetColumnByName('OPM_Select_RESS_platform_configuration').SetAttributeValue('Dell R340XL')
    row.GetColumnByName('OPM_Additional_Memory_for_RESS_Server').SetAttributeValue('No')
    row.GetColumnByName('OPM_Additional_Hard_Disk_For_RESS_Server').SetAttributeValue('No')
    row.SetColumnValue("OPM_No_of_RESS_Remote_Users",'0')
    row.GetColumnByName('OPM_Type_of_RPS_and_Thin_Client_for_EST').SetAttributeValue('None')
    row.GetColumnByName('OPM_Type_of_RPS_and_Thin_Client_for_ESC_ESF_ESCE').SetAttributeValue('None')
    break
migrationPlatform.Calculate()


FTESwitcgesMigration = getContainer("OPM_FTE_Switches_migration_info")
for row in FTESwitcgesMigration.Rows:
    row.GetColumnByName('OPM_Is_L1_L2_Switch_HW_refresh_required').SetAttributeValue('None')
    row.SetColumnValue("OPM_Quantity_of_L1_L2_Switches",'0')
    row.GetColumnByName('OPM_Is_Backbone_or_Agg_Switch_HW_refresh_required').SetAttributeValue('None')
    row.SetColumnValue("OPM_Qty_of_Backbone_or_Agg_Fiber_Optic_Switch",'0')
    break
FTESwitcgesMigration.Calculate()

serviceCon = getContainer("OPM_Services")
for row in serviceCon.Rows:
    row.GetColumnByName('OPM_Acceptance_Test_Required').SetAttributeValue('SAT')
    row.GetColumnByName('OPM_is_system_required_Domain_controller_upgrade').SetAttributeValue('No')
    row.SetColumnValue("OPM_Additional_hrs_for_Document_Customization",'0')
    break
serviceCon.Calculate()

LCNDesignInputsCon = getContainer("LCN_Design_Inputs_for_TPN_OTU_Upgrade")
for row in LCNDesignInputsCon.Rows:
    row.SetColumnValue("LCN_No_of_TPN_nodes",'0')
    row.SetColumnValue("LCN_No_of_TPN_Controllers",'0')
    row.GetColumnByName('LCN_Is_there_redundant_History_Module').SetAttributeValue('No')
    row.GetColumnByName('LCN_Do_you_want_HG_Point_Bar_Trend_Display').SetAttributeValue('No')
    break
LCNDesignInputsCon.Calculate()

nonSESPDesignInputsExpCon = getContainer("NONSESP_Design_Inputs_for_Experion_Upgrade_License")
for row in nonSESPDesignInputsExpCon.Rows:
    row.GetColumnByName('NONSESP_Sever_Redundancy').SetAttributeValue('No')
    row.GetColumnByName('NONSESP_Should_RSLinx_be_added').SetAttributeValue('No')
    row.SetColumnValue("NONSESP_No_of_process_points",'0')
    row.SetColumnValue("NONSESP_No_of_SCADA_points",'0')
    row.SetColumnValue("NONSESP_No_of_Flex_Console_Ext_Stations_ESF_ESCE",'0')
    row.SetColumnValue("NONSESP_No_of_Console_Stations_ESC_and_EST",'0')
    row.SetColumnValue("NONSESP_No_of_TPS_Connections_LCNP_Cards",'0')
    row.SetColumnValue("NONSESP_No_of_3rdParty_MS_SQL_Client_License",'0')
    row.SetColumnValue("NONSESP_No_of_3rd_Party_MS_Visual_Studio_License",'0')
    row.SetColumnValue("NONSESP_No_of_CAB_Developer_Licenses",'0')
    row.SetColumnValue("NONSESP_No_of_RESS_Remote_Users",'0')
    break
nonSESPDesignInputsExpCon.Calculate()

nonSESPDesignInputsEServerCon = getContainer("NONSESP_Design_Inputs_for_eServer_Upgrade_License")
for row in nonSESPDesignInputsEServerCon.Rows:
    row.SetColumnValue("NONSESP_No_of_Premium_Access_Connections",'0')
    break
nonSESPDesignInputsEServerCon.Calculate()

ebrHardwareToHostCon = getContainer('EBR_Hardware_to_Host_EBR_Physical_Node_Only')
for row in ebrHardwareToHostCon.Rows:
    row.GetColumnByName('EBR_Additional_Network_Storage_Device_NAS_required').SetAttributeValue('No')
    row.GetColumnByName('EBR_Additional_Hard_Drive_required').SetAttributeValue('No')
    break
ebrHardwareToHostCon.Calculate()

ebrNewAdditionalCon = getContainer('EBR_New_Additional_EBR')
for row in ebrNewAdditionalCon.Rows:
    row.SetColumnValue("EBR_Qty_of_EBR_New_Additional_for_Virtual_Node",'0')
    row.SetColumnValue("EBR_Qty_of_EBR_New_Additional_for_Workstation",'0')
    row.SetColumnValue("EBR_Qty_of_EBR_New_Additional_for_Server",'0')
    break
ebrNewAdditionalCon.Calculate()

ebrUpgradeCon = getContainer('EBR_Upgrade')
for row in ebrUpgradeCon.Rows:
    row.SetColumnValue("EBR_Qty_of_EBR_Upgrade_for_Virtual_Node",'0')
    row.SetColumnValue("EBR_Qty_of_EBR_Upgrade_for_Workstation",'0')
    row.SetColumnValue("EBR_Qty_of_EBR_Upgrade_for_Server",'0')
    break
ebrUpgradeCon.Calculate()

ebrBasicInfoCon = getContainer('EBR_Basic_Information')
for row in ebrBasicInfoCon.Rows:
    row.GetColumnByName('EBR_Media_kit_type').SetAttributeValue('Electronic delivery')
    row.GetColumnByName('EBR_Future_EBR_Release').SetAttributeValue('R520')
    row.GetColumnByName('EBR_Current_EBR_Release_only_for_EBR_Upgrade').SetAttributeValue('R410 (Acronis)')
    break
ebrBasicInfoCon.Calculate()

ebrServicesCon = getContainer('EBR_Services')
for row in ebrServicesCon.Rows:
    row.GetColumnByName('EBR_Site_Acceptance_Test_required').SetAttributeValue('No')
    break
ebrServicesCon.Calculate()

ELCNBasicInformation = getContainer('ELCN_Basic_Information')
setAttributes = {"ELCN_If_ELCN_Bridge_is_not_present_in_LCN": "Nothing - ELCN Bridge is present", "ELCN_Type_of_Cabinet_where_the_ELCN_Bridge": "None", "ELCN_Type_of_Cabinet_to_Install_the_Physical_nodes": "LCN Cabinet", "ELCN_Additional_Switches_needed": "EightPortCISCOSwitch", "ELCN_Qty_of_Additional_Switches": "0"}
row = ELCNBasicInformation.Rows[0]
for key in setAttributes:
    if key == "ELCN_Qty_of_Additional_Switches":
        row.SetColumnValue(key,'0')
    else:
        row.GetColumnByName(key).SetAttributeValue(setAttributes[key])
ELCNBasicInformation.Calculate()

ELCNUpgradeNewELCNNodes = getContainer('ELCN_Upgrade_New_ELCN_Nodes')
setAttributes =["ELCN_Qty_of_Non_Redundant_ESVTs", "ELCN_Qty_of_Redundant_ESVTs", "ELCN_Qty_of_ESTs ELCN_Qty_of_ACE_Ts", "ELCN_Qty_of_EAPPs ELCN_Qty_of_HMs", "ELCN_Qty_of_Non_redundant_AMs", "ELCN_Qty_of_Redundant_AMs", "ELCN_Qty_of_Non_Redundant_HGs", "ELCN_Qty_of_Redundant_HGs", "ELCN_Qty_of_Non_Redundant_EHBs", "ELCN_Qty_of_Redundant_EHBs", "ELCN_Qty_of_Non_Redundant_ETN_EHBs", "ELCN_Qty_of_Redundant_ETN_EHBs", "ELCN_Qty_of_Non_Redundant_NIMs", "ELCN_Qty_of_Redundant_NIMs", "ELCN_Qty_of_Non_Redundant_ENIMs", "ELCN_Qty_of_Redundant_ENIMs", "ELCN_Qty_of_Non_Redundant_ETN_ENIMs", "ELCN_Qty_of_Redundant_ETN_ENIMs", "ELCN_Qty_of_Non_Redundant_xPLCGs", "ELCN_Qty_of_Redundant_xPLCGs", "ELCN_Qty_of_Network_Gateways"]
row = ELCNUpgradeNewELCNNodes.Rows[0]
for key in setAttributes:
    row.SetColumnValue(key,'0')

row = ELCNUpgradeNewELCNNodes.Rows[1]
for key in setAttributes:
    if key not in ["ELCN_Qty_of_Non_Redundant_xPLCGs", "ELCN_Qty_of_Redundant_xPLCGs"]:
        row.SetColumnValue(key,'0')

row = ELCNUpgradeNewELCNNodes.Rows[3]
for key in setAttributes:
    if key in ["ELCN_Qty_of_HMs", "ELCN_Qty_of_Non_redundant_AMs", "ELCN_Qty_of_Redundant_AMs","ELCN_Qty_of_Non_Redundant_EHBs", "ELCN_Qty_of_Redundant_EHBs", "ELCN_Qty_of_Non_Redundant_ENIMs", "ELCN_Qty_of_Redundant_ENIMs", "ELCN_Qty_of_Network_Gateways"]:
        row.SetColumnValue(key,'0')

row = ELCNUpgradeNewELCNNodes.Rows[4]
for key in setAttributes:
    if key in ["ELCN_Qty_of_HMs", "ELCN_Qty_of_Non_redundant_AMs", "ELCN_Qty_of_Redundant_AMs","ELCN_Qty_of_Non_Redundant_EHBs", "ELCN_Qty_of_Redundant_EHBs", "ELCN_Qty_of_Non_Redundant_ENIMs", "ELCN_Qty_of_Redundant_ENIMs", "ELCN_Qty_of_Network_Gateways"]:
        row.SetColumnValue(key,'0')
ELCNUpgradeNewELCNNodes.Calculate()

ELCNNetworkGatewayUpgrade = getContainer('ELCN_Network_Gateway_Upgrade')
setAttributes = {"ELCN_Select_Switch_configuration_required": "None required from Honeywell", "ELCN_Qty_of_NGs_more_than_100mts_from_existing_fiber_concentrators": "0", "ELCN_Select_type_of_fiber_optic_switch": "Moxa (SM-G512I2)"}
row = ELCNNetworkGatewayUpgrade.Rows[0]
for key in setAttributes:
    if key == 'ELCN_Select_Switch_configuration_required':
        row.GetColumnByName(key).ReferencingAttribute.SelectDisplayValue(setAttributes[key])
    elif key == "ELCN_Qty_of_NGs_more_than_100mts_from_existing_fiber_concentrators":
        row.SetColumnValue(key,'0')
    else:
        row.GetColumnByName(key).SetAttributeValue(setAttributes[key])
ELCNNetworkGatewayUpgrade.Calculate()

ELCNServices  = getContainer('ELCN_Services')
setAttributes = {"ELCN_Off_Process_Setup_Validation_Required": "No", "ELCN_Will_OPM_or_TPS_to_Experion_be_performed":"No", "ELCN_Additional_hours_for_FTE_setup":"0", "ELCN_Services_for_NG_Switch_Configuration": "No"}
row = ELCNServices.Rows[0]
for key in setAttributes:
    if key == "ELCN_Additional_hours_for_FTE_setup":
        row.SetColumnValue(key,'0')
    else:
        row.GetColumnByName(key).SetAttributeValue(setAttributes[key])
ELCNServices.Calculate()

ELCNServerCabinetConfiguration = getContainer('ELCN_Server_Cabinet_Configuration')
setAttributes = {"ELCN_Cabinet_Depth_Size": "800 cm", "ELCN_Power_Supply_Voltage": "120V, 60 Hz", "ELCN_Cabinet_Door_Type": "Standard", "ELCN_Cabinet_Keylock_Type": "Standard", "ELCN_Cabinet_Hinge_Type": "130 Degrees", "ELCN_Cabinet_Thermostat_Required": "No", "ELCN_Cabinet_Base_Required": "No", "ELCN_Cabinet_Color": "Gray-RAL7035"}
row = ELCNServerCabinetConfiguration.Rows[0]
for key in setAttributes:
    row.GetColumnByName(key).SetAttributeValue(setAttributes[key])
ELCNServerCabinetConfiguration.Calculate()

xPMNetworkUpgradeCont = getContainer('xPM_Network_Upgrade_Cont')
setAttributes = {"xPM_Customer_requires_Fiber_Communication": "No - Quote 9200L 24ports Switch Pair 2ea SI-920LN4","xPM_Distance_of_Fiber_Optic_Extenders":"2 km"}
row = xPMNetworkUpgradeCont.Rows[0]
for key in setAttributes:
    row.GetColumnByName(key).SetAttributeValue(setAttributes[key])
xPMNetworkUpgradeCont.Calculate()

xpmServiceCon = getContainer('xPM_Services_Cont')
row = xpmServiceCon.Rows[0]
row.GetColumnByName("xPM_Factory_Acceptance_Test_Required").SetAttributeValue("No")
xpmServiceCon.Calculate()


orionStationConfiguration = getContainer('Orion_Station_Configuration')
setAttributes = ['Orion_Number_of_console_bases_with_same_configuration','Orion_Number_of_2_Position_Base_Unit','Orion_Number_of_3_Position_Base_Unit','Orion_Number_of_Left_Auxiliary_Equipment_Unit','Orion_Number_of_Right_Auxiliary_Equipment_Unit','Orion_Number_of_Right_Extended_Auxiliary_Equipment_Unit','Orion_Number_of_Center_Straight_Auxiliary_Equipment_Unit','Orion_Number_of_Center_Curved_Auxiliary_Equipment_Unit','Orion_Number_of_Center_Curved_Extended_Auxiliary_Equipment_Unit','Orion_Number_of_Center_Joining_Unit','Orion_Number_of_Jack_Lift_&_Ramps_System_needed','Orion_Number_of_Additional_23_monitors','Orion_Number_of_Additional_Monitor_Mounting_Arm_for_23','Orion_Number_of_Left_Extended_Auxiliary_Equipment_Unit']

for column in setAttributes:
    for row in orionStationConfiguration.Rows:
        row.SetColumnValue(column,'0')
for row in orionStationConfiguration.Rows:
    row.GetColumnByName('Orion_Auxiliary_Equipment_Unit_AEU_Turret_Type').SetAttributeValue('None')
    row.GetColumnByName('Orion_Monitor_Type').SetAttributeValue('55-inch')
    row.GetColumnByName('Orion_Membrane_Keyboard_Type').SetAttributeValue('None')
    row.GetColumnByName('Orion_Advanced_Solution_Pack_license_required').SetAttributeValue('No')
    row.GetColumnByName('Orion_Turret_Position_for_the_Left_Ext_Aux_Equip_Unit').SetAttributeValue('Wide')
    row.GetColumnByName('Orion_Turret_Position_for_the_Right_Ext_Aux_Equip_Unit').SetAttributeValue('Wide')
    row.GetColumnByName('Orion_Turret_Position_for_the_Center_Curved_Ext_Aux_Equip_Unit').SetAttributeValue('Wide')
    row.GetColumnByName('Orion_Remote_Peripheral_Solution_RPS_Type').SetAttributeValue('None')
    row.GetColumnByName('Orion_Extended_Heigh_Alarm_Ligth_Panel').SetAttributeValue('No')
    row.GetColumnByName('Orion_Console_Alarm_Light_Custom_Logo').SetAttributeValue('No')
    row.GetColumnByName('Orion_Alarm_Sounds').SetAttributeValue('No')
    row.SetColumnValue('Orion_Display_Devices_per_position','1')
orionStationConfiguration.Calculate()

orionGeneralInformation1 = getContainer('Orion_General_Information_Container2')
for row in orionGeneralInformation1.Rows:
    row.SetColumnValue('Orion_Number_of_Orion_Console_configurations_needed','0')
orionGeneralInformation1.Calculate()

orionService = getContainer('Orion_Services')
for row in orionService.Rows:
    row.GetColumnByName('Orion_How_is_this_Orion_Console_Installation_performed').SetAttributeValue('Part of a Migration')
    row.GetColumnByName('Orion_Is_Graphics_Scaling_needed').SetAttributeValue('No')
    row.SetColumnValue('Orion_Number_of_existing_stations_that_will_be_migrated_to_Orion_Console','0')
    row.SetColumnValue('Orion_Number_of_new_Orion_stations_that_will_be_installed','0')
    row.SetColumnValue('Orion_Number_of_existing_HMI_Graphics','0')
    row.SetColumnValue('Orion_Honeywell_hours_for_Orion_Console_unboxing_and_installation_in_Control_Room','0')
    row.GetColumnByName('MSID_Will_Honeywell_perform_equipment_installation').SetAttributeValue('Yes') 
orionService.Calculate()

con = getContainer("TPS_EX_General_Questions")
defaultDict = {
    "IS_Migration_Part_Of_ELCN_Migration": "Yes",
    "Setup_FTE_Network_Infrastructure": "No a FTE Network exists",
    "FTE_Switch_Type": "TwentyFourSTPPortCISCOSwitch",
    "Additional_Switches_Type": "TwentyFourSTPPortCISCOSwitch",
    "Additional_Server_ESV_Stations_ESF_ESC_ESF_Required": "No"
}
for row in con.Rows:
    for col in row.Columns:
        defaultVal = defaultDict.get(col.Name)
        if defaultVal:
            col.SetAttributeValue(defaultVal)

con = getContainer("TPS_EX_Conversion_ESVT_Server")
defaultDict = {
    "TPS_EX_ESVT_Redundant": "No",
    "TPS_EX_ESVT_Server_Hardware": "HP DL360 G10",
    "TPS_EX_Additional_Hard_Drives": "No"
}
for row in con.Rows:
    for col in row.Columns:
        defaultVal = defaultDict.get(col.Name)
        if defaultVal:
            col.SetAttributeValue(defaultVal)

con = getContainer("TPS_EX_Bundle_Conversion_Server_Stations")
defaultDict = {
    "TPS_EX_Non_Reduntant_Conversion_ESVT": "No",
    "TPS_EX_Redundant_Conversion_ESVT": "No",
    "TPS_EX_Bundle_Conversion_Existing_Node": "AM",
    "TPS_EX_Bundle_Conversion_ESVT_Server_Hardware": "HP DL360 G10",
    "TPS_EX_Bundle_Conversion_EST_Station_Hardware": "HP Z4 G4",
    "TPS_EX_Bundle_Conversion_EST_Station_Mounting_Furn": "Desktop"
}
for row in con.Rows:
    for col in row.Columns:
        defaultVal = defaultDict.get(col.Name)
        if defaultVal:
            col.SetAttributeValue(defaultVal)

con = getContainer("TPS_EX_Server_Cabinet_Config")
defaultDict = {
    "TPS_EX_Cabinet_Depth_Size": "800 mm",
    "TPS_EX_Power_Supply_Voltage": "120V, 60 Hz",
    "TPS_EX_Cabinet_Door_Type": "Standard",
    "TPS_EX_Cabinet_Keylock_Type": "Standard",
    "TPS_EX_Cabinet_Hinge_Type": "130 Degrees",
    "TPS_EX_Cabinet_Thermostat_Required": "No",
    "TPS_EX_Cabinet_Base_Required":"No",
    "TPS_EX_Cabinet_Color":"Gray-RAL7035"
}
for row in con.Rows:
    for col in row.Columns:
        defaultVal = defaultDict.get(col.Name)
        if defaultVal:
            col.SetAttributeValue(defaultVal)

con = getContainer("TPS_EX_Service")
defaultDict = {
    #"TPS_EX_Service_Switch_Config_Honeywell_Scope": "No",
    #"TPS_EX_Service_Acceptance_Test_Required": "SAT",
    "TPS_EX_Will_System_be_migrated_virtual_system": "No",
    "TPS_Will_Honeywell_perform_equipment_installation":"Yes"
    #"MSID_Will_Honeywell_perform_equipment_installation": "Yes"
}
for row in con.Rows:
    for col in row.Columns:
        defaultVal = defaultDict.get(col.Name)
        if defaultVal:
            col.SetAttributeValue(defaultVal)

con = Product.GetContainerByName("TPS_EX_Additional_Servers")
defaultDict = {
    "TPS_EX_Additional_Server_Hardware": "HP DL360 G10",
    "TPS_EX_Addtional_Server_Additional_Hard_Drive": "No",
    "TPS_EX_Additional_Server_Additional_Memory": "None",
    "TPS_EX_Additional_Server_Optional_DVD": "No",
    "TPS_EX_Additional_Server_Display": "None",
    "TPS_EX_Additional_Server_Trackball": "No",
    "TPS_EX_Additional_Server_Cabinet_Mounting_Type": "None"
}
attr_replace = {
                "TPS_EX_Additional_Server_Hardware": "TPS_EX_Additional_Server_Hardware",
                "TPS_EX_Addtional_Server_Additional_Hard_Drive": "TPS_EX_Additional_Hard_Drives",
                "TPS_EX_Additional_Server_Additional_Memory": "TPS_EX_Additional_Server_Additional_Memory",
                "TPS_EX_Additional_Server_Optional_DVD": "TPS_EX_Additional_Server_Optional_DVD",
                "TPS_EX_Additional_Server_Display": "TPS_EX_Additional_Server_Display",
                "TPS_EX_Additional_Server_Trackball": "TPS_EX_Trackball",
                "TPS_EX_Additional_Server_Cabinet_Mounting_Type" : "TPS_EX_Cabinet_Mounting_Type"
                }
for row in con.Rows:
    for col in row.Columns:
        defaultVal = defaultDict.get(col.Name)
        if defaultVal:
            row[col.Name] = defaultVal
            col.SetAttributeValue(defaultVal)
            row.Product.Attr(attr_replace[col.Name]).SelectDisplayValue(defaultVal)
            row.Product.Attr(attr_replace[col.Name]).SelectValue(defaultVal)
            row.Product.ApplyRules()
            row.ApplyProductChanges()
            row.Calculate()
    con.Calculate()
con.Calculate()

con = getContainer("TPS_EX_Additional_Stations")
defaultDict = {
    "TPS_EX_Additional_Stations_Desk_Hardware": "Dell T5820XL",
    "TPS_EX_Additional_Stations_Cabinat_Hardware": "Dell T5820XL",
    "TPS_EX_Additional_Stations_RPS_Type": "None",
    "TPS_EX_Additional_Stations_RPS_Quad_Video_Required": "No",
    "TPS_EX_Additional_Stations_RPS_Mounting_Furniture": "Desk",
    "TPS_EX_Additional_Stations_Multi_Window_Support": "No",
    "TPS_EX_Additional_Stations_Display_Size": "Wide",
    "TPS_EX_Additional_Stations_Touch_Screen": "No",
    "TPS_EX_Additional_Stations_Trackball": "No",
    "TPS_EX_Additional_Stations_IKB_OEP": "None",
    "TPS_EX_Additional_Stations_Interface_card": "FTE",
    "TPS_EX_Additional_Stations_Cabinet_Mounting_Type": "None",
    "TPS_EX_Additional_Stations_Station_License?" : "No"
}

for row in con.Rows:
    for col in row.Columns:
        defaultVal = defaultDict.get(col.Name)
        if defaultVal:
            try:
                row[col.Name] = defaultVal
                col.SetAttributeValue(defaultVal)
                row.Product.Attr(attr_replace[col.Name]).SelectDisplayValue(defaultVal)
                row.Product.Attr(attr_replace[col.Name]).SelectValue(defaultVal)
                row.ApplyProductChanges()
                row.Calculate()
            except:
                pass
con.Calculate()

con = getContainer("TPS_EX_Station_Conversion_EST")
defaultDict = {
    "TPS_EX_Hardware": "HP Z4 G4",
    "TPS_EX_Future_Mounting_Furniture": "Desktop",
    "TPS_EX_Computer_Adapter_Kit": "No",
    "TPS_EX_RPS_Type": "None",
    "TPS_EX_Existing_Monitor_Type": "Quad",
    "TPS_EX_Keyboard_Type": "None",
    "TPS_EX_Quad_Display": "Yes"
}
for row in con.Rows:
    for col in row.Columns:
        defaultVal = defaultDict.get(col.Name)
        if defaultVal:
            col.SetAttributeValue(defaultVal)
            
con = getContainer("TPS_EX_Conversion_ACET_EAPP")
defaultDict = {
    "TPS_EX_Conversion_ACET_EAPP_Server_Hardware" : "HP DL360 G10"
}
for row in con.Rows:
    for col in row.Columns:
        defaultVal = defaultDict.get(col.Name)
        if defaultVal:
            col.SetAttributeValue(defaultVal)

tcmiGeneralInfo = getContainer('TCMI_General_Information')
for row in tcmiGeneralInfo.Rows:
    row.GetColumnByName('TCMI_Is_the_current_TPN_release_at_R687_or_greater').SetAttributeValue('Yes')
    row.GetColumnByName('TCMI_Is_the_current_Experion_Release_at_R432.2').SetAttributeValue('Yes')
    row.GetColumnByName('TCMI_Is_the_current_Triconex_Controller_HW_&_SW').SetAttributeValue('Yes')
tcmiGeneralInfo.Calculate()

tcmiServices = getContainer('TCMI_Services')
for row in tcmiServices.Rows:
    row.GetColumnByName('TCMI_Is_Triconex_SMM_being_migrated_with_xPM_in').SetAttributeValue('No')
tcmiServices.Calculate()

spareParts = getContainer('Spare_Parts')
for row in spareParts.Rows:
    row.SetColumnValue('Spare_Parts_Quantity','0')
spareParts.Calculate()

c200GeneralQns1 = getContainer('C200_Migration_General_Qns_Cont') # for dropdown values
for row in c200GeneralQns1.Rows:
    row.GetColumnByName('C200_Connection _to_Experion_Server').SetAttributeValue('FTE')
    row.GetColumnByName('C200_FTE_Switch_to_connect_required_exp_servers').SetAttributeValue('None')
    row.GetColumnByName('C200_Is_Honeywell_Providing_FTE_cables').SetAttributeValue('Yes')
    row.GetColumnByName('C200_Average_Cable_Length').SetAttributeValue('10m')
    row.GetColumnByName('C200_Type_of_UOC').SetAttributeValue('UOC')
    row.GetColumnByName('C200_Type_of_downlink_communication_UOC').SetAttributeValue('E/IP')
c200GeneralQns1.Calculate()

c200GeneralQns2 = getContainer('C200_Migration_General_Qns_Cont') # for input values
for row in c200GeneralQns2.Rows:
    row.SetColumnValue('C200_How_many_C200s_are_we_migrating','0')
    row.SetColumnValue('C200_How_many_co_located_C200_groups_exists','0')
    row.SetColumnValue('C200_Number_of_additional_switches','0')
c200GeneralQns2.Calculate()

c200ServicesCont1 = getContainer('C200_Services_1_Cont')
for row in c200ServicesCont1.Rows:
    row.GetColumnByName('C200_Data_Gathering_Required').SetAttributeValue('No')
    row.GetColumnByName('C200_Documentation_Required').ReferencingAttribute.SelectDisplayValue('No')
    row.SetColumnValue('C200_additional_hours_for_UOC_installation','0')
c200ServicesCont1.Calculate()

c200ServicesCont2 = getContainer('C200_Services_2_Cont')
for row in c200ServicesCont2.Rows:
    row.GetColumnByName('C200_Factory_Acceptance_Test_Required').SetAttributeValue('No')
    row.GetColumnByName('C200_Will_Honeywell_Perform_Equipment_Installation_Activities').SetAttributeValue('No')
c200ServicesCont2.Calculate()

c200C300Cabinet = getContainer('C200_C300_Series_C_Cabinet_Config_Cont')
for row in c200C300Cabinet.Rows:
    #row.GetColumnByName('C200_C300_Cabinet_Type').ReferencingAttribute.SelectDisplayValue('Front Access Only')
    row.GetColumnByName('C200_C300_Cabinet_Doors').ReferencingAttribute.SelectDisplayValue('Standard')
    row.GetColumnByName('C200_C300_Cabinet_Hinge_Type').SetAttributeValue('130 Degrees')
    row.GetColumnByName('C200_C300_Cabinet_Light_Required').SetAttributeValue('No')
    row.GetColumnByName('C200_C300_Cabinet_Thermostat_Required').SetAttributeValue('No')
    #row.GetColumnByName('C200_C300_Integrated_Marshalling_Cabinet_Layout').SetAttributeValue('Front to Back')
    row.GetColumnByName('C200_C300_Cabinet_Keylock_Type').SetAttributeValue('Standard')
    row.GetColumnByName('C200_C300_Power_Entry').SetAttributeValue('None')
    row.GetColumnByName('C200_C300_TDI_Power_Supply_Cable_Length').SetAttributeValue('48 in')
    row.GetColumnByName('C200_C300_Cabinet_Color').SetAttributeValue('Gray-RAL7035')
c200C300Cabinet.Calculate()

c200C300CabinetFAO = getContainer('C200_C300_Series_C_Cabinet_Config_Cont_FAOnly')
for row in c200C300CabinetFAO.Rows:
    #row.GetColumnByName('C200_C300_Cabinet_Type').ReferencingAttribute.SelectDisplayValue('Front Access Only')
    row.GetColumnByName('C200_C300_Cabinet_Doors_FAOnly').ReferencingAttribute.SelectDisplayValue('Standard')
    row.GetColumnByName('C200_C300_Cabinet_Hinge_Type_FAOnly').SetAttributeValue('130 Degrees')
    row.GetColumnByName('C200_C300_Cabinet_Light_Required_FAOnly').SetAttributeValue('No')
    row.GetColumnByName('C200_C300_Cabinet_Thermostat_Required_FAOnly').SetAttributeValue('No')
    #row.GetColumnByName('C200_C300_Integrated_Marshalling_Cabinet_Layout').SetAttributeValue('Front to Back')
    row.GetColumnByName('C200_C300_Cabinet_Keylock_Type_FAOnly').SetAttributeValue('Standard')
    row.GetColumnByName('C200_C300_Power_Entry_FAOnly').SetAttributeValue('None')
    row.GetColumnByName('C200_C300_TDI_Power_Supply_Cable_Length_FAOnly').SetAttributeValue('48 in')
    row.GetColumnByName('C200_C300_Cabinet_Color_FAOnly').SetAttributeValue('Gray-RAL7035')
c200C300CabinetFAO.Calculate()

EHPMHARTIOGeneralQns1= getContainer('EHPM_HART_IO_General_Qns_Cont')	# for dropdown values
for row in EHPMHARTIOGeneralQns1.Rows:
    row.GetColumnByName('Current_Experion_Release').SetAttributeValue('Less than R511.4')
    row.GetColumnByName('Current_TPN_Release').SetAttributeValue('Less than R688.5')
    row.GetColumnByName('Current_FDM_Release').SetAttributeValue('None')
EHPMHARTIOGeneralQns1.Calculate()

EHPMHARTIOGeneralQns2 = getContainer('EHPM_HART_IO_General_Qns_Cont') # for input values
for row in EHPMHARTIOGeneralQns2.Rows:
    row.SetColumnValue('Number_of_EHPM_integration_licenses_needed','0')
EHPMHARTIOGeneralQns2.Calculate()

EHPMHARTIOConfiguration= getContainer('EHPM_HART_IO_Configuration_Cont')	# for input values
for row in EHPMHARTIOConfiguration.Rows:
    row.SetColumnValue('Number_of_Non_Redundant_HART_HLAI','0')
    row.SetColumnValue('Number_of_Redundant_Hart_HLAI','0')
    row.SetColumnValue('Number_of_Non-Red_IOP&Red_FTA_HART_HLAI','0')
    row.SetColumnValue('Number_of_Non-Redundant_HART_AO_8points','0')
    row.SetColumnValue('Number_of_Non-Redundan_ HART_AO_16points','0')
    row.SetColumnValue('Number_of_Redundant_HART_AO_16points','0')
EHPMHARTIOConfiguration.Calculate()

EHPMHARTIOServices = getContainer('EHPM_HART_IO_Services_Cont')	# for dropdown values
for row in EHPMHARTIOServices.Rows:
    row.SetColumnValue('Number_of_Experion_Systems (0-10)','0')
    row.SetColumnValue('Number_of_EHPM_where_HART_IO_will_be_installed','0')
    row.GetColumnByName('Wiring_termination_type').SetAttributeValue('Compression')
    row.GetColumnByName('Commissioning_required').SetAttributeValue('No')
EHPMHARTIOServices.Calculate()

CBECUpgradetoC300UHIOBasicConfiguration= getContainer('CB_EC_migration_to_C300_UHIO_Configuration_Cont')	# for dropdown values for CB_EC_Upgrade_C300-UHIO for basic controoler cont
for row in CBECUpgradetoC300UHIOBasicConfiguration.Rows:
    row.GetColumnByName('CB_EC_Do_you_want_IO_redundancy').SetAttributeValue('No')
    row.GetColumnByName('CB_EC_Do_you_want_new_TCB_cables_or_just_the_Adapter_cables').SetAttributeValue('Yes - New TCB cables 10m')
    row.GetColumnByName('CB_EC_Do_you_want_Series_C_RAM_Battery_Backup').SetAttributeValue('No')
    row.GetColumnByName('CB_EC_Do_you_want_FTE_cables_to_run_between_the_C300_C9_Firewall_and_FTE_Switches').SetAttributeValue('No')
    row.SetColumnValue('CB_EC_If_terminal_blocks_are_required_for_spare_UIO_points','0')
    row.SetColumnValue('CB_EC_How_many_CBs_are_being_migrated','0')
    row.SetColumnValue('CB_EC_How_many_ECs_are_being_migrated','0')
CBECUpgradetoC300UHIOBasicConfiguration.Calculate()

CBECUpgradetoC300UHIOservices1= getContainer('CB_EC_Services_1_Cont')	# for dropdown values for CB_EC_Upgrade_C300-UHIO for Services 1 Cont
for row in CBECUpgradetoC300UHIOservices1.Rows:
    row.GetColumnByName('CB_EC_Is_CB_EC_interfacing_with_DHEB_on_the_system').SetAttributeValue('No')
    row.GetColumnByName('CB_EC_Does_the_Customer_have_all_updated_ILDs').SetAttributeValue('Yes')
    row.GetColumnByName('CB_EC_Does_Customer_want _to_validate_ILDs_by_Honeywell').SetAttributeValue('No')
    row.GetColumnByName('CB_EC_Do_you_know_the_number_of AI_AO_Regulatory_points_DI_DO_and_Digital_Composite_points').SetAttributeValue('No')
CBECUpgradetoC300UHIOservices1.Calculate()

CBECUpgradetoC300UHIOservices2= getContainer('CB_EC_Services_2_Cont')	# for dropdown values for CB_EC_Upgrade_C300-UHIO for Services 2 Cont
for row in CBECUpgradetoC300UHIOservices2.Rows:
    row.GetColumnByName('CB_EC_Is_common_PV_sharing_between_two_or_more_than_two_CB_EC').SetAttributeValue('No')
    row.GetColumnByName('CB_EC_Detailed_DDS_required').SetAttributeValue('Yes')
    row.GetColumnByName('CB_EC_Is_HotCutover_required').SetAttributeValue('Yes')
CBECUpgradetoC300UHIOservices2.Calculate()

FSCtoSMConfiguration = getContainer("FSC_to_SM_Configuration")
if FSCtoSMConfiguration.Rows.Count > 0:
    for row in FSCtoSMConfiguration.Rows:
        row.GetColumnByName('FSC_to_SM_Are_the_FSCs_in_this_configuration_connected_to_a_SafeNet_network').SetAttributeValue('No')
        row.GetColumnByName('FSC_to_SM_Current_FSC_to_DCS_communication').SetAttributeValue('Serial Modbus-RTU ')
        row.GetColumnByName('FSC_to_SM_SM_communication_to_DCS').SetAttributeValue('Serial Modbus-RTU ')
        row.GetColumnByName('FSC_to_SM_Installed_generation_of_IO_modules').SetAttributeValue('Series-1 ')
    FSCtoSMConfiguration.Calculate()

FSCtoSMIOGC1 = getContainer("FSC_to_SM_IO_Migration_General_Information")
for row in FSCtoSMIOGC1.Rows:
    row.GetColumnByName('FSC_to_SM_IO_Migration_Where_will_the_IOs_be_installed').SetAttributeValue('Existing FSC cabinet ')
FSCtoSMIOGC1.Calculate()

FSCtoSMServices = getContainer("FSC_to_SM_Services")
for row in FSCtoSMServices.Rows:
    row.GetColumnByName('FSC_to_SM_ACAD').SetAttributeValue('No')
    row.GetColumnByName('FSC_to_SM_Factory_Acceptance_Test_required').SetAttributeValue('Yes')
    row.GetColumnByName('FSC_to_SM_Has_the_System_Audit_been_performed').SetAttributeValue('No')
FSCtoSMServices.Calculate()

FSCtoSMIOServices = getContainer("FSC_to_SM_IO_Services")
for row in FSCtoSMIOServices.Rows:
    row.GetColumnByName('FSC_to_SM_IO_Is_Honeywell_executing_the_field_cros').SetAttributeValue('No')
    row.GetColumnByName('FSC_to_SM_IO_Software_Factory_Acceptance_Test_Requ').SetAttributeValue('No')
    row.GetColumnByName('FSC_to_SM_IO_Has_the_FSC_IO_Audit_been_performed').SetAttributeValue('No')
FSCtoSMIOServices.Calculate()

xpmC300GeneralQns = getContainer('xPM_C300_General_Qns_Cont')
for row in xpmC300GeneralQns.Rows:
    row.GetColumnByName('xPM_C300_FTE_System_already_installed_on_Site').SetAttributeValue('Yes')
    row.GetColumnByName('xPM_C300_FTE_switch').SetAttributeValue('None')
    row.GetColumnByName('xPM_C300_Is_Honeywell_Providing_FTE_cables').SetAttributeValue('Yes')
    row.GetColumnByName('xPM_C300_Average_Cable_Length').SetAttributeValue('10m')
    row.SetColumnValue('xPM_C300_Number_of_xPMs_to_be_Migrated_to_C300_with_PMIO','0')
    row.SetColumnValue('xPM_C300_Number_of_additional_switches','0')
xpmC300GeneralQns.Calculate()

xpmC300SeriesCabinet = getContainer('xPM_C300_Series_ C_Cabinet_Configuration')
for row in xpmC300SeriesCabinet.Rows:
    row.GetColumnByName('xPM_C300_Cabinet_Light_Required').SetAttributeValue('No')
    row.GetColumnByName('xPM_C300_Cabinet_Thermostat_Required').SetAttributeValue('No')
    row.GetColumnByName('xPM_C300_TDI_Power_Supply_Cable_Length').SetAttributeValue('48 in')
    row.GetColumnByName('xPM_C300_Cabinet_Color').SetAttributeValue('Gray-RAL7035')
xpmC300SeriesCabinet.Calculate()

xpmC300SeriesCabinet = getContainer('xPM_C300_Series_C_Cabinet_Configuration_FAOnly')
for row in xpmC300SeriesCabinet.Rows:
    row.GetColumnByName('xPM_C300_Cabinet_Light_Required_FAOnly').SetAttributeValue('No')
    row.GetColumnByName('xPM_C300_Cabinet_Thermostat_Required_FAOnly').SetAttributeValue('No')
    row.GetColumnByName('xPM_C300_TDI_Power_Supply_Cable_Length_FAOnly').SetAttributeValue('48 in')
    row.GetColumnByName('xPM_C300_Cabinet_Color_FAOnly').SetAttributeValue('Gray-RAL7035')
xpmC300SeriesCabinet.Calculate()

xpmC300Services = getContainer('xPM_C300_Services_Cont')
for row in xpmC300Services.Rows:
    row.GetColumnByName('xPM_C300_Data_Gathering_required').SetAttributeValue('No')
    row.GetColumnByName('xPM_C300_Will_Honeywell_perform_equipment_installa').SetAttributeValue('No')
xpmC300Services.Calculate()

xpmC300Services2 = getContainer('xPM_C300_Services_Cont')
for row in xpmC300Services2.Rows:
    row.SetColumnValue('xPM_C300_Number_of_AM_migrating_to_ACE','0')
    row.SetColumnValue('xPM_C300_Number_of_AM_points','0')
xpmC300Services2.Calculate()

fdmGenQue = getContainer('FDM_Upgrade_General_questions')
colValuesDict = {"FDM_Upgrade_What_is_the_current_release_of_the_system_to_be_upgraded":"FDM R440 or Lower","FDM_Upgrade_Select_desired_FDM_release":"FDM R511","FDM_Upgrade_FDM_Media_Delivery":"Electronic Download","FDM_Upgrade_Additional_Components_to_be_offered_for_number_of_FDMs_?":"No"}
for row in fdmGenQue.Rows:
    for col in row.Columns:
        defaultVal = colValuesDict.get(col.Name)
        if defaultVal:
            col.SetAttributeValue(defaultVal)

fdmConfiguration = getContainer('FDM_Upgrade_Configuration')
colValuesDict = {"FDM_Upgrade_Do_you_want_to_upgrade_this_FDM":"No"}
for row in fdmConfiguration.Rows:
    for col in row.Columns:
        defaultVal = colValuesDict.get(col.Name)
        if defaultVal:
            col.SetAttributeValue(defaultVal)
            row.SetColumnValue(col.Name,defaultVal)
fdmConfiguration.Calculate()
fdmHWtoHost = getContainer('FDM_Upgrade_Hardware_to_host_FDM_Server')
for row in fdmHWtoHost.Rows:
    row.GetColumnByName('FDM_Upgrade_Is_HW_required_for_this_FDM').SetAttributeValue('No')
    row.GetColumnByName('FDM_Upgrade_Will_Honeywell_provide_the_FDM_server').SetAttributeValue('No')
    row.GetColumnByName('FDM_Upgrade_FDM_Gateway_PC_Hardware_Selection').SetAttributeValue('Tower')
fdmHWtoHost.Calculate()

fsctoamCabinetConfig = getContainer('FSC_to_SM_IO_New_SM_Cabinet_Configuration')
for row in fsctoamCabinetConfig.Rows:
    row.GetColumnByName('FSC_to_SM_IO_Cabinet_Access').SetAttributeValue('Front')
    row.GetColumnByName('FSC_to_SM_IO_Cabinet_IP_Rating').SetAttributeValue('Up to IP20')
    row.GetColumnByName('FSC_to_SM_IO_Cabinet_Depth').SetAttributeValue('800mm')
    row.GetColumnByName('FSC_to_SM_IO_Cabinet_Base_Plinth').SetAttributeValue('No')
    row.GetColumnByName('FSC_to_SM_IO_Cabinet_Front_Door').SetAttributeValue('Single Left Hinged')
    row.GetColumnByName('FSC_to_SM_IO_Swing_Frame').SetAttributeValue('No')
    row.GetColumnByName('FSC_to_SM_IO_Cabinet_Light').SetAttributeValue('No')
fsctoamCabinetConfig.Calculate()
fsctosmgeneralinfo2 = getContainer('FSC_to_SM_IO_Migration_General_Information2')
for row in fsctosmgeneralinfo2.Rows:
    if row.RowIndex > 1:
        break
    row['FSC_to_SM_IO_Migration_3rd_Party_Hardware_per_Audit_Report'] = '0'
fsctosmgeneralinfo2.Calculate()

lmToELMM = getContainer('LM_to_ELMM_ControlEdge_PLC_Migration_Gen_Cont')
for row in lmToELMM.Rows:
    try:
        row.GetColumnByName('LM_Does_The_Customer_Have_TPN_Release_R688.1_Or_Later').SetAttributeValue('No')
        row.GetColumnByName('Is_Honeywell_Providing_FTE_Cables').SetAttributeValue('No')
        row.GetColumnByName('Average_Cable_Length_For_PLC_Uplink').SetAttributeValue('10m')
    except:
        Trace.Write('Error setting - Default value for LM_to_ELMM_ControlEdge_PLC_Migration_Gen_Cont')
lmToELMM.Calculate()
lmToELMM3Party = getContainer('LM_to_ELMM_3rd_Party_Items')
for row in lmToELMM3Party.Rows:
    if row.RowIndex > 1:
        break
    row['LM_to_ELMM_3rd_Party_Hardware_Weidmuller'] = '0'
    row['LM_to_ELMM_3rd_Party_Hardware_Interposing_Relays'] = '0'
    row['LM_to_ELMM_3rd_Party_Hardware_Others'] = '0'
    row['LM_to_ELMM_3rd_Party_Hardware_Cabinet'] = '0'
lmToELMM3Party.Calculate()

fdmServices = getContainer('FDM_Upgrade_Services')
for row in fdmServices.Rows:
    row.GetColumnByName('FDM_Upgrade_Site_Acceptance_Test').SetAttributeValue('No')
    row.SetColumnValue('FDM_Upgrade_Number_of_Experion/TPS_Server_interface','0')
    row.SetColumnValue('FDM_Upgrade_Number_of_FDM_Gateways','0')
    row.SetColumnValue('FDM_Upgrade_Number_of_Server_Network_Interface_Licenses','0')
    row.SetColumnValue('FDM_Upgrade_Number_of_Exp_Stations_w/FDM_Maintenance_Station_View_features','0')
    #row.SetColumnValue('FDM_Upgrade_Number_of_PVST_Planner','0')
fdmServices.Calculate()

fdmAddlConfiguration = getContainer('FDM_Upgrade_Additional_Configuration')
colValuesDict = {"FDM_Upgrade_Are_additional_components_required_for_this_FDM":"No"}
for row in fdmAddlConfiguration.Rows:
    for col in row.Columns:
        defaultVal = colValuesDict.get(col.Name)
        if defaultVal:
            col.SetAttributeValue(defaultVal)