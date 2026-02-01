Log.Write("PS_PopulateRegionalCost executed")
def getContainer(product,Name):
    return product.GetContainerByName(Name)

def addFinalHours(totalDict , partNumber,key, value):
    partDict = totalDict.get(partNumber,dict())
    partDict[key] = getFloat(partDict.get(key , 0)) + getFloat(value)
    totalDict[partNumber] = partDict

def getFloat(Var):
    if Var:
        return float(Var)
    return 0

def getpartNumbersData(container,product):
    partsNumbers[productCon[product]] = dict()
    for row in container.Rows:
        if row["Regional_Cost"] not in ('',0.0):
            addFinalHours(partsNumbers[productCon[product]],row["FO_Eng"],"Cost",row["Regional_Cost"])
            addFinalHours(partsNumbers[productCon[product]],row["FO_Eng"],"Qty",(round(getFloat(row["Final_Hrs"]) * getFloat(row["FO_Eng_Percentage_Split"]) / 100)))
        if row["FOUnitWTWCost"] not in ('',0.0):
            addFinalHours(partsNumbers[productCon[product]],row["FO_Eng"],"WTWCost",row["FOUnitWTWCost"])
        if row["GES_Regional_Cost"] not in ('',0.0):
            addFinalHours(partsNumbers[productCon[product]],row["GES_Eng"],"Cost",row["GES_Regional_Cost"])
            addFinalHours(partsNumbers[productCon[product]],row["GES_Eng"],"Qty",(round(getFloat(row["Final_Hrs"]) * getFloat(row["GES_Eng_Percentage_Split"]) / 100)))
        if row["FO_ListPrice"] not in ('',0.0):
            addFinalHours(partsNumbers[productCon[product]],row["FO_Eng"],"ListPrice",row["FO_ListPrice"])
        if row["GES_ListPrice"] not in ('',0.0):
            addFinalHours(partsNumbers[productCon[product]],row["GES_Eng"],"ListPrice",row["GES_ListPrice"])
        if row["GES_MPA_Price"] not in ('',0.0):
            addFinalHours(partsNumbers[productCon[product]],row["GES_Eng"],"MPAPrice",row["GES_MPA_Price"])
            addFinalHours(partsNumbers[productCon[product]],row["GES_Eng"],"MPAQty",(round(getFloat(row["Final_Hrs"]) * getFloat(row["GES_Eng_Percentage_Split"]) / 100)))
        if row["FO_MPA_Price"] not in ('',0.0):
            addFinalHours(partsNumbers[productCon[product]],row["FO_Eng"],"MPAPrice",row["FO_MPA_Price"])
            addFinalHours(partsNumbers[productCon[product]],row["FO_Eng"],"MPAQty",(round(getFloat(row["Final_Hrs"]) * getFloat(row["FO_Eng_Percentage_Split"]) / 100)))


if 1:
    productCon = dict()
    partsNumbers = dict()
    laborParts = dict()
    laborPartsListPrice = dict()
    

    productCon["Trace Software"] = "001"
    productCon["Project Management"] = "002"
    traceSoftwareCon = getContainer(Product,"Trace_Software_Labor_con")
    projectManagementCon = getContainer(Product,"Trace_Project_Management_Labor_con")

    if productCon.get("Trace Software"):
        getpartNumbersData(traceSoftwareCon,"Trace Software")
    if productCon.get("Project Management"):
        getpartNumbersData(projectManagementCon,"Project Management")
    Trace.Write(str(partsNumbers))
    #Trace.Write(str(laborParts))
    #Trace.Write(str(laborPartsListPrice))
    if partsNumbers:
        parentitem = ''
        module = {}
        for item in arg.QuoteItemCollection:
            if 1:
                if parentitem == '' or parentitem == item.ParentItemGuid:
                    parentitem = item.ParentItemGuid
                    module =  partsNumbers["001"]
                else:
                    module =  partsNumbers["002"]
                Trace.Write(JsonHelper.Serialize(module))
                partData = module.get(item.PartNumber,'')
                #item.QI_Manual_labor_Regional_Cost.Value = float(x.get(item.PartNumber,0))
                if partData :
                    if "Cost" in partData and getFloat(partData.get("Qty",0))>0:
                        unitCost = getFloat(partData.get("Cost",0)) / getFloat(partData.get("Qty",0))
                        Trace.Write("Test2 = " + str(unitCost))
                        item.QI_GESRegionalCost.Value = getFloat(unitCost) if unitCost else 0
                    if "WTWCost" in partData and getFloat(partData.get("Qty",0))>0:
                        unitWtwCost = getFloat(partData.get("WTWCost",0)) / getFloat(partData.get("Qty",0))
                        Trace.Write("Test3 = " + str(unitWtwCost))
                        item.QI_FoWTWCost.Value = getFloat(unitWtwCost) if unitWtwCost else 0
                    if "ListPrice" in partData and getFloat(partData.get("Qty",0))>0:
                        unitListPrice = getFloat(partData.get("ListPrice",0)) / getFloat(partData.get("Qty",0))
                        Trace.Write("Test4 = " + str(unitListPrice))
                        item.QI_LaorPartsListPrice.Value = getFloat(unitListPrice) if unitListPrice else 0
                    if "MPAPrice" in partData and getFloat(partData.get("MPAQty",0))>0:
                        unitMPAPrice = getFloat(partData.get("MPAPrice",0)) / getFloat(partData.get("MPAQty",0))
                        item.QI_MPA_Price.Value = getFloat(unitMPAPrice) if unitMPAPrice else 0
Quote.Calculate()