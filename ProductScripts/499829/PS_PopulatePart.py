import math
from ProductUtil import getContainer

def log_dict(d):
    Trace.Write(RestClient.SerializeToJson(d))
    return RestClient.SerializeToJson(d)

def getFloat(var):
    if var:
        return float(var)
    return 0

def addFinalHours(totalDict, key, value):
    totalDict[key] = getFloat(totalDict.get(key, 0)) + getFloat(value)

def migrationAttrDict(product):
    migrationAttrDict = dict()

    return migrationAttrDict

def getPartDetailDict(partsList):
    resDict = dict()
    query = "select PRODUCT_CATALOG_CODE, PRODUCT_NAME, PLSG, PLSGDesc from products p join HPS_PRODUCTS_MASTER hpm ON p.PRODUCT_CATALOG_CODE = hpm.PartNumber where PRODUCT_CATALOG_CODE in ('{0}') UNION select PRODUCT_CATALOG_CODE, PRODUCT_NAME, PLSG, PLSGDesc from Migration_Third_Party_Products where PRODUCT_CATALOG_CODE in ('{0}')"
    query = query.format("','".join(partsList))

    res = SqlHelper.GetList(query)
    for r in res:
        resDict[r.PRODUCT_CATALOG_CODE] = [r.PRODUCT_NAME, r.PLSG, r.PLSGDesc]
    return resDict

def getPartsToBeAdded(attributeValueDict):
    partNumbersToBeAdded = {
        
        "PM": dict(),
        "Trace": dict(),
    }
    partsList = set()

    
    return partNumbersToBeAdded, partsList

def getUserInputMap(container):
    userInputMap = dict()
    for row in container.Rows:
        data = {
            'adjQty' : row['Adj Quantity'],
            'comment' : row['Comments']
        }
        userInputMap[row['PartNumber']] = data

    return userInputMap



attributeValueDict = migrationAttrDict(Product)

partNumbersToBeAdded, partsList = getPartsToBeAdded(attributeValueDict)

if Product.Attr('Trace_Software_Scope_Choices').GetValue() != "HW/SW":
    
    def getLaborContainerData(container,product):
        for row in container.Rows:
            if row["Deliverable"] not in ('Total','Off-Site','On-Site'):
                if row["FO_Eng"]:
                    foQty = round((getFloat(row["Final_Hrs"]) * getFloat(row["FO_Eng_Percentage_Split"]) / 100))
                    addFinalHours(partNumbersToBeAdded[product],row["FO_Eng"],foQty)
                if row["FO_Eng"] not in partsList:
                    partsList.add(row["FO_Eng"])
                if row["GES_Eng"] != '' and row["GES_Eng_Percentage_Split"] != '0':
                    gesQty = round((getFloat(row["Final_Hrs"]) * getFloat(row["GES_Eng_Percentage_Split"]) / 100))
                    #Trace.Write("value = " + str(x))
                    addFinalHours(partNumbersToBeAdded[product],row["GES_Eng"],gesQty)
                if row["GES_Eng"] not in partsList:
                    partsList.add(row["GES_Eng"])

    traceCon = getContainer(Product,"Trace_Software_Labor_con")
    getLaborContainerData(traceCon,"Trace")

    projectManagementCon = getContainer(Product, "Trace_Project_Management_Labor_con")
    for row in projectManagementCon.Rows:
        if row["Deliverable"] not in ('Total','Off-Site','On-Site'):
            if row["FO_Eng"]:
                foQty = round((getFloat(row["Final_Hrs"]) * getFloat(row["FO_Eng_Percentage_Split"]) / 100))
                addFinalHours(partNumbersToBeAdded["PM"],row["FO_Eng"],foQty)
            if row["FO_Eng"] not in partsList:
                partsList.add(row["FO_Eng"])
            if row["GES_Eng"] != '' and row["GES_Eng_Percentage_Split"] != '0':
                gesQty = round((getFloat(row["Final_Hrs"]) * getFloat(row["GES_Eng_Percentage_Split"]) / 100))
                #Trace.Write("value = " + str(x))
                addFinalHours(partNumbersToBeAdded["PM"],row["GES_Eng"],gesQty)
            if row["GES_Eng"] not in partsList:
                partsList.add(row["GES_Eng"])

Trace.Write(RestClient.SerializeToJson(partNumbersToBeAdded))

containerNameMapping = {
    
    "PM": getContainer(Product, "MSID_PM_Added_Parts_Common_Container"),
    "Trace": getContainer(Product, "Trace_Software_Added_Parts_Common_Container")
    
}

partDetailsDict = getPartDetailDict(partsList)

for product, parts in partNumbersToBeAdded.items():
    container = containerNameMapping[product]
    userInputMap = getUserInputMap(container)
    container.Clear()
    for part, qty in parts.items():
        if qty > 0.00 and qty != '':
            row = container.AddNewRow(False)
            row['PartNumber'] = part
            row['Quantity'] = str(qty)
            adjQty = 0
            comment = ''
            if userInputMap.get(part):
                adjQty = getFloat(userInputMap[part]['adjQty'])
                comment = userInputMap[part]['comment']

            row['Adj Quantity'] = str(adjQty)
            row['Final Quantity'] = str(getFloat(qty) + adjQty)
            row['Comments'] = comment
            if partDetailsDict.get(part):
                row['PartDescription'] = partDetailsDict[part][0]
                row['PLSG'] = partDetailsDict[part][1]
                row['plsgDescription'] = partDetailsDict[part][2]

container.Calculate()
x = log_dict(attributeValueDict)