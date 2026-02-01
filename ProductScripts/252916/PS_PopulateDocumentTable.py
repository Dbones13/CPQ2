def getContainer(product, name):
    return product.GetContainerByName(name)


def updateAttributeDict(container, msidAttributeDict):
    if container.Name == "ELCN_Upgrade_New_ELCN_Nodes":
        suffixList = [
            "_Upgrade_Physical",
            "_Upgrade_Virtual",
            "",
            "_New_Physical",
            "_New_Virtual",
        ]
        for row in filter(lambda r: r.RowIndex != 2 and  r.RowIndex < 5, container.Rows):
            for col in row.Columns:
                val = getValue(col,row)
                msidAttributeDict[col.Name + suffixList[row.RowIndex]] = val if val else 0
        return
    for row in container.Rows:
        for col in row.Columns:
            if str(container.Name) in('Orion_Services','MSID_CommonQuestions','xPM_Services_Cont') and col.Name == 'MSID_Will_Honeywell_perform_equipment_installation':
                pdt=Product.Attr("MSID_Selected_Products").GetValue()
                if "EHPM/EHPMX/ C300PM" in pdt and str(col.DisplayValue) in ('Yes','No') and str(container.Name) in('xPM_Services_Cont'):
                    msidAttributeDict[col.Name] = getValue(col,row)
                elif "Orion Console" in pdt and str(col.DisplayValue) in ('Yes','No') and str(container.Name) in('Orion_Services'):
                    msidAttributeDict[col.Name] = getValue(col,row)
            else:
                msidAttributeDict[col.Name] = getValue(col,row)
            # msidAttributeDict[col.Name] = getValue(col,row)
        break
    if container.Name == "OPM_Node_Configuration":
        for row in container.Rows:
            if row.RowIndex == 2:
                for col in row.Columns:
                    msidAttributeDict[col.Name + "_HW_Replace"] = getValue(col,row)
                break
    if msidAttributeDict.get("OPM_Is_this_is_a_Remote_Migration_Service_RMS") is not None and msidAttributeDict.get("OPM_Is_this_is_a_Remote_Migration_Service_RMS") == '':
        msidAttributeDict["OPM_Is_this_is_a_Remote_Migration_Service_RMS"] = "No"


def updateMultilineAttributeDict(container, msidAttributeDict):
    for row in container.Rows:
        for col in row.Columns:
            shouldDelete = msidAttributeDict.get(col.Name+"_delete",True)
            val = getValue(col,row)
            if val not in ('','0',"None","No",0,None,"Yes - Local and Remote","Yes - Only Remote"):
                shouldDelete = False
            msidAttributeDict[col.Name+"_delete"] = shouldDelete
            l = msidAttributeDict.get(col.Name,list())
            l.append(getValue(col,row))
            msidAttributeDict[col.Name] = l



def updateMultilineAttributeDict_fsc(container, msidAttributeDict):
    for row in container.Rows:
        for col in row.Columns:
            shouldDelete_fsc = msidAttributeDict.get(col.Name+"_delete",1)
            val = getValue(col,row)
            if val not in ('','0'):
                shouldDelete_fsc = 0
            msidAttributeDict[col.Name+"_delete"] = shouldDelete_fsc
            l = msidAttributeDict.get(col.Name,list())
            l.append(getValue(col,row))
            msidAttributeDict[col.Name] = l

def populateQuoteTableIAA(guid, attr, attr_value, table, msid_esids=''):
    row = table.AddNewRow()
    row["MSID_GUID"] = guid
    row["Attribute"] = attr
    row['Item_Number'] = msid_esids
    row["Attribute_Value"] = ",".join(attr_value) if str(type(attr_value)) == "<type 'list'>" else str(attr_value)

def populateQuoteTable(guid, dataDict, table):

    for key, value in dataDict.items():
        row = table.AddNewRow()
        row["MSID_GUID"] = guid
        row["Attribute"] = key
        row["Attribute_Value"] = ",".join(value) if str(type(value)) == "<type 'list'>" else str(value)


def getValue(col,row):
    if col.DisplayType == "DropDown":
        if col.DisplayValue != '':
            return col.DisplayValue
        return row[col.Name]
    if col.DisplayType == "TextBox":
        if col.DataType == "Number" and col.Value == "":
            return "0"
        return col.Value
    return ""


def populateMsidAttributes(product):
    msidAttributeDict = dict()

    attributeContianers = [
        "Orion_Services",
        "MSID_CommonQuestions",
        "LCN_Design_Inputs_for_TPN_OTU_Upgrade",
        "NONSESP_Design_Inputs_for_Experion_Upgrade_License",
        "NONSESP_Design_Inputs_for_eServer_Upgrade_License",
        "OPM_Basic_Information",
        "OPM_Node_Configuration",
        "OPM_Migration_platforms",
        "OPM_FTE_Switches_migration_info",
        "OPM_Services",
        "EBR_Basic_Information",
        "EBR_Upgrade",
        "EBR_New_Additional_EBR",
        "EBR_Hardware_to_Host_EBR_Physical_Node_Only",
        "EBR_Services",
        "ELCN_Basic_Information",
        "ELCN_Network_Gateway_Upgrade",
        "ELCN_Server_Cabinet_Configuration",
        "ELCN_Services",
        "ELCN_Upgrade_New_ELCN_Nodes",
        "xPM_Migration_Scenario_Cont",
        "xPM_Services_Cont",
        "xPM_Migration_General_Qns_Cont",
        "xPM_Network_Upgrade_Cont",
        "ENB_Migration_General_Qns_Cont",
        "TPS_EX_Conversion_ESVT_Server",
        "TPS_EX_Bundle_Conversion_Server_Stations",
        "TPS_EX_General_Questions",
        "TPS_EX_Service",
        "Orion_General_Information_Container2",
        "TCMI_Hardware_and_Licenses",
        "TCMI_Services",
        "TCMI_General_Information",
        "EHPM_HART_IO_General_Qns_Cont",
        "EHPM_HART_IO_Services_Cont",
        "C200_Migration_General_Qns_Cont",
        "C200_Migration_Scenario_Cont",
        "C200_Services_1_Cont",
        "C200_Services_2_Cont",
        "xPM_Migration_General_Qns_Cont",
        "CB_EC_migration_to_C300_UHIO_Configuration_Cont",
        "CB_EC_Services_1_Cont",
        "CB_EC_Services_2_Cont",
        "xPM_C300_Services_Cont",
        "xPM_C300_General_Qns_Cont",
        "FSC_to_SM_Services",
        "FSC_to_SM_General_Information",
        "xPM_C300_General_Qns_Cont",
        "FDM_Upgrade_General_questions",
        "FDM_Upgrade_Services",
        "LM_to_ELMM_ControlEdge_PLC_Migration_Gen_Cont",
        "LM_to_ELMM_Services",
        "FSC_to_SM_IO_Migration_General_Information",
        "Graphics_Migration_Migration_Scenario",
        "Graphics_Migration_Training_Testing_Documentation",
        "Graphics_Migration_Additional_Questions",
        "XP10_Actuator_General_Information",
        "FSC_to_SM_IO_Migration_General_Information",
        "FSC_to_SM_IO_New_SM_Cabinet_Configuration",
        "FSC_to_SM_IO_Services",
        "CD_Actuator_IF_Upgrade_General_Info_Cont",
        "CD_Actuator_IF_Upgrade_Services_Cont"
    ]
    multilineContainer = [
        "ENB_Migration_Config_Cont",
        "xPM_Migration_Config_Cont",
        "TPS_EX_Station_Conversion_EST",
        "TPS_EX_Additional_Servers",
        "TPS_EX_Additional_Stations",
        "TPS_EX_Conversion_ACET_EAPP",
        "Orion_Station_Configuration",
        "EHPM_HART_IO_Configuration_Cont",
        "C200_Migration_Config_Cont",
        "FSC_to_SM_Configuration",
        "FDM_Upgrade_Configuration",
        "FDM_Upgrade_Additional_Configuration",
        "LM_to_ELMM_Migration_Additional_IO_Cont",
        "LM_to_ELMM_ControlEdge_PLC_Cont",
        "LM_to_ELMM_ControlEdge_PLC_Remote_IO_Cont",
        "LM_to_ELMM_ControlEdge_PLC_Local_IO_Cont",
        "FDM_Upgrade_Hardware_to_host_FDM_Server",
        "xPM_C300_Migration_Configuration_Cont",
        "Graphics_Migration_Displays_Shapes_Faceplates",
    ]
    
    multilineContainer_fsc = ["FSC_to_SM_IO_Series_1_&_2_FSC_IO_configurations"]

    for containerName in attributeContianers:
        container = getContainer(product, containerName)
        updateAttributeDict(container, msidAttributeDict)

    for containerName in multilineContainer:
        container = getContainer(product, containerName)
        updateMultilineAttributeDict(container, msidAttributeDict)

    for containerName in multilineContainer_fsc:
        container = getContainer(product, containerName)
        updateMultilineAttributeDict_fsc(container, msidAttributeDict)

        

    msidAttributeDict["MSID_Selected_Products"] = product.Attr(
        "MSID_Selected_Products"
    ).GetValue()
    msidAttributeDict["Migration_MSID_System_Number"] = product.Attr(
        "Migration_MSID_System_Number"
    ).GetValue()
    msidAttributeDict["OPM_Which_documentation_is_required"] = product.Attr(
        "OPM_Which_documentation_is_required"
    ).GetValue()
    msidAttributeDict["xPM_Which_documentation_is_required"] = product.Attr(
        "xPM_Which_documentation_is_required"
    ).GetValue()
    msidAttributeDict["TPS_EX_Which_Documentation_Required"] = product.Attr(
        "TPS_EX_Which_Documentation_Required"
    ).GetValue()
    msidAttributeDict["Orion_Which_documentation_is_required"] = product.Attr(
        "Orion_Which_documentation_is_required"
    ).GetValue()
    msidAttributeDict["EHPM_HART_IO_Which_documentation_is_required?"] = product.Attr(
        "EHPM_HART_IO_Which_documentation_is_required?"
    ).GetValue()
    msidAttributeDict["Migration_MSID_Choices"] = product.Attr(
        "Migration_MSID_Choices"
    ).GetValue()
    msidAttributeDict["xPM_C300_Which_Documentation_Required"] = product.Attr(
        "xPM_C300_Which_Documentation_Required"
    ).GetValue()
    msidAttributeDict["MIgration_Scope_Choices"] = product.Attr(
        "MIgration_Scope_Choices"
    ).GetValue()
    msidAttributeDict["FSC_to_SM_IO_Is_the_series_2_FTA_and_SIC_cable_reu"] = product.Attr(
        "FSC_to_SM_IO_Is_the_series_2_FTA_and_SIC_cable_reu"
    ).GetValue()
    msidAttributeDict["LM_to_ELMM_Local_Remote_Flag"] = product.Attr(
        "LM_to_ELMM_Local_Remote_Flag"
    ).GetValue()
    return msidAttributeDict
def DeleteQuoteTableItem(table):
    item_delete = []
    for row in table.Rows:
        if str(row['MIgration_GUID'])  == "": # exception for IAA -Project
            item_delete.append(row.Id)
    c=sorted(item_delete, reverse=True)
    for r in c:
        table.DeleteRow(r)
    table.Save()

msidCont = Product.GetContainerByName("Migration_MSID_Selection_Container")

msidAttributeDict = dict()
table = Quote.QuoteTables["Migration_Document_Data"]
#table.Rows.Clear()
parentItemGUID = ''
for i in arg.QuoteItemCollection:
    parentItemGUID = i.ParentItemGuid
DeleteQuoteTableItem(table)
for msidRow in msidCont.Rows:
    msidAttributeDict = populateMsidAttributes(msidRow.Product)
    x = RestClient.SerializeToJson (msidAttributeDict)
    #Trace.Write(RestClient.SerializeToJson (msidAttributeDict))
    populateQuoteTable(msidRow.UniqueIdentifier, msidAttributeDict, table)

    contIAA1 = getContainer(msidRow.Product, "IAA Inputs_Cont")
    for row in contIAA1.Rows:
        guid = msidRow.UniqueIdentifier
        msid_esid = row["IAA_List_individual_MSIDs/ESIDs"]
        attr = row["IAA_Assessment_Type"]
        attr_value = row["IAA_Quantity"]
        populateQuoteTableIAA(guid, attr, attr_value, table, msid_esid)

    contIAA2 = getContainer(msidRow.Product, "IAA Inputs_Cont_2")
    for row in contIAA2.Rows:
        guid = msidRow.UniqueIdentifier
        attr = row["Name"]
        attr_value = row["Quantity"]
        populateQuoteTableIAA(guid, attr, attr_value, table)

    contIAAprice = getContainer(msidRow.Product, "IAA Pricing")
    for row in contIAAprice.Rows:
        guid = msidRow.UniqueIdentifier
        attr = row["Name"]
        attr_value = row["Price"]
        populateQuoteTableIAA(guid, attr, attr_value, table)

table.Save()