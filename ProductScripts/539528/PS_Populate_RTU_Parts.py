import ProductUtil
import math

def getAttrValue(attrName):
    return Product.Attr(attrName).GetValue()

def setAttrValue(attrName , value):
    Product.Attr(attrName).AssignValue(value)

def getRowAttrValue(row , attrName):
    return row.Product.Attr(attrName).GetValue()

def setRowAttrValue(row , attrName , attrValue):
    row.Product.Attr(attrName).AssignValue(attrValue)

def printMsg(msg):
    Trace.Write(str(msg))

def getAttrValueDict():
    attrValueDict = dict()
    for attr in Product.Attributes:
        if attr.DisplayType != 'Container':
            value = attr.GetValue()
            attrValueDict[attr.Name] = value if value else 0
    return attrValueDict

def calculateIOCount(hart , nonHart , sparePercentage):
    hart = hart if hart else 0
    nonHart = nonHart if hart else 0

    totalInput = int(hart) + int(nonHart)

    spare = (int(sparePercentage) + 100) / 100.0
    return math.ceil(totalInput * spare)

def getSystemIdDict(partsList):
    query = "select SYSTEM_ID,PRODUCT_NAME,PRODUCT_CATALOG_CODE from products where PRODUCT_CATALOG_CODE in ('{}') and PRODUCT_ACTIVE = 'True'".format("','".join(partsList))
    res = SqlHelper.GetList(query)
    partsDict = dict()
    for r in res:
        partsDict[r.PRODUCT_CATALOG_CODE] = r.SYSTEM_ID
    return partsDict

def getIOLimitDict():
    return {
        "LogicalInput"  : 8.0,
        "LogicalOutput" : 2.0,
        "DigitalInput"  : 10.0,
        "DigitalOutput" : 6.0,
        "PulseInput"    : 2.0,
        "WirelessIO"    : 25.0
    }

attrValueDict       = getAttrValueDict()
controllerType      = attrValueDict["Controller Type"]
release             = attrValueDict["Release"]
IOLimitDict         = getIOLimitDict()

partsToAdd = dict()
partsList = []
toBeDeleted = []

sparePercentage     = attrValueDict["IO Spare Percentage"] if attrValueDict["IO Spare Percentage"] else 0

inputIOCount        = calculateIOCount(attrValueDict["Hart Analog Input"] , attrValueDict["Non-Hart Analog Input"] , sparePercentage )
logicalModuleInput  = math.ceil(inputIOCount / IOLimitDict["LogicalInput"])

outputIOCount       = calculateIOCount(attrValueDict["Hart Analog Output"] , attrValueDict["Non-Hart Analog Output"] , sparePercentage)
logicalModuleOutput = math.ceil(outputIOCount / IOLimitDict["LogicalOutput"])

digitalInIOCount    = calculateIOCount(attrValueDict["Digital Input"] , 0 , sparePercentage)
logicalModuleDigIn  = math.ceil(digitalInIOCount / IOLimitDict["DigitalInput"])

digitalOutIOCount   = calculateIOCount(attrValueDict["Digital Output"] , 0 , sparePercentage)
logicalModuleDigOut = math.ceil(digitalOutIOCount / IOLimitDict["DigitalOutput"])

pulseInIOCount      = calculateIOCount(attrValueDict["Pulse Input"] , 0 , sparePercentage)
logicalModulePulseIn= math.ceil(pulseInIOCount / IOLimitDict["PulseInput"])

mixedIOCount        = max(logicalModuleInput , logicalModuleOutput , logicalModuleDigIn , logicalModuleDigOut , logicalModulePulseIn)

finalMixedIOCount   = mixedIOCount if controllerType == "Redundant" else mixedIOCount - 1

if finalMixedIOCount > 0:
    partsToAdd["SC-UMIX01"] = finalMixedIOCount

    rtuRows             = math.ceil(finalMixedIOCount / 9.0)

    leftEndPlate = rtuRows - 1
    if leftEndPlate > 0:
        partsToAdd['SC-TEPL01'] = leftEndPlate

    righEndPlate = rtuRows
    if righEndPlate > 0:
        partsToAdd['SC-TEPR01'] = righEndPlate

    rtuCount = math.ceil(finalMixedIOCount / 30.0)

    if controllerType == "Non-Redundant":
        partsToAdd['SC-UCMX02' if release == 'R160' else 'SC-UCMX01'] = rtuCount
    else:
        partsToAdd['SC-UCNN11'] = rtuCount

    if attrValueDict['ELEPIU Library Required'] == "Yes":
        partsToAdd['SP-LEPIU1'] = rtuCount

    if int(attrValueDict['Hart Analog Input']) + int(attrValueDict['Hart Analog Output']) > 0:
        partsToAdd['SP-IHARTP'] = mixedIOCount

if int(attrValueDict['ISA100 Wireless Devices']) > 0:
    wirelessIOCount = calculateIOCount(attrValueDict["ISA100 Wireless Devices"] , 0 , sparePercentage)
    wirelessIOCount = math.ceil(wirelessIOCount / IOLimitDict["WirelessIO"])
    wirelessIOCount = wirelessIOCount if wirelessIOCount < 25 else 25
    partsToAdd['SP-IWIO01'] = wirelessIOCount

meterRun = int(attrValueDict['Liquid Meter Run Licenses']) + int(attrValueDict['Gas Meter Run Licenses'])
if meterRun:
    partsToAdd['SP-MRUN01'] = meterRun

rtuParts = Product.GetContainerByName("RTU Parts")

for row in rtuParts.Rows:
    partNumber = row['Part Number']
    if partsToAdd.get(partNumber , 0):
        row['ItemQuantity'] = str(partsToAdd.get(partNumber))
        #setRowAttrValue(row , "ItemQuantity" , str(partsToAdd.get(partNumber)))
        partsToAdd.pop(partNumber)
        continue
    toBeDeleted.append(row.RowIndex)

systemIdDict = getSystemIdDict(partsToAdd.keys())

deletedCount = 0

for index in toBeDeleted:
    rtuParts.DeleteRow(index - deletedCount)
    deletedCount -= 1

for partNumber , quantity in partsToAdd.items():
    row = rtuParts.AddNewRow(systemIdDict[partNumber] , False)
    row['Part Number'] = partNumber
    row['ItemQuantity'] = str(quantity)
    #setRowAttrValue(row , "ItemQuantity" , str(partsToAdd.get(partNumber)))

rtuParts.Calculate()