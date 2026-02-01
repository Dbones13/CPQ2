import GS_Approval_Labor_Migration
def clearvalues():
    for item in Quote.MainItems:
        if item.ProductName != "Trace Software" and item.ParentItemGuid =='':
            item["QI_Local_Labor"].Value = 0
            item["QI_Cross_Border_Labor"].Value = 0
            item["QI_GES_Work_GES_Location"].Value = 0
            item["QI_GES_Work_Non_GES_Location"].Value = 0

def process_labor_hours_Cyber(item,Quote):
    Local_Labor = Cross_Border_Labor = GES_Location = Non_GES_Location = 0
    container = []
    conNames = {
        "Cyber Generic System":"Generic_System_Activities",
        "SMX": "AR_SMX_Activities",
        "ASSESSMENT": "AR_Assessment_Activities",
        "PCN": "AR_PCNH_Activities",
        "MSS": "AR_MSS_Activities",
        "CYBER_APP_CNTRL": "AR_CAC_Activities",
        "Project Management": "Cyber_Labor_Project_Management"
        }


    for key, conName in conNames.items():
        con = item.SelectedAttributes.GetContainerByName(conName)
        if not con:
            continue
        else:
            container.append(conName)
    container = list(set([val for val in container if val]))
    laborHours = GS_Approval_Labor_Migration.getFinalHoursCyber(item, container, Quote)
    Local_Labor += laborHours.get("Local Labor", 0)
    Cross_Border_Labor += laborHours.get("Cross Border Labor", 0)
    GES_Location += laborHours.get("GES - Work @ GES Location", 0)
    Non_GES_Location += laborHours.get("GES - Work @ Non GES Location", 0)

    item["QI_Local_Labor"].Value = Local_Labor
    item["QI_Cross_Border_Labor"].Value = Cross_Border_Labor
    item["QI_GES_Work_GES_Location"].Value = GES_Location
    item["QI_GES_Work_Non_GES_Location"].Value = Non_GES_Location

def process_labor_hours_hci(item,Quote):
    Local_Labor = Cross_Border_Labor = GES_Location = Non_GES_Location = 0
    container = []
    if item.ProductName in ("PHD Labor","AFM Labor","Uniformance Insight Labor"):
        conNames = {"HCI Labor Eng":"HCI_PHD_EngineeringLabour","HCI Labor PM2":"HCI_PHD_ProjectManagement2","HCI Labor PM":"HCI_PHD_ProjectManagement","HCI Labor AD":"HCI_PHD_AdditionalDeliverables"}
    elif item.ProductName == "HCI Labor Upload":
        conNames = {"HCI Labor Upload":"AR_HCI_LABOR_CONTAINER"}
    for key, conName in conNames.items():
        con = item.SelectedAttributes.GetContainerByName(conName)
        if not con:
            continue
        else:
            container.append(conName)
    container = list(set([val for val in container if val]))
    laborHours = GS_Approval_Labor_Migration.getFinalHours_hci(item, container, Quote)
    Local_Labor += laborHours.get("Local Labor", 0)
    Cross_Border_Labor += laborHours.get("Cross Border Labor", 0)
    GES_Location += laborHours.get("GES - Work @ GES Location", 0)
    Non_GES_Location += laborHours.get("GES - Work @ Non GES Location", 0)

    item["QI_Local_Labor"].Value = Local_Labor
    item["QI_Cross_Border_Labor"].Value = Cross_Border_Labor
    item["QI_GES_Work_GES_Location"].Value = GES_Location
    item["QI_GES_Work_Non_GES_Location"].Value = Non_GES_Location

def process_labor_hours_winest(item, Quote):
    Local_Labor = Cross_Border_Labor = GES_Location = Non_GES_Location = 0
    contList = ["Winest Labor Container", "Winest Additional Labor Container"]
    laborHours = GS_Approval_Labor_Migration.getFinalHours_winest(item,contList,Quote)
    Local_Labor = laborHours.get("Local Labor", 0)
    Cross_Border_Labor = laborHours.get("Cross Border Labor", 0)
    GES_Location = laborHours.get("GES - Work @ GES Location", 0)
    Non_GES_Location = laborHours.get("GES - Work @ Non GES Location", 0)
    item["QI_Local_Labor"].Value = Local_Labor
    item["QI_Cross_Border_Labor"].Value = Cross_Border_Labor
    item["QI_GES_Work_GES_Location"].Value = GES_Location
    item["QI_GES_Work_Non_GES_Location"].Value = Non_GES_Location

def Quote_Items(quote):
    import GS_Approval_Labor_PRJT
    clearvalues()
    laborHours={}
    laborHours_prjt={}
    added_products=[]
    Local_Labor_prjt=0
    Cross_Border_Labor_prjt=0
    GES_Location_prjt=0
    Non_GES_Location_prjt=0
    fdm_upgrade_processed = False
    ct=0
    for item in Quote.MainItems:
        txt=item.PartNumber
        Quantity =0
        ct = ct+1
        if item.ProductTypeName =="Honeywell Labor" and item.ParentItemGuid =='' and item.ProductName != "HCI Labor Config":
            if txt in ('SVC_GES_P350B_IN','SVC_GES_P350B_CN','SVC_GES_P350B_RO','SVC_GES_P350B_UZ','SVC_GES_P335B_IN','SVC_GES_P335B_CN','SVC_GES_P335B_RO','SVC_GES_P335B_UZ','SVC_GES_P215B_IN','SVC_GES_P215B_CN','SVC_GES_P215B_RO','SVC_GES_P215B_UZ','SVC_GES_PLCB_IN','SVC_GES_PLCB_CN','SVC_GES_PLCB_RO','SVC_GES_PLCB_UZ','HPS_GES_P350B_IN','HPS_GES_P350B_CN','HPS_GES_P350B_RO','HPS_GES_P350B_UZ','HPS_GES_P335B_IN','HPS_GES_P335B_CN','HPS_GES_P335B_RO','HPS_GES_P335B_UZ','HPS_GES_P215B_IN','HPS_GES_P215B_CN','HPS_GES_P215B_RO','HPS_GES_P215B_UZ','HPS_GES_P215F_CN','HPS_GES_P215F_IN','HPS_GES_P215F_RO','HPS_GES_P215F_UZ','HPS_GES_P335F_CN','HPS_GES_P335F_IN','HPS_GES_P335F_RO','HPS_GES_P335F_UZ','SVC_GES_P350B_EG','SVC_GES_P335B_EG','SVC_GES_PLCB_EG','SVC_GES_P215B_EG','SVC_GES_P215F_EG'):
                item["QI_GES_Work_GES_Location"].Value = item.Quantity
            elif txt in ('SVC_GES_P350F_IN','SVC_GES_P350F_CN','SVC_GES_P350F_RO','SVC_GES_P350F_UZ','SVC_GES_P335F_IN','SVC_GES_P335F_CN','SVC_GES_P335F_RO','SVC_GES_P335F_UZ','SVC_GES_P215F_IN','SVC_GES_P215F_CN','SVC_GES_P215F_RO','SVC_GES_P215F_UZ','SVC_GES_PLCF_IN','SVC_GES_PLCF_CN','SVC_GES_PLCF_RO','SVC_GES_PLCF_UZ','HPS_GES_P350F_IN','HPS_GES_P350F_CN','HPS_GES_P350F_RO','HPS_GES_P350F_UZ','SVC_GES_P350F_EG','SVC_GES_P335F_EG','SVC_GES_P215B_EG','SVC_GES_P215F_EG'):
                item["QI_GES_Work_GES_Location"].Value = item.Quantity
            else:
                item["QI_Local_Labor"].Value = item.Quantity
        def process_labor_hours(item, msidContainer, fdm_upgrade_processed, is_msid_new=False):
            if msidContainer is None:
                Trace.Write("Error: msidContainer not found.")
                return  

            Local_Labor = Cross_Border_Labor = GES_Location = Non_GES_Location = 0

            for row in msidContainer.Rows:
                selectedProducts = row['Selected_Products'].split('<br>')
                container = []

                if row['Scope'] in ['LABOR', 'HW/SW/LABOR', 'HWSWLABOR']:
                    container.append("MSID_Labor_Project_Management")

                if not fdm_upgrade_processed:
                    if any(fdm in selectedProducts for fdm in ["FDM Upgrade 1", "FDM Upgrade 2", "FDM Upgrade 3"]):
                        container.append("MSID_Labor_FDM_Upgrade_Con")
                        fdm_upgrade_processed = True

                conditions = [
                    ("OPM", "MSID_Labor_OPM_Engineering"),
                    ("LCN One Time Upgrade", "MSID_Labor_LCN_One_Time_Upgrade_Engineering"),
                    ("EBR", "MSID_Labor_EBR_Con"),
                    ("ELCN", "MSID_Labor_ELCN_Con"),
                    ("Orion Console", "MSID_Labor_Orion_Console_Con"),
                    ("EHPM/EHPMX/ C300PM", "MSID_Labor_EHPM_C300PM_Con"),
                    ("TPS to Experion", "MSID_Labor_TPS_TO_EXPERION_Con"),
                    ("TCMI", "MSID_Labor_TCMI_Con"),
                    ("C200 Migration", "MSID_Labor_C200_Migration_Con"),
                    ("CB-EC Upgrade to C300-UHIO", "MSID_Labor_CB-EC_Upgrade_to_C300-UHIO_con"),
                    ("xPM to C300 Migration", "MSID_Labor_xPM_to_C300_Migration_Con"),
                    ("FSC to SM", "MSID_Labor_FSC_to_SM_con"),
                    ("FSC to SM", "MSID_Labor_FSC_to_SM_audit_Con"),
                    ("FSC to SM IO Migration", "MSID_Labor_FSCtoSM_IO_con"),
                    ("FSC to SM IO Migration", "MSID_Labor_FSC_to_SM_IO_Audit_Con"),
                    ("LM to ELMM ControlEdge PLC", "MSID_Labor_LM_to_ELMM_Con"),
                    ("EHPM HART IO", "MSID_Labor_EHPM_HART_IO_Con"),
                    ("XP10 Actuator Upgrade", "MSID_Labor_XP10_Actuator_Upgrade_con"),
                    ("Graphics Migration", "MSID_Labor_Graphics_Migration_con"),
                    ("CWS RAE Upgrade", "MSID_Labor_CWS_RAE_Upgrade_con"),
                    ("CD Actuator I-F Upgrade", "MSID_Labor_CD_Actuator_con"),
                    ("3rd Party PLC to ControlEdge PLC/UOC", "3rd_Party_PLC_UOC_Labor"),
                    ("Virtualization System", "MSID_Labor_Virtualization_con"),
                    ("Virtualization System Migration", "MSID_Labor_Virtualization_con"),
                    ("QCS RAE Upgrade", "MSID_Labor_QCS_RAE_Upgrade_con"),
                    ("TPA/PMD Migration", "MSID_Labor_TPA_con"),
                    ("ELEPIU ControlEdge RTU Migration Engineering", "MSID_Labor_ELEPIU_con"),
                    ("Project Management", "MSID_Labor_Project_Management"),
                    ("Generic System", "MSID_Labor_Generic_System1_Cont"),
                    ("Generic System Migration", "MSID_Labor_Generic_System1_Cont")
                ]

                for product, labor_code in conditions:
                    if product in selectedProducts and "Generic System Migration" not in selectedProducts:
                        container.append(labor_code)

                if is_msid_new:
                    generic_system_conditions = [
                        ("Generic System 1", "MSID_Labor_Generic_System1_Cont"),
                        ("Generic System 2", "MSID_Labor_Generic_System2_Cont"),
                        ("Generic System 3", "MSID_Labor_Generic_System3_Cont"),
                        ("Generic System 4", "MSID_Labor_Generic_System4_Cont"),
                        ("Generic System 5", "MSID_Labor_Generic_System5_Cont")
                    ]

                    for system, system_code in generic_system_conditions:
                        if row['Product Name'] == system and "Generic System Migration" in selectedProducts:
                            container.append(system_code)

                container = list(set([val for val in container if val]))

                laborHours = GS_Approval_Labor_Migration.getFinalHours(item, container, Quote, row.RowIndex)
                Local_Labor += laborHours.get("Local Labor", 0)
                Cross_Border_Labor += laborHours.get("Cross Border Labor", 0)
                GES_Location += laborHours.get("GES - Work @ GES Location", 0)
                Non_GES_Location += laborHours.get("GES - Work @ Non GES Location", 0)

            item["QI_Local_Labor"].Value = Local_Labor
            item["QI_Cross_Border_Labor"].Value = Cross_Border_Labor
            item["QI_GES_Work_GES_Location"].Value = GES_Location
            item["QI_GES_Work_Non_GES_Location"].Value = Non_GES_Location

        if item.ProductName == "Migration":
            added_products.append(item.ProductName)
            msidContainer = item.SelectedAttributes.GetContainerByName("Migration_MSID_Selection_Container")
            process_labor_hours(item, msidContainer, fdm_upgrade_processed)

        if item.ProductName == "MSID_New":
            added_products.append(item.ProductName)
            msidContainer = item.SelectedAttributes.GetContainerByName("CONT_MSID_SUBPRD")
            process_labor_hours(item, msidContainer, fdm_upgrade_processed, is_msid_new=True)
        if item.ProductName == "New / Expansion Project":
            added_products.append(item.ProductName)
            laborHours_prjt=GS_Approval_Labor_PRJT.labor_prjt(Quote, item)
            if laborHours_prjt is not None:
                Local_Labor_prjt = laborHours_prjt.get("Local Labor",0)
                Cross_Border_Labor_prjt = laborHours_prjt.get("Cross Border Labor",0)
                GES_Location_prjt = laborHours_prjt.get("GES - Work @ GES Location",0)
                Non_GES_Location_prjt = laborHours_prjt.get("GES - Work @ Non GES Location",0)
            item["QI_Local_Labor"].Value = Local_Labor_prjt
            item["QI_Cross_Border_Labor"].Value = Cross_Border_Labor_prjt
            item["QI_GES_Work_GES_Location"].Value = GES_Location_prjt
            item["QI_GES_Work_Non_GES_Location"].Value = Non_GES_Location_prjt
        if item.ProductName == "Cyber":
            process_labor_hours_Cyber(item,Quote)
        if Quote.GetCustomField('R2Q_Save').Content == 'Submit' and ct and item.ProductName =="HCI Labor Config": #HCI Labor Config
            Quote.GetItemByQuoteItem(ct).AsMainItem.Reconfigure()
        if item.ProductName in ("PHD Labor","AFM Labor","Uniformance Insight Labor") or item.ProductName == "HCI Labor Upload":
            process_labor_hours_hci(item,Quote)
        if item.ProductName == "Winest Labor Import":
            process_labor_hours_winest(item,Quote)
    #Quote.Calculate(1)
#Quote=Param.Quote
if 1:
    Quote_Items(Quote)
    import GS_PopulateEGAPApproversQuoteTable_Helper
    GS_PopulateEGAPApproversQuoteTable_Helper.populateLabor_and_Engineering_Service(Quote)