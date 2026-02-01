def getFloat(Var):
    if Var:
        return float(Var)
    return 0


def getCFValue(CFName):
  return Quote.GetCustomField(CFName).Content


def addValues(totalDict , partNumber,key, value):
    partDict = totalDict.get(partNumber,dict())
    partDict[key] = getFloat(partDict.get(key , 0)) + getFloat(value)
    totalDict[partNumber] = partDict

def populateQuoteTable(serviceTable,systemgroup,itemDataDict,header):
    addRow = serviceTable.AddNewRow()
    addRow["Service_Materials"] = "Total"
    addRow["System_Group"] = systemgroup.PartNumber if systemgroup else ''
    addRow["Quote_Item_GuId"] = systemgroup.QuoteItemGuid if systemgroup else ''
    addRow["IsHeader"] = header
    for partnumber in itemDataDict:
        Trace.Write(partnumber)
        addRow = serviceTable.AddNewRow()
        partData = itemDataDict[partnumber]
        addRow["Service_Material_Name"] = partData.get("Service_Material_Name",'')
        addRow["Service_Materials"] = partnumber
        addRow["Hours"] = round(partData.get("Hours",0),2)
        addRow["Unit_Cost"] = str(format(round(partData.get("Unit_Cost",0),2), ".2f"))
        addRow["Total_Cost"] = round(partData.get("Total_Cost",0),2)
        addRow["Unit_Sell_Price"] = str(format(round(partData.get("Unit_Sell_Price",0),2), ".2f"))
        addRow["Total_Sell_Price"] = round(partData.get("Total_Sell_Price",0),2)
        addRow["Quote_Item_GuId"] = systemgroup.QuoteItemGuid if systemgroup else ''
        addRow["IsHeader"] = header
    Trace.Write(str(itemDataDict))

def calculateTotals(serviceTable,systemgroup):
    if serviceTable.Rows.Count > 0:
        totalHours = 0
        totalcost = 0
        totalSellPrice = 0
        for row in serviceTable.Rows:
            if row["Quote_Item_GuId"] == systemgroup.QuoteItemGuid:
                totalHours += getFloat(row["Hours"])
                totalcost += getFloat(row["Total_Cost"])
                totalSellPrice += getFloat(row["Total_Sell_Price"])
        for row in serviceTable.Rows:
            if row["Quote_Item_GuId"] == systemgroup.QuoteItemGuid:
                if row["Service_Materials"] == "Total":
                    row["Hours"] = totalHours
                    row["Total_Cost"] = totalcost
                    row["Total_Sell_Price"] = totalSellPrice
                else:
                    row["Percentage"] = str(format(round((getFloat(row["Hours"]) / totalHours) * 100,2),".2f")) if  totalHours > 0 else 0
                    row["Percentage"] = str(row["Percentage"])+str("%")
def getItemsData(module):
    for part in module.Children:
        if part.ProductTypeName.lower() == "honeywell labor":
            addValues(itemData,part.PartNumber,"Hours",part.Quantity)
            #addValues(itemData,part.PartNumber,"Unit_Cost",part.Cost)
            addValues(itemData,part.PartNumber,"Total_Cost",part.ExtendedCost)
            #addValues(itemData,part.PartNumber,"Unit_Sell_Price",part.NetPrice)
            addValues(itemData,part.PartNumber,"Total_Sell_Price",part.ExtendedAmount)
            itemData[part.PartNumber]["Service_Material_Name"] = part.ProductName
            itemData[part.PartNumber]["Unit_Cost"] = round(itemData[part.PartNumber]["Total_Cost"]/itemData[part.PartNumber]["Hours"],2)
            itemData[part.PartNumber]["Unit_Sell_Price"] = round(itemData[part.PartNumber]["Total_Sell_Price"]/itemData[part.PartNumber]["Hours"],2)

def getsystemgroupItemsData(module):
    for part in module.Children:
        if part.ProductTypeName.lower() == "honeywell labor":
            addValues(systemData,part.PartNumber,"Hours",part.Quantity)
            #addValues(systemData,part.PartNumber,"Unit_Cost",part.Cost)
            addValues(systemData,part.PartNumber,"Total_Cost",part.ExtendedCost)
            #addValues(systemData,part.PartNumber,"Unit_Sell_Price",part.NetPrice)
            addValues(systemData,part.PartNumber,"Total_Sell_Price",part.ExtendedAmount)
            systemData[part.PartNumber]["Service_Material_Name"] = part.ProductName
            systemData[part.PartNumber]["Unit_Cost"] = round(systemData[part.PartNumber]["Total_Cost"]/systemData[part.PartNumber]["Hours"],2)
            systemData[part.PartNumber]["Unit_Sell_Price"] = round(systemData[part.PartNumber]["Total_Sell_Price"]/systemData[part.PartNumber]["Hours"],2)
try:
    product_name=["One Wireless System","Tank Gauging Engineering","Public Address General Alarm System","PRMS Skid Engineering","Metering Skid Engineering", "Fire Detection & Alarm Engineering","MS Analyser System Engineering","Gas MeterSuite Engineering - C300 Functions","Liquid MeterSuite Engineering - C300 Functions","Industrial Security (Access Control)","MeterSuite Engineering - MSC Functions"]
    if getCFValue("Quote Type") == "Projects" and (getCFValue("Booking LOB") == "LSS" or getCFValue("Booking LOB") == "PAS" or getCFValue("Booking LOB") == "PMC"):
        serviceTable = Quote.QuoteTables["Sys_Grp_Service_Material_Labor"]
        serviceTable.Rows.Clear()
        itemData = dict()
        for item in Quote.MainItems:
            if item.PartNumber == "PRJT":
                #itemData = dict()
                for systemgroup in item.Children:
                    systemData = dict()
                    if systemgroup.ProductName == "System Group":
                        for module in systemgroup.Children:
                            if module.ProductName in product_name:
                                getItemsData(module)
                                getsystemgroupItemsData(module)
                        Trace.Write(str(systemData))
                        populateQuoteTable(serviceTable,systemgroup,systemData,"No")
                        calculateTotals(serviceTable,systemgroup)
        headerserviceTable = Quote.QuoteTables["Service_Material_Labor_Type"]
        headerserviceTable.Rows.Clear()
        populateQuoteTable(headerserviceTable,"",itemData,"Yes")
        if headerserviceTable.Rows.Count > 0:
            totalHours = 0
            totalcost = 0
            totalSellPrice = 0
            for row in headerserviceTable.Rows:
                if row["IsHeader"] == "Yes":
                    totalHours += getFloat(row["Hours"])
                    totalcost += getFloat(row["Total_Cost"])
                    totalSellPrice += getFloat(row["Total_Sell_Price"])
            for row in headerserviceTable.Rows:
                if row["IsHeader"] == "Yes":
                    if row["Service_Materials"] == "Total":
                        row["Hours"] = totalHours
                        row["Total_Cost"] = totalcost
                        row["Total_Sell_Price"] = totalSellPrice
                    else:
                        row["Percentage"] = str(format(round((getFloat(row["Hours"]) / totalHours) * 100,2),".2f")) if  totalHours > 0 else 0
                        row["Percentage"] = str(row["Percentage"])+str("%")
        serviceTable.Save()
        headerserviceTable.Save()
except Exception as e:
    Log.Write("Non ICSS"+str(e))