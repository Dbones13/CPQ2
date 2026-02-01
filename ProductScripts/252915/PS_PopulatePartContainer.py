import math
from ProductUtil import getContainer
from GS_MigrationPartsUtil import (
    updateAttributeWithCustomC200MigrationValues,
    updateAttributeWithCustomELCNValues,
    updateAttrWithCustomCBECValues,
    updateAttrWithCustomTpsValues
)
from GS_Msid_Populatepartcontainer import checkPartQtyToBeAdded #
from GS_MigrationPartsUtil_2 import updateAttrDictWithCustomC200toC300
from GS_MigrationPartsUtil_3 import updateAttrDictWithCustomxPMC300
from GS_MigrationPartsUtil_4 import updateAttributeWithLMtoELMMValues, populateSparePartCabinetSummary
from GS_MigrationPartsUtil_5 import updateAttrDictWithCustomFDMUpgrade, updateAttrDictWithXP10Actuator,updateAttrDictWithCWSRAE,updateAttrDictWithQCSRAE
from GS_MigrationPartsUtil_6 import GetPartAndModulesDict #updateAttrWithTpsExpValues
from GS_MigrationPartsUtil_7 import FSCtoSM_IOparts, updateAttrDictWithTPA
from GS_MigrationPartsUtil_8 import updateAttrDictWithCustomXpm
def log_dict(d):
    Trace.Write(RestClient.SerializeToJson(d))
    return RestClient.SerializeToJson(d)

def getFloat(var):
    if var:
        return float(var)
    return 0

def addFinalHours(totalDict, key, value):
    totalDict[key] = getFloat(totalDict.get(key, 0)) + getFloat(value)

def getValue(row,col):
    if col.IsProductAttribute and col.ReferencingAttribute and col.ReferencingAttribute.SelectedValue:
        val = col.ReferencingAttribute.SelectedValue.Display
        if not val:
            val = col.DisplayValue
            if not val:
                val = row[col.Name] if row[col.Name] else ''
        return val
    if col.DisplayType == 'DropDown':
        val = col.DisplayValue
        if not val:
            val = row[col.Name] if row[col.Name] else ''
        return val
    if col.DisplayType == 'TextBox':
        return col.Value
    if col.DisplayType == "Label":
        return col.Value
    return ""

def updateAttributeDict(product, attributeValueDict, containerNames):
    for containerName in containerNames:
        container = getContainer(product, containerName)
        for row in container.Rows:
            for col in row.Columns:
                attributeValueDict[col.Name] = getValue(row,col)
            if containerName != "OPM_Node_Configuration":
                break

def updateAttributeDictWithMultiplier(product, attributeValueDict, containerNames):
    for containerName in containerNames:
        total = 0
        container = getContainer(product, containerName)
        for row in container.Rows:
            for col in row.Columns:
                try:
                    total += float(getValue(row,col))
                except:
                    pass
        if total > 0:
            attributeValueDict[containerName+"_Multiplier"] = 1
        else:
            attributeValueDict[containerName+"_Multiplier"] = 0

def updateAttributeDictMultiRow(product, attributeValueDict, containerNames):
    for containerName in containerNames:
        container = getContainer(product, containerName)
        for row in container.Rows:
            for col in row.Columns:
                l = attributeValueDict.get(col.Name,list())
                l.append(getValue(row,col))
                attributeValueDict[col.Name] = l

def updateContainerDetails(product, containerNames, attributeValueDict):
    for containerName in containerNames:
        container = getContainer(product, containerName)
        row = container.Rows[0]
        for col in row.Columns:
            attributeValueDict[col.Name] = getValue(row,col)

def getELCNTotalSum(attributeValueDict, keys , prefix):
    total = 0
    for key in keys:
        total += getFloat(attributeValueDict[prefix + "_" + key])
    return total

def updateAttributeDictWithCustomOrion(product, migrationAttrDict):
    con = getContainer(product, "Orion_Station_Configuration")
    for row in con.Rows:
        l = migrationAttrDict.get("Orion_Left_Aux_Sum_0",list())
        l.append(str(getFloat(row["Orion_Number_of_Left_Auxiliary_Equipment_Unit"]) + getFloat(row["Orion_Number_of_Left_Extended_Auxiliary_Equipment_Unit"]) == 0).upper())
        migrationAttrDict["Orion_Left_Aux_Sum_0"] = l

        l = migrationAttrDict.get("Orion_Right_Aux_Sum_0",list())
        l.append(str(getFloat(row["Orion_Number_of_Right_Auxiliary_Equipment_Unit"]) + getFloat(row["Orion_Number_of_Right_Extended_Auxiliary_Equipment_Unit"]) == 0).upper())
        migrationAttrDict["Orion_Right_Aux_Sum_0"] = l

        l = migrationAttrDict.get("Orion_2_3_Position_Sum_1",list())
        l.append(str(getFloat(row["Orion_Number_of_2_Position_Base_Unit"]) + getFloat(row["Orion_Number_of_3_Position_Base_Unit"]) == 1).upper())
        migrationAttrDict["Orion_2_3_Position_Sum_1"] = l

        l = migrationAttrDict.get("Orion_2_Position_multiplier",list())
        l.append(1 if getFloat(row["Orion_Number_of_2_Position_Base_Unit"]) > 0 else 0)
        migrationAttrDict["Orion_2_Position_multiplier"] = l

        l = migrationAttrDict.get("Orion_3_Position_multiplier",list())
        l.append(1 if getFloat(row["Orion_Number_of_3_Position_Base_Unit"]) > 0 else 0)
        migrationAttrDict["Orion_3_Position_multiplier"] = l

def updateAttributeWithCustomEHPMHARTIOValues(product, attributeValueDict):
    container = Product.GetContainerByName("EHPM_HART_IO_Configuration_Cont")
    for row in container.Rows:
        if row.RowIndex == 0:
            customKey = 'With_License'
        elif row.RowIndex == 2:
            customKey = 'Without_License'
        else:
            continue
        for col in row.Columns:
            try:
                attributeValueDict[customKey+"_"+col.Name] = float(getValue(row,col))
            except:
                attributeValueDict[customKey+"_"+col.Name] = 0
                pass

def updateAttributeWithC200MigrationSESP(product, attributeValueDict):
    sespType = Quote.GetCustomField("Entitlement").Content if Quote and Quote.GetCustomField("Entitlement").Content else "No"
    C200sMigrating = getFloat(getContainer(Product, 'C200_Migration_General_Qns_Cont').Rows[0]['C200_How_many_C200s_are_we_migrating'])

    if sespType in ("No","Support Flex", "Value Support Flex"):
        EPUPUOC1Points = C200sMigrating
        attributeValueDict["EPUPUOC1Points"] = EPUPUOC1Points
    else:
        pass

def updateAttributeDictWithCustomFSCtoSM(product, migrationAttrDict):
    con = getContainer(product, "FSC_to_SM_Configuration")
    for row in con.Rows:
        l = migrationAttrDict.get("FSC_to_SM_Serial_communication_System_gtr_2",list())
        l.append('True' if getFloat(row["FSC_to_SM_Serial_communication_System"]) > 2 else 'False')
        migrationAttrDict["FSC_to_SM_Serial_communication_System_gtr_2"] = l

def updateAttributeDictWithCustomFSSMcom(product, migrationAttrDict):
    con = getContainer(product, "FSC_to_SM_Configuration")
    for row in con.Rows:
        l = migrationAttrDict.get("FSC_to_SM_Serial_communication_System_gtr_0",list())
        l.append('True' if getFloat(row["FSC_to_SM_Serial_communication_System"]) > 0 else 'False')
        migrationAttrDict["FSC_to_SM_Serial_communication_System_gtr_0"] = l

def updateAttrDictWithCustomFSCtoSMParts(product, attrValDict, Quote):
    product = Product
    con1 = getContainer(product, 'FSC_to_SM_Configuration')
    sespType = Quote.GetCustomField("Entitlement").Content if Quote and Quote.GetCustomField("Entitlement").Content else "No"
    if con1.Rows.Count >0:
        FC_DCOM_485 = 0.00
        #SDW_550EC = 0.00
        SDW_50194005_001 = 0.00
        FS_CCI_UNI_04 = 0.00
        FS_CCI_HSE_02 = 0.00
        MTL24571 = 0.00
        FS_CCI_UNI_04_data = 0.00
        FS_CCI_HSE_02_data = 0.00
        FC_DCOM_485_data = 0.0
        SDW_550EC_data = 0.0
        MTL24571_data = 0.0
        FS_SMSNUPL801 = 0.0
        diff = 0.0
        FS_SMSNUPL801_01S = 0.0
        FS_SMSNE810_01 = 0.0
        for row in con1.Rows:
            fscComSystem = getFloat(row['FSC_to_SM_Serial_communication_System'])
            fscDCS = (row['FSC_to_SM_SM_communication_to_DCS'])
            migratedSystemCount = getFloat(row['FSC_to_SM_How_many_systems_with_same_configuration_to_be_migrated_in_this_proposal'])
            fscSysSafeNet = getFloat(row['FSC_to_SM_How_many_FSC_Systems_are_in_the_SafeNet_network'])
            fcsConfigConn = (row['FSC_to_SM_Are_the_FSCs_in_this_configuration_connected_to_a_SafeNet_network'])
            fcsSysSafeNetMig = getFloat(row['FSC_to_SM_How_many_FSC_Systems_from_the_SafeNet_network_are_we_migrating_in_the_first_phase'])
            if fscComSystem == 0.00:
                FC_DCOM_485_data  =  1.00
            elif fscComSystem > 0.00:
                if fscDCS == 'Serial Modbus-RTU' or fscDCS == '' :
                    FC_DCOM_485_data = 2.00 + fscComSystem
                else:
                    FC_DCOM_485_data = fscComSystem
            FS_CCI_UNI_04_data = ((2.00 * FC_DCOM_485_data) - 2.00)
            if fscDCS == 'Modbus-TCP/IP' or fscDCS == 'EUCN' :
                SDW_550EC_data = 3.00
            else:
                SDW_550EC_data = 1.00
            if fscDCS == 'FTE-SCADA':
                MTL24571_data = 2.00
            else:
                MTL24571_data = 0.00
            if fcsConfigConn == 'Yes' or fcsConfigConn == '':
                diff = fscSysSafeNet - fcsSysSafeNetMig
                if diff > 0.0 and sespType == 'No':
                    FS_SMSNUPL801 += diff
                    FS_SMSNE810_01 = 1
                    attrValDict['FS_SMSNUPL801'] = round(FS_SMSNUPL801)
                elif diff > 0.0 and (sespType == 'Yes' or sespType == 'K&E Pricing Plus' or sespType == 'K&E Pricing Flex' or sespType == 'Non-SESP MSID with new SESP Plus' or sespType == 'Non-SESP MSID with new SESP Flex'):
                    FS_SMSNUPL801_01S += diff
                    FS_SMSNE810_01 = 1
                    attrValDict['FS_SMSNUPL801_01S'] = round(FS_SMSNUPL801_01S)
            FS_CCI_HSE_02_data =round(float((SDW_550EC_data + MTL24571_data)/2.00))

            FC_DCOM_485 += float(FC_DCOM_485_data * migratedSystemCount)
            #SDW_550EC += float(SDW_550EC_data * migratedSystemCount)
            SDW_50194005_001 += float(SDW_550EC_data * migratedSystemCount)
            MTL24571 += float(MTL24571_data * migratedSystemCount)
            FS_CCI_UNI_04 += float(FS_CCI_UNI_04_data * migratedSystemCount)
            FS_CCI_HSE_02 += float(FS_CCI_HSE_02_data * migratedSystemCount)

        attrValDict['FS_CCI_HSE_02'] = round(FS_CCI_HSE_02)
        attrValDict['FC_DCOM_485'] = round(FC_DCOM_485)
        #attrValDict['SDW_550EC'] = round(SDW_550EC)
        attrValDict['SDW_50194005_001'] = round(SDW_50194005_001)
        attrValDict['MTL24571'] = round(MTL24571)
        attrValDict['FS_CCI_UNI_04'] = round(FS_CCI_UNI_04)
        attrValDict['FS_SMSNE810_01'] = round(FS_SMSNE810_01)

def migrationAttrDict(product):
    migrationAttrDict = dict()
    updateAttributeDict(product, migrationAttrDict, [
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
        "C200_Migration_General_Qns_Cont",
        "CB_EC_migration_to_C300_UHIO_Configuration_Cont",
        "FDM_Upgrade_General_questions",
        "FSC_to_SM_General_Information",
        "xPM_C300_Series_ C_Cabinet_Configuration",
        "C200_Migration_Scenario_Cont",
        "LM_to_ELMM_ControlEdge_PLC_Migration_Gen_Cont",
        "XP10_Actuator_General_Information"
    ])
    updateAttributeDictWithMultiplier(product, migrationAttrDict, [
        "LCN_Design_Inputs_for_TPN_OTU_Upgrade",
        "NONSESP_Design_Inputs_for_Experion_Upgrade_License",
        "NONSESP_Design_Inputs_for_eServer_Upgrade_License"
    ])

    updateAttributeDictMultiRow(product, migrationAttrDict, [
    	"Orion_Station_Configuration",
        "xPM_Migration_Config_Cont",
        "ENB_Migration_Config_Cont",
        "TPS_EX_Additional_Stations",
        "TPS_EX_Additional_Servers",
        "TPS_EX_Station_Conversion_EST",
        "TPS_EX_Conversion_ACET_EAPP",
        "C200_Migration_Config_Cont",
        "FDM_Upgrade_Configuration",
        "FDM_Upgrade_Hardware_to_host_FDM_Server",
        "FDM_Upgrade_Additional_Configuration",
        "FSC_to_SM_Configuration",
        "LM_to_ELMM_ControlEdge_PLC_Cont",
        "LM_to_ELMM_ControlEdge_PLC_Local_IO_Cont",
        "LM_to_ELMM_ControlEdge_PLC_Remote_IO_Cont"
    ])

    migrationAttrDict["TPS_EX_Need_Domain_Controller_Added"] = product.Attr("TPS_EX_Need_Domain_Controller_Added").GetValue()
    #updateAttrWithTpsExpValues(product, migrationAttrDict)
    updateAttributeDictWithCustomFSCtoSM(product, migrationAttrDict)
    updateAttributeDictWithCustomFSSMcom(product, migrationAttrDict)
    updateAttrDictWithCustomFDMUpgrade(product, migrationAttrDict)
    updateAttributeDictWithCustomOrion(product, migrationAttrDict)
    updateAttrDictWithCustomXpm(product, migrationAttrDict, Quote)
    updateAttrWithCustomTpsValues(product, migrationAttrDict)
    updateAttributeWithCustomELCNValues(product, migrationAttrDict)
    updateAttributeWithCustomEHPMHARTIOValues(product, migrationAttrDict)
    FSCtoSM_IOparts(product, migrationAttrDict)
    #updateAttributeWithCustomC200MigrationValues(product, migrationAttrDict)
    updateAttrWithCustomCBECValues(product, migrationAttrDict)
    updateAttributeWithLMtoELMMValues(product, migrationAttrDict)
    updateAttributeWithC200MigrationSESP(product, migrationAttrDict)
    updateAttrDictWithCustomxPMC300(product, migrationAttrDict, Quote)
    #updateAttrDictWithCustomC200toC300(product, migrationAttrDict, Quote)
    updateAttrDictWithCustomFSCtoSMParts(product, migrationAttrDict, Quote)
    updateAttrDictWithXP10Actuator(product, migrationAttrDict)
    if Product.Attr("MIgration_Scope_Choices").GetValue() not in ["LABOR"]:
    	updateAttrDictWithCWSRAE(product, migrationAttrDict)
        updateAttrDictWithQCSRAE(product, migrationAttrDict)
        updateAttrDictWithTPA(product, migrationAttrDict,Quote)
    con = product.GetContainerByName('C200_Migration_Scenario_Cont')
    if con:
        TypeofUOC = con.Rows[0]['C200_Select_the_Migration_Scenario']
        if TypeofUOC =='C200 to ControlEdge UOC':
            updateAttributeWithCustomC200MigrationValues(product, migrationAttrDict)
        else:
            updateAttrDictWithCustomC200toC300(product, migrationAttrDict, Quote)
    return migrationAttrDict

def updateProductDict(dictToUpdate, row, qty):
    if row.IsThirdParty:
        productDict = dictToUpdate["THIRD_PARTY"]
        partQty = productDict.get(row.Child_Part + row.Product_Name, [row.Child_Part, row.Product_Name, 0])
        partQty[2] = partQty[2] + int(qty)
        productDict[row.Child_Part + row.Product_Name] = partQty
    else:
        productDict = dictToUpdate[row.Product_Name]
        partQty = productDict.get(row.Child_Part, 0)
        productDict[row.Child_Part] = partQty + int(qty)

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
        return attrValues.get(migrationQuestion,'').lower()
    defaultAns = defaults.get(name)
    if defaultAns is not None:
        return defaultAns.lower()

def canBeadded(row, attrValues, queDict, defaults):
    if row.Attribute_Name and migrationValue(row.Attribute_Name, queDict, attrValues, defaults) != row.Attribute_Value_Code.lower():
        Trace.Write("Condition Failed {} : {} != {}".format(row.Attribute_Name, migrationValue(row.Attribute_Name, queDict, attrValues, defaults) , row.Attribute_Value_Code ))
        return False
    if row.Dependency_Attribute_Name and migrationValue(row.Dependency_Attribute_Name, queDict, attrValues, defaults) != row.Dependency_Attribute_Value_Code.lower():
        Trace.Write("Condition Failed {} : {} != {}".format(row.Dependency_Attribute_Name, migrationValue(row.Dependency_Attribute_Name, queDict, attrValues, defaults), row.Dependency_Attribute_Value_Code ))
        return False
    if row.Dependency_Attribute_Name_2 and migrationValue(row.Dependency_Attribute_Name_2, queDict, attrValues, defaults) != row.Dependency_Attribute_Value_Code_2.lower():
        Trace.Write("Condition Failed {} : {} != {}".format(row.Dependency_Attribute_Name_2, migrationValue(row.Dependency_Attribute_Name_2, queDict, attrValues, defaults) , row.Dependency_Attribute_Value_Code_2 ))
        return False
    return True

def getPricingPartsForModel(res, attrValues, queDict, partNumbersToBeAdded, qty, prod, defaults):
    partsAdded = set()
    for row in res:
        if canBeadded(row, attrValues, queDict, defaults):
            productDict = partNumbersToBeAdded[prod]
            partQty = productDict.get(row.Child_Products, 0)
            productDict[row.Child_Products] = partQty + (qty * int(row.Quantity))
            if partQty + (qty * int(row.Quantity)) > 0:
                partsAdded.add(row.Child_Products)
    return partsAdded

def getDefaultAnswer():
    query = "select * from KE_QUE_DEFAULT"
    res = SqlHelper.GetList(query)
    d = dict()
    for r in res:
        d[r.Attribute_Name] = r.Default
    return d

def getPricingParts(modules, attributeValueDict, partNumbersToBeAdded, partsList):

    query = "select Child_Products, Quantity, Attribute_Name, Attribute_Value_Code, Dependency_Attribute_Name, Dependency_Attribute_Value_Code, Dependency_Attribute_Name_2, Dependency_Attribute_Value_Code_2 from KE_Package_Part_Qty_Mapping_Old where Package_Model_Number = '{0}' and Pricing = 'Yes' union select Child_Products, Quantity, Attribute_Name, Attribute_Value_Code, '','','','' from SERVER_CABINET_PART_QTY_MAPPING where Package_Model_Number = '{0}' and Pricing = 'Yes'"

    defaults = getDefaultAnswer()

    for product, packages in modules.items():
        queDict = getQuestionMapping(product)
        for module, qty in packages.items():
            res = SqlHelper.GetList(query.format(module))
            partsList = partsList.union(getPricingPartsForModel(res, attributeValueDict, queDict.get(module,queDict.get("",dict())), partNumbersToBeAdded, qty, product, defaults))
    return partsList

def qtyBasedOnExpRelease(remoteUserEntered):
    qty= "0"
    if remoteUserEntered >= 6 and remoteUserEntered <= 10:
        qty = "1"
    elif remoteUserEntered >= 11 and remoteUserEntered <= 15:
        qty = "2"
    return qty

def getPartDetailDict(partsList):
    resDict = dict()
    query = "select PRODUCT_CATALOG_CODE, PRODUCT_NAME, PLSG, PLSGDesc from products p join HPS_PRODUCTS_MASTER hpm ON p.PRODUCT_CATALOG_CODE = hpm.PartNumber where PRODUCT_CATALOG_CODE in ('{0}') UNION select PRODUCT_CATALOG_CODE, PRODUCT_NAME, PLSG, PLSGDesc from Migration_Third_Party_Products where PRODUCT_CATALOG_CODE in ('{0}')"
    query = query.format("','".join(partsList))

    res = SqlHelper.GetList(query)
    for r in res:
        resDict[r.PRODUCT_CATALOG_CODE] = [r.PRODUCT_NAME, r.PLSG, r.PLSGDesc]
    return resDict

def getPartsToBeAdded(attributeValueDict):
    partNumbersToBeAdded, modules = GetPartAndModulesDict()
    partsList = set()
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
    query = "select * from MIGRATION_PART_MAPPING_OLD where CpqTableEntryId>{}".format(r.CpqTableEntryId)
    res = SqlHelper.GetList(query)

    for r in res:
        qty = checkPartQtyToBeAdded(r, attributeValueDict)

        if qty and r.Module_Name:
            updateProductDict(modules, r, qty)
            partsList.add(r.Child_Part)

        if qty:
            updateProductDict(partNumbersToBeAdded, r, qty)
            partsList.add(r.Child_Part)
    query = "select * from MIGRATION_PART_MAPPING_OLD where CpqTableEntryId>{}".format(r.CpqTableEntryId)
    res = SqlHelper.GetList(query)

    for r in res:
        qty = checkPartQtyToBeAdded(r, attributeValueDict)

        if qty and r.Module_Name:
            updateProductDict(modules, r, qty)
            partsList.add(r.Child_Part)

        if qty:
            updateProductDict(partNumbersToBeAdded, r, qty)
            partsList.add(r.Child_Part)

    partsList = getPricingParts(modules, attributeValueDict, partNumbersToBeAdded, partsList)

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

tempdata = {"C300_var_2": 0, "C300_var_11":  0, "C200_UOC_var_9": 0}
Product.Attr('Temporary Data').AssignValue(str(tempdata))

attributeValueDict = migrationAttrDict(Product)

partNumbersToBeAdded, partsList = getPartsToBeAdded(attributeValueDict)

if Product.Attr('MIgration_Scope_Choices').GetValue() != "HW/SW":
    opmEngineeringCon = getContainer(Product,"MSID_Labor_OPM_Engineering")
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

    lcnOneTimeUpgradeCon = getContainer(Product,"MSID_Labor_LCN_One_Time_Upgrade_Engineering")
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
                    addFinalHours(partNumbersToBeAdded[product],row["GES_Eng"],gesQty)
                if row["GES_Eng"] not in partsList:
                    partsList.add(row["GES_Eng"])

    ebrCon = getContainer(Product,"MSID_Labor_EBR_Con")
    getLaborContainerData(ebrCon,"EBR")

    elcnCon = getContainer(Product, "MSID_Labor_ELCN_Con")
    getLaborContainerData(elcnCon,"ELCN")

    orionConsoleCon = getContainer(Product,"MSID_Labor_Orion_Console_Con")
    getLaborContainerData(orionConsoleCon,"Orion_Console")

    ehpmCon = getContainer(Product, "MSID_Labor_EHPM_C300PM_Con")
    getLaborContainerData(ehpmCon,"EHPM/EHPMX/ C300PM")

    tpsCon = getContainer(Product, "MSID_Labor_TPS_TO_EXPERION_Con")
    getLaborContainerData(tpsCon,"TPS_EXP")

    tcmiCon = getContainer(Product, "MSID_Labor_TCMI_Con")
    getLaborContainerData(tcmiCon,"TCMI")

    ehpmhartioCon = getContainer(Product, "MSID_Labor_EHPM_HART_IO_Con")
    getLaborContainerData(ehpmhartioCon,"EHPMHART")

    c200MigrationCon = getContainer(Product, "MSID_Labor_C200_Migration_Con")
    getLaborContainerData(c200MigrationCon,"C200 Migration")

    cbCEtoC300UHIOCon = getContainer(Product, "MSID_Labor_CB-EC_Upgrade_to_C300-UHIO_con")
    getLaborContainerData(cbCEtoC300UHIOCon,"CBEC")

    xPMCon = getContainer(Product, "MSID_Labor_xPM_to_C300_Migration_Con")
    getLaborContainerData(xPMCon,"XPM C300")

    fscCon = getContainer(Product, "MSID_Labor_FSC_to_SM_con")
    getLaborContainerData(fscCon,"FSC_to_SM")

    fscauditCon = getContainer(Product, "MSID_Labor_FSC_to_SM_audit_Con")
    getLaborContainerData(fscauditCon,"FSC_to_SM_audit")

    fdmCon = getContainer(Product, "MSID_Labor_FDM_Upgrade_Con")
    getLaborContainerData(fdmCon,"FDM_Upgrade")

    LMCon = getContainer(Product, "MSID_Labor_LM_to_ELMM_Con")
    getLaborContainerData(LMCon,"LMTOELMM")

    XP10con = getContainer(Product, "MSID_Labor_XP10_Actuator_Upgrade_con")
    getLaborContainerData(XP10con,"XP10_Actuator")

    GraphicsCon = getContainer(Product, "MSID_Labor_Graphics_Migration_con")
    getLaborContainerData(GraphicsCon,"Graphics_Migration")

    CWSRAECon = getContainer(Product, "MSID_Labor_CWS_RAE_Upgrade_con")
    getLaborContainerData(CWSRAECon,"CWS_RAE_Upgrade")

    fscsmioCon = getContainer(Product, "MSID_Labor_FSCtoSM_IO_con")
    getLaborContainerData(fscsmioCon,"FSCtoSM_IO")
    
    fscsmioauditCon = getContainer(Product, "MSID_Labor_FSC_to_SM_IO_Audit_Con")
    getLaborContainerData(fscsmioauditCon,"FSCtoSM_IO_AUDIT")
    
    CDActuatorCon = getContainer(Product, "MSID_Labor_CD_Actuator_con")
    getLaborContainerData(CDActuatorCon,"CD_Actuator_IF_Upgrade")
    
    gs1Con = getContainer(Product, "MSID_Labor_Generic_System1_Cont")
    getLaborContainerData(gs1Con,"GS_Migration_1")

    gs2Con = getContainer(Product, "MSID_Labor_Generic_System2_Cont")
    getLaborContainerData(gs2Con,"GS_Migration_2")
    gs3Con = getContainer(Product, "MSID_Labor_Generic_System3_Cont")
    getLaborContainerData(gs3Con,"GS_Migration_3")
    gs4Con = getContainer(Product, "MSID_Labor_Generic_System4_Cont")
    getLaborContainerData(gs4Con,"GS_Migration_4")
    gs5Con = getContainer(Product, "MSID_Labor_Generic_System5_Cont")
    getLaborContainerData(gs5Con,"GS_Migration_5")

    VirtCon = getContainer(Product, "MSID_Labor_Virtualization_con")
    getLaborContainerData(VirtCon,"Virtualization_System_Migration")
    
    QCSCon = getContainer(Product, "MSID_Labor_QCS_RAE_Upgrade_con")
    getLaborContainerData(QCSCon,"QCS_RAE_Upgrade")

    TPACon = getContainer(Product, "MSID_Labor_TPA_con")
    getLaborContainerData(TPACon,"TPA/PMD_Migration")

     # Extended Logic for Labor Part summary ELEPIU Module -- Dipak Shekokar : CXCPQ-60173
    ELEPIUCon = getContainer(Product, "MSID_Labor_ELEPIU_con")
    getLaborContainerData(ELEPIUCon,"ELEPIU_ControlEdge_RTU_Migration_Engineering")

    projectManagementCon = getContainer(Product, "MSID_Labor_Project_Management")
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
sparePartsCabinetDict = populateSparePartCabinetSummary(Product, partsList)
partNumbersToBeAdded["Spare Parts"] = sparePartsCabinetDict
Trace.Write(RestClient.SerializeToJson(partNumbersToBeAdded))

containerNameMapping = {
    "OPM": getContainer(Product, "MSID_OPM_Added_Parts_Common_Container"),
    "LCN": getContainer(Product, "MSID_LCN_Added_Parts_Common_Container"),
    "NONSESP": getContainer(Product, "MSID_NON_SESP_Added_Parts_Common_Container"),
    "EBR": getContainer(Product, "MSID_EBR_Added_Parts_Common_Container"),
    "ELCN": getContainer(Product, "MSID_ELCN_Added_Parts_Common_Container"),
    "PM": getContainer(Product, "MSID_PM_Added_Parts_Common_Container"),
    "Orion_Console": getContainer(Product, "MSID_Orion_Console_Added_Parts_Common_Container"),
    "EHPM/EHPMX/ C300PM": getContainer(Product, "MSID_EHPM_C300PM_Added_Parts_Common_Container"),
    "TPS_EXP": getContainer(Product, "MSID_TPS_EXP_Added_Parts_Common_Container"),
    "TCMI": getContainer(Product, "MSID_TCMI_Added_Parts_Common_Container"),
    "LMTOELMM": getContainer(Product, "MSID_LM_TO_ELMM_Added_Parts_Common_Container"),
    "Spare Parts": getContainer(Product, "MSID_Spare_Parts_Added_Parts_Common_Container"),
    "EHPMHART": getContainer(Product, "MSID_EHPM_HART_IO_Added_Parts_Common_Container"),
    "C200 Migration": getContainer(Product, "MSID_C200_Migration_Added_Parts_Common_Container"),
    "CBEC": getContainer(Product, "MSID_CB_EC_Added_Parts_Common_Container"),
    "XPM C300": getContainer(Product, "MSID_xPM_C300_Added_Parts_Common_Container"),
    "FDM_Upgrade": getContainer(Product, "MSID_FDM_Upgrade_Added_Parts_Common_Container"),
    "FSC_to_SM": getContainer(Product, "MSID_FSC_to_SM_Added_Parts_Common_Container"),
    "FSC_to_SM_audit": getContainer(Product, "MSID_FSC_to_SM_audit_Added_Parts_Common_Container"),
    "THIRD_PARTY" : getContainer(Product, "MSID_Third_Party_Added_Parts_Common_Container"),
    "XP10_Actuator": getContainer(Product, "MSID_XP10_Actuator_Added_Parts_Common_Container"),
    "CWS_RAE_Upgrade": getContainer(Product, "MSID_CWS_RAE_Upgrade_Added_Parts_Common_Container"),
    "Graphics_Migration": getContainer(Product, "MSID_Graphics_Added_Parts_Common_Container"),
    "FSCtoSM_IO": getContainer(Product, "MSID_FSCtoSM_IO_Added_Parts_Common_Container"),
    "CD_Actuator_IF_Upgrade": getContainer(Product, "MSID_CD_Actuator_Added_Parts_Common_Container"),
    "3rd_Party_PLC_to_ControlEdge_PLC/UOC": getContainer(Product, "MSID_Third_Party_PLC_Added_Parts_Common_Container"),
    "Virtualization_System_Migration": getContainer(Product, "MSID_Virtualization_Added_Parts_Common_Container"),
    "QCS_RAE_Upgrade": getContainer(Product, "MSID_QCS_Added_Parts_Common_Container"),
    "GS_Migration_1": getContainer(Product, "MSID_GS1_Added_Parts_Common_Container"),
    "GS_Migration_2": getContainer(Product, "MSID_GS2_Added_Parts_Common_Container"),
    "GS_Migration_3": getContainer(Product, "MSID_GS3_Added_Parts_Common_Container"),
    "GS_Migration_4": getContainer(Product, "MSID_GS4_Added_Parts_Common_Container"),
    "GS_Migration_5": getContainer(Product, "MSID_GS5_Added_Parts_Common_Container"),
    "FSCtoSM_IO_AUDIT": getContainer(Product, "MSID_FSCtoSM_IO_audit_Added_Parts_Common_Container"),
    "TPA/PMD_Migration": getContainer(Product, "MSID_TPA_Added_Parts_Common_Container"),
    # Extended Logic for Labor Part summary ELEPIU Module -- Dipak Shekokar : CXCPQ-60173
    "ELEPIU_ControlEdge_RTU_Migration_Engineering": getContainer(Product, "MSID_ELEPIU_Added_Parts_Common_Container")
}
partsList.add("EP-S08CAL")
partsList.add("EP-S04CAL")
partDetailsDict = getPartDetailDict(partsList)
opmUserInput = getUserInputMap(containerNameMapping["OPM"])
for product, parts in partNumbersToBeAdded.items():
    container = containerNameMapping[product]
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
if TargetExpRelease in ('R501','R510','R511','R520'):
    if Qty != "0":
        row = container.AddNewRow(False)
        row['PartNumber'] = "EP-S04CAL"
        row['Quantity']  = Qty
        adjQty = 0
        comment = ''
        if opmUserInput.get(part):
            adjQty = getFloat(opmUserInput[part]['adjQty'])
            comment = userInputMap[part]['comment']
        row['Adj Quantity'] = str(adjQty)
        row['Final Quantity'] = str(getFloat(qty) + adjQty)
        row['Comments'] = comment
        if partDetailsDict.get("EP-S04CAL"):
            row['PartDescription'] = partDetailsDict["EP-S04CAL"][0]
            row['PLSG'] = partDetailsDict["EP-S04CAL"][1]
            row['plsgDescription'] = partDetailsDict["EP-S04CAL"][2]

elif TargetExpRelease in ('R432'):
    if Qty != "0":
        row = container.AddNewRow(False)
        row['PartNumber'] = "EP-S08CAL"
        row['Quantity']  = Qty
        adjQty = 0
        comment = ''
        if opmUserInput.get(part):
            adjQty = getFloat(opmUserInput[part]['adjQty'])
            comment = userInputMap[part]['comment']
        row['Adj Quantity'] = str(adjQty)
        row['Final Quantity'] = str(getFloat(qty) + adjQty)
        row['Comments'] = comment
        if partDetailsDict.get("EP-S08CAL"):
            row['PartDescription'] = partDetailsDict["EP-S08CAL"][0]
            row['PLSG'] = partDetailsDict["EP-S08CAL"][1]
            row['plsgDescription'] = partDetailsDict["EP-S08CAL"][2]

container.Calculate()
x = log_dict(attributeValueDict)