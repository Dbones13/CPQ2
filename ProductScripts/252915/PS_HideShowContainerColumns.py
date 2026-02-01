MSID_Scope_Val = Product.Attr('MIgration_Scope_Choices').SelectedValue
if MSID_Scope_Val:
    MSID_Scope_Val = MSID_Scope_Val.ValueCode
else:
    MSID_Scope_Val = ''
tabName = ''

def getAttributeValue(Name):
    return Product.Attr(Name).GetValue()

def getContainer(Name):
    return Product.GetContainerByName(Name)

def hideColumn(container,Column):
    Product.ParseString('<*CTX( Container({}).Column({}).SetPermission(Hidden) )*>'.format(container,Column))
    Product.ParseString('<*CTX( Container({}).Row(1).Column({}).Set() )*>'.format(container,Column))

def visibleColumn(container,Column):
    Product.ParseString('<*CTX( Container({}).Column({}).SetPermission(Editable) )*>'.format(container,Column))

def isHidden(container,Column):
    return Product.ParseString('<*CTX( Container({}).Column({}).GetPermission )*>'.format(container,Column)) == 'Hidden'

def resetColumnValue(container,Column):
    Product.ParseString('<*CTX( Container({}).Row(1).Column({}).Set() )*>'.format(container,Column))

def readOnlyColumn(container,Column):
    Product.ParseString('<*CTX( Container({}).Column({}).SetPermission(ReadOnly) )*>'.format(container,Column))

def editableColumn(container,Column):
    Product.ParseString('<*CTX( Container({}).Column({}).SetPermission(Editable) )*>'.format(container,Column))

def getContainer(Name):
    return Product.GetContainerByName(Name)

def getValue(row,col):
    if col.DisplayType == 'DropDown':
        val = col.DisplayValue
        if not val:
            val = row[col.Name] if row[col.Name] else ''
        return val
    if col.DisplayType == 'TextBox':
        return col.Value
    if col.DisplayType == "Label":
        return col.Value
    return ""

def setDefaultValue(container,column):
    ColumnSet1 = {"LCN_Do_you_want_HG_Point_Bar_Trend_Display": "No", "LCN_Is_there_redundant_History_Module": "No", "NONSESP_Sever_Redundancy": "No", "NONSESP_Should_RSLinx_be_added": "No", "OPM_Does_the_customer_have_EBR_installed": "No", "OPM_Is_Backbone_or_Agg_Switch_HW_refresh_required": "None", "OPM_Is_L1_L2_Switch_HW_refresh_required": "None", "OPM_Additional_Hard_Disk_For_RESS_Server": "No", "OPM_Additional_Memory_for_RESS_Server": "No", "OPM_ESC_ESF_or_ESCE_Tower_Hardware_Selection": "HP Z4 G4", "OPM_EST_Tower_Hardware_Selection": "HP Z4 G4", "OPM_Type_of_RPS_and_Thin_Client_for_ESC_ESF_ESCE": "None", "OPM_Type_of_RPS_and_Thin_Client_for_EST": "None", "OPM_Acceptance_Test_Required": "SAT", "OPM_is_system_required_Domain_controller_upgrade": "No","MSID_FEL_Data_Gathering_Required": "None", "EBR_Additional_Network_Storage_Device_NAS_required": "No", "EBR_Additional_Hard_Drive_required": "No", "EBR_Media_kit_type": "Electronic delivery", "EBR_Future_EBR_Release": "R520", "EBR_Current_EBR_Release_only_for_EBR_Upgrade": "R410 (Acronis)", "EBR_Site_Acceptance_Test_required": "No", "Orion_Auxiliary_Equipment_Unit_AEU_Turret_Type": "None", "Orion_Monitor_Type": "55-inch", "Orion_Membrane_Keyboard_Type": "None", "Orion_Advanced_Solution_Pack_license_required": "No", "Orion_Turret_Position_for_the_Left_Ext_Aux_Equip_Unit": "Wide", "Orion_Turret_Position_for_the_Right_Ext_Aux_Equip_Unit": "Wide", "Orion_Turret_Position_for_the_Center_Curved_Ext_Aux_Equip_Unit": "Wide", "Orion_Remote_Peripheral_Solution_RPS_Type": "None", "Orion_Extended_Heigh_Alarm_Ligth_Panel": "No", "Orion_Console_Alarm_Light_Custom_Logo": "No", "Orion_Alarm_Sounds": "No", "Orion_How_is_this_Orion_Console_Installation_performed": "Part of a Migration", "Orion_Is_Graphics_Scaling_needed": "No", "IS_Migration_Part_Of_ELCN_Migration": "YES", "Setup_FTE_Network_Infrastructure": "NO_FTE_NETWORK_EXISTS", "FTE_Switch_Type": "TwentyFourSTPPortCISCOSwitch", "Additional_Switches_Type": "TwentyFourSTPPortCISCOSwitch", "Additional_Server_ESV_Stations_ESF_ESC_ESF_Required": "No", "ELCN_Select_type_of_fiber_optic_switch": "Moxa (SM-G512I2)", "ELCN_Cabinet_Depth_Size": "800 cm", "ELCN_Power_Supply_Voltage": "120V, 60 Hz", "ELCN_Cabinet_Door_Type": "Standard", "ELCN_Cabinet_Keylock_Type": "Standard", "ELCN_Cabinet_Hinge_Type": "130 Degrees", "ELCN_Cabinet_Thermostat_Required": "No", "ELCN_Cabinet_Base_Required": "No", "ELCN_Cabinet_Color": "Gray-RAL7035", "TPS_EX_ESVT_Redundant": "No", "TPS_EX_ESVT_Server_Hardware": "HP DL360 G10", "TPS_EX_Additional_Hard_Drives": "No", "TPS_EX_Non_Reduntant_Conversion_ESVT": "No", "TPS_EX_Redundant_Conversion_ESVT": "No", "TPS_EX_Bundle_Conversion_Existing_Node": "AM", "TPS_EX_Bundle_Conversion_ESVT_Server_Hardware": "HP DL360 G10", "TPS_EX_Bundle_Conversion_EST_Station_Hardware": "HP Z4 G4", "TPS_EX_Bundle_Conversion_EST_Station_Mounting_Furn": "Desktop", "TPS_EX_Cabinet_Depth_Size": "800 mm", "TPS_EX_Power_Supply_Voltage": "120V, 60 Hz", "TPS_EX_Cabinet_Door_Type": "Standard", "TPS_EX_Cabinet_Keylock_Type": "Standard", "TPS_EX_Cabinet_Hinge_Type": "130 Degrees", "TPS_EX_Cabinet_Thermostat_Required": "No", "TPS_EX_Cabinet_Base_Required": "No", "TPS_EX_Cabinet_Color": "Gray-RAL7035", "TPS_EX_Additional_Server_Hardware": "HP DL360 G10", "TPS_EX_Addtional_Server_Additional_Hard_Drive": "No", "TPS_EX_Additional_Server_Additional_Memory": "None", "TPS_EX_Additional_Server_Optional_DVD": "No", "TPS_EX_Additional_Server_Display": "None", "TPS_EX_Additional_Server_Trackball": "No", "TPS_EX_Additional_Server_Cabinet_Mounting_Type": "None", "TPS_EX_Additional_Stations_Desk_Hardware": "Dell T5820XL", "TPS_EX_Additional_Stations_Cabinat_Hardware": "Dell T5820XL", "TPS_EX_Additional_Stations_RPS_Type": "None", "TPS_EX_Additional_Stations_RPS_Quad_Video_Required": "No","TPS_EX_Additional_Stations_RPS_Mounting_Furniture": "Desk", "TPS_EX_Additional_Stations_Multi_Window_Support": "No", "TPS_EX_Additional_Stations_Display_Size": "Wide", "TPS_EX_Additional_Stations_Touch_Screen": "No", "TPS_EX_Additional_Stations_Trackball": "No", "TPS_EX_Additional_Stations_IKB_OEP": "None", "TPS_EX_Additional_Stations_Interface_card": "Ethernet", "TPS_EX_Additional_Stations_Cabinet_Mounting_Type": "None","TPS_EX_Additional_Stations_Station_License?": "No", "TPS_EX_Hardware": "HP Z4 G4", "TPS_EX_Future_Mounting_Furniture": "Desktop", "TPS_EX_Computer_Adapter_Kit": "No", "TPS_EX_RPS_Type": "None", "TPS_EX_Existing_Monitor_Type": "Quad", "TPS_EX_Keyboard_Type": "None", "TPS_EX_Conversion_ACET_EAPP_Server_Hardware" : "HP DL360 G10",'TCMI_Is_Triconex_SMM_being_migrated_with_xPM_in': 'No','C200_Type_of_UOC':'UOC','C200_Type_of_downlink_communication_UOC':'E/IP','C200_Data_Gathering_Required':'No','C200_Documentation_Required':'No','C200_Factory_Acceptance_Test_Required':'No','C200_Will_Honeywell_Perform_Equipment_Installation_Activities':'No',"Number_of_Experion_Systems":'0',"Number_of_EHPM_where_HART_IO_will_be_installed":'0',"Wiring_termination_type":'Compression',"Commissioning_required":'No','C200_C300_Cabinet_Doors':'Standard','C200_C300_Cabinet_Hinge_Type':'130 Degrees','C200_C300_Cabinet_Light_Required':'No','C200_C300_Cabinet_Thermostat_Required':'No','C200_C300_Cabinet_Keylock_Type':'Standard','C200_C300_Power_Entry':'None','C200_C300_TDI_Power_Supply_Cable_Length':'48 in','C200_C300_Cabinet_Color':'Gray-RAL7035','C200_C300_Cabinet_Doors_FAOnly':'Standard','C200_C300_Cabinet_Hinge_Type_FAOnly':'130 Degrees','C200_C300_Cabinet_Light_Required_FAOnly':'No','C200_C300_Cabinet_Thermostat_Required_FAOnly':'No','C200_C300_Cabinet_Keylock_Type_FAOnly':'Standard','C200_C300_Power_Entry_FAOnly':'None','C200_C300_TDI_Power_Supply_Cable_Length_FAOnly':'48 in','C200_C300_Cabinet_Color_FAOnly':'Gray-RAL7035','CB_EC_Do_you_want_new_TCB_cables_or_just_the_Adapter_cables':'Yes - New TCB cables 10m','FSC_to_SM_IO_Migration_Where_will_the_IOs_be_installed':'Existing FSC cabinet ','FSC_to_SM_IO_Is_Honeywell_executing_the_field_cros':'No ','FSC_to_SM_IO_Software_Factory_Acceptance_Test_Requ':'No ','FSC_to_SM_IO_Has_the_FSC_IO_Audit_been_performed':'No ','xPM_C300_Average_Cable_Length':'10m','xPM_C300_Cabinet_Light_Required':'No','xPM_C300_Cabinet_Thermostat_Required':'No','xPM_C300_TDI_Power_Supply_Cable_Length':'48 in','xPM_C300_Cabinet_Color':'Gray-RAL7035','xPM_C300_Data_Gathering_required':'No','xPM_C300_Will_Honeywell_perform_equipment_installa':'No','FDM_Upgrade_What_is_the_current_release_of_the_system_to_be_upgraded':'FDM R440 or Lower','FDM_Upgrade_Select_desired_FDM_release':'FDM R511','FDM_Upgrade_FDM_Media_Delivery':'Electronic Download','FDM_Upgrade_Will_Honeywell_provide_the_FDM_server':'No','FDM_Upgrade_FDM_Gateway_PC_Hardware_Selection':'Tower', "FSC_to_SM_IO_Cabinet_Access":'Front',"FSC_to_SM_IO_Cabinet_IP_Rating":'Up to IP20',"FSC_to_SM_IO_Cabinet_Depth":'800mm',"FSC_to_SM_IO_Cabinet_Base_Plinth":'No',"FSC_to_SM_IO_Cabinet_Front_Door":'Single Left Hinged',"FSC_to_SM_IO_Cabinet_Rear_Door":'Single Left Hinged',"FSC_to_SM_IO_Swing_Frame":'No',"FSC_to_SM_IO_Is_the_series_2_FTA_and_SIC_cable_reu":'No',"FSC_to_SM_ACAD":'No',"FSC_to_SM_Factory_Acceptance_Test_required":'Yes'}
    ColumnSet2 = {"LCN_No_of_TPN_Controllers":"0","LCN_No_of_TPN_nodes":"0","NONSESP_No_of_Premium_Access_Connections":"0","NONSESP_No_of_3rd_Party_MS_Visual_Studio_License":"0","NONSESP_No_of_3rdParty_MS_SQL_Client_License":"0","NONSESP_No_of_CAB_Developer_Licenses":"0","NONSESP_No_of_Console_Stations_ESC_and_EST":"0","NONSESP_No_of_Flex_Console_Ext_Stations_ESF_ESCE":"0","NONSESP_No_of_process_points":"0","NONSESP_No_of_RESS_Remote_Users":"0","NONSESP_No_of_SCADA_points":"0","NONSESP_No_of_TPS_Connections_LCNP_Cards":"0","OPM_No_of_RESS_Remote_Users":"0","OPM_Qty_of_Control_Firewalls_CF9s":"0","OPM_Qty_of_Fieldbus_Interface_Modules":"0","OPM_Qty_of_Profibus_Modules":"0","OPM_Qty_of_RPS_and_Thin_Clients":"0","OPM_Qty_of_Series_A_IO_Modules":"0","OPM_Qty_of_Series_C_Controllers":"0","OPM_Qty_of_Series_C_IO_Modules_excluding_UIO":"0","OPM_Qty_of_UIO_UIO2_Modules":"0","OPM_Additional_hrs_for_Document_Customization":"0","NONSESP_No_of_CAB_Developer_Licenses":"0","EBR_Qty_of_EBR_New_Additional_for_Virtual_Node":"0","EBR_Qty_of_EBR_New_Additional_for_Workstation":"0","EBR_Qty_of_EBR_New_Additional_for_Server":"0",'Orion_Number_of_console_bases_with_same_configuration':"0",'Orion_Number_of_2_Position_Base_Unit':"0",'Orion_Number_of_3_Position_Base_Unit':"0",'Orion_Number_of_Left_Auxiliary_Equipment_Unit':"0",'Orion_Number_of_Right_Auxiliary_Equipment_Unit':"0",'Orion_Number_of_Right_Extended_Auxiliary_Equipment_Unit':"0",'Orion_Number_of_Center_Straight_Auxiliary_Equipment_Unit':"0",'Orion_Number_of_Center_Curved_Auxiliary_Equipment_Unit':"0",'Orion_Number_of_Center_Curved_Extended_Auxiliary_Equipment_Unit':"0",'Orion_Number_of_Center_Joining_Unit':"0",'Orion_Number_of_Jack_Lift_&_Ramps_System_needed':"0",'Orion_Number_of_Additional_23_monitors':"0",'Orion_Number_of_Additional_Monitor_Mounting_Arm_for_23':"0",'Orion_Number_of_Left_Extended_Auxiliary_Equipment_Unit':"0",'Orion_Display_Devices_per_position':'1','Orion_Number_of_existing_stations_that_will_be_migrated_to_Orion_Console':'0','Orion_Number_of_new_Orion_stations_that_will_be_installed':'0','Orion_Number_of_existing_HMI_Graphics':'0','Orion_Honeywell_hours_for_Orion_Console_unboxing_and_installation_in_Control_Room':'0','Orion_Number_of_Orion_Console_configurations_needed':'0', "ELCN_Qty_of_NGs_more_than_100mts_from_existing_fiber_concentrators": "0",'Spare_Parts_Quantity':'0','C200_additional_hours_for_UOC_installation':'0','C200_How_many_co_located_C200_groups_exists':'0','xPM_C300_Number_of_xPM_Analog_Input_points':'0','xPM_C300_Number_of_xPM_Analog_Output_points':'0','xPM_C300_Number_of_xPM_Digital_Input_points':'0','xPM_C300_Number_of_xPM_Digital_output_points':'0','xPM_C300_Number_of_xPM_Digital_composite_points':'0','xPM_C300_Number_of_xPM_Regulatory_CNTL_points':'0','xPM_C300_Number_of_xPM_Regulatory_PV_points':'0','xPM_C300_Numer_of_xPM_Flags_Numeric_timer':'0','xPM_C300_Number_of_xPM_Logic_points':'0','xPM_C300_Number_of_xPM_CL':'0','xPM_C300_Number_of_Simple_xPM_CL':'0','xPM_C300_Number_of_Complex_xPM_CL':'0','xPM_C300_Number_of_AM_CL':'0','xPM_C300_Number_of_Simple_AM_CL':'0','xPM_C300_Number_of_medium_AM_CL':'0','xPM_C300_Number_of_complex_AM_CL':'0','xPM_C300_Number_of_xPM_IOMs':'0','xPM_C300_Number_of_Pulse_Input_IOMs':'0','xPM_C300_Number_of_Serial_Interface_modules':'0','xPM_C300_Number_of_Serial_Interface_points_for_Scada_conversion':'0','xPM_C300_Number_of_devices_connected_to_xPM_SI_for_PCDI_conversion':'0','xPM_C300_Number_of_SI_Modbus_and_Allen_Bradley_Rockwell_Array_points_for_PCDI_conversion':'0','xPM_C300_Number_of_LLAI_with_FW_Rev_less_than_6.0':'0','xPM_C300_Number_of_LLMUX_with_FW_Rev_less_than_4.1':'0','xPM_C300_Number_of_RHMUX_with_FW_Rev_less_than_6.0':'0','xPM_C300_Number_of_HLAI_with_FW_Rev_bet_3.4_and_6.0':'0','xPM_C300_Number_of_HLAI_with_FW_Rev_GEQ_3.3':'0','xPM_C300_Number_of_STI_MV_with_FW_Rev_less_than_6.0':'0','xPM_C300_Number_of_AM_migrating_to_ACE':'0','xPM_C300_Number_of_AM_points':'0','C200_Number_of_Redundant_FIM2_IOMs_to_FIM4_conversion':'0','C200_Number_of_Redundant_FIM2_IOMs_to_FIM8_conversion':'0',"OPM_RESS_Server_configuration":"Physical"}
    ColumnSet3 = {"OPM_Experion_Server_Hardware_Selection":"HP DL360 G10","OPM_Select_RESS_platform_configuration":"HP DL360 G10",'CB_EC_Do_you_know_the_number_of AI_AO_Regulatory_points_DI_DO_and_Digital_Composite_points':'No',"xPM_Distance_of_Fiber_Optic_Extenders":"2 km","OPM_Is_this_is_a_Remote_Migration_Service_RMS": "Yes","OPM_Other_Servers_Hardware_Selection": "HP DL360 G10", "OPM_ACET_EAPP_Server_Hardware_Selection": "HP DL360 G10"}
    Container = getContainer(container)
    for row in Container.Rows:
        if column in ColumnSet1:
            row.GetColumnByName(column).SetAttributeValue(ColumnSet1[column])
        elif column in ColumnSet2:
            row.SetColumnValue(column,ColumnSet2[column])
        elif column in ColumnSet3:
            row.GetColumnByName(column).ReferencingAttribute.SelectValue(ColumnSet3[column])
            row.ApplyProductChanges()
            Container.Calculate()
        break

for tab in Product.Tabs:
    if tab.IsSelected:
        tabName = tab.Name

columnsToBeHidden = dict()
MigrationConfigRules1 =SqlHelper.GetList("Select * from MIGRATION_CONFIGURATION_RULES where Product = '"+tabName+"'")
for rule in MigrationConfigRules1:
    l = columnsToBeHidden.get(rule.Container,list())
    if rule.Container_Column not in l:
        l.append(rule.Container_Column)
    columnsToBeHidden[rule.Container] = l

MigrationConfigRules =SqlHelper.GetList("Select * from MIGRATION_CONFIGURATION_RULES where (Scope = '"+MSID_Scope_Val+"' or Scope = '')and Product = '"+tabName+"'" )

for rule in MigrationConfigRules:

    if rule.Dept_Cont_1 == '':
        if isHidden(rule.Container,rule.Container_Column):
            visibleColumn(rule.Container,rule.Container_Column)
            setDefaultValue(rule.Container,rule.Container_Column)
        columnsToBeHidden[rule.Container].remove(rule.Container_Column)

    elif rule.Dept_Cont_1 != '' and rule.Dept_Cont_2 == '' and rule.Dept_Cont_3 == '' and rule.Dept_Cont_4 == '':
        DeptContainer1 = getContainer(rule.Dept_Cont_1)
        for row in DeptContainer1.Rows:
            if row[rule.Dept_Cont_Col_1] == rule.Dept_Cont_Col_Value_1:
                if isHidden(rule.Container,rule.Container_Column):
                    visibleColumn(rule.Container,rule.Container_Column)
                    setDefaultValue(rule.Container,rule.Container_Column)
                try:
                    columnsToBeHidden[rule.Container].remove(rule.Container_Column)
                except:
                    pass
            break

    elif rule.Dept_Cont_1 != '' and rule.Dept_Cont_2 != '' and rule.Dept_Cont_3 == '' and rule.Dept_Cont_4 == '':
        DeptContainer1 = getContainer(rule.Dept_Cont_1)
        DeptContainer2 = getContainer(rule.Dept_Cont_2)
        for row1 in DeptContainer1.Rows:
            for row2 in DeptContainer2.Rows:
                if row1[rule.Dept_Cont_Col_1] == rule.Dept_Cont_Col_Value_1 and row2[rule.Dept_Cont_Col_2] == rule.Dept_Cont_Col_Value_2:
                    if isHidden(rule.Container,rule.Container_Column):
                        visibleColumn(rule.Container,rule.Container_Column)
                        setDefaultValue(rule.Container,rule.Container_Column)
                    columnsToBeHidden[rule.Container].remove(rule.Container_Column)
                break
            break

    elif rule.Dept_Cont_1 != '' and rule.Dept_Cont_2 != '' and rule.Dept_Cont_3 != '' and rule.Dept_Cont_4 == '':
        DeptContainer1 = getContainer(rule.Dept_Cont_1)
        DeptContainer2 = getContainer(rule.Dept_Cont_2)
        DeptContainer3 = getContainer(rule.Dept_Cont_3)
        for row1 in DeptContainer1.Rows:
            for row2 in DeptContainer2.Rows:
                for row3 in DeptContainer3.Rows:
                    if row1[rule.Dept_Cont_Col_1] == rule.Dept_Cont_Col_Value_1 and row2[rule.Dept_Cont_Col_2] == rule.Dept_Cont_Col_Value_2 and row3[rule.Dept_Cont_Col_3] == rule.Dept_Cont_Col_Value_3:
                        if isHidden(rule.Container,rule.Container_Column):
                            visibleColumn(rule.Container,rule.Container_Column)
                            setDefaultValue(rule.Container,rule.Container_Column)
                        columnsToBeHidden[rule.Container].remove(rule.Container_Column)
                    break
                break
            break

    elif rule.Dept_Cont_1 != '' and rule.Dept_Cont_2 != '' and rule.Dept_Cont_3 != '' and rule.Dept_Cont_4 != '':
        DeptContainer1 = getContainer(rule.Dept_Cont_1)
        DeptContainer2 = getContainer(rule.Dept_Cont_2)
        DeptContainer3 = getContainer(rule.Dept_Cont_3)
        DeptContainer4 = getContainer(rule.Dept_Cont_4)
        for row1 in DeptContainer1.Rows:
            for row2 in DeptContainer2.Rows:
                for row3 in DeptContainer3.Rows:
                    for row4 in DeptContainer4.Rows:
                        if row1[rule.Dept_Cont_Col_1] == rule.Dept_Cont_Col_Value_1 and row2[rule.Dept_Cont_Col_2] == rule.Dept_Cont_Col_Value_2 and row3[rule.Dept_Cont_Col_3] == rule.Dept_Cont_Col_Value_3 and row4[rule.Dept_Cont_Col_4] == rule.Dept_Cont_Col_Value_4:
                            if isHidden(rule.Container,rule.Container_Column):
                                visibleColumn(rule.Container,rule.Container_Column)
                                setDefaultValue(rule.Container,rule.Container_Column)
                            columnsToBeHidden[rule.Container].remove(rule.Container_Column)
                        break
                    break
                break
            break
for row in getContainer("TPS_EX_General_Questions").Rows:
    if row['QTY_New_Cabinates'] in ('','0'):
        x = columnsToBeHidden.get("TPS_EX_Server_Cabinet_Config",list())
        x.append('TPS_EX_Cabinet_Depth_Size')
        x.append('TPS_EX_Power_Supply_Voltage')
        x.append('TPS_EX_Cabinet_Door_Type')
        x.append('TPS_EX_Cabinet_Keylock_Type')
        x.append('TPS_EX_Cabinet_Hinge_Type')
        x.append('TPS_EX_Cabinet_Thermostat_Required')
        x.append('TPS_EX_Cabinet_Base_Required')
        x.append('TPS_EX_Cabinet_Color')
        columnsToBeHidden["TPS_EX_Server_Cabinet_Config"] = x

for container in columnsToBeHidden.keys():
    if columnsToBeHidden.get(container):
        for column in columnsToBeHidden.get(container):
            hideColumn(container,column)

selectedProducts = list()

for row in getContainer("MSID_Product_Container").Rows:
    selectedProducts.append(row["Product Name"])

if getAttributeValue("MSID_Selected_Products") and 'LCN One Time Upgrade' not in selectedProducts:
    hideColumn("MSID_CommonQuestions","MSID_Current_TPN_Release")
    hideColumn("MSID_CommonQuestions","MSID_Future_TPN_Release")
else:
    if isHidden("MSID_CommonQuestions","MSID_Current_TPN_Release"):
        visibleColumn("MSID_CommonQuestions","MSID_Current_TPN_Release")
    if isHidden("MSID_CommonQuestions","MSID_Future_TPN_Release"):
        visibleColumn("MSID_CommonQuestions","MSID_Future_TPN_Release")
'''if getAttributeValue("MSID_Selected_Products") and 'OPM' not in selectedProducts and 'Non-SESP Exp Upgrade' not in selectedProducts and 'TPS to Experion' not in selectedProducts:
    hideColumn("MSID_CommonQuestions","MSID_Current_Experion_Release")
    hideColumn("MSID_CommonQuestions","MSID_Future_Experion_Release")
else:
    if isHidden("MSID_CommonQuestions","MSID_Current_Experion_Release"):
        visibleColumn("MSID_CommonQuestions","MSID_Current_Experion_Release")
    if isHidden("MSID_CommonQuestions","MSID_Future_Experion_Release"):
        visibleColumn("MSID_CommonQuestions","MSID_Future_Experion_Release")'''
if getAttributeValue("MIgration_Scope_Choices") == "HW/SW":
    Product.DisallowAttr("OPM_Which_documentation_is_required")
    Product.DisallowAttr("TPS_EX_Which_Documentation_Required")
    Product.DisallowAttr("EHPM_HART_IO_Which_documentation_is_required?")
    Product.DisallowAttr("Orion_Which_documentation_is_required")
    Product.DisallowAttr("xPM_C300_Which_Documentation_Required")
else:
    Product.AllowAttr("OPM_Which_documentation_is_required")
    Product.AllowAttr("TPS_EX_Which_Documentation_Required")
    Product.AllowAttr("EHPM_HART_IO_Which_documentation_is_required?")
    Product.AllowAttr("Orion_Which_documentation_is_required")
    Product.AllowAttr("xPM_C300_Which_Documentation_Required")

if 'EBR' in selectedProducts:
    ebrBasicCon =  getContainer('EBR_Basic_Information')
    hwtohostebrphysical = getContainer('EBR_Hardware_to_Host_EBR_Physical_Node_Only')
    for row in ebrBasicCon.Rows:
        if row['EBR_Current_EBR_Release_only_for_EBR_Upgrade'] in ('R43x (Acronis)','R501 (Acronis)'):
            visibleColumn('EBR_Upgrade', 'EBR_Qty_of_EBR_Upgrade_for_Virtual_Node')
            break
        else:
            hideColumn('EBR_Upgrade', 'EBR_Qty_of_EBR_Upgrade_for_Virtual_Node')
            break
    for row1 in hwtohostebrphysical.Rows:
        if row1['EBR_If_hardware_desired_select_host_type'] in ('DELL T150 STD TPM','DELL T550 STD TPM','DELL T550 STD No TPM','DELL R250XE STD TPM','DELL R450 STD TPM','DELL R450 STD No TPM'):
            hideColumn('EBR_Hardware_to_Host_EBR_Physical_Node_Only','EBR_Additional_Hard_Drive_required')
            break
        else:
            visibleColumn('EBR_Hardware_to_Host_EBR_Physical_Node_Only','EBR_Additional_Hard_Drive_required')
            break
if 'ELCN' in selectedProducts:
    elcnUpgradeNewElcnNodesCon =  getContainer('ELCN_Upgrade_New_ELCN_Nodes')
    totalQtyOfNetworkGateway = 0
    rowAssetDB = 2
    rowIndex = 0
    '''Sum of Upgrade Physical, Virtual, New Physical, and Virtual Quantities'''
    for row in elcnUpgradeNewElcnNodesCon.Rows:
        if rowIndex != rowAssetDB:
            for column in row.Columns:
                if column.Name == "ELCN_Qty_of_Network_Gateways" and row[column.Name] != '':
                    totalQtyOfNetworkGateway += int(row[column.Name])
                    break
        rowIndex += 1
    if totalQtyOfNetworkGateway > 0 :
        if getAttributeValue("MIgration_Scope_Choices") in ["LABOR", "HW/SW/LABOR"]:
            if isHidden("ELCN_Services", "ELCN_Services_for_NG_Switch_Configuration"):
                visibleColumn("ELCN_Services", "ELCN_Services_for_NG_Switch_Configuration")
                setDefaultValue("ELCN_Services", "ELCN_Services_for_NG_Switch_Configuration")
        if getAttributeValue("MIgration_Scope_Choices") in ["HW/SW", "HW/SW/LABOR"]:
            if isHidden("ELCN_Network_Gateway_Upgrade", "ELCN_Select_Switch_configuration_required"):
                visibleColumn("ELCN_Network_Gateway_Upgrade", "ELCN_Select_Switch_configuration_required")
                setDefaultValue("ELCN_Network_Gateway_Upgrade", "ELCN_Select_Switch_configuration_required")
        '''Hide entire Network Gateway Upgrade if scope not in HW/SW or HW/SW/LABOR'''
        if getAttributeValue("MIgration_Scope_Choices") not in ["HW/SW", "HW/SW/LABOR"]:
            hideColumn("ELCN_Network_Gateway_Upgrade", "ELCN_Select_Switch_configuration_required")
            hideColumn("ELCN_Network_Gateway_Upgrade", "ELCN_Qty_of_NGs_more_than_100mts_from_existing_fiber_concentrators")
            hideColumn("ELCN_Network_Gateway_Upgrade", "ELCN_Select_type_of_fiber_optic_switch")
        else:
            visibleColumn("ELCN_Network_Gateway_Upgrade", "ELCN_Select_Switch_configuration_required")
            setDefaultValue("ELCN_Network_Gateway_Upgrade", "ELCN_Select_Switch_configuration_required")
    else:
        if getAttributeValue("MIgration_Scope_Choices") in ["LABOR", "HW/SW/LABOR"]:
            hideColumn("ELCN_Services", "ELCN_Services_for_NG_Switch_Configuration")
        '''Hide entire Network Gateway Upgrade'''
        hideColumn("ELCN_Network_Gateway_Upgrade", "ELCN_Select_Switch_configuration_required")
        hideColumn("ELCN_Network_Gateway_Upgrade", "ELCN_Qty_of_NGs_more_than_100mts_from_existing_fiber_concentrators")
        hideColumn("ELCN_Network_Gateway_Upgrade", "ELCN_Select_type_of_fiber_optic_switch")
    container = getContainer('ELCN_Upgrade_New_ELCN_Nodes')
    elcnbasicCon= getContainer('ELCN_Basic_Information')
    Zero_Quantity = '0'
    keys_to_check = ['ELCN_Qty_of_Non_Redundant_ESVTs','ELCN_Qty_of_ESTs','ELCN_Qty_of_Redundant_ESVTs','ELCN_Qty_of_EAPPs','ELCN_Qty_of_HMs','ELCN_Qty_of_Non_redundant_AMs','ELCN_Qty_of_Redundant_AMs','ELCN_Qty_of_Non_Redundant_HGs','ELCN_Qty_of_Redundant_HGs','ELCN_Qty_of_Non_Redundant_EHBs','ELCN_Qty_of_Redundant_EHBs','ELCN_Qty_of_Non_Redundant_ETN_EHBs','ELCN_Qty_of_Redundant_ETN_EHBs','ELCN_Qty_of_Non_Redundant_NIMs','ELCN_Qty_of_Redundant_NIMs','ELCN_Qty_of_Non_Redundant_ENIMs','ELCN_Qty_of_Redundant_ENIMs','ELCN_Qty_of_Non_Redundant_ETN_ENIMs','ELCN_Qty_of_Redundant_ETN_ENIMs','ELCN_Qty_of_Non_Redundant_xPLCGs','ELCN_Qty_of_Redundant_xPLCGs','ELCN_Qty_of_Network_Gateways','ELCN_Qty_of_ACE_Ts']
    if getAttributeValue("MIgration_Scope_Choices") == "LABOR":
        for qty in elcnbasicCon.Rows:
            if qty['ELCN_Qty_of_Additional_Switches']!=0:
                qty['ELCN_Qty_of_Additional_Switches']=Zero_Quantity
                hideColumn("ELCN_Basic_Information", "ELCN_Qty_of_Additional_Switches")
        for row in container.Rows:
            for key in keys_to_check:
                if row[key] != 0:
                    row[key] = Zero_Quantity
    else:
        visibleColumn("ELCN_Basic_Information","ELCN_Qty_of_Additional_Switches")
if 'TPS to Experion' in selectedProducts:
    visibleColumn("MSID_CommonQuestions","MSID_Acceptance_Test_Required")
    hideColumn("MSID_CommonQuestions", "MSID_Will_Honeywell_perform_equipment_installation")
if 'EHPM/EHPMX/ C300PM' in selectedProducts or 'Orion Console' in selectedProducts:
    hideColumn("MSID_CommonQuestions", "MSID_Will_Honeywell_perform_equipment_installation")
else:
    hideColumn("MSID_CommonQuestions", "MSID_Will_Honeywell_perform_equipment_installation")

selectedProducts = Product.Attr('MSID_Selected_Products').GetValue().split('<br>')
if len(selectedProducts) == 1 and ("TCMI" in selectedProducts or "Orion Console" in selectedProducts or "LCN One Time Upgrade" in selectedProducts):
    hideColumn("MSID_CommonQuestions", "MSID_FEL_Data_Gathering_Required")

if 'C200 Migration' in selectedProducts or 'xPM to C300 Migration' in selectedProducts or "LM to ELMM ControlEdge PLC" in selectedProducts or "3rd Party PLC to ControlEdge PLC/UOC" in selectedProducts:
    if isHidden("MSID_CommonQuestions","MSID_Is_FTE_based_System_already_installed_on_Site"):
        visibleColumn("MSID_CommonQuestions","MSID_Is_FTE_based_System_already_installed_on_Site")
else:
    hideColumn("MSID_CommonQuestions", "MSID_Is_FTE_based_System_already_installed_on_Site")

if 'C200 Migration' in selectedProducts or  'xPM to C300 Migration' in selectedProducts or 'TPS to Experion' in selectedProducts:
    if isHidden("MSID_CommonQuestions","MSID_Is_Switch_Configuration_in_Honeywell_Scope"):
        visibleColumn("MSID_CommonQuestions","MSID_Is_Switch_Configuration_in_Honeywell_Scope")
else:
    hideColumn("MSID_CommonQuestions", "MSID_Is_Switch_Configuration_in_Honeywell_Scope")

if 'C200 Migration' in selectedProducts and len(selectedProducts) == 1:
    if not isHidden("MSID_CommonQuestions","MSID_Will_Honeywell_perform_equipment_installation"):
        hideColumn("MSID_CommonQuestions","MSID_Will_Honeywell_perform_equipment_installation")
if 'xPM to C300 Migration' in selectedProducts and len(selectedProducts) == 1:
    if not isHidden("MSID_CommonQuestions","MSID_Will_Honeywell_perform_equipment_installation"):
        hideColumn("MSID_CommonQuestions","MSID_Will_Honeywell_perform_equipment_installation")

if 'CB-EC Upgrade to C300-UHIO' in selectedProducts and MSID_Scope_Val!="HWSW":
    CBECServicesCont=  getContainer('CB_EC_Services_1_Cont')
    rowCBECServicesCont= CBECServicesCont.Rows[0]
    if rowCBECServicesCont['CB_EC_Do_you_know_the_number_of AI_AO_Regulatory_points_DI_DO_and_Digital_Composite_points'] == "Yes":
        editableColumn("CB_EC_Services_1_Cont", "CB_EC_Total_Number_of_Analog_Input_points_HGAIN")
        editableColumn("CB_EC_Services_1_Cont", "CB_EC_Total_Number_of_Analog_Output_points_HGAOT")
        editableColumn("CB_EC_Services_1_Cont", "CB_EC_Total_Number_of_Regulatory_points_HGREG")
        editableColumn("CB_EC_Services_1_Cont", "CB_EC_Total_Number_of_Digital_Input_points_HGDIN")
        editableColumn("CB_EC_Services_1_Cont", "CB_EC_Total_Number_of_Digital_Output_points_HGDOT")
        editableColumn("CB_EC_Services_1_Cont", "CB_EC_Total_Number_of_Digital_Composite_points_HGDCP")
    else:
        readOnlyColumn("CB_EC_Services_1_Cont", "CB_EC_Total_Number_of_Analog_Input_points_HGAIN")
        readOnlyColumn("CB_EC_Services_1_Cont", "CB_EC_Total_Number_of_Analog_Output_points_HGAOT")
        readOnlyColumn("CB_EC_Services_1_Cont", "CB_EC_Total_Number_of_Regulatory_points_HGREG")
        readOnlyColumn("CB_EC_Services_1_Cont", "CB_EC_Total_Number_of_Digital_Input_points_HGDIN")
        readOnlyColumn("CB_EC_Services_1_Cont", "CB_EC_Total_Number_of_Digital_Output_points_HGDOT")
        readOnlyColumn("CB_EC_Services_1_Cont", "CB_EC_Total_Number_of_Digital_Composite_points_HGDCP")
    
    proposalType = Quote.GetCustomField("EGAP_Proposal_Type").Content
    if proposalType == "Budgetary":
        readOnlyColumn("CB_EC_Services_1_Cont", "CB_EC_Total_Number_of_Cascade_Loop")
        readOnlyColumn("CB_EC_Services_1_Cont", "CB_EC_Total_Number_of_Complex_Loop")
        readOnlyColumn("CB_EC_Services_1_Cont", "CB_EC_Total_Number_of_Aux_function")
    else:
        editableColumn("CB_EC_Services_1_Cont", "CB_EC_Total_Number_of_Cascade_Loop")
        editableColumn("CB_EC_Services_1_Cont", "CB_EC_Total_Number_of_Complex_Loop")
        editableColumn("CB_EC_Services_1_Cont", "CB_EC_Total_Number_of_Aux_function")

if 'EHPM HART IO' in selectedProducts and len(selectedProducts) == 1:
    if not isHidden("MSID_CommonQuestions","MSID_FEL_Data_Gathering_Required"):
        hideColumn("MSID_CommonQuestions","MSID_FEL_Data_Gathering_Required")

if 'CB-EC Upgrade to C300-UHIO' in selectedProducts and len(selectedProducts) == 1:
    if not isHidden("MSID_CommonQuestions","MSID_FEL_Data_Gathering_Required"):
        hideColumn("MSID_CommonQuestions","MSID_FEL_Data_Gathering_Required")

if 'CB-EC Upgrade to C300-UHIO' in selectedProducts and len(selectedProducts) == 1:
    if not isHidden("MSID_CommonQuestions","MSID_Will_Honeywell_perform_equipment_installation"):
        hideColumn("MSID_CommonQuestions","MSID_Will_Honeywell_perform_equipment_installation")

if 'C200 Migration' in selectedProducts and len(selectedProducts) == 1:
    if not isHidden("MSID_CommonQuestions","MSID_FEL_Data_Gathering_Required"):
        hideColumn("MSID_CommonQuestions","MSID_FEL_Data_Gathering_Required")
if 'xPM to C300 Migration' in selectedProducts or 'ELCN' in selectedProducts:
    if isHidden("MSID_CommonQuestions","MSID_Is_Site_Acceptance_Test_Required"):
        visibleColumn("MSID_CommonQuestions","MSID_Is_Site_Acceptance_Test_Required")
else:
    hideColumn("MSID_CommonQuestions","MSID_Is_Site_Acceptance_Test_Required")
    hideColumn("MSID_CommonQuestions","XPM_to_C300_Power_and_Heat_Calculation")
if 'xPM to C300 Migration' in selectedProducts or 'EHPM HART IO' in selectedProducts:
    if not isHidden("MSID_CommonQuestions","MSID_Acceptance_Test_Required") and ('CB-EC Upgrade to C300-UHIO' not in selectedProducts and 'TPS to Experion' not in selectedProducts):
        hideColumn("MSID_CommonQuestions","MSID_Acceptance_Test_Required")
if 'EHPM HART IO' in selectedProducts:
    if isHidden("MSID_CommonQuestions","EHPM_HART_IO_Costruction_Work_Package_documentation_required"):
        visibleColumn("MSID_CommonQuestions","EHPM_HART_IO_Costruction_Work_Package_documentation_required")
else:
    hideColumn("MSID_CommonQuestions", "EHPM_HART_IO_Costruction_Work_Package_documentation_required")
if ('Non - SESP FDM Upgrade' in selectedProducts or "FDM Upgrade" in selectedProducts )and len(selectedProducts) == 1:
    hideColumn("MSID_CommonQuestions","MSID_FEL_Data_Gathering_Required")
    hideColumn("MSID_CommonQuestions","MSID_Acceptance_Test_Required")
if "EBR" in selectedProducts and len(selectedProducts) == 1:
    hideColumn("MSID_CommonQuestions","MSID_FEL_Data_Gathering_Required")
    hideColumn("MSID_CommonQuestions","MSID_Will_Honeywell_perform_equipment_installation")
    hideColumn("MSID_CommonQuestions","MSID_Acceptance_Test_Required")
if "FSC to SM" in selectedProducts and Quote.GetCustomField('EGAP_Proposal_Type').Content == 'Budgetary':
    hideColumn("FSC_to_SM_Services","FSC_to_SM_Has_the_System_Audit_been_performed")
    hideColumn("FSC_to_SM_Services","FSC_to_SM_In_Office_Eng_hours_per_Audit_Report")
    hideColumn("FSC_to_SM_Services","FSC_to_SM_On_Site_Eng_hours_per_Audit_Report")
    hideColumn("FSC_to_SM_3rd_Party_Items","FSC_to_SM_3rd_Party_Hardware_per_Audit_Report")
if "FSC to SM IO Migration" in selectedProducts and Quote.GetCustomField('EGAP_Proposal_Type').Content == 'Budgetary':
    hideColumn("FSC_to_SM_IO_Migration_General_Information2","FSC_to_SM_IO_Migration_3rd_Party_Hardware_per_Audit_Report")
    hideColumn("FSC_to_SM_IO_Services","FSC_to_SM_IO_Has_the_FSC_IO_Audit_been_performed")
    hideColumn("FSC_to_SM_IO_Services2","FSC_to_SM_IO_In_Office_Eng_hours_per_Audit_Report")
    hideColumn("FSC_to_SM_IO_Services2","FSC_to_SM_IO_On_Site_Eng_hours_per_Audit_Report")
if "FDM Upgrade" in selectedProducts and MSID_Scope_Val!="LABOR" :
    con = Product.GetContainerByName("FDM_Upgrade_Additional_Configuration")
    for i in con.Rows:
        if(i["FDM_Upgrade_Audit_trail_file_required"] =="No"):
            i["FDM_Upgrade_Number_of_Audit_Trail_Devices"] = "0"
if 'C200 Migration' in selectedProducts:
    c200con = getContainer('C200_Migration_General_Qns_Cont')
    c200conrow = c200con.Rows[0]
    if c200conrow["C200_FTE_Switch_to_connect_required_exp_servers"] in ("None" or " "):
        hideColumn("C200_Migration_General_Qns_Cont","C200_Number_of_additional_switches")
if 'OPM' in selectedProducts:
    if getAttributeValue("MIgration_Scope_Choices") == "HW/SW":
        hideColumn('OPM_Basic_Information','OPM_Is_this_is_a_Remote_Migration_Service_RMS')
        hideColumn('OPM_Basic_Information','OPM_If_AMT_Will_Not_Be_Used')