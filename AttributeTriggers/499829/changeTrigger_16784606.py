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



def updateDefualtPart(container,mpaAvailable,activeServiceContract):
    if container == "Trace_Software_Labor_con":
        for row in getContainer(container).Rows:
            if row["Deliverable"] in ('Trace Existing Drawings Updates'):
                if mpaAvailable or activeServiceContract == "Yes":
                    row["FO_Eng"] = "SVC-EAPS-ST"
                else:
                    row["FO_Eng"] = "SVC-EAPS-ST-NC"
            elif row["Deliverable"] in ('Trace Installation'):
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

ScriptExecutor.Execute('PopulatePartNumberContainer')
projectManagementCon = getContainer("Trace_Project_Management_Labor_con")
additonalCustomDelivCon = getContainer("Trace_Additional_Custom_Deliverables")
foPartNumberCon = getContainer("MSID_Labor_FO_Part_Number")
mpaAvailable = checkForMPACustomer()
activeServiceContract = Product.Attr("Trace_software_Active_Service_Contract").GetValue()

containers = ['Trace_Software_Labor_con']

for container in containers:
    updateDefualtPart(container,mpaAvailable,activeServiceContract)

populatePMCon(projectManagementCon,mpaAvailable,activeServiceContract)
resetContainerColumn(additonalCustomDelivCon,"FO_Eng")