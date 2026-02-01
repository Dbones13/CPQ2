###################################################################
#Modified by Abhijeet Shinde on 20/10/22
#Commented at line 161 and added at line no 162
#Eliminate the 12% labor discount when “AMT” is selected. (Labor hours will be the same for “Original” and “AMT”).
###################################################################


from GS_MigrationLaborHoursModule import getnumberOfjumpRealease,getRowData,getRowDataIndex,getEBRInstaltion,getOrionConsoleLabourHours,getEHPMLabourHours,getTPSLabourHours,getTCMILabourHours,calculateELCNHWSWOrder,checkForMPACustomer,calculateTotals,calculateELCNSiteInstallationAndSAT,getContainer,getFloat
from GS_MigrationLaborHoursModule_2 import getEHPMHARTIOLabourHours,getC200MigrationLabourHours,getCBECLabourHours,calculateFinalHours1,reCalAdj
from GS_MigrationLaborHoursUtil import getProjectMangementHours
from GS_MigrationLaborHoursModule_4 import calculateEMPEfforts
mpaAvailable = checkForMPACustomer(TagParserQuote)
activeServiceContract = Product.Attr("MSID_Active_Service_Contract").GetValue()
entitlement = Quote.GetCustomField("Entitlement").Content
opmEngineeringCon = getContainer(Product,"MSID_Labor_OPM_Engineering")
lcnOneTimeUpgradeCon = getContainer(Product,"MSID_Labor_LCN_One_Time_Upgrade_Engineering")
ebrCon = getContainer(Product,"MSID_Labor_EBR_Con")
elcnCon = getContainer(Product,"MSID_Labor_ELCN_Con")
orionConsoleCon = getContainer(Product,"MSID_Labor_Orion_Console_Con")
ehpmCon = getContainer(Product,"MSID_Labor_EHPM_C300PM_Con")
tpsCon = getContainer(Product,"MSID_Labor_TPS_TO_EXPERION_Con")
tcmiCon = getContainer(Product,"MSID_Labor_TCMI_Con")
ehpmhartioCon = getContainer(Product,"MSID_Labor_EHPM_HART_IO_Con")
c200migrationCon = getContainer(Product,"MSID_Labor_C200_Migration_Con")
cbecCon = getContainer(Product,"MSID_Labor_CB-EC_Upgrade_to_C300-UHIO_con")
projectManagementCon = getContainer(Product,"MSID_Labor_Project_Management")

parameters = {"MSID_CommonQuestions":{"Var_22":"MSID_FEL_Data_Gathering_Required","Var_5":"MSID_Current_Experion_Release"},"OPM_Node_Configuration":{"Var_1":"OPM_No_of_Experion_Servers","Var_2_1":"OPM_No_of_ACET_Servers_LCN_Connected","Var_2_2":"OPM_No_of_EAPP_Servers_LCN_Connected","Var_3_1":"OPM_Qty_of_ESF_and_ES-CE_Rack_Mount","Var_3_2":"OPM_Qty_of_ESF_and_ESCE_Tower","Var_27_1":"OPM_Qty_of_ESC_Rack_Mount","Var_27_2":"OPM_Qty_of_ESC_Tower","Var_4_1":"OPM_No_of_EST_Rack_mount","Var_4_2":"OPM_No_of_EST_Tower","Var_8":"OPM_No_of_Other_Servers_to_be_migrated","Var_9":"OPM_Qty_of_RPS_and_Thin_Clients","Var_10":"OPM_Qty_of_Series_C_Controllers","Var_11":"OPM_Qty_of_Profibus_Modules","Var_12":"OPM_Qty_of_Control_Firewalls_CF9s","Var_13":"OPM_Qty_of_Series_C_IO_Modules_excluding_UIO","Var_14":"OPM_Qty_of_Fieldbus_Interface_Modules","Var_25":"OPM_Qty_of_Series_A_IO_Modules","Var_26":"OPM_Qty_of_UIO_UIO2_Modules"},"OPM_Services":{"Var_32":"OPM_is_system_required_Domain_controller_upgrade","Var_33":"OPM_Additional_hrs_for_Document_Customization","Var_23":"OPM_Acceptance_Test_Required"},"OPM_Basic_Information":{"Var_24":"OPM_RESS_Migration_in_scope","Var_21":"OPM_Is_the_Experion_System_LCN_Connected"},"OPM_FTE_Switches_migration_info":{"Var_28":"OPM_Quantity_of_L1_L2_Switches","Var_29":"OPM_Qty_of_Backbone_or_Agg_Fiber_Optic_Switch"}}

parameters2 = {"ELCN_Basic_Information":{"var17":"ELCN_If_ELCN_Bridge_is_not_present_in_LCN"},"ELCN_Services":{"var18":"ELCN_Will_OPM_or_TPS_to_Experion_be_performed","var21":"ELCN_Additional_hours_for_FTE_setup","var29":"ELCN_Services_for_NG_Switch_Configuration"},"ELCN_Upgrade_New_ELCN_Nodes":{"var1":"ELCN_Qty_of_Non_Redundant_ESVTs","var3":"ELCN_Qty_of_Redundant_ESVTs","var5":"ELCN_Qty_of_ESTs","var7":"ELCN_Qty_of_ACE_Ts","var9":"ELCN_Qty_of_EAPPs","var11":"ELCN_Qty_of_HMs","var13_1":"ELCN_Qty_of_Non_redundant_AMs","var13_2":"ELCN_Qty_of_Non_Redundant_HGs","var13_3":"ELCN_Qty_of_Non_Redundant_EHBs","var13_4":"ELCN_Qty_of_Non_Redundant_ETN_EHBs","var13_5":"ELCN_Qty_of_Non_Redundant_NIMs","var13_7":"ELCN_Qty_of_Non_Redundant_ENIMs","var13_8":"ELCN_Qty_of_Non_Redundant_ETN_ENIMs","var13_9":"ELCN_Qty_of_Network_Gateways","var14":"ELCN_Qty_of_Non_Redundant_xPLCGs","var15_1":"ELCN_Qty_of_Redundant_AMs","var15_2":"ELCN_Qty_of_Redundant_HGs","var15_3":"ELCN_Qty_of_Redundant_EHBs","var15_4":"ELCN_Qty_of_Redundant_ETN_EHBs","var15_5":"ELCN_Qty_of_Redundant_NIMs","var15_7":"ELCN_Qty_of_Redundant_ENIMs","var15_8":"ELCN_Qty_of_Redundant_ETN_ENIMs","var16":"ELCN_Qty_of_Redundant_xPLCGs"},"MSID_CommonQuestions":{"var28":"MSID_Is_Site_Acceptance_Test_Required"}}

for key in parameters:
    if key == "MSID_CommonQuestions":
        Var_22 = getRowData(Product,key,parameters[key]["Var_22"])
        Var_5 = getRowData(Product,key,parameters[key]["Var_5"])
    elif key == "OPM_Node_Configuration":
        Var_1 = getFloat(getRowData(Product,key,parameters[key]["Var_1"]))
        Var_2 = getFloat(getRowData(Product,key,parameters[key]["Var_2_1"])) + getFloat(getRowData(Product,key,parameters[key]["Var_2_2"]))
        Var_3 = getFloat(getRowData(Product,key,parameters[key]["Var_3_1"])) + getFloat(getRowData(Product,key,parameters[key]["Var_3_2"]))
        Var_27 = getFloat(getRowData(Product,key,parameters[key]["Var_27_1"])) + getFloat(getRowData(Product,key,parameters[key]["Var_27_2"]))
        Var_4 = getFloat(getRowData(Product,key,parameters[key]["Var_4_1"])) + getFloat(getRowData(Product,key,parameters[key]["Var_4_2"]))
        Var_8 = getFloat(getRowData(Product,key,parameters[key]["Var_8"]))
        Var_9 = getFloat(getRowData(Product,key,parameters[key]["Var_9"]))
        Var_10 = getFloat(getRowData(Product,key,parameters[key]["Var_10"]))
        Var_11 = getFloat(getRowData(Product,key,parameters[key]["Var_11"]))
        Var_12 = getFloat(getRowData(Product,key,parameters[key]["Var_12"]))
        Var_13 = getFloat(getRowData(Product,key,parameters[key]["Var_13"]))
        Var_14 = getFloat(getRowData(Product,key,parameters[key]["Var_14"]))
        Var_25 = getFloat(getRowData(Product,key,parameters[key]["Var_25"]))
        Var_26 = getFloat(getRowData(Product,key,parameters[key]["Var_26"]))

    elif key == "OPM_Services":
        Var_32 = getRowData(Product,key,parameters[key]["Var_32"])
        Var_33 = getFloat(getRowData(Product,key,parameters[key]["Var_33"]))
        Var_23 = getRowData(Product,key,parameters[key]["Var_23"])
    elif key == "OPM_Basic_Information":
        ressScope = getRowData(Product,key,parameters[key]["Var_24"])
        Var_24 = 0
        if ressScope == "Yes":
            Var_24 = 1
        elif ressScope == "No":
            Var_24 = 0
        Var_21 = getRowData(Product,key,parameters[key]["Var_21"])
    elif key == "OPM_FTE_Switches_migration_info":
        Var_28 = getFloat(getRowData(Product,key,parameters[key]["Var_28"]))
        Var_29 = getFloat(getRowData(Product,key,parameters[key]["Var_29"]))

for key in parameters2:
    if key == "ELCN_Basic_Information":
        var17 = getRowData(Product,key,parameters2[key]["var17"])
    elif key == "ELCN_Services":
        var18 = getRowData(Product,key,parameters2[key]["var18"])
        var21 = getFloat(getRowData(Product,key,parameters2[key]["var21"]))
        #var28 = getRowData(Product,key,parameters2[key]["var28"])
        var29 = getRowData(Product,key,parameters2[key]["var29"])
    elif key == "MSID_CommonQuestions":
        var28 = getRowData(Product,key,parameters2[key]["var28"])
    elif key == "ELCN_Upgrade_New_ELCN_Nodes":
        var1 = getFloat(getRowDataIndex(Product,key,parameters2[key]["var1"],0))
        var2 = getFloat(getRowDataIndex(Product,key,parameters2[key]["var1"],1))
        var3 = getFloat(getRowDataIndex(Product,key,parameters2[key]["var3"],0))
        var4 = getFloat(getRowDataIndex(Product,key,parameters2[key]["var3"],1))
        var5 = getFloat(getRowDataIndex(Product,key,parameters2[key]["var5"],0))
        var6 = getFloat(getRowDataIndex(Product,key,parameters2[key]["var5"],1))
        var7 = getFloat(getRowDataIndex(Product,key,parameters2[key]["var7"],0))
        var8 = getFloat(getRowDataIndex(Product,key,parameters2[key]["var7"],1))
        var9 = getFloat(getRowDataIndex(Product,key,parameters2[key]["var9"],0))
        var10 = getFloat(getRowDataIndex(Product,key,parameters2[key]["var9"],1))
        var11 = getFloat(getRowDataIndex(Product,key,parameters2[key]["var11"],0))
        var12 = getFloat(getRowDataIndex(Product,key,parameters2[key]["var11"],1))
        var13 = getFloat(getRowDataIndex(Product,key,parameters2[key]["var13_1"],1)) + getFloat(getRowDataIndex(Product,key,parameters2[key]["var13_2"],1)) + getFloat(getRowDataIndex(Product,key,parameters2[key]["var13_3"],1)) + getFloat(getRowDataIndex(Product,key,parameters2[key]["var13_4"],1)) + getFloat(getRowDataIndex(Product,key,parameters2[key]["var13_5"],1)) + getFloat(getRowDataIndex(Product,key,parameters2[key]["var13_7"],1)) + getFloat(getRowDataIndex(Product,key,parameters2[key]["var13_8"],1)) + getFloat(getRowDataIndex(Product,key,parameters2[key]["var13_9"],1))
        var14 = getFloat(getRowDataIndex(Product,key,parameters2[key]["var13_1"],0)) + getFloat(getRowDataIndex(Product,key,parameters2[key]["var13_2"],0)) + getFloat(getRowDataIndex(Product,key,parameters2[key]["var13_3"],0)) + getFloat(getRowDataIndex(Product,key,parameters2[key]["var13_4"],0)) + getFloat(getRowDataIndex(Product,key,parameters2[key]["var13_5"],0)) + getFloat(getRowDataIndex(Product,key,parameters2[key]["var13_7"],0)) + getFloat(getRowDataIndex(Product,key,parameters2[key]["var13_8"],0)) + getFloat(getRowDataIndex(Product,key,parameters2[key]["var13_9"],0)) + getFloat(getRowDataIndex(Product,key,parameters2[key]["var14"],0))
        var15 = getFloat(getRowDataIndex(Product,key,parameters2[key]["var15_1"],1)) + getFloat(getRowDataIndex(Product,key,parameters2[key]["var15_2"],1)) + getFloat(getRowDataIndex(Product,key,parameters2[key]["var15_3"],1)) + getFloat(getRowDataIndex(Product,key,parameters2[key]["var15_4"],1)) + getFloat(getRowDataIndex(Product,key,parameters2[key]["var15_5"],1)) + getFloat(getRowDataIndex(Product,key,parameters2[key]["var15_7"],1)) + getFloat(getRowDataIndex(Product,key,parameters2[key]["var15_8"],1))
        var16 = getFloat(getRowDataIndex(Product,key,parameters2[key]["var15_1"],0)) + getFloat(getRowDataIndex(Product,key,parameters2[key]["var15_2"],0)) + getFloat(getRowDataIndex(Product,key,parameters2[key]["var15_3"],0)) + getFloat(getRowDataIndex(Product,key,parameters2[key]["var15_4"],0)) + getFloat(getRowDataIndex(Product,key,parameters2[key]["var15_5"],0)) + getFloat(getRowDataIndex(Product,key,parameters2[key]["var15_7"],0)) + getFloat(getRowDataIndex(Product,key,parameters2[key]["var15_8"],0)) + getFloat(getRowDataIndex(Product,key,parameters2[key]["var16"],0))

        var22 = getFloat(getRowDataIndex(Product,key,parameters2[key]["var11"],3))
        var23 = getFloat(getRowDataIndex(Product,key,parameters2[key]["var11"],4))

        var24 = getFloat(getRowDataIndex(Product,key,parameters2[key]["var13_1"],4)) +getFloat(getRowDataIndex(Product,key,parameters2[key]["var13_3"],4)) + getFloat(getRowDataIndex(Product,key,parameters2[key]["var13_7"],4)) + getFloat(getRowDataIndex(Product,key,parameters2[key]["var13_9"],4))

        var25 = getFloat(getRowDataIndex(Product,key,parameters2[key]["var13_1"],3)) +getFloat(getRowDataIndex(Product,key,parameters2[key]["var13_3"],3)) + getFloat(getRowDataIndex(Product,key,parameters2[key]["var13_7"],3)) + getFloat(getRowDataIndex(Product,key,parameters2[key]["var13_9"],3))

        var26 = getFloat(getRowDataIndex(Product,key,parameters2[key]["var15_1"],4)) +getFloat(getRowDataIndex(Product,key,parameters2[key]["var15_3"],4)) + getFloat(getRowDataIndex(Product,key,parameters2[key]["var15_7"],4))

        var27 = getFloat(getRowDataIndex(Product,key,parameters2[key]["var15_1"],3)) +getFloat(getRowDataIndex(Product,key,parameters2[key]["var15_3"],3)) + getFloat(getRowDataIndex(Product,key,parameters2[key]["var15_7"],3))


additonOfParamenters = Var_1 + Var_2 + Var_3 + Var_4 + Var_8 + Var_27
Var_7 = getFloat(getnumberOfjumpRealease(Product))

if lcnOneTimeUpgradeCon.Rows.Count > 0:
    controllersValue = 0
    if getRowData(Product,"LCN_Design_Inputs_for_TPN_OTU_Upgrade","LCN_No_of_TPN_Controllers"):
        controllersValue = int(getRowData(Product,"LCN_Design_Inputs_for_TPN_OTU_Upgrade","LCN_No_of_TPN_Controllers"))
    totalHours = 0.00
    if controllersValue > 0:
        totalHours = 16 + (0.25 * controllersValue)
    for row in lcnOneTimeUpgradeCon.Rows:
        oldCalHrs = row["Calculated_Hrs"]
        finalHours = 0.00
        if row["Deliverable"] == "One Time TPN Updgrade":
            row["Calculated_Hrs"] = str(totalHours)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
    calculateTotals(lcnOneTimeUpgradeCon)

if ebrCon.Rows.Count > 0:
    for row in ebrCon.Rows:
        oldCalHrs = row["Calculated_Hrs"]
        if row["Deliverable"] == "HW/SW order to factory":
            row["Calculated_Hrs"] = str(calculateELCNHWSWOrder(Product))
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Installation":
            row["Calculated_Hrs"] = str(getEBRInstaltion(Product))
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "SAT":
            row["Calculated_Hrs"] = "4"
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
    calculateEMPEfforts(Product,ebrCon)
    calculateTotals(ebrCon)

if elcnCon.Rows.Count > 0:
    siteInstallationHours,SAT = calculateELCNSiteInstallationAndSAT(var17,var18,var11,var12,var13,var14,var15,var16,var22,var23,var24,var25,var26,var27,var1,var2,var3,var4,var7,var8,var9,var10,var5,var6,var21,var29,var28)
    for row in elcnCon.Rows:
        oldCalHrs = row["Calculated_Hrs"]
        if row["Deliverable"] == "Plan review & KOM":
            row["Calculated_Hrs"] = "8"
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "FEL Site Visit Data Gathering":
            row["Calculated_Hrs"] = "16"
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Migration DDS":
            row["Calculated_Hrs"] = "8"
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "SW_HW order":
            row["Calculated_Hrs"] = "4"
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Pre-FAT":
            row["Calculated_Hrs"] = "16"
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "FAT":
            row["Calculated_Hrs"] = "16"
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Site Installation":
            row["Calculated_Hrs"] = str(siteInstallationHours)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "SAT":
            row["Calculated_Hrs"] = str(SAT)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
    calculateEMPEfforts(Product,elcnCon)
    calculateTotals(elcnCon)

if orionConsoleCon.Rows.Count > 0:
    planReviewHours,documentation,inhouseEngineering,siteInstallationEAPS,siteInstallationEST1,SAT = getOrionConsoleLabourHours(Product)
    for row in orionConsoleCon.Rows:
        oldCalHrs = row["Calculated_Hrs"]
        if row["Deliverable"] == "Plan Review & Kick off meetings":
            row["Calculated_Hrs"] = str(planReviewHours)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "HW SW order to factory":
            row["Calculated_Hrs"] = "4"
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Documentation":
            row["Calculated_Hrs"] = str(documentation)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Inhouse Engineering":
            row["Calculated_Hrs"] = str(inhouseEngineering)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Site Installation - EAPS":
            row["Calculated_Hrs"] = str(siteInstallationEAPS)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Site Installation - EST1":
            row["Calculated_Hrs"] = str(siteInstallationEST1)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "SAT":
            row["Calculated_Hrs"] = str(SAT)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
    calculateEMPEfforts(Product,orionConsoleCon)
    calculateTotals(orionConsoleCon)

if ehpmCon.Rows.Count > 0:
    planReviewEAPS,planReviewESSS,felDataGathering,migrationDDS,integrationEPKS,swHwOrder,preFAT,FAT,siteInstallation,SAT = getEHPMLabourHours(Quote,Product)
    for row in ehpmCon.Rows:
        oldCalHrs = row["Calculated_Hrs"]
        if row["Deliverable"] == "Plan Review (Kickoffs) - EAPS":
            row["Calculated_Hrs"] = str(planReviewEAPS)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Plan Review (Kickoffs) - ESSS":
            row["Calculated_Hrs"] = str(planReviewESSS)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "FEL Site Visit Data Gathering":
            row["Calculated_Hrs"] = str(felDataGathering)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Migration DDS":
            row["Calculated_Hrs"] = str(migrationDDS)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Integration EPKS config DDS":
            row["Calculated_Hrs"] = str(integrationEPKS)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "SW_HW Order":
            row["Calculated_Hrs"] = str(swHwOrder)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Pre-FAT":
            row["Calculated_Hrs"] = str(preFAT)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "FAT":
            row["Calculated_Hrs"] = str(FAT)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Site Installation":
            row["Calculated_Hrs"] = str(siteInstallation)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "SAT":
            row["Calculated_Hrs"] = str(SAT)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
	calculateEMPEfforts(Product,ehpmCon)
    calculateTotals(ehpmCon)

if tpsCon.Rows.Count > 0:
    felDataGathering,migrationDocumentation,offSiteActivities,fatProcedure,preFAT,siteInstallationEAPS,siteInstallationEST1,SAT = getTPSLabourHours(Product)
    for row in tpsCon.Rows:
        oldCalHrs = row["Calculated_Hrs"]
        if row["Deliverable"] == "Plan Review & KOM":
            row["Calculated_Hrs"] = "4"
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "FEL Site Visit Data Gathering":
            row["Calculated_Hrs"] = str(felDataGathering)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Migration Documentation":
            row["Calculated_Hrs"] = str(migrationDocumentation)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "SW_HW order":
            row["Calculated_Hrs"] = "4"
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Off-site activities":
            row["Calculated_Hrs"] = str(offSiteActivities)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "FAT Procedure":
            row["Calculated_Hrs"] = str(fatProcedure)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Pre-FAT":
            row["Calculated_Hrs"] = str(preFAT)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "FAT":
            row["Calculated_Hrs"] = str(preFAT * 0.6)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Site Installation - EAPS":
            row["Calculated_Hrs"] = str(siteInstallationEAPS)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Site Installation - EST1":
            row["Calculated_Hrs"] = str(siteInstallationEST1)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "SAT":
            row["Calculated_Hrs"] = str(SAT)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
    calculateEMPEfforts(Product,tpsCon)
    calculateTotals(tpsCon)

if tcmiCon.Rows.Count > 0:
    felSiteDataGathering,migrationDDS,siteInstallation,SAT = getTCMILabourHours(Product)
    for row in tcmiCon.Rows:
        oldCalHrs = row["Calculated_Hrs"]
        if row["Deliverable"] == "Plan Review & Kick off meetings":
            row["Calculated_Hrs"] = "2"
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "FEL Site Visit Data Gathering":
            row["Calculated_Hrs"] = str(felSiteDataGathering)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Migration DDS":
            row["Calculated_Hrs"] = str(migrationDDS)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Site Installation":
            row["Calculated_Hrs"] = str(siteInstallation)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "SAT":
            row["Calculated_Hrs"] = str(SAT)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
    calculateTotals(tcmiCon)

if ehpmhartioCon.Rows.Count > 0:
    documentation, commissioning, siteInstallation = getEHPMHARTIOLabourHours(Product)
    for row in ehpmhartioCon.Rows:
        oldCalHrs = row["Calculated_Hrs"]
        if row["Deliverable"] == "Plan Review & Kick off meetings":
            row["Calculated_Hrs"] = "2"
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "HW SW order to factory":
            row["Calculated_Hrs"] = "2"
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Documentation":
            row["Calculated_Hrs"] = str(documentation)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Site Installation":
            row["Calculated_Hrs"] = str(siteInstallation)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Commissioning":
            row["Calculated_Hrs"] = str(commissioning)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
    calculateEMPEfforts(Product,ehpmhartioCon)
    calculateTotals(ehpmhartioCon)

if c200migrationCon.Rows.Count > 0:
    migrationScenarioCon = getContainer(Product,'C200_Migration_Scenario_Cont').Rows
    for row in migrationScenarioCon:
        migrationScenario = row['C200_Select_the_Migration_Scenario']
        break
    if migrationScenario in ['C200 to C300','']:
        felSiteDataGathering,inHouseEngineering,preFat,migrationDDS,fat,sat,siteInstallation =  getC200MigrationLabourHours(Product)
        for row in c200migrationCon.Rows:
            oldCalHrs = row["Calculated_Hrs"]
            if row["Deliverable"] == "Plan Review & Kick off meetings":
                row["Calculated_Hrs"] = "18"
                row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
                row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
            elif row["Deliverable"] == "FEL Site Visit Data Gathering":
                row["Calculated_Hrs"] = str(felSiteDataGathering)
                row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
                row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
            elif row["Deliverable"] == "Migration DDS":
                row["Calculated_Hrs"] = str(migrationDDS)
                row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
                row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
            elif row["Deliverable"] == "SW_HW Order":
                row["Calculated_Hrs"] = "8"
                row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
                row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
            elif row["Deliverable"] == "Inhouse Engineering":
                row["Calculated_Hrs"] = str(inHouseEngineering)
                row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
                row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
            elif row["Deliverable"] == "Pre- FAT":
                row["Calculated_Hrs"] = str(preFat)
                row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
                row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
            elif row["Deliverable"] == "FAT":
                row["Calculated_Hrs"] = str(fat)
                row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
                row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
            elif row["Deliverable"] == "Site Installation":
                row["Calculated_Hrs"] = str(siteInstallation)
                row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
                row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
            elif row["Deliverable"] == "SAT":
                row["Calculated_Hrs"] = str(sat)
                row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
                row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        calculateTotals(c200migrationCon)
    elif migrationScenario == 'C200 to ControlEdge UOC':
        felSiteDataGathering,migrationDocumentation,inHouseEngineering,preFAT,fat,siteInstallationEaps,sat,siteInstallationEST1 =  getC200MigrationLabourHours(Product)
        for row in c200migrationCon.Rows:
            oldCalHrs = row["Calculated_Hrs"]
            if row["Deliverable"] == "Plan Review & Kick off meetings":
                row["Calculated_Hrs"] = "4"
                row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
                row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
            elif row["Deliverable"] == "FEL Site Visit Data Gathering":
                row["Calculated_Hrs"] = str(felSiteDataGathering)
                row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
                row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
            elif row["Deliverable"] == "Migration DDS":
                row["Calculated_Hrs"] = str(migrationDocumentation)
                row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
                row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
            elif row["Deliverable"] == "SW_HW Order":
                row["Calculated_Hrs"] = "4"
                row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
                row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
            elif row["Deliverable"] == "Inhouse Engineering":
                row["Calculated_Hrs"] = str(inHouseEngineering)
                row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
                row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
            elif row["Deliverable"] == "Pre- FAT":
                row["Calculated_Hrs"] = str(preFAT)
                row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
                row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
            elif row["Deliverable"] == "FAT":
                row["Calculated_Hrs"] = str(fat)
                row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
                row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
            elif row["Deliverable"] == "Site Installation - EAPS":
                row["Calculated_Hrs"] = str(siteInstallationEaps)
                row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
                row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
            elif row["Deliverable"] == "Site Installation - EST1":
                row["Calculated_Hrs"] = str(siteInstallationEST1)
                row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
                row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
            elif row["Deliverable"] == "SAT":
                row["Calculated_Hrs"] = str(sat)
                row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
                row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        calculateEMPEfforts(Product,c200migrationCon)
        calculateTotals(c200migrationCon)

if cbecCon.Rows.Count > 0:
    migrationDDS,inhouseEngineering,felSiteVisitDataGathering,fat,siteInstallation,sat = getCBECLabourHours(Product)
    for row in cbecCon.Rows:
        oldCalHrs = row["Calculated_Hrs"]
        if row["Deliverable"] == "Plan Review (Kickoffs)":
            row["Calculated_Hrs"] = "4"
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "FEL Site Visit Data Gathering":
            row["Calculated_Hrs"] = str(felSiteVisitDataGathering)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Migration DDS":
            row["Calculated_Hrs"] = str(migrationDDS)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Inhouse Engineering":
            row["Calculated_Hrs"] = str(inhouseEngineering)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "SW_HW Order":
            row["Calculated_Hrs"] = "6"
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "FAT":
            row["Calculated_Hrs"] = str(fat)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Site Installation":
            row["Calculated_Hrs"] = str(siteInstallation)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "SAT":
            row["Calculated_Hrs"] = str(sat)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
    calculateTotals(cbecCon)

if projectManagementCon.Rows.Count > 0:
    pmOtherActivities,paOtherActivities,paMonthlyProjectManagement,pmEngineeringManagement = getProjectMangementHours(Product)
    for row in projectManagementCon.Rows:
        oldCalHrs = row["Calculated_Hrs"]
        if row["Deliverable"] == "PM Engineering Management":
            row["Calculated_Hrs"] = str(pmEngineeringManagement)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "PM Other activities":
            row["Calculated_Hrs"] = str(pmOtherActivities)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "PA Monthly Project Management":
            row["Calculated_Hrs"] = str(paMonthlyProjectManagement)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "PA Other activities":
            row["Calculated_Hrs"] = str(paOtherActivities)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
    calculateTotals(projectManagementCon)