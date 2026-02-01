def getFloat(Var):
    return float(Var) if Var else 0

def getCFValue(CFName):
    return Quote.GetCustomField(CFName).Content

def replacekeys(data_dict):
    keys_to_replace = ['FDM Upgrade 1', 'FDM Upgrade 2', 'FDM Upgrade 3']
    if 'FDM Upgrade 1' in data_dict or 'FDM Upgrade 2' in data_dict or 'FDM Upgrade ' in data_dict:
        for key in keys_to_replace:
            if key in data_dict:
                if 'FDM Upgrade' in data_dict:
                    data_dict['FDM Upgrade'].update(data_dict.pop(key))
                else:
                    data_dict['FDM Upgrade'] = data_dict.pop(key)
    key_mapping = {'C200_Migration': 'C200 Migration','Virtualization System': 'Virtualization System Migration','TPS_to_EXP': 'TPS to Experion','LCN': 'LCN One Time Upgrade','LM_ELMM_ControlEdge_PLC': 'LM to ELMM ControlEdge PLC','CB_EC_Upgrade_to_C300_UHIO': 'CB-EC Upgrade to C300-UHIO','EHPM_HART_IO': 'EHPM HART IO'}
    for old_key, new_key in key_mapping.items():
        if old_key in data_dict:
            data_dict[new_key] = data_dict.pop(old_key)
    return data_dict

def addValues(totalDict , partNumber,key, value):
    partDict = totalDict.get(partNumber,dict())
    partDict[key] = getFloat(partDict.get(key , 0)) + getFloat(value)
    totalDict[partNumber] = partDict

def getExecutionCountry():
    #marketCode = Quote.SelectedMarket.MarketCode
    #salesOrg = marketCode.partition('_')[0]
    salesOrg = Quote.GetCustomField('Sales Area').Content
    query = SqlHelper.GetFirst("select Execution_County from EXECUTION_COUNTRY_SALES_ORG_MAPPING where Execution_Country_Sales_Org = '{}'".format(salesOrg))
    return query.Execution_County if query else None

def getSelectedProducts(item):
    selectedProducts = next((attr.Values[0].Display.split('<br>') for attr in item.SelectedAttributes
         if attr.Name == "MSID_Selected_Products"), [])
    if "Project Management" not in selectedProducts:
        selectedProducts.append("Project Management")
    if any(upgrade in selectedProducts for upgrade in ['FDM Upgrade 1', 'FDM Upgrade 2', 'FDM Upgrade 3']):
        selectedProducts.append('FDM Upgrade')
    if "FSC to SM" in selectedProducts:
        selectedProducts.append('FSC to SM Audit')
    if "FSC to SM IO Migration" in selectedProducts:
        selectedProducts.append('FSC to SM IO Audit')
    return selectedProducts


def getItemData():
    itemDataDict = dict()
    for item in Quote.MainItems:
        if item.PartNumber == "Migration":
            for msid in item.Children:
                msidData = itemDataDict.get(msid.PartNumber,dict())
                for module in msid.Children:
                    partData = msidData.get(module.PartNumber,dict())
                    for part in module.Children:
                        if part.ProductTypeName.lower() == "honeywell labor":
                            partData[part.PartNumber] = part.NetPrice
                    msidData[module.PartNumber] = partData
                itemDataDict[msid.PartNumber] = msidData
                keys_to_replace = ['FDM Upgrade 1', 'FDM Upgrade 2', 'FDM Upgrade 3', 'C200_Migration','Virtualization System','TPS_to_EXP','LCN','LM_ELMM_ControlEdge_PLC','CB_EC_Upgrade_to_C300_UHIO']
                keys = itemDataDict[msid.PartNumber].keys()
                itemDataDict[msid.PartNumber] = replacekeys(itemDataDict[msid.PartNumber]) if len(list(filter(lambda key: key in keys, keys_to_replace))) > 0 else itemDataDict[msid.PartNumber]
        if item.PartNumber in ("CYBER","HCI_Labor_config"):
            msidData = itemDataDict.get(item.PartNumber+'-'+item.QuoteItemGuid,dict())
            for module in item.Children:
                partData = msidData.get(module.PartNumber,dict())
                for part in module.Children:
                    if part.ProductTypeName.lower() == "honeywell labor":
                        partData[part.PartNumber] = part.NetPrice
                msidData[module.PartNumber] = partData
            itemDataDict[item.PartNumber] = msidData
        if item.PartNumber == "HCI_LABOR":
            msidData = itemDataDict.get(item.PartNumber+'-'+item.QuoteItemGuid,dict())
            for module in item.Children:
                if module.ProductTypeName.lower() == "honeywell labor":
                    msidData[module.PartNumber] = module.NetPrice
            itemDataDict[item.ProductName] = msidData
    #Trace.Write("itemDataDict = " + str(keys))
    return itemDataDict

def getSellPriceData(laboHours,item):
    sellPriceDict = dict()
    if item.PartNumber in ("PHD_Labor","AFM_Labor","Uniformance_Insight_Labor"):
        itemSellPriceData = itemData['HCI_Labor_config']
    elif item.PartNumber == "HCI_LABOR":
        itemSellPriceData = itemData
    else:
        itemSellPriceData = itemData.get(item.PartNumber,'')
                                                                                                                         
    for key,value in laboHours.items():
        sellPrice = 0
        for key1,value1 in value.items():
            if itemSellPriceData:
                if key1 in ('Generic System 1','Generic System 2','Generic System 3','Generic System 4','Generic System 5'):
                    key1 = 'Generic System Migration'
                moduleLevelData = itemSellPriceData.get(key1,'')
                if moduleLevelData:
                    for part,hours in value1.items():
                        sellPrice += getFloat(hours) * getFloat(moduleLevelData.get(part,0))
        #Trace.Write(sellPrice)
        sellPriceDict[key] = round(getFloat(sellPrice), 2)
    #Trace.Write("sellPriceDict = " + str(sellPriceDict))
    #Trace.Write(str(sellPriceDict))
    return sellPriceDict

def populateLaborTypeTable1(labotTypeTable,item,laborTypeDict,sellPriceDict):
    addRow = labotTypeTable.AddNewRow()
    addRow["Labor_Type"] = "Total"
    addRow["MSID"] = item.PartNumber
    addRow["Quote_Item_GuId"] = item.QuoteItemGuid
    addRow["IsHeader"] = "No"
    for laborType in laborTypes:
        addRow = labotTypeTable.AddNewRow()
        addRow["Labor_Type"] = laborType
        addRow["IsHeader"] = "No"
        typeData = laborTypeDict.get(laborType,'')
        if typeData:
            addRow["Hours"] = typeData.get("Hours",0)
            addRow["Total_Cost"] = round(typeData.get("Total Cost",0), 2)
            addRow["Total_Sell_Price"] = sellPriceDict.get(laborType,0)
            addRow["Quote_Item_GuId"] = item.QuoteItemGuid

def populateLaborTypeTable2(labotTypeTable,laborTypeTableData):
    addRow = labotTypeTable.AddNewRow()
    addRow["Labor_Type"] = "Total"
    addRow["IsHeader"] = "Yes"
    for laborType in laborTypes:
        addRow = labotTypeTable.AddNewRow()
        addRow["Labor_Type"] = laborType
        addRow["IsHeader"] = "Yes"
        typeData = laborTypeTableData.get(laborType,'')
        if typeData:
            addRow["Hours"] = typeData.get("Hours",0)
            addRow["Total_Cost"] = typeData.get("Total_Cost",0)
            addRow["Total_Sell_Price"] = typeData.get("Total_Sell_Price",0)

def calculateTotals(labotTypeTable,item):
    if labotTypeTable.Rows.Count > 0:
        totalHours = 0
        totalcost = 0
        totalSellPrice = 0
        for row in labotTypeTable.Rows:
            if row["Quote_Item_GuId"] == item.QuoteItemGuid:
                totalHours += getFloat(row["Hours"])
                totalcost += getFloat(row["Total_Cost"])
                totalSellPrice += getFloat(row["Total_Sell_Price"])
        for row in labotTypeTable.Rows:
            if row["Quote_Item_GuId"] == item.QuoteItemGuid:
                if row["Labor_Type"] == "Total":
                    row["Hours"] = totalHours
                    row["Total_Cost"] = totalcost
                    row["Total_Sell_Price"] = totalSellPrice
                else:
                    row["Percentage"] = str(round((getFloat(row["Hours"]) / totalHours) * 100,1)) if  totalHours > 0 else 0

def getFinalHours(container,product):
    for row in container.Rows:
        if row["Deliverable"] not in ('Off-Site','On-Site','Total'):
            if row["Execution_Country"] == excecutionCountry and row["Final_Hrs"] not in ('',"0") and row["FO_Eng"] != '' and row["FO_Eng_Percentage_Split"] != '0':
                addValues(laborTypeDict,"Front Office Labor","Hours",round(getFloat(row["Final_Hrs"]) * getFloat(row["FO_Eng_Percentage_Split"]) / 100))
                addValues(laborTypeDict,"Front Office Labor","Total Cost",round(getFloat(row["Regional_Cost"])))
                addValues(laboHours["Front Office Labor"], product, row["FO_Eng"],round(getFloat(row["Final_Hrs"]) * getFloat(row["FO_Eng_Percentage_Split"]) / 100))
            elif row["Final_Hrs"] not in ('',"0") and row["FO_Eng"] != '' and row["FO_Eng_Percentage_Split"] != '0':
                addValues(laborTypeDict,"Intercompany Labor","Hours", round(getFloat(row["Final_Hrs"]) * getFloat(row["FO_Eng_Percentage_Split"]) / 100))
                addValues(laborTypeDict,"Intercompany Labor", "Total Cost",round(getFloat(row["Regional_Cost"])))
                addValues(laboHours["Intercompany Labor"], product, row["FO_Eng"],round(getFloat(row["Final_Hrs"]) * getFloat(row["FO_Eng_Percentage_Split"]) / 100))
            if row["Final_Hrs"] not in ('',"0") and row["GES_Eng"] != '' and row["GES_Eng_Percentage_Split"] != '0':
                if row["GES_Eng"] in ('SVC_GES_P350B_IN','SVC_GES_P350B_CN','SVC_GES_P350B_RO','SVC_GES_P350B_UZ','SVC_GES_P335B_IN','SVC_GES_P335B_CN','SVC_GES_P335B_RO','SVC_GES_P335B_UZ','SVC_GES_P215B_IN','SVC_GES_P215B_CN','SVC_GES_P215B_RO','SVC_GES_P215B_UZ','SVC_GES_PLCB_IN','SVC_GES_PLCB_CN','SVC_GES_PLCB_RO','SVC_GES_PLCB_UZ','SVC_GES_P350B_EG','SVC_GES_P335B_EG','SVC_GES_PLCB_EG','SVC_GES_P215B_EG'):
                    addValues(laborTypeDict,"GES Back -office Labor","Hours", round(getFloat(row["Final_Hrs"]) * getFloat(row["GES_Eng_Percentage_Split"]) / 100))
                    addValues(laborTypeDict,"GES Back -office Labor", "Total Cost",round(getFloat(row["GES_Regional_Cost"])))
                    addValues(laboHours["GES Back -office Labor"], product, row["GES_Eng"],round(getFloat(row["Final_Hrs"]) * getFloat(row["GES_Eng_Percentage_Split"]) / 100))
                else:
                    addValues(laborTypeDict,"GES On-site Labor","Hours", round(getFloat(row["Final_Hrs"]) * getFloat(row["GES_Eng_Percentage_Split"]) / 100))
                    addValues(laborTypeDict,"GES On-site Labor", "Total Cost",round(getFloat(row["GES_Regional_Cost"])))
                    addValues(laboHours["GES On-site Labor"], product, row["GES_Eng"],round(getFloat(row["Final_Hrs"]) * getFloat(row["GES_Eng_Percentage_Split"]) / 100))

def getFinalHours_hci(container,partnumber):
    for row in container.Rows:
        if partnumber in ("PHD_Labor","AFM_Labor","Uniformance_Insight_Labor"): #product=="PHD Labor": # and row.IsSelected:
            if row["Eng"] and "GES" not in row["Eng"] and row["Execution Country"] == excecutionCountry and row["Final Hrs"] not in ('',"0.0"): # and row["Eng Total WTW Cost"] not in ('',"0.0"):
                #Trace.Write(str(row["Deliverable"])+"-->"+str(row["Execution Country"])+"--check---222--"+str(excecutionCountry)+"-->"+str(row["Calculated Hrs"]))
                part_number=SqlHelper.GetFirst("select Service_Material from CT_HCI_PHD_LABORMATERIAL where Labor='{}'".format(row["Eng"])).Service_Material
                addValues(laborTypeDict,"Front Office Labor","Hours",float(row["Final Hrs"]))
                addValues(laborTypeDict,"Front Office Labor","Total Cost",round(getFloat(row["Eng Total Regional Cost"]), 2)) # Eng Total Regional Cost, Eng Unit Regional Cost
                addValues(laboHours["Front Office Labor"],partnumber,part_number,float(row["Final Hrs"]))
            elif row["Eng"] and "GES" not in row["Eng"] and row["Execution Country"] != excecutionCountry and row["Final Hrs"] not in ('',"0.0"): # and row["Eng Total WTW Cost"] not in ('',"0.0"):
                #Trace.Write(str(row["Eng"])+"--->"+str(row["Deliverable"])+"-->"+str(row["Execution Country"])+"--check---333--"+str(excecutionCountry)+"-->"+str(row["Calculated Hrs"])+"-->"+str(row["Eng Total Regional Cost"]))
                part_number=SqlHelper.GetFirst("select Service_Material from CT_HCI_PHD_LABORMATERIAL where Labor='{}'".format(row["Eng"])).Service_Material
                addValues(laborTypeDict,"Intercompany Labor", "Hours",float(row["Final Hrs"]))
                addValues(laborTypeDict,"Intercompany Labor", "Total Cost",round(getFloat(row["Eng Total Regional Cost"]), 2))
                addValues(laboHours["Intercompany Labor"],partnumber,part_number,float(row["Final Hrs"]))
            if row["Eng"] and "GES" in row["Eng"] and row["Final Hrs"] not in ('',"0.0"): # and row["Eng Total Regional Cost"] not in ('',"0.0"):
                #Trace.Write(str(row["Eng"])+"-->"+str(row["Execution Country"])+"--check---111--"+str(excecutionCountry)+"-->"+str(row["Calculated Hrs"]))
                part_number=SqlHelper.GetFirst("select Service_Material from CT_HCI_PHD_LABORMATERIAL where Labor='{}'".format(row["Eng"])).Service_Material
                addValues(laborTypeDict,"GES Back -office Labor", "Hours",float(row["Final Hrs"]))
                addValues(laborTypeDict,"GES Back -office Labor", "Total Cost",round(getFloat(row["Eng Total Regional Cost"]), 2))
                addValues(laboHours["GES Back -office Labor"],partnumber,part_number,float(row["Final Hrs"]))

if getCFValue("Quote Type") == "Projects" and (getCFValue("Booking LOB") == "LSS" or getCFValue("Booking LOB") == "PAS" or getCFValue("Booking LOB") == "PMC") or getCFValue("cyberProductPresent") == "Yes" or getCFValue("Booking LOB") == "HCP":
    excecutionCountry = getExecutionCountry()
    laborTypes = ['Front Office Labor','Intercompany Labor','GES Back -office Labor','GES On-site Labor']
    labotTypeTable = Quote.QuoteTables["Labor_Type_Table_Excel"]
    labotTypeTable.Rows.Clear()
    itemData = getItemData()
    ct=0
    for item in Quote.MainItems:
        ct=ct+1
        if item.ProductName in ("MSID_New","MSID") :
            laborTypeDict = dict()
            laboHours = dict()
            laboHours["Front Office Labor"] = dict()
            laboHours["Intercompany Labor"] = dict()
            laboHours["GES Back -office Labor"] = dict()
            laboHours["GES On-site Labor"] = dict()
            selectedProducts = getSelectedProducts(item)
            Trace.Write(str(selectedProducts))
            product_containers = {"EBR": "MSID_Labor_EBR_Con", "ELCN": "MSID_Labor_ELCN_Con", "Orion Console": "MSID_Labor_Orion_Console_Con", "EHPM/EHPMX/ C300PM": "MSID_Labor_EHPM_C300PM_Con", "TPS to Experion": "MSID_Labor_TPS_TO_EXPERION_Con", "TCMI": "MSID_Labor_TCMI_Con", "C200 Migration": "MSID_Labor_C200_Migration_Con", "CB-EC Upgrade to C300-UHIO": "MSID_Labor_CB-EC_Upgrade_to_C300-UHIO_con", "FSC to SM": "MSID_Labor_FSC_to_SM_con", "FSC to SM Audit": "MSID_Labor_FSC_to_SM_audit_Con", "xPM to C300 Migration": "MSID_Labor_xPM_to_C300_Migration_Con", "LM to ELMM ControlEdge PLC": "MSID_Labor_LM_to_ELMM_Con", "EHPM HART IO": "MSID_Labor_EHPM_HART_IO_Con", "XP10 Actuator Upgrade": "MSID_Labor_XP10_Actuator_Upgrade_con", "Graphics Migration": "MSID_Labor_Graphics_Migration_con", "CD Actuator I-F Upgrade": "MSID_Labor_CD_Actuator_con", "FSC to SM IO Migration": "MSID_Labor_FSCtoSM_IO_con", "FSC to SM IO Audit": "MSID_Labor_FSC_to_SM_IO_Audit_Con", "3rd Party PLC to ControlEdge PLC/UOC": "3rd_Party_PLC_UOC_Labor","OPM": "MSID_Labor_OPM_Engineering", "LCN One Time Upgrade": "MSID_Labor_LCN_One_Time_Upgrade_Engineering", "CWS RAE Upgrade": "MSID_Labor_CWS_RAE_Upgrade_con", "Virtualization System Migration": "MSID_Labor_Virtualization_con", "Generic System 1": "MSID_Labor_Generic_System1_Cont", "Generic System 2": "MSID_Labor_Generic_System2_Cont", "Generic System 3": "MSID_Labor_Generic_System3_Cont", "Generic System 4": "MSID_Labor_Generic_System4_Cont", "Generic System 5": "MSID_Labor_Generic_System5_Cont", "QCS RAE Upgrade": "MSID_Labor_QCS_RAE_Upgrade_con", "TPA/PMD Migration": "MSID_Labor_TPA_con", "ELEPIU ControlEdge RTU Migration Engineering": "MSID_Labor_ELEPIU_con","FDM Upgrade":"MSID_Labor_FDM_Upgrade_Con","Project Management":"MSID_Labor_Project_Management","Trace Software":"Trace_Software_Labor_con"}
            for product in selectedProducts:
                    container = item.SelectedAttributes.GetContainerByName(product_containers.get(product))
                    if container:
                        getFinalHours(container, product)
            #Trace.Write("laboHours = " + str(laboHours))
            #Trace.Write(str(laborTypeDict))
            sellPriceDict = getSellPriceData(laboHours,item)
            populateLaborTypeTable1(labotTypeTable,item,laborTypeDict,sellPriceDict)
            calculateTotals(labotTypeTable,item)
        if item.ProductName == "Trace Software" and Quote.GetCustomField('R2Q_Save').Content=='' and item.ParentItemGuid =='':
            laborTypeDict = dict()
            laboHours = dict()
            laboHours["Front Office Labor"] = dict()
            laboHours["Intercompany Labor"] = dict()
            laboHours["GES Back -office Labor"] = dict()
            laboHours["GES On-site Labor"] = dict()
            tsCon = item.SelectedAttributes.GetContainerByName("Trace_Software_Labor_con")
            pmCon = item.SelectedAttributes.GetContainerByName("Trace_Project_Management_Labor_con")
            getFinalHours(tsCon,"Trace Software") if tsCon else 0
            getFinalHours(pmCon,"Project Management") if pmCon else 0
            sellPriceDict = getSellPriceData(laboHours,item)
            populateLaborTypeTable1(labotTypeTable,item,laborTypeDict,sellPriceDict)
            calculateTotals(labotTypeTable,item)
        if Quote.GetCustomField('R2Q_Save').Content == 'Submit' and ct and item.ProductName =="HCI Labor Config":
            Quote.GetItemByQuoteItem(ct).AsMainItem.Reconfigure()
        if item.ProductName in ("PHD Labor","AFM Labor","Uniformance Insight Labor"): #HCI Labor Config
            #Trace.Write("--PHD Labor---->"+str(dir(item.SelectedAttributes.GetContainerByName)))
            Con = item.SelectedAttributes.GetContainerByName("HCI_PHD_EngineeringLabour")
            if Con is None and Quote.GetCustomField('R2Q_Save').Content == 'Submit':
				Quote.GetItemByQuoteItem(ct).AsMainItem.Reconfigure()
            laborTypeDict = dict()
            laboHours = dict()
            laboHours["Front Office Labor"] = dict()
            laboHours["Intercompany Labor"] = dict()
            laboHours["GES Back -office Labor"] = dict()
            laboHours["GES On-site Labor"] = dict()
            elCon = item.SelectedAttributes.GetContainerByName("HCI_PHD_EngineeringLabour")
            pmCon2 = item.SelectedAttributes.GetContainerByName("HCI_PHD_ProjectManagement2")
            pmCon = item.SelectedAttributes.GetContainerByName("HCI_PHD_ProjectManagement")
            adCon = item.SelectedAttributes.GetContainerByName("HCI_PHD_AdditionalDeliverables")
            getFinalHours_hci(elCon,item.PartNumber) if elCon else 0
            getFinalHours_hci(pmCon2,item.PartNumber) if pmCon2 else 0
            getFinalHours_hci(pmCon,item.PartNumber) if pmCon else 0
            getFinalHours_hci(adCon,item.PartNumber) if adCon else 0
            sellPriceDict = getSellPriceData(laboHours,item)
            populateLaborTypeTable1(labotTypeTable,item,laborTypeDict,sellPriceDict)
            calculateTotals(labotTypeTable,item)
        if item.ProductName == "HCI Labor Upload":
            #Trace.Write("--PHD Labor---->"+str(dir(item.SelectedAttributes.GetContainerByName)))
            laborTypeDict = dict()
            laboHours = dict()
            laboHours["Front Office Labor"] = dict()
            laboHours["Intercompany Labor"] = dict()
            laboHours["GES Back -office Labor"] = dict()
            laboHours["GES On-site Labor"] = dict()
            laborCon = item.SelectedAttributes.GetContainerByName("AR_HCI_LABOR_CONTAINER")
            if laborCon:
                for row in laborCon.Rows:
                    #Trace.Write("---laborCon---000---"+str(row["ExecutionCountry"]))
                    if row["LaborResource"] and "GES" not in row["LaborResource"] and row["ExecutionCountry"] == excecutionCountry and row["FinalHours"] not in ('',"0.0"): #and row["TransferCost"]:
                        #Trace.Write(str(row["LaborResource"])+"---laborCon---111---"+str(row["ExecutionCountry"])+"-->"+str(row["FinalHours"])) # W2WCost
                        addValues(laborTypeDict,"Front Office Labor","Hours",float(row["FinalHours"]))
                        addValues(laborTypeDict,"Front Office Labor","Total Cost",float(row["FinalHours"]) * getFloat(row["TransferCost"]))
                        addValues(laboHours["Front Office Labor"],item.ProductName,row["LaborResource"],float(row["FinalHours"]))
                    elif row["LaborResource"] and "GES" not in row["LaborResource"] and row["ExecutionCountry"] != excecutionCountry and row["FinalHours"] not in ('',"0.0"): #and row["TransferCost"]:
                        addValues(laborTypeDict,"Intercompany Labor","Hours",float(row["FinalHours"]))
                        addValues(laborTypeDict,"Intercompany Labor","Total Cost",float(row["FinalHours"]) * getFloat(row["TransferCost"]))
                        addValues(laboHours["Intercompany Labor"],item.ProductName,row["LaborResource"],float(row["FinalHours"]))
                    if row["LaborResource"] and "GES" in row["LaborResource"] and row["FinalHours"] not in ('',"0.0"): #and row["TransferCost"]:
                        addValues(laborTypeDict,"GES Back -office Labor","Hours",float(row["FinalHours"]))
                        addValues(laborTypeDict,"GES Back -office Labor","Total Cost",float(row["FinalHours"]) * getFloat(row["TransferCost"]))
                        addValues(laboHours["GES Back -office Labor"],item.ProductName,row["LaborResource"],float(row["FinalHours"]))
            sellPriceDict = getSellPriceData(laboHours,item)
            populateLaborTypeTable1(labotTypeTable,item,laborTypeDict,sellPriceDict)
            calculateTotals(labotTypeTable,item)
        if item.ProductName == "Cyber" :
            laborTypeDict = dict()
            laboHours = dict()
            laboHours["Front Office Labor"] = dict()
            laboHours["Intercompany Labor"] = dict()
            laboHours["GES Back -office Labor"] = dict()
            laboHours["GES On-site Labor"] = dict()
            conNames = {
                "Cyber Generic System":"Generic_System_Activities",
                "SMX": "AR_SMX_Activities",
                "ASSESSMENT": "AR_Assessment_Activities",
                "PCN": "AR_PCNH_Activities",
                "MSS": "AR_MSS_Activities",
                "CYBER_APP_CNTRL": "AR_CAC_Activities",
                "Project Management": "Cyber_Labor_Project_Management"
                }
            for key, conName in conNames.items():
                con = item.SelectedAttributes.GetContainerByName(conName)
                if not con:
                    continue
                for row in con.Rows:
                    if key != 'Project Management':
                        cost = getFloat(row["Regional_Cost"])/getFloat(row["Edit Hours"]) if getFloat(row["Edit Hours"]) not in ['',0,0.0,0.00] else 0.00
                        #listPrice = row["FO_List_Price"]
                        partNumber = row["PartNumber"]
                        hours_field = row["Edit Hours"]
                        activity_key = row["Activity"]
                        country = row["Execution Country"]
                    else:
                        cost = getFloat(row["Regional_Cost"])/getFloat(row["Final_Hrs"]) if getFloat(row["Final_Hrs"]) not in ['',0,0.0,0.00] else 0.00
                        #listPrice = row["FO_ListPrice"]
                        partNumber = row["FO_Eng"]
                        hours_field = row["Final_Hrs"]
                        activity_key = row["Deliverable"]
                        country = row["Execution_Country"]

                    if activity_key not in ('Off-Site','On-Site','Total'):
                        if country == excecutionCountry and hours_field not in ('',"0") and partNumber != '':
                            addValues(laborTypeDict,"Front Office Labor","Hours",getFloat(hours_field))
                            addValues(laborTypeDict,"Front Office Labor","Total Cost",round(getFloat(cost), 2) * getFloat(hours_field))
                            addValues(laboHours["Front Office Labor"], key, partNumber,getFloat(hours_field))
                        elif hours_field not in ('',"0") and partNumber != '':
                            addValues(laborTypeDict,"Intercompany Labor","Hours", getFloat(hours_field))
                            addValues(laborTypeDict,"Intercompany Labor", "Total Cost",round(getFloat(cost), 2) * getFloat(hours_field))
                            addValues(laboHours["Intercompany Labor"], key, partNumber,getFloat(hours_field))
            #Trace.Write("laboHours = " + str(laboHours))
            #Trace.Write(str(laborTypeDict))
            sellPriceDict = getSellPriceData(laboHours,item)
            populateLaborTypeTable1(labotTypeTable,item,laborTypeDict,sellPriceDict)
            calculateTotals(labotTypeTable,item)


    laborTypeTableData = dict()
    for row in labotTypeTable.Rows:
        if row["Labor_Type"] != "Total":
            addValues(laborTypeTableData,row["Labor_Type"],"Hours",row["Hours"])
            addValues(laborTypeTableData,row["Labor_Type"],"Total_Cost",round(getFloat(row["Total_Cost"]), 2))
            addValues(laborTypeTableData,row["Labor_Type"],"Total_Sell_Price",round(getFloat(row["Total_Sell_Price"]), 2))
    Trace.Write(str('1111111:: ')+str(laborTypeTableData))

    headerlabotTypeTable = Quote.QuoteTables["Header_Labor_Type_Table_Excel"]
    headerlabotTypeTable.Rows.Clear()
    populateLaborTypeTable2(headerlabotTypeTable,laborTypeTableData)

    if headerlabotTypeTable.Rows.Count > 0:
        totalHours = 0
        totalcost = 0
        totalSellPrice = 0
        for row in headerlabotTypeTable.Rows:
            if row["IsHeader"] == "Yes":
                totalHours += getFloat(row["Hours"])
                totalcost += getFloat(row["Total_Cost"])
                totalSellPrice += getFloat(row["Total_Sell_Price"])
        for row in headerlabotTypeTable.Rows:
            if row["IsHeader"] == "Yes":
                if row["Labor_Type"] == "Total":
                    row["Hours"] = totalHours
                    row["Total_Cost"] = totalcost
                    row["Total_Sell_Price"] = totalSellPrice
                else:
                    row["Percentage"] = str(round((getFloat(row["Hours"]) / totalHours) * 100,1)) if  totalHours > 0 else 0
    labotTypeTable.Save()
    headerlabotTypeTable.Save()