def getCFValue(name):
    return Quote.GetCustomField(name).Content

def getCFValueCode(name):
    return Quote.GetCustomField(name).Content

def getAuthCred():
    authCred = {}
    query = SqlHelper.GetList("select * from HPS_INTEGRATION_PARAMS")
    if query is not None:
        for rec in query:
            if rec.Key in ('Project_Create_UserName','Project_Create_Password'):
                authCred[rec.Key] = rec.Value
    #Trace.Write(str(authCred))
    return authCred

def getBearerToken(header , record):
    #url = "https://oauthasservices-h197bcf13.us3.hana.ondemand.com"
    #url = "https://hon-s4-prod-integrations-lzmw5lfz.authentication.us21.hana.ondemand.com"
    #endPoint = "/oauth/token?grant_type=client_credentials"
    #res = RestClient.Post('{}{}'.format(url , endPoint) ,record, header)
    
        #https://hon-s4-qa-integration-oxhchcn0.authentication.us21.hana.ondemand.com/oauth/token
    
    #Code change for Order Booking - H122094 - Start Here
    
    #url = "https://hon-s4-qa-integration-oxhchcn0.authentication.us21.hana.ondemand.com"
    #endPoint = "/oauth/token?grant_type=client_credentials"
    #res = RestClient.Post('{}{}'.format(url , endPoint) ,record, header)
    
    ProjToken = SqlHelper.GetFirst("SELECT Value FROM HPS_INTEGRATION_PARAMS WHERE [Key] = 'PROJECT_BEARER_TOKEN' ").Value
    res = RestClient.Post('{}'.format(ProjToken),record, header)
    #Code change for Order Booking - H122094 - End Here
    
    return "{} {}".format(res.token_type , res.access_token)

def sendProjectJSON(header , record):
    #url = "https://hon-s4-prod-integrations-lzmw5lfz.it-cpi013-rt.cfapps.us21.hana.ondemand.com/http"
    #endPoint = "/HPSCPQ/ERP/ProjectBooking/PROD"
    #res = RestClient.Post('{}{}'.format(url , endPoint),record, header)
    
    #Code change for Order Booking - H122094 - Start Here
    #url = ""https://l251076-iflmap.hcisbp.us3.hana.ondemand.com/http""
    #endPoint = ""/HPSCPQ/ERP/ProjectBooking//QA""
    SendProjectUrL = SqlHelper.GetFirst("SELECT Value FROM HPS_INTEGRATION_PARAMS WHERE [Key] = 'PROJECT_CREATION_URL' ").Value
    res = RestClient.Post('{}'.format(SendProjectUrL),record, header)
     #url = ""https://hon-s4-qa-integration-oxhchcn0.it-cpi013-rt.cfapps.us21.hana.ondemand.com/http""
    #endPoint = ""/HPSCPQ/ERP/ProjectBooking/QA""
    #res = RestClient.Post('{}{}'.format(url , endPoint),record, header)
    #Code change for Order Booking - H122094 - End Here
    return res


def getMilestoneUsageCode():
    milUsageCodeDict = dict()
    usageCode = SqlHelper.GetList("select * from MILESTONE_DESCRIPTION where MilestoneUsageCode != ''")
    if usageCode is not None:
        for rec in usageCode:
            milUsageCodeDict[rec.Billing_Milestone] = rec.MilestoneUsageCode
    #Trace.Write(str(milUsageCodeDict))
    return milUsageCodeDict

def getActivityDetails():
    activityDict = dict()
    query = SqlHelper.GetList("select * from PROJECT_ACTIVITY_DETAILS")
    if query is not None:
        for rec in query:
            activityDict[rec.ProductType] = [rec.ControlKey,rec.ActivityName,rec.GLAccount]
    return activityDict

def populateMilestoneTable(milestoneTable,poDate,milUsageCodeDict):
    for row in milestoneTable.Rows:
        if row["EGAP_Weeks_ARO"]  >= 0 and poDate:
            milestoneDate = str(UserPersonalizationHelper.CovertToDate(poDate).AddDays(row["EGAP_Weeks_ARO"] * 7))
            row['Milestone_Date'] = str( TagParserQuote.ParseString('<*CTX( Date({}).Format(yyyyMMdd) )*>'.format(milestoneDate)))
        row['Milestone_Usage_Code'] = milUsageCodeDict.get(row['EGAP_Milestone_Name'],"")

poDate = getCFValue("PurchaseOrderDate")
milestoneTable = Quote.QuoteTables['EGAP_Project_Milestone']
milUsageCodeDict = getMilestoneUsageCode()
populateMilestoneTable(milestoneTable,poDate,milUsageCodeDict)
projectType = TagParserQuote.ParseString('<*CTX( Quote.CustomField(EGAP_Project_Type).AttrValueCode )*>')
contractEndDate = TagParserQuote.ParseString('<*CTX( Quote.CustomField(EGAP_Contract_End_Date).Format(yyyyMMdd) )*>')

projectCreationJson = {}
projetOrderBooking = projectCreationJson.get("Project_Order_Booking",{})

projetheader = projetOrderBooking.get("ProjectHeader",dict())
projetheader["QuoteCompositeNumber"] = Quote.CompositeNumber
projetheader["ProjectCrystalId"] = getCFValue("Opportunity Number")
projetheader["ProjectCurrencyCode"] = getCFValue("Currency")
projetheader["ProjectFinishDate"] = contractEndDate
projetheader["ProjectProfitCenter"] = Quote.GetCustomField('ProfitCentre').Content.Split(',')[0] 
projetheader["ProjectCategory"] = getCFValue("Opportunity Category")
projetheader["ProjectName"] = getCFValue("Opportunity Name")
projetheader["ProjectType"] = projectType if projectType else ''
projetOrderBooking["ProjectHeader"] = projetheader

if projectType!="TIME & MATERIAL":
    projectMilestones = projetOrderBooking.get("ProjectMilestone",[])
    for row in milestoneTable.Rows:
        milestoneDict = dict()
        milestoneDict["ProjectMilestoneDate"] = row["Milestone_Date"] if row["Milestone_Date"] else ""
        milestoneDict["ProjectMilestoneDescription"] = row["EGAP_Milestone_Description"]
        milestoneDict["ProjectMilestoneInvoicePercentage"] = row["EGAP_Pct_of_Total_Milestone_Payment"]
        milestoneDict["ProjectMilestoneUsageCode"] = row["Milestone_Usage_Code"] if row["Milestone_Usage_Code"] else ""
        projectMilestones.append(milestoneDict)
    projetOrderBooking["ProjectMilestone"] = projectMilestones

activityDict = getActivityDetails()
projectActivity = projetOrderBooking.get("ProjectActivity",[])
activityTable = Quote.QuoteTables["QT_Booking_Report"]
for row in activityTable.Rows:
    if row["Product_Type"] and row["Product_Type"] in activityDict and row["Product_Type"] != "Honeywell Labor":
        rowDict = dict()
        rowDict["ProjectActivityControlKey"] = activityDict[row["Product_Type"]][0]
        rowDict["ProjectActivityName"] = activityDict[row["Product_Type"]][1]
        rowDict["ProjectActivityCost"] = row["Cost"]
        rowDict["ProjectGLAccount"] = activityDict[row["Product_Type"]][2]
        rowDict["ProjectNetworkName"] = activityDict[row["Product_Type"]][1]
        rowDict["ProjectQuantity"] = ""
        rowDict["ProjectUnitOfMeasure"] = "EA"
        rowDict["ProjectWBSCategory"] = row["Product_Type"]
        rowDict["ProjectWBSLevel4"] = activityDict[row["Product_Type"]][1]
        rowDict["ProjectWorkCenter"] = ""
        projectActivity.append(rowDict)
    if row["Order_Product_Type"] == "Honeywell Labor":
        rowDict = dict()
        rowDict["ProjectActivityControlKey"] = activityDict["Honeywell Labor"][0]
        rowDict["ProjectActivityName"] = row["Product_Line_Description"]
        rowDict["ProjectActivityCost"] = row["Cost"]
        rowDict["ProjectGLAccount"] = activityDict["Honeywell Labor"][2]
        rowDict["ProjectNetworkName"] = row["Order_SAP_Network_Name"]
        rowDict["ProjectQuantity"] = row["Hrs"]
        rowDict["ProjectUnitOfMeasure"] = "HR"
        rowDict["ProjectWBSCategory"] = activityDict["Honeywell Labor"][1]
        rowDict["ProjectWBSLevel4"] = activityDict["Honeywell Labor"][1]
        rowDict["ProjectWorkCenter"] = ""
        projectActivity.append(rowDict)
projetOrderBooking["ProjectActivity"] = projectActivity

costPlandHeader = projetOrderBooking.get("CostPlanHeader",{})
costPlandHeader["CostPlanCurrencyCode"] = getCFValue("Currency")
costPlanItems = costPlandHeader.get("CostPlanItem",[])
for row in activityTable.Rows:
    if row["Product_Type"] and row["Product_Type"] in activityDict:
        costItemDict = dict()
        costItemDict["CostPlanItemType"] = activityDict[row["Product_Type"]][1]
        costItemDict["CostPlanItemCost"] = row["Cost"]
        costPlanItems.append(costItemDict)
costPlandHeader["CostPlanItem"] = costPlanItems
projetOrderBooking["CostPlanHeader"] = costPlandHeader

projectCreationJson["Project_Order_Booking"] = projetOrderBooking

Trace.Write(RestClient.SerializeToJson(projectCreationJson))

authCred = getAuthCred()
if authCred:
    basicToken = RestClient.GetBasicAuthenticationHeader('{}'.format(authCred['Project_Create_UserName']),'{}'.format(authCred['Project_Create_Password']))
    header = {'Authorization': basicToken}
    bearerToken = getBearerToken(header,'')

    header1 = {'Authorization': bearerToken}
    #projectCreationJson = RestClient.SerializeToJson(projectCreationJson)
    #Trace.Write(str(projectCreationJson))
    res = sendProjectJSON(header1,projectCreationJson)
    Trace.Write(str(res))
    #x = RestClient.Post('https://l251076-iflmap.hcisbp.us3.hana.ondemand.com/http/HPSCPQ/ERP/ProjectBooking//QA',projectCreationJson,header, 'application/json', False)
    response = res.ZPSCREATEPROJECTResponse
    idhocID = response["IdocAssign"]["DbId"] if response else ''
    Trace.Write("idhocID = " + str(idhocID))
    if idhocID != '':
        Quote.ChangeQuoteStatus('Pending Project Creation')
        tableInfo = SqlHelper.GetTable("PROJECTCREATION_BOOKING_IDHOCS")
        tablerow = { "QuoteNumber" : Quote.CompositeNumber, "ProjectCreationIdhocID" :idhocID}
        tableInfo.AddRow(tablerow)
        upsertResult = SqlHelper.Upsert(tableInfo)
ScriptExecutor.Execute('CPQ_SF_CreateUpdateOpportunity')