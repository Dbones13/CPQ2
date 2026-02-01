import clr
import sys
import System
clr.AddReference("System.Core")
clr.ImportExtensions(System.Linq)
def getContainer(containerName):
     return Product.GetContainerByName(containerName)
def getFloat(Var):
    if Var:
        return float(Var)
    return 0

def getAttributeValue(Name):
    return Product.Attr(Name).GetValue()

def setAttrValue(Name,value):
    Product.Attr(Name).AssignValue(value)

def isVisible(container,Column):
    return Product.ParseString('<*CTX( Container({}).Column({}).GetPermission )*>'.format(container,Column)) == 'Editable'

def getContainerColSum(containerName , rowId):
    container = getContainer(containerName)
    sum = 0
    for row in container.Rows:
        if row.RowIndex == rowId:
            for col in row.Columns:
                try:
                    sum += float(row[col.Name])
                except:
                    pass
    return sum > 0

selectedScope = Product.Attr('MIgration_Scope_Choices').GetValue()
messageFields = []
setAttrValue("Genral_Input_Message",'')
container = "MSID_CommonQuestions"
commonQue = getContainer(container)
for row in commonQue.Rows:
    for col in row.Columns:
        if isVisible(container,col.Name) and col.DisplayValue == 'None':
            if col.HeaderLabel not in messageFields:
                messageFields.append(col.HeaderLabel)
    break

def getmessageFields(attributs,messageFields):
    for attr in attributs:
        if attr.Allowed:
            if attr.GetValue() == '':
                if attr.GetLabel() not in messageFields:
                    messageFields.append(attr.GetLabel())
    return messageFields

activeAttr = Product.Attr('MSID_Active_Service_Contract')
gesLocationAttr = Product.Attr('MSID_GES_Location')
messageFields = getmessageFields([activeAttr,gesLocationAttr],messageFields)

producttMsg = ''
#Trace.Write(str(messageFields))
if len(messageFields) > 0:
    producttMsg = "Please select '{}' on General input tab".format("','".join(messageFields))
#Trace.Write(producttMsg)
if producttMsg:
    setAttrValue("Genral_Input_Message",producttMsg)

opmBasic = getContainer("OPM_Basic_Information")
row = opmBasic.Rows[0]
hwReplaceNeeded = row["OPM_Servers_and_Stations_HW_replace_needed"] == 'Yes' and Product.Attr('MIgration_Scope_Choices').GetValue() != "LABOR"

selectedProducts = Product.Attr('MSID_Selected_Products').GetValue().split('<br>')
incomplete = []
if "OPM" in selectedProducts:
    if not getContainerColSum("OPM_Node_Configuration" , 0):
        incomplete.append("OPM_Node_Configuration")
    if hwReplaceNeeded:
        if not getContainerColSum("OPM_Node_Configuration" , 2):
            incomplete.append("OPMNode_Configuration_HW")
if "Non-SESP Exp Upgrade" in selectedProducts:
    if not getContainerColSum("NONSESP_Design_Inputs_for_Experion_Upgrade_License" , 0):
        incomplete.append("NONSESP_Design_Inputs_for_Experion_Upgrade_License")
if "LCN One Time Upgrade" in selectedProducts:
    if not getContainerColSum("LCN_Design_Inputs_for_TPN_OTU_Upgrade" , 0):
        incomplete.append("LCN_Design_Inputs_for_TPN_OTU_Upgrade")

if 'ELCN' in selectedProducts:
    elcnUpgradeNewElcnNodesCon =  getContainer('ELCN_Upgrade_New_ELCN_Nodes')
    totalQtyOfNetworkGateway = 0
    rowAssetDB = 2
    rowIndex = 0
    '''Sum of Upgrade Physical, Virtual, New Physical, and Virtual Quantities'''
    for row in elcnUpgradeNewElcnNodesCon.Rows:
        if rowIndex != rowAssetDB:
            for column in row.Columns:
                if row[column.Name] != '':
                    totalQtyOfNetworkGateway += int(row[column.Name])
        rowIndex += 1
    if totalQtyOfNetworkGateway == 0:
        incomplete.append("ELCN_Nodes")

if 'EHPM/EHPMX/ C300PM' in selectedProducts:
    xPMMigrationGeneralQnsCont =  getContainer('xPM_Migration_General_Qns_Cont')
    ENBMigrationGeneralQnsCont =  getContainer('ENB_Migration_General_Qns_Cont')
    xPMMigrationConfigCont =  getContainer('xPM_Migration_Config_Cont')
    ENBMigrationConfigCont = getContainer('ENB_Migration_Config_Cont')
    xPMMigrationScenarioCont = getContainer('xPM_Migration_Scenario_Cont')
    row1 = xPMMigrationGeneralQnsCont.Rows[0]
    row2 = ENBMigrationGeneralQnsCont.Rows[0]
    row3 = xPMMigrationScenarioCont.Rows[0]
    xPMMigrations = xPMMigrations = int(row1['xPM_How_many_xPMs_configurations_are_we_migrating']) if  row1['xPM_How_many_xPMs_configurations_are_we_migrating'].strip() != '' else 0
    NIMMigrations = int(row2['xPM_Number_of_NIMs_configurations_to_be_migrated']) if row2['xPM_Number_of_NIMs_configurations_to_be_migrated'].strip() != '' else 0
    tpnRelease = row1["xPM_TPN_SW_Release_at_time_of_xPM_migration"]
    epksRelease = row1["xPM_EPKS_SW_Release_at_time_of_xPM_migration"]
    if tpnRelease == '-':
        incomplete.append("xpm_select_tpn")
    if epksRelease == '-':
        incomplete.append("xpm_select_epks")
    if (xPMMigrations + NIMMigrations) <= 0:
        incomplete.append("How_many_xPMs")
    else:
        noOfConfigInValid = False
        totalNoOfIncludedSi = False
        peertopeer = False
        if xPMMigrations > 0:
            for row in xPMMigrationConfigCont.Rows:
                noOfConfigs = int(row['xPM_Number_of_xPMs_in_this_config']) if  row['xPM_Number_of_xPMs_in_this_config'].strip() != '' else 0
                if row['xPM_Number_of_xPM_Points_including_SI'].strip() in ('',"0",0):
                    totalNoOfIncludedSi = True
                if noOfConfigs <= 0:
                    noOfConfigInValid = True
                else:
                    if getFloat(row["xPM_EHPMX_need_Experion_peer_to_peer_connectivity"]) > noOfConfigs or getFloat(row["xPM_Controller_need_Experion_peer_to_peer_connectivity"])> noOfConfigs or getFloat(row["xPM_How_many_EHPMs_will_require_Exp_conn"] )> noOfConfigs:
                        peertopeer = True

            if noOfConfigInValid:
                incomplete.append("No_of_xPMs")
            if totalNoOfIncludedSi and row3["xPM_Select_the_migration_scenario"] == "xPM to C300PM" and selectedScope != "LABOR":
                incomplete.append("No_of_included_si")
            if peertopeer:
                incomplete.append("EHPM_peertopeer")
        if NIMMigrations > 0:
            isInvalid = False
            networkUpgradeCon = getContainer('xPM_Network_Upgrade_Cont')
            fteCount = int(networkUpgradeCon.Rows[0]['xPM_Qty_of_FTE_Networks_kits']) if networkUpgradeCon.Rows[0]['xPM_Qty_of_FTE_Networks_kits'] else 0
            if fteCount <= 0 and selectedScope != "LABOR":
                incomplete.append("xPM_fte_input")
            for row in ENBMigrationConfigCont.Rows:
                noOfConfigs = int(row['xPM_Number_of_NIMs_in_this_config']) if  row['xPM_Number_of_NIMs_in_this_config'].strip() != '' else 0
                if noOfConfigs <= 0:
                    isInvalid = True
                    break
            if isInvalid:
                incomplete.append("No_of_NIMs")

if 'TPS to Experion' in selectedProducts:
    monitors = getContainer('TPS_EX_Monitors')
    bundle = getContainer('TPS_EX_Bundle_Conversion_Server_Stations')
    est =  getContainer('TPS_EX_Station_Conversion_EST')
    esvt = getContainer("TPS_EX_Conversion_ESVT_Server")
    for row in monitors.Rows:
        for col in row.Columns:
            if row[col.Name] and float(row[col.Name]) > 0:
                break
            incomplete.append("TPSmonitorValidation")
            break
        break
    '''checkQty = True
    sum = 0
    for row in bundle.Rows:
        if row["TPS_EX_Non_Reduntant_Conversion_ESVT"] == "Yes" or row["TPS_EX_Redundant_Conversion_ESVT"] == "Yes":
            checkQty = False
        break
    if checkQty:
        sum = getContainerColSum("TPS_EX_Conversion_ESVT_Server" , 0)
        for row in est.Rows:
            try:
                sum += float(row["Quantity"])
            except:
                pass
        if sum <= 0:'''
    estCon = getContainer("TPS_EX_Station_Conversion_EST")
    AcetCon = getContainer("TPS_EX_Conversion_ACET_EAPP")
    acet = 0
    for row in estCon.Rows:
        acet += getFloat(row["TPS_EX_Quantity"])
    for row in AcetCon.Rows:
        #Trace.Write(row["TPS_EX_Conversion_ACET_EAPP_Qty"])
        acet += getFloat(row["TPS_EX_Conversion_ACET_EAPP_Qty"])
    if not getContainerColSum("TPS_EX_Station_Conversion_EST" , 0):
        if acet <= 0:
            if not getContainerColSum("TPS_EX_Conversion_ESVT_Server",0):
                    incomplete.append("TPSserverValidation")
    qty1 = 0
    qty2 = 0
    for row in bundle.Rows:
        if row["TPS_EX_Non_Reduntant_Conversion_ESVT"] == "YES" or row["TPS_EX_Redundant_Conversion_ESVT"] == "YES":
            #Trace.Write(row["TPS_EX_Non_Reduntant_Conversion_ESVT"])
            qty1 += 1
            #Trace.Write(qty1)
        break
    for row in esvt.Rows:
        for col in row.Columns:
            if col.Name in ["TPS_EX_TDC_US_ESVT","TPS_EX_TDC_AM_ESVT","TPS_EX_TDC_APP_ESVT","TPS_EX_TDC_GUS_ESVT","TPS_EX_ESVT_WO_Trade_Ins"]:
                #Trace.Write(col.Value)
                qty2 += getFloat(col.Value)
        break
    esvt_qty = qty1 + qty2
    if esvt_qty > 5:
        incomplete.append("ESVT_msg")

if 'EHPM HART IO' in selectedProducts:	#EHPM HART IO validation
    EHPMHARTIOGeneralQnsCont =  getContainer('EHPM_HART_IO_General_Qns_Cont')
    EHPMHARTIOServicesCont =  getContainer('EHPM_HART_IO_Services_Cont')
    EHPMHARTIOConfigCont = getContainer('EHPM_HART_IO_Configuration_Cont')
    row1 = EHPMHARTIOGeneralQnsCont.Rows[0]
    row2 = EHPMHARTIOServicesCont.Rows[0]
    #row3 = EHPMHARTIOConfigCont.Rows[0]
    #row4 = EHPMHARTIOConfigCont.Rows[1]
    numberofins = 0
    sumOfIoConfig = 0

    for row in EHPMHARTIOConfigCont.Rows:
        for column in row.Columns:
            if row[column.Name] not in ('',"0"):
                sumOfIoConfig = int(row[column.Name])

    cxrRelease = row1["Current_Experion_Release"]
    tpnRelease = row1["Current_TPN_Release"]
    if cxrRelease == '-':
        incomplete.append("Current_Experion_Release")
    if tpnRelease == '-':
        incomplete.append("Current_TPN_Release")
    if getAttributeValue("MIgration_Scope_Choices") in ["LABOR", "HW/SW/LABOR"]:
        numberofins = int(row2["Number_of_EHPM_where_HART_IO_will_be_installed"])
        if numberofins <= 0:
            incomplete.append("Number_of_EHPM_where_HART_IO_will_be_installed")
    if sumOfIoConfig <= 0:
        incomplete.append("Number_of_Non_Redundant_HART_HLAI")

if 'CB-EC Upgrade to C300-UHIO' in selectedProducts:		#CB-EC
    CBECConfigCont = getContainer('CB_EC_migration_to_C300_UHIO_Configuration_Cont')
    row1=CBECConfigCont.Rows[0]
    sumOfCBAndEC=int(row1["CB_EC_How_many_CBs_are_being_migrated"])+int(row1["CB_EC_How_many_ECs_are_being_migrated"])
    if(sumOfCBAndEC) < 2:
        incomplete.append("Sum_of_CB_And_EC")

c200MigrationgeneralQns = getContainer('C200_Migration_General_Qns_Cont')
c200migrationScenario = getContainer('C200_Migration_Scenario_Cont')
c200Configurations = getContainer('C200_Migration_Config_Cont')
try:
    scope = Product.Attr('MSID_Scope').SelectedValue.Display
except:
    pass
if "C200 Migration" in selectedProducts:
    rowMigScenario = c200migrationScenario.Rows[0]
    rowsGQns = c200MigrationgeneralQns.Rows[0]
    rowsConfig = c200Configurations.Rows
    rowScenario = rowMigScenario['C200_Select_the_Migration_Scenario']
    rowC200Migrations = rowsGQns['C200_How_many_C200s_are_we_migrating']
    rowC200Colocated = rowsGQns['C200_How_many_co_located_C200_groups_exists']
    for configrow in rowsConfig:
        rowPMIOMs = configrow['C200_Number_of_PM_IOMs']
        row1756IOMs = configrow['C200_Number_of_1756_IOMs']
        rowABIOMs = configrow['C200_Number_of_Serial_Interface_Allen_Bradley_IOMs']
        rowABPoints = configrow['C200_Number_of_Serial_Interface_Allen_Bradley_points']
        rowModbusIOMs = configrow['C200_Number_of_Serial_Interface_Modbus_IOMs']
        rowModbusPoints = configrow['C200_Number_of_Serial_Interface_Modbus_points']
        rowSIIOMs = configrow['C200_Number_of_Serial_Interface_IOMs']
        rowSIPoints = configrow['C200_Number_of_Serial_Interface_points']
        #rowModbusIOMs = configrow['C200_Number_of_Serial_Interface_Modbus_IOMs']
        rowAIORacks = configrow['C200_C300_Number_of_Series_A_IO_Racks']
        if (rowPMIOMs == '0' or rowPMIOMs == '') and (row1756IOMs == '0' or row1756IOMs == '') and (rowScenario == 'C200 to C300') and (scope == 'HWSW' or scope == 'HWSWLABOR'):
            incomplete.append("C200_Both_questions_PMIOMs_1756IOMs")
        '''if (row1756IOMs == '0' or row1756IOMs == '') and (rowScenario == 'C200 to C300') and (scope == 'HWSW' or scope == 'HWSWLABOR'):
            incomplete.append("C200_Both_questions_PMIOMs_1756IOMs")'''
        if (rowABIOMs > '0' and rowABIOMs != '' and rowABIOMs != '0') and (rowABPoints == '0' or rowABPoints == '') and (rowScenario == 'C200 to C300') and (scope == 'LABOR' or scope == 'HWSWLABOR'):
            incomplete.append("C200_Serial_Interface_Allen_Bradley")
        if (rowModbusIOMs > '0' and rowModbusIOMs != '' and rowModbusIOMs != '0') and (rowModbusPoints == '0' or rowModbusPoints == '') and (rowScenario == 'C200 to C300') and (scope == 'LABOR' or scope == 'HWSWLABOR'):
            incomplete.append("C200_Serial_Interface_Modbus")
        if (rowSIIOMs > '0' and rowSIIOMs != '' and rowSIIOMs != '0') and (rowSIPoints == '0' or rowSIPoints == '') and (rowScenario == 'C200 to ControlEdge UOC') and (rowScenario != 'C200 to C300') and (scope == 'LABOR' or scope == 'HWSWLABOR'): ###
            incomplete.append("C200_Serial_Interface")
        if (row1756IOMs > '0' and row1756IOMs != '' and row1756IOMs != '0') and (rowAIORacks == '0' or rowAIORacks == '') and (rowScenario == 'C200 to C300') and (scope == 'HWSW' or scope == 'HWSWLABOR'):
            incomplete.append("C200_A_IO_Racks")
    if rowC200Migrations == '0':
        incomplete.append("C200_How_many_C200s")
    if (rowC200Colocated == '0' or rowC200Colocated == '') and (rowScenario == 'C200 to ControlEdge UOC') and (scope == 'HWSW' or scope == 'HWSWLABOR'):
        incomplete.append("C200_How_many_Co_located")

if "CB-EC Upgrade to C300-UHIO" in selectedProducts:	#CB-EC Validation
    CBECConfigCont = getContainer('CB_EC_Services_1_Cont')
    row = CBECConfigCont.Rows[0]
    if (row["CB_EC_Total_Number_of_Analog_Input_points_HGAIN"] == '' or row["CB_EC_Total_Number_of_Analog_Input_points_HGAIN"] == "0") and (row["CB_EC_Total_Number_of_Analog_Output_points_HGAOT"] == '' or row["CB_EC_Total_Number_of_Analog_Output_points_HGAOT"] == "0") and (row["CB_EC_Total_Number_of_Regulatory_points_HGREG"] == '' or row["CB_EC_Total_Number_of_Regulatory_points_HGREG"] == "0") and (row["CB_EC_Total_Number_of_Digital_Input_points_HGDIN"] == '' or row["CB_EC_Total_Number_of_Digital_Input_points_HGDIN"] == "0") and (row["CB_EC_Total_Number_of_Digital_Output_points_HGDOT"] == '' or row["CB_EC_Total_Number_of_Digital_Output_points_HGDOT"] == "0") and (row["CB_EC_Total_Number_of_Digital_Composite_points_HGDCP"] == '' or row["CB_EC_Total_Number_of_Digital_Composite_points_HGDCP"] == "0") and (row["CB_EC_Total_Number_of_Cascade_Loop"] == '' or row["CB_EC_Total_Number_of_Cascade_Loop"] == "0") and (row["CB_EC_Total_Number_of_Complex_Loop"] == '' or row["CB_EC_Total_Number_of_Complex_Loop"] == "0") and (row["CB_EC_Total_Number_of_Aux_function"] == '' or row["CB_EC_Total_Number_of_Aux_function"] == "0") and row["CB_EC_Do_you_know_the_number_of AI_AO_Regulatory_points_DI_DO_and_Digital_Composite_points"] =="Yes":
		incomplete.append("CBEC_Services")

if 'xPM to C300 Migration' in selectedProducts:
    xpmC300GenQns = getContainer('xPM_C300_General_Qns_Cont')
    xpmC300Config = getContainer('xPM_C300_Migration_Configuration_Cont')
    xpmC300Services = getContainer('xPM_C300_Services_Cont')
    ###

    rowGenQnsMigrations = xpmC300GenQns.Rows[0]
    rowServices = xpmC300Services.Rows[0]
    rowConfig = xpmC300Config.Rows

    noOfMigrations = rowGenQnsMigrations['xPM_C300_Number_of_xPMs_to_be_Migrated_to_C300_with_PMIO']
    test = rowServices['xPM_C300_Number_of_AM_points']
    AM_ACE = 0
    AMPoints = 0
    if scope != 'HWSW':
        if rowServices['xPM_C300_Number_of_AM_migrating_to_ACE']:
            AM_ACE = int(rowServices['xPM_C300_Number_of_AM_migrating_to_ACE'])
    else:
        AM_ACE = 0
    if scope != 'HWSW':
        if rowServices['xPM_C300_Number_of_AM_points']:
            AMPoints = int(rowServices['xPM_C300_Number_of_AM_points'])
    else:
        AMPoints = 0

    if noOfMigrations == '0' or noOfMigrations == '':
        incomplete.append("xPMs_to_be_Migrated")
    if scope != 'HWSW' and AM_ACE > 0 and AMPoints <= 0:
        incomplete.append("AM_ACE_Points")
    for row in rowConfig:
        analogInputs = getFloat(row['xPM_C300_Number_of_xPM_Analog_Input_points'])
        analogOutputs = getFloat(row['xPM_C300_Number_of_xPM_Analog_Output_points'])
        digitalInputs = getFloat(row['xPM_C300_Number_of_xPM_Digital_Input_points'])
        digitalOutputs = getFloat(row['xPM_C300_Number_of_xPM_Digital_output_points'])
        analogInputs = getFloat(row['xPM_C300_Number_of_xPM_Analog_Input_points'])
        analogOutputs = getFloat(row['xPM_C300_Number_of_xPM_Analog_Output_points'])
        digitalInputs = getFloat(row['xPM_C300_Number_of_xPM_Digital_Input_points'])
        digitalOutputs = getFloat(row['xPM_C300_Number_of_xPM_Digital_output_points'])
        SerialInterfacePoints = getFloat(row['xPM_C300_Number_of_Serial_Interface_points_for_Scada_conversion'])
        devices_xpmSI = getFloat(row['xPM_C300_Number_of_devices_connected_to_xPM_SI_for_PCDI_conversion'])
        if scope != 'HWSW':
            SerialInterfaceModules = 0 if row['xPM_C300_Number_of_Serial_Interface_modules'] == "" else int(row['xPM_C300_Number_of_Serial_Interface_modules'])
        else:
            SerialInterfaceModules = 0
        if scope != 'HWSW':
            SI_AB_Modbus = 0 if row['xPM_C300_Number_of_SI_Modbus_and_Allen_Bradley_Rockwell_Array_points_for_PCDI_conversion'] == "" else int(row['xPM_C300_Number_of_SI_Modbus_and_Allen_Bradley_Rockwell_Array_points_for_PCDI_conversion'])
        else:
            SI_AB_Modbus = 0
        if scope != 'LABOR':
            xpmIOMs = 0 if row['xPM_C300_Number_of_xPM_IOMs'] == "" else int(row['xPM_C300_Number_of_xPM_IOMs'])
        else:
            xpmIOMs = 0
        totalPoints1 = analogInputs + analogOutputs + digitalInputs + digitalOutputs
        totalPoints2 = SerialInterfacePoints + SI_AB_Modbus
        totalPoints3 = SerialInterfacePoints + devices_xpmSI + SI_AB_Modbus
        #if totalPoints1 == 0:
        if ((row['xPM_C300_Number_of_xPM_Analog_Input_points'] == '0' or row['xPM_C300_Number_of_xPM_Analog_Input_points'] == '') and (row['xPM_C300_Number_of_xPM_Analog_Output_points'] == '0' or row['xPM_C300_Number_of_xPM_Analog_Output_points'] == '') and (row['xPM_C300_Number_of_xPM_Digital_Input_points'] == '0' or row['xPM_C300_Number_of_xPM_Digital_Input_points'] == '') and (row['xPM_C300_Number_of_xPM_Digital_output_points'] == '0' or row['xPM_C300_Number_of_xPM_Digital_output_points'] == '')) or totalPoints1 == 0:
            incomplete.append("2ndValidation")
        if totalPoints1 + totalPoints2 > 45000:
            incomplete.append("3rdValidation")
        if xpmIOMs <= 0 and scope != 'LABOR':
            incomplete.append("xpm_IOMs")
        if SerialInterfaceModules > 0 and totalPoints3 <= 0 and scope != 'HWSW':
            incomplete.append("5thValidation")
if 'LM to ELMM ControlEdge PLC' in selectedProducts:
    lmToELMM3Party = getContainer('LM_to_ELMM_3rd_Party_Items')
    row = lmToELMM3Party.Rows
    for col in lmToELMM3Party.Properties:
        col_name = col.Name.split('|')[0]
        if row.Count > 0:
            if (float(row[0][col_name] if row[0][col_name] != '' else 0 ) > 0  and (float(row[1][col_name] if row[1][col_name] != '' else 0) == 0 or row[2][col_name] == '')) or (float(row[1][col_name] if row[1][col_name] != '' else 0 ) > 0  and (float(row[0][col_name] if row[0][col_name] != '' else 0) == 1 or row[2][col_name] == '')):
                incomplete.append("LMThirdPatryWriteIn")
    qtyLMPair = 0
    lmToELMMGenCont = getContainer('LM_to_ELMM_ControlEdge_PLC_Migration_Gen_Cont')
    for r in lmToELMMGenCont.Rows:
        if r['LM_Qty_Of_LM_Pair_To_Be_Migrated'] == '' or (r['LM_Qty_Of_LM_Pair_To_Be_Migrated']).ToString() == "0":
            incomplete.append("QtyOfLMPair")
        else:
            qtyLMPair = 1
        if int(r['LM_Number_Of_Additional_Switches'] if r['LM_Number_Of_Additional_Switches'] != "" else 0) >0 and (r['LM_Additional_Switch_Selection'] == "None" or r['LM_Additional_Switch_Selection'] == ""):
            incomplete.append("AdditionalSwitchValidation")
    lmToELMMAdditionalIOCont = getContainer('LM_to_ELMM_Migration_Additional_IO_Cont')
    for r in lmToELMMAdditionalIOCont.Rows:
        if (r['qty_IO_points_to_be_rewired_0_5000'] == '' or str(r['qty_IO_points_to_be_rewired_0_5000']) == "0") and selectedScope != 'HW/SW':
            incomplete.append("QtyOfIORewired")
    con2 = getContainer("LM_to_ELMM_ControlEdge_PLC_Cont")
    lmLocalIO = getContainer("LM_to_ELMM_ControlEdge_PLC_Local_IO_Cont")
    lmRemoteIO = getContainer("LM_to_ELMM_ControlEdge_PLC_Remote_IO_Cont")

    for row in con2.Rows:
        if qtyLMPair == 0:
            break
        if row['LM_are_the_IO_Racks_remotely_located'] == 'Yes - Only Remote' and row.RowIndex <= lmRemoteIO.Rows.Count -1:
            row_remote = sum(lmRemoteIO.Rows[row.RowIndex].Columns.ToList().Where(lambda y: y.Name != 'total_remote_serial_IO_racks_0_16' and y.Name != 'no_of_PLC_Remote_IO_group_0_16').Select(lambda c: int(c.Value if c.Value != '' else 0)))
            row_plc_remote_io = sum(lmRemoteIO.Rows[row.RowIndex].Columns.ToList().Where(lambda y: y.Name == 'no_of_PLC_Remote_IO_group_0_16').Select(lambda c: int(c.Value if c.Value != '' else 0)))
            row_total_remote_serial_io = sum(lmRemoteIO.Rows[row.RowIndex].Columns.ToList().Where(lambda y: y.Name == 'total_remote_serial_IO_racks_0_16').Select(lambda c: int(c.Value if c.Value != '' else 0)))
            if row_remote == 0:
                incomplete.append("QtyOfRemoteIO")
            if row_plc_remote_io == 0 or row_total_remote_serial_io == 0:
                incomplete.append("RemoteIO_Qty_Validation2")
        if row['LM_are_the_IO_Racks_remotely_located'] in ['No', ''] and row.RowIndex <= lmLocalIO.Rows.Count -1:
            row_local = getContainerColSum("LM_to_ELMM_ControlEdge_PLC_Local_IO_Cont", row.RowIndex)
            if row_local == 0:
                incomplete.append("QtyOfLocalIO")
        if row['LM_are_the_IO_Racks_remotely_located'] == 'Yes - Local and Remote' and row.RowIndex <= lmLocalIO.Rows.Count -1:
            row_local = getContainerColSum("LM_to_ELMM_ControlEdge_PLC_Local_IO_Cont", row.RowIndex)
            if row_local == 0:
                incomplete.append("QtyOfLocalIO")
            row_remote = getContainerColSum("LM_to_ELMM_ControlEdge_PLC_Remote_IO_Cont", row.RowIndex)
            row_plc_remote_io = sum(lmRemoteIO.Rows[row.RowIndex].Columns.ToList().Where(lambda y: y.Name == 'no_of_PLC_Remote_IO_group_0_16').Select(lambda c: int(c.Value if c.Value != '' else 0)))
            row_total_remote_serial_io = sum(lmRemoteIO.Rows[row.RowIndex].Columns.ToList().Where(lambda y: y.Name == 'total_remote_serial_IO_racks_0_16').Select(lambda c: int(c.Value if c.Value != '' else 0)))
            if row_remote == 0:
                incomplete.append("QtyOfRemoteIO")
            if row_plc_remote_io == 0 or row_total_remote_serial_io == 0:
                incomplete.append("RemoteIO_Qty_Validation2")
if 'FDM Upgrade' in selectedProducts:
    fdmcontainer = getContainer("FDM_Upgrade_Configuration")

    flag = 0
    count = 0
    for i in fdmcontainer.Rows:
        flag = 0
        if str(i["FDM_Upgrade_Do_you_want_to_upgrade_this_FDM"]) == "Yes":
            if i["FDM_Upgrade_Total_number_of_Server_Device_Points"] == '0' or i["FDM_Upgrade_Total_number_of_Server_Device_Points"] == None or i["FDM_Upgrade_Total_number_of_Server_Device_Points"] == '':
                flag += 1
            else:
                flag = 0
                continue
            if i["FDM_Upgrade_Total_number_of_Audit_Trail_Devices"] == '0' or i["FDM_Upgrade_Total_number_of_Audit_Trail_Devices"] == None or i["FDM_Upgrade_Total_number_of_Audit_Trail_Devices"] == '':
                flag += 1
            else:
                flag = 0
                continue
            if i["FDM_Upgrade_Total_RCIs_including_Experion_PKS_Server_Interfaces"] == '0' or i["FDM_Upgrade_Total_RCIs_including_Experion_PKS_Server_Interfaces"] == None or i["FDM_Upgrade_Total_RCIs_including_Experion_PKS_Server_Interfaces"] == '':
                flag += 1
            else:
                flag = 0
                continue
            if i["FDM_Upgrade_Total_RCIs_excluding_Experion_PKS_Server_Interfaces"] == '0' or i["FDM_Upgrade_Total_RCIs_excluding_Experion_PKS_Server_Interfaces"] == None or i["FDM_Upgrade_Total_RCIs_excluding_Experion_PKS_Server_Interfaces"] == '':
                flag += 1
            else:
                flag = 0
                continue
            if i["FDM_Upgrade_Total_FDM_Clients"] == '0' or i["FDM_Upgrade_Total_FDM_Clients"] == None or i["FDM_Upgrade_Total_FDM_Clients"] == '':
                flag += 1
            else:
                flag = 0
                continue
        if flag != 0:
            count = 1
            break

    flag1 = 0
    count1 = 0
    check = Product.ParseString('<*CTX( Container(FDM_Upgrade_General_questions).Row(1).Column(FDM_Upgrade_Additional_Components_to_be_offered_for_number_of_FDMs_?).GetDisplayValue )*>')
    if check == "Yes":
        fdmaddcontainer = getContainer("FDM_Upgrade_Additional_Configuration")
        for i in fdmaddcontainer.Rows:
            flag1 = 0
            if i["FDM_Upgrade_Are_additional_components_required_for_this_FDM"] == "Yes":
                if i["FDM_Upgrade_How_many_devices_will_be_managed"] == '0' or i["FDM_Upgrade_How_many_devices_will_be_managed"] == None or i["FDM_Upgrade_How_many_devices_will_be_managed"] == '':
                    flag1 += 1
                else:
                    flag1 = 0
                    continue
                if i["FDM_Upgrade_Number_of_Audit_Trail_Devices"] == '0' or i["FDM_Upgrade_Number_of_Audit_Trail_Devices"] == None or i["FDM_Upgrade_Number_of_Audit_Trail_Devices"] == '':
                    flag1 += 1
                else:
                    flag1 = 0
                    continue
                if i["FDM_Upgrade_Number_of_FDM_Clients"] == '0' or i["FDM_Upgrade_Number_of_FDM_Clients"] == None or i["FDM_Upgrade_Number_of_FDM_Clients"] == '':
                    flag1 += 1
                else:
                    flag1 = 0
                    continue
                if i["FDM_Upgrade_Number_of_Experion_TPS_Servers_for_FDM_Integration"] == '0' or i["FDM_Upgrade_Number_of_Experion_TPS_Servers_for_FDM_Integration"] == None or i["FDM_Upgrade_Number_of_Experion_TPS_Servers_for_FDM_Integration"] == '':
                    flag1 += 1
                else:
                    flag1 = 0
                    continue
                if i["FDM_Upgrade_Number_of_Server_Network_Interface_Licenses_Add"] == '0' or i["FDM_Upgrade_Number_of_Server_Network_Interface_Licenses_Add"] == None or i["FDM_Upgrade_Number_of_Server_Network_Interface_Licenses_Add"] == '':
                    flag1 += 1
                else:
                    flag1 = 0
                    continue
            if flag1 != 0:
                count1 = 1
                break

    if count > 0:
        incomplete.append("FDMflag")
    if count1 > 0:
        incomplete.append("FDMaddflag")

if 'FSC to SM' in selectedProducts:
    flag1 = 0
    flag2 = 0
    confsc = getContainer("FSC_to_SM_General_Information")
    check = getFloat(confsc.Rows[0]["FSC_to_SM_Number_of_configurations_to_be_migrated"])
    if check > 0:
        fscConfig = getContainer("FSC_to_SM_Configuration")
        for row in fscConfig.Rows:
            if row["FSC_to_SM_How_many_systems_with_same_configuration_to_be_migrated_in_this_proposal"] in ("0",None,""):
                flag1 = 1
            if getFloat(row["FSC_to_SM_How_many_FSC_Systems_from_the_SafeNet_network_are_we_migrating_in_the_first_phase"]) > getFloat(row["FSC_to_SM_How_many_FSC_Systems_are_in_the_SafeNet_network"]):
                flag2 = 1
    if flag1 == 1:
        incomplete.append("sameconfigFSC")
    if flag2 == 1:
        incomplete.append("safenetFSC")

    fsc3rdparty = getContainer("FSC_to_SM_3rd_Party_Items")
    price = getFloat(fsc3rdparty.Rows[0]["FSC_to_SM_3rd_Party_Hardware_per_Audit_Report"])
    cost = getFloat(fsc3rdparty.Rows[2]["FSC_to_SM_3rd_Party_Hardware_per_Audit_Report"])
    description = fsc3rdparty.Rows[3]["FSC_to_SM_3rd_Party_Hardware_per_Audit_Report"]
    if (price > 0 and (cost == 0 or description == "")) or (cost > 0 and (price == 0 or description == "")):
        incomplete.append("thirdpartyFSC")

if 'FSC to SM IO Migration' in selectedProducts:

    if Product.Attr('MIgration_Scope_Choices').GetValue() != "HW/SW":
        qcf_proposalType = Quote.GetCustomField('EGAP_Proposal_Type').Content
        if Quote.GetCustomField('EGAP_Proposal_Type').Content:
            qcf_proposalType = Quote.GetCustomField('EGAP_Proposal_Type').Content
            if qcf_proposalType == "Firm":
                conAudit = getContainer("FSC_to_SM_IO_Services")
                auditRow = conAudit.Rows[0]["FSC_to_SM_IO_Has_the_FSC_IO_Audit_been_performed"]
                if auditRow in ("","No"):
                    incomplete.append("flagAuditFSCio")

    flagQtyFSCio = 0
    flagSumFSCio = 0
    flagIORacks = 0
    flagAnalogDigital = 0
    scope_labor = 0
    
    flagFscRed = 0
    flagFscNonRed = 0
    flagFscRange1 = 0
    flagFscRange2 = 0
    flagFscRange3 = 0

    

    confscio = getContainer("FSC_to_SM_IO_Migration_General_Information")
    check = getFloat(confscio.Rows[0]["FSC_to_SM_IO_Migration_Total_FSC_SM_Systems"])

    if Product.Attr('MIgration_Scope_Choices').GetValue() != "LABOR":
        fsc_to_sm_migration_gen_info2 = getContainer("FSC_to_SM_IO_Migration_General_Information2")
        row = fsc_to_sm_migration_gen_info2.Rows[0]
        row1 = fsc_to_sm_migration_gen_info2.Rows[1]
        row2 = fsc_to_sm_migration_gen_info2.Rows[2]
        price = getFloat(row["FSC_to_SM_IO_Migration_3rd_Party_Hardware_per_Audit_Report"])
        cost = getFloat(row1["FSC_to_SM_IO_Migration_3rd_Party_Hardware_per_Audit_Report"])
        description = len(row2["FSC_to_SM_IO_Migration_3rd_Party_Hardware_per_Audit_Report"])
        if price != 0 or cost != 0 or description != 0:
            if price == 0 or cost == 0 or description == 0:
                incomplete.append("fsc_to_sm_3rd_party_price")
        check1 = confscio.Rows[0]["FSC_to_SM_IO_Migration_Where_will_the_IOs_be_installed"]
        if check1 != 'New SM Cabinet':
            scope_labor = 1

    if check > 0:
        for row in getContainer("FSC_to_SM_IO_Series_1_&_2_FSC_IO_configurations").Rows:
            if getFloat(row["FSC_to_SM_IO_Quantity_of_Cabinets_containing_IO_Rack"]) == 0:
                flagQtyFSCio += 1
            #else:
                #if getFloat(row["FSC_to_SM_IO_Number_of_IO_Racks"]) == 0:
                    #flagFscRed += 1
                #if getFloat(row["NON_RED_FSC_to_SM_IO_Number_of_IO_Racks"]) == 0:
                    #flagFscNonRed += 1
                    
                
            if (getFloat(row["FSC_to_SM_IO_Number_of_IO_Racks"]) + getFloat(row["NON_RED_FSC_to_SM_IO_Number_of_IO_Racks"])) > 34:
                flagSumFSCio += 1
            if (getFloat(row["FSC_to_SM_IO_Number_of_IO_Racks"]) + getFloat(row["NON_RED_FSC_to_SM_IO_Number_of_IO_Racks"])) > 8 and (getFloat(row["FSC_to_SM_IO_Number_of_IO_Racks"]) + getFloat(row["NON_RED_FSC_to_SM_IO_Number_of_IO_Racks"])) <= 17 and getFloat(row["FSC_to_SM_IO_Quantity_of_Cabinets_containing_IO_Rack"]) < 2:
                flagFscRange1 += 1
            if (getFloat(row["FSC_to_SM_IO_Number_of_IO_Racks"]) + getFloat(row["NON_RED_FSC_to_SM_IO_Number_of_IO_Racks"])) > 17 and (getFloat(row["FSC_to_SM_IO_Number_of_IO_Racks"]) + getFloat(row["NON_RED_FSC_to_SM_IO_Number_of_IO_Racks"])) <= 25 and getFloat(row["FSC_to_SM_IO_Quantity_of_Cabinets_containing_IO_Rack"]) < 3:
                flagFscRange2 += 1
            if (getFloat(row["FSC_to_SM_IO_Number_of_IO_Racks"]) + getFloat(row["NON_RED_FSC_to_SM_IO_Number_of_IO_Racks"])) > 25 and (getFloat(row["FSC_to_SM_IO_Number_of_IO_Racks"]) + getFloat(row["NON_RED_FSC_to_SM_IO_Number_of_IO_Racks"])) <= 34 and getFloat(row["FSC_to_SM_IO_Quantity_of_Cabinets_containing_IO_Rack"]) < 4:
                flagFscRange3 += 1
            if scope_labor == 1:
                if (getFloat(row["FSC_to_SM_IO_Number_of_IO_Racks"]) + getFloat(row["NON_RED_FSC_to_SM_IO_Number_of_IO_Racks"])) == 0:
                    flagIORacks += 1

            sum = 0
            for col in row.Columns:
                if col.Name not in ("FSC_to_SM_IO_Quantity_of_Cabinets_containing_IO_Rack","FSC_to_SM_IO_IO_Module_IO_Rack_Type","FSC_to_SM_IO_Number_of_IO_Racks","FSC_to_SM_IO_Series_1_FSC_IO","FSC_to_SM_IO_Series_2_FSC_IO","NON_RED_FSC_to_SM_IO_IO_Module_IO_Rack_Type","NON_RED_FSC_to_SM_IO_Number_of_IO_Racks","NON_RED_FSC_to_SM_IO_Series_1_FSC_IO","NON_RED_FSC_to_SM_IO_Series_2_FSC_IO"):
                    if getFloat(row[col.Name]) > 0:
                        sum += 1
                        break
            if sum == 0:
                flagAnalogDigital += 1

    if flagQtyFSCio > 0:
        incomplete.append("flagQtyFSCio")
    if flagSumFSCio > 0:
        incomplete.append("flagSumFSCio")
    if flagIORacks > 0:
        incomplete.append("flagFSCIORacks")
    if flagAnalogDigital > 0:
        incomplete.append("flagFSCioAnalogDigital")
    #if flagFscRed > 0:
        #incomplete.append("flagFscRed")
    #if flagFscNonRed > 0:
        #incomplete.append("flagFscNonRed")
    if flagFscRange1 > 0:
        incomplete.append("flagFscRange1")
    if flagFscRange2 > 0:
        incomplete.append("flagFscRange2")
    if flagFscRange3 > 0:
        incomplete.append("flagFscRange3")

if 'Graphics Migration' in selectedProducts:

    if Product.Attr('MIgration_Scope_Choices').GetValue() != "HW/SW":
        if getContainer("Graphics_Migration_Additional_Questions"):
            graphicAddCon = getContainer("Graphics_Migration_Additional_Questions")
            rowAddCon = graphicAddCon.Rows[0]
            if rowAddCon["Graphics_Migration_New_Safeview_Configuration"] not in ("None"):
                if getFloat(rowAddCon["Graphics_Migration_Number_of_station_licenses"]) == 0:
                    incomplete.append("graphicAdditionalCon")
    GraphicsMenuCont = getContainer('Graphics_Migration_Displays_Shapes_Faceplates')
    row=GraphicsMenuCont.Rows[0]
    sumOfDisplays = getFloat(row["Number_of_Simple_Displays"]) + getFloat(row["Number_of_Medium_Displays"]) + getFloat(row["Number_of_Complex_Displays"]) + getFloat(row["Number_of_Very_Complex_Displays"]) + getFloat(row["Number_of_Repeats_Displays"])
    if(sumOfDisplays) <= 0:
        incomplete.append("Sum_of_Displays")

    sumofShapes = getFloat(row["Number_of_Simple_Custom_Shapes"]) + getFloat(row["Number_of_Medium_Custom_Shapes"]) + getFloat(row["Number_of_Complex_Custom_Shapes"]) + getFloat(row["Number_of_Very_Complex_Custom_Shapes"]) + getFloat(row["Number_of_Repeats_Custom_Shapes"])
    if(sumofShapes) <= 0:
        incomplete.append("Sum_of_Shapes")

    sumOfFaceplates = getFloat(row["Number_of_Simple_Custom_Faceplates"]) + getFloat(row["Number_of_Medium_Custom_Faceplates"]) + getFloat(row["Number_of_Complex_Custom_Faceplates"]) + getFloat(row["Number_of_Very_Complex_Custom_Faceplates"]) + getFloat(row["Number_of_Repeats_Custom_Faceplates"])
    if(sumOfFaceplates) <= 0:
        incomplete.append("Sum_of_Faceplates")

if 'CD Actuator I-F Upgrade' in selectedProducts:
    cd_act_gen_info_cont = getContainer("CD_Actuator_IF_Upgrade_General_Info_Cont")
    row = cd_act_gen_info_cont.Rows[0]
    Actuator_zone = getFloat(row["CD_Actuator_Number_of_Actuators_Zones"])
    if Actuator_zone < 10 or Actuator_zone > 256:
        incomplete.append("Actuator_zone_incomplete_msg")
    if Product.Attr('MIgration_Scope_Choices').GetValue() != "LABOR":    
        cd_act_gen_info_cont = getContainer("CD_Actuator_pricing_factory_cost")
    	row = cd_act_gen_info_cont.Rows[0]
    	row1 = cd_act_gen_info_cont.Rows[1]
        row2 = cd_act_gen_info_cont.Rows[2]
    	price = getFloat(row["CD_Actuator_Special_Special_or_iLon_upgrade_pricing"])
    	cost = getFloat(row1["CD_Actuator_Special_Special_or_iLon_upgrade_pricing"])
    	description = len(row2["CD_Actuator_Special_Special_or_iLon_upgrade_pricing"])
        if price != 0 or cost != 0 or description != 0:
            if price == 0 or cost == 0 or description == 0:
                incomplete.append("cd_actuator_pricing_factory_cost")

if 'TCMI' in selectedProducts:
    TCMIcon = getContainer("TCMI_Hardware_and_Licenses") 
    for row in TCMIcon.Rows:
        sum1 = getFloat(row["TCMI_Number_of_systems_Upgrading_TCMI_for_TPN_Only"]) + getFloat(row["TCMI_Number_of_systems_Upgrading_TCMI_for_Hybrid_TPN-EPKS"])
        sum2 = getFloat(row["TCMI_Number_of_Front_and_Rear_Access_Upgrade_TCMI"]) + getFloat(row["TCMI_Number_of_Front_Access_Upgrade_TCMI"])
        sum3 = getFloat(row["TCMI_Number_of_NEW_systems_TCMI_for_TPN_Only"]) + getFloat(row["TCMI_Number_of_NEW_systems_TCMI_for_Hybrid_TPN-EPKS"])
        sum4 = getFloat(row["TCMI_Number_of_Front_and_Rear_Access_New_TCMI"]) + getFloat(row["TCMI_Number_of_Front_Access_New_TCMI"])
        break
        
    if sum1 != sum2:
        incomplete.append("TCMI_Upgrade")    
    if sum3 != sum4:
        incomplete.append("TCMI_New")  

Product.Attr('Incomplete').AssignValue(",".join(incomplete))