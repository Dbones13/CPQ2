def getContainer(Name):
    return Product.GetContainerByName(Name)

def resetContainerColumn(container,column):
    for row in container.Rows:
        if row.IsSelected:
            row[column] = ''

def getFloat(Var):
    if Var:
        return float(Var)
    return 0

def checkForMPACustomer():
    PricePlanPresent = False
    query = TagParserQuote.ParseString("select * from MPA_PRICE_PLAN_MAPPING where Honeywell_Ref = '<*CTX(Quote.CustomField(MPA Honeywell Ref))*>' and Price_Plan_Status= 'Active' and Price_Plan_Parts_Discount = 'Y' and Price_Plan_Start_Date < '<*CTX( Date.Format(MM/dd/yyyy) )*>' and Price_Plan_End_Date > '<*CTX( Date.Format(MM/dd/yyyy) )*>'")
    res = SqlHelper.GetList(query)
    if res and len(res) > 0:
        PricePlanPresent = True
    return PricePlanPresent

def assignOPMParts(row,mpaAvailable,activeServiceContract):
    if row["Deliverable"] in ["OPM Pre-Migration Audit","OPM Plan Review & Migration Registration KOM","OPM Site Visit Data Gathering","OPM Pre-FAT & FAT","OPM Migration L2","OPM Migration L1","OPM SAT","OPM Post Migration Task","OPM Deployment L2 - AMT"]:
        if (mpaAvailable or activeServiceContract == "Yes"):
            row["FO_Eng"] = "SVC-ESSS-ST" 
        else :
            row["FO_Eng"] = "SVC-ESSS-ST-NC" 
    else:
        if (mpaAvailable or activeServiceContract == "Yes"):
            row["FO_Eng"] = "SVC-EST1-ST"
        else:
            row["FO_Eng"] = "SVC-EST1-ST-NC"

def updateDefualtPart(container,mpaAvailable,activeServiceContract):
    if container == "MSID_Labor_OPM_Engineering":
        for row in getContainer(container).Rows:
            if row["Deliverable"] not in ('Total','Off-Site','On-Site'):
                assignOPMParts(row,mpaAvailable,activeServiceContract)
    elif container == "MSID_Labor_XP10_Actuator_Upgrade_con" or container == "MSID_Labor_CWS_RAE_Upgrade_con" or container == "MSID_Labor_QCS_RAE_Upgrade_con":
        for row in getContainer(container).Rows:
            if row["Deliverable"] not in ('Total','Off-Site','On-Site'):
                if mpaAvailable or activeServiceContract == "Yes":
                    row["FO_Eng"] = "SVC-QST1-ST"
                else:
                    row["FO_Eng"] = "SVC-QST1-ST-NC"
    elif container == "3rd_Party_PLC_UOC_Labor":
        for row in getContainer(container).Rows:
            if row["Deliverable"] not in ('Total','Off-Site','On-Site'):
                if mpaAvailable or activeServiceContract == "Yes":
                    row["FO_Eng"] = "SVC-PLC-ST"
                else:
                    row["FO_Eng"] = "SVC-PLC-ST-NC"
    elif container == "MSID_Labor_CD_Actuator_con": 
        for row in getContainer(container).Rows:
            if row["Deliverable"] not in ('Total','Off-Site','On-Site'):
                if mpaAvailable or activeServiceContract == "Yes":
                    if row["Deliverable"] == "In-house engineering":
                        row["FO_Eng"] = "SVC-QST1-ST"
                    else:
                        row["FO_Eng"] = "SVC-QAPS-ST"
                else:
                    if row["Deliverable"] == "In-house engineering":
                        row["FO_Eng"] = "SVC-QST1-ST-NC"
                    else:
                        row["FO_Eng"] = "SVC-QAPS-ST-NC"
    elif container == "MSID_Labor_Virtualization_con":
        for row in getContainer(container).Rows:
            if row["Deliverable"] not in ('Total','Off-Site','On-Site'):
                if mpaAvailable or activeServiceContract == "Yes":
                    if row["Deliverable"] in ('Plan review & Kick off Meetings','HW/SW order to factory','Documentation','Off Site Config activities','FAT'):
                        row["FO_Eng"] = "SVC-EAPS-ST"
                    elif row["Deliverable"] in ('On Site activities','SAT'):
                        row["FO_Eng"] = "SVC-ESSS-ST"
                    else:
                        row["FO_Eng"] = "SVC-EST1-ST"
                else:
                    if row["Deliverable"] in ('Plan review & Kick off Meetings','HW/SW order to factory','Documentation','Off Site Config activities','FAT'):
                        row["FO_Eng"] = "SVC-EAPS-ST-NC"
                    elif row["Deliverable"] in ('On Site activities','SAT'):
                        row["FO_Eng"] = "SVC-ESSS-ST-NC"
                    else:
                        row["FO_Eng"] = "SVC-EST1-ST-NC"
    elif container == "MSID_Labor_TPA_con":
        for row in getContainer(container).Rows:
            if row["Deliverable"] not in ('Total','Off-Site','On-Site'):
                if mpaAvailable or activeServiceContract == "Yes":
                    if row["Deliverable"] in ('HMI Engineering','Block Engineering','Network Engineering','Factory Acceptance Test','Cyber Factory Acceptance Test ','Network Factory Acceptance Test ','Serial Interface Factory Acceptance Test ','Profibus Factory Acceptance Test ','Serial Interface Engineering','Profibus Engineering','HMI Engineering OnSite','Block Engineering OnSite','Network Engineering OnSite','Serial Interface Engineering OnSite','Profibus Engineering OnSite','IO Replacement OnSite','Installation','Hardware Engineering OnSite'):
                        row["FO_Eng"] = "SVC-QAPS-ST"
                    elif row["Deliverable"] in ('Hardware Engineering','IO Replacement Hardware Engineer','','',''):
                        row["FO_Eng"] = "SVC-QST1-ST"
                    elif row["Deliverable"] in ('Lead Engineer Effort','Factory Acceptance Test - Lead Engineer','MD-CD Line Drive Engineering','IO Replacement - Lead Engineer','Lead Engineer Effort OnSite','MD-CD Line Drive Engineering OnSite'):
                        row["FO_Eng"] = "SVC-QST2-ST"
                else:
                    if row["Deliverable"] in ('HMI Engineering','Block Engineering','Network Engineering','Factory Acceptance Test','Cyber Factory Acceptance Test ','Network Factory Acceptance Test ','Serial Interface Factory Acceptance Test ','Profibus Factory Acceptance Test ','Serial Interface Engineering','Profibus Engineering','HMI Engineering OnSite','Block Engineering OnSite','Network Engineering OnSite','Serial Interface Engineering OnSite','Profibus Engineering OnSite','IO Replacement OnSite','Installation','Hardware Engineering OnSite'):
                        row["FO_Eng"] = "SVC-QAPS-ST-NC"
                    elif row["Deliverable"] in ('Hardware Engineering','IO Replacement Hardware Engineer','','',''):
                        row["FO_Eng"] = "SVC-QST1-ST-NC"
                    elif row["Deliverable"] in ('Lead Engineer Effort','Factory Acceptance Test - Lead Engineer','MD-CD Line Drive Engineering','IO Replacement - Lead Engineer','Lead Engineer Effort OnSite','MD-CD Line Drive Engineering OnSite'):
                        row["FO_Eng"] = "SVC-QST2-ST-NC"
    # To populate Labor table details based on Active Service Contract and MPA pricing data availability -- Janhavi Tanna : CXCPQ-60159 :start
    elif container == "MSID_Labor_ELEPIU_con":
        for row in getContainer(container).Rows:
            if row["Deliverable"] not in ('Total','Off-Site','On-Site'):
                if mpaAvailable or activeServiceContract == "Yes":
                    if row["Deliverable"] in ('Plan Review & KOM','FEL Site Visit Data Gathering','Migration DDS','Offsite Services','SW_HW Order','Factory Acceptance Test','Site Installation','Site Acceptance Test'):
                        row["FO_Eng"] = "SVC-QAPS-ST"
                else:
                    if row["Deliverable"] in ('Plan Review & KOM','FEL Site Visit Data Gathering','Migration DDS','Offsite Services','SW_HW Order','Factory Acceptance Test','Site Installation','Site Acceptance Test'):
                        row["FO_Eng"] = "SVC-QAPS-ST-NC"
    #-- Janhavi Tanna : CXCPQ-60159 :end
    else:
        for row in getContainer(container).Rows:
            if row["Deliverable"] not in ('Total','Off-Site','On-Site','Site Installation - EST1','Plan Review (Kickoffs) - ESSS','Site Installation - EST1','Site Installation-EST1','Plan Review & KOM - ESSS','Migration DDS - ESSS','In-house engineering - ESSS'):
                if mpaAvailable or activeServiceContract == "Yes":
                    row["FO_Eng"] = "SVC-EAPS-ST"
                else:
                    row["FO_Eng"] = "SVC-EAPS-ST-NC"
            elif row["Deliverable"] in ('Site Installation - EST1','Site Installation - EST1','Site Installation-EST1'):
                if mpaAvailable or activeServiceContract == "Yes":
                    row["FO_Eng"] = "SVC-EST1-ST"
                else:
                    row["FO_Eng"] = "SVC-EST1-ST-NC"
            elif row["Deliverable"] in ('Plan Review (Kickoffs) - ESSS','Plan Review & KOM - ESSS','Migration DDS - ESSS','In-house engineering - ESSS'):
                if mpaAvailable or activeServiceContract == "Yes":
                    row["FO_Eng"] = "SVC-ESSS-ST"
                else:
                    row["FO_Eng"] = "SVC-ESSS-ST-NC"
        

def populatePMCon(container,mpaAvailable,activeServiceContract):
    for row in container.Rows:
        if row["Deliverable"] not in ('Total','Off-Site','On-Site'):
            if row["Deliverable_Flag"] == "PM":
                if mpaAvailable or activeServiceContract == "Yes":
                    row["FO_Eng"] = "SVC-PMGT-ST"
                else:
                    row["FO_Eng"] = "SVC-PMGT-ST-NC"
            elif row["Deliverable_Flag"] == "PA":
                if mpaAvailable or activeServiceContract == "Yes":
                    row["FO_Eng"] = "SVC-PADM-ST"
                else:
                    row["FO_Eng"] = "SVC-PADM-ST-NC"

ScriptExecutor.Execute('PS_PopulatePartNumberContainer',{"Product": Product})
projectManagementCon = getContainer("MSID_Labor_Project_Management")
additonalCustomDelivCon = getContainer("MSID_Additional_Custom_Deliverables")
foPartNumberCon = getContainer("MSID_Labor_FO_Part_Number")
mpaAvailable = checkForMPACustomer()
activeServiceContract = Product.Attr("MSID_Active_Service_Contract").GetValue()
# Added "MSID_Labor_ELEPIU_con" in container list to populate Labor table details based on Active Service Contract and MPA pricing data availability -- Janhavi Tanna : CXCPQ-60159 :start
containers = ['MSID_Labor_OPM_Engineering','MSID_Labor_LCN_One_Time_Upgrade_Engineering','MSID_Labor_EBR_Con','MSID_Labor_ELCN_Con','MSID_Labor_Orion_Console_Con','MSID_Labor_EHPM_C300PM_Con','MSID_Labor_TPS_TO_EXPERION_Con','MSID_Labor_TCMI_Con','MSID_Labor_EHPM_HART_IO_Con','MSID_Labor_C200_Migration_Con','MSID_Labor_CB-EC_Upgrade_to_C300-UHIO_con','MSID_Labor_xPM_to_C300_Migration_Con','MSID_Labor_FDM_Upgrade_Con','MSID_Labor_FSC_to_SM_con','MSID_Labor_LM_to_ELMM_Con','MSID_Labor_Graphics_Migration_con','MSID_Labor_FSC_to_SM_audit_Con','MSID_Labor_XP10_Actuator_Upgrade_con','MSID_Labor_CD_Actuator_con','MSID_Labor_CWS_RAE_Upgrade_con','MSID_Labor_FSCtoSM_IO_con','3rd_Party_PLC_UOC_Labor','MSID_Labor_Virtualization_con','MSID_Labor_QCS_RAE_Upgrade_con','MSID_Labor_Generic_System1_Cont','MSID_Labor_Generic_System2_Cont','MSID_Labor_Generic_System3_Cont','MSID_Labor_Generic_System4_Cont','MSID_Labor_Generic_System5_Cont','MSID_Labor_TPA_con','MSID_Labor_FSC_to_SM_IO_Audit_Con','MSID_Labor_ELEPIU_con']
#-- Janhavi Tanna : CXCPQ-60159 :end
for container in containers:
    updateDefualtPart(container,mpaAvailable,activeServiceContract)
    
populatePMCon(projectManagementCon,mpaAvailable,activeServiceContract)
resetContainerColumn(additonalCustomDelivCon,"FO_Eng")