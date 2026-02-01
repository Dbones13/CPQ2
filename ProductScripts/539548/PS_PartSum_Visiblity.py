def getActiveTab():
    for tab in Product.Tabs:
        if tab.IsSelected:
            return tab.Name

currentTab = getActiveTab()
subprdcont = Product.GetContainerByName("CONT_MSID_SUBPRD")
prdlist = []
for row in subprdcont.Rows:
    prodRow = row.Product.Name
    prdlist.append(prodRow)

if currentTab == 'Part Summary':

    prtsumcont = {
            "OPM": "MSID_OPM_Added_Parts_Common_Container",
            "LCN One Time Upgrade": "MSID_LCN_Added_Parts_Common_Container",
            "Non-SESP Exp Upgrade": "MSID_NON_SESP_Added_Parts_Common_Container",
            "EBR": "MSID_EBR_Added_Parts_Common_Container",
            "ELCN": "MSID_ELCN_Added_Parts_Common_Container",
            "Project Management": "MSID_PM_Added_Parts_Common_Container",
            "Orion Console": "MSID_Orion_Console_Added_Parts_Common_Container",
            "EHPM/EHPMX/ C300PM": "MSID_EHPM_C300PM_Added_Parts_Common_Container",
            "TPS to Experion": "MSID_TPS_EXP_Added_Parts_Common_Container",
            "TCMI": "MSID_TCMI_Added_Parts_Common_Container",
            "LM to ELMM ControlEdge PLC": "MSID_LM_TO_ELMM_Added_Parts_Common_Container",
            "Spare Parts": "MSID_Spare_Parts_Added_Parts_Common_Container",
            "EHPM HART IO": "MSID_EHPM_HART_IO_Added_Parts_Common_Container",
            "C200 Migration": "MSID_C200_Migration_Added_Parts_Common_Container",
            "CB-EC Upgrade to C300-UHIO": "MSID_CB_EC_Added_Parts_Common_Container",
            "xPM to C300 Migration": "MSID_xPM_C300_Added_Parts_Common_Container",
            "FDM Upgrade 1": "MSID_FDM_Upgrade_1_Added_Parts_Common_Container",
            "FDM Upgrade 2": "MSID_FDM_Upgrade_2_Added_Parts_Common_Container",
            "FDM Upgrade 3": "MSID_FDM_Upgrade_3_Added_Parts_Common_Container",
            "FSC to SM": "MSID_FSC_to_SM_Added_Parts_Common_Container",
            "THIRD_PARTY" : "MSID_Third_Party_Added_Parts_Common_Container",
            "XP10 Actuator Upgrade": "MSID_XP10_Actuator_Added_Parts_Common_Container",
            "CWS RAE Upgrade": "MSID_CWS_RAE_Upgrade_Added_Parts_Common_Container",
            "Graphics Migration": "MSID_Graphics_Added_Parts_Common_Container",
            "FSC to SM IO Migration": "MSID_FSCtoSM_IO_Added_Parts_Common_Container",
            "CD Actuator I-F Upgrade": "MSID_CD_Actuator_Added_Parts_Common_Container",
            "3rd Party PLC to ControlEdge PLC/UOC": "MSID_Third_Party_PLC_Added_Parts_Common_Container",
            "Virtualization System Migration": "MSID_Virtualization_Added_Parts_Common_Container",
            "QCS RAE Upgrade": "MSID_QCS_Added_Parts_Common_Container",
            "TPA/PMD Migration": "MSID_TPA_Added_Parts_Common_Container",
            "ELEPIU ControlEdge RTU Migration Engineering": "MSID_ELEPIU_Added_Parts_Common_Container",
            "GS_Migration_1": "MSID_GS1_Added_Parts_Common_Container",
            "GS_Migration_2": "MSID_GS2_Added_Parts_Common_Container",
            "GS_Migration_3": "MSID_GS3_Added_Parts_Common_Container",
            "GS_Migration_4": "MSID_GS4_Added_Parts_Common_Container",
            "GS_Migration_5": "MSID_GS5_Added_Parts_Common_Container",
            "FSC_to_SM_audit": "MSID_FSC_to_SM_audit_Added_Parts_Common_Container",
            "FSCtoSM_IO_AUDIT": "MSID_FSCtoSM_IO_audit_Added_Parts_Common_Container",
        }
    for key in prtsumcont.keys():
        if key in prdlist:
            Trace.Write('key  '+str(key))
            Product.AllowAttr(prtsumcont[key])
        else:
            Trace.Write('keyelse '+str(key))
            Product.DisallowAttr(prtsumcont[key])

'''if currentTab == 'Labor Deliverables':
    # Trace.Write("Labor deliverabless tab")
    labor_deliverables_cont = {
        "OPM": [
            "MSID_Labor_OPM_Engineering",
            "OPM_Execution_Year",
            "OPM_Execution_Country" ,
            "OPM_Adjustment_Productivity",
            "MSID_Labor_FO_Part_Number",

        ],
        "EBR": [
            "MSID_Labor_EBR_Con",
            "EBR_Execution_Year",
            "EBR_Execution_Country",
            "EBR_Adjustment_Productivity",
        ],
        "LCN One Time Upgrade": [
            "MSID_Labor_LCN_One_Time_Upgrade_Engineering",
            "LCN_Execution_Country",
            "LCN_Execution_Year",
            "LCN_Adjustment_Productivity",
        ],
        "XP10 Actuator Upgrade": [
            "MSID_Labor_XP10_Actuator_Upgrade_con",
            "XP10_Actuator_Upgrade_Execution_Country",
            "XP10_Actuator_Upgrade_Adjustment_Productivity",
            "XP10_Actuator_Upgrade_Execution_Year",
        ],
        "FDM Upgrade 3" : [
            "FDM_Upgrade_3_Additional_Configuration",
        ],
        "FDM Upgrade 2" : [
            "FDM_Upgrade_2_Hardware_to_host_FDM_Server",
        ],
        "FDM Upgrade 1" : [
            "MSID_Labor_FDM_Upgrade_Con",
            "FDM_Upgrade_Adjustment_Productivity",
            "FDM_Upgrade_Execution_Country",
            "FDM_Upgrade_Execution_Year",
        ],
        "LM to ELM ControlEdge PLC" : [
            "MSID_Labor_LM_to_ELMM_Con",
            "LM_to_ELMM_Execution_Country",
            "LM_to_ELMM_Adjustment_Productivity",
            "LM_to_ELMM_Execution_Year",
        ],
        "xPM to C300 Migration": [
            "MSID_Labor_xPM_to_C300_Migration_Con",
            "xPM_to_C300_Migration_Execution_Year",
            "xPM_to_C300_Migration_Adjustment_Productivity",
            "xPM_to_C300_Migration_Execution_Country",
        ],
        "CB-EC Upgrade to C300-UHIO": [
            "MSID_Labor_CB-EC_Upgrade_to_C300-UHIO_con",
            "CB-EC_Upgrade_to_C300-UHIO_Execution_Year",
            "CB-EC_Upgrade_to_C300-UHIO_Adjustment_Productivity",
            "Labor_CB-EC_Upgrade_to_C300-UHIO_Message",
            "CB-EC_Upgrade_to_C300-UHIO_Execution_Country",
        ],
        "ELCN" : [
            "Labor_ELCN_Message",
            "MSID_Labor_ELCN_Con",
            "ELCN_Execution_Year",
            "ELCN_Execution_Country",
            "ELCN_Adjustment_Productivity",
        ],
        "C200 Migration": [
            "Labor_C200_Migration_Message",
            "C200_Migration_Adjustment_Productivity",
            "C200_Migration_Execution_Country",
            "C200_Migration_Execution_Year",
            "MSID_Labor_C200_Migration_Con",
        ],
        "TCMI" : [
            "TCMI_Adjustment_Productivity",
            "TCMI_Execution_Country",
            "TCMI_Execution_Year",
            "MSID_Labor_TCMI_Con",
            "Labor_TCMI_Message",
        ],
        "EHPM HART IO": [
            "EHPM_HART_IO_Adjustment_Productivity",
            "EHPM_HART_IO_Execution_Year",
            "EHPM_HART_IO_Execution_Country",
            "MSID_Labor_EHPM_HART_IO_Con",
            "Labor_EHPM_HART_IO_Message",
        ],
        "Orion Console": [
            "Labor_Orion_Console_Message",
            "MSID_Labor_Orion_Console_Con",
            "Orion_Console_Adjustment_Productivity",
            "Orion_Console_Execution_Country",
            "Orion_Console_Execution_Year",
        ],
        "EHPM/EHPMX/ C300PM": [
            "EHPM_C300PM_Execution_Year",
            "EHPM_C300PM_Adjustment_Productivity",
            "EHPM_C300PM_Execution_Country",
            "Labor_EHPM_C300PM_Message",
            "MSID_Labor_EHPM_C300PM_Con",
        ],
        "TPS to Experion": [
            "Labor_TPS_TO_EXPERION_Message",
            "MSID_Labor_TPS_TO_EXPERION_Con",
            "TPS_TO_EXPERION_Adjustment_Productivity",
            "TPS_TO_EXPERION_Execution_Country",
            "TPS_TO_EXPERION_Execution_Year",
        ],
        "FSC to SM IO Migration" : [
            "MSID_Labor_FSCtoSM_IO_con",
            "FSCtoSM_IO_Adjustment_Productivity",
            "FSCtoSM_IO_Execution_Country",
            "FSCtoSM_IO_Execution_Year",
            "FSC_to_SM_IO_audit_Execution_Country",
            "FSC_to_SM_IO_audit_Execution_Year",
            "MSID_Labor_Fsc_SM_IO_Audit_Productivity",
            "MSID_Labor_FSC_to_SM_IO_Audit_Con",
        ],
        "FSC to SM" : [
            "FSC_to_SM_Execution_Year",
            "FSC_to_SM_Adjustment_Productivity",
            "FSC_to_SM_Execution_Country",
            "MSID_Labor_FSC_to_SM_con",
            "FSC_to_SM_audit_Execution_Country",
            "FSC_to_SM_audit_Adjustment_Productivity",
            "FSC_to_SM_audit_Execution_Year",
            "MSID_Labor_FSC_to_SM_audit_Con",
        ],
        "Graphics Migration" : [
            "Graphics_Migration_Execution_Country",
            "Graphics_Migration_Execution_Year",
            "Graphics_Migration_Adjustment_Productivity",
            "MSID_Labor_Graphics_Migration_con",
        ],
        "XP10 Actuator Upgrade" : [
            "MSID_Labor_XP10_Actuator_Upgrade_con",
            "XP10_Actuator_Upgrade_Execution_Country",
            "XP10_Actuator_Upgrade_Adjustment_Productivity",
            "XP10_Actuator_Upgrade_Execution_Year",
        ],
        "CD Actuator I-F Upgrade" : [
            "MSID_Labor_CD_Actuator_con",
            "CD_Actuator_Adjustment_Productivity",
            "CD_Actuator_Execution_Country",
            "CD_Actuator_Execution_Year",
        ],
        "ELEPIU ControlEdge RTU Migration Engineering" : [
            "ELEPIU_Adjustment_Productivity",
            "ELEPIU_Execution_Year",
            "ELEPIU_Execution_Country",
            "MSID_Labor_ELEPIU_con",
        ],
        "CWS RAE Upgrade" : [
            "MSID_Labor_CWS_RAE_Upgrade_con",
            "CWS_RAE_Upgrade_Adjustment_Productivity",
            "CWS_RAE_Upgrade_Execution_Country",
            "CWS_RAE_Upgrade_Execution_Year",
            "Labor_CWS_RAE_Upgrade_Message",
        ],
        "GS_Migration_1" : [
            "MSID_Generic_System_Products_Count", #tobeconfirmed
            "MSID_Labor_Generic_System1_Cont", 
            "Generic1_Productivity",
            "Generic1_Execution_Year",
            "Generic1_Execution_Country",
        ],
        "GS_Migration_2" : [
            "MSID_Labor_Generic_System2_Cont",
            "Generic2_Productivity",
            "Generic2_Execution_Year",
            "Generic2_Execution_Country",

        ],
        "GS_Migration_3" : [
            "MSID_Labor_Generic_System3_Cont",
            "Generic3_Productivity",
            "Generic3_Execution_Year",
            "Generic3_Execution_Country",
        ],
        "GS_Migration_4" : [
            "MSID_Labor_Generic_System4_Cont",
            "Generic4_Productivity",
            "Generic4_Execution_Year",
            "Generic4_Execution_Country",
        ],
        "GS_Migration_5" : [
            "MSID_Labor_Generic_System5_Cont",
            "Generic5_Productivity",
            "Generic5_Execution_Year",
            "Generic5_Execution_Country",
        ],
        "3rd Party PLC to ControlEdge PLC/UOC/UOC": [
            "3rd_Party_PLC_UOC_Labor_Execution_year",
            "3rd_Party_PLC_UOC_Labor_Execution_country",
            "3rd_Party_PLC_UOC_Labor_Productivity",
            "3rd_Party_PLC_UOC_Labor",
        ],
        "Virtualization System": [
            "MSID_Labor_Virtualization_con",
            "Labor_Virtualization_Message",
            "Virtualization_Execution_Country",
            "Virtualization_Execution_Year",
            "Virtualization_Adjustment_Productivity",
        ],
        "QCS RAE Upgrade": [
            "MSID_Labor_QCS_RAE_Upgrade_con",
            "QCS_RAE_Upgrade_Adjustment_Productivity",
            "QCS_RAE_Upgrade_Execution_Year",
            "QCS_RAE_Upgrade_Execution_Country",
        ],
        "TPA/PMD Migration": [
            "MSID_Labor_TPA_con",
            "TPA_Execution_Country",
            "TPA_Adjustment_Productivity",
            "TPA_Execution_Year",
            "Labor_TPA_Message",
        ],
        "hidden" : [#tobeconfirmed
            "MSID_Labor_Message",
            "OPM_LaborAMT_Details",
            "MSID_Active_Service_Contract",
            "MSID_Labor_Apply_Deliverables",
            "Msg_MSID_OPM_Engineering",
            "Msg_MSID_EBR",
            "Msg_MSID_LCN_One_Time",
            "Msg_MSID_XP10_Actuator_Upgrade",
            "Msg_MSID_FDM_Upgrade",
            "Msg_MSID_LM_to_ELMM",
            "Msg_MSID_xPM_to_C300_Migration",
            "Msg_MSID_CB-EC_Upgrade_to_C300-UHIO",
            "Msg_MSID_C200_Migration",
            "Msg_MSID_TCMI",
            "Msg_MSID_EHPM_HART_IO",
            "Msg_MSID_Orion_Console",
            "Msg_MSID_EHPM_C300PM",
            "Msg_MSID_TPS_TO_EXPERION",
            "Msg_MSID_FSCtoSM_IO",
            "Msg_MSID_FSC_to_SM_IO_audit",
            "Msg_MSID_FSC_to_SM",
            "Msg_MSID_FSC_to_SM_audit",
            "Msg_MSID_Graphics_Migration",
            "Msg_MSID_XP10_Actuator_Upgrade",
            "Msg_MSID_CD_Actuator",
            "Msg_MSID_ELEPIU",
            "Msg_MSID_CWS_RAE_Upgrade",
            "Msg_Generic1",
            "Msg_Generic2",
            "Msg_Generic3",
            "Msg_Generic4",
            "Msg_Generic5",
            "Msg_MSID_3rd_party_PLC_UOC",
            "Msg_MSID_Virtualization",
            "Msg_MSID_QCS_RAE_Upgrade",
            "Msg_MSID_TPA",
        ]
    }

    for key in labor_deliverables_cont.keys():
        if key in prdlist:
            # Trace.Write('labor key  ' + str(labor_deliverables_cont[key]))
            for attr in labor_deliverables_cont[key]:
                Product.AllowAttr(attr)
        else:
            # Trace.Write('labor else key   '+ str(labor_deliverables_cont[key]))
            for attr in labor_deliverables_cont[key]:
                Product.DisallowAttr(attr)
                '''