########
#scriptDefinition:
#  id : 259
#  name: GS_MigrationPartsUtil
#  systemId: GS_MigrationPartsUtil_cpq
#  active : true
#  isModule : true
######


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


def updateAttrDictWithCustomOrion(product, attrValDict):
    con = getContainer(product, "Orion_Station_Configuration")
    for row in con.Rows:
        l = attrValDict.get("Orion_Left_Aux_Sum_0",list())
        l.append(str(getFloat(row["Orion_Number_of_Left_Auxiliary_Equipment_Unit"]) + getFloat(row["Orion_Number_of_Left_Extended_Auxiliary_Equipment_Unit"]) == 0).upper())
        attrValDict["Orion_Left_Aux_Sum_0"] = l

        l = attrValDict.get("Orion_Right_Aux_Sum_0",list())
        l.append(str(getFloat(row["Orion_Number_of_Right_Auxiliary_Equipment_Unit"]) + getFloat(row["Orion_Number_of_Right_Extended_Auxiliary_Equipment_Unit"]) == 0).upper())
        attrValDict["Orion_Right_Aux_Sum_0"] = l

        l = attrValDict.get("Orion_2_3_Position_Sum_1",list())
        l.append(str(getFloat(row["Orion_Number_of_2_Position_Base_Unit"]) + getFloat(row["Orion_Number_of_3_Position_Base_Unit"]) == 1).upper())
        attrValDict["Orion_2_3_Position_Sum_1"] = l

        l = attrValDict.get("Orion_2_Position_multiplier",list())
        l.append(1 if getFloat(row["Orion_Number_of_2_Position_Base_Unit"]) > 0 else 0)
        attrValDict["Orion_2_Position_multiplier"] = l

        l = attrValDict.get("Orion_3_Position_multiplier",list())
        l.append(1 if getFloat(row["Orion_Number_of_3_Position_Base_Unit"]) > 0 else 0)
        attrValDict["Orion_3_Position_multiplier"] = l


def updateAttrWithCustomTpsValues(product, attrValDict):
    numberOfSwitches = 0
    multiplier = 2 if attrValDict["TPS_EX_ESVT_Redundant"] == "Yes" else 1

    numberOfSwitches = (
        getFloat(attrValDict["TPS_EX_TDC_US_ESVT"]) +
        getFloat(attrValDict["TPS_EX_TDC_AM_ESVT"]) +
        getFloat(attrValDict["TPS_EX_TDC_APP_ESVT"]) +
        getFloat(attrValDict["TPS_EX_TDC_GUS_ESVT"]) +
        getFloat(attrValDict["TPS_EX_ESVT_WO_Trade_Ins"])
    ) * multiplier

    numberOfSwitches += sum([getFloat(x) for x in attrValDict["TPS_EX_Quantity"]])
    numberOfSwitches += sum([getFloat(x) for x in attrValDict["TPS_EX_Conversion_ACET_EAPP_Qty"]])

    attrValDict["TPS_EX_Tree_Qty"] = numberOfSwitches

    numberOfSwitches += 4 if attrValDict["TPS_EX_Non_Reduntant_Conversion_ESVT"] == "Yes" else 0
    numberOfSwitches += 5 if attrValDict["TPS_EX_Redundant_Conversion_ESVT"] == "Yes" else 0

    attrValDict["TPS_EX_Number_of_Switches"] = numberOfSwitches * 2

    for row in getContainer(product, "TPS_EX_Station_Conversion_EST").Rows:
        for col in row.Columns:
            attrValDict["{}_{}".format(col.Name, row["TPS_EX_Station_Conversion_Type"])] = getValue(row, col)

    for row in getContainer(product, "TPS_EX_Conversion_ACET_EAPP").Rows:
        for col in row.Columns:
            attrValDict["{}_{}".format(col.Name, row["TPS_EX_Conversion_ACET_EAPP_Type"])] = getValue(row, col)


    typeMap = {
        'Flex Station - Desk' : ['TPS_STAT01'],
        'Flex Station - Cabinet' : ['TPS_STAT01'],
        'Flex Station - Orion' : ['TPS_STAT01'],
        'Console Station - Desk': ['TPS_STAC01'],
        'Console Station - Cabinet': ['TPS_STAC01'],
        'Console Station - Orion': ['TPS_STAC01'],
        'ES-T Station - Desk' : ['TPS_STAC01', 'TPS_CONTPS'],
        'ES-T Station - Cabinet' : ['TPS_STAC01', 'TPS_CONTPS'],
        'ES-T Station - Orion' : ['TPS_STAC01', 'TPS_CONTPS']
    }

    attrValDict['TPS_STAT01'] = 0
    attrValDict['TPS_STAC01'] = 0
    attrValDict['TPS_CONTPS'] = 0

    for row in getContainer(product, "TPS_EX_Additional_Stations").Rows:
        sType = row["TPS_EX_Additional_Stations_Type"]
        licenseReqiured = row['TPS_EX_Additional_Stations_Station_License?'] == 'Yes'
        qty = row['TPS_EX_Additional_Stations_Quantity']
        if licenseReqiured and sType in typeMap:
            for m in typeMap[sType]:
                attrValDict[m] += int(qty)

    attrValDict['futureReleaseBelow520'] = str(True)
    if attrValDict['MSID_Future_Experion_Release'] in ("R520"):
        attrValDict["futureReleaseBelow520"] = str(False)

def updateContainerDetails(product, containerNames, attributeValueDict):
    for containerName in containerNames:
        container = getContainer(product, containerName)
        row = container.Rows[0]
        for col in row.Columns:
            attributeValueDict[col.Name] = getValue(row, col)

def updateAttributeWithCustomC200MigrationValues(product, attrValDict):
    con1 = getContainer(product, "C200_Migration_General_Qns_Cont")
    con2 = getContainer(product, "C200_Migration_Config_Cont")

    X1756EN2TRPoints_1 = 0
    RM2Points_1 = 0
    CN2RPoints_1 = 0
    TKFXX102Points_1 = 0
    TKFPCXX2Points_1 = 0
    X1756EN2TRPoints_2 = 0
    RM2Points_2 = 0
    CN2RPoints_2 = 0
    TKFXX102Points_2 = 0
    TKFPCXX2Points_2 = 0
    X1756EN2TRPoints_3 = 0
    RM2Points_3 = 0
    CN2RPoints_3 = 0
    TKFXX102Points_3 = 0
    TKFPCXX2Points_3 = 0
    X1756EN2TRPoints_4 = 0
    RM2Points_4 = 0
    CN2RPoints_4 = 0
    TKFXX102Points_4 = 0
    TKFPCXX2Points_4 = 0
    X1756EN2TRPoints_51 = 0
    RM2Points_51 = 0
    CN2RPoints_51 = 0
    TKFXX102Points_51 = 0
    TKFPCXX2Points_51 = 0
    X1756EN2TRPoints_52 = 0
    RM2Points_52 = 0
    CN2RPoints_52 = 0
    TKFXX102Points_52 = 0
    TKFPCXX2Points_52 = 0
    Qty900CP1 = 0
    Qty1756 = 0
    Points5103Parts = 0
    QtySI3300I2 = 0
    QtySI920LN8 = 0
    QtySI920LN4 = 0

    typeDownlink = con1.Rows[0]["C200_Type_of_downlink_communication_UOC"]
    providingFTECables = con1.Rows[0]["C200_Is_Honeywell_Providing_FTE_cables"]
    existingC200Server = con1.Rows[0]["C200_Connection _to_Experion_Server"]
    AvgCableLength = con1.Rows[0]["C200_Average_Cable_Length"]
    C200FTEexpServ = con1.Rows[0]["C200_FTE_Switch_to_connect_required_exp_servers"]  # empty
    TypeofUOC = con1.Rows[0]["C200_Type_of_UOC"]  # empty
    C200Peer = ""
    colocatedGroups = getFloat(con1.Rows[0]["C200_How_many_co_located_C200_groups_exists"])
    additionalSwitches = getFloat(con1.Rows[0]["C200_Number_of_additional_switches"])
    attrValDict["thirdpartycabinet"] = 0
    tempData = eval(product.Attr("Temporary Data").GetValue())

    for row in con2.Rows:
        currentThirdPartyCabinet = 0
        controllerRedundancy = row["C200_Controller_Redundancy"]
        noOf1765DIIOMs = getFloat(row["C200_Number_of_1756_DI_IOMs"])
        AIOControllerRacks = row["C200_Series_A_IO_in_Controller_Rack_Non-Redundant"]
        IORacks = getFloat(row["C200_UOC_Number_of_Series_A_IO_Racks"])
        CNISegments = row["C200_Number_of_CNI_segments"]
        if (typeDownlink == "CNET Redundant") and (controllerRedundancy == "Redundant" or controllerRedundancy == "") and (noOf1765DIIOMs > 32):
            X1756EN2TRPoints_1 += 4
            RM2Points_1 += 4
            if CNISegments == "1" or CNISegments == "":
                CNISegments = "1"
            CN2RPoints_1 += getFloat(CNISegments) * 4
            TKFXX102Points_1 += 2
            TKFPCXX2Points_1 += 2
            currentThirdPartyCabinet = 2
            Trace.Write("Yes 1")
            # attrDict["test"] = X1756EN2TRPoints_1
            attrValDict["X1756EN2TRPoints_1"] = X1756EN2TRPoints_1
            attrValDict["RM2Points_1"] = RM2Points_1
            attrValDict["CN2RPoints_1"] = CN2RPoints_1
            attrValDict["TKFXX102Points_1"] = TKFXX102Points_1
            attrValDict["TKFPCXX2Points_1"] = TKFPCXX2Points_1
        elif (typeDownlink == "CNET Redundant") and (controllerRedundancy == "Redundant" or controllerRedundancy == "") and (noOf1765DIIOMs <= 32):
            X1756EN2TRPoints_1 += 2
            RM2Points_1 += 2
            if CNISegments == "1" or CNISegments == "":
                CNISegments = "1"
            CN2RPoints_1 += getFloat(CNISegments) * 2
            Trace.Write("No 1")
            attrValDict["X1756EN2TRPoints_1"] = X1756EN2TRPoints_1
            attrValDict["RM2Points_1"] = RM2Points_1
            attrValDict["CN2RPoints_1"] = CN2RPoints_1
        if (typeDownlink == "CNET Redundant") and (controllerRedundancy == "Non Redundant") and (noOf1765DIIOMs > 32) and (AIOControllerRacks == "Yes"):
            X1756EN2TRPoints_2 += 4
            RM2Points_2 += 4
            if CNISegments == "1" or CNISegments == "":
                CNISegments = "1"
            CN2RPoints_2 += getFloat(CNISegments) * 4
            TKFXX102Points_2 += 4
            TKFPCXX2Points_2 += 4
            currentThirdPartyCabinet = 4
            attrValDict["X1756EN2TRPoints_2"] = X1756EN2TRPoints_2
            attrValDict["RM2Points_2"] = RM2Points_2
            attrValDict["CN2RPoints_2"] = CN2RPoints_2
            attrValDict["TKFXX102Points_2"] = TKFXX102Points_2
            attrValDict["TKFPCXX2Points_2"] = TKFPCXX2Points_2
            Trace.Write("Yes 2")
        elif (typeDownlink == "CNET Redundant") and (controllerRedundancy == "Non Redundant") and (noOf1765DIIOMs <= 32) and (AIOControllerRacks == "Yes"):
            X1756EN2TRPoints_2 += 2
            RM2Points_2 += 2
            if CNISegments == "1" or CNISegments == "":
                CNISegments = "1"
            CN2RPoints_2 += getFloat(CNISegments) * 2
            TKFXX102Points_2 += 2
            TKFPCXX2Points_2 += 2
            currentThirdPartyCabinet = 2
            Trace.Write("No 2")
            attrValDict["X1756EN2TRPoints_2"] = X1756EN2TRPoints_2
            attrValDict["RM2Points_2"] = RM2Points_2
            attrValDict["CN2RPoints_2"] = CN2RPoints_2
            attrValDict["TKFXX102Points_2"] = TKFXX102Points_2
            attrValDict["TKFPCXX2Points_2"] = TKFPCXX2Points_2
        if (typeDownlink == "CNET Redundant") and (controllerRedundancy == "Non Redundant") and (noOf1765DIIOMs > 32) and (AIOControllerRacks == "No" or AIOControllerRacks == ""):
            X1756EN2TRPoints_3 += 4
            RM2Points_3 += 4
            if CNISegments == "1" or CNISegments == "":
                CNISegments = "1"
            CN2RPoints_3 += getFloat(CNISegments) * 4
            TKFXX102Points_3 += 3
            TKFPCXX2Points_3 += 3
            currentThirdPartyCabinet = 3
            Trace.Write("Yes 3")
            attrValDict["X1756EN2TRPoints_3"] = X1756EN2TRPoints_3
            attrValDict["RM2Points_3"] = RM2Points_3
            attrValDict["CN2RPoints_3"] = CN2RPoints_3
            attrValDict["TKFXX102Points_3"] = TKFXX102Points_3
            attrValDict["TKFPCXX2Points_3"] = TKFPCXX2Points_3
        elif (typeDownlink == "CNET Redundant") and (controllerRedundancy == "Non Redundant") and (noOf1765DIIOMs <= 32) and (AIOControllerRacks == "No" or AIOControllerRacks == ""):
            X1756EN2TRPoints_3 += 2
            RM2Points_3 += 2
            if CNISegments == "1" or CNISegments == "":
                CNISegments = "1"
            CN2RPoints_3 += getFloat(CNISegments) * 2
            TKFXX102Points_3 += 1
            TKFPCXX2Points_3 += 1
            currentThirdPartyCabinet = 1
            Trace.Write("No 3")
            attrValDict["X1756EN2TRPoints_3"] = X1756EN2TRPoints_3
            attrValDict["RM2Points_3"] = RM2Points_3
            attrValDict["CN2RPoints_3"] = CN2RPoints_3
            attrValDict["TKFXX102Points_3"] = TKFXX102Points_3
            attrValDict["TKFPCXX2Points_3"] = TKFPCXX2Points_3
        if (typeDownlink == "CNET Non-Redundant") and (controllerRedundancy == "Redundant" or controllerRedundancy == "") and (noOf1765DIIOMs > 32):
            X1756EN2TRPoints_4 += 2
            if CNISegments == "1" or CNISegments == "":
                CNISegments = "1"
            CN2RPoints_4 += getFloat(CNISegments)
            attrValDict["X1756EN2TRPoints_4"] = X1756EN2TRPoints_4
            attrValDict["CN2RPoints_4"] = CN2RPoints_4
            Trace.Write("Yes 4")
        elif (typeDownlink == "CNET Non-Redundant") and (controllerRedundancy == "Redundant" or controllerRedundancy == "") and (noOf1765DIIOMs <= 32):
            X1756EN2TRPoints_4 += 1
            if CNISegments == "1" or CNISegments == "":
                CNISegments = "1"
            CN2RPoints_4 += getFloat(CNISegments)
            Trace.Write("No 4")
            attrValDict["X1756EN2TRPoints_4"] = X1756EN2TRPoints_4
            attrValDict["CN2RPoints_4"] = CN2RPoints_4
        if (typeDownlink == "CNET Non-Redundant") and (controllerRedundancy == "Non Redundant") and (noOf1765DIIOMs > 32) and (AIOControllerRacks == "Yes"):
            X1756EN2TRPoints_51 += 2
            if CNISegments == "1" or CNISegments == "":
                CNISegments = "1"
            CN2RPoints_51 += getFloat(CNISegments)
            TKFXX102Points_51 += 1
            TKFPCXX2Points_51 += 1
            currentThirdPartyCabinet = 1
            Trace.Write("Yes 5-1")
            attrValDict["X1756EN2TRPoints_51"] = X1756EN2TRPoints_51
            attrValDict["CN2RPoints_51"] = CN2RPoints_51
            attrValDict["TKFXX102Points_51"] = TKFXX102Points_51
            attrValDict["TKFPCXX2Points_51"] = TKFPCXX2Points_51
        elif (typeDownlink == "CNET Non-Redundant") and (controllerRedundancy == "Non Redundant") and (noOf1765DIIOMs <= 32) and (AIOControllerRacks == "Yes"):
            X1756EN2TRPoints_51 += 1
            if CNISegments == "1" or CNISegments == "":
                CNISegments = "1"
            CN2RPoints_51 += getFloat(CNISegments)
            TKFXX102Points_51 += 1
            TKFPCXX2Points_51 += 1
            currentThirdPartyCabinet = 1
            Trace.Write("No 5-1")
            attrValDict["X1756EN2TRPoints_51"] = X1756EN2TRPoints_51
            attrValDict["CN2RPoints_51"] = CN2RPoints_51
            attrValDict["TKFXX102Points_51"] = TKFXX102Points_51
            attrValDict["TKFPCXX2Points_51"] = TKFPCXX2Points_51
        if (typeDownlink == "CNET Non-Redundant") and (controllerRedundancy == "Non Redundant") and (noOf1765DIIOMs > 32) and (AIOControllerRacks == "No" or AIOControllerRacks == ""):
            X1756EN2TRPoints_52 += 2
            if CNISegments == "1" or CNISegments == "":
                CNISegments = "1"
            CN2RPoints_52 += getFloat(CNISegments)
            Trace.Write("Yes 5-2")
            attrValDict["X1756EN2TRPoints_52"] = X1756EN2TRPoints_52
            attrValDict["CN2RPoints_52"] = CN2RPoints_52
        elif (typeDownlink == "CNET Non-Redundant") and (controllerRedundancy == "Non Redundant") and (noOf1765DIIOMs <= 32) and (AIOControllerRacks == "No" or AIOControllerRacks == ""):
            X1756EN2TRPoints_52 += 1
            if CNISegments == "1" or CNISegments == "":
                CNISegments = "1"
            CN2RPoints_52 += getFloat(CNISegments)
            Trace.Write("No 5-2")
            attrValDict["X1756EN2TRPoints_52"] = X1756EN2TRPoints_52
            attrValDict["CN2RPoints_52"] = CN2RPoints_52
        # 3rd Party Cabinet
        attrValDict["thirdpartycabinet"] += math.ceil((currentThirdPartyCabinet) / 4.0)
        tempData["C200_UOC_var_9"] = attrValDict["thirdpartycabinet"]
        product.Attr("Temporary Data").AssignValue(str(tempData))
        ##5130... Parts
        # Count1756_1 = 0
        Count1756_2 = 0
        C200Peer += row["C200_peer_to_peer_communication"]
        Count1756_1 = C200Peer.count("ControlNet")
        Trace.Write(C200Peer)
        Count1765_2 = X1756EN2TRPoints_1 + X1756EN2TRPoints_2 + X1756EN2TRPoints_3 + X1756EN2TRPoints_4 + X1756EN2TRPoints_51 + X1756EN2TRPoints_52
        Qty1756 = Count1756_1 + Count1765_2  # Total 1765 Count
        if (controllerRedundancy == "Redundant" or controllerRedundancy == "") and (TypeofUOC == "UOC" or TypeofUOC == ""):
            Qty900CP1 += 2
        if (controllerRedundancy == "Non Redundant") and (TypeofUOC == "UOC" or TypeofUOC == ""):
            Qty900CP1 += 1
        cal5130Parts = Qty900CP1 * 2 + Qty1756
        if (existingC200Server != "FTE" or existingC200Server != "") and (providingFTECables == "Yes" or providingFTECables == "") and (AvgCableLength == "2m"):
            Trace.Write("check 1 - 2")
            attrValDict["51305482-102"] = cal5130Parts
            attrValDict["51305482-202"] = cal5130Parts
        if (existingC200Server != "FTE" or existingC200Server != "") and (providingFTECables == "Yes" or providingFTECables == "") and (AvgCableLength == "5m"):
            Trace.Write("check 3 - 4")
            attrValDict["51305482-105"] = cal5130Parts
            attrValDict["51305482-205"] = cal5130Parts
        if (existingC200Server != "FTE" or existingC200Server != "") and (providingFTECables == "Yes" or providingFTECables == "") and (AvgCableLength == "10m" or AvgCableLength == ""):
            Trace.Write("check 5 - 6")
            attrValDict["51305482-110"] = cal5130Parts
            attrValDict["51305482-210"] = cal5130Parts
        if (existingC200Server != "FTE" or existingC200Server != "") and (providingFTECables == "Yes" or providingFTECables == "") and (AvgCableLength == "20m"):
            Trace.Write("check 7 - 8")
            attrValDict["51305482-120"] = cal5130Parts
            attrValDict["51305482-220"] = cal5130Parts
        #last segment implementation
        if (existingC200Server != "FTE" or existingC200Server != "") and (C200FTEexpServ == "EightPortCISCOSwitch"):
            QtySI3300I2 = (math.ceil(colocatedGroups / 8)) * 2 + additionalSwitches
        if (existingC200Server != "FTE" or existingC200Server != "") and (C200FTEexpServ == "EightPortCISCOSplitSwitch"):
            QtySI3300I2 = (math.ceil(colocatedGroups / 6)) * 2 + additionalSwitches
        if (existingC200Server != "FTE" or existingC200Server != "") and (C200FTEexpServ == "TwentyFourSTPPortCISCOSwitch"):
            QtySI920LN4 = (math.ceil(colocatedGroups / 24)) * 2 + additionalSwitches
        if (existingC200Server != "FTE" or existingC200Server != "") and (C200FTEexpServ == "TwentyFourSTPPortCISCOSplitSwitch"):
            QtySI920LN4 = (math.ceil(colocatedGroups / 22)) * 2 + additionalSwitches
        if (existingC200Server != "FTE" or existingC200Server != "") and (C200FTEexpServ == "TwentyFourSTPPortCISCOGBSwitch"):
            QtySI920LN4 = (math.ceil(colocatedGroups / 24)) * 2 + additionalSwitches
        if (existingC200Server != "FTE" or existingC200Server != "") and (C200FTEexpServ == "TwentyFourSTPPortCISCOGBSplitSwitch"):
            QtySI920LN4 = (math.ceil(colocatedGroups / 22)) * 2 + additionalSwitches
        if (existingC200Server != "FTE" or existingC200Server != "") and (C200FTEexpServ == "FortyEightSTPPortCISCOSwitch"):
            QtySI920LN8 = (math.ceil(colocatedGroups / 48)) * 2 + additionalSwitches
        if (existingC200Server != "FTE" or existingC200Server != "") and (C200FTEexpServ == "FortyEightSTPPortCISCOSplitSwitch"):
            QtySI920LN8 = (math.ceil(colocatedGroups / 48)) * 2 + additionalSwitches
        if (existingC200Server != "FTE" or existingC200Server != "") and (C200FTEexpServ == "FortyEightSTPPortCISCONonRoutableGBSwitch"):
            QtySI920LN8 = (math.ceil(colocatedGroups / 46)) * 2 + additionalSwitches
        if (existingC200Server != "FTE" or existingC200Server != "") and (C200FTEexpServ == "FortyEightSTPPortCISCONonRoutableGBSplitSwitch"):
            QtySI920LN8 = (math.ceil(colocatedGroups / 46)) * 2 + additionalSwitches
        ###33
        if (providingFTECables == "Yes" or providingFTECables == "" and C200FTEexpServ == "EightPortCISCOSwitch"):
            test = attrValDict["51305786-502"] = math.ceil(QtySI3300I2) / 2
        if (providingFTECables == "Yes" or providingFTECables == "" and C200FTEexpServ == "TwentyFourSTPPortCISCOSwitch"):
            test = attrValDict["51305786-502"] = math.ceil(QtySI920LN4) / 2
        if (providingFTECables == "Yes" or providingFTECables == "" and C200FTEexpServ == "TwentyFourSTPPortCISCOGBSwitch"):
            test = attrValDict["51305786-502"] = math.ceil(QtySI920LN4) / 2
        if (providingFTECables == "Yes" or providingFTECables == "" and (C200FTEexpServ == "FortyEightSTPPortCISCOSwitch" or C200FTEexpServ == "FortyEightSTPPortCISCONonRoutableGBSwitch")):
            test = attrValDict["51305786-502"] = math.ceil(QtySI920LN8) / 2
        if (providingFTECables == "Yes" or providingFTECables == "" and C200FTEexpServ == "EightPortCISCOSplitSwitch"):
            test = attrValDict["51305786-502"] = math.ceil(QtySI3300I2) / 2 * 3
        if (providingFTECables == "Yes" or providingFTECables == "" and C200FTEexpServ == "TwentyFourSTPPortCISCOSplitSwitch"):
            test = attrValDict["51305786-502"] = math.ceil(QtySI920LN4) / 2 * 3
        if (providingFTECables == "Yes" or providingFTECables == "" and C200FTEexpServ == "TwentyFourSTPPortCISCOGBSplitSwitch"):
            test = attrValDict["51305786-502"] = math.ceil(QtySI920LN4) / 2 * 3
        if (providingFTECables == "Yes" or providingFTECables == "" and (C200FTEexpServ == "FortyEightSTPPortCISCOSplitSwitch" or C200FTEexpServ == "FortyEightSTPPortCISCONonRoutableGBSplitSwitch")):
            test = attrValDict["51305786-502"] = math.ceil(QtySI920LN8) / 2 * 3

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

def populateWriteIns(product):

    pos2_55 = 0
    pos2_23 = 0
    pos3_55 = 0
    pos3_23 = 0

    for row in getContainer(product, "Orion_Station_Configuration").Rows:
        col = row.GetColumnByName("Orion_Monitor_Type")
        val = getValue(row, col)
        noOfConfig = getFloat(row["Orion_Number_of_console_bases_with_same_configuration"])

        if val == "55 inch NTS":
            pos2_55 += getFloat(row["Orion_Number_of_2_Position_Base_Unit"]) * noOfConfig
            pos3_55 += getFloat(row["Orion_Number_of_3_Position_Base_Unit"]) * noOfConfig
        elif val == "23 inch NTS":
            pos2_23 += getFloat(row["Orion_Number_of_2_Position_Base_Unit"]) * noOfConfig
            pos3_23 += getFloat(row["Orion_Number_of_3_Position_Base_Unit"]) * noOfConfig

    writeInData = dict()
    thirdPartyCost = 0
    thirdPartyPrice = 0
    msid= product.Attr('Migration_MSID_Choices').GetValue()
    sysNumber= product.Attr('Migration_MSID_System_Number').GetValue()
    area = msid +" - "+ sysNumber

    for row in getContainer(product, "Orion_General_Information").Rows:
        col = row.GetColumnByName("WriteIn")
        if getValue(row, col) == "Cables and adapters per 2 base unit w/55in":
            thirdPartyPrice += pos2_55 * getFloat(row["Price"])
            thirdPartyCost += pos2_55 * getFloat(row["Cost"])
        elif getValue(row, col) == "Cables and adapters per 3 base unit w/55in":
            thirdPartyPrice += pos3_55 * getFloat(row["Price"])
            thirdPartyCost += pos3_55 * getFloat(row["Cost"])
        elif getValue(row, col) == "Cables and adapters per 2 base unit w/23in":
            thirdPartyPrice += pos2_23 * getFloat(row["Price"])
            thirdPartyCost += pos2_23 * getFloat(row["Cost"])
        elif getValue(row, col) == "Cables and adapters per 3 base unit w/23in":
            thirdPartyPrice += pos3_23 * getFloat(row["Price"])
            thirdPartyCost += pos3_23 * getFloat(row["Cost"])
    writeInData["Write-in Third Party Hardware Misc"] = [str(thirdPartyPrice), str(thirdPartyCost), "",area]

    con = getContainer(product, "Orion_General_Information_Container")

    for row in con.Rows:
        writeInData[row["WriteInProduct"]] = [row["Price"] if row["Price"] else "0", row["Cost"] if row["Cost"] else "0", row["ExtendedDescription"], area ]

    productContainer = product.GetContainerByName("MSID_Product_Container")
    productRow = productContainer.Rows.GetByColumnName("Product Name", "Orion Console")
    prod = productRow.Product
    con = prod.GetContainerByName("WriteInProduct")
    #if con.Rows.Count > 0:
    con.Rows.Clear()
    for wi, wiData in writeInData.items():
        if (wiData[0] and getFloat(wiData[0])) or (wiData[1] and getFloat(wiData[1])):
            row = con.Rows.GetByColumnName("WriteInProducts", wi)
            row = con.AddNewRow()
            #if not row:
                #row = con.AddNewRow()
            row.Product.Attr("Selected_WriteIn").AssignValue(wi)
            row.Product.Attr("Price").AssignValue(wiData[0])
            row.Product.Attr("Cost").AssignValue(wiData[1])
            row.Product.Attr("QI_Area").AssignValue(wiData[3])
            row.Product.Attr("ItemQuantity").AssignValue("1")
            row.Product.Attr("Extended Description").AssignValue(wiData[2])
            row.Product.ApplyRules()
            row.ApplyProductChanges()
            row.Calculate()
    con.Calculate()

def updateAttrWithCustomCBECValues(product, attrValDict):
    con1 = getContainer(product, "CB_EC_migration_to_C300_UHIO_Configuration_Cont")
    for row in con1.Rows:
        IORedundancy = row["CB_EC_Do_you_want_IO_redundancy"]
        CBs = getFloat(row["CB_EC_How_many_CBs_are_being_migrated"])
        ECs = getFloat(row["CB_EC_How_many_ECs_are_being_migrated"])
        if (CBs + ECs) > 0:
            if IORedundancy == "Yes":
                CC_ZHR021 = 0
                CC_ZHR031 = 0
                CC_ZHR021 = math.ceil(((CBs+ECs)-3)/2)
                if ((CBs+ECs)%2) != 0:
                    CC_ZHR031 = 1
                attrValDict["CC-ZHR013"] = 2
                attrValDict["CC-ZHR021"] = CC_ZHR021
                attrValDict["CC-ZHR031"] = CC_ZHR031
            else:
                CC_ZHN021 = 0
                CC_ZHN031 = 0
                CC_ZHN021 = math.ceil(((CBs+ECs)-3)/2)
                if ((CBs+ECs)%2) != 0:
                    CC_ZHN031 = 1
                attrValDict["CC-ZHN013"] = 2
                attrValDict["CC-ZHN021"] = CC_ZHN021
                attrValDict["CC-ZHN031"] = CC_ZHN031
        B51202329_726 = 0
        if  (CBs + ECs) > 4 and (CBs + ECs) < 11:
            B51202329_726 = 1
        elif  (CBs + ECs) > 10 and (CBs + ECs) < 17:
            B51202329_726 = 2
        elif  (CBs + ECs) > 16:
            B51202329_726 = 3
        attrValDict["51202329-726"] = B51202329_726
        break

def getRowData(Product, container, column):
    Container = getContainer(Product, container)
    for row in Container.Rows:
        return row[column]

def populateWriteInsC200(product):
    writeInData = dict()
    msid= product.Attr('Migration_MSID_Choices').GetValue()
    sysNumber= product.Attr('Migration_MSID_System_Number').GetValue()
    area = msid +" - "+ sysNumber
    con = getContainer(product, "C200_Third_Party_Items_Cont")
    for row in con.Rows:
        if getFloat(row["Price"]) > 0 and getFloat(row["Cost"]) > 0 and row["ExtendedDescription"] != "":
            writeInData[row["WriteIn"]] = [row["Price"] if row["Price"] else "0", row["Cost"] if row["Cost"] else "0", row["ExtendedDescription"],area]

    productContainer = product.GetContainerByName("MSID_Product_Container")
    productRow = productContainer.Rows.GetByColumnName("Product Name", "C200 Migration")
    prod = productRow.Product
    con = prod.GetContainerByName("WriteInProduct")
    con.Clear()
    for wi, wiData in writeInData.items():
        if (wiData[0] and getFloat(wiData[0])) or (wiData[1] and getFloat(wiData[1])):
            row = con.AddNewRow()
            row.Product.Attr("Selected_WriteIn").AssignValue("Write-In Third Party Hardware & Software")
            row.Product.Attr("Price").AssignValue(wiData[0])
            row.Product.Attr("Cost").AssignValue(wiData[1])
            row.Product.Attr("ItemQuantity").AssignValue("1")
            row.Product.Attr("QI_Area").AssignValue(wiData[3])
            row.Product.Attr("Extended Description").AssignValue(wiData[2])
            row.Product.ApplyRules()
            row.ApplyProductChanges()
            row.Calculate()
        con.Calculate()

def populateWriteInsFSC(product):
    writeInData = dict()
    msid= product.Attr('Migration_MSID_Choices').GetValue()
    sysNumber= product.Attr('Migration_MSID_System_Number').GetValue()
    area = msid +" - "+ sysNumber

    con = getContainer(product, "FSC_to_SM_3rd_Party_Items")


    i=1
    price = 0
    cost = 0
    extendedDesc  = 0
    for row in con.Rows:
        if(i == 1):
            price = str(row["FSC_to_SM_3rd_Party_Hardware_per_Audit_Report"] if row["FSC_to_SM_3rd_Party_Hardware_per_Audit_Report"] !='' else 0)
        elif(i == 3):
            cost = str(row["FSC_to_SM_3rd_Party_Hardware_per_Audit_Report"] if row["FSC_to_SM_3rd_Party_Hardware_per_Audit_Report"] !='' else 0)
        elif(i == 4):
            extendedDesc = str(row["FSC_to_SM_3rd_Party_Hardware_per_Audit_Report"])
        i+=1

    writeInData["Write-in Third Party Hardware Misc"] = [price,cost,extendedDesc,area]
    if (float(price) > 0  and float(cost) > 0):
        productContainer = product.GetContainerByName("MSID_Product_Container")
        productRow = productContainer.Rows.GetByColumnName("Product Name", "FSC to SM")
        prod = productRow.Product
        con = prod.GetContainerByName("WriteInProduct")
        if con.Rows.Count == 1:
            con.DeleteRow(0)
        for wi, wiData in writeInData.items():
                if con.Rows.Count == 0:
                    row = con.AddNewRow()
                row.Product.Attr("Selected_WriteIn").AssignValue(wi)
                row.Product.Attr("Price").AssignValue(wiData[0])
                row.Product.Attr("Cost").AssignValue(wiData[1])
                row.Product.Attr("QI_Area").AssignValue(wiData[3])
                row.Product.Attr("ItemQuantity").AssignValue("1")
                row.Product.Attr("Extended Description").AssignValue(wiData[2])
                row.Product.ApplyRules()
                row.ApplyProductChanges()
                row.Calculate()
    elif(float(price) == 0  or float(cost) == 0):
        productContainer = product.GetContainerByName("MSID_Product_Container")
        productRow = productContainer.Rows.GetByColumnName("Product Name", "FSC to SM")
        prod = productRow.Product
        con = prod.GetContainerByName("WriteInProduct")
        con.DeleteRow(0)
    con.Calculate()