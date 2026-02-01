def getContainer(Product,Name):
    return Product.GetContainerByName(Name)

def getRowData(Product,container,column):
    Container = getContainer(Product,container)
    for row in Container.Rows:
        return row[column]

def getAttrData(Product,attr):
    return Product.Attr(attr).GetValue()

def getRowDataIndex(Product,container,column,index):
    Container = getContainer(Product,container)
    for row in Container.Rows:
        if row.RowIndex == index:
            return row[column]

def getFloat(Var):
    if Var:
        return float(Var)
    return 0

def getnumberOfjumpRealease(Product,msid_product):
    Current_Release = getAttrData(Product,"MSID_Current_Experion_Release")
    Target_Release = getAttrData(Product,"MSID_Future_Experion_Release")
    jump = 0
    Container =msid_product.GetContainerByName('OPM_Basic_Information')

    for row in Container.Rows:
        Trace.Write (str(row["OPM_Is_this_is_a_Remote_Migration_Service_RMS"]))
        AMT = str(row["OPM_Is_this_is_a_Remote_Migration_Service_RMS"])
        break

    if AMT == 'Yes' and Target_Release == 'R530':
        query = SqlHelper.GetFirst("select Jumps from Labor_Number_Jump_Releases_Second where Current_Release = '{}' and Target_Release = '{}'".format(Current_Release,Target_Release))
    else:
        query = SqlHelper.GetFirst("select Jumps from LABOR_NUMBER_JUMP_RELEASES where Current_Release = '{}' and Target_Release = '{}'".format(Current_Release,Target_Release))
    if query is not None and query.Jumps != '':
        jump = query.Jumps
    return jump

def getTotalEngHours(Product,container):
    totalFinalHours = 0
    for row in getContainer(Product,container).Rows:
        if row["Deliverable"] == "Total":
            totalFinalHours += getFloat(row["Final_Hrs"])
    return totalFinalHours



def getEBRInstaltion(Product):
    parameters = {"EBR_Upgrade":{"var_1":"EBR_Qty_of_EBR_Upgrade_for_Server","var_2":"EBR_Qty_of_EBR_Upgrade_for_Workstation","var_3":"EBR_Qty_of_EBR_Upgrade_for_Virtual_Node"},"EBR_New_Additional_EBR":{"var_4":"EBR_Qty_of_EBR_New_Additional_for_Server","var_5":"EBR_Qty_of_EBR_New_Additional_for_Workstation","var_6":"EBR_Qty_of_EBR_New_Additional_for_Virtual_Node"},"EBR_Hardware_to_Host_EBR_Physical_Node_Only":{"var_7":"EBR_Additional_Hard_Drive_required","var_8":"EBR_Additional_Network_Storage_Device_NAS_required"}}

    for key in parameters:
        if key == "EBR_Upgrade":
            var_1 = getFloat(getRowData(Product,key,parameters[key]["var_1"]))
            var_2 = getFloat(getRowData(Product,key,parameters[key]["var_2"])) 
            var_3 = getFloat(getRowData(Product,key,parameters[key]["var_3"])) 
        '''if key == "EBR_Hardware_to_Host_EBR_Physical_Node_Only":
            var_7 = getRowData(Product,key,parameters[key]["var_7"])
            var_8 = getRowData(Product,key,parameters[key]["var_8"])''
        if key == "EBR_Upgrade":
            var_1 = getFloat(getRowData(Product,key,parameters[key]["var_1"]))
            var_2 = getFloat(getRowData(Product,key,parameters[key]["var_2"])) 
            var_3 = getFloat(getRowData(Product,key,parameters[key]["var_3"])) 
        ''elif key == "EBR_New_Additional_EBR":
            var_4 = getFloat(getRowData(Product,key,parameters[key]["var_4"])) 
            var_5 = getFloat(getRowData(Product,key,parameters[key]["var_5"])) 
            var_6 = getFloat(getRowData(Product,key,parameters[key]["var_6"]))'''
    
    var_7 = Product.Attr( "EBR_Additional_Hard_Drive_required").GetValue()
    var_8 = Product.Attr( "EBR_Additional_Network_Storage_Device_NAS_required").GetValue()
    var_4 = getFloat(Product.Attr( "Attr_New/AdditionalServer").GetValue())
    var_5 = getFloat(Product.Attr( "Attr_NewAddWorkstation").GetValue())
    var_6 = getFloat(Product.Attr( "Attr_NewAddVirtual_Node").GetValue())
            
     

    installationHours = 0
    installationHours += 6 + (var_1 + var_4 ) * 2 + (var_2 + var_5) * 2 + (var_3 + var_6) * 4
    installationHours += 8 if var_7 == "Yes" else 0
    installationHours += 0 if var_8 in ('',"No") else 4
    installationHours = round(installationHours / 8) * 8
    return installationHours

def getOrionConsoleLabourHours(Product,msid_product):
    parameters = {"Orion_Station_Configuration":{"var_0":"Orion_Number_of_console_bases_with_same_configuration","var_1":"Orion_Number_of_2_Position_Base_Unit","var_2":"Orion_Number_of_3_Position_Base_Unit","var_5_1":"Orion_Membrane_Keyboard_Type","var_7_1":"Orion_Remote_Peripheral_Solution_RPS_Type","var_6_1":"Orion_Number_of_Left_Auxiliary_Equipment_Unit","var_6_2":"Orion_Number_of_Left_Extended_Auxiliary_Equipment_Unit","var_6_3":"Orion_Number_of_Right_Auxiliary_Equipment_Unit","var_6_4":"Orion_Number_of_Right_Extended_Auxiliary_Equipment_Unit","var_6_5":"Orion_Number_of_Center_Straight_Auxiliary_Equipment_Unit","var_6_6":"Orion_Number_of_Center_Curved_Auxiliary_Equipment_Unit","var_6_7":"Orion_Number_of_Center_Curved_Extended_Auxiliary_Equipment_Unit"},"Orion_Services":{"var_3":"Orion_Number_of_existing_stations_that_will_be_migrated_to_Orion_Console","var_4":"Orion_Number_of_new_Orion_stations_that_will_be_installed","var_8":"Orion_Number_of_existing_HMI_Graphics","":"","var_15":"Orion_How_is_this_Orion_Console_Installation_performed","var_16":"Orion_Is_Graphics_Scaling_needed","var_17":"Orion_Honeywell_hours_for_Orion_Console_unboxing_and_installation_in_Control_Room","var_14":"MSID_Will_Honeywell_perform_equipment_installation"},"MSID_CommonQuestions":{"var_9":"LM_ELMM_Construction_work_package_document_prepared_by_Honeywell"}}
    var_1 = 0
    var_2 = 0
    var_5 = 0
    var_6 = 0
    var_7 = 0
    for key in parameters:
        if key == "Orion_Station_Configuration":
            for row in getContainer(Product,key).Rows:
                var_1 += getFloat(row[parameters[key]["var_1"]]) * getFloat(row[parameters[key]["var_0"]])
                var_2 += getFloat(row[parameters[key]["var_2"]]) * getFloat(row[parameters[key]["var_0"]])
                if row[parameters[key]["var_5_1"]] == "Operator Touch Panel":
                    var_5 += ((getFloat(row[parameters[key]["var_1"]]) * 2) + ( getFloat(row[parameters[key]["var_2"]]) * 3)) * getFloat(row[parameters[key]["var_0"]])
                if row[parameters[key]["var_7_1"]] == "WYZE 5070 - Thin Client":
                    var_7 += ((getFloat(row[parameters[key]["var_1"]]) * 2) + ( getFloat(row[parameters[key]["var_2"]]) * 3)) * getFloat(row[parameters[key]["var_0"]])
                var_6 += (getFloat(row[parameters[key]["var_6_1"]]) + getFloat(row[parameters[key]["var_6_2"]]) + getFloat(row[parameters[key]["var_6_3"]]) + getFloat(row[parameters[key]["var_6_4"]]) + getFloat(row[parameters[key]["var_6_5"]]) + getFloat(row[parameters[key]["var_6_6"]]) + getFloat(row[parameters[key]["var_6_7"]])) * getFloat(row[parameters[key]["var_0"]])
        if key == "Orion_Services":
            var_3 = getFloat(Product.Attr('Attr_NoOfexistingstations').GetValue())
            var_4 = getFloat(Product.Attr('Attr_OrionStationsInstalled').GetValue())
            var_8 = getFloat(Product.Attr('Attr_HMIGraphics').GetValue())
            var_15 = Product.Attr('Orion_How_is_this_Orion_Console_Installation').GetValue()
            var_16 = Product.Attr('Orion_Is_Graphics_Scaling_needed').GetValue()
            var_17 = getFloat(Product.Attr('Attr_installationControl Room').GetValue())
            var_14 = Product.Attr('MSID_Will_Honeywell_perform_equipment_installation').GetValue()
        if key == "MSID_CommonQuestions":
            var_9 = msid_product.Attr('Yes-No Selection').GetValue()
    planReviewHours = 0 if var_15 in ("Part of a Migration",'') else 8
    documentation = 0
    documentationRequired = Product.Attr('Orion_Which_documentation_is_required').GetValue()
    selectedDocumentation = documentationRequired.split(',')
    selectedDocumentation = [x.strip() for x in selectedDocumentation]
    #var_9 = "Construction work package document"
    var_10 = "Orion Console planning"
    var_11 = "Power & Heat load calculation"
    var_12 = "Make or update a drawing package"
    documentation += (24 + ( var_1 + var_2 - 1 ) * 8) if var_9 == 'Yes' else 0
    documentation += (8 + ( var_1 + var_2 - 1 ) * 4) if var_10 in selectedDocumentation else 0
    documentation += (8 + ( var_1 + var_2 - 1 ) * 4) if var_11 in selectedDocumentation else 0
    documentation += 32 if var_12 in selectedDocumentation else 0
    inhouseEngineering = (var_8 * 2.2) if var_16 == "Yes" else 0
    siteInstallationEAPS = 0
    siteInstallationEAPS += (var_1 + var_6) * 12 + var_2 * 18 + var_5 * 2 + 4 + (var_1 + var_2 - 1) * 2 + var_7 * 2
    siteInstallationEAPS += (var_3 + var_4 * 6) if var_15 == "Standalone" else 0
    siteInstallationEST1 = 0
    siteInstallationEST1 += ((var_1 + var_6) * 6 + var_2 * 9 + var_5 * 2) if var_14 == "Yes" else 0
    siteInstallationEST1 += var_17
    SAT = 0
    SAT += (var_1 + var_2 + var_6) * 1 + var_5 * 0.5
    SAT += 7 if var_15 == "Standalone" else 0
    return planReviewHours,documentation,inhouseEngineering,siteInstallationEAPS,siteInstallationEST1,SAT


def getEHPMLabourHours(Quote,Product,msid_product):
    parameters = {"xPM_Migration_Scenario_Cont":{"var_1_1":"xPM_Select_the_migration_scenario"},"xPM_Migration_Config_Cont":{"var_0":"xPM_Number_of_xPMs_in_this_config","var1EHPM":"xPM_How_many_EHPMs_will_require_Exp_conn", "var1C300":"xPM_Controller_need_Experion_peer_to_peer_connectivity", "var1EHPMX":"xPM_EHPMX_need_Experion_peer_to_peer_connectivity", "var_3_1":"xPM_Migration_Scenario","var_17":"xPM_Number_of_Red_EHPM_Exp_connected_wo_config","var_18":"xPM_Number_of_Red_EHPM_Non_Exp_connected","var_19":"xPM_How_many_xPM_Power_Supply_upgrade","var_20":"xPM_How_many_xPM_Power_System_upgrade"},"ENB_Migration_Config_Cont":{"var_2":"xPM_Number_of_NIMs_in_this_config"},"MSID_CommonQuestions":{"var_8":"MSID_FEL_Data_Gathering_Required"},"ENB_Migration_General_Qns_Cont":{"var_5_1":"xPM_Number_of_DNCF_long_power_cable_needed","var_5_2":"xPM_Number_of_DNCF_needed"},"xPM_Services_Cont":{"var_10":"xPM_Factory_Acceptance_Test_Required","var_7":"MSID_Will_Honeywell_perform_equipment_installation"}}
    var_1 = 0
    var_2 = 0
    var_17 = 0
    var_18 = 0
    var_19 = 0
    var_20 = 0
    var_11 = 'No' if Quote.GetCustomField('Entitlement').Content == '' else 'Yes'
    var_3 = 0
    var_4 = 0
    for key in parameters:
        if key == "xPM_Migration_Scenario_Cont":
            #var_1_1 = getRowData(Product,key,parameters[key]["var_1_1"])
            var_1_1 = Product.Attr('xPM_Select_the_migration_scenario').GetValue()
        if key == "xPM_Migration_Config_Cont":
            for row in getContainer(Product,key).Rows:
                if var_1_1 == "xPM to EHPM":
                    var_1 += getFloat(row[parameters[key]["var1EHPM"]])
                    
                if row[parameters[key]["var_3_1"]] in ('UPG HPM TO EHPM RED Without IOL','UPG HPM TO EHPM Non RED Without IOL','UPG HPM TO EHPM RED With IOL','UPG HPM TO EHPM Non RED With IOL','Non-redundant HPM to C300PM','Redundant HPM to C300PM','Non-redundant EHPM to C300PM','Redundant EHPM to C300PM','Non-redundant HPM to EHPM','Redundant HPM to EHPM','Non-redundant EHPMX to C300PM','Redundant EHPMX to C300PM','Non-redundant HPM to EHPMX','Redundant HPM to EHPMX','Non-redundant EHPM to EHPMX','Redundant EHPM to EHPMX'):
                    var_3 += getFloat(row[parameters[key]["var_0"]])
                if row[parameters[key]["var_3_1"]] in ('UPG PM/APM TO 15-SLOT EHPM RED With IOL','UPG PM/APM TO 7-SLOT EHPM RED With IOL','UPG PM/APM TO 15-SLOT EHPM Non RED With IOL','UPG PM/APM TO 7-SLOT EHPM Non RED With IOL','Non-redundant PM/APM to EHPM in 7-slot chassis','Non-redundant PM/APM to EHPM in 15-slot chassis','Redundant PM/APM to EHPM in 7-slot chassis','Redundant PM/APM to EHPM in15-slot chassis','Non-redundant PM/APM to C300PM in 7-slot chassis','Non-redundant PM/APM to C300PM in 15-slot chassis','Redundant PM/APM to C300PM in 7-slot chassis','Redundant PM/APM to C300PM in15-slot chassis','Redundant PM/APM to EHPMX in15-slot chassis','Redundant PM/APM to EHPMX in 7-slot chassis','Non-redundant PM/APM to EHPMX in 15-slot chassis','Non-redundant PM/APM to EHPMX in 7-slot chassis'):
                    var_4 += getFloat(row[parameters[key]["var_0"]])
                if var_1_1 == "xPM to C300PM":
                    var_1 += getFloat(row[parameters[key]["var1C300"]])
                    var_17 += getFloat(row[parameters[key]["var_17"]])
                    var_18 += getFloat(row[parameters[key]["var_18"]])
                if var_1_1 == "xPM to EHPMX":
                    var_1 += getFloat(row[parameters[key]["var1EHPMX"]])
                    var_17 += getFloat(row[parameters[key]["var_17"]])
                    var_18 += getFloat(row[parameters[key]["var_18"]])
                var_19 += getFloat(row[parameters[key]["var_19"]])
                var_20 += getFloat(row[parameters[key]["var_20"]])
        if key == "ENB_Migration_Config_Cont":
            for row in getContainer(Product,key).Rows:
                var_2 += getFloat(row[parameters[key]["var_2"]])
        if key == "MSID_CommonQuestions":
            #var_7 = getRowData(Product,key,parameters[key]["var_7"])
            var_8 = msid_product.Attr('MSID_FEL_Data_Gathering_Required').GetValue()
            
        if key == "ENB_Migration_General_Qns_Cont":
            #var_5 = getFloat(getRowData(Product,key,parameters[key]["var_5_1"])) + getFloat(getRowData(Product,key,parameters[key]["var_5_2"]))
            var_5 = getFloat(Product.Attr('xPM_DNCFLPCN').GetValue()) + getFloat(Product.Attr('xPM_NUMDNCF').GetValue())
        if key == "xPM_Services_Cont":
            #var_10 = getRowData(Product,key,parameters[key]["var_10"])
            var_10 = Product.Attr('xPM_Factory_Acceptance_Test_Required').GetValue()
            #var_7 = getRowData(Product,key,parameters[key]["var_7"])
            var_7 = Product.Attr('MSID_Will_Honeywell_perform_equipment_installation').GetValue()
    planReviewEAPS = 16 if var_11 == "Yes" else ( 16 * 0.95)
    planReviewESSS = 0 if var_11 == "Yes" else (16 * 0.05)

    felDataGathering = 24 if var_8 == "Yes" else 0

    migrationDDS = 0
    documentationRequired = Product.Attr('xPM_Which_documentation_is_required').GetValue()
    selectedDocumentation = documentationRequired.split(',')
    selectedDocumentation = [x.strip() for x in selectedDocumentation]
    var_9 = "Basic Documentation"
    var_12 = "Method Statement/ Risk Analysis"
    var_13 = "Power and Heat Calculation"
    var_14 = "Site Readiness Checklist"
    var_15 = "BOM Validation"
    var_16 = "System Architecture"

    if var_9 in selectedDocumentation:
        migrationDDS += 8 + (var_3 - 1) * 4
        if var_7 == "Yes":
            migrationDDS += ( 8 +(var_3 - 1 ) * 4 )
        migrationDDS += 2
    if var_12 in selectedDocumentation:
        if var_3 < 5:
            migrationDDS += 16
        else:
            migrationDDS += 40 if var_3 > 8 else 24
    if var_13 in selectedDocumentation:
        if var_3 < 5:
            migrationDDS += 4
        else:
            migrationDDS += 8 if var_3 > 8 else 6
    migrationDDS += 8 if var_14 in selectedDocumentation else 0
    migrationDDS += 4 if var_15 in selectedDocumentation else 0
    if var_16 in selectedDocumentation:
        migrationDDS += 12 if var_3 < 5 else 16

    integrationEPKS = 0
    if var_9 in selectedDocumentation:
        integrationEPKS += 4 if var_1 > 0 else 0
        integrationEPKS += (var_1 - 1)  * 2 if var_1 > 1 else 0
    swHwOrder = 5 if var_1 > 0 else 4
    preFAT = 0
    if var_10 == "Yes":
        preFAT += 21
        preFAT += 4 * (var_2 - 1) if var_2 > 1 else 0
        preFAT += 3.5 * (var_3 - 1) if var_3 > 1 else 0
        preFAT += 3 if var_1 > 0 else 0
    FAT = var_2 * 4 + var_3 * 4 if var_10 == "Yes" else 0
    siteInstallation = 0
    siteInstallation +=  (1.35 + 4.45 * var_2 + 5.425 * var_3 + var_5 * 1.95) if var_7 == "Yes" else (0.85 + 3.45 * var_2 + 3.3 * var_3)
    siteInstallation += 1.85 * var_1
    siteInstallation += 2 * var_3 if var_4 > 0 else 0
    siteInstallation += var_17 * 1.85 + var_18 * (1.85 + 3.1) + 0.5 * var_19 + var_20
    SAT = 4 + 2.5 * (var_2 - 1) + 2.5 * (var_3 - 1)
    
    return planReviewEAPS,planReviewESSS,felDataGathering,migrationDDS,integrationEPKS,swHwOrder,preFAT,FAT,siteInstallation,SAT


def getTPSLabourHours(Product,msid_product):
    parameters = {"TPS_EX_General_Questions":{"var_1":"ATT_IS_Migration_Part_Of_ELCN_Migration","var_34":"TPS_EX_Additional_Switches","var_27":"TPS_EX_QTY_New_Cabinates","var_41":"TPS_EX_Setup_FTE_Network_Infrastructure"},"TPS_EX_Conversion_ESVT_Server":{"var_5":"TPS_EX_TDC_US_ESVT","var_6":"TPS_EX_TDC_AM_ESVT","var_7":"TPS_EX_TDC_APP_ESVT","var_8":"TPS_EX_TDC_GUS_ESVT","var_3_1":"TPS_EX_ESVT_WO_Trade_Ins","var_3_2":"TPS_EX_ESVT_Redundant"},"MSID_CommonQuestions":{"var_32":"MSID_FEL_Data_Gathering_Required","var_31":"MSID_Acceptance_Test_Required","var_30":"MSID_Is_Switch_Configuration_in_Honeywell_Scope"},"TPS_EX_Station_Conversion_EST":{"var_121314":"TPS_EX_Quantity"},"TPS_EX_Additional_Servers":{"var_20":"TPS_EX_Additional_Server_Quantity"},"TPS_EX_Additional_Stations":{"var0":"TPS_EX_Additional_Stations_Quantity"},"TPS_EX_Bundle_Conversion_Server_Stations":{"var_4_1":"TPS_EX_Non_Reduntant_Conversion_ESVT","var_3_1":"TPS_EX_Redundant_Conversion_ESVT"},"TPS_EX_Conversion_ACET_EAPP":{"var9_10":"TPS_EX_Conversion_ACET_EAPP_Qty"},"var_11":"TPS_EX_Need_Domain_Controller_Added","TPS_EX_Monitors":{"var_21_1":"TPS_EX_Number_FPD_Lower_Tier_OEP_NON_TS","var_21_2":"TPS_EX_Number_FPD_Lower_Tier_OEP_TS","var_21_3":"TPS_EX_Number_FPD_Lower_Tier_IKB_Non_TS","var_21_4":"TPS_EX_Number_FPD_Lower_Tier_IKB_TS","var_21_5":"TPS_EX_Number_FPD_Upper_Tier_Non_TS","var_21_6":"TPS_EX_Number_FPD_Lower_Tier_TS","var_22_1":"TPS_EX_Desktop_Number_55in_FPD_Non_TS","var_22_2":"TPS_EX_Desktop_Number_23in_FPD_Non_TS","var_22_3":"TPS_EX_Desktop_Number_22in_FPD_TS","var_22_4":"TPS_EX_Desktop_Number_21_3in_FPD_Non_TS","var_22_5":"TPS_EX_Desktop_Number_21_3in_FPD_TS","var_26_1":"TPS_EX_Z_Console_Number_22in_FPD_Non_TS","var_26_2":"TPS_EX_Z_Console_Number_22in_FPS_TS","var_25_1":"TPS_EX_EZ_Console_Number_21_3in_FPD_Non_TS","var_25_2":"TPS_EX_EZ_Console_Number_21_3in_FPD_TS","var_25_3":"TPS_EX_EZ_Console_Number_22in_FPD_NON_TS","var_25_4":"TPS_EX_EZ_Console_Number_22in_FPD_TS","var_23_1":"TPS_EX_Icon_Console_Number_21_3in_FPD_Non_TS","var_23_2":"TPS_EX_Icon_Console_Number_21_3in_FPD_TS"},"TPS_EX_Service":{"var_28":"ATT_TPS_Qty_Existing_Cabinets","var_2":"TPS_EX_Will_System_be_migrated_virtual_system","var_29":"TPS_Will_Honeywell_perform_equipment_installation"}}#"MSID_Will_Honeywell_perform_equipment_installation"}}
    var_12 =0
    var_13 =0
    var_14 =0
    var_9 = 0
    var_10 = 0
    for key in parameters:
        if key == "TPS_EX_General_Questions":
            var_1 = getAttrData(Product,parameters[key]["var_1"])
            if var_1 == '':
                var_1 = "Yes"
            var_34 = getFloat(getAttrData(Product,parameters[key]["var_34"]))
            var_27 = getFloat(getAttrData(Product,parameters[key]["var_27"]))
            var_41 = getAttrData(Product,parameters[key]["var_41"])
            if var_41 in ('','NO_FTE_NETWORK_EXISTS','NO_HANDLED_BY_CUSTOMER'):
                var_41 = 'No'
            else:
                var_41 = 'Yes'
        if key == "TPS_EX_Service":
            var_29 = getAttrData(Product,parameters[key]["var_29"])
            #var_30 = getRowData(Product,key,parameters[key]["var_30"])
            #if var_30 == '':
            #    var_30 = "No"
            #var_31 = getRowData(Product,key,parameters[key]["var_31"])
            #if var_31 == '':
            #    var_31 = "SAT"
            var_28 = getFloat(getAttrData(Product,parameters[key]["var_28"]))
            var_2 = getAttrData(Product,parameters[key]["var_2"])
            if var_2 == '':
                var_2 = "No"
        if key == "TPS_EX_Conversion_ESVT_Server":
            var_5 = getFloat(getAttrData(Product,parameters[key]["var_5"]))
            var_6 = getFloat(getAttrData(Product,parameters[key]["var_6"]))
            var_7 = getFloat(getAttrData(Product,parameters[key]["var_7"]))
            var_8 = getFloat(getAttrData(Product,parameters[key]["var_8"]))
            var_3_1 = getFloat(getAttrData(Product,parameters[key]["var_3_1"]))
            var_3_2 = getAttrData(Product,parameters[key]["var_3_2"])

        if key == "MSID_CommonQuestions":
            #var_29 = getRowData(Product,key,parameters[key]["var_29"])
            var_32 = getAttrData(msid_product,parameters[key]["var_32"])
            var_30 = getAttrData(msid_product,parameters[key]["var_30"])
            if var_30 == '':
                var_30 = "No"
            var_31 = getAttrData(msid_product,parameters[key]["var_31"])
            if var_31 == '':
                var_31 = "SAT"

        if key == "TPS_EX_Station_Conversion_EST":
            for row in getContainer(Product,key).Rows:
                if row["TPS_EX_Station_Conversion_Type"] == "US_AM to ES-T":
                    var_12 = getFloat(row[parameters[key]["var_121314"]])
                if row["TPS_EX_Station_Conversion_Type"] == "GUS to ES-T":
                    var_14 = getFloat(row[parameters[key]["var_121314"]])
                if row["TPS_EX_Station_Conversion_Type"] == "UGUS to ES-T":
                    var_13 = getFloat(row[parameters[key]["var_121314"]])
        
        if key == "TPS_EX_Additional_Servers":
            var_20 =  getFloat(getRowDataIndex(Product,key,parameters[key]["var_20"],0)) + getFloat(getRowDataIndex(Product,key,parameters[key]["var_20"],1))

        if key == "TPS_EX_Additional_Stations":
            var_17 = 0
            var_18 = 0
            var_19 = 0
            for row in getContainer(Product,key).Rows:
                if row["TPS_EX_Additional_Stations_Type"] in ('Flex Station - Desk','Flex Station - Cabinet','Flex Station - Orion'):
                    var_17 += getFloat(row[parameters[key]["var0"]])
                if row["TPS_EX_Additional_Stations_Type"] in ('Console Extended Station - Desk','Console Extended Station - Cabinet','Console Extended Station - Orion'):
                    var_18 += getFloat(row[parameters[key]["var0"]])
                if row["TPS_EX_Additional_Stations_Type"] in ('Console Station - Desk','Console Station - Cabinet','Console Station - Orion','ES-T Station - Desk','ES-T Station - Cabinet','ES-T Station - Orion'):
                    var_19 += getFloat(row[parameters[key]["var0"]])

        if key == "TPS_EX_Bundle_Conversion_Server_Stations":
            var_52 = getAttrData(Product,parameters[key]["var_4_1"])
            var_51 = getAttrData(Product,parameters[key]["var_3_1"])
            if var_52 != "No" or var_51 != "No":
                var_40 = 3
            else:
                var_40 = 0
 
        if key == "TPS_EX_Conversion_ACET_EAPP":
            for row in getContainer(Product,key).Rows:
                if row["TPS_EX_Conversion_ACET_EAPP_Type"] == "APP to EAPP":
                    var_10 = getFloat(row[parameters[key]["var9_10"]
                    ])
                if row["TPS_EX_Conversion_ACET_EAPP_Type"] == "APP to ACE-T":
                    var_9 = getFloat(row[parameters[key]["var9_10"]])

        if key == "TPS_EX_Monitors":
            var_21 = getFloat(getAttrData(Product,parameters[key]["var_21_1"])) + getFloat(getAttrData(Product,parameters[key]["var_21_2"])) + getFloat(getAttrData(Product,parameters[key]["var_21_3"])) + getFloat(getAttrData(Product,parameters[key]["var_21_4"])) + getFloat(getAttrData(Product,parameters[key]["var_21_5"])) + getFloat(getAttrData(Product,parameters[key]["var_21_6"]))
            var_22 = getFloat(getAttrData(Product,parameters[key]["var_22_1"])) + getFloat(getAttrData(Product,parameters[key]["var_22_2"])) + getFloat(getAttrData(Product,parameters[key]["var_22_3"])) + getFloat(getAttrData(Product,parameters[key]["var_22_4"])) + getFloat(getAttrData(Product,parameters[key]["var_22_5"]))
            var_26 = getFloat(getAttrData(Product,parameters[key]["var_26_1"])) + getFloat(getAttrData(Product,parameters[key]["var_26_2"]))
            var_25 = getFloat(getAttrData(Product,parameters[key]["var_25_1"])) + getFloat(getAttrData(Product,parameters[key]["var_25_2"])) + getFloat(getAttrData(Product,parameters[key]["var_25_3"])) + getFloat(getAttrData(Product,parameters[key]["var_25_4"]))
            var_23 = getFloat(getAttrData(Product,parameters[key]["var_23_1"])) + getFloat(getAttrData(Product,parameters[key]["var_23_2"]))

    var_11 = Product.Attr('TPS_EX_Need_Domain_Controller_Added').GetValue()
    if var_11 in ('Yes Add a HP Rack Mounted DC','Yes Add a Dell Rack Mounted DC'):
        var_11 = 1
    else:
        var_11 = 0

    var_3 = 0
    var_4 = 0
    var_3 += (var_5 + var_6 + var_7+ var_8 + var_3_1) if var_3_2 == "Yes" else 0
    var_3 += 1 if var_51 == "Yes" else 0
    var_4 += (var_5 + var_6 + var_7+ var_8 + var_3_1) if var_3_2 == "No" else 0
    var_4 += 1 if var_52 == "Yes" else 0

    var_15 = 0
    var_16 = 0
    var_24 = 0

    felDataGathering = 16 if var_32 == "Yes" else 0
    migrationDocumentation = 0
    documentationRequired = Product.Attr('TPS_EX_Which_Documentation_Required').GetValue()
    selectedDocumentation = documentationRequired.split(',')
    selectedDocumentation = [x.strip() for x in selectedDocumentation]
    var_33 = "Migration FDS required?"
    var_35 = "Migration DDS required?"
    var_36 = "Cabinet Drawings required?"
    var_37 = "Network Drawings required?"
    var_38 = "Power & Heat Calculation required?"
    var_39 = "Migration Execution Plan required?"
    migrationDocumentation += 12 if var_33 in selectedDocumentation else 0
    migrationDocumentation += (40 + (var_3 + var_4 + var_20 - 1) * 4) if var_35 in selectedDocumentation else 0
    if var_36 in selectedDocumentation:
        migrationDocumentation += (8 + (var_27- 1 ) * 6) if var_27 > 0 else 0
        migrationDocumentation += (6 + (var_28 - 1) * 4) if var_28 > 0 else 0
    migrationDocumentation += 6 if var_37 in selectedDocumentation else 0
    if var_38 in selectedDocumentation:
        migrationDocumentation += 8 if (var_27+var_28) > 6 else (var_27 + var_28) * 1.5
    migrationDocumentation += (24 + (var_3 + var_4 + var_20 - 1) * 2) if var_39 in selectedDocumentation else 0
    offSiteActivities = 0
    if var_31 != "SAT":
        offSiteActivities += (var_3+var_4+var_20)*8
        offSiteActivities += (var_3+var_4+var_20)*4
        offSiteActivities += ((var_5+var_6+var_7+var_8+var_12+var_13+var_14+var_15+var_16)*15/60)
        offSiteActivities += (var_3*14+var_4*8+var_20*14)
        offSiteActivities += (var_12+var_13+var_14+var_15+var_16+var_17+var_18+var_19+var_40)*5.5
        offSiteActivities += (var_9*6+var_10*6)
        offSiteActivities += var_11*4
        if var_30 == "Yes":
            offSiteActivities += var_34*2
            offSiteActivities += 4 if var_41 == "Yes" else 0
    fatProcedure = 0 if var_31 == "SAT" else 12 + (var_3 + var_4 + var_20 - 1) * 5
    preFAT = 0
    if var_31 != "SAT":
        preFAT += (var_3*1.5+var_4*1)+var_20*1 if var_2 == "No" else (var_3+var_4+var_20)*1
        preFAT += (var_27*4) if var_2 == "No" else 0
        preFAT += 2 if var_2 == "No" else 0
        preFAT += (var_12+var_13+var_14+var_15+var_16+var_17+var_18+var_19+var_40)*30/60 if var_2 == "No" else (var_12+var_13+var_14+var_15+var_16+var_17+var_18+var_19+var_40)*20/60
    siteInstallationEAPS = 0
    if var_31 == "SAT":
        if var_30 == "Yes":
            siteInstallationEAPS += var_34 * 2
            siteInstallationEAPS += 4 if var_41 == "Yes" else 0
        siteInstallationEAPS += var_11*4
        siteInstallationEAPS += (var_3+var_4+var_20)*8
        siteInstallationEAPS += (var_3+var_4+var_20)*4 
        siteInstallationEAPS += (var_3*14+var_4*8+var_20*14)
        siteInstallationEAPS += (var_12+var_13+var_14+var_15+var_16+var_17+var_18+var_19+var_40)*5.5
        siteInstallationEAPS += (var_9*6+var_10*6)
    siteInstallationEAPS +=  (var_5+var_6+var_7+var_8+var_12+var_13+var_14+var_15+var_16)*15/60
    siteInstallationEAPS += (var_3+var_20)*10/60+(var_4+var_12+var_13+var_14+var_15+var_16+var_17+var_18+var_19+var_40)*5/60
    siteInstallationEAPS += (var_3+var_20)*30/60
    siteInstallationEAPS += 8 if (var_12+var_13+var_14+var_15+var_16+var_17+var_18+var_19+var_40+var_3+var_4+var_20) < 8 else 16
    siteInstallationEAPS += 24 if (var_12+var_13+var_14+var_15+var_16+var_17+var_18+var_19+var_40+var_3+var_4+var_20) < 8 else 40

    siteInstallationEST1 = 0
    if var_29 == "Yes":
        siteInstallationEST1 += ((var_5+var_12)*120/60)+((var_16+var_15)*30/60)
        siteInstallationEST1 += (var_8+var_13+var_14)*20/60
        siteInstallationEST1 += (var_7+var_9+var_10)*20/60
        siteInstallationEST1 += (getFloat(var_6*30))/60
        siteInstallationEST1 += 4 if var_1 == "YES" else 0
        siteInstallationEST1 += var_27*4
        siteInstallationEST1 += ((var_3+var_20)*1+(getFloat(var_4*30)/60)) if var_28 > 0 else 0
        siteInstallationEST1 += (var_12+var_13+var_14+var_15+var_16+var_17+var_18+var_19+var_40)*30/60 if var_28 > 0 else 0
        siteInstallationEST1 += (var_3*1+(getFloat(var_4*30)/60)) if var_1 == "NO" else 0
        siteInstallationEST1 += (var_21*1 + var_22*0.7 + var_23 + var_25*1.3 + var_26*1.3)*30/60
        siteInstallationEST1 += getFloat(var_11*30)/60
        siteInstallationEST1 += var_34*2
        siteInstallationEST1 += 4 if var_41 == "Yes" else 0
        siteInstallationEST1 += (var_3+var_20)*10/60+(var_4+var_12+var_13+var_14+var_15+var_16+var_17+var_18+var_19+var_40)*5/60
    SAT = 0
    if var_31 != "FAT":
        SAT += 8+(var_3+var_4+var_20-1)*2
        SAT += 4
        SAT += (var_3*8+var_20*8+var_4*6)
    return felDataGathering,migrationDocumentation,offSiteActivities,fatProcedure,preFAT,siteInstallationEAPS,siteInstallationEST1,SAT


def getTCMILabourHours(Product):
    var_aa = 0
    var_cc = 'No'
    parameters = {"TCMI_Hardware_and_Licenses":{"aa1":"TCMI_Number_of_Front_and_Rear_Access_Upgrade_TCMI","aa2":"TCMI_Number_of_Front_and_Rear_Access_New_TCMI","aa3":"TCMI_Number_of_Front_Access_Upgrade_TCMI","aa4":"TCMI_Number_of_Front_Access_New_TCMI"},"TCMI_Services":{"cc1":"TCMI_Is_Triconex_SMM_being_migrated_with_xPM_in"}}
    for key in parameters:
        if key == "TCMI_Hardware_and_Licenses":
            var_aa = getFloat(getRowData(Product,key,parameters[key]["aa1"])) + getFloat(getRowData(Product,key,parameters[key]["aa2"])) + getFloat(getRowData(Product,key,parameters[key]["aa3"])) + getFloat(getRowData(Product,key,parameters[key]["aa4"]))
        if key == "TCMI_Services":
            var_cc = getAttrData(Product,parameters[key]["cc1"])
    felSiteDataGathering = 2 + var_aa
    migrationDDS = 0
    migrationDDS += 4.5 + var_aa if var_cc == 'Yes' else 8 + (var_aa - 1)
    migrationDDS += 0.5
    migrationDDS += 1 + var_aa if var_cc == 'Yes' else 8 + (var_aa - 1)
    siteInstallation = 4 + (var_aa * 3)
    SAT = 0
    SAT += 2 if var_cc == "Yes" else 4 + var_aa - 1
    SAT += 1.5 if var_cc == "Yes" else 2 + var_aa - 1
    return felSiteDataGathering,migrationDDS,siteInstallation,SAT


def calculateELCNHWSWOrder(Product):
    qty = Product.Attr( "Attr_New/AdditionalServer").GetValue()
    qty1 = Product.Attr( "Attr_NewAddWorkstation").GetValue()
    qty2 = Product.Attr( "Attr_NewAddVirtual_Node").GetValue()
    quantities = [qty, qty1, qty2]
    if qty not in ('0','') or qty1 not in ('0','') or qty2 not in ('0',''):
        return 8

    return 4

def calculateFinalHours(row):
    if getFloat(row["Calculated_Hrs"]) == 0:
        return str(round(getFloat(row["Final_Hrs"])))
    return str(round(getFloat(row["Calculated_Hrs"]) * getFloat(row["Adjustment_Productivity"])))

def checkForMPACustomer(TagParserQuote):
    PricePlanPresent = False
    query = TagParserQuote.ParseString("select * from MPA_PRICE_PLAN_MAPPING where Agreement_Name= '<*CTX(Quote.CustomField(MPA))*>' and Price_Plan_Status= 'Active' and Price_Plan_Parts_Discount = 'Y' and Price_Plan_Start_Date <= '<*CTX( Date.Format(MM/dd/yyyy) )*>' and Price_Plan_End_Date >= '<*CTX( Date.Format(MM/dd/yyyy) )*>'")
    res = SqlHelper.GetList(query)
    if res and len(res) > 0:
        PricePlanPresent = True
    return PricePlanPresent

def calculateTotals(container):
    totalOffSiteHrs = 0
    totalOnSiteHrs = 0
    totalOffSiteFinalHrs = 0
    totalOnSiteFinalHrs = 0
    totalCalculatedHrs = 0
    totalFinalHrs = 0
    for row in container.Rows:
        if row["Deliverable_Type"] in ("Offsite","Off-Site"):
            #if row["Calculated_Hrs"] != "0":
            totalOffSiteHrs = totalOffSiteHrs + getFloat(row["Calculated_Hrs"])
            totalOffSiteFinalHrs = totalOffSiteFinalHrs + getFloat(row["Final_Hrs"])
        elif row["Deliverable_Type"] in ("Onsite","On-Site"):
            #if row["Calculated_Hrs"] != "0":
            totalOnSiteHrs = totalOnSiteHrs + getFloat(row["Calculated_Hrs"])
            totalOnSiteFinalHrs = totalOnSiteFinalHrs + getFloat(row["Final_Hrs"])
        totalCalculatedHrs = totalOffSiteHrs + totalOnSiteHrs
        totalFinalHrs = totalOffSiteFinalHrs + totalOnSiteFinalHrs
    for row in container.Rows:
        if row["Deliverable"] == "Off-Site":
            row["Calculated_Hrs"] = str(totalOffSiteHrs)
            row["Final_Hrs"] = str(totalOffSiteFinalHrs)
        elif row["Deliverable"] == "On-Site":
            row["Calculated_Hrs"] = str(totalOnSiteHrs)
            row["Final_Hrs"] = str(totalOnSiteFinalHrs)
        elif row["Deliverable"] == "Total":
            row["Calculated_Hrs"] = str(totalCalculatedHrs)
            row["Final_Hrs"] = str(totalFinalHrs)
    container.Calculate()


def calculateELCNSiteInstallationAndSAT(var17,var18,var11,var12,var13,var14,var15,var16,var22,var23,var24,var25,var26,var27,var1,var2,var3,var4,var7,var8,var9,var10,var5,var6,var21,var29,var28):
    siteInstallationHours = 0
    siteInstallationHours += 0 if var17 == "Nothing - ELCN Bridge is present" else 16
    if var18 == "Yes":
        siteInstallationHours +=  (8 + var11 * 12 + var12 * 12 + var13 * 4.8 + var14 * 8 + var15 * 8 + var16 * 10 ) + (var22 * 16 + var23 * 16 + var24 * 12 + var25 * 16 + var26 * 8 +var27 * 20 + (var22 + var23 + var24 + var25 + var26 + var27 )*5 )
    elif var18 in ('','No'):
        siteInstallationHours +=  (8 + var11 * 12 + var12 * 12 + var13 * 4.8 + var14 * 8 + var15 * 8 + var16 * 10 ) + ( var1 * 8 + var2 * 8 + var3 * 16 + var4 * 16 + var7 * 6 + var8 * 6 + var9 * 6 + var10 * 6 )
        siteInstallationHours += var5 * 2.8 if var5 > 4 else var5 * 4
        siteInstallationHours += var6 * 2.8 if var6 > 4 else var6 * 4
        siteInstallationHours += (var22 * 16 + var23 * 16 + var24 * 12 + var25 * 16 + var26 * 8 + var27 * 20) + (var22 + var23 + var24 + var25 + var26 + var27 ) * 5
    siteInstallationHours += var21
    siteInstallationHours += 0 if var29 == "Yes" else -4
    SAT = 0
    if var28 == "Yes":
        SAT += 0 if var18 == "Yes" else 16
    return siteInstallationHours,SAT