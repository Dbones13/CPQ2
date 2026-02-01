def getContainer(Name):
    return Product.GetContainerByName(Name)

GraphicsMigrationScenario = getContainer('Graphics_Migration_Migration_Scenario')
colValuesDict = {"Graphics_Migration_Select_Vertical_Market_Picklist_with_values": "Oil and Gas", "Graphics_Migration_Type_of_Existing_Displays": "Existing US Graphics"}
for row in GraphicsMigrationScenario.Rows:
    for col in row.Columns:
        defaultVal = colValuesDict.get(col.Name)
        if defaultVal:
            col.SetAttributeValue(defaultVal)
            row.SetColumnValue(col.Name,defaultVal)
	row.SetColumnValue('Graphics_Migration_For_existing_US_GUS_DSP_what_percentage_of_Standard_Builds_will_be_used?','100')

GraphicsMigrationScenario.Calculate()

GraphicsMigrationTraining = getContainer('Graphics_Migration_Training_Testing_Documentation')
colValuesDict = {"Graphics_Migration_FAT_required?": "No", "Graphics_Migration_Does_the_customer_require_SAT?": "No", "Graphics_Migration_Does_the_customer_require_Operator_Training_Basic?": "No", "Graphics_Migration_FDS_Required?": "No", "Graphics_Migration_DDS_Required?":"No"}
for row in GraphicsMigrationTraining.Rows:
    for col in row.Columns:
        defaultVal = colValuesDict.get(col.Name)
        if defaultVal:
            col.SetAttributeValue(defaultVal)
            row.SetColumnValue(col.Name,defaultVal)
GraphicsMigrationTraining.Calculate()

GraphicsMigrationAddlQue = getContainer('Graphics_Migration_Additional_Questions')
colValuesDict = {"Graphics_Migration_Gap_Analysis_done?": "No", "Graphics_Migration_For_GAP_Analysis_project_com": "No limitation to use GES", "Graphics_Migration_DCA_IRA_done": "No", "Graphics_Migration_New_Safeview_Configuration": "None", "Graphics_Migration_Alarm_groups_configured?": "No","Graphics_Migration_For_GAP_Analysis_project_com":"No limitation to use GES" }
for row in GraphicsMigrationAddlQue.Rows:
    for col in row.Columns:
        defaultVal = colValuesDict.get(col.Name)
        if defaultVal:
            col.SetAttributeValue(defaultVal)
            row.SetColumnValue(col.Name,defaultVal)
GraphicsMigrationAddlQue.Calculate()

GraphicsMigrationDisplyShape = getContainer('Graphics_Migration_Displays_Shapes_Faceplates')
colValuesDict = {"Experion_shapes_multiplier": "1.0"}
for row in GraphicsMigrationDisplyShape.Rows:
    for col in row.Columns:
        defaultVal = colValuesDict.get(col.Name)
        if defaultVal:
            row[col.Name] = defaultVal
GraphicsMigrationDisplyShape.Calculate()

xP10GenQue = getContainer('XP10_Actuator_General_Information')
colValuesDict = {"XP10_Actuator_Select_current_actuator_model":"A5","XP10_Actuator_Select_current_valve_plug_model":"A","XP10_Actuator_Will_a_seat_removal_tool_be_needed":"Yes", "XP10_Actuator_XP10_seat_adapter_tool_be_needed":"Yes", "XP10_Actuator_XP10_adapter_tool_be_needed":"Yes"}
for row in xP10GenQue.Rows:
    for col in row.Columns:
        defaultVal = colValuesDict.get(col.Name)
        if defaultVal:
            col.SetAttributeValue(defaultVal)
            row.SetColumnValue(col.Name,defaultVal)
xP10GenQue.Calculate()

cd_actuator_ser_cont = getContainer('CD_Actuator_IF_Upgrade_Services_Cont')
colValuesDict = {"CD_Actuator_HSE_and_Quality_Plan_required":"No","CD_Actuator_Update_existing_documents":"No","CD_Actuator_SAT_required":"No"}
for row in cd_actuator_ser_cont.Rows:
    for col in row.Columns:
        defaultVal = colValuesDict.get(col.Name)
        if defaultVal:
            col.SetAttributeValue(defaultVal)
            row.SetColumnValue(col.Name,defaultVal)
cd_actuator_ser_cont.Calculate()


cd_actuator_gen_cont = getContainer('CD_Actuator_IF_Upgrade_General_Info_Cont')
colValuesDict = {"CD_Actuator_Actuator_Type":"Non-Intelligent Actuator", "CD_Actuator_Actuator_Model":"Aqualizer", "CD_Actuator_Processor_Type":"EPC6", "CD_Actuator_Interlocks":"None","CD_Actuator_Will_the_current_Interlocks_be":"None","CD_Actuator_Interlock_Voltage":"24 VDC","CD_Actuator_Line_Voltage_Single_Phase_Supply_Voltage":"120 VAC","CD_Actuator_QCS_Type":"Performance CD Open Version 3 or newer","CD_Actuator_Lynk_Type":"LON","CD_Actuator_For_Aquatrol_what_is_solenoid_voltage":"24 VDC","CD_Actuator_For_Caltrol_or_Thermatrol_Is_feedback": "No"}
for row in cd_actuator_gen_cont.Rows:
    for col in row.Columns:
        defaultVal = colValuesDict.get(col.Name)
        if defaultVal:
            col.SetAttributeValue(defaultVal)
            row.SetColumnValue(col.Name,defaultVal)
    row.SetColumnValue('CD_Actuator_Line_Voltage_Three_Phase_Supply_Voltage','480')
    row.SetColumnValue('CD_Actuator_Existing_sets_of_extra_edge_actuators','0')
cd_actuator_gen_cont.Calculate()

cdactuatorPricing = getContainer('CD_Actuator_pricing_factory_cost')
for row in cdactuatorPricing.Rows:
    if row.RowIndex > 1:
        break
    row['CD_Actuator_Special_Special_or_iLon_upgrade_pricing'] = '0'
cdactuatorPricing.Calculate()
