def getContainer(Name):
    return Product.GetContainerByName(Name)

def getAttrValue(Name):
    return Product.Attr(Name).GetValue()

def setAttrValue(Name,value):
    Product.Attr(Name).AssignValue(value)

def getFloat(Var):
    if Var:
        return float(Var)
    return 0

def getContainerData(container):
    containerData = {}
    for row in container.Rows:
        containerData[row.RowIndex] = dict()
        for column in row.Columns:
            containerData[row.RowIndex][column.Name] = row[column.Name]
        containerData[row.RowIndex]["SelectedRow"] = row.IsSelected
    return containerData

def updateTotals(container):
    totalOffSiteFinalHrs = 0
    totalOnSiteFinalHrs = 0
    totalFinalHrs = 0
    for row in container.Rows:
        if row["Deliverable_Type"] in ("Offsite","Off-Site"):
            totalOffSiteFinalHrs = totalOffSiteFinalHrs + getFloat(row["Final_Hrs"])
        elif row["Deliverable_Type"] in ("Onsite","On-Site"):
            totalOnSiteFinalHrs = totalOnSiteFinalHrs + getFloat(row["Final_Hrs"])
        totalFinalHrs = totalOffSiteFinalHrs + totalOnSiteFinalHrs
    for row in container.Rows:
        if row["Deliverable"] == "Off-Site":
            row["Final_Hrs"] = str(totalOffSiteFinalHrs)
        elif row["Deliverable"] == "On-Site":
            row["Final_Hrs"] = str(totalOnSiteFinalHrs)
        elif row["Deliverable"] == "Total":
            row["Final_Hrs"] = str(totalFinalHrs)
    container.Calculate()


def populateOPM(container,row):
    deliverablePresent = False
    for Row in container.Rows:
        if Row["Deliverable"] == row["Deliverable_Name"]:
            Row["Final_Hrs"] = row["Final_Hrs"]
            Row["Deliverable_Type"] = row["Type"]
            Row["FO_Eng"] = row["FO_Eng"]
            Row["FO_Eng_Percentage_Split"] = row["FO_Eng_Percentage_Split"]
            Row["GES_Eng"] = row["GES_Eng"]
            Row["GES_Eng_Percentage_Split"] = row["GES_Eng_Percentage_Split"]
            Row["Standard_Deliverable_Selection"] = row["Deliverable"]
            Row["Manual_Entry"] = row["Manual_Entry"]
            Row["Regional_Cost"] = row["Regional_Cost"]
            Row["GES_Regional_Cost"] = row["GES_Regional_Cost"]
            Row["Execution_Year"] = row["Execution_Year"]
            Row["Execution_Country"] = row["Execution_Country"]
            Row["FOUnitWTWCost"] = row["FOUnitWTWCost"]
            Row["FO_ListPrice"] = row["FO_ListPrice"]
            Row["Standard Deliverable selection"] = row["Deliverable"]
            deliverablePresent = True
    if not deliverablePresent:
        if row["Product_Module"] in ('OPM','EBR','ELCN','Orion Console','EHPM/EHPMX/ C300PM','TPS TO EXPERION','TCMI','EHPM HART IO','C200 Migration','CB-EC Upgrade to C300-UHIO','FDM Upgrade','FSC to SM','xPM to C300 Migration','LM to ELMM ControlEdge PLC','Graphics Migration','XP10 Actuator Upgrade','CD Actuator I-F Upgrade','CWS RAE Upgrade','FSC to SM IO Migration','3rd Party PLC to ControlEdge PLC/UOC','Virtualization System','QCS RAE Upgrade','Generic System 1','Generic System 2','Generic System 3','Generic System 4','Generic System 5','TPA/PMD Migration','FSC to SM IO Audit','ELEPIU ControlEdge RTU Migration Engineering') and row["Type"] == "Off-Site":
            containerData = getContainerData(container)
            container.Rows.Clear()
            for data in containerData:
                if containerData[data]["Deliverable"] == "On-Site":
                    addRow = container.AddNewRow(False)
                    addRow["Deliverable"] = row["Deliverable_Name"]
                    addRow["Calculated_Hrs"] = "0.00"
                    addRow["Adjustment_Productivity"] = "1"
                    addRow["Final_Hrs"] = row["Final_Hrs"]
                    addRow["FO_Eng"] = row["FO_Eng"]
                    addRow["FO_Eng_Percentage_Split"] = row["FO_Eng_Percentage_Split"]
                    addRow["GES_Eng"] = row["GES_Eng"]
                    addRow["GES_Eng_Percentage_Split"] = row["GES_Eng_Percentage_Split"]
                    addRow["Standard_Deliverable_Selection"] = row["Deliverable"]
                    addRow["Manual_Entry"] = row["Manual_Entry"]
                    addRow["Regional_Cost"] = row["Regional_Cost"]
                    addRow["GES_Regional_Cost"] = row["GES_Regional_Cost"]
                    addRow["Execution_Year"] = row["Execution_Year"]
                    addRow["Execution_Country"] = row["Execution_Country"]
                    addRow["FOUnitWTWCost"] = row["FOUnitWTWCost"]
                    addRow["FO_ListPrice"] = row["FO_ListPrice"]
                    addRow["Deliverable_Type"] = row["Type"]
                    addRow["Standard Deliverable selection"] = row["Deliverable"]

                addRow = container.AddNewRow(False)
                for column in addRow.Columns:
                    for key,value in containerData[data].items():
                        if column.Name == key:
                            addRow[column.Name] = value
                    if containerData[data]["SelectedRow"] == True and addRow.IsSelected == False:
                        addRow.IsSelected = True
        else:
            addRow = container.AddNewRow(False)
            addRow["Deliverable"] = row["Deliverable_Name"]
            addRow["Calculated_Hrs"] = "0.00"
            addRow["Adjustment_Productivity"] = "1"
            addRow["Final_Hrs"] = row["Final_Hrs"]
            addRow["FO_Eng"] = row["FO_Eng"]
            addRow["FO_Eng_Percentage_Split"] = row["FO_Eng_Percentage_Split"]
            addRow["GES_Eng"] = row["GES_Eng"]
            addRow["GES_Eng_Percentage_Split"] = row["GES_Eng_Percentage_Split"]
            addRow["Standard_Deliverable_Selection"] = row["Deliverable"]
            addRow["Manual_Entry"] = row["Manual_Entry"]
            addRow["Regional_Cost"] = row["Regional_Cost"]
            addRow["GES_Regional_Cost"] = row["GES_Regional_Cost"]
            addRow["Execution_Year"] = row["Execution_Year"]
            addRow["Execution_Country"] = row["Execution_Country"]
            addRow["FOUnitWTWCost"] = row["FOUnitWTWCost"]
            addRow["FO_ListPrice"] = row["FO_ListPrice"]
            addRow["Deliverable_Type"] = row["Type"]
            addRow["Standard Deliverable selection"] = row["Deliverable"]
    container.Calculate()
    setAttrValue("MSID_Labor_Message","Deliverables has been sucessfully applied")


opmEngineeringCon = getContainer("MSID_Labor_OPM_Engineering")
additonalCustomDelivCon = getContainer("MSID_Additional_Custom_Deliverables")
#opmAdjustmentProductivity =getAttrValue("OPM_Adjustment_Productivity")
#lcnAdjustmentProductivity =getAttrValue("LCN_Adjustment_Productivity")
#pmAdjustmentProductivity = getAttrValue("PM_Adjustment_Productivity")
lcnOneTimeUpgradeCon = getContainer("MSID_Labor_LCN_One_Time_Upgrade_Engineering")
ebrCon = getContainer("MSID_Labor_EBR_Con")
elcnCon = getContainer("MSID_Labor_ELCN_Con")
orionConsoleCon = getContainer("MSID_Labor_Orion_Console_Con")
ehpmCon = getContainer("MSID_Labor_EHPM_C300PM_Con")
tpsCon = getContainer("MSID_Labor_TPS_TO_EXPERION_Con")
tcmiCon = getContainer("MSID_Labor_TCMI_Con")
ehpmhartioCon = getContainer("MSID_Labor_EHPM_HART_IO_Con")
c200Con =getContainer("MSID_Labor_C200_Migration_Con")
cbecCon = getContainer("MSID_Labor_CB-EC_Upgrade_to_C300-UHIO_con")
fsctosmCon = getContainer("MSID_Labor_FSC_to_SM_con")
fdmupgradeCon = getContainer("MSID_Labor_FDM_Upgrade_Con")
lmCon = getContainer("MSID_Labor_LM_to_ELMM_Con")
xPMCon = getContainer("MSID_Labor_xPM_to_C300_Migration_Con")
projectManagementCon = getContainer("MSID_Labor_Project_Management")
GraphicsCon = getContainer("MSID_Labor_Graphics_Migration_con")
XP10Con = getContainer("MSID_Labor_XP10_Actuator_Upgrade_con")
CDActuatorCon = getContainer("MSID_Labor_CD_Actuator_con")
fscsmioCon = getContainer("MSID_Labor_FSCtoSM_IO_con")
CWSCon = getContainer("MSID_Labor_CWS_RAE_Upgrade_con")
QCSCon = getContainer("MSID_Labor_QCS_RAE_Upgrade_con")
plcuocCon = getContainer("3rd_Party_PLC_UOC_Labor")
VirtualizationCon = getContainer("MSID_Labor_Virtualization_con")
gs1Con = getContainer('MSID_Labor_Generic_System1_Cont')
gs2Con = getContainer('MSID_Labor_Generic_System2_Cont')
gs3Con = getContainer('MSID_Labor_Generic_System3_Cont')
gs4Con = getContainer('MSID_Labor_Generic_System4_Cont')
gs5Con = getContainer('MSID_Labor_Generic_System5_Cont')
fscsmioauditCon = getContainer('MSID_Labor_FSC_to_SM_IO_Audit_Con')
TPACon = getContainer("MSID_Labor_TPA_con")
# Added cont. name for ELEPIU Module -- Dipak Shekokar : CXCPQ-60170
ELEPIUon = getContainer("MSID_Labor_ELEPIU_con")

setAttrValue("MSID_Labor_Message",'')
setAttrValue("IncompleteAdditionalDeliverables",'')
#Product.AllowAttr("MSID_Labor_Apply_Deliverables")
if additonalCustomDelivCon.Rows.Count > 0:
    for row in additonalCustomDelivCon.Rows:
        if row["Deliverable_Name"] == '':
            setAttrValue("MSID_Labor_Message","Deliverable Name is empty. Please enter the deliverable Name.")
            setAttrValue("IncompleteAdditionalDeliverables","1")
            #Product.DisallowAttr("MSID_Labor_Apply_Deliverables")
            break
        elif row["Final_Hrs"] == '':
            setAttrValue("MSID_Labor_Message","Final Hrs is empty. Please enter the Final Hours.")
            setAttrValue("IncompleteAdditionalDeliverables","1")
            #Product.DisallowAttr("MSID_Labor_Apply_Deliverables")
            break
        elif row["FO_Eng"] == '':
            setAttrValue("MSID_Labor_Message","FO Eng is empty. Please apply Fo Eng material.")
            setAttrValue("IncompleteAdditionalDeliverables","1")
            #Product.DisallowAttr("MSID_Labor_Apply_Deliverables")
            break
        elif row["GES_Eng"] == '' and Product.Attr('MSID_GES_Location').GetValue() != 'None' and row["FO_Eng_Percentage_Split"] != "100":
            setAttrValue("MSID_Labor_Message","GES Eng is empty. Please apply GES Eng material.")
            setAttrValue("IncompleteAdditionalDeliverables","1")
            break
        elif row["Execution_Country"] == '':
            setAttrValue("MSID_Labor_Message","Execution Country is empty. Please apply Execution Country.")
            setAttrValue("IncompleteAdditionalDeliverables","1")
            break
        elif row["Execution_Year"] == '':
            setAttrValue("MSID_Labor_Message","Execution Year is empty. Please apply Execution Year.")
            setAttrValue("IncompleteAdditionalDeliverables","1")
            break

        if row["Product_Module"] == "OPM":
            populateOPM(opmEngineeringCon,row)
            updateTotals(opmEngineeringCon)
        elif row["Product_Module"] == "LCN":
            populateOPM(lcnOneTimeUpgradeCon,row)
            updateTotals(lcnOneTimeUpgradeCon)
        elif row["Product_Module"] == "EBR":
            populateOPM(ebrCon,row)
            updateTotals(ebrCon)
        elif row["Product_Module"] == "ELCN":
            populateOPM(elcnCon,row)
            updateTotals(elcnCon)
        elif row["Product_Module"] == "Orion Console":
            populateOPM(orionConsoleCon,row)
            updateTotals(orionConsoleCon)
        elif row["Product_Module"] == "EHPM/EHPMX/ C300PM":
            populateOPM(ehpmCon,row)
            updateTotals(ehpmCon)
        elif row["Product_Module"] == "TPS TO EXPERION":
            populateOPM(tpsCon,row)
            updateTotals(tpsCon)
        elif row["Product_Module"] == "TCMI":
            populateOPM(tcmiCon,row)
            updateTotals(tcmiCon)
        elif row["Product_Module"] == "EHPM HART IO":
            populateOPM(ehpmhartioCon,row)
            updateTotals(ehpmhartioCon)
        elif row["Product_Module"] == "C200 Migration":
            populateOPM(c200Con,row)
            updateTotals(c200Con)
        elif row["Product_Module"] == "CB-EC Upgrade to C300-UHIO":
            populateOPM(cbecCon,row)
            updateTotals(cbecCon)
        elif row["Product_Module"] == "FSC to SM":
            populateOPM(fsctosmCon,row)
            updateTotals(fsctosmCon)
        elif row["Product_Module"] == "FDM Upgrade":
            populateOPM(fdmupgradeCon,row)
            updateTotals(fdmupgradeCon)
        elif row["Product_Module"] == "XP10 Actuator Upgrade":
            populateOPM(XP10Con,row)
            updateTotals(XP10Con)
        elif row["Product_Module"] == "LM to ELMM ControlEdge PLC":
            populateOPM(lmCon,row)
            updateTotals(lmCon)
        elif row["Product_Module"] == "xPM to C300 Migration":
            populateOPM(xPMCon,row)
            updateTotals(xPMCon)
        elif row["Product_Module"] == "Graphics Migration":
            populateOPM(GraphicsCon,row)
            updateTotals(GraphicsCon)
        elif row["Product_Module"] == "CD Actuator I-F Upgrade":
            populateOPM(CDActuatorCon,row)
            updateTotals(CDActuatorCon)
        elif row["Product_Module"] == "FSC to SM IO Migration":
            populateOPM(fscsmioCon,row)
            updateTotals(fscsmioCon)
        elif row["Product_Module"] =='FSC to SM IO Audit':
            populateOPM(fscsmioauditCon,row)
            updateTotals(fscsmioauditCon)
        elif row["Product_Module"] == "CWS RAE Upgrade":
            populateOPM(CWSCon,row)
            updateTotals(CWSCon)
        elif row["Product_Module"] == "QCS RAE Upgrade":
            populateOPM(QCSCon,row)
            updateTotals(QCSCon)
        elif row["Product_Module"] == "3rd Party PLC to ControlEdge PLC/UOC":
            populateOPM(plcuocCon,row)
            updateTotals(plcuocCon)
        elif row["Product_Module"] == "Virtualization System":
            populateOPM(VirtualizationCon,row)
            updateTotals(VirtualizationCon)
        elif row["Product_Module"] == "Generic System 1":
            populateOPM(gs1Con,row)
            updateTotals(gs1Con)
        elif row["Product_Module"] == "Generic System 2":
            populateOPM(gs2Con,row)
            updateTotals(gs2Con)
        elif row["Product_Module"] == "Generic System 3":
            populateOPM(gs3Con,row)
            updateTotals(gs3Con)
        elif row["Product_Module"] == "Generic System 4":
            populateOPM(gs4Con,row)
            updateTotals(gs4Con)
        elif row["Product_Module"] == "Generic System 5":
            populateOPM(gs5Con,row)
            updateTotals(gs5Con)
        elif row["Product_Module"] == "TPA/PMD Migration":
            populateOPM(TPACon,row)
            updateTotals(TPACon)
        # Extended Logic Additional Cust. Deliverables for ELEPIU Module -- Dipak Shekokar : CXCPQ-60170
        elif row["Product_Module"] == "ELEPIU ControlEdge RTU Migration Engineering":
            populateOPM(ELEPIUon,row)
            updateTotals(ELEPIUon)
        elif row["Product_Module"] == "PM":
            populateOPM(projectManagementCon,row)
            updateTotals(projectManagementCon)
    ScriptExecutor.ExecuteGlobal('GS_CalculateLaborHoursTotals')
    ScriptExecutor.Execute('PS_CalculateProjectManagementLaborHours')
    ScriptExecutor.Execute('PS_PopulatePartSummary')
    ScriptExecutor.Execute('PS_PopulateChildParts')