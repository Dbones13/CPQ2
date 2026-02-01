import ProductUtil

def getAttrValue(row , colName):
    return row.GetColumnByName(colName).DisplayValue

def getRowAttrValue(row , attrName):
    return row.Product.Attr(attrName).GetValue()

def setRowAttrValue(row , attrName , attrValue):
    row.Product.Attr(attrName).AssignValue(attrValue)

def getSystemIdDict(partsList):
    query = "select SYSTEM_ID,PRODUCT_NAME,PRODUCT_CATALOG_CODE from products where PRODUCT_CATALOG_CODE in ('{}') and PRODUCT_ACTIVE = 'True'".format("','".join(partsList))
    res = SqlHelper.GetList(query)
    partsDict = dict()
    for r in res:
        partsDict[r.PRODUCT_CATALOG_CODE] = r.SYSTEM_ID
    return partsDict

def getPLSG(partNumber):
    query = "select PLSG from HPS_PRODUCTS_MASTER where PartNumber = '{}'".format(partNumber)
    res = SqlHelper.GetFirst(query)
    return res.PLSG

fieldContainer = Product.GetContainerByName("RTU Field container")
row = fieldContainer.Rows[0]

systemType = getAttrValue(row , "System Type")
mediaType = getAttrValue(row , "Media Type")
release = getAttrValue(row , "Release")
enggStation = getAttrValue(row , "Engineering Stations")
meteringLibrary = getAttrValue(row , "Calculation Library Required")

rtuContainer = Product.GetContainerByName("RTU Groups")
rtuParts = Product.GetContainerByName("RTU Parts")

partDict = {
    "Physical R151" : "SP-EMD151" ,
    "Physical R160" : "SP-EMD160" ,
    "Physical R150" : "SP-EMD150",
    "Electronic R151" : "SP-EMD151-ESD" ,
    "Electronic R160" : "SP-EMD160-ESD" ,
    "Electronic R150" : "SP-EMD150-ESD"
}

partsToAdd = dict()
partsList = []
toBeDeleted = []

if systemType == "New":
    if mediaType and release:
        key = "{} {}".format(mediaType.split()[0] , release)
        partsToAdd[partDict[key]] = 1
        partsList.append(partDict[key])
    if enggStation:
        partsToAdd["SP-EBLDR1"] = enggStation
        partsList.append("SP-EBLDR1")
    if meteringLibrary == "Yes":
        partsToAdd["SP-MCALC1"] = 1
        partsList.append("SP-MCALC1")

for row in rtuParts.Rows:
    partNumber = row['Part Number']
    if partsToAdd.get(partNumber , 0):
        row['ItemQuantity'] = str(partsToAdd.get(partNumber))
        #row.Product.Attributes.GetByName("ItemQuantity").AssignValue(str(partsToAdd.get(partNumber)))
        #Trace.Write("ItemQuantity "+str(row.Product.Attributes.GetByName("ItemQuantity").GetValue()))
        row.ApplyProductChanges()
        partsToAdd.pop(partNumber)
        continue
    toBeDeleted.append(row.RowIndex)

systemIdDict = getSystemIdDict(partsList)

for partNumber , quantity in partsToAdd.items():
    row = rtuParts.AddNewRow(systemIdDict[partNumber] , False)
    row['Part Number'] = partNumber
    row['ItemQuantity'] = str(quantity)
    row['PLSG'] = getPLSG(partNumber)
    #row.Product.Attributes.GetByName("ItemQuantity").AssignValue(str(partsToAdd.get(partNumber)))
    #Trace.Write("ItemQuantity "+str(row.Product.Attributes.GetByName("ItemQuantity").GetValue()))
    row.ApplyProductChanges()

deletedCount = 0

for index in toBeDeleted:
    rtuParts.DeleteRow(index - deletedCount)
    deletedCount -= 1

rtuParts.Calculate()