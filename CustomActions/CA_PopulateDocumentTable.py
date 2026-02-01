from GS_DocumentData_Function import getMsidBOM,getMigrationBomDictConsolidated,getMigrationBomDictByMsid,Delete_Quote_Item
from GS_PopulateRow_DocumentTable import populateRow,populateNewRow
def getMsidFromGUID(guid):
    return Quote.GetItemByUniqueIdentifier(guid).PartNumber
def getFloat(val):
    if val:
        return float(val)
    return 0
def populateBOMTableByMsid(bomDict , msidList):
    table = Quote.QuoteTables["Migration_BOM_Table"]
    table.Rows.Clear()
    counter = 0
    for msidGuid  in msidList:
        partsDict = bomDict.get(msidGuid,dict())
        counter = 1
        row = table.AddNewRow()
        row["Item_GUID"] = msidGuid
        row["Part_Description"] = "MSID - {}".format(getMsidFromGUID(msidGuid))
        for part , partData in partsDict.items():
            row = table.AddNewRow()
            row["Item_GUID"] = msidGuid
            row["Item_Number"] = counter
            row["Part_Number"] = part
            row["Part_Description"] = partData[0]
            row["Qty"] = int(partData[1])
            counter += 1
    table.Save()
def getMsidBOM_old(item):
    bomDict = dict()
    msidList = list()
    msidGuidMap = dict()
    for msid in item.Children:
        msidList.append(msid.QuoteItemGuid)
        msidGuidMap[msid.QuoteItemGuid] = msid.PartNumber
        partDict = bomDict.get(msid.QuoteItemGuid , dict())
        for module in msid.Children:
            for part in module.Children:
                if part.PartNumber.startswith('SVC'):
                    continue
                if part.Description == 'CE PLC Control Group' or part.Description == 'UOC Control Group':
                    def temp(part,partDict,msid):
                        for i in part.Children:
                            if i.Description == 'CE PLC Remote Group' or i.Description == 'UOC Remote Group':
                                temp(i,partDict,msid)
                                continue
                            partData1 = partDict.get(i.PartNumber , ["" , 0,"","",""])
                            partData1[0] = i.Description
                            partData1[1] += i.Quantity
                            partData1[2] = i['QI_PLSG'].Value
                            partData1[3] = msid.Description
                            partData1[4] = i.ProductTypeName
                            partDict[i.PartNumber] = partData1
                    temp(part,partDict,msid)
                    continue
                partData = partDict.get(part.PartNumber , ["" , 0,"","",""])
                partData[0] = part.Description
                partData[1] += part.Quantity
                partData[2] = part['QI_PLSG'].Value
                partData[3] = msid.Description
                partData[4] = part.ProductTypeName
                partDict[part.PartNumber] = partData
        bomDict[msid.QuoteItemGuid] = partDict
    return (msidList , bomDict,msidGuidMap)
def getMigrationConsolidatedBom(main_dict):
    consolidated_dict = dict()
    for msid , msidData in main_dict.items():
        for part in msidData:
            partData = consolidated_dict.get(part, ["", 0,"",""])
            partData[0] = msidData[part][0]
            partData[1] += int(msidData[part][1])
            partData[2] = msidData[part][2]
            partData[3] = msidData[part][4]
            consolidated_dict[part] = partData
    return consolidated_dict
def addQuoteTableRow(table, counter, part, description, plsg, qty, productType, MSID_or_Consolidated, msid=""):
  row = table.AddNewRow()
  row["SerialNo"] = counter
  row["MSID"] = msid
  row["ModelNo"] = part
  row["ModelDescription"] = description
  row["PLSG"] = plsg
  row["Total"] = str(qty)
  row["MSID_or_Consolidated"] = str(MSID_or_Consolidated)
  row["Project_Type"] = productType
  table.Save()
def populateQuoteTableBOMExcel(table, bomDict, msidGuidMap, MSID_or_Consolidated):
    try:
        for msid , msidData in bomDict.items():
            addQuoteTableRow(table, "", "", "", "", "", "0","", msidGuidMap[msid])
            counter = 1
            for part in msidData:
                description = msidData[part][0]
                qty = msidData[part][1]
                plsg = msidData[part][2]
                msid = msidData[part][3]
                productType = msidData[part][4]
                addQuoteTableRow(table, counter, part, description, plsg, qty, productType, MSID_or_Consolidated, msid)
                counter += 1
    except:
        Trace.Write("Missing Msid")
def populateQuoteTableConsolidatedBOMExcel(table, consolidated_BOM,MSID_or_Consolidated):
    counter = 1
    for item in consolidated_BOM:
        addQuoteTableRow(table, counter, item, consolidated_BOM[item][0], consolidated_BOM[item][2], consolidated_BOM[item][1],consolidated_BOM[item][3], MSID_or_Consolidated)
    counter += 1
def populateNonMigrationBOM(bomDict):
    table = Quote.QuoteTables["Migration_BOM_Table"]
    counter = 1
    if bomDict:
        row = table.AddNewRow()
        row["Item_GUID"] = ""
        row["Part_Description"] = "Additional Parts"
    for part , partData in bomDict.items():
        row = table.AddNewRow()
        row["Item_Number"] = counter
        row["Part_Number"] = part
        row["Part_Description"] = partData[0]
        row["Qty"] = int(partData[1])
        counter += 1
    table.Save()
def populateCyberBOM(bomDict):
    table = Quote.QuoteTables["Migration_BOM_Table"]
    counter = 1
    if bomDict:
        row = table.AddNewRow()
        row["Item_GUID"] = ""
        row["Part_Description"] = "Cyber Product"
    for part , partData in bomDict.items():
        row = table.AddNewRow()
        row["Item_Number"] = counter
        row["Part_Number"] = part
        row["Part_Description"] = partData[0]
        #row["Product_Type"] = partData[3]
        row["Qty"] = int(partData[1])
        counter += 1
    table.Save()
def populateTraceBOM(bomDict):
    table = Quote.QuoteTables["Migration_BOM_Table"]
    counter = 1
    if bomDict:
        row = table.AddNewRow()
        row["Item_GUID"] = ""
        row["Part_Description"] = "Trace Software"
    for part , partData in bomDict.items():
        row = table.AddNewRow()
        row["Item_Number"] = counter
        row["Part_Number"] = part
        row["Part_Description"] = partData[0]
        #row["Product_Type"] = partData[3]
        row["Qty"] = int(partData[1])
        counter += 1
    table.Save()
def populateNonMigrationBOMConsolidated(bomDict):
    table = Quote.QuoteTables["Migration_BOM_Table"]
    counter = table.Rows.Count
    for part , partData in bomDict.items():
        row = table.AddNewRow()
        row["Item_Number"] = counter
        row["Part_Number"] = part
        row["Part_Description"] = partData[0]
        row["Qty"] = int(partData[1])
        counter += 1
    table.Save()
def populateCyberBomConsolidated(bomDict):
    table = Quote.QuoteTables["Migration_BOM_Table"]
    counter = table.Rows.Count
    for part , partData in bomDict.items():
        row = table.AddNewRow()
        row["Item_Number"] = counter
        row["Part_Number"] = part
        row["Part_Description"] = partData[0]
        row["Qty"] = int(partData[1])
        counter += 1
    table.Save()
def populateTraceBomConsolidated(bomDict):
    table = Quote.QuoteTables["Migration_BOM_Table"]
    counter = table.Rows.Count
    for part , partData in bomDict.items():
        row = table.AddNewRow()
        row["Item_Number"] = counter
        row["Part_Number"] = part
        row["Part_Description"] = partData[0]
        row["Qty"] = int(partData[1])
        counter += 1
    table.Save()
def populateBOMTableConsolidated(bomDict):
    table = Quote.QuoteTables["Migration_BOM_Table"]
    table.Rows.Clear()
    counter = 1
    for part , partData in bomDict.items():
        row = table.AddNewRow()
        row["Item_Number"] = counter
        row["Part_Number"] = part
        row["Part_Description"] = partData[0]
        #row["Product_Type"] = partData[3]
        row["Qty"] = int(partData[1])
        counter += 1
    table.Save()
def populateBOMTable(bomDict , msidList):
    if Quote.GetCustomField("BOM Type").Content == "By MSID":
        populateBOMTableByMsid(bomDict , msidList)
        return
    populateBOMTableConsolidated(bomDict)
def populateNonMigrationBOMTable(bomDict):
    if Quote.GetCustomField("BOM Type").Content == "By MSID":
        populateNonMigrationBOM(bomDict)
        return
    populateNonMigrationBOMConsolidated(bomDict)
def populateCyberBomTable(bomDict):
    if Quote.GetCustomField("BOM Type").Content == "By MSID":
        populateCyberBOM(bomDict)
        return
    populateCyberBomConsolidated(bomDict)
def populateTraceBomTable(bomDict):
    if Quote.GetCustomField("BOM Type").Content == "By MSID":
        populateTraceBOM(bomDict)
        return
    populateTraceBomConsolidated(bomDict)
def getMigrationBomDictConsolidated_old(item):
    bomDict = dict()
    msidList = list()
    msidGuidMap = dict()
    for msid in item.Children:
        msidList.append(msid.QuoteItemGuid)
        for module in msid.Children:
            for part in module.Children:
                if part.PartNumber.startswith('SVC'):
                    continue
                if part.Description == 'CE PLC Control Group' or part.Description == 'UOC Control Group':
                    def temp(part,bomDict):
                        for i in part.Children:
                            if i.Description == 'CE PLC Remote Group' or i.Description == 'UOC Remote Group':
                                temp(i,bomDict)
                                continue
                            partData1 = bomDict.get(i.PartNumber , ["" , 0, ""])
                            partData1[0] = i.Description
                            partData1[1] += i.Quantity
                            partData1[2] = i.ProductTypeName
                            bomDict[i.PartNumber] = partData1
                    temp(part,partDict)
                    continue
                partData = bomDict.get(part.PartNumber , ["" , 0 , ""])
                partData[0] = part.Description
                partData[1] += part.Quantity
                partData[2] = part.ProductTypeName
                bomDict[part.PartNumber] = partData
    return (msidList , bomDict,msidGuidMap)
def getMigrationBomDictByMsid_old(item):
    bomDict = dict()
    msidList = list()
    msidGuidMap = dict()
    for msid in item.Children:
        msidList.append(msid.QuoteItemGuid)
        msidGuidMap[msid.QuoteItemGuid] = msid.PartNumber
        partDict = bomDict.get(msid.QuoteItemGuid , dict())
        for module in msid.Children:
            for part in module.Children:
                if part.PartNumber.startswith('SVC'):
                    continue
                if part.Description == 'CE PLC Control Group' or part.Description == 'UOC Control Group':
                    def temp(part,partDict):
                        for i in part.Children:
                            if i.Description == 'CE PLC Remote Group' or i.Description == 'UOC Remote Group':
                                temp(i,partDict)
                                continue
                            partData1 = partDict.get(i.PartNumber , ["" , 0, ""])
                            partData1[0] = i.Description
                            partData1[1] += i.Quantity
                            partData1[2] = i.ProductTypeName
                            partDict[i.PartNumber] = partData1
                    temp(part,partDict)
                    continue
                partData = partDict.get(part.PartNumber , ["" , 0, ""])
                partData[0] = part.Description
                partData[1] += part.Quantity
                partData[2] = part.ProductTypeName
                partDict[part.PartNumber] = partData
        bomDict[msid.QuoteItemGuid] = partDict
    return (msidList , bomDict,msidGuidMap)
def getPartBomDictByMsid(item,partBomDict):
    if Quote.GetCustomField("BOM Type").Content == "By MSID":
        partDict = partBomDict.get(item["QI_Area"].Value , dict())
        partData = partDict.get(item.PartNumber , ["" , 0, ""])
        partData[0] = item.Description
        partData[1] += item.Quantity
        partData[2] = item.ProductTypeName
        partDict[item.PartNumber] = partData
        partBomDict[item["QI_Area"].Value ] = partDict
    return partBomDict
def getMigrationBomDict(item):
    if Quote.GetCustomField("BOM Type").Content == "By MSID":
        return getMigrationBomDictByMsid(item)
    return getMigrationBomDictConsolidated(item)
def getMigrationBomDict_old(item):
    if Quote.GetCustomField("BOM Type").Content == "By MSID":
        return getMigrationBomDictByMsid_old(item)
    return getMigrationBomDictConsolidated_old(item)
def getHwSWPrice(item):
    total = 0
    services = 0
    for child in filter(lambda x : x.PartNumber != "Project Management" , item.Children):
        total += child.ExtendedAmount
        for childItems in filter(lambda x : x.PartNumber.startswith('SVC') , child.Children):
            services += childItems.ExtendedAmount
    return total - services
def getPMPrice(item):
    for child in filter(lambda x : x.PartNumber == "Project Management" , item.Children):
        return child.ExtendedAmount
    return 0
def getOffSitePrice(item,productDict_off):
    total = 0
    for child in item.Children:
        partDict = productDict_off.get(child.PartNumber)
        if not partDict:
            continue
        for childItem in child.Children:
            if partDict.get(childItem.PartNumber):
                total += childItem.NetPrice * partDict.get(childItem.PartNumber)
                partDict.pop(childItem.PartNumber)
    return total
def getOnSitePrice(item,productDict_on):
    total = 0
    for child in item.Children:
        partDict = productDict_on.get(child.PartNumber)
        if not partDict:
            continue
        for childItem in child.Children:
            if partDict.get(childItem.PartNumber):
                total += childItem.NetPrice * partDict.get(childItem.PartNumber)
                partDict.pop(childItem.PartNumber)
    return total
def getAuditPrice(item):
    total = 0
    attrs = item.SelectedAttributes
    containerNames = {
        "FSC to SM Audit" : "MSID_Labor_FSC_to_SM_audit_Con"
    }
    productDict = dict()
    for partKey , containerName in containerNames.items():
        partDict = dict()
        con = attrs.GetContainerByName(containerName)
        if not con:
            continue
        for row in filter(lambda x: x['Deliverable_Type'] in ['Offsite','Onsite'] , con.Rows):
            partDict[row['FO_Eng']] = round(getFloat(row['Final_Hrs']) * getFloat(row['FO_Eng_Percentage_Split'])/100, 0) + partDict.get(row['FO_Eng'] , 0)
            partDict[row['GES_Eng']] = round(getFloat(row["Final_Hrs"]) * getFloat(row["GES_Eng_Percentage_Split"]) / 100, 0) + partDict.get(row['GES_Eng'] , 0)
        productDict[partKey] = partDict
    for child in item.Children:
        partDict = productDict.get(child.PartNumber)
        if not partDict:
            continue
        for childItem in child.Children:
            if partDict.get(childItem.PartNumber):
                total += childItem.NetPrice * partDict.get(childItem.PartNumber)
                partDict.pop(childItem.PartNumber)
    return total
def getMsidPriceDict(item , laborSeprated = False):
    attrs = item.SelectedAttributes
    containerNames = {
        "OPM" : "MSID_Labor_OPM_Engineering",
        "LCN" : "MSID_Labor_LCN_One_Time_Upgrade_Engineering",
        "EBR" : "MSID_Labor_EBR_Con",
        "EHPM/EHPMX/ C300PM" : "MSID_Labor_EHPM_C300PM_Con",
        "ELCN" : "MSID_Labor_ELCN_Con",
        "Orion Console" : "MSID_Labor_Orion_Console_Con",
        "TCMI" : "MSID_Labor_TCMI_Con",
        "TPS_to_EXP" : "MSID_Labor_TPS_TO_EXPERION_Con",
        "C200_Migration" : "MSID_Labor_C200_Migration_Con",
        "CB_EC_Upgrade_to_C300_UHIO" : "MSID_Labor_CB-EC_Upgrade_to_C300-UHIO_con",
        "FDM Upgrade" : "MSID_Labor_FDM_Upgrade_Con",
        "XP10 Actuator Upgrade" : "MSID_Labor_XP10_Actuator_Upgrade_con",
        "FSC to SM" : "MSID_Labor_FSC_to_SM_con",
        "xPM to C300 Migration" : "MSID_Labor_xPM_to_C300_Migration_Con",
        "LM_ELMM_ControlEdge_PLC" : "MSID_Labor_LM_to_ELMM_Con",
        "Graphics Migration" : "MSID_Labor_Graphics_Migration_con",
        "FSC to SM IO Migration" : "MSID_Labor_FSCtoSM_IO_con",
        "CD Actuator I-F Upgrade" : "MSID_Labor_CD_Actuator_con",
        "Trace Software" : "Trace_Software_Labor_con",
        "QCS RAE Upgrade" : "MSID_Labor_QCS_RAE_Upgrade_con",
        "3rd Party PLC to ControlEdge PLC/UOC" : "3rd_Party_PLC_UOC_Labor",
        "TPA/PMD Migration" : "MSID_Labor_TPA_con","Virtualization System" : "MSID_Labor_Virtualization_con","CWS RAE Upgrade" : "MSID_Labor_CWS_RAE_Upgrade_con"
    }
    productDict_off = dict()
    productDict_on = dict()
    for partKey , containerName in containerNames.items():
        partDict_off = dict()
        partDict_on = dict()
        con = attrs.GetContainerByName(containerName)
        if not con:
            continue
        for row in filter(lambda x: x['Deliverable_Type'] == 'Offsite' , con.Rows):
            partDict_off[row['FO_Eng']] = round(getFloat(row['Final_Hrs']) * getFloat(row['FO_Eng_Percentage_Split'])/100, 0) + partDict.get(row['FO_Eng'] , 0)
            partDict_off[row['GES_Eng']] = round(getFloat(row["Final_Hrs"]) * getFloat(row["GES_Eng_Percentage_Split"]) / 100, 0) + partDict.get(row['GES_Eng'] , 0)
        productDict_off[partKey] = partDict_off
        for row in filter(lambda x: x['Deliverable_Type'] == 'Onsite' , con.Rows):
            partDict_on[row['FO_Eng']] = round(getFloat(row['Final_Hrs']) * getFloat(row['FO_Eng_Percentage_Split'])/100 , 0) + partDict.get(row['FO_Eng'] , 0)
            partDict_on[row['GES_Eng']] = round(getFloat(row["Final_Hrs"]) * getFloat(row["GES_Eng_Percentage_Split"]) / 100 , 0) + partDict.get(row['GES_Eng'] , 0)
        productDict_on[partKey] = partDict_on
    migrationTotal = item.ExtendedAmount
    hwPrice = getHwSWPrice(item)
    offSitePrice = getPMPrice(item) + getOffSitePrice(item,productDict_off)
    onSitePrice =  getOnSitePrice(item,productDict_on)
    auditTotal = getAuditPrice(item)
    diff = migrationTotal - (hwPrice + offSitePrice + onSitePrice + auditTotal)
    if laborSeprated:
        return {
            "DOC_KEY_HWSW" : hwPrice,
            "DOC_KEY_PM_OFF_Site" : offSitePrice,
            "DOC_KEY_ON_Site" : onSitePrice + diff,
            "DOC_KEY_FSC_Audit_Total": auditTotal
        }
    return {
        "DOC_KEY_HWSW" : hwPrice,
        "DOC_KEY_PM_OFF_Site_On_site" : offSitePrice + onSitePrice + diff,
        "DOC_KEY_FSC_Audit_Total": auditTotal
    }
def updateTotal(totalDict , resDict):
    for key , value in resDict.items():
        totalDict[key] = value + totalDict[key]
    return totalDict
def getTotalMsidPriceDict(item  , laborSeprated = False):
    totalDict = {
        "DOC_KEY_HWSW" : 0,
        "DOC_KEY_PM_OFF_Site" :0,
        "DOC_KEY_ON_Site" : 0,
        "DOC_KEY_FSC_Audit_Total":0
    } if laborSeprated else {
        "DOC_KEY_HWSW" : 0,
        "DOC_KEY_PM_OFF_Site_On_site" : 0,
        "DOC_KEY_FSC_Audit_Total":0
    }
    for child in item.Children:
        res = getMsidPriceDict(child , laborSeprated)
        totalDict = updateTotal(totalDict , res)
    return totalDict
def getChildTotalMsidPriceDict(item  , laborSeprated = False):
    totalDict = {
        "DOC_KEY_HWSW" : 0,
        "DOC_KEY_PM_OFF_Site" :0,
        "DOC_KEY_ON_Site" : 0
    } if laborSeprated else {
        "DOC_KEY_HWSW" : 0,
        "DOC_KEY_PM_OFF_Site_On_site" : 0
    }
    res = getMsidPriceDict(item , laborSeprated)
    totalDict = updateTotal(totalDict , res)
    return totalDict
def getPricingData(item):
    pricingDict = dict()
    pricingType = Quote.GetCustomField("Pricing Summary Type").Content
    if pricingType == "By MSID - Labor broken out":
        for msid in item.Children:
            pricingDict[msid.QuoteItemGuid] = getMsidPriceDict(msid , True)
    if pricingType == "By MSID - Labor consolidated":
        for msid in item.Children:
            pricingDict[msid.QuoteItemGuid] = getMsidPriceDict(msid , False)
    if pricingType == "Total - Labor broken out":
        pricingDict[item.QuoteItemGuid] = getTotalMsidPriceDict(item , True)
    if pricingType == "Total - Labor consolidated":
        pricingDict[item.QuoteItemGuid] = getTotalMsidPriceDict(item , False)
    return pricingDict
def getChildPricingData(item, partPricingData):
    area = item["QI_Area"].Value
    pricingType = Quote.GetCustomField("Pricing Summary Type").Content
    laborSeprated = False
    if pricingType == "By MSID - Labor broken out" or pricingType == "Total - Labor broken out":
        laborSeprated = True
    pricingDict = {
        "DOC_KEY_HWSW" : item.ExtendedAmount,
        "DOC_KEY_PM_OFF_Site_On_site" : 0,
        "DOC_KEY_FSC_Audit_Total": 0
    }
    if laborSeprated:
        pricingDict = {
            "DOC_KEY_HWSW" : item.ExtendedAmount,
            "DOC_KEY_PM_OFF_Site" : 0,
            "DOC_KEY_ON_Site" : 0,
            "DOC_KEY_FSC_Audit_Total": 0
        }
    if pricingType == "By MSID - Labor broken out" or pricingType == "By MSID - Labor consolidated":
        if partPricingData.get(area):
            partPricingData[area] = updateTotal(partPricingData[area] , pricingDict)
        else:
            partPricingData[area] = pricingDict
    if pricingType == "Total - Labor broken out" or pricingType == "Total - Labor consolidated":
        if partPricingData:
            partPricingData = updateTotal(partPricingData , pricingDict)
        else:
            partPricingData = pricingDict
    return partPricingData
def removeKeyRow(table , keys):
    s = set(keys)
    for row in table.Rows:
        if row["Attribute"] in s:
            table.DeleteRow(row.Id)
def populatePricingData(dataDict):
    table = Quote.QuoteTables["Migration_Document_Data"]
    removeKeyRow(table , [
        "DOC_KEY_HWSW",
        "DOC_KEY_PM_OFF_Site",
        "DOC_KEY_ON_Site",
        "DOC_KEY_HWSW",
        "DOC_KEY_PM_OFF_Site_On_site",
        "DOC_KEY_Total",
        "DOC_KEY_Total_Add",
        "DOC_KEY_Quote_Total",
        "DOC_KEY_Total_Cyber",
        "DOC_KEY_Total_Mig_Add",
        "DOC_KEY_FSC_Audit_Total"
    ])
    total = 0
    for item in Quote.MainItems:
        data = dataDict.get(item.QuoteItemGuid)
        if data:
            for key , value in data.items():
                row = table.AddNewRow()
                row["MSID_GUID"] = item.QuoteItemGuid
                row["Attribute"] = key
                row["Attribute_Value"] = UserPersonalizationHelper.ToUserFormat(value)
                total += value
    row = table.AddNewRow()
    row["Attribute"] = "DOC_KEY_Total"
    row["Attribute_Value"] = UserPersonalizationHelper.ToUserFormat(total)
    table.Save()
    return total
def getNonMigrationBomDictByMsid(item):
    bomDict = dict()
    msidList = list()
    for msid in item.Children:
        msidList.append(msid.QuoteItemGuid)
        partDict = bomDict.get(msid.QuoteItemGuid , dict())
        for module in msid.Children:
            for part in module.Children:
                if part.PartNumber.startswith('SVC'):
                    continue
                partData = partDict.get(part.PartNumber , ["" , 0, ""])
                partData[0] = part.Description
                partData[1] += part.Quantity
                partData[2] = part.ProductTypeName
                partDict[part.PartNumber] = partData
        bomDict[msid.QuoteItemGuid] = partDict
    return (msidList , bomDict)
def getCyberBomDict(cyberPart):
    bomDict = dict()
    cyberTotal = 0
    for child in cyberPart.Children:
        if not child.PartNumber.startswith('SVC'):
            cyberTotal += child.ExtendedAmount
            partData = bomDict.get(child.PartNumber , ["" , 0, ""])
            partData[0] = child.Description
            partData[1] += child.Quantity
            partData[2] = child.ProductTypeName
            bomDict[child.PartNumber] = partData
    return bomDict, cyberTotal
def getTraceBomDict(tracePart):
    bomDict = dict()
    traceTotal = 0
    for child in tracePart.Children:
        subChild=False 
        for i in child.Children:
            subChild=True
            if not i.PartNumber.startswith('SVC') and not i.PartNumber.startswith('Write-In'):
                traceTotal += child.ExtendedAmount
                partData = bomDict.get(i.PartNumber , ["" , 0,'','',''])
                partData[0] = i.Description
                partData[1] += i.Quantity
                partData[2] = i['QI_PLSG'].Value
                partData[3] = i.Description
                partData[4] = i.ProductTypeName
                bomDict[i.PartNumber] = partData
        if not child.PartNumber.startswith('SVC') and not child.PartNumber.startswith('Write-In')and subChild == False:
            traceTotal += child.ExtendedAmount
            partData = bomDict.get(child.PartNumber , ["" , 0,'','',''])
            partData[0] = child.Description
            partData[1] += child.Quantity
            partData[2] = child['QI_PLSG'].Value
            partData[3] = child.Description
            partData[4] = child.ProductTypeName
            bomDict[child.PartNumber] = partData
    return bomDict, traceTotal
def getMigrationBomDict_loose_parts(item,msidGuidMap):
    bomDict = dict()
    msid_guid = ''
    partDict = bomDict.get(item.QuoteItemGuid , dict())
    partData = partDict.get(item.PartNumber , ["" , 0,'','',''])
    partData[0] = item.Description
    partData[1] += item.Quantity
    partData[2] = item['QI_PLSG'].Value
    partData[3] = item["QI_Area"].Value
    partData[4] = item.ProductTypeName
    partDict[item.PartNumber] = partData
    for key, value in msidGuidMap.items():
        if str(item.QI_Area.Value) == (value+" "):
            msid_guid = key
        if str(item.QI_Area.Value) not in (value+" "):
            msid_guid = item.QuoteItemGuid
    bomDict[msid_guid] = partDict
    return bomDict
def getPricingData_looseitems(item):
    pricingDict = dict()
    pricingType = Quote.GetCustomField("Pricing Summary Type").Content
    if pricingType == "By MSID - Labor broken out":
        pricingDict[item.QI_Area.Value] = getMsidPriceDict(item , True)
    if pricingType == "By MSID - Labor consolidated":
        pricingDict[item.QI_Area.Value] = getMsidPriceDict(item , False)
    if pricingType == "Total - Labor broken out":
        pricingDict[item.QI_Area.Value] = getTotalMsidPriceDict(item , True)
    if pricingType == "Total - Labor consolidated":
        pricingDict[item.QI_Area.Value] = getTotalMsidPriceDict(item , False)
    return pricingDict
nonMigrationBomDict = dict()
migTotal = 0
cyberBomDict = dict()
cyberTotal = 0
traceBomDict = dict()
traceTotal = 0
nonMigrationTotal = 0
partBomDict = dict()
partDict = dict()
msidList = []
bomDict = dict()
migrationPricingData = dict()
migrationPricingData1 = dict()
main_dict = dict()
main_dict_trace= dict()
main_dict_loose = dict()
msidGuidMap	= dict()
msidGuidMap1 = dict()
msidGuidMap3 = dict()
msidGuidMap4 = dict()
loose_bom_dict = dict()
partPricingData = dict()
table_BOM = Quote.QuoteTables["Migration_BOM_Table_Excel"]
table_BOM.Rows.Clear()
for item in Quote.MainItems:
    if item.PartNumber == "Migration":
        if "Migration_New" in item.ProductName:
            msidList , bomDict, msidGuidMap = getMigrationBomDict(item)
            x,y,z = getMsidBOM(item)
        else:
            msidList , bomDict, msidGuidMap = getMigrationBomDict_old(item)
            x,y,z = getMsidBOM_old(item)
        for d in y:
            main_dict[d] = y[d]
        for dd in z:
          msidGuidMap1[dd] = z[dd]
        migrationPricingData = getPricingData(item)
        continue
    if item.PartNumber == "Cyber Products":
        cyberBomDict, cyberTotal = getCyberBomDict(item)
        continue
    if item.PartNumber == "Trace Software" and Quote.GetCustomField('R2Q_Save').Content=='':
        traceBomDict, traceTotal = getTraceBomDict(item)
        main_dict_trace[item.QuoteItemGuid]=traceBomDict
        msidGuidMap3[item.QuoteItemGuid]='Trace Software'
        continue
    if item.PartNumber.startswith('SVC') or '.' in item.RolledUpQuoteItem:
        continue
    if '.' not in item.RolledUpQuoteItem and item["QI_Area"].Value:
        #CXCPQ-50675 & CXCPQ-50539 - Added this vfd condition for populating vfd BOM and Proposal based on area functionality
        vfdquery = SqlHelper.GetFirst("Select VFD_VC_Model from VFD_VC_Models where VFD_VC_Model = '{}'".format(item.PartNumber))
        vfdsparequery = SqlHelper.GetFirst("Select VFD_VC_Model from VFD_VC_Models where VFD_VC_Model = '{}'".format(item.QI_ParentVcModel.Value))
        if vfdquery is not None or vfdsparequery is not None:
            continue
        else:
            partDict = getPartBomDictByMsid(item,partBomDict)
            partPricingData = getChildPricingData(item, partPricingData)
            migrationPricingData.update(getPricingData_looseitems(item))
            loose_bom_dict = getMigrationBomDict_loose_parts(item,msidGuidMap)
            for key,value in loose_bom_dict.items():
                if key in main_dict:
                    main_dict[key].update(value)
                else:
                    main_dict[key] = value

            msidGuidMap4[item.QuoteItemGuid] = item.PartNumber
            msidGuidMap1.update(msidGuidMap4)
            continue
    nonMigrationTotal += item.ExtendedAmount
    partData = nonMigrationBomDict.get(item.PartNumber , ["" , 0,""])
    partData[0] = item.Description
    partData[1] += item.Quantity
    partData[2] = item.ProductTypeName
    nonMigrationBomDict[item.PartNumber] = partData
if partDict:
    for guid ,msid in msidGuidMap.items():
        try:
            partDict[guid] = partDict.pop(msid)
        except:
            pass
if partPricingData and partPricingData.get("DOC_KEY_HWSW", "Not Found") == "Not Found":
    for guid, msid in msidGuidMap.items():
        try:
            partPricingData[guid] = partPricingData.pop(msid)
        except:
            pass
    for guid, priceData in partPricingData.items():
        if migrationPricingData.get(guid):
            msidPriceData = migrationPricingData[guid]
            migrationPricingData[guid] = updateTotal(migrationPricingData[guid], priceData)
else:
    for guid in migrationPricingData.keys():
        migrationPricingData[guid] = updateTotal(migrationPricingData[guid], partPricingData)
populateBOMTable(bomDict, msidList)
migTotal = populatePricingData(migrationPricingData)
Delete_Quote_Item(Quote)
x = RestClient.SerializeToJson(nonMigrationBomDict)
y = RestClient.SerializeToJson(cyberBomDict)
z = RestClient.SerializeToJson(traceBomDict)
populateCyberBomTable(cyberBomDict)
populateTraceBomTable(traceBomDict)
populateNonMigrationBOMTable(nonMigrationBomDict)
populateQuoteTableBOMExcel(table_BOM, main_dict,msidGuidMap1,0)
consolidated_BOM = getMigrationConsolidatedBom(main_dict)
populateQuoteTableConsolidatedBOMExcel(table_BOM, consolidated_BOM,1)
populateQuoteTableBOMExcel(table_BOM,main_dict_trace,msidGuidMap3,0)
consolidated_BOM_trace = getMigrationConsolidatedBom(main_dict_trace)
populateQuoteTableConsolidatedBOMExcel(table_BOM, consolidated_BOM_trace,1)
table = Quote.QuoteTables["Migration_Document_Data"]
row = table.AddNewRow()
row["Attribute"] = "DOC_KEY_Total_Add"
row["Attribute_Value"] = UserPersonalizationHelper.ToUserFormat(nonMigrationTotal)
row = table.AddNewRow()
row["Attribute"] = "DOC_KEY_Total_Cyber"
row["Attribute_Value"] = UserPersonalizationHelper.ToUserFormat(cyberTotal)
row = table.AddNewRow()
row["Attribute"] = "DOC_KEY_Total_Mig_Add"
row["Attribute_Value"] = UserPersonalizationHelper.ToUserFormat(nonMigrationTotal + migTotal)
table.Save()
if  Quote.GetCustomField("Booking LOB").Content == 'PMC':
    table = Quote.QuoteTables['Document_Table']
    table.Rows.Clear()
    query = "select * from DOCUMENT_TOBE_OMIT_PARTS where Filter = 'dummy'"
    res = SqlHelper.GetList(query)
    dummyParts = [r.parts for r in res]
    spareParts = []
    materials = []
    services = []
    totals = {
        "TotalBaseMaterial": [0 , 0],"TotalBaseService": [0 , 0],"TotalBaseSpare": [0 , 0],"TotalOptionalMaterial": [0 , 0],"TotalOptionalService": [0 , 0],"TotalOptionalSpare": [0 , 0],"SurchargeBaseMaterial": [0 , 0],"SurchargeBaseSpare": [0 , 0],"SurchargeOptionalMaterial": [0 , 0],"SurchargeOptionalSpare": [0 , 0]
    }
    for item in Quote.Items:
        if item.PartNumber in dummyParts:
            continue
        if item.PartNumber[:3] == 'SVC':
            services.append(item)
            continue
        if item['QI_SparePartsFlag'].Value == "Spare Part":
            spareParts.append(item)
            continue
        materials.append(item)
    itemNumbers = {
        'base' : 1,'optional' : 1,'all' : 1
    }
    for item in materials:
        row = table.AddNewRow()
        FlagValue = False
        quuery = SqlHelper.GetFirst("Select Family_Code FROM PMC_GASETO_YSPEC_MARINE_PRODUCTS WHERE PartNumber = '{}'".format(item.PartNumber))
        if quuery is not None:
            if quuery.Family_Code is not None:
                if quuery.Family_Code == 'Gas Products':
                    FlagValue = True
        if item.IsOptional:
            populateRow(row , item , '{}'.format(itemNumbers['optional']) , 'Material' , 'Optional')
            if FlagValue == True:
                totals['TotalOptionalMaterial'][0] += item.QI_NetPrice_With_ETO.Value
            else:
                totals['TotalOptionalMaterial'][0] += item.ExtendedAmount
            totals['TotalOptionalMaterial'][1] += item.ExtendedListPrice
            totals['SurchargeOptionalMaterial'][0] += item['QI_Tariff_Amount'].Value if item['QI_Tariff_Amount'] else 0.00
            totals['SurchargeOptionalMaterial'][1] += item['QI_Sell_Price_Inc_Tariff'].Value if item['QI_Sell_Price_Inc_Tariff'] else 0.00
            itemNumbers['optional'] += 1
        else:
            populateRow(row , item , '{}'.format(itemNumbers['base']) , 'Material' , 'Base')
            if FlagValue == True:
                totals['TotalBaseMaterial'][0] += item.QI_NetPrice_With_ETO.Value
            else:
                totals['TotalBaseMaterial'][0] += item.ExtendedAmount
            totals['TotalBaseMaterial'][1] += item.ExtendedListPrice
            totals['SurchargeBaseMaterial'][0] += item['QI_Tariff_Amount'].Value if item['QI_Tariff_Amount'] else 0.00
            totals['SurchargeBaseMaterial'][1] += item['QI_Sell_Price_Inc_Tariff'].Value if item['QI_Sell_Price_Inc_Tariff'] else 0.00
            itemNumbers['base'] += 1
    itemNumbers = {
        'base' : 1,'optional' : 1,'all' : 1
    }
    for item in spareParts:
        row = table.AddNewRow()
        if item.IsOptional:
            populateRow(row , item , 'SP{}'.format(itemNumbers['optional']) , 'Spare Part' , 'Optional')
            totals['TotalOptionalSpare'][0] += item.ExtendedAmount
            totals['TotalOptionalSpare'][1] += item.ExtendedListPrice
            totals['SurchargeOptionalSpare'][0] += item['QI_Tariff_Amount'].Value if item['QI_Tariff_Amount'] else 0.00
            totals['SurchargeOptionalSpare'][1] += item['QI_Sell_Price_Inc_Tariff'].Value if item['QI_Sell_Price_Inc_Tariff'] else 0.00
            itemNumbers['optional'] += 1
        else:
            populateRow(row , item , 'SP{}'.format(itemNumbers['base']) , 'Spare Part' , 'Base')
            totals['TotalBaseSpare'][0] += item.ExtendedAmount
            totals['TotalBaseSpare'][1] += item.ExtendedListPrice
            totals['SurchargeBaseSpare'][0] += item['QI_Tariff_Amount'].Value if item['QI_Tariff_Amount'] else 0.00
            totals['SurchargeBaseSpare'][1] += item['QI_Sell_Price_Inc_Tariff'].Value if item['QI_Sell_Price_Inc_Tariff'] else 0.00
            itemNumbers['base'] += 1
    itemNumbers = {
        'base' : 1,'optional' : 1,'all' : 1
    }
    for item in services:
        row = table.AddNewRow()
        if item.IsOptional:
            populateRow(row , item , 'S{}'.format(itemNumbers['optional']) , 'Service' , 'Optional')
            totals['TotalOptionalService'][0] += item.ExtendedAmount
            totals['TotalOptionalService'][1] += item.ExtendedListPrice
            itemNumbers['optional'] += 1
        else:
            populateRow(row , item , 'S{}'.format(itemNumbers['base']) , 'Service' , 'Base')
            totals['TotalBaseService'][0] += item.ExtendedAmount
            totals['TotalBaseService'][1] += item.ExtendedListPrice
            itemNumbers['base'] += 1
    for key , value in totals.items():
        row = table.AddNewRow()
        if key in ["SurchargeBaseSpare","SurchargeBaseMaterial","SurchargeOptionalMaterial","SurchargeOptionalSpare"]:
            row['Surcharge_Price'] = value[0]
            row['Total_Sell_Price'] = value[1]
            row['Item_Type'] = key
        else:
            row['Total_Price'] = value[0]
            row['List_Price'] = value[1]
            row['Item_Type'] = key
    row = table.AddNewRow()
    row['Total_Price'] = totals['TotalBaseService'][0] + totals['TotalBaseMaterial'][0] + totals['TotalBaseSpare'][0]
    row['List_Price'] = totals['TotalBaseService'][1] + totals['TotalBaseMaterial'][1] + totals['TotalBaseSpare'][1]
    row['Item_Type'] = 'TotalBase'
    row = table.AddNewRow()
    row['Total_Price'] = totals['TotalOptionalService'][0] + totals['TotalOptionalSpare'][0] + totals['TotalOptionalMaterial'][0]
    row['List_Price'] = totals['TotalOptionalService'][1] + totals['TotalOptionalSpare'][1] + totals['TotalOptionalMaterial'][1]
    row['Item_Type'] = 'TotalOptional'
    row = table.AddNewRow()
    row['Surcharge_Price'] = totals['SurchargeBaseMaterial'][0] + totals['SurchargeBaseSpare'][0]
    row['Total_Sell_Price'] = totals['SurchargeBaseMaterial'][1] + totals['SurchargeBaseSpare'][1] + totals['TotalBaseService'][0]
    row['Item_Type'] = 'TotalBaseTariff'
    row = table.AddNewRow()
    row['Surcharge_Price'] = totals['SurchargeOptionalSpare'][0] + totals['SurchargeOptionalMaterial'][0]
    row['Total_Sell_Price'] = totals['SurchargeOptionalMaterial'][1] + totals['SurchargeOptionalSpare'][1] + totals['TotalOptionalService'][0]
    row['Item_Type'] = 'TotalOptionalTariff'
    table.Save()
if  Quote.GetCustomField("Booking LOB").Content == 'PMC':
    rowDictionary = dict()
    toBeDeletedRows = []
    vcModelTable = Quote.QuoteTables['VCModelConfiguration']
    for row in vcModelTable.Rows:
        rowList = rowDictionary.get(row['CartItemGUID'] , list())
        rowList.append(row)
        rowDictionary[row['CartItemGUID']] = rowList

    vcModelTable.Rows.Clear()
    for item in filter(lambda x : x.QI_FME.Value and True,Quote.Items):
        rowList = rowDictionary.get(item.QuoteItemGuid , list())
        for row in rowList:
            populateNewRow(vcModelTable , row , item.RolledUpQuoteItem)
    vcModelTable.Save()