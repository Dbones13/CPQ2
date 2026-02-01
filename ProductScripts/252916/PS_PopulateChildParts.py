import math
from GS_Msid_Populatepartcontainer import checkPartQtyToBeAdded
import GS_MigrationPartsUtil as mpu
import GS_MigrationPartsUtil_2 as mpu2
import GS_MigrationPartsUtil_3 as mpu3
import GS_MigrationPartsUtil_4 as mpu4
import GS_MigrationPartsUtil_5 as mpu5
import GS_MigrationPartsUtil_6 as mpu6
import GS_MigrationPartsUtil_7 as mpu7
import GS_MigrationPartsUtil_8 as mpu8

globalQueDict = dict()
def log_dict(dictionary):
    Trace.Write(RestClient.SerializeToJson(dictionary))

def getContainer(product, containerName):
    return product.GetContainerByName(containerName)

def getAttrValue(name, partNumber, prodName):
    queDict = globalQueDict.get(prodName)
    if not queDict:
        return

    que = queDict.get(partNumber)
    if que is None:
        return

    migrationQuestion = que.get(name)
    if migrationQuestion is not None:
        return attributeValueDict.get(migrationQuestion)

def updateChildAttributes(row, productRow):
    if not row.Product:
        return
    for attr in filter(lambda a : a.DisplayType != "Container", row.Product.Attributes):
        if attr.Name == "ItemQuantity":
            attr.AssignValue(row["Quantity"])
            continue
        value = getAttrValue(attr.Name, row.Product.PartNumber, productRow.Product.Name)
        if value:
            value = value[0] if type(value) == type([]) else value
            if attr.DisplayType == "FreeInputNoMatching":
                attr.AssignValue(value)
                continue
            attr.SelectValue(value)

def populatePartsInChild(productRow, container):
    product = productRow.Product
    lineItemContainer = product.GetContainerByName("MSID_Added_Parts_Common_Container")
    lineItemContainer.Clear()
    for row in container.Rows:
        qty = row["Final Quantity"] if row["Final Quantity"] else 0
        if float(qty):
            childRow = lineItemContainer.AddNewRow()
            childRow["PartNumber"] = row["PartNumber"]
            childRow["Quantity"] = str(int(float(row["Final Quantity"])))

    lineItemContainer.Calculate()
    for row in lineItemContainer.Rows:
        row.IsSelected = True
        updateChildAttributes(row, productRow)

    lineItemContainer.Calculate()
    productRow.ApplyProductChanges()

def populateChildPartForMSID(product):
    partContainers, contProductMap = mpu6.getChildContainerMap()

    productContainer = product.GetContainerByName("MSID_Product_Container")
    for container in partContainers:
        if container == "MSID_Virtualization_Added_Parts_Common_Container":
            productContainerVirt = product.GetContainerByName("MSID_Product_Container_Virtualization_hidden")
            contVirt = product.GetContainerByName("MSID_Virtualization_Added_Parts_Common_Container")
            productRowVirt = productContainerVirt.Rows.GetByColumnName("Product Name", "Virtualization System")
            if not productRowVirt:
                continue
            populatePartsInChild(productRowVirt, contVirt)
        elif container == "MSID_Generic_System_Added_Parts_Common_Container":
            pass
            '''productContainerGen = product.GetContainerByName("MSID_Product_Container_Generic_hidden")
            i = 1
            for genericSysRow in product.GetContainerByName("MSID_Product_Container_Generic_hidden").Rows:
                contGen = genericSysRow.Product.GetContainerByName("MSID_Generic_System1_Added_Parts_Common_Container")
                productRowGen = productContainerGen.Rows.GetByColumnName("Product Name", "Generic System "+str(i))
                i=i+1
                if not productRowGen:
                    continue
                populatePartsInChild(productRowGen, contGen)'''
        else:
            cont = product.GetContainerByName(container)
            productRow = productContainer.Rows.GetByColumnName("Product Name", contProductMap[container])
            if not productRow:
                continue
            populatePartsInChild(productRow, cont)
            if contProductMap[container] == "FSC to SM":
                productContainerfsc = product.GetContainerByName("MSID_Product_Container_FSC_hidden")
                contfsc = product.GetContainerByName("MSID_FSC_to_SM_audit_Added_Parts_Common_Container")
                productRowfsc = productContainerfsc.Rows.GetByColumnName("Product Name", "FSC to SM Audit")
                populatePartsInChild(productRowfsc, contfsc)
            if contProductMap[container] == "FSC to SM IO Migration":
                productContainerfscio = product.GetContainerByName("MSID_Product_Container_FSC_IO_hidden")
                contfscio = product.GetContainerByName("MSID_FSCtoSM_IO_audit_Added_Parts_Common_Container")
                productRowfsc = productContainerfscio.Rows.GetByColumnName("Product Name", "FSC to SM IO Audit")
                populatePartsInChild(productRowfsc, contfscio)
            
def getFloat(v):
    if v:
        return float(v)
    return 0

def addFinalHours(totalDict, key, value):
    totalDict[key] = getFloat(totalDict.get(key, 0)) + getFloat(value)

def updateAttrDict(product, attributeValueDict, containerNames):
    for containerName in containerNames:
        container = getContainer(product, containerName)
        for row in container.Rows:
            for col in row.Columns:
                attributeValueDict[col.Name] = mpu.getValue(row,col)
            if containerName != "OPM_Node_Configuration":
                break

def updateAttrDictWithMultiplier(product, attrValDict, conNames):
    for conName in conNames:
        total = 0
        container = getContainer(product, conName)
        for row in container.Rows:
            for col in row.Columns:
                try:
                    total += float(mpu.getValue(row,col))
                except:
                    pass
        if total > 0:
            attrValDict[conName+"_Multiplier"] = 1
        else:
            attrValDict[conName+"_Multiplier"] = 0

def updateAttrDictMultiRow(product, attributeValueDict, containerNames):
    for containerName in containerNames:
        container = getContainer(product, containerName)
        for row in container.Rows:
            for col in row.Columns:
                l = attributeValueDict.get(col.Name,list())
                l.append(mpu.getValue(row,col))
                attributeValueDict[col.Name] = l

def updateContainerDetails(product, containerNames, attrValDict):
    for containerName in containerNames:
        container = getContainer(product, containerName)
        row = container.Rows[0]
        for col in row.Columns:
            attrValDict[col.Name] = mpu.getValue(row,col)

def getELCNTotalSum(attrValDict, keys , prefix):
    total = 0
    for key in keys:
        total += getFloat(attrValDict[prefix + "_" + key])
    return total

def updateAttrWithCustomEHPMHARTIOValues(product, attrValDict):
    container = product.GetContainerByName("EHPM_HART_IO_Configuration_Cont")

    for row in container.Rows:
        if row.RowIndex == 0:
            customKey = 'With_License'
        elif row.RowIndex == 2:
            customKey = 'Without_License'
        else:
            continue
        for col in row.Columns:
            try:
                attrValDict[customKey+"_"+col.Name] = float(mpu.getValue(row,col))
            except:
                attrValDict[customKey+"_"+col.Name] = 0
                pass

def updateAttrWithC200MigrationSESP(product, attrValDict):
    sespType = Quote.GetCustomField("Entitlement").Content if Quote and Quote.GetCustomField("Entitlement").Content else "No"
    C200sMigrating = getFloat(getContainer(product, 'C200_Migration_General_Qns_Cont').Rows[0]['C200_How_many_C200s_are_we_migrating'])

    if sespType in ("No","Support Flex", "Value Support Flex"):
        EPUPUOC1Points = C200sMigrating
        attrValDict["EPUPUOC1Points"] = EPUPUOC1Points
    else:
        pass

def migrationAttrDict(product):

    migAttrDict = dict()
    updateAttrDict(product, migAttrDict, [
        "OPM_Basic_Information",
        "OPM_Migration_platforms",
        "OPM_Node_Configuration",
        "OPM_FTE_Switches_migration_info",
        "OPM_Services",
        "MSID_CommonQuestions",
        "LCN_Design_Inputs_for_TPN_OTU_Upgrade",
        "NONSESP_Design_Inputs_for_Experion_Upgrade_License",
        "NONSESP_Design_Inputs_for_eServer_Upgrade_License",
        "EBR_Basic_Information",
        "EBR_Upgrade",
        "EBR_New_Additional_EBR",
        "EBR_Hardware_to_Host_EBR_Physical_Node_Only",
        "EBR_Services",
        "TPS_EX_Server_Cabinet_Config",
        "TPS_EX_Conversion_ESVT_Server",
        "TPS_EX_General_Questions",
        "TPS_EX_Monitors",
        "xPM_Network_Upgrade_Cont",
        "TPS_EX_Bundle_Conversion_Server_Stations",
        "xPM_Migration_General_Qns_Cont",
        "TCMI_General_Information",
        "TCMI_Hardware_and_Licenses",
        "TCMI_Services",
        "ENB_Migration_General_Qns_Cont",
        "EHPM_HART_IO_General_Qns_Cont",
        "CB_EC_migration_to_C300_UHIO_Configuration_Cont",
        "FSC_to_SM_General_Information",
        "C200_Migration_General_Qns_Cont",
        "FDM_Upgrade_General_questions",
        "xPM_C300_Series_ C_Cabinet_Configuration",
        "C200_Migration_Scenario_Cont",
        "LM_to_ELMM_ControlEdge_PLC_Migration_Gen_Cont",
        "XP10_Actuator_General_Information"
    ])
    updateAttrDictWithMultiplier(product, migAttrDict, [
        "LCN_Design_Inputs_for_TPN_OTU_Upgrade",
        "NONSESP_Design_Inputs_for_Experion_Upgrade_License",
        "NONSESP_Design_Inputs_for_eServer_Upgrade_License",
        "C200_Migration_General_Qns_Cont"
    ])

    updateAttrDictMultiRow(product, migAttrDict, [
    	"Orion_Station_Configuration",
        "xPM_Migration_Config_Cont",
        "ENB_Migration_Config_Cont",
        "TPS_EX_Additional_Stations",
        "TPS_EX_Additional_Servers",
        "TPS_EX_Station_Conversion_EST",
        "TPS_EX_Conversion_ACET_EAPP",
        "C200_Migration_Config_Cont",
        "FSC_to_SM_Configuration",
        "FDM_Upgrade_Hardware_to_host_FDM_Server",
        "FDM_Upgrade_Configuration",
        "LM_to_ELMM_ControlEdge_PLC_Cont",
        "LM_to_ELMM_ControlEdge_PLC_Local_IO_Cont",
        "LM_to_ELMM_ControlEdge_PLC_Remote_IO_Cont"
    ])
    migAttrDict["TPS_EX_Need_Domain_Controller_Added"] = product.Attr("TPS_EX_Need_Domain_Controller_Added").GetValue()
    mpu6.updateAttributeDictWithCustomFSCtoSM(product, migAttrDict)
    mpu6.updateAttributeDictWithCustomFSSMcom(product, migAttrDict)
    mpu5.updateAttrDictWithCustomFDMUpgrade(product, migAttrDict)
    mpu.updateAttrDictWithCustomOrion(product, migAttrDict)
    mpu8.updateAttrDictWithCustomXpm(product, migAttrDict, Quote)
    mpu.updateAttrWithCustomTpsValues(product, migAttrDict)
    mpu.updateAttributeWithCustomELCNValues(product, migAttrDict)
    updateAttrWithCustomEHPMHARTIOValues(product, migAttrDict)
    mpu.updateAttrWithCustomCBECValues(product, migAttrDict)
    mpu4.updateAttributeWithLMtoELMMValues(product, migAttrDict)
    updateAttrWithC200MigrationSESP(product, migAttrDict)
    mpu3.updateAttrDictWithCustomxPMC300(product, migAttrDict, Quote)
    mpu6.updateAttrDictWithCustomFSCtoSMParts(product, migAttrDict, Quote)
    mpu5.updateAttrDictWithXP10Actuator(product, migAttrDict)
    mpu7.FSCtoSM_IOparts(product, migAttrDict)
    if product.Attr("MIgration_Scope_Choices").GetValue() not in ["LABOR"]:
        mpu5.updateAttrDictWithCWSRAE(product, migAttrDict)
        mpu5.updateAttrDictWithQCSRAE(product, migAttrDict)
        mpu7.updateAttrDictWithTPA(product, migAttrDict,Quote)

    con = product.GetContainerByName('C200_Migration_Scenario_Cont')
    if con:
        TypeofUOC = con.Rows[0]['C200_Select_the_Migration_Scenario']
        if TypeofUOC =='C200 to ControlEdge UOC':
            mpu.updateAttributeWithCustomC200MigrationValues(product, migAttrDict)
        else:
            mpu2.updateAttrDictWithCustomC200toC300(product, migAttrDict, Quote)

    return migAttrDict

def updateProductDict(dictToUpdate, row, qty):
    if row.IsThirdParty:
        productDict = dictToUpdate["THIRD_PARTY"]
        partQty = productDict.get(row.Child_Part + row.Product_Name, [row.Child_Part, row.Product_Name, 0])
        partQty[2] = int(partQty[2]) + int(qty)
        productDict[row.Child_Part + row.Product_Name] = partQty
    else:
        productDict = dictToUpdate[row.Product_Name]
        partQty = productDict.get(row.Child_Part, 0)
        productDict[row.Child_Part] = int(partQty) + int(qty)

def getQuestionMapping(product_key):
    query = "select * from MIGRATION_MODULE_QUE_MAP where product_key = '{}'".format(product_key)
    res = SqlHelper.GetList(query)

    resDict = dict()
    for r in res:
        rDict = resDict.get(r.Module_Key,dict())
        rDict[r.Module_Question] = r.Migration_Question
        resDict[r.Module_Key] = rDict
    return resDict

def migrationValue(name, que, attrValues, defaults):
    migrationQuestion = que.get(name)
    if migrationQuestion is not None:
        Trace.Write(migrationQuestion)
        return attrValues.get(migrationQuestion).lower()
    defaultAns = defaults.get(name)
    if defaultAns is not None:
        return defaultAns.lower()

def canBeadded(row, attrValues, queDict, defaults):
    if row.Attribute_Name and migrationValue(row.Attribute_Name, queDict, attrValues, defaults) != row.Attribute_Value_Code.lower():
        return False
    if row.Dependency_Attribute_Name and migrationValue(row.Dependency_Attribute_Name, queDict, attrValues, defaults) != row.Dependency_Attribute_Value_Code.lower():
        return False
    if row.Dependency_Attribute_Name_2 and migrationValue(row.Dependency_Attribute_Name_2, queDict, attrValues, defaults) != row.Dependency_Attribute_Value_Code_2.lower():
        return False
    return True

def getPricingPartsForModel(res, attrValues, queDict, partNumbersToBeAdded, qty, prod, defaults):
    for row in res:
        if canBeadded(row, attrValues, queDict, defaults):
            productDict = partNumbersToBeAdded[prod]
            partQty = productDict.get(row.Child_Products, 0)
            productDict[row.Child_Products] = partQty + (qty * int(row.Quantity))

def getDefaultAnswer():
    query = "select * from KE_QUE_DEFAULT"
    res = SqlHelper.GetList(query)
    d = dict()
    for r in res:
        d[r.Attribute_Name] = r.Default
    return d

def getPricingParts(modules, attributeValueDict, partNumbersToBeAdded):
    global queDict
    global globalQueDict

    query = "select Child_Products, Quantity, Attribute_Name, Attribute_Value_Code, Dependency_Attribute_Name, Dependency_Attribute_Value_Code, Dependency_Attribute_Name_2, Dependency_Attribute_Value_Code_2  from KE_Package_Part_Qty_Mapping_Old where Package_Model_Number = '{0}' and Pricing = 'Yes' union select Child_Products, Quantity, Attribute_Name, Attribute_Value_Code, '','','','' from SERVER_CABINET_PART_QTY_MAPPING where Package_Model_Number = '{0}' and Pricing = 'Yes'"

    defaults = getDefaultAnswer()

    for product, packages in modules.items():
        queDict = getQuestionMapping(product)
        globalQueDict[product] = queDict
        for module, qty in packages.items():
            res = SqlHelper.GetList(query.format(module))
            getPricingPartsForModel(res, attributeValueDict, queDict.get(module,queDict.get("",dict())), partNumbersToBeAdded, qty, product, defaults)

def qtyBasedOnExpRelease(remoteUserEntered):
    qty= "0"
    if remoteUserEntered >= 6 and remoteUserEntered <= 10:
        qty = "1"
    elif remoteUserEntered >= 11 and remoteUserEntered <= 15:
        qty = "2"
    return qty

def getPartDetailDict(partsList):
    resDict = dict()
    query = "select PRODUCT_CATALOG_CODE, PRODUCT_NAME, PLSG, PLSGDesc from products p join HPS_PRODUCTS_MASTER hpm ON p.PRODUCT_CATALOG_CODE = hpm.PartNumber where PRODUCT_CATALOG_CODE in ('{}')"
    query = query.format("','".join(partsList))

    res = SqlHelper.GetList(query)
    for r in res:
        resDict[r.PRODUCT_CATALOG_CODE] = [r.PRODUCT_NAME, r.PLSG, r.PLSGDesc]
    return resDict

def getPartsToBeAdded(attributeValueDict):
    partNumbersToBeAdded = {
        "OPM": dict(),
        "LCN": dict(),
        "NONSESP": dict(),
        "EBR": dict(),
        "ELCN": dict(),
        "Orion_Console": dict(),
        "EHPM/EHPMX/ C300PM": dict(),
        "PM": dict(),
        "TPS_EXP": dict(),
        "TCMI": dict(),
        "LMTOELMM": dict(),
        "Spare Parts": dict(),
        "EHPMHART": dict(),
        "CBEC": dict(),
        "C200 Migration": dict(),
        "XPM C300": dict(),
        "FDM_Upgrade": dict(),
        "FSC_to_SM": dict(),
        "FSC_to_SM_audit": dict(),
        "XP10_Actuator": dict(),
        "Graphics_Migration": dict(),
        "FSCtoSM_IO": dict(),
        "FSCtoSM_IO_AUDIT": dict(),
        "CD_Actuator_IF_Upgrade": dict(),
        "CWS_RAE_Upgrade": dict(),
        "3rd_Party_PLC_to_ControlEdge_PLC/UOC": dict(),
        "Virtualization_System_Migration": dict(),
        "GS_Migration_1":dict(),
        "GS_Migration_2":dict(),
        "GS_Migration_3":dict(),
        "GS_Migration_4":dict(),
        "GS_Migration_5":dict(),
        "QCS_RAE_Upgrade": dict(),
        "TPA/PMD_Migration": dict(),
        # Added Module name -- Dipak Shekokar : CXCPQ-60173
        "ELEPIU_ControlEdge_RTU_Migration_Engineering": dict()
    }
    partsList = set()

    modules = {
        "OPM": dict(),
        "LCN": dict(),
        "NONSESP": dict(),
        "EBR": dict(),
        "ELCN": dict(),
        "Orion_Console": dict(),
        "EHPM/EHPMX/ C300PM": dict(),
        "PM": dict(),
        "TPS_EXP": dict(),
        "TCMI": dict(),
        "LMTOELMM": dict(),
        "Spare Parts": dict(),
        "EHPMHART": dict(),
        "CBEC": dict(),
        "C200 Migration": dict(),
        "XPM C300": dict(),
        "FDM_Upgrade": dict(),
        "FSC_to_SM": dict(),
        "FSC_to_SM_audit": dict(),
        "XP10_Actuator": dict(),
        "Graphics_Migration": dict(),
        "FSCtoSM_IO": dict(),
        "FSCtoSM_IO_AUDIT": dict(),
        "CD_Actuator_IF_Upgrade": dict(),
        "CWS_RAE_Upgrade": dict(),
        "3rd_Party_PLC_to_ControlEdge_PLC/UOC": dict(),
        "Virtualization_System_Migration": dict(),
        "GS_Migration_1":dict(),
        "GS_Migration_2":dict(),
        "GS_Migration_3":dict(),
        "GS_Migration_4":dict(),
        "GS_Migration_5":dict(),
        "QCS_RAE_Upgrade": dict(),
        "TPA/PMD_Migration": dict(),
        # Added Module name -- Dipak Shekokar : CXCPQ-60173
        "ELEPIU_ControlEdge_RTU_Migration_Engineering": dict()
    }

    query = "select * from MIGRATION_PART_MAPPING_OLD"
    res = SqlHelper.GetList(query)

    for r in res:
        qty = checkPartQtyToBeAdded(r, attributeValueDict)

        if qty and r.Module_Name:
            updateProductDict(modules, r, qty)
            partsList.add(r.Child_Part)

        if qty:
            updateProductDict(partNumbersToBeAdded, r, qty)
            partsList.add(r.Child_Part)

    query = "select * from MIGRATION_PART_MAPPING_OLD where CpqTableEntryId > {}".format(r.CpqTableEntryId)
    res = SqlHelper.GetList(query)
    for r in res:
        qty = checkPartQtyToBeAdded(r, attributeValueDict)

        if qty and r.Module_Name:
            updateProductDict(modules, r, qty)
            partsList.add(r.Child_Part)

        if qty:
            updateProductDict(partNumbersToBeAdded, r, qty)
            partsList.add(r.Child_Part)

    query = "select * from MIGRATION_PART_MAPPING_OLD where CpqTableEntryId > {}".format(r.CpqTableEntryId)
    res = SqlHelper.GetList(query)
    for r in res:
        qty = checkPartQtyToBeAdded(r, attributeValueDict)

        if qty and r.Module_Name:
            updateProductDict(modules, r, qty)
            partsList.add(r.Child_Part)

        if qty:
            updateProductDict(partNumbersToBeAdded, r, qty)
            partsList.add(r.Child_Part)
    getPricingParts(modules, attributeValueDict, partNumbersToBeAdded)

    return partNumbersToBeAdded, partsList

def getUserInputMap(container):
    userInputMap = dict()
    if container:
        for row in container.Rows:
            data = {
                'adjQty' : row['Adj Quantity'],
                'comment' : row['Comments']
            }
            userInputMap[row['PartNumber']] = data
    return userInputMap

def populatePartForMSID(msidProduct):
    global attributeValueDict
    attributeValueDict =  migrationAttrDict(msidProduct)
    log_dict(attributeValueDict)
    partNumbersToBeAdded, partsList = getPartsToBeAdded(attributeValueDict)

    if msidProduct.Attr('MIgration_Scope_Choices').GetValue() != "HW/SW":
        opmEngineeringCon = getContainer(msidProduct,"MSID_Labor_OPM_Engineering")
        for row in opmEngineeringCon.Rows:
            if row["Deliverable"] not in ('Total','Off-Site','On-Site'):
                if row["FO_Eng"]:
                    foQty = round((getFloat(row["Final_Hrs"]) * getFloat(row["FO_Eng_Percentage_Split"]) / 100))
                    addFinalHours(partNumbersToBeAdded["OPM"],row["FO_Eng"],foQty)
                if row["FO_Eng"] not in partsList:
                    partsList.add(row["FO_Eng"])
                if row["GES_Eng"] != '' and row["GES_Eng_Percentage_Split"] != '0':
                    gesQty = round((getFloat(row["Final_Hrs"]) * getFloat(row["GES_Eng_Percentage_Split"]) / 100))
                    addFinalHours(partNumbersToBeAdded["OPM"],row["GES_Eng"],gesQty)
                if row["GES_Eng"] not in partsList:
                    partsList.add(row["GES_Eng"])
        lcnOneTimeUpgradeCon = getContainer(msidProduct,"MSID_Labor_LCN_One_Time_Upgrade_Engineering")
        for row in lcnOneTimeUpgradeCon.Rows:
            if row["Deliverable"] not in ('Total','Off-Site','On-Site'):
                if row["FO_Eng"]:
                    foQty = round((getFloat(row["Final_Hrs"]) * getFloat(row["FO_Eng_Percentage_Split"]) / 100))
                    addFinalHours(partNumbersToBeAdded["LCN"],row["FO_Eng"],foQty)
                if row["FO_Eng"] not in partsList:
                    partsList.add(row["FO_Eng"])
                if row["GES_Eng"] != '' and row["GES_Eng_Percentage_Split"] != '0':
                    gesQty = round((getFloat(row["Final_Hrs"]) * getFloat(row["GES_Eng_Percentage_Split"]) / 100))
                    addFinalHours(partNumbersToBeAdded["LCN"],row["GES_Eng"],gesQty)
                if row["GES_Eng"] not in partsList:
                    partsList.add(row["GES_Eng"])

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

        ebrCon = getContainer(msidProduct,"MSID_Labor_EBR_Con")
        getLaborContainerData(ebrCon,"EBR")

        elcnCon = getContainer(msidProduct,"MSID_Labor_ELCN_Con")
        getLaborContainerData(elcnCon,"ELCN")

        orionConsoleCon = getContainer(msidProduct,"MSID_Labor_Orion_Console_Con")
        getLaborContainerData(orionConsoleCon,"Orion_Console")

        ehpmCon = getContainer(msidProduct,"MSID_Labor_EHPM_C300PM_Con")
        getLaborContainerData(ehpmCon,"EHPM/EHPMX/ C300PM")

        tpsCon = getContainer(msidProduct,"MSID_Labor_TPS_TO_EXPERION_Con")
        getLaborContainerData(tpsCon,"TPS_EXP")

        tcmiCon = getContainer(msidProduct,"MSID_Labor_TCMI_Con")
        getLaborContainerData(tcmiCon,"TCMI")

        ehpmhartioCon = getContainer(msidProduct,"MSID_Labor_EHPM_HART_IO_Con")
        getLaborContainerData(ehpmhartioCon,"EHPMHART")
        
        c200MigrationCon = getContainer(msidProduct,"MSID_Labor_C200_Migration_Con")
        getLaborContainerData(c200MigrationCon,"C200 Migration")
        
        cbCEtoC300UHIOCon = getContainer(msidProduct, "MSID_Labor_CB-EC_Upgrade_to_C300-UHIO_con")
        getLaborContainerData(cbCEtoC300UHIOCon,"CBEC")

        xPMCon = getContainer(msidProduct, "MSID_Labor_xPM_to_C300_Migration_Con")
        getLaborContainerData(xPMCon,"XPM C300")
        
        fscCon = getContainer(msidProduct, "MSID_Labor_FSC_to_SM_con")
        getLaborContainerData(fscCon,"FSC_to_SM")
        
        fscauditCon = getContainer(msidProduct, "MSID_Labor_FSC_to_SM_audit_Con")
        getLaborContainerData(fscauditCon,"FSC_to_SM_audit")
        
        fdmCon = getContainer(msidProduct, "MSID_Labor_FDM_Upgrade_Con")
        getLaborContainerData(fdmCon,"FDM_Upgrade")
        
        LMCon = getContainer(msidProduct, "MSID_Labor_LM_to_ELMM_Con")
        getLaborContainerData(LMCon,"LMTOELMM")
        
        XP10con = getContainer(msidProduct, "MSID_Labor_XP10_Actuator_Upgrade_con")
        getLaborContainerData(XP10con,"XP10_Actuator")
        
        CWSRAECon = getContainer(msidProduct, "MSID_Labor_CWS_RAE_Upgrade_con")
        getLaborContainerData(CWSRAECon,"CWS_RAE_Upgrade")

        GraphicsCon = getContainer(msidProduct, "MSID_Labor_Graphics_Migration_con")
        getLaborContainerData(GraphicsCon,"Graphics_Migration")
        
        fscsmioCon = getContainer(msidProduct, "MSID_Labor_FSCtoSM_IO_con")
        getLaborContainerData(fscsmioCon,"FSCtoSM_IO")
        
        fscsmioauditCon = getContainer(msidProduct, "MSID_Labor_FSC_to_SM_IO_Audit_Con")
        getLaborContainerData(fscsmioauditCon,"FSCtoSM_IO_AUDIT")
        
        CDActuatorCon = getContainer(msidProduct, "MSID_Labor_CD_Actuator_con")
        getLaborContainerData(CDActuatorCon,"CD_Actuator_IF_Upgrade")
        
        genCon1 = getContainer(msidProduct, "MSID_Labor_Generic_System1_Cont")
        getLaborContainerData(genCon1,"GS_Migration_1")

        genCon2 = getContainer(msidProduct, "MSID_Labor_Generic_System2_Cont")
        getLaborContainerData(genCon2,"GS_Migration_2")

        genCon3 = getContainer(msidProduct, "MSID_Labor_Generic_System3_Cont")
        getLaborContainerData(genCon3,"GS_Migration_3")

        genCon4 = getContainer(msidProduct, "MSID_Labor_Generic_System4_Cont")
        getLaborContainerData(genCon4,"GS_Migration_4")

        genCon5 = getContainer(msidProduct, "MSID_Labor_Generic_System5_Cont")
        getLaborContainerData(genCon5,"GS_Migration_5")

        VirtCon = getContainer(msidProduct, "MSID_Labor_Virtualization_con")
        getLaborContainerData(VirtCon,"Virtualization_System_Migration")
        
        QCSCon = getContainer(msidProduct, "MSID_Labor_QCS_RAE_Upgrade_con")
        getLaborContainerData(QCSCon,"QCS_RAE_Upgrade")
        
        TPACon = getContainer(msidProduct, "MSID_Labor_TPA_con")
        getLaborContainerData(TPACon,"TPA/PMD_Migration")

         # Extended Logic for ELEPIU Module -- Dipak Shekokar : CXCPQ-60173
        ELEPIUCon = getContainer(msidProduct, "MSID_Labor_ELEPIU_con")
        getLaborContainerData(ELEPIUCon,"ELEPIU_ControlEdge_RTU_Migration_Engineering")

        projectManagementCon = getContainer(msidProduct,"MSID_Labor_Project_Management")
        for row in projectManagementCon.Rows:
            if row["Deliverable"] not in ('Total','Off-Site','On-Site'):
                if row["FO_Eng"]:
                    foQty = round((getFloat(row["Final_Hrs"]) * getFloat(row["FO_Eng_Percentage_Split"]) / 100))
                    addFinalHours(partNumbersToBeAdded["PM"],row["FO_Eng"],foQty)
                if row["FO_Eng"] not in partsList:
                    partsList.add(row["FO_Eng"])
                if row["GES_Eng"] != '' and row["GES_Eng_Percentage_Split"] != '0':
                    gesQty = round((getFloat(row["Final_Hrs"]) * getFloat(row["GES_Eng_Percentage_Split"]) / 100))
                    addFinalHours(partNumbersToBeAdded["PM"],row["GES_Eng"],gesQty)
                if row["GES_Eng"] not in partsList:
                    partsList.add(row["GES_Eng"])

    sparePartsCabinetDict = mpu4.populateSparePartCabinetSummary(msidProduct, partsList)
    _3ptyplcuoc = mpu6.updteAttrDict3PartyPLCUOC(msidProduct)
    gs_dic_1 = mpu6.updAttrDictGS(msidProduct,0,partNumbersToBeAdded["GS_Migration_1"])
    gs_dic_2 = mpu6.updAttrDictGS(msidProduct,1,partNumbersToBeAdded["GS_Migration_2"])
    gs_dic_3 = mpu6.updAttrDictGS(msidProduct,2,partNumbersToBeAdded["GS_Migration_3"])
    gs_dic_4 = mpu6.updAttrDictGS(msidProduct,3,partNumbersToBeAdded["GS_Migration_4"])
    gs_dic_5 = mpu6.updAttrDictGS(msidProduct,4,partNumbersToBeAdded["GS_Migration_5"])
    partNumbersToBeAdded["Spare Parts"] = sparePartsCabinetDict
    partNumbersToBeAdded["3rd_Party_PLC_to_ControlEdge_PLC/UOC"] = _3ptyplcuoc
    partNumbersToBeAdded["GS_Migration_1"] = gs_dic_1
    partNumbersToBeAdded["GS_Migration_2"] = gs_dic_2
    partNumbersToBeAdded["GS_Migration_3"] = gs_dic_3
    partNumbersToBeAdded["GS_Migration_4"] = gs_dic_4
    partNumbersToBeAdded["GS_Migration_5"] = gs_dic_5

    containerNameMapping = {
        "OPM": getContainer(msidProduct, "MSID_OPM_Added_Parts_Common_Container"),
        "LCN": getContainer(msidProduct, "MSID_LCN_Added_Parts_Common_Container"),
        "NONSESP": getContainer(msidProduct, "MSID_NON_SESP_Added_Parts_Common_Container"),
        "EBR": getContainer(msidProduct,"MSID_EBR_Added_Parts_Common_Container"),
        "ELCN": getContainer(msidProduct,"MSID_ELCN_Added_Parts_Common_Container"),
        "PM": getContainer(msidProduct, "MSID_PM_Added_Parts_Common_Container"),
        "Orion_Console": getContainer(msidProduct,"MSID_Orion_Console_Added_Parts_Common_Container"),
        "EHPM/EHPMX/ C300PM": getContainer(msidProduct,"MSID_EHPM_C300PM_Added_Parts_Common_Container"),
        "TPS_EXP": getContainer(msidProduct,"MSID_TPS_EXP_Added_Parts_Common_Container"),
        "TCMI": getContainer(msidProduct,"MSID_TCMI_Added_Parts_Common_Container"),
        "LMTOELMM": getContainer(msidProduct,"MSID_LM_TO_ELMM_Added_Parts_Common_Container"),
        "Spare Parts": getContainer(msidProduct,"MSID_Spare_Parts_Added_Parts_Common_Container"),
        "EHPMHART": getContainer(msidProduct,"MSID_EHPM_HART_IO_Added_Parts_Common_Container"),
        "CBEC": getContainer(msidProduct,"MSID_CB_EC_Added_Parts_Common_Container"),
        "C200 Migration": getContainer(msidProduct,"MSID_C200_Migration_Added_Parts_Common_Container"),
        "XPM C300": getContainer(msidProduct, "MSID_xPM_C300_Added_Parts_Common_Container"),
        "FDM_Upgrade": getContainer(msidProduct, "MSID_FDM_Upgrade_Added_Parts_Common_Container"),
        "FSC_to_SM": getContainer(msidProduct, "MSID_FSC_to_SM_Added_Parts_Common_Container"),
        "FSC_to_SM_audit": getContainer(msidProduct, "MSID_FSC_to_SM_audit_Added_Parts_Common_Container"),
        "THIRD_PARTY" : getContainer(msidProduct, "MSID_Third_Party_Added_Parts_Common_Container"),
        "XP10_Actuator": getContainer(msidProduct, "MSID_XP10_Actuator_Added_Parts_Common_Container"),
        "Graphics_Migration": getContainer(msidProduct, "MSID_Graphics_Added_Parts_Common_Container"),
        "FSCtoSM_IO": getContainer(msidProduct, "MSID_FSCtoSM_IO_Added_Parts_Common_Container"),
        "FSCtoSM_IO_AUDIT" : getContainer(msidProduct, "MSID_FSCtoSM_IO_audit_Added_Parts_Common_Container"),
        "CD_Actuator_IF_Upgrade": getContainer(msidProduct, "MSID_CD_Actuator_Added_Parts_Common_Container"),
        "CWS_RAE_Upgrade": getContainer(msidProduct, "MSID_CWS_RAE_Upgrade_Added_Parts_Common_Container"),
        "3rd_Party_PLC_to_ControlEdge_PLC/UOC": getContainer(msidProduct, "MSID_Third_Party_PLC_Added_Parts_Common_Container"),
        "Virtualization_System_Migration": getContainer(msidProduct, "MSID_Virtualization_Added_Parts_Common_Container"),
        "GS_Migration_1" : mpu6.getGenericSystemCont(msidProduct,'MSID_Generic_System1_Added_Parts_Common_Container',0),
        "GS_Migration_2" : mpu6.getGenericSystemCont(msidProduct,'MSID_Generic_System1_Added_Parts_Common_Container',1),
        "GS_Migration_3" : mpu6.getGenericSystemCont(msidProduct,'MSID_Generic_System1_Added_Parts_Common_Container',2),
        "GS_Migration_4" : mpu6.getGenericSystemCont(msidProduct,'MSID_Generic_System1_Added_Parts_Common_Container',3),
        "GS_Migration_5" : mpu6.getGenericSystemCont(msidProduct,'MSID_Generic_System1_Added_Parts_Common_Container',4),
        "QCS_RAE_Upgrade": getContainer(msidProduct, "MSID_QCS_Added_Parts_Common_Container"),
        "TPA/PMD_Migration": getContainer(msidProduct, "MSID_TPA_Added_Parts_Common_Container"),
         # Extended Logic for ELEPIU Module -- Dipak Shekokar : CXCPQ-60173
        "ELEPIU_ControlEdge_RTU_Migration_Engineering": getContainer(msidProduct, "MSID_ELEPIU_Added_Parts_Common_Container")
    }
    partsList.add("EP-S08CAL")
    partsList.add("EP-S04CAL")
    log_dict(partsList)
    partDetailsDict = getPartDetailDict(partsList)
    opmUserInput = getUserInputMap(containerNameMapping["OPM"])

    for product, parts in partNumbersToBeAdded.items():
        container = containerNameMapping[product]
        if container == None:
            continue
        if product == "THIRD_PARTY":
            container.Clear()
            for part, data in parts.items():
                if data[2] > 0.00 and data[2] != '':
                    row = container.AddNewRow(False)
                    row['PartNumber'] = data[0]
                    row['Quantity'] = str(data[2])
                    adjQty = 0
                    row['Adj Quantity'] = str(adjQty)
                    row['Final Quantity'] = str(getFloat(data[2]) + adjQty)
                    row['ModuleName'] = data[1]
                    if partDetailsDict.get(data[0]):
                        row['PartDescription'] = partDetailsDict[data[0]][0]
                        row['PLSG'] = partDetailsDict[data[0]][1]
                        row['plsgDescription'] = partDetailsDict[data[0]][2]
            continue
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

    TargetExpRelease = attributeValueDict["MSID_Future_Experion_Release"]
    remoteUserEntered  = int(attributeValueDict["OPM_No_of_RESS_Remote_Users"] if attributeValueDict["OPM_No_of_RESS_Remote_Users"] else 0)
    container = containerNameMapping["OPM"]
    Qty =  qtyBasedOnExpRelease(remoteUserEntered)
    epPart = ""
    if TargetExpRelease in ('R501','R510','R511','R520'):
        epPart = "EP-S04CAL"
    elif TargetExpRelease in ('R432'):
        epPart = "EP-S08CAL"
    if epPart and Qty != "0":
        row = container.AddNewRow(False)
        row['PartNumber'] = epPart
        row['Quantity']  = Qty
        adjQty = 0
        comment = ''
        if opmUserInput.get(part):
            adjQty = getFloat(opmUserInput[part]['adjQty'])
            comment = userInputMap[part]['comment']
        row['Adj Quantity'] = str(adjQty)
        row['Final Quantity'] = str(getFloat(qty) + adjQty)
        row['Comments'] = comment
        if partDetailsDict.get(epPart):
            row['PartDescription'] = partDetailsDict[epPart][0]
            row['PLSG'] = partDetailsDict[epPart][1]
            row['plsgDescription'] = partDetailsDict[epPart][2]

    container.Calculate()
msidContainer = getContainer(Product, "Migration_MSID_Selection_Container")
for row in msidContainer.Rows:
    msidProduct = row.Product
    populatePartForMSID(msidProduct)
    populateChildPartForMSID(msidProduct)
    if "Orion Console" in row.Product.Attr("MSID_Selected_Products").GetValue():
        mpu.populateWriteIns(msidProduct)
    if "FSC to SM" in row.Product.Attr("MSID_Selected_Products").GetValue() and "FSC to SM IO Migration" not in row.Product.Attr("MSID_Selected_Products").GetValue():
        mpu.populateWriteInsFSC(msidProduct)
    if "TPS to Experion" in row.Product.Attr("MSID_Selected_Products").GetValue():
        mpu2.populateWriteInsTPS(msidProduct)
    if "LM to ELMM ControlEdge PLC" in row.Product.Attr("MSID_Selected_Products").GetValue():
        mpu5.populateWriteInsLM(msidProduct)
    if "CD Actuator I-F Upgrade" in row.Product.Attr("MSID_Selected_Products").GetValue():
        mpu2.populateWriteInsCDActuatorIFUpgrade(msidProduct)
    if "CWS RAE Upgrade" in row.Product.Attr("MSID_Selected_Products").GetValue():
        if msidProduct.Attr("MIgration_Scope_Choices").GetValue() not in ["LABOR"]:
            mpu3.populateWriteInsCWSRAEUpgrade(msidProduct,Quote)
    if "TPA/PMD Migration" in row.Product.Attr("MSID_Selected_Products").GetValue():
        mpu8.populateWriteInsTPAPMD(msidProduct)
    if "C200 Migration" in row.Product.Attr("MSID_Selected_Products").GetValue():
        migScenario = mpu.getRowData(msidProduct, "C200_Migration_Scenario_Cont","C200_Select_the_Migration_Scenario")
        #if migScenario == 'C200 to ControlEdge UOC':
        mpu.populateWriteInsC200(msidProduct)
    if "OPM" in row.Product.Attr("MSID_Selected_Products").GetValue():
        mpu2.populateWriteInsOPM(msidProduct)
    if "CB-EC Upgrade to C300-UHIO" in row.Product.Attr("MSID_Selected_Products").GetValue():
        mpu8.populateCBECwritein(msidProduct)
    row.ApplyProductChanges()
msidContainer.Calculate()