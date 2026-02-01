import math

def getContainer(prod, conName):
    return prod.GetContainerByName(conName)

def getFloat(var):
    if var:
        return float(var)
    return 0

def getValue(row, col):
    if col.IsProductAttribute and col.ReferencingAttribute and col.ReferencingAttribute.SelectedValue:
        val = col.ReferencingAttribute.SelectedValue.Display
        if not val:
            val = col.DisplayValue
            if not val:
                val = row[col.Name] if row[col.Name] else ""
        return val
    if col.DisplayType == "DropDown":
        val = col.DisplayValue
        if not val:
            val = row[col.Name] if row[col.Name] else ""
        return val
    if col.DisplayType == "TextBox":
        return col.Value
    if col.DisplayType == "Label":
        return col.Value
    return ""

def updateStandAloneAttributesDict(product, attributesMapping, attributeValueDict):
    for attrName in attributesMapping:
        colName = attributesMapping[attrName]
        attrValue = product.Attr(attrName).GetValue()
        attributeValueDict[colName] = attrValue

def updateContainerDetails(product, containerNames, attributeValueDict):
    for containerName in containerNames:
        container = getContainer(product, containerName)
        if container:
            row = container.Rows[0]
            for col in row.Columns:
                attributeValueDict[col.Name] = getValue(row, col)
        elif containerName == 'ELCN_Network_Gateway_Upgrade':
            attributesMapping = {
                'ELCN_Select_Switch_configuration_required': 'ELCN_Select_Switch_configuration_required',
                'ATT_ELCN_Qty_of_NGs_more_than_100mts': 'ELCN_Qty_of_NGs_more_than_100mts_from_existing_fiber_concentrators',
                'ELCN_Select_type_of_fiber_optic_switch': 'ELCN_Select_type_of_fiber_optic_switch'
            }
            updateStandAloneAttributesDict(product, attributesMapping, attributeValueDict)
        elif containerName == 'ELCN_Server_Cabinet_Configuration':
            attributesMapping = {
                'ELCN_Cabinet_Depth_Size': 'ELCN_Cabinet_Depth_Size',
                'ELCN_Power_Supply_Voltage': 'ELCN_Power_Supply_Voltage',
                'ELCN_Cabinet_Door_Type': 'ELCN_Cabinet_Door_Type',
                'ELCN_Cabinet_Keylock_Type': 'ELCN_Cabinet_Keylock_Type',
                'ELCN_Cabinet_Hinge_Type': 'ELCN_Cabinet_Hinge_Type',
                'ELCN_Cabinet_Thermostat_Required': 'ELCN_Cabinet_Thermostat_Required',
                'ELCN_Cabinet_Base_Required': 'ELCN_Cabinet_Base_Required',
                'ELCN_Cabinet_Color': 'ELCN_Cabinet_Color'
            }
            updateStandAloneAttributesDict(product, attributesMapping, attributeValueDict)

def getELCNTotalSum(attrValDict, keys, prefix):
    total = 0
    for key in keys:
        total += getFloat(attrValDict[prefix + "_" + key])
    return total

def updateAttributeWithCustomELCNValues(prod, attrDict):
    attrDict["Total_Upgrade"] = 0
    attrDict["Total_Upgrade_Virtual"] = 0
    attrDict["Total_New"] = 0
    attrDict["Total_New_Virtual"] = 0
    updateContainerDetails(prod, ["ELCN_Basic_Information", "ELCN_Network_Gateway_Upgrade", "ELCN_Server_Cabinet_Configuration"], attrDict)
    container = getContainer(prod, "ELCN_Upgrade_New_ELCN_Nodes")
    for row in container.Rows:
        if row.RowIndex == 0:
            customKey = "Upgrade_Physical"
        elif row.RowIndex == 1:
            customKey = "Upgrade_Virtual"
        elif row.RowIndex == 3:
            customKey = "New_Physical"
        elif row.RowIndex == 4:
            customKey = "New_Virtual"
        else:
            continue
        total = 0
        for col in row.Columns:
            try:
                total += float(getValue(row, col))
                attrDict[customKey + "_" + col.Name] = float(getValue(row, col))
            except:
                attrDict[customKey + "_" + col.Name] = 0
                pass
        attrDict["Total_" + customKey] = total
    attrDict["Total_Upgrade"] = getELCNTotalSum(
        attrDict,
        [
            "ELCN_Qty_of_ESTs",
            "ELCN_Qty_of_ACE_Ts",
            "ELCN_Qty_of_EAPPs",
            "ELCN_Qty_of_HMs",
            "ELCN_Qty_of_Non_Redundant_ESVTs",
            "ELCN_Qty_of_Non_redundant_AMs",
            "ELCN_Qty_of_Non_Redundant_HGs",
            "ELCN_Qty_of_Non_Redundant_EHBs",
            "ELCN_Qty_of_Non_Redundant_NIMs",
            "ELCN_Qty_of_Non_Redundant_ENIMs",
            "ELCN_Qty_of_Non_Redundant_xPLCGs",
            "ELCN_Qty_of_Network_Gateways",
            "ELCN_Qty_of_Redundant_ESVTs",
            "ELCN_Qty_of_Redundant_ESVTs",
            "ELCN_Qty_of_Redundant_AMs",
            "ELCN_Qty_of_Redundant_AMs",
            "ELCN_Qty_of_Redundant_HGs",
            "ELCN_Qty_of_Redundant_HGs",
            "ELCN_Qty_of_Redundant_EHBs",
            "ELCN_Qty_of_Redundant_EHBs",
            "ELCN_Qty_of_Redundant_NIMs",
            "ELCN_Qty_of_Redundant_NIMs",
            "ELCN_Qty_of_Redundant_ENIMs",
            "ELCN_Qty_of_Redundant_ENIMs",
            "ELCN_Qty_of_Redundant_xPLCGs",
            "ELCN_Qty_of_Redundant_xPLCGs",
        ],
        "Upgrade_Physical"
    )
    attrDict['Total_Upgrade'] += getELCNTotalSum(
        attrDict,
        [
            "ELCN_Qty_of_ESTs",
            "ELCN_Qty_of_ACE_Ts",
            "ELCN_Qty_of_EAPPs",
            "ELCN_Qty_of_HMs",
            "ELCN_Qty_of_Non_Redundant_ESVTs",
            "ELCN_Qty_of_Non_redundant_AMs",
            "ELCN_Qty_of_Non_Redundant_HGs",
            "ELCN_Qty_of_Non_Redundant_EHBs",
            "ELCN_Qty_of_Non_Redundant_NIMs",
            "ELCN_Qty_of_Non_Redundant_ENIMs",
            "ELCN_Qty_of_Non_Redundant_xPLCGs",
            "ELCN_Qty_of_Network_Gateways",
            "ELCN_Qty_of_Redundant_ESVTs",
            "ELCN_Qty_of_Redundant_ESVTs",
            "ELCN_Qty_of_Redundant_AMs",
            "ELCN_Qty_of_Redundant_AMs",
            "ELCN_Qty_of_Redundant_HGs",
            "ELCN_Qty_of_Redundant_HGs",
            "ELCN_Qty_of_Redundant_EHBs",
            "ELCN_Qty_of_Redundant_EHBs",
            "ELCN_Qty_of_Redundant_NIMs",
            "ELCN_Qty_of_Redundant_NIMs",
            "ELCN_Qty_of_Redundant_ENIMs",
            "ELCN_Qty_of_Redundant_ENIMs",
            "ELCN_Qty_of_Redundant_xPLCGs",
            "ELCN_Qty_of_Redundant_xPLCGs",
        ],
        "Upgrade_Virtual"
    )
    attrDict["EP_ZLCN10"] = math.floor(attrDict["Total_Upgrade"] / 10)
    attrDict["EP_ZLCN05"] = math.floor((attrDict["Total_Upgrade"] - (attrDict["EP_ZLCN10"] * 10)) / 5)
    attrDict["Total_New"] = getELCNTotalSum(
        attrDict,
        [
            "ELCN_Qty_of_HMs",
            "ELCN_Qty_of_Non_redundant_AMs",
            "ELCN_Qty_of_Non_Redundant_EHBs",
            "ELCN_Qty_of_Non_Redundant_ENIMs",
            "ELCN_Qty_of_Network_Gateways",
            "ELCN_Qty_of_Redundant_AMs",
            "ELCN_Qty_of_Redundant_AMs",
            "ELCN_Qty_of_Redundant_EHBs",
            "ELCN_Qty_of_Redundant_EHBs",
            "ELCN_Qty_of_Redundant_ENIMs",
            "ELCN_Qty_of_Redundant_ENIMs"
        ],
        "New_Physical"
    )
    attrDict["Total_New"] += getELCNTotalSum(
        attrDict,
        [
            "ELCN_Qty_of_HMs",
            "ELCN_Qty_of_Non_redundant_AMs",
            "ELCN_Qty_of_Non_Redundant_EHBs",
            "ELCN_Qty_of_Non_Redundant_ENIMs",
            "ELCN_Qty_of_Network_Gateways",
            "ELCN_Qty_of_Redundant_AMs",
            "ELCN_Qty_of_Redundant_AMs",
            "ELCN_Qty_of_Redundant_EHBs",
            "ELCN_Qty_of_Redundant_EHBs",
            "ELCN_Qty_of_Redundant_ENIMs",
            "ELCN_Qty_of_Redundant_ENIMs"
        ],
        "New_Virtual"
    )
    attrDict["EP_LCN010"] = math.floor(attrDict["Total_New"] / 10)
    attrDict["EP_LCN005"] = math.floor((attrDict["Total_New"] - (attrDict["EP_LCN010"] * 10)) / 5)
    attrDict["Total_Upgrade_Virtual"] = getELCNTotalSum(
        attrDict,
        [
            "ELCN_Qty_of_Non_redundant_AMs",
            "ELCN_Qty_of_Non_Redundant_HGs",
            "ELCN_Qty_of_Non_Redundant_EHBs",
            "ELCN_Qty_of_Non_Redundant_NIMs",
            "ELCN_Qty_of_Non_Redundant_ENIMs",
            "ELCN_Qty_of_Network_Gateways",
            "ELCN_Qty_of_Redundant_AMs",
            "ELCN_Qty_of_Redundant_AMs",
            "ELCN_Qty_of_Redundant_HGs",
            "ELCN_Qty_of_Redundant_HGs",
            "ELCN_Qty_of_Redundant_EHBs",
            "ELCN_Qty_of_Redundant_EHBs",
            "ELCN_Qty_of_Redundant_NIMs",
            "ELCN_Qty_of_Redundant_NIMs",
            "ELCN_Qty_of_Redundant_ENIMs",
            "ELCN_Qty_of_Redundant_ENIMs"
        ],
        "Upgrade_Virtual"
    )
    attrDict["EP_ZLCV10"] = math.floor(attrDict["Total_Upgrade_Virtual"] / 10)
    attrDict["EP_ZLCV05"] = math.floor((attrDict["Total_Upgrade_Virtual"] - (attrDict["EP_ZLCV10"] * 10)) / 5)
    attrDict["Total_New_Virtual"] = getELCNTotalSum(
        attrDict,
        [
            "ELCN_Qty_of_HMs",
            "ELCN_Qty_of_Non_redundant_AMs",
            "ELCN_Qty_of_Non_Redundant_EHBs",
            "ELCN_Qty_of_Non_Redundant_ENIMs",
            "ELCN_Qty_of_Network_Gateways",
            "ELCN_Qty_of_Redundant_AMs",
            "ELCN_Qty_of_Redundant_AMs",
            "ELCN_Qty_of_Redundant_EHBs",
            "ELCN_Qty_of_Redundant_EHBs",
            "ELCN_Qty_of_Redundant_ENIMs",
            "ELCN_Qty_of_Redundant_ENIMs"
        ],
        "New_Virtual"
    )
    attrDict["EP_LCNV10"] = math.floor(attrDict["Total_New_Virtual"] / 10)
    attrDict["EP_LCNV05"] = math.floor((attrDict["Total_New_Virtual"] - (attrDict["EP_LCNV10"] * 10)) / 5)
    attrDict["EH_UMT020"] = 0
    if attrDict["ELCN_Type_of_Cabinet_to_Install_the_Physical_nodes"] == "Server Cabinet":
        listUMT020 = ["Upgrade_Physical_ELCN_Qty_of_Non_redundant_AMs","Upgrade_Physical_ELCN_Qty_of_Non_Redundant_HGs","Upgrade_Physical_ELCN_Qty_of_Non_Redundant_EHBs","Upgrade_Physical_ELCN_Qty_of_Non_Redundant_ETN_EHBs","Upgrade_Physical_ELCN_Qty_of_Non_Redundant_NIMs","Upgrade_Physical_ELCN_Qty_of_Non_Redundant_ENIMs","Upgrade_Physical_ELCN_Qty_of_Network_Gateways","Upgrade_Physical_ELCN_Qty_of_Redundant_AMs","Upgrade_Physical_ELCN_Qty_of_Redundant_HGs","Upgrade_Physical_ELCN_Qty_of_Redundant_EHBs","Upgrade_Physical_ELCN_Qty_of_Redundant_ETN_EHBs","Upgrade_Physical_ELCN_Qty_of_Redundant_NIMs","Upgrade_Physical_ELCN_Qty_of_Redundant_ENIMs","Upgrade_Physical_ELCN_Qty_of_Redundant_ETN_ENIMs","Upgrade_Physical_ELCN_Qty_of_Network_Gateways","New_Physical_ELCN_Qty_of_Non_redundant_AMs","New_Physical_ELCN_Qty_of_Non_Redundant_EHBs","New_Physical_ELCN_Qty_of_Non_Redundant_ENIMs","New_Physical_ELCN_Qty_of_Network_Gateways","New_Physical_ELCN_Qty_of_Redundant_AMs","New_Physical_ELCN_Qty_of_Redundant_EHBs","New_Physical_ELCN_Qty_of_Redundant_ENIMs","New_Physical_ELCN_Qty_of_Network_Gateways"]
        for col in listUMT020:
            attrDict["EH_UMT020"] += attrDict[col]
    if attrDict["ELCN_Type_of_Cabinet_where_the_ELCN_Bridge"] in ["In Existing Server Cabinet",  "In New Server cabinet"] and attrDict["ELCN_If_ELCN_Bridge_is_not_present_in_LCN"] != "Nothing - ELCN Bridge is present":
        attrDict["EH_UMT020"] += 1
    fiber = getFloat(attrDict["ELCN_Qty_of_NGs_more_than_100mts_from_existing_fiber_concentrators"])
    switchConfig = attrDict["ELCN_Select_Switch_configuration_required"]
    attrDict["SI_930SN4"] = 0
    if fiber > 0:
        if switchConfig == "Responsible - Alternate configuration":
            attrDict["SI_930SN4"] = 2
        elif switchConfig == "Non Responsible - Alternate configuration":
            attrDict["SI_930SN4"] = 1

def GetPartNumberDict():
    partNumberdict = {"OPM":"OPM","LCN One Time Upgrade":"LCN","Non-SESP Exp Upgrade":"NONSESP","EBR":"EBR","ELCN":"ELCN","PM":"PM","Orion Console":"Orion_Console","EHPM/EHPMX/ C300PM":"EHPM/EHPMX/ C300PM","TPS to Experion":"TPS_EXP","TCMI":"TCMI","LM to ELMM ControlEdge PLC":"LMTOELMM","Spare Parts":"Spare Parts","EHPM HART IO":"EHPMHART","C200 Migration":"C200 Migration","CB-EC Upgrade to C300-UHIO":"CBEC","xPM to C300 Migration":"XPM C300","FDM Upgrade 1":"FDM_Upgrade","FDM Upgrade 2":"FDM_Upgrade_2","FDM Upgrade 3":"FDM_Upgrade_3","FSC to SM":"FSC_to_SM","FSC_to_SM_audit":"FSC_to_SM_audit","THIRD_PARTY":"THIRD_PARTY","XP10 Actuator Upgrade":"XP10_Actuator","CWS RAE Upgrade":"CWS_RAE_Upgrade","Graphics Migration":"Graphics_Migration","FSC to SM IO Migration":"FSCtoSM_IO","FSCtoSM_IO_AUDIT":"FSCtoSM_IO_AUDIT","CD Actuator I-F Upgrade":"CD_Actuator_IF_Upgrade","3rd Party PLC to ControlEdge PLC/UOC":"3rd_Party_PLC_to_ControlEdge_PLC/UOC","Virtualization System Migration":"Virtualization_System_Migration","QCS RAE Upgrade":"QCS_RAE_Upgrade","GS_Migration_1":"GS_Migration_1","GS_Migration_2":"GS_Migration_2","GS_Migration_3":"GS_Migration_3","GS_Migration_4":"GS_Migration_4","GS_Migration_5":"GS_Migration_5","TPA/PMD Migration":"TPA/PMD_Migration","ELEPIU ControlEdge RTU Migration Engineering":"ELEPIU_ControlEdge_RTU_Migration_Engineering"}

    return partNumberdict