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
def setDefaultColumnForDropdown(container,Column, value):
    Product.ParseString('<*CTX( Container({}).Row(1).Column({}).Set({}) )*>'.format(container,Column, value))
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
    ColumnSet3 = {"xPM_Distance_of_Fiber_Optic_Extenders":"2 km"}
    Container = getContainer(container)
    for row in Container.Rows:
        if column in ColumnSet3:
            Trace.Write('Attribute Update Succesful : {}'.format(row.GetColumnByName(column).ReferencingAttribute.SelectValue(ColumnSet3[column])))
            row.ApplyProductChanges()
            Container.Calculate()
        break

selectedProducts = list()
for row in getContainer("MSID_Product_Container").Rows:
    selectedProducts.append(row["Product Name"])

if 'Graphics Migration' in selectedProducts:
    graphicscon = getContainer('Graphics_Migration_Migration_Scenario')
    graphicsconrow = graphicscon.Rows[0]
    if getAttributeValue("MIgration_Scope_Choices") in ["HW/SW"]:
        hideColumn("Graphics_Migration_Migration_Scenario","Graphics_Migration_For_existing_US_GUS_DSP_what_percentage_of_Standard_Builds_will_be_used?")
    if graphicsconrow["Graphics_Migration_Type_of_Existing_Displays"] in ('Existing US Graphics','Existing GUS Graphics','Existing Experion .DSP Graphics'):
        hideColumn("Graphics_Migration_Migration_Scenario","Graphics_Migration_Is_Standard_Builds_used_for_EXP_to_EXP?")
    else:
        if getAttributeValue("MIgration_Scope_Choices") not in ["HW/SW"]:
            if isHidden("Graphics_Migration_Migration_Scenario","Graphics_Migration_Is_Standard_Builds_used_for_EXP_to_EXP?"):
                visibleColumn("Graphics_Migration_Migration_Scenario","Graphics_Migration_Is_Standard_Builds_used_for_EXP_to_EXP?")
                setDefaultColumnForDropdown("Graphics_Migration_Migration_Scenario","Graphics_Migration_Is_Standard_Builds_used_for_EXP_to_EXP?","No")
    if graphicsconrow["Graphics_Migration_Type_of_Existing_Displays"] not in ('Existing US Graphics','Existing GUS Graphics','Existing Experion .DSP Graphics'):
        hideColumn("Graphics_Migration_Migration_Scenario","Graphics_Migration_For_existing_US_GUS_DSP_what_percentage_of_Standard_Builds_will_be_used?")
    else:
        if getAttributeValue("MIgration_Scope_Choices") not in ["HW/SW"]:
            if isHidden("Graphics_Migration_Migration_Scenario","Graphics_Migration_For_existing_US_GUS_DSP_what_percentage_of_Standard_Builds_will_be_used?"):
                visibleColumn("Graphics_Migration_Migration_Scenario","Graphics_Migration_For_existing_US_GUS_DSP_what_percentage_of_Standard_Builds_will_be_used?")
                graphicsconrow["Graphics_Migration_For_existing_US_GUS_DSP_what_percentage_of_Standard_Builds_will_be_used?"] = "100"
    if graphicsconrow["Graphics_Migration_For_existing_US_GUS_DSP_what_percentage_of_Standard_Builds_will_be_used?"] == "100" or isHidden("Graphics_Migration_Migration_Scenario","Graphics_Migration_For_existing_US_GUS_DSP_what_percentage_of_Standard_Builds_will_be_used?"):
        listColumnhide = ["Graphics_Migration_Using_device_control_digital_composite_block_for_all_digital_equipment?","Graphics_Migration_Have_multiple_DI_or_DO_parameters_that_must_be_combined_in_one_shape?","Graphics_Migration_Is_the_system_connected_to_Hiway_Gateway_Controllers?","Graphics_Migration_Require_multi_tag_shapes?","Graphics_Migration_Have_process_module_point_AM_custom_Data_points_as_part_of_the_point_config","Graphics_Migration_Require_an_HMI_interface_for_AM_or_HPM_CL_applications?","Graphics_Migration_Have_array_point_that_requires_a_HMIWeb_interface?","Graphics_Migration_Willing_to_accept_alternative_visualization_solution_for_specific_functions?","Graphics_Migration_Have_specific_native_or_GUS_displays_that_support_a_specific_application?"]
        for col in listColumnhide:
            hideColumn("Graphics_Migration_Migration_Scenario",col)
    else:
        if getAttributeValue("MIgration_Scope_Choices") not in ["HW/SW"] and not isHidden("Graphics_Migration_Migration_Scenario","Graphics_Migration_For_existing_US_GUS_DSP_what_percentage_of_Standard_Builds_will_be_used?"):
            listColumn = ["Graphics_Migration_Using_device_control_digital_composite_block_for_all_digital_equipment?","Graphics_Migration_Have_multiple_DI_or_DO_parameters_that_must_be_combined_in_one_shape?","Graphics_Migration_Is_the_system_connected_to_Hiway_Gateway_Controllers?","Graphics_Migration_Have_process_module_point_AM_custom_Data_points_as_part_of_the_point_config","Graphics_Migration_Require_an_HMI_interface_for_AM_or_HPM_CL_applications?","Graphics_Migration_Have_array_point_that_requires_a_HMIWeb_interface?","Graphics_Migration_Willing_to_accept_alternative_visualization_solution_for_specific_functions?","Graphics_Migration_Have_specific_native_or_GUS_displays_that_support_a_specific_application?"]
            for col in listColumn:
                if isHidden("Graphics_Migration_Migration_Scenario",col):
                    visibleColumn("Graphics_Migration_Migration_Scenario",col)
                    setDefaultColumnForDropdown("Graphics_Migration_Migration_Scenario",col,"No")
            if isHidden("Graphics_Migration_Migration_Scenario","Graphics_Migration_Require_multi_tag_shapes?"):
                visibleColumn("Graphics_Migration_Migration_Scenario","Graphics_Migration_Require_multi_tag_shapes?")
                setDefaultColumnForDropdown("Graphics_Migration_Migration_Scenario","Graphics_Migration_Require_multi_tag_shapes?","Yes")
    proposalType = Quote.GetCustomField("EGAP_Proposal_Type").Content
    if proposalType == "Budgetary":
        hideColumn("Graphics_Migration_Displays_Shapes_Faceplates", "Number_of_Repeats_Custom_Faceplates")
        hideColumn("Graphics_Migration_Displays_Shapes_Faceplates", "Number_of_Custom_Context_Menus")
        hideColumn("Graphics_Migration_Displays_Shapes_Faceplates", "Experion_shapes_multiplier")
    else:
        if getAttributeValue("MIgration_Scope_Choices") not in ["HW/SW"]:
            visibleColumn("Graphics_Migration_Displays_Shapes_Faceplates", "Number_of_Repeats_Custom_Faceplates")
            visibleColumn("Graphics_Migration_Displays_Shapes_Faceplates", "Number_of_Custom_Context_Menus")
            if isHidden("Graphics_Migration_Displays_Shapes_Faceplates", "Experion_shapes_multiplier"):
                visibleColumn("Graphics_Migration_Displays_Shapes_Faceplates", "Experion_shapes_multiplier")
                '''shapes_cont = getContainer('Graphics_Migration_Displays_Shapes_Faceplates')
                for r in shapes_cont.Rows:
                    r['Experion_shapes_multiplier'] = "1.0"
                shapes_cont.Calculate()'''
    if getAttributeValue("MIgration_Scope_Choices") in ["HW/SW"]:
        hideColumn("Graphics_Migration_Additional_Questions","Graphics_Migration_New_Safeview_Configuration")
    else:
        graphicscon1 = getContainer('Graphics_Migration_Additional_Questions')
        graphicsconrow1 = graphicscon1.Rows[0]
        if graphicsconrow1["Graphics_Migration_New_Safeview_Configuration"] in ("None",""):
            hideColumn("Graphics_Migration_Additional_Questions","Graphics_Migration_Alarm_groups_configured?")
            hideColumn("Graphics_Migration_Additional_Questions","Graphics_Migration_Number_of_station_licenses")
        else:
            if isHidden("Graphics_Migration_Additional_Questions","Graphics_Migration_Alarm_groups_configured?"):
                visibleColumn("Graphics_Migration_Additional_Questions", "Graphics_Migration_Alarm_groups_configured?")
                visibleColumn("Graphics_Migration_Additional_Questions", "Graphics_Migration_Number_of_station_licenses")
                setDefaultColumnForDropdown("Graphics_Migration_Additional_Questions","Graphics_Migration_Alarm_groups_configured?","No")


if 'XP10 Actuator Upgrade' in selectedProducts:
	if getAttributeValue("MIgration_Scope_Choices") in ["LABOR"]:
		hideColumn("XP10_Actuator_General_Information","XP10_Actuator_Will_an_A7_actuator_tool_be_needed")
	else:
		xp10con = getContainer('XP10_Actuator_General_Information')
		xp10conrow = xp10con.Rows[0]
		if xp10conrow["XP10_Actuator_Select_current_actuator_model"] in ("A5",""):
			hideColumn("XP10_Actuator_General_Information","XP10_Actuator_Will_an_A7_actuator_tool_be_needed")
		else:
			if isHidden("XP10_Actuator_General_Information","XP10_Actuator_Will_an_A7_actuator_tool_be_needed"):
				visibleColumn("XP10_Actuator_General_Information", "XP10_Actuator_Will_an_A7_actuator_tool_be_needed")
				setDefaultColumnForDropdown("XP10_Actuator_General_Information","XP10_Actuator_Will_an_A7_actuator_tool_be_needed","No")

if 'CD Actuator I-F Upgrade' in selectedProducts:
    cdact = getContainer('CD_Actuator_IF_Upgrade_General_Info_Cont')
    cdactrow = cdact.Rows[0]
    if cdactrow["CD_Actuator_QCS_Type"] in ("MXOpen" , "Performance CD Open Version 2 or older" , "Performance CD Open Version 3 or newer"):
        hideColumn("CD_Actuator_IF_Upgrade_General_Info_Cont","CD_Actuator_If_other_please_provide_information")
    else:
		if isHidden("CD_Actuator_IF_Upgrade_General_Info_Cont","CD_Actuator_If_other_please_provide_information"):
			visibleColumn("CD_Actuator_IF_Upgrade_General_Info_Cont","CD_Actuator_If_other_please_provide_information")

    if cdactrow["CD_Actuator_Actuator_Model"] not in ("Thermatrol (No Feedback)","Thermatrol (With Feedback)","Caltrol I or II (No Feedback)","Caltrol I or II (With Feedback)"):
        hideColumn("CD_Actuator_IF_Upgrade_General_Info_Cont","CD_Actuator_For_Caltrol_or_Thermatrol_Is_feedback")
    else:
        if isHidden("CD_Actuator_IF_Upgrade_General_Info_Cont","CD_Actuator_For_Caltrol_or_Thermatrol_Is_feedback"):
            visibleColumn("CD_Actuator_IF_Upgrade_General_Info_Cont","CD_Actuator_For_Caltrol_or_Thermatrol_Is_feedback")
            setDefaultColumnForDropdown("CD_Actuator_IF_Upgrade_General_Info_Cont","CD_Actuator_For_Caltrol_or_Thermatrol_Is_feedback","No")

    if cdactrow["CD_Actuator_Actuator_Model"] not in ("Aquatrol (24VDC solenoids)","Aquatrol (24VAC or 48VDC solenoids)"):
        hideColumn("CD_Actuator_IF_Upgrade_General_Info_Cont","CD_Actuator_For_Aquatrol_what_is_solenoid_voltage")
    else:
        if isHidden("CD_Actuator_IF_Upgrade_General_Info_Cont","CD_Actuator_For_Aquatrol_what_is_solenoid_voltage"):
            visibleColumn("CD_Actuator_IF_Upgrade_General_Info_Cont","CD_Actuator_For_Aquatrol_what_is_solenoid_voltage")


if 'EHPM/EHPMX/ C300PM' in selectedProducts:
    xPMMigrationScenarioCont =  getContainer('xPM_Migration_Scenario_Cont')
    xPMNetworkUpgradeCont = getContainer('xPM_Network_Upgrade_Cont')
    xPMGenQuCont = getContainer('xPM_Migration_General_Qns_Cont')
    requireFiberCommunication = ''
    rowMigrationScenario = xPMMigrationScenarioCont.Rows[0]
    rowNetworkUpgrade = xPMNetworkUpgradeCont.Rows[0]
    rowGenQues = xPMGenQuCont.Rows[0]
    for col in rowNetworkUpgrade.Columns:
        if col.Name == "xPM_Customer_requires_Fiber_Communication":
            requireFiberCommunication = getValue(rowNetworkUpgrade,col)
    migrationScenario = rowMigrationScenario['xPM_Select_the_migration_scenario']
    epks=rowGenQues['xPM_EPKS_SW_Release_at_time_of_xPM_migration']

    if getAttributeValue("MIgration_Scope_Choices") in ["LABOR"] or migrationScenario == 'xPM to EHPM':
        hideColumn("xPM_Migration_General_Qns_Cont", "xPM_Experion_Server_Redundancy")
        Product.GetContainerByName("xPM_Migration_General_Qns_Cont").Rows[0]['xPM_Experion_Server_Redundancy'] = ''
    else:
        visibleColumn("xPM_Migration_General_Qns_Cont", "xPM_Experion_Server_Redundancy")
        if not Product.GetContainerByName("xPM_Migration_General_Qns_Cont").Rows[0]['xPM_Experion_Server_Redundancy']:
            Product.GetContainerByName("xPM_Migration_General_Qns_Cont").Rows[0]['xPM_Experion_Server_Redundancy'] = 'Redundant'
    if migrationScenario == 'xPM to EHPM':
        hideColumn("xPM_Migration_General_Qns_Cont", "xPM_On_Process_Red_HPMs_EHPMs_only")
        hideColumn("xPM_Migration_Config_Cont", "xPM_Number_of_Red_EHPM_Exp_connected_wo_config")
        hideColumn("xPM_Migration_Config_Cont", "xPM_Number_of_Red_EHPM_Non_Exp_connected")
        hideColumn("xPM_Network_Upgrade_Cont", "xPM_Qty_Additional_Red_pair_of_CF9_firewalls")
        hideColumn("xPM_Migration_Config_Cont", "xPM_CE_Mark_or_Not")
        hideColumn("xPM_Migration_Config_Cont", "xPM_Number_of_HLAI_with_FW_Rev")
        hideColumn("xPM_Migration_Config_Cont", "xPM_Number_of_AO16_with_FW_Rev_2.0")
        hideColumn("xPM_Migration_Config_Cont", "xPM_Number_of_DI/DI24_with_FW_Rev_5.0")
        hideColumn("xPM_Migration_Config_Cont", "xPM_Number_of_DO16_with_FW_Rev_4.3")
        hideColumn("xPM_Migration_Config_Cont", "xPM_Number_of_DO32_with_FW_Rev_4.3")
    else:
        visibleColumn("xPM_Migration_General_Qns_Cont", "xPM_On_Process_Red_HPMs_EHPMs_only")
        visibleColumn("xPM_Migration_Config_Cont", "xPM_Number_of_Red_EHPM_Exp_connected_wo_config")
        visibleColumn("xPM_Migration_Config_Cont","xPM_Number_of_Red_EHPM_Non_Exp_connected")
        visibleColumn("xPM_Migration_Config_Cont", "xPM_Number_of_HLAI_with_FW_Rev")
        visibleColumn("xPM_Migration_Config_Cont", "xPM_Number_of_AO16_with_FW_Rev_2.0")
        visibleColumn("xPM_Migration_Config_Cont", "xPM_Number_of_DI/DI24_with_FW_Rev_5.0")
        visibleColumn("xPM_Migration_Config_Cont", "xPM_Number_of_DO16_with_FW_Rev_4.3")
        visibleColumn("xPM_Migration_Config_Cont", "xPM_Number_of_DO32_with_FW_Rev_4.3")
    if migrationScenario == 'xPM to C300PM':
        hideColumn("xPM_Migration_Config_Cont", "xPM_CE_Mark_or_Not")
        hideColumn("xPM_Network_Upgrade_Cont", "xPM_Qty_of_Red_pair_of_CF9_firewalls")

    if migrationScenario in['xPM to C300PM','xPM to EHPMX']:
        hideColumn("xPM_Migration_General_Qns_Cont", "xPM_On_Process_Red_HPMs_or_Off_Process_Migration")
        hideColumn("xPM_Migration_Config_Cont", "xPM_How_many_EHPMs_will_require_Exp_conn")
    else:
        visibleColumn("xPM_Migration_General_Qns_Cont","xPM_On_Process_Red_HPMs_or_Off_Process_Migration")
        visibleColumn("xPM_Migration_Config_Cont","xPM_How_many_EHPMs_will_require_Exp_conn")
    if migrationScenario in['xPM to EHPM','xPM to EHPMX']:
        hideColumn("xPM_Migration_General_Qns_Cont", "xPM_On_Process_Red_HPMs_EHPMs_only")
        hideColumn("xPM_Migration_Config_Cont", "xPM_Controller_need_Experion_peer_to_peer_connectivity")
    else:
        visibleColumn("xPM_Migration_General_Qns_Cont","xPM_On_Process_Red_HPMs_EHPMs_only")
        visibleColumn("xPM_Migration_Config_Cont","xPM_Controller_need_Experion_peer_to_peer_connectivity")
    if migrationScenario in['xPM to EHPM','xPM to C300PM']:
        hideColumn("xPM_Migration_General_Qns_Cont", "xPM_On_Process_Red_HPMs_EHPMs_for_EHPMX_mig")
        hideColumn("xPM_Migration_Config_Cont", "xPM_EHPMX_need_Experion_peer_to_peer_connectivity")
    else:
        visibleColumn("xPM_Migration_General_Qns_Cont","xPM_On_Process_Red_HPMs_EHPMs_for_EHPMX_mig")
        visibleColumn("xPM_Migration_Config_Cont","xPM_EHPMX_need_Experion_peer_to_peer_connectivity")
    if migrationScenario in['xPM to EHPM','xPM to EHPMX'] or epks == 'None' :
        hideColumn("xPM_Migration_Config_Cont","xPM_Number_of_xPM_Points_including_SI")
    else:
        visibleColumn("xPM_Migration_Config_Cont","xPM_Number_of_xPM_Points_including_SI")

    if getAttributeValue("MIgration_Scope_Choices") in ["LABOR"]:
        hideColumn("xPM_Migration_Config_Cont", "xPM_CE_Mark_or_Not")
        hideColumn("xPM_Migration_Config_Cont", "xPM_Number_of_xPM_Points_including_SI")
        hideColumn("ENB_Migration_Config_Cont", "xPM_ENB_CE_Mark_or_Not")
        hideColumn("ENB_Migration_Config_Cont", "xPM_What_is_the_NIM_migration_scenario")
        hideColumn("ENB_Migration_Config_Cont", "xPM_Does_the_customer_have_K4_processor_boards")
        hideColumn("xPM_Network_Upgrade_Cont", "xPM_Customer_requires_Fiber_Communication")
        hideColumn("xPM_Network_Upgrade_Cont", "xPM_Distance_of_Fiber_Optic_Extenders")
        hideColumn("xPM_Network_Upgrade_Cont", "xPM_Qty_of_Red_pair_of_CF9_firewalls")
        hideColumn("xPM_Network_Upgrade_Cont", "xPM_Qty_Additional_Red_pair_of_CF9_firewalls")
        hideColumn("xPM_Network_Upgrade_Cont", "xPM_Qty_of_FTE_Networks_kits")
    else:
        if migrationScenario != 'xPM to EHPM':
            visibleColumn("xPM_Network_Upgrade_Cont", "xPM_Qty_Additional_Red_pair_of_CF9_firewalls")
        if migrationScenario == 'xPM to C300PM':
            visibleColumn("xPM_Migration_Config_Cont", "xPM_Number_of_xPM_Points_including_SI")
        visibleColumn("ENB_Migration_Config_Cont", "xPM_ENB_CE_Mark_or_Not")
        visibleColumn("ENB_Migration_Config_Cont", "xPM_What_is_the_NIM_migration_scenario")
        visibleColumn("ENB_Migration_Config_Cont", "xPM_Does_the_customer_have_K4_processor_boards")
        visibleColumn("xPM_Network_Upgrade_Cont", "xPM_Customer_requires_Fiber_Communication")
        if isHidden("xPM_Network_Upgrade_Cont","xPM_Distance_of_Fiber_Optic_Extenders"):
            visibleColumn("xPM_Network_Upgrade_Cont", "xPM_Distance_of_Fiber_Optic_Extenders")
            setDefaultValue("xPM_Network_Upgrade_Cont","xPM_Distance_of_Fiber_Optic_Extenders")
        if migrationScenario != 'xPM to C300PM':
            visibleColumn("xPM_Network_Upgrade_Cont", "xPM_Qty_of_Red_pair_of_CF9_firewalls")
            visibleColumn("xPM_Migration_Config_Cont", "xPM_CE_Mark_or_Not")
            hideColumn("xPM_Migration_Config_Cont", "xPM_CE_Mark_or_Not")
        visibleColumn("xPM_Network_Upgrade_Cont", "xPM_Qty_of_FTE_Networks_kits")
    if getAttributeValue("MIgration_Scope_Choices") in ["HW/SW"]:
        hideColumn("xPM_Migration_Config_Cont", "xPM_Number_of_Red_EHPM_Exp_connected_wo_config")
        hideColumn("xPM_Migration_Config_Cont", "xPM_Number_of_Red_EHPM_Non_Exp_connected")
        hideColumn("xPM_Services_Cont", "xPM_Which_documentation_is_required")
        Product.DisallowAttr("xPM_Which_documentation_is_required")
        hideColumn("xPM_Services_Cont", "xPM_Factory_Acceptance_Test_Required")
        hideColumn("xPM_Services_Cont", "MSID_Will_Honeywell_perform_equipment_installation")
    else:
        if migrationScenario != 'xPM to EHPM':
            visibleColumn("xPM_Migration_Config_Cont", "xPM_Number_of_Red_EHPM_Exp_connected_wo_config")
            visibleColumn("xPM_Migration_Config_Cont", "xPM_Number_of_Red_EHPM_Non_Exp_connected")
        visibleColumn("xPM_Services_Cont", "xPM_Which_documentation_is_required")
        Product.AllowAttr("xPM_Which_documentation_is_required")
        visibleColumn("xPM_Services_Cont", "xPM_Factory_Acceptance_Test_Required")
        hideColumn("xPM_Migration_Config_Cont", "xPM_CE_Mark_or_Not")
    if getAttributeValue("MIgration_Scope_Choices") not in ["LABOR"]:
    	if requireFiberCommunication in ('No - Quote IE3000+ Switch Pair with 16 Cu ports 1ea NE-ZFTEB2', 'No - Quote 9200L 24ports Switch Pair 2ea SI-920LN4'):
        	hideColumn("xPM_Network_Upgrade_Cont","xPM_Distance_of_Fiber_Optic_Extenders")
    	elif isHidden("xPM_Network_Upgrade_Cont","xPM_Distance_of_Fiber_Optic_Extenders"):
        	Trace.Write("Visibility Check")
        	visibleColumn("xPM_Network_Upgrade_Cont","xPM_Distance_of_Fiber_Optic_Extenders")
        	setDefaultValue("xPM_Network_Upgrade_Cont","xPM_Distance_of_Fiber_Optic_Extenders")