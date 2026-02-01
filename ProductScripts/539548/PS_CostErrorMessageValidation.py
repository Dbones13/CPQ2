def CostValidation(container):
    i = 0
    deliverables = ''
    for row in container.Rows:
        if i in (0,1):
            i += 1
            continue
        i += 1
        deliverable = row['Deliverable']
        GES_Eng_Split = FO_Eng_Split = FO_Eng_Cost = GES_Eng_Cost = 0
        if row.GetColumnByName('GES_Eng_Percentage_Split').Value not in ('','0'):
            GES_Eng_Split = float(row.GetColumnByName('GES_Eng_Percentage_Split').Value)
        if row.GetColumnByName('FO_Eng_Percentage_Split').Value not in ('','0'):
            FO_Eng_Split = float(row.GetColumnByName('FO_Eng_Percentage_Split').Value)
        if row.GetColumnByName('Regional_Cost').Value not in ('','0'):
            FO_Eng_Cost = float(row.GetColumnByName('Regional_Cost').Value)
        if row.GetColumnByName('GES_Regional_Cost').Value not in ('','0'):
            GES_Eng_Cost = float(row.GetColumnByName('GES_Regional_Cost').Value)
        FO_Eng = row.GetColumnByName('FO_Eng').Value
        GES_Eng = row.GetColumnByName('GES_Eng').Value
        finalHrs = row.GetColumnByName('Final_Hrs').Value
        if (finalHrs not in ('','0','0.0') and ((FO_Eng != '' and FO_Eng != 'None' and FO_Eng_Cost == 0 and FO_Eng_Split > 0) or (GES_Eng != '' and GES_Eng != 'None' and GES_Eng_Cost == 0 and GES_Eng_Split > 0))):
            deliverables = deliverables + " - " +str(deliverable) + "<br>"
    return deliverables

laborCont = ['MSID_Labor_FDM_Upgrade_Con', 'MSID_Labor_OPM_Engineering', 'MSID_Labor_LM_to_ELMM_Con',
    'MSID_Labor_FSC_to_SM_con', 'MSID_Labor_xPM_to_C300_Migration_Con', 'MSID_Labor_CB-EC_Upgrade_to_C300-UHIO_con',
    'MSID_Labor_C200_Migration_Con', 'MSID_Labor_TCMI_Con', 'MSID_Labor_EHPM_HART_IO_Con', 'MSID_Labor_Orion_Console_Con',
    'MSID_Labor_EHPM_C300PM_Con', 'MSID_Labor_TPS_TO_EXPERION_Con', 'MSID_Labor_ELCN_Con', 'MSID_Labor_EBR_Con',
    'MSID_Labor_LCN_One_Time_Upgrade_Engineering', 'MSID_Labor_Project_Management', 'MSID_Additional_Custom_Deliverables',
    'MSID_Labor_FSC_to_SM_audit_Con', 'MSID_Labor_XP10_Actuator_Upgrade_con', 'MSID_Labor_Graphics_Migration_con',
    'MSID_Labor_FSCtoSM_IO_con', 'MSID_Labor_CD_Actuator_con', 'MSID_Labor_CWS_RAE_Upgrade_con', '3rd_Party_PLC_UOC_Labor',
    'MSID_Labor_Virtualization_con', 'MSID_Labor_QCS_RAE_Upgrade_con', 'MSID_Labor_Generic_System1_Cont',
    'MSID_Labor_Generic_System2_Cont', 'MSID_Labor_Generic_System3_Cont', 'MSID_Labor_Generic_System4_Cont',
    'MSID_Labor_Generic_System5_Cont', 'MSID_Labor_TPA_con', 'MSID_Labor_FSC_to_SM_IO_Audit_Con', 'MSID_Labor_ELEPIU_con']

Product.Attr('ErrorMessage').AssignValue('')
laborMessage = 'Cost is not available for selected resource. Please select different resource or different Execution Country.Deliverables to look into: <br>'
laborMessage1 = ''
count = 0
for cont in laborCont:
    if Product.Attr(cont).Allowed:
        container = Product.GetContainerByName(cont)
        deliverables = CostValidation(container)
        if len(deliverables) > 0:
            count += 1
            laborMessage1 += deliverables

if count > 0:
    message = laborMessage + '<br>' + laborMessage1
    Product.Attr('ErrorMessage').AssignValue(message)