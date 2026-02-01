def getContainer(Name):
    return Product.GetContainerByName(Name)
def getAttrValue(Name):
    return Product.Attr(Name).GetValue()

containers = ['MSID_Labor_OPM_Engineering','MSID_Labor_LCN_One_Time_Upgrade_Engineering','MSID_Labor_Project_Management','MSID_Labor_EBR_Con','MSID_Labor_ELCN_Con','MSID_Labor_Orion_Console_Con','MSID_Labor_EHPM_C300PM_Con','MSID_Labor_TPS_TO_EXPERION_Con','MSID_Additional_Custom_Deliverables','MSID_Labor_TCMI_Con','MSID_Labor_EHPM_HART_IO_Con','MSID_Labor_C200_Migration_Con','MSID_Labor_CB-EC_Upgrade_to_C300-UHIO_con','MSID_Labor_xPM_to_C300_Migration_Con','MSID_Labor_FDM_Upgrade_Con','MSID_Labor_FSC_to_SM_con','MSID_Labor_LM_to_ELMM_Con','MSID_Labor_Graphics_Migration_con','MSID_Labor_FSC_to_SM_audit_Con','MSID_Labor_XP10_Actuator_Upgrade_con','MSID_Labor_CD_Actuator_con','MSID_Labor_FSCtoSM_IO_con','MSID_Labor_CWS_RAE_Upgrade_con','3rd_Party_PLC_UOC_Labor','MSID_Labor_QCS_RAE_Upgrade_con','MSID_Labor_Virtualization_con','MSID_Labor_Generic_System1_Cont','MSID_Labor_Generic_System2_Cont','MSID_Labor_Generic_System3_Cont','MSID_Labor_Generic_System4_Cont','MSID_Labor_Generic_System5_Cont','MSID_Labor_TPA_con','MSID_Labor_FSC_to_SM_IO_Audit_Con','MSID_Labor_ELEPIU_con']

if getAttrValue("MSID_GES_Location") != 'None':
    #ScriptExecutor.Execute('PS_PopulatePartNumberContainer')
    for container in containers:
        if container != "MSID_Additional_Custom_Deliverables":
            for row in getContainer(container).Rows:
                if row["Deliverable_Type"] in ("Offsite","Off-Site") and container != "MSID_Labor_Project_Management":
                    Trace.Write("Check1" +","+ str(container))
                    if container == "MSID_Labor_CWS_RAE_Upgrade_con" or container == "MSID_Labor_QCS_RAE_Upgrade_con":
                        if row["Deliverable"] in  ('MD CD Configuration', 'In-house Engineering MD-CD'):
                            row["GES_Eng"] = "SVC_GES_P350B_CN"
                        else:
                            row["GES_Eng"] = "SVC_GES_P350B_{}".format(TagParserProduct.ParseString('<*ValueCode(MSID_GES_Location)*>'))
                    elif container != "MSID_Labor_Graphics_Migration_con" and container != "3rd_Party_PLC_UOC_Labor":
                        row["GES_Eng"] = "SVC_GES_P350B_{}".format(TagParserProduct.ParseString('<*ValueCode(MSID_GES_Location)*>'))
                    elif container == "3rd_Party_PLC_UOC_Labor":
                        row["GES_Eng"] = "SVC_GES_PLCB_{}".format(TagParserProduct.ParseString('<*ValueCode(MSID_GES_Location)*>'))
                    else:
                        row["GES_Eng"] = "SVC_GES_P335B_{}".format(TagParserProduct.ParseString('<*ValueCode(MSID_GES_Location)*>'))
                    if Product.Attr('MSID_GES_check').GetValue() != "Country":
                        if container in ('MSID_Labor_OPM_Engineering','MSID_Labor_Orion_Console_Con','MSID_Labor_EHPM_C300PM_Con','MSID_Labor_TCMI_Con','MSID_Labor_EHPM_HART_IO_Con'):
                            if row["Deliverable"] in ('OPM Documentation','Documentation','Migration DDS'):
                                row["FO_Eng_Percentage_Split"] = "20"
                                row["GES_Eng_Percentage_Split"] = "80"
                            if row["Deliverable"] in ('Inhouse Engineering'):
                                row["FO_Eng_Percentage_Split"] = "0"
                                row["GES_Eng_Percentage_Split"] = "100"
                        elif container == "MSID_Labor_TPS_TO_EXPERION_Con":
                            if row["Deliverable"] in ('Migration Documentation','FAT Procedure'):
                                row["FO_Eng_Percentage_Split"] = "10"
                                row["GES_Eng_Percentage_Split"] = "90"
                        elif container == "MSID_Labor_xPM_to_C300_Migration_Con":
                            if row["Deliverable"] == "Migration DDS":
                                row["FO_Eng_Percentage_Split"] = "10"
                                row["GES_Eng_Percentage_Split"] = "90"
                            elif row["Deliverable"] in ('In-house engineering','FAT Procedure','Pre FAT'):
                                row["FO_Eng_Percentage_Split"] = "0"
                                row["GES_Eng_Percentage_Split"] = "100"
                            elif row["Deliverable"] == "FAT":
                                row["FO_Eng_Percentage_Split"] = "50"
                                row["GES_Eng_Percentage_Split"] = "50"
                        elif container == "MSID_Labor_CD_Actuator_con":
                            if row["Deliverable"] == "In-house engineering":
                                row["FO_Eng_Percentage_Split"] = "0"
                                row["GES_Eng_Percentage_Split"] = "100"
                        elif container == "MSID_Labor_Graphics_Migration_con":
                            if row["Deliverable"] == "Customer Input Study":
                                row["FO_Eng_Percentage_Split"] = "25"
                                row["GES_Eng_Percentage_Split"] = "75"
                            elif row["Deliverable"] == "Display Generation":
                                row["FO_Eng_Percentage_Split"] = "25"
                                row["GES_Eng_Percentage_Split"] = "75"
                            elif row["Deliverable"] == "Shapes":
                                row["FO_Eng_Percentage_Split"] = "20"
                                row["GES_Eng_Percentage_Split"] = "80"
                            elif row["Deliverable"] == "Safeview Configuration":
                                row["FO_Eng_Percentage_Split"] = "30"
                                row["GES_Eng_Percentage_Split"] = "70"
                            elif row["Deliverable"] == "Testing System Setup":
                                row["FO_Eng_Percentage_Split"] = "30"
                                row["GES_Eng_Percentage_Split"] = "70"
                            elif row["Deliverable"] == "Query Generation & Clarification":
                                row["FO_Eng_Percentage_Split"] = "0"
                                row["GES_Eng_Percentage_Split"] = "100"
                            elif row["Deliverable"] == "Migration FDS":
                                row["FO_Eng_Percentage_Split"] = "70"
                                row["GES_Eng_Percentage_Split"] = "30"
                            elif row["Deliverable"] == "FAT & SAT Documentation":
                                row["FO_Eng_Percentage_Split"] = "40"
                                row["GES_Eng_Percentage_Split"] = "60"
                            elif row["Deliverable"] == "Migration DDS":
                                row["FO_Eng_Percentage_Split"] = "30"
                                row["GES_Eng_Percentage_Split"] = "70"
                            elif row["Deliverable"] == "Faceplates":
                                row["FO_Eng_Percentage_Split"] = "16.67"
                                row["GES_Eng_Percentage_Split"] = "83.33"
                            elif row["Deliverable"] == "GAP Analysis":
                                Conta = getContainer("Graphics_Migration_Additional_Questions")
                                rows = Conta.Rows[0]
                                var_36 = rows["Graphics_Migration_For_GAP_Analysis_project_com"]
                                if var_36 == "Limitations to use GES":
                                    row["FO_Eng_Percentage_Split"] = "70"
                                    row["GES_Eng_Percentage_Split"] = "30"
                                else:
                                    row["FO_Eng_Percentage_Split"] = "30"
                                    row["GES_Eng_Percentage_Split"] = "70"
                            elif row["Deliverable"] == "FAT Support":
                                contb = getContainer("Graphics_Migration_Training_Testing_Documentation")
                                rows = contb.Rows[0]
                                var_22 = rows["Graphics_Migration_FAT_required?"]
                                if var_22 == "Yes via VEP/Remote GES":
                                    row["FO_Eng_Percentage_Split"] = "50"
                                    row["GES_Eng_Percentage_Split"] = "50"
                                else:
                                    row["FO_Eng_Percentage_Split"] = "100"
                                    row["GES_Eng_Percentage_Split"] = "0"
                        elif container == "MSID_Labor_CWS_RAE_Upgrade_con":
                            if row["Deliverable"] in ('MD CD Configuration','Server/Station Build'):
                                    row["FO_Eng_Percentage_Split"] = "0"
                                    row["GES_Eng_Percentage_Split"] = "100"
                        elif container == "MSID_Labor_QCS_RAE_Upgrade_con":
                            if row["Deliverable"] in ('In-house Engineering MD-CD','Server/Station Build','In-house Engineering','System Specials'):
                                    row["FO_Eng_Percentage_Split"] = "0"
                                    row["GES_Eng_Percentage_Split"] = "100"
                        elif container == "3rd_Party_PLC_UOC_Labor":
                            row["GES_Eng"] = "SVC_GES_PLCB_{}".format(TagParserProduct.ParseString('<*ValueCode(MSID_GES_Location)*>'))
                            Trace.Write("3rd_Party_PLC_UOC_Labor --- "+row["Deliverable"])
                            if row["Deliverable"] == "Migration DDS":
                                row["FO_Eng_Percentage_Split"] = "50"
                                row["GES_Eng_Percentage_Split"] = "50"
                            if row["Deliverable"] == "Inhouse Engineering":
                                row["FO_Eng_Percentage_Split"] = "10"
                                row["GES_Eng_Percentage_Split"] = "90"
                            if row["Deliverable"] == "FAT Procedure":
                                row["FO_Eng_Percentage_Split"] = "0"
                                row["GES_Eng_Percentage_Split"] = "100"
                            if row["Deliverable"] == "Pre-FAT":
                                row["FO_Eng_Percentage_Split"] = "50"
                                row["GES_Eng_Percentage_Split"] = "50"
                            if row["Deliverable"] == "FAT":
                                row["FO_Eng_Percentage_Split"] = "60"
                                row["GES_Eng_Percentage_Split"] = "40"
                        elif container == "MSID_Labor_Virtualization_con":
                            if row["Deliverable"] == "Documentation":
                                row["FO_Eng_Percentage_Split"] = "30"
                                row["GES_Eng_Percentage_Split"] = "70"
                        elif container == "MSID_Labor_TPA_con":
                            if row["Deliverable"] == "HMI Engineering":
                                row["FO_Eng_Percentage_Split"] = "20"
                                row["GES_Eng_Percentage_Split"] = "80"
                            if row["Deliverable"] == "Block Engineering":
                                row["FO_Eng_Percentage_Split"] = TagParserProduct.ParseString('[IF]([AND]([NEQ](<* Value(TPA_What_system_are_we_migrating) *>,TPA Alcont),[NEQ](<* Value(TPA_What_system_are_we_migrating) *>,PMD R61x or older))){100}{45}[ENDIF]')
                                row["GES_Eng_Percentage_Split"] = TagParserProduct.ParseString('[IF]([AND]([NEQ](<* Value(TPA_What_system_are_we_migrating) *>,TPA Alcont),[NEQ](<* Value(TPA_What_system_are_we_migrating) *>,PMD R61x or older))){0}{55}[ENDIF]')
                            if row["Deliverable"] == "Factory Acceptance Test":
                                row["FO_Eng_Percentage_Split"] = "30"
                                row["GES_Eng_Percentage_Split"] = "70"
                elif row["Deliverable_Type"] in ("Offsite","Off-Site") and container == "MSID_Labor_Project_Management":
                    Trace.Write("Check2" +","+ str(container))
                    row["GES_Eng"] = "SVC_GES_P215B_{}".format(TagParserProduct.ParseString('<*ValueCode(MSID_GES_Location)*>'))
                if row["Deliverable_Type"] in ("Onsite","On-Site"):
                    if container != "MSID_Labor_Graphics_Migration_con" and container != "3rd_Party_PLC_UOC_Labor":
                        row["GES_Eng"] = "SVC_GES_P350F_{}".format(TagParserProduct.ParseString('<*ValueCode(MSID_GES_Location)*>'))
                    elif container == "3rd_Party_PLC_UOC_Labor":
                        row["GES_Eng"] = "SVC_GES_PLCB_{}".format(TagParserProduct.ParseString('<*ValueCode(MSID_GES_Location)*>'))
                    else:
                        row["GES_Eng"] = "SVC_GES_P335F_{}".format(TagParserProduct.ParseString('<*ValueCode(MSID_GES_Location)*>'))
            #showGESColumns(container)
    Product.Attr('MSID_GES_check').AssignValue('Country')
else:
    Product.Attr('MSID_GES_check').AssignValue('None')
    for container in containers:
        for row in getContainer(container).Rows:
            if row["Deliverable"] not in ('Total','Off-Site','On-Site'):
                if (container == "MSID_Labor_CWS_RAE_Upgrade_con" and row["Deliverable"] in ("MD CD Configuration","Server/Station Build")) or (container == "MSID_Labor_QCS_RAE_Upgrade_con" and row["Deliverable"] in ("In-house Engineering MD-CD","Server/Station Build")):
                    row["GES_Eng_Percentage_Split"] = "0"
                    row["FO_Eng_Percentage_Split"] = "0"
                else:
                    row["GES_Eng_Percentage_Split"] = "0"
                    row["FO_Eng_Percentage_Split"] = "100"
        #hideGESColumns(container)
ScriptExecutor.Execute('PS_PopulatePartNumberContainer',{"Product": Product})