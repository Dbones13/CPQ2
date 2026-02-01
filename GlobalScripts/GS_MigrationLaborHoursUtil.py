def getContainer(Product,Name):
    return Product.GetContainerByName(Name)

def getRowData(Product,container,column):
    Container = getContainer(Product,container)
    for row in Container.Rows:
        return row[column]

def getRowDataIndex(Product,container,column,index):
    Container = getContainer(Product,container)
    for row in Container.Rows:
        if row.RowIndex == index:
            return row[column]

def getFloat(Var):
    if Var:
        return float(Var)
    return 0

def getTotalEngHours(Product,container):
    totalFinalHours = 0
    for row in getContainer(Product,container).Rows:
        if row["Deliverable"] == "Total":
            totalFinalHours += getFloat(row["Final_Hrs"])
    return totalFinalHours

def getProjectMangementHours(Product):
    selectedProducts = Product.Attr('MSID_Selected_Products').GetValue().split('<br>')
    totalOpmFinalHours = getTotalEngHours(Product,"MSID_Labor_OPM_Engineering") if "OPM" in selectedProducts else 0
    totalLcnFinalHours = getTotalEngHours(Product,"MSID_Labor_LCN_One_Time_Upgrade_Engineering") if "LCN One Time Upgrade" in selectedProducts else 0
    totalEbrFinalHours = getTotalEngHours(Product,"MSID_Labor_EBR_Con") if "EBR" in selectedProducts else 0
    totalElcnFinalHours = getTotalEngHours(Product,"MSID_Labor_ELCN_Con") if "ELCN" in selectedProducts else 0
    totalOrionConsoleHours = getTotalEngHours(Product,"MSID_Labor_Orion_Console_Con") if "Orion Console" in selectedProducts else 0
    totalEHPMHours = getTotalEngHours(Product,"MSID_Labor_EHPM_C300PM_Con") if "EHPM/EHPMX/ C300PM" in selectedProducts else 0
    totalTPSHours = getTotalEngHours(Product,"MSID_Labor_TPS_TO_EXPERION_Con") if "TPS to Experion" in selectedProducts else 0
    totalTCMIHours = getTotalEngHours(Product,"MSID_Labor_TCMI_Con") if "TCMI" in selectedProducts else 0
    totalEHPMHARTIOHours = getTotalEngHours(Product,"MSID_Labor_EHPM_HART_IO_Con") if "EHPM HART IO" in selectedProducts else 0
    totalC200Hours = getTotalEngHours(Product,"MSID_Labor_C200_Migration_Con") if "C200 Migration" in selectedProducts else 0
    totalfsctosmHours = getTotalEngHours(Product,"MSID_Labor_FSC_to_SM_con") if "FSC to SM" in selectedProducts else 0
    totalfsctosmauditHours = getTotalEngHours(Product,"MSID_Labor_FSC_to_SM_audit_Con") if "FSC to SM" in selectedProducts else 0
    totalfdmupgradeHours = getTotalEngHours(Product,"MSID_Labor_FDM_Upgrade_Con") if "FDM Upgrade" in selectedProducts else 0
    totalXP10Hours = getTotalEngHours(Product,"MSID_Labor_XP10_Actuator_Upgrade_con") if "XP10 Actuator Upgrade" in selectedProducts else 0
    totalcbecHours = getTotalEngHours(Product,"MSID_Labor_CB-EC_Upgrade_to_C300-UHIO_con") if "CB-EC Upgrade to C300-UHIO" in selectedProducts else 0
    totalxPMHours = getTotalEngHours(Product,"MSID_Labor_xPM_to_C300_Migration_Con") if "xPM to C300 Migration" in selectedProducts else 0
    totalGraphicsHours = getTotalEngHours(Product,"MSID_Labor_Graphics_Migration_con") if "Graphics Migration" in selectedProducts else 0
    totallmHours = getTotalEngHours(Product,"MSID_Labor_LM_to_ELMM_Con") if "LM to ELMM ControlEdge PLC" in selectedProducts else 0
    totalCDActuatorHours = getTotalEngHours(Product,"MSID_Labor_CD_Actuator_con") if "CD Actuator I-F Upgrade" in selectedProducts else 0
    totalfscsmioHours = getTotalEngHours(Product,"MSID_Labor_FSCtoSM_IO_con") if "FSC to SM IO Migration" in selectedProducts else 0
    totalCWSHours = getTotalEngHours(Product,"MSID_Labor_CWS_RAE_Upgrade_con") if "CWS RAE Upgrade" in selectedProducts else 0
    totalplcuocHours = getTotalEngHours(Product,"3rd_Party_PLC_UOC_Labor") if "3rd Party PLC to ControlEdge PLC/UOC" in selectedProducts else 0
    totalVirtHours = getTotalEngHours(Product,"MSID_Labor_Virtualization_con") if "Virtualization System" in selectedProducts else 0
    totalQCSHours = getTotalEngHours(Product,"MSID_Labor_QCS_RAE_Upgrade_con") if "QCS RAE Upgrade" in selectedProducts else 0
    totalGS1Hours = getTotalEngHours(Product,"MSID_Labor_Generic_System1_Cont") if "Generic System" in selectedProducts else 0
    totalGS2Hours = getTotalEngHours(Product,"MSID_Labor_Generic_System1_Cont") if "Generic System" in selectedProducts else 0
    totalGS3Hours = getTotalEngHours(Product,"MSID_Labor_Generic_System1_Cont") if "Generic System" in selectedProducts else 0
    totalGS4Hours = getTotalEngHours(Product,"MSID_Labor_Generic_System1_Cont") if "Generic System" in selectedProducts else 0
    totalGS5Hours = getTotalEngHours(Product,"MSID_Labor_Generic_System1_Cont") if "Generic System" in selectedProducts else 0
    totalTPAHours = getTotalEngHours(Product,"MSID_Labor_TPA_con") if "TPA/PMD Migration" in selectedProducts else 0
    EngHours = totalOpmFinalHours + totalLcnFinalHours + totalEbrFinalHours + totalElcnFinalHours + totalOrionConsoleHours + totalEHPMHours + totalTPSHours + totalTCMIHours + totalEHPMHARTIOHours + totalC200Hours + totalcbecHours + totalxPMHours + totalfsctosmHours + totalfdmupgradeHours + totallmHours + totalfsctosmauditHours + totalXP10Hours + totalGraphicsHours + totalCDActuatorHours + totalfscsmioHours + totalCWSHours + totalplcuocHours + totalVirtHours + totalQCSHours  + totalGS1Hours + totalGS2Hours + totalGS3Hours + totalGS4Hours + totalGS5Hours + totalTPAHours

    pmOtherActivities = 0
    if EngHours > 0:
        pmOtherActivities = 24
    else:
        pmOtherActivities = 0

    paOtherActivities = 0
    if EngHours > 0:
        paOtherActivities = 8
    else:
        paOtherActivities = 0

    paMonthlyProjectManagement = 0
    if EngHours <= 160 :
        paMonthlyProjectManagement = 0
    else:
        paMonthlyProjectManagement = 16

    pmEngineeringManagement = 0
    if EngHours <= 160:
        pmEngineeringManagement = 0
    elif EngHours > 160 and EngHours <= 2000:
        pmEngineeringManagement = round((EngHours -160) * 0.1)
    else:
        pmEngineeringManagement = 176 + round((EngHours - 2000 -160) * 0.05)

    return pmOtherActivities,paOtherActivities,paMonthlyProjectManagement,pmEngineeringManagement