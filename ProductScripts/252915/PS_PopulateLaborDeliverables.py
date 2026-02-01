from System import DateTime

def getContainer(Name):
    return Product.GetContainerByName(Name)

def getCfValue(Name):
    return Quote.GetCustomField(Name).Content

def getAttrValue(Name):
    return Product.Attr(Name).GetValue()

def getFloat(Var):
    if Var:
        return float(Var)
    return 0

def getRowData(container,column):
    Container = getContainer(container)
    for row in Container.Rows:
        return row[column]

def getDefaultExecutionYear():
    executionYear = str(DateTime.Now.Year)
    yearsList = []
    currentYear = DateTime.Now.Year
    i = 0
    while i < 4:
        year = currentYear + i
        yearsList.append(year)
        i += 1
    if getCfValue("EGAP_Contract_Start_Date") != '':
        year = UserPersonalizationHelper.CovertToDate(getCfValue("EGAP_Contract_Start_Date")).Year
        if year in yearsList:
            executionYear = year
        else:
            executionYear = yearsList[-1] if len(yearsList) > 0 else str(DateTime.Now.Year)
    return executionYear

def checkForMPACustomer():
    PricePlanPresent = False
    query = TagParserQuote.ParseString("select * from MPA_PRICE_PLAN_MAPPING where Honeywell_Ref = '<*CTX(Quote.CustomField(MPA Honeywell Ref))*>' and Price_Plan_Status= 'Active' and Price_Plan_Parts_Discount = 'Y' and Price_Plan_Start_Date < '<*CTX( Date.Format(MM/dd/yyyy) )*>' and Price_Plan_End_Date > '<*CTX( Date.Format(MM/dd/yyyy) )*>'")
    res = SqlHelper.GetList(query)
    if res and len(res) > 0:
        PricePlanPresent = True
    return PricePlanPresent

def getExecutionCountry():
    marketCode = Quote.SelectedMarket.MarketCode
    salesOrg = Quote.GetCustomField('Sales Area').Content
    #Updated logic for Defect 27359
    currency = Quote.GetCustomField('Currency').Content
    query = SqlHelper.GetFirst("select Execution_County from NEW_EXECUTION_COUNTRY_SALES_ORG_MAPPING where Sales_Area = '{}' and Currency = '{}'".format(salesOrg,currency))
    #query = SqlHelper.GetFirst("select Execution_County from EXECUTION_COUNTRY_SALES_ORG_MAPPING where Execution_Country_Sales_Org = '{}'".format(salesOrg))
    if query is not None:
        return query.Execution_County

def assignOPMParts(row,entry,mpaAvailable,activeServiceContract):
    if entry.Deliverables in ["OPM Pre-Migration Audit","OPM Plan Review & Migration Registration KOM","OPM Site Visit Data Gathering","OPM Pre-FAT & FAT","OPM Migration L2","OPM Migration L1","OPM SAT","OPM Post Migration Task","OPM Deployment L2 - AMT","Regional Migration Principal Efforts"]:
        if (mpaAvailable or activeServiceContract == "Yes"):
            row["FO_Eng"] = "SVC-ESSS-ST" 
        else :
            row["FO_Eng"] = "SVC-ESSS-ST-NC" 
    else:
        if (mpaAvailable or activeServiceContract == "Yes"):
            row["FO_Eng"] = "SVC-EST1-ST"
        else:
            row["FO_Eng"] = "SVC-EST1-ST-NC"

def populateOpmCon(container,productModule,mpaAvailable,activeServiceContract):
    #container.Rows.Clear()
    if container.Rows.Count == 0:
        amt = getRowData("OPM_Basic_Information","OPM_Is_this_is_a_Remote_Migration_Service_RMS")
        dataGatheringRequired = getRowData("MSID_CommonQuestions","MSID_FEL_Data_Gathering_Required")
        queryData = SqlHelper.GetList("select * from LABOR_DELIVERABLES where Product_Module = '{}'".format(productModule))
        if queryData is not None:
            for entry in queryData:
                if entry.Deliverable_Type == "Onsite" and entry.Deliverables == 'OPM Deployment L2 - AMT' and amt in ('No',''):
                    continue
                if entry.Deliverable_Type == "Offsite" and entry.Deliverables == 'OPM MCOE - AMT' and amt in ('No',''):
                    continue
                if entry.Deliverable_Type == "Offsite" and entry.Deliverables == 'OPM Site Visit Data Gathering' and dataGatheringRequired in ('NO','','None'):
                    continue
                if entry.Deliverable_Type == "Onsite" and entry.Deliverables == 'OPM Migration L2' and amt == 'Yes':
                    continue
                row = container.AddNewRow(False)
                row["Deliverable"] = entry.Deliverables
                row["Deliverable_Type"] = entry.Deliverable_Type if entry.Deliverable_Type else ''
                if entry.Deliverables not in ('On-Site','Total','Off-Site'):
                    row["Execution_Year"] = str(executionYear)
                if entry.Deliverables not in ('Total','Off-Site','On-Site'):
                    row["Adjustment_Productivity"] = "1"
                    assignOPMParts(row,entry,mpaAvailable,activeServiceContract)
                    if getAttrValue("MSID_GES_Location") != 'None':
                        row["FO_Eng_Percentage_Split"] = entry.FO_Eng_Split if entry.FO_Eng_Split else "100"
                        row["GES_Eng_Percentage_Split"] = entry.GES_Eng_Split if entry.GES_Eng_Split else "0"
                        if entry.Deliverable_Type == "Offsite":
                            row["GES_Eng"] = "SVC_GES_P350B_{}".format(TagParserProduct.ParseString('<*ValueCode(MSID_GES_Location)*>'))
                        elif entry.Deliverable_Type == "Onsite":
                            row["GES_Eng"] = "SVC_GES_P350F_{}".format(TagParserProduct.ParseString('<*ValueCode(MSID_GES_Location)*>'))
                    else:
                        row["FO_Eng_Percentage_Split"] = "100"
                        row["GES_Eng_Percentage_Split"] = "0"
                    if excecutionCountry:
                        row["Execution_Country"] = excecutionCountry

def populatelcnOneTimeUpgradeCon(lcnOneTimeUpgradeCon,lcnAdjustmentProductivity,mpaAvailable,activeServiceContract):
    if lcnOneTimeUpgradeCon.Rows.Count == 0:
        excecutionCountry = getExecutionCountry()
        queryData = SqlHelper.GetList("select * from LABOR_DELIVERABLES where Product_Module = 'LCN'")
        row = lcnOneTimeUpgradeCon.AddNewRow(False)
        row["Deliverable"] = "Total"
        row = lcnOneTimeUpgradeCon.AddNewRow(False)
        row["Deliverable"] = "Off-Site"
        if queryData is not None:
            for entry in queryData:
                if entry.Deliverable_Type == "Offsite":
                    row = lcnOneTimeUpgradeCon.AddNewRow(False)
                    row["Deliverable"] = entry.Deliverables
                    row["Adjustment_Productivity"] = lcnAdjustmentProductivity
                    row["Deliverable_Type"] = entry.Deliverable_Type
                    row["FO_Eng_Percentage_Split"] = "100"
                    row["GES_Eng_Percentage_Split"] = "0"
                    if mpaAvailable or activeServiceContract == "Yes":
                        row["FO_Eng"] = "SVC-EAPS-ST"
                    else:
                        row["FO_Eng"] = "SVC-EAPS-ST-NC"
                    row["Execution_Year"] =str(executionYear)
                    if getAttrValue("MSID_GES_Location") != 'None':
                        row["GES_Eng"] = "SVC_GES_P350B_{}".format(TagParserProduct.ParseString('<*ValueCode(MSID_GES_Location)*>'))
                    if excecutionCountry:
                        row["Execution_Country"] = excecutionCountry

def addNewRow(container,productivity,mpaAvailable,activeServiceContract,excecutionCountry,entry):
    row = container.AddNewRow(False)
    row["Deliverable"] = entry.Deliverables
    row["Adjustment_Productivity"] = productivity
    row["Deliverable_Type"] = entry.Deliverable_Type
    row["FO_Eng_Percentage_Split"] = "100"
    row["GES_Eng_Percentage_Split"] = "0"
    if entry.Deliverables=="Regional Migration Principal Efforts":
		if (mpaAvailable or activeServiceContract == "Yes"):
			row["FO_Eng"] = entry.FO_Eng
		else :
			row["FO_Eng"] = entry.FO_Eng+"-NC"
    elif mpaAvailable or activeServiceContract == "Yes":
        row["FO_Eng"] = "SVC-EAPS-ST"
    else:
        row["FO_Eng"] = "SVC-EAPS-ST-NC"
    row["Execution_Year"] = str(executionYear)
    if getAttrValue("MSID_GES_Location") != 'None':
        if entry.Deliverable_Type == "Offsite":
            row["GES_Eng"] = "SVC_GES_P350B_{}".format(TagParserProduct.ParseString('<*ValueCode(MSID_GES_Location)*>'))
        else:
            row["GES_Eng"] = "SVC_GES_P350F_{}".format(TagParserProduct.ParseString('<*ValueCode(MSID_GES_Location)*>'))
    if excecutionCountry:
        row["Execution_Country"] = excecutionCountry

def populatelEBRCon(ebrCon,ebrAdjustmentProductivity,mpaAvailable,activeServiceContract,excecutionCountry):
    siteAccepTest = getRowData("EBR_Services","EBR_Site_Acceptance_Test_required")
    if ebrCon.Rows.Count == 0:
        queryData = SqlHelper.GetList("select * from LABOR_DELIVERABLES where Product_Module = 'EBR'")
        row = ebrCon.AddNewRow(False)
        row["Deliverable"] = "Total"
        row = ebrCon.AddNewRow(False)
        row["Deliverable"] = "Off-Site"
        if queryData is not None:
            for entry in queryData:
                if entry.Deliverable_Type == "Offsite":
                    addNewRow(ebrCon,ebrAdjustmentProductivity,mpaAvailable,activeServiceContract,excecutionCountry,entry)
            row = ebrCon.AddNewRow(False)
            row["Deliverable"] = "On-Site"
            for entry in queryData:
                if entry.Deliverable_Type == "Onsite":
                    if siteAccepTest in ('No','') and entry.Deliverables == "SAT":
                        continue
                    addNewRow(ebrCon,ebrAdjustmentProductivity,mpaAvailable,activeServiceContract,excecutionCountry,entry)

def migrationDDSCheck(elcnUpgradeNew):
    sum = 0
    rowIndex = 0
    for row in elcnUpgradeNew.Rows:
        if rowIndex < 2:
            for column in row.Columns:
                if row[column.Name] != '':
                    sum += int(row[column.Name])
        rowIndex += 1
    if sum > 0:
        return sum
    else:
        return 0

def populatelLabCon(LabCon,AdjustmentProductivity,mpaAvailable,activeServiceContract,contractType,modulename):
    if LabCon.Rows.Count == 0:
        excecutionCountry = getExecutionCountry()
        queryData = SqlHelper.GetList("select * from LABOR_DELIVERABLES where Product_Module = '{}'and Contract = '{}'".format(modulename,contractType))
        row = LabCon.AddNewRow(False)
        row["Deliverable"] = "Total"
        row = LabCon.AddNewRow(False)
        row["Deliverable"] = "Off-Site"
        if queryData is not None:
            for entry in queryData:
                if Product.ParseString(entry.Deliverable_Type) == "Offsite":
                    row = LabCon.AddNewRow(False)
                    row["Deliverable"] = entry.Deliverables
                    row["Deliverable_Type"] = "Offsite"
                    row["Adjustment_Productivity"] = AdjustmentProductivity
                    row["Execution_Year"] = str(executionYear)
                    row["FO_Eng"] = entry.FO_Eng
                    if getAttrValue("MSID_GES_Location") != 'None':
                        row["FO_Eng_Percentage_Split"] = Product.ParseString(entry.FO_Eng_Split)
                        row["GES_Eng_Percentage_Split"] = Product.ParseString(entry.GES_Eng_Split)
                        row["GES_Eng"] = "SVC_GES_P350B_{}".format(TagParserProduct.ParseString('<*ValueCode(MSID_GES_Location)*>'))
                    else:
                        row["FO_Eng_Percentage_Split"] = "100"
                        row["GES_Eng_Percentage_Split"] = "0"
                    if excecutionCountry:
                        row["Execution_Country"] = excecutionCountry
            row = LabCon.AddNewRow(False)
            row["Deliverable"] = "On-Site"
            for entry in queryData:
                if Product.ParseString(entry.Deliverable_Type) == "Onsite":
                    row = LabCon.AddNewRow(False)
                    row["Deliverable"] = entry.Deliverables
                    row["Deliverable_Type"] = "Onsite"
                    row["Adjustment_Productivity"] = AdjustmentProductivity
                    row["Execution_Year"] = str(executionYear)
                    row["FO_Eng"] = entry.FO_Eng
                    if getAttrValue("MSID_GES_Location") != 'None':
                        row["FO_Eng_Percentage_Split"] = Product.ParseString(entry.FO_Eng_Split)
                        row["GES_Eng_Percentage_Split"] = Product.ParseString(entry.GES_Eng_Split)
                        row["GES_Eng"] = "SVC_GES_P350F_{}".format(TagParserProduct.ParseString('<*ValueCode(MSID_GES_Location)*>'))
                    else:
                        row["FO_Eng_Percentage_Split"] = "100"
                        row["GES_Eng_Percentage_Split"] = "0"
                    if excecutionCountry:
                        row["Execution_Country"] = excecutionCountry

def populatelCWSRAELabCon(LabCon,AdjustmentProductivity,mpaAvailable,activeServiceContract,contractType,modulename):
    if LabCon.Rows.Count == 0:
        excecutionCountry = getExecutionCountry()
        queryData = SqlHelper.GetList("select * from LABOR_DELIVERABLES where Product_Module = '{}'and Contract = '{}'".format(modulename,contractType))
        row = LabCon.AddNewRow(False)
        row["Deliverable"] = "Total"
        row = LabCon.AddNewRow(False)
        row["Deliverable"] = "Off-Site"
        if queryData is not None:
            for entry in queryData:
                if Product.ParseString(entry.Deliverable_Type) == "Offsite":
                    row = LabCon.AddNewRow(False)
                    row["Deliverable"] = entry.Deliverables
                    row["Deliverable_Type"] = "Offsite"
                    row["Adjustment_Productivity"] = AdjustmentProductivity
                    row["Execution_Year"] = str(executionYear)
                    row["FO_Eng"] = entry.FO_Eng
                    if getAttrValue("MSID_GES_Location") != 'None':
                        row["FO_Eng_Percentage_Split"] = Product.ParseString(entry.FO_Eng_Split)
                        row["GES_Eng_Percentage_Split"] = Product.ParseString(entry.GES_Eng_Split)
                        if row["Deliverable"] == "MD CD Configuration":
                            row["GES_Eng"] = "SVC_GES_P350B_CN"
                        else:
                            row["GES_Eng"] = "SVC_GES_P350B_{}".format(TagParserProduct.ParseString('<*ValueCode(MSID_GES_Location)*>'))
                    else:
                        if row["Deliverable"] in ("MD CD Configuration","Server/Station Build"):
                            row["FO_Eng_Percentage_Split"] = "0"
                            row["GES_Eng_Percentage_Split"] = "0"
                        else:
                            row["FO_Eng_Percentage_Split"] = "100"
                            row["GES_Eng_Percentage_Split"] = "0"
                    if excecutionCountry:
                        row["Execution_Country"] = excecutionCountry
            row = LabCon.AddNewRow(False)
            row["Deliverable"] = "On-Site"
            for entry in queryData:
                if Product.ParseString(entry.Deliverable_Type) == "Onsite":
                    row = LabCon.AddNewRow(False)
                    row["Deliverable"] = entry.Deliverables
                    row["Deliverable_Type"] = "Onsite"
                    row["Adjustment_Productivity"] = AdjustmentProductivity
                    row["Execution_Year"] = str(executionYear)
                    row["FO_Eng"] = entry.FO_Eng
                    if getAttrValue("MSID_GES_Location") != 'None':
                        row["FO_Eng_Percentage_Split"] = Product.ParseString(entry.FO_Eng_Split)
                        row["GES_Eng_Percentage_Split"] = Product.ParseString(entry.GES_Eng_Split)
                        row["GES_Eng"] = "SVC_GES_P350F_{}".format(TagParserProduct.ParseString('<*ValueCode(MSID_GES_Location)*>'))
                    else:
                        row["FO_Eng_Percentage_Split"] = "100"
                        row["GES_Eng_Percentage_Split"] = "0"
                    if excecutionCountry:
                        row["Execution_Country"] = excecutionCountry

def populatelGraphicsLabCon(LabCon,AdjustmentProductivity,mpaAvailable,activeServiceContract,contractType,modulename):
    if LabCon.Rows.Count == 0:
        excecutionCountry = getExecutionCountry()
        queryData = SqlHelper.GetList("select * from LABOR_DELIVERABLES where Product_Module = '{}'and Contract = '{}'".format(modulename,contractType))
        row = LabCon.AddNewRow(False)
        row["Deliverable"] = "Total"
        row = LabCon.AddNewRow(False)
        row["Deliverable"] = "Off-Site"
        if queryData is not None:
            for entry in queryData:
                if Product.ParseString(entry.Deliverable_Type) == "Offsite":
                    row = LabCon.AddNewRow(False)
                    row["Deliverable"] = entry.Deliverables
                    row["Deliverable_Type"] = "Offsite"
                    row["Adjustment_Productivity"] = AdjustmentProductivity
                    row["Execution_Year"] = str(executionYear)
                    row["FO_Eng"] = entry.FO_Eng
                    if getAttrValue("MSID_GES_Location") != 'None':
                        row["FO_Eng_Percentage_Split"] = Product.ParseString(entry.FO_Eng_Split)
                        row["GES_Eng_Percentage_Split"] = Product.ParseString(entry.GES_Eng_Split)
                        row["GES_Eng"] = "SVC_GES_P335B_{}".format(TagParserProduct.ParseString('<*ValueCode(MSID_GES_Location)*>'))
                    else:
                        row["FO_Eng_Percentage_Split"] = "100"
                        row["GES_Eng_Percentage_Split"] = "0"
                    if excecutionCountry:
                        row["Execution_Country"] = excecutionCountry
            row = LabCon.AddNewRow(False)
            row["Deliverable"] = "On-Site"
            for entry in queryData:
                if Product.ParseString(entry.Deliverable_Type) == "Onsite":
                    row = LabCon.AddNewRow(False)
                    row["Deliverable"] = entry.Deliverables
                    row["Deliverable_Type"] = "Onsite"
                    row["Adjustment_Productivity"] = AdjustmentProductivity
                    row["Execution_Year"] = str(executionYear)
                    row["FO_Eng"] = entry.FO_Eng
                    if getAttrValue("MSID_GES_Location") != 'None':
                        row["FO_Eng_Percentage_Split"] = Product.ParseString(entry.FO_Eng_Split)
                        row["GES_Eng_Percentage_Split"] = Product.ParseString(entry.GES_Eng_Split)
                        row["GES_Eng"] = "SVC_GES_P335F_{}".format(TagParserProduct.ParseString('<*ValueCode(MSID_GES_Location)*>'))
                    else:
                        row["FO_Eng_Percentage_Split"] = "100"
                        row["GES_Eng_Percentage_Split"] = "0"
                    if excecutionCountry:
                        row["Execution_Country"] = excecutionCountry
                    

def populatelELCNCon(elcnCon,elcnAdjustmentProductivity,mpaAvailable,activeServiceContract):
    dataGatheringRequired = getRowData("MSID_CommonQuestions","MSID_FEL_Data_Gathering_Required")
    offProcessSetup = getRowData("ELCN_Services","ELCN_Off_Process_Setup_Validation_Required")
    willOpmandTPStoExperion = getRowData("ELCN_Services","ELCN_Will_OPM_or_TPS_to_Experion_be_performed")
    elcnUpgradeNew = getContainer("ELCN_Upgrade_New_ELCN_Nodes")
    sum = migrationDDSCheck(elcnUpgradeNew)
    if elcnCon.Rows.Count == 0:
        excecutionCountry = getExecutionCountry()
        queryData = SqlHelper.GetList("select * from LABOR_DELIVERABLES where Product_Module = 'ELCN'")
        row = elcnCon.AddNewRow(False)
        row["Deliverable"] = "Total"
        row = elcnCon.AddNewRow(False)
        row["Deliverable"] = "Off-Site"
        if queryData is not None:
            for entry in queryData:
                if entry.Deliverable_Type == "Offsite":
                    if (dataGatheringRequired == "NO" and entry.Deliverables == "FEL Site Visit Data Gathering") or (offProcessSetup in ('No','') and entry.Deliverables in ('Pre-FAT','FAT')) or (sum == 0 and entry.Deliverables == "Migration DDS"):
                        continue
                    addNewRow(elcnCon,elcnAdjustmentProductivity,mpaAvailable,activeServiceContract,excecutionCountry,entry)
            row = elcnCon.AddNewRow(False)
            row["Deliverable"] = "On-Site"
            for entry in queryData:
                if entry.Deliverable_Type == "Onsite":
                    if willOpmandTPStoExperion == "Yes" and entry.Deliverables == "SAT":
                        continue
                    addNewRow(elcnCon,elcnAdjustmentProductivity,mpaAvailable,activeServiceContract,excecutionCountry,entry)

def populatelCBECCon(cbecCon,cbecAdjustmentProductivity,mpaAvailable,activeServiceContract,contractType):
    if cbecCon.Rows.Count == 0:
        excecutionCountry = getExecutionCountry()
        queryData = SqlHelper.GetList("select * from LABOR_DELIVERABLES where Product_Module = 'CB-EC Upgrade to C300-UHIO'and Contract = '{}'".format(contractType))
        row = cbecCon.AddNewRow(False)
        row["Deliverable"] = "Total"
        row = cbecCon.AddNewRow(False)
        row["Deliverable"] = "Off-Site"
        if queryData is not None:
            for entry in queryData:
                if entry.Deliverable_Type == "Offsite":
                    addNewRow(cbecCon,cbecAdjustmentProductivity,mpaAvailable,activeServiceContract,excecutionCountry,entry)
            row = cbecCon.AddNewRow(False)
            row["Deliverable"] = "On-Site"
            for entry in queryData:
                if entry.Deliverable_Type == "Onsite":
                    addNewRow(cbecCon,cbecAdjustmentProductivity,mpaAvailable,activeServiceContract,excecutionCountry,entry)

def populateLaborContainers(container,productModule,activeServiceContract):
    if container.Rows.Count == 0:
        queryData = SqlHelper.GetList("select * from LABOR_DELIVERABLES where Product_Module = '{}' and Contract = '{}'".format(productModule,activeServiceContract))
        if queryData is not None:
            for entry in queryData:
                row = container.AddNewRow(False)
                row["Deliverable"] = entry.Deliverables
                row["Deliverable_Type"] = entry.Deliverable_Type if entry.Deliverable_Type else ''
                row["FO_Eng"] = entry.FO_Eng if entry.FO_Eng else ''
                if entry.Deliverables not in ('On-Site','Total','Off-Site'):
                    row["Execution_Year"] = str(executionYear)
                if entry.Deliverables not in ('Total','Off-Site','On-Site'):
                    row["Adjustment_Productivity"] = "1"
                    if getAttrValue("MSID_GES_Location") != 'None':
                        row["FO_Eng_Percentage_Split"] = entry.FO_Eng_Split if entry.FO_Eng_Split else "100"
                        row["GES_Eng_Percentage_Split"] = entry.GES_Eng_Split if entry.GES_Eng_Split else "0"
                        if entry.Deliverable_Type == "Offsite":
                            row["GES_Eng"] = "SVC_GES_P350B_{}".format(TagParserProduct.ParseString('<*ValueCode(MSID_GES_Location)*>'))
                        elif entry.Deliverable_Type == "Onsite":
                            row["GES_Eng"] = "SVC_GES_P350F_{}".format(TagParserProduct.ParseString('<*ValueCode(MSID_GES_Location)*>'))
                    else:
                        row["FO_Eng_Percentage_Split"] = "100"
                        row["GES_Eng_Percentage_Split"] = "0"
                    if excecutionCountry:
                        row["Execution_Country"] = excecutionCountry


def populateprojectManagementCon(projectManagementCon,pmAdjustmentProductivity,mpaAvailable,activeServiceContract):
    if projectManagementCon.Rows.Count == 0:
        excecutionCountry = getExecutionCountry()
        queryData = SqlHelper.GetList("select * from LABOR_DELIVERABLES where Product_Module = 'PM'")
        row = projectManagementCon.AddNewRow(False)
        row["Deliverable"] = "Total"
        if queryData is not None:
            for entry in queryData:
                if entry.Deliverable_Type == "Offsite":
                    row = projectManagementCon.AddNewRow(False)
                    row["Deliverable"] = entry.Deliverables
                    row["Adjustment_Productivity"] = pmAdjustmentProductivity
                    row["Deliverable_Flag"] = entry.Deliverable_Flag
                    row["Deliverable_Type"] = entry.Deliverable_Type
                    row["FO_Eng_Percentage_Split"] = "100"
                    row["GES_Eng_Percentage_Split"] = "0"
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
                    row["Execution_Year"] = str(executionYear)
                    if getAttrValue("MSID_GES_Location") != 'None':
                        row["GES_Eng"] = "SVC_GES_P215B_{}".format(TagParserProduct.ParseString('<*ValueCode(MSID_GES_Location)*>'))
                    if excecutionCountry:
                        row["Execution_Country"] = excecutionCountry
def populatelThirdpartyPLC_UOC_LabCon(LabCon,AdjustmentProductivity,mpaAvailable,activeServiceContract,contractType,modulename):
    if LabCon.Rows.Count == 0:
        excecutionCountry = getExecutionCountry()
        queryData = SqlHelper.GetList("select * from TABLE_3RD_PARTY_PLC_UOC_LABOR_DELIVERABLES")
        row = LabCon.AddNewRow(False)
        row["Deliverable"] = "Total"
        row = LabCon.AddNewRow(False)
        row["Deliverable"] = "Off-Site"
        if queryData is not None:
            for entry in queryData:
                if Product.ParseString(entry.Deliverable_Type) == "Offsite":
                    row = LabCon.AddNewRow(False)
                    row["Deliverable"] = entry.Deliverables
                    row["Deliverable_Type"] = "Offsite"
                    row["Adjustment_Productivity"] = AdjustmentProductivity
                    row["Execution_Year"] = str(executionYear)
                    if mpaAvailable or activeServiceContract == "Yes":
                        row["FO_Eng"] = entry.FO_Eng
                    else:
                        row["FO_Eng"] = str(entry.FO_Eng) + '-NC'
                    if getAttrValue("MSID_GES_Location") != 'None':
                        row["FO_Eng_Percentage_Split"] = Product.ParseString(entry.FO_Eng_Split)
                        row["GES_Eng_Percentage_Split"] = Product.ParseString(entry.GES_Eng_Split)
                        row["GES_Eng"] = "SVC_GES_PLCB_{}".format(TagParserProduct.ParseString('<*ValueCode(MSID_GES_Location)*>'))
                    else:
                        row["FO_Eng_Percentage_Split"] = "100"
                        row["GES_Eng_Percentage_Split"] = "0"
                    if excecutionCountry:
                        row["Execution_Country"] = excecutionCountry
            row = LabCon.AddNewRow(False)
            row["Deliverable"] = "On-Site"
            for entry in queryData:
                if Product.ParseString(entry.Deliverable_Type) == "Onsite":
                    row = LabCon.AddNewRow(False)
                    row["Deliverable"] = entry.Deliverables
                    row["Deliverable_Type"] = "Onsite"
                    row["Adjustment_Productivity"] = AdjustmentProductivity
                    row["Execution_Year"] = str(executionYear)
                    if mpaAvailable or activeServiceContract == "Yes":
                        row["FO_Eng"] = entry.FO_Eng
                    else:
                        row["FO_Eng"] = entry.FO_Eng + '-NC'
                    if getAttrValue("MSID_GES_Location") != 'None':
                        row["FO_Eng_Percentage_Split"] = Product.ParseString(entry.FO_Eng_Split)
                        row["GES_Eng_Percentage_Split"] = Product.ParseString(entry.GES_Eng_Split)
                        row["GES_Eng"] = "SVC_GES_PLCB_{}".format(TagParserProduct.ParseString('<*ValueCode(MSID_GES_Location)*>'))
                    else:
                        row["FO_Eng_Percentage_Split"] = "100"
                        row["GES_Eng_Percentage_Split"] = "0"
                    if excecutionCountry:
                        row["Execution_Country"] = excecutionCountry
if Product.Attr('MIgration_Scope_Choices').GetValue() != "HW/SW":
    excecutionCountry = getExecutionCountry()
    executionYear = getDefaultExecutionYear()
    foPartNumberCon = getContainer("MSID_Labor_FO_Part_Number")
    opmEngineeringCon = getContainer("MSID_Labor_OPM_Engineering")
    lcnOneTimeUpgradeCon = getContainer("MSID_Labor_LCN_One_Time_Upgrade_Engineering")
    ebrCon = getContainer("MSID_Labor_EBR_Con")
    elcnCon = getContainer("MSID_Labor_ELCN_Con")
    orionConsoleCon = getContainer("MSID_Labor_Orion_Console_Con")
    ehpmCon = getContainer("MSID_Labor_EHPM_C300PM_Con")
    tpsCon = getContainer("MSID_Labor_TPS_TO_EXPERION_Con")
    tcmiCon = getContainer("MSID_Labor_TCMI_Con")
    c200MigrationCon = getContainer("MSID_Labor_C200_Migration_Con")
    ehpmhartioCon = getContainer("MSID_Labor_EHPM_HART_IO_Con")
    cbecCon = getContainer("MSID_Labor_CB-EC_Upgrade_to_C300-UHIO_con")
    fsctosmCon = getContainer("MSID_Labor_FSC_to_SM_con")
    fsctosmauditCon = getContainer("MSID_Labor_FSC_to_SM_audit_Con")
    fdmCon = getContainer("MSID_Labor_FDM_Upgrade_Con")
    xPMCon = getContainer("MSID_Labor_xPM_to_C300_Migration_Con")
    lmCon = getContainer("MSID_Labor_LM_to_ELMM_Con")
    XP10Con = getContainer("MSID_Labor_XP10_Actuator_Upgrade_con")
    CDActuatorCon = getContainer("MSID_Labor_CD_Actuator_con")
    fscsmioCon = getContainer("MSID_Labor_FSCtoSM_IO_con")
    fsctosmioauditCon = getContainer("MSID_Labor_FSC_to_SM_IO_Audit_Con")
    thirdPartyConPLC_UOC = getContainer("3rd_Party_PLC_UOC_Labor")
    projectManagementCon = getContainer("MSID_Labor_Project_Management")
    opmAdjustmentProductivity =getAttrValue("OPM_Adjustment_Productivity")
    lcnAdjustmentProductivity =getAttrValue("LCN_Adjustment_Productivity")
    ebrAdjustmentProductivity =getAttrValue("EBR_Adjustment_Productivity")
    elcnAdjustmentProductivity =getAttrValue("ELCN_Adjustment_Productivity")
    cbecAdjustmentProductivity =getAttrValue("CB-EC_Upgrade_to_C300-UHIO_Adjustment_Productivity")
    fsctosmAdjustmentProductivity = getAttrValue("FSC_to_SM_Adjustment_Productivity")
    fsctosmauditAdjustmentProductivity = getAttrValue("FSC_to_SM_audit_Adjustment_Productivity")
    fdmAdjustmentProductivity =getAttrValue("FDM_Upgrade_Adjustment_Productivity")
    xPMAdjustmentProductivity =getAttrValue("xPM_to_C300_Migration_Adjustment_Productivity")
    lmAdjustmentProductivity =getAttrValue("LM_to_ELMM_Adjustment_Productivity")
    XP10AdjustmentProductivity =getAttrValue("XP10_Actuator_Upgrade_Adjustment_Productivity")
    pmAdjustmentProductivity = getAttrValue("PM_Adjustment_Productivity")
    thirdPartyAdjustmentProductivity_PLC_UOC = getAttrValue("3rd_Party_PLC_UOC_Labor_Productivity") if getAttrValue("3rd_Party_PLC_UOC_Labor_Productivity") else "1"
    GraphicsCon = getContainer("MSID_Labor_Graphics_Migration_con")
    GraphicsAdjustmentProductivity = getAttrValue("Graphics_Migration_Adjustment_Productivity")
    CWSRAECon = getContainer("MSID_Labor_CWS_RAE_Upgrade_con")
    CWSRAEAdjustmentProductivity = getAttrValue("CWS_RAE_Upgrade_Adjustment_Productivity")
    CDActuatorAdjustmentProductivity = getAttrValue("CD_Actuator_Adjustment_Productivity")
    fscsmioAdjustmentProductivity = getAttrValue("FSCtoSM_IO_Adjustment_Productivity")
    fsctosmioauditAdjustmentProductivity = getAttrValue("MSID_Labor_Fsc_SM_IO_Audit_Productivity")
    mpaAvailable = checkForMPACustomer()
    activeServiceContract = getAttrValue("MSID_Active_Service_Contract")
    if activeServiceContract == 'Yes' or mpaAvailable:
        contractType = "Contract"
    else:
        contractType = "Non-Contract"

    selectedProducts = Product.Attr('MSID_Selected_Products').GetValue().split('<br>')

    if foPartNumberCon.Rows.Count == 0 or (str(selectedProducts) != Product.Attr("MSID_Selected_Products_Flag").GetValue()):
        ScriptExecutor.Execute('PS_PopulatePartNumberContainer',{"Product": Product})
        Product.Attr("MSID_Selected_Products_Flag").AssignValue(str(selectedProducts))

    populateOpmCon(opmEngineeringCon,"OPM",mpaAvailable,activeServiceContract) if "OPM" in selectedProducts else 0
    populatelcnOneTimeUpgradeCon(lcnOneTimeUpgradeCon,lcnAdjustmentProductivity,mpaAvailable,activeServiceContract) if "LCN One Time Upgrade" in selectedProducts else 0
    populatelEBRCon(ebrCon,ebrAdjustmentProductivity,mpaAvailable,activeServiceContract,excecutionCountry) if "EBR" in selectedProducts else 0
    populatelELCNCon(elcnCon,elcnAdjustmentProductivity,mpaAvailable,activeServiceContract) if "ELCN" in selectedProducts else 0
    populatelCBECCon(cbecCon,cbecAdjustmentProductivity,mpaAvailable,activeServiceContract,contractType) if "CB-EC Upgrade to C300-UHIO" in selectedProducts else 0
    populatelLabCon(fdmCon,fdmAdjustmentProductivity,mpaAvailable,activeServiceContract,contractType,"FDM Upgrade") if "FDM Upgrade" in selectedProducts else 0
    populatelLabCon(XP10Con,XP10AdjustmentProductivity,mpaAvailable,activeServiceContract,contractType,"XP10 Actuator Upgrade") if "XP10 Actuator Upgrade" in selectedProducts else 0
    populatelLabCon(fsctosmCon,fsctosmAdjustmentProductivity,mpaAvailable,activeServiceContract,contractType,"FSC to SM") if "FSC to SM" in selectedProducts else 0
    populatelLabCon(fsctosmauditCon,fsctosmauditAdjustmentProductivity,mpaAvailable,activeServiceContract,contractType,"FSC to SM Audit") if "FSC to SM" in selectedProducts else 0
    populatelLabCon(xPMCon,xPMAdjustmentProductivity,mpaAvailable,activeServiceContract,contractType,"xPM to C300 Migration") if "xPM to C300 Migration" in selectedProducts else 0
    populatelLabCon(lmCon,lmAdjustmentProductivity,mpaAvailable,activeServiceContract,contractType,"LM to ELMM ControlEdge PLC") if "LM to ELMM ControlEdge PLC" in selectedProducts else 0
    populatelGraphicsLabCon(GraphicsCon,GraphicsAdjustmentProductivity,mpaAvailable,activeServiceContract,contractType,"Graphics Migration") if "Graphics Migration" in selectedProducts else 0
    #populatelLabCon(CWSRAECon,CWSRAEAdjustmentProductivity,mpaAvailable,activeServiceContract,contractType,"CWS RAE Upgrade") if "CWS RAE Upgrade" in selectedProducts else 0
    populatelCWSRAELabCon(CWSRAECon,CWSRAEAdjustmentProductivity,mpaAvailable,activeServiceContract,contractType,"CWS RAE Upgrade") if "CWS RAE Upgrade" in selectedProducts else 0
    populatelLabCon( CDActuatorCon,CDActuatorAdjustmentProductivity,mpaAvailable,activeServiceContract,contractType,"CD Actuator I-F Upgrade") if "CD Actuator I-F Upgrade" in selectedProducts else 0
    populatelThirdpartyPLC_UOC_LabCon( thirdPartyConPLC_UOC,thirdPartyAdjustmentProductivity_PLC_UOC,mpaAvailable,activeServiceContract,contractType,"3rd Party PLC to ControlEdge PLC/UOC") if "3rd Party PLC to ControlEdge PLC/UOC" in selectedProducts else 0
    populatelLabCon( fscsmioCon,fscsmioAdjustmentProductivity,mpaAvailable,activeServiceContract,contractType,"FSC to SM IO Migration") if "FSC to SM IO Migration" in selectedProducts else 0
    populateprojectManagementCon(projectManagementCon,pmAdjustmentProductivity,mpaAvailable,activeServiceContract) 
    populateLaborContainers(orionConsoleCon,"Orion Console",contractType) if "Orion Console" in selectedProducts else 0
    populateLaborContainers(ehpmCon,"EHPM/EHPMX/ C300PM",contractType) if "EHPM/EHPMX/ C300PM" in selectedProducts else 0
    populateLaborContainers(tpsCon,"TPS TO EXPERION",contractType) if "TPS to Experion" in selectedProducts else 0
    populateLaborContainers(tcmiCon,"TCMI",contractType) if "TCMI" in selectedProducts else 0
    populateLaborContainers(ehpmhartioCon,"EHPM HART IO",contractType) if "EHPM HART IO" in selectedProducts else 0
    populatelLabCon(fsctosmioauditCon,fsctosmioauditAdjustmentProductivity,mpaAvailable,activeServiceContract,contractType,"FSC to SM IO Audit") if "FSC to SM IO Migration" in selectedProducts else 0
    
    if "C200 Migration" in selectedProducts:
        migrationScenarioCon = getContainer('C200_Migration_Scenario_Cont').Rows
        for row in migrationScenarioCon:
            migrationScenario = row['C200_Select_the_Migration_Scenario']
            break
        if migrationScenario in ['C200 to C300','']:
            #c200MigrationCon.Clear()
            populateLaborContainers(c200MigrationCon,"C200 C300 Migration",contractType)
        elif migrationScenario == 'C200 to ControlEdge UOC':
            #c200MigrationCon.Clear()
            populateLaborContainers(c200MigrationCon,"C200 Migration",contractType)