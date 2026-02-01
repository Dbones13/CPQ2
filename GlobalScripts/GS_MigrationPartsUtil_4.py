import math
def getContainer(prod, conName):
    return prod.GetContainerByName(conName)

def getInt(var):
    if var != "":
        return int(var)
    return 0


def getFloat(var):
    if var != "":
        return float(var)
    return 0

def Calcualte_BOM_IO_Switch(Location_IO_Racks, Switch_Type, Calculated_Racks, Total_Remote_Serial, No_PLC_Remote_IO):
    if Location_IO_Racks == "No":
        Query = "select * from LM_BOM_IO_SWITCH where IO_Racks_Location = 'No' and Switch_Type='"+Switch_Type+"' and ("+Calculated_Racks+" between Calculated_IO_Racks_LB and Calculated_IO_Racks_UB)"
        res = SqlHelper.GetFirst(Query)
    elif Calculated_Racks != '' and Total_Remote_Serial != '':
        Query = "select * from LM_BOM_IO_SWITCH where IO_Racks_Location = '"+Location_IO_Racks+"' and Switch_Type='"+Switch_Type+"' and (Calculated_IO_Racks_LB is NULL or "+Calculated_Racks+" between Calculated_IO_Racks_LB and Calculated_IO_Racks_UB) and (Total_Remote_Serial_IO_Racks_LB is NULL or "+Total_Remote_Serial+" between Total_Remote_Serial_IO_Racks_LB and Total_Remote_Serial_IO_Racks_UB ) and PLC_Remote_IO_Group ={}".format(No_PLC_Remote_IO)
        res = SqlHelper.GetFirst(Query)
    elif Calculated_Racks != '' and Total_Remote_Serial == '':
        Query = "select * from LM_BOM_IO_SWITCH where IO_Racks_Location = '"+Location_IO_Racks+"' and Switch_Type='"+Switch_Type+"' and (Calculated_IO_Racks_LB is NULL or "+Calculated_Racks+" between Calculated_IO_Racks_LB and Calculated_IO_Racks_UB) and Total_Remote_Serial_IO_Racks_LB is NULL and PLC_Remote_IO_Group ={}".format(No_PLC_Remote_IO)
        res = SqlHelper.GetFirst(Query)
    elif Calculated_Racks == '' and Total_Remote_Serial != '':
        Query = "select * from LM_BOM_IO_SWITCH where IO_Racks_Location = '"+Location_IO_Racks+"' and Switch_Type='"+Switch_Type+"' and Calculated_IO_Racks_LB is NULL and (Total_Remote_Serial_IO_Racks_LB is NULL or "+Total_Remote_Serial+" between Total_Remote_Serial_IO_Racks_LB and Total_Remote_Serial_IO_Racks_UB) and PLC_Remote_IO_Group ={}".format(No_PLC_Remote_IO)
        res = SqlHelper.GetFirst(Query)
    else:
        Query = "select * from LM_BOM_IO_SWITCH where IO_Racks_Location = '"+Location_IO_Racks+"' and Switch_Type='"+Switch_Type+"' and Calculated_IO_Racks_LB is NULL and Total_Remote_Serial_IO_Racks_LB is NULL and PLC_Remote_IO_Group ={}".format(No_PLC_Remote_IO)
        res = SqlHelper.GetFirst(Query)
    return res



def updateAttributeWithLMtoELMMValues(product, attrValDict):
    lmPLCCont = getContainer(product, "LM_to_ELMM_ControlEdge_PLC_Cont")
    lmLocalIO = getContainer(product, "LM_to_ELMM_ControlEdge_PLC_Local_IO_Cont")
    lmRemoteIO = getContainer(product, "LM_to_ELMM_ControlEdge_PLC_Remote_IO_Cont")
    lmGenQues = getContainer(product, "LM_to_ELMM_ControlEdge_PLC_Migration_Gen_Cont")
    for row in lmPLCCont.Rows:
        index = row.RowIndex

        l = attrValDict.get("900A01-0202 Local I/O",list())
        l.append(str(getInt(lmLocalIO.Rows[index]["qty_621_0022_AR_VR_Isolated_AI_IOM_0_72"]) + (2*getInt(lmLocalIO.Rows[index]["qty_621_0020R_UAIM_621_0025R_RTDM_IOM_0_72"]))))
        attrValDict["900A01-0202 Local I/O"] = l

        l = attrValDict.get("900A01-0202 Remote I/O",list())
        l.append(str(getInt(lmRemoteIO.Rows[index]["total_qty_621_0022_AR_0022_VR_Isolated_AI_IOM_0_72"]) + (2*getInt(lmRemoteIO.Rows[index]["total_qty_621_0020R_UAIM_0025R_RTDM_IOM_0_72"]))))
        attrValDict["900A01-0202 Remote I/O"] = l

        l = attrValDict.get("900B01-0301 Local I/O",list())
        l.append(str(getInt(lmLocalIO.Rows[index]["qty_621_0010_AR_VR_AO_IOM_0_72"])))
        attrValDict["900B01-0301 Local I/O"] = l

        l = attrValDict.get("900B01-0301 Remote I/O",list())
        l.append(str(getInt(lmRemoteIO.Rows[index]["total_qty_621_0010_AR_0010_VR_AO_IOM_0_72"])))
        attrValDict["900B01-0301 Remote I/O"] = l

        l = attrValDict.get("900G03-0202 Local I/O",list())
        l.append(str(math.ceil(getFloat(lmLocalIO.Rows[index]["qty_621_1100R_115_VAC_VDC_DI_IOM_0_72"])/2)+ getInt(lmLocalIO.Rows[index]["qty_621_1160R_1250R_115VAC_240VAC_DI_IOM_0_72"]) + (2*getInt(lmLocalIO.Rows[index]["qty_621_1180R_115_VAC_VDC_Isolated_DI_IOM_0_72"]))))
        attrValDict["900G03-0202 Local I/O"] = l

        l = attrValDict.get("900G03-0202 Remote I/O",list())
        l.append(str(math.ceil(getFloat(lmRemoteIO.Rows[index]["total_qty_621_1100R_115_Vac_Vdc_DI_IOM_0_72"])/2)+ getInt(lmRemoteIO.Rows[index]["total_qty_621_1160R_1250R_115Vac_240_Vac_DI_IOM_0_72"]) + (2*getInt(lmRemoteIO.Rows[index]["total_qty_621_1180R_115_Vac_Vdc_Isolated_DI_IOM_0_72"]))))
        attrValDict["900G03-0202 Remote I/O"] = l

        l = attrValDict.get("900G32-0101 Local I/O",list())
        l.append(str(math.ceil(getFloat(lmLocalIO.Rows[index]["qty_621_1500R_24_VAC_VDC_DI_IOM_0_72"])/4)+ math.ceil(getFloat(lmLocalIO.Rows[index]["qty_621_3552R_3560R_24_VAC_VDC_Sink_DI_IOM_0_72"])/2) + getInt(lmLocalIO.Rows[index]["qty_621_3580_24_VDC_DI_IOM_0_72"]) + math.ceil(getFloat(lmLocalIO.Rows[index]["qty_621_4500R_24_VDC_Source_DI_IOM_0_72"])/4)))
        attrValDict["900G32-0101 Local I/O"] = l

        l = attrValDict.get("900G32-0101 Remote I/O",list())
        l.append(str(math.ceil(getFloat(lmRemoteIO.Rows[index]["total_qty_621_1500R_24_Vac_Vdc_DI_IOM_0_72"])/4)+ math.ceil(getFloat(lmRemoteIO.Rows[index]["total_qty_621_3552R_3560R_24_Vdc_Sink_DI_IOM_0_72"])/2) + getInt(lmRemoteIO.Rows[index]["total_qty_621_3580_24Vdc_DI_IOM_0_72"]) + math.ceil(getFloat(lmRemoteIO.Rows[index]["total_qty_621_4500R_24_Vdc_Source_DI_IOM_0_72"])/4)))
        attrValDict["900G32-0101 Remote I/O"] = l

        l = attrValDict.get("900H01-0202 Local I/O",list())
        l.append(str(getInt(lmLocalIO.Rows[index]["qty_621_0007R_Reed_Relay_Output_IOM_0_72"])))
        attrValDict["900H01-0202 Local I/O"] = l

        l = attrValDict.get("900H01-0202 Remote I/O",list())
        l.append(str(getInt(lmRemoteIO.Rows[index]["total_qty_621_0007R_Reed_Relay_Output_IOM_0_72"])))
        attrValDict["900H01-0202 Remote I/O"] = l

        l = attrValDict.get("900H03-0202 Local I/O",list())
        l.append(str(getInt(lmLocalIO.Rows[index]["qty_621_2100R_2101R_2102R_115_VAC_DO_IOM_0_72"]) + (2 * getInt(lmLocalIO.Rows[index]["qty_621_2150R_115VAC_DO_IOM_0_72"])) + getInt(lmLocalIO.Rows[index]["qty_621_2200R_230_VAC_DO_IOM_0_72"])))
        attrValDict["900H03-0202 Local I/O"] = l

        l = attrValDict.get("900H03-0202 Remote I/O",list())
        l.append(str(getInt(lmRemoteIO.Rows[index]["total_qty_621_2100R_2101R_2102R_115_Vac_DO_IOM_0_72"]) + (2 * getInt(lmRemoteIO.Rows[index]["total_qty_621_2150R_115_Vac_DO_IOM_0_72"])) + getInt(lmRemoteIO.Rows[index]["total_qty_621_2200R_230_Vac_DO_IOM_0_72"])))
        attrValDict["900H03-0202 Remote I/O"] = l

        l = attrValDict.get("900H32-0102 Local I/O",list())
        l.append(str((math.ceil(getFloat(lmLocalIO.Rows[index]["qty_621_6550R_6551R_24_VDC_DO_IOM_0_72"])/2) + math.ceil(getFloat(lmLocalIO.Rows[index]["qty_621_6500R_12_24_VDC_Source_DO_IOM_0_72"])/4)) + math.ceil(getFloat(lmLocalIO.Rows[index]["qty_621_6503R_12_24_VDC_Source_Self_Protected_DO_IOM_0_72"])/4) + getInt(lmLocalIO.Rows[index]["qty_621_6575_24_VDC_DO_IOM_0_72"])))
        attrValDict["900H32-0102 Local I/O"] = l

        l = attrValDict.get("900H32-0102 Remote I/O",list())
        l.append(str((math.ceil(getFloat(lmRemoteIO.Rows[index]["total_qty_621_6550R_6551R_24_Vdc_DO_IOM_0_72"])/2) + math.ceil(getFloat(lmRemoteIO.Rows[index]["total_qty_621_6500R_12_24_Vdc_Source_DO_IOM_0_72"])/4)) + math.ceil(getFloat(lmRemoteIO.Rows[index]["total_qty_621_6503R_12_24_Vdc_Source_Self-Protected_DO_IOM_0_72"])/4) + getInt(lmRemoteIO.Rows[index]["total_qty_621_6575_24_Vdc_DO_IOM_0_72"])))
        attrValDict["900H32-0102 Remote I/O"] = l

        l = attrValDict.get("900ES1-0100 Local I/O",list())
        l.append(str(getInt(lmLocalIO.Rows[index]["qty_ASCII_IOM_0_6"])))
        attrValDict["900ES1-0100 Local I/O"] = l

        l = attrValDict.get("900ES1-0100 Remote I/O",list())
        l.append(str(getInt(lmRemoteIO.Rows[index]["total_qty_ASCII_IOM_0_6"])))
        attrValDict["900ES1-0100 Remote I/O"] = l

        l = attrValDict.get("900K01-0201 Local I/O",list())
        l.append(str(getInt(lmLocalIO.Rows[index]["qty_621_0024R_0307R_Pulse_Input_Module_High_Speed_Counter_IOM_0_6"])))
        attrValDict["900K01-0201 Local I/O"] = l

        l = attrValDict.get("900K01-0201 Remote I/O",list())
        l.append(str(getInt(lmRemoteIO.Rows[index]["total_qty_621_0024R_0307R_Pulse_Input_Module_High_Speed_Counter_IOM_0_6"])))
        attrValDict["900K01-0201 Remote I/O"] = l

        l = attrValDict.get("900G04-0101 Local I/O",list())
        l.append(str(math.ceil(getFloat(lmLocalIO.Rows[index]["qty_621_1101R_115_VAC_VDC_Isolated_DI_IOM_0_72"])/2)))
        attrValDict["900G04-0101 Local I/O"] = l

        l = attrValDict.get("900G04-0101 Remote I/O",list())
        l.append(str(math.ceil(getFloat(lmRemoteIO.Rows[index]["total_qty_621_1101R_115_Vac_Vdc_Isolated_DI_IOM_0_72"])/2)))
        attrValDict["900G04-0101 Remote I/O"] = l

        l = attrValDict.get("900A01-0202",list())
        l.append(getFloat(attrValDict["900A01-0202 Local I/O"][-1]) + getFloat(attrValDict["900A01-0202 Remote I/O"][-1]))
        attrValDict["900A01-0202"]=l

        l = attrValDict.get("900B01-0301",list())
        l.append(getFloat(attrValDict["900B01-0301 Local I/O"][-1]) + getFloat(attrValDict["900B01-0301 Remote I/O"][-1]))
        attrValDict["900B01-0301"]=l

        l = attrValDict.get("900G03-0202",list())
        l.append(getFloat(attrValDict["900G03-0202 Local I/O"][-1]) + getFloat(attrValDict["900G03-0202 Remote I/O"][-1]))
        attrValDict["900G03-0202"]=l

        l = attrValDict.get("900G32-0301",list())
        l.append(getFloat(attrValDict["900G32-0101 Local I/O"][-1]) + getFloat(attrValDict["900G32-0101 Remote I/O"][-1]))
        attrValDict["900G32-0301"]=l

        l = attrValDict.get("900H01-0202",list())
        l.append(getFloat(attrValDict["900H01-0202 Local I/O"][-1]) + getFloat(attrValDict["900H01-0202 Remote I/O"][-1]))
        attrValDict["900H01-0202"]=l

        l = attrValDict.get("900H03-0202",list())
        l.append(getFloat(attrValDict["900H03-0202 Local I/O"][-1]) + getFloat(attrValDict["900H03-0202 Remote I/O"][-1]))
        attrValDict["900H03-0202"]=l

        l = attrValDict.get("900H32-0302",list())
        l.append(getFloat(attrValDict["900H32-0102 Local I/O"][-1]) + getFloat(attrValDict["900H32-0102 Remote I/O"][-1]))
        attrValDict["900H32-0302"]=l

        l = attrValDict.get("900ES1-0100",list())
        l.append(getFloat(attrValDict["900ES1-0100 Local I/O"][-1]) + getFloat(attrValDict["900ES1-0100 Remote I/O"][-1]))
        attrValDict["900ES1-0100"]=l

        l = attrValDict.get("900K01-0201",list())
        l.append(getFloat(attrValDict["900K01-0201 Local I/O"][-1]) + getFloat(attrValDict["900K01-0201 Remote I/O"][-1]))
        attrValDict["900K01-0201"]=l

        l = attrValDict.get("900G04-0101",list())
        l.append(getFloat(attrValDict["900G04-0101 Local I/O"][-1]) + getFloat(attrValDict["900G04-0101 Remote I/O"][-1]))
        attrValDict["900G04-0101"]=l

        l = attrValDict.get("900TEK-0200",list())
        l.append(getFloat(attrValDict["900A01-0202"][-1]) + getFloat(attrValDict["900B01-0301"][-1]) + getFloat(attrValDict["900K01-0201"][-1]))
        attrValDict["900TEK-0200"]=l

        l = attrValDict.get("900TER-0200",list())
        l.append(getFloat(attrValDict["900G03-0202"][-1]) + getFloat(attrValDict["900H01-0202"][-1]) + getFloat(attrValDict["900H03-0202"][-1]))
        attrValDict["900TER-0200"]=l

        l = attrValDict.get("900TCK-0200",list())
        l.append(getFloat(attrValDict["900G32-0301"][-1]) + getFloat(attrValDict["900H32-0302"][-1]) + getFloat(attrValDict["900G04-0101"][-1]))
        attrValDict["900TCK-0200"]=l


        IO_Racks_Location= "No" if lmPLCCont.Rows[index]["LM_are_the_IO_Racks_remotely_located"] == "" else lmPLCCont.Rows[index]["LM_are_the_IO_Racks_remotely_located"]
        IO_Racks_Type= "12 Slot Rack" if lmPLCCont.Rows[index]["LM_type_of_IO_Rack_to_be_installed"] == "" else lmPLCCont.Rows[index]["LM_type_of_IO_Rack_to_be_installed"]
        IO_Racks_Redundant= "No" if lmPLCCont.Rows[index]["LM_do_you_need_Redundant_PS_for_IO_Racks"] == "" else lmPLCCont.Rows[index]["LM_do_you_need_Redundant_PS_for_IO_Racks"]
        Total_Remote_Serial= 0 if lmRemoteIO.Rows[index]["total_remote_serial_IO_racks_0_16"] == "" else getInt(lmRemoteIO.Rows[index]["total_remote_serial_IO_racks_0_16"])

        LM900R08_0200 = 0
        LM900R08R_0200 = 0
        LM900R12_0200 = 0
        LM900R12R_0200 = 0
        LM900P24_0301 = 0
        LM51305482_102 = 0
        LM51305482_202 = 0
        LM51305482_105 = 0
        LM51305482_205 = 0
        LM51305482_110 = 0
        LM51305482_210 = 0
        LM51305482_120 = 0
        LM51305482_220 = 0
        THIRDPARTY_CABINET = 0
        division_factor = 8 if IO_Racks_Type=="8 Slot Rack" else 12
        if IO_Racks_Type=="8 Slot Rack" and IO_Racks_Redundant in ["No",""]:
            if IO_Racks_Location  in ["No",""]:
                LM900R08_0200 = math.ceil((getFloat(attrValDict["900A01-0202"][-1]) + getFloat(attrValDict["900B01-0301"][-1]) + getFloat(attrValDict["900G03-0202"][-1]) +getFloat(attrValDict["900G32-0301"][-1]) + getFloat(attrValDict["900H01-0202"][-1]) + getFloat(attrValDict["900H03-0202"][-1]) + getFloat(attrValDict["900H32-0302"][-1]) + getFloat(attrValDict["900ES1-0100"][-1]) + getFloat(attrValDict["900K01-0201"][-1]) + getFloat(attrValDict["900G04-0101"][-1]) ) / division_factor )
            if IO_Racks_Location == "Yes - Local and Remote":
                LM900R08_0200 = math.ceil(( getFloat(attrValDict["900A01-0202 Local I/O"][-1]) + getFloat(attrValDict["900B01-0301 Local I/O"][-1]) + getFloat(attrValDict["900G03-0202 Local I/O"][-1]) + getFloat(attrValDict["900G32-0101 Local I/O"][-1]) + getFloat(attrValDict["900H01-0202 Local I/O"][-1]) + getFloat(attrValDict["900H03-0202 Local I/O"][-1]) + getFloat(attrValDict["900H32-0102 Local I/O"][-1]) + getFloat(attrValDict["900ES1-0100 Local I/O"][-1]) + getFloat(attrValDict["900K01-0201 Local I/O"][-1]) + getFloat(attrValDict["900G04-0101 Local I/O"][-1]) ) / division_factor ) + (Total_Remote_Serial)
            if IO_Racks_Location == "Yes - Only Remote":
                LM900R08_0200 = Total_Remote_Serial

        if IO_Racks_Type=="8 Slot Rack" and IO_Racks_Redundant=="Yes":
            if IO_Racks_Location  in ["No",""]: 
                LM900R08R_0200 = math.ceil(( getFloat(attrValDict["900A01-0202"][-1]) + getFloat(attrValDict["900B01-0301"][-1]) + getFloat(attrValDict["900G03-0202"][-1]) +getFloat(attrValDict["900G32-0301"][-1]) + getFloat(attrValDict["900H01-0202"][-1]) + getFloat(attrValDict["900H03-0202"][-1]) + getFloat(attrValDict["900H32-0302"][-1]) + getFloat(attrValDict["900ES1-0100"][-1]) + getFloat(attrValDict["900K01-0201"][-1]) + getFloat(attrValDict["900G04-0101"][-1]) ) / division_factor)
            if IO_Racks_Location == "Yes - Local and Remote":
                LM900R08R_0200 = math.ceil(( getFloat(attrValDict["900A01-0202 Local I/O"][-1]) + getFloat(attrValDict["900B01-0301 Local I/O"][-1]) + getFloat(attrValDict["900G03-0202 Local I/O"][-1]) + getFloat(attrValDict["900G32-0101 Local I/O"][-1]) + getFloat(attrValDict["900H01-0202 Local I/O"][-1]) + getFloat(attrValDict["900H03-0202 Local I/O"][-1]) + getFloat(attrValDict["900H32-0102 Local I/O"][-1]) + getFloat(attrValDict["900ES1-0100 Local I/O"][-1]) + getFloat(attrValDict["900K01-0201 Local I/O"][-1]) + getFloat(attrValDict["900G04-0101 Local I/O"][-1]) ) / division_factor ) + (Total_Remote_Serial)
            if IO_Racks_Location == "Yes - Only Remote":
                LM900R08R_0200 = Total_Remote_Serial


        if IO_Racks_Type=="12 Slot Rack" and IO_Racks_Redundant in ["No",""]:
            if IO_Racks_Location  in ["No",""]: 
                LM900R12_0200 = math.ceil((getFloat(attrValDict["900A01-0202"][-1]) + getFloat(attrValDict["900B01-0301"][-1]) + getFloat(attrValDict["900G03-0202"][-1]) +getFloat(attrValDict["900G32-0301"][-1]) + getFloat(attrValDict["900H01-0202"][-1]) + getFloat(attrValDict["900H03-0202"][-1]) + getFloat(attrValDict["900H32-0302"][-1]) + getFloat(attrValDict["900ES1-0100"][-1]) + getFloat(attrValDict["900K01-0201"][-1]) + getFloat(attrValDict["900G04-0101"][-1]) ) / division_factor)
            if IO_Racks_Location == "Yes - Local and Remote":
                LM900R12_0200 = math.ceil(( getFloat(attrValDict["900A01-0202 Local I/O"][-1]) + getFloat(attrValDict["900B01-0301 Local I/O"][-1]) + getFloat(attrValDict["900G03-0202 Local I/O"][-1]) + getFloat(attrValDict["900G32-0101 Local I/O"][-1]) + getFloat(attrValDict["900H01-0202 Local I/O"][-1]) + getFloat(attrValDict["900H03-0202 Local I/O"][-1]) + getFloat(attrValDict["900H32-0102 Local I/O"][-1]) + getFloat(attrValDict["900ES1-0100 Local I/O"][-1]) + getFloat(attrValDict["900K01-0201 Local I/O"][-1]) + getFloat(attrValDict["900G04-0101 Local I/O"][-1]) ) / division_factor ) + (Total_Remote_Serial)
            if IO_Racks_Location == "Yes - Only Remote":
                LM900R12_0200 = Total_Remote_Serial

        if IO_Racks_Type=="12 Slot Rack" and IO_Racks_Redundant=="Yes":
            if IO_Racks_Location  in ["No",""]: 
                LM900R12R_0200 = math.ceil((getFloat(attrValDict["900A01-0202"][-1]) + getFloat(attrValDict["900B01-0301"][-1]) + getFloat(attrValDict["900G03-0202"][-1]) +getFloat(attrValDict["900G32-0301"][-1]) + getFloat(attrValDict["900H01-0202"][-1]) + getFloat(attrValDict["900H03-0202"][-1]) + getFloat(attrValDict["900H32-0302"][-1]) + getFloat(attrValDict["900ES1-0100"][-1]) + getFloat(attrValDict["900K01-0201"][-1]) + getFloat(attrValDict["900G04-0101"][-1]) ) / division_factor)
            if IO_Racks_Location == "Yes - Local and Remote":
                LM900R12R_0200 = math.ceil(( getFloat(attrValDict["900A01-0202 Local I/O"][-1]) + getFloat(attrValDict["900B01-0301 Local I/O"][-1]) + getFloat(attrValDict["900G03-0202 Local I/O"][-1]) + getFloat(attrValDict["900G32-0101 Local I/O"][-1]) + getFloat(attrValDict["900H01-0202 Local I/O"][-1]) + getFloat(attrValDict["900H03-0202 Local I/O"][-1]) + getFloat(attrValDict["900H32-0102 Local I/O"][-1]) + getFloat(attrValDict["900ES1-0100 Local I/O"][-1]) + getFloat(attrValDict["900K01-0201 Local I/O"][-1]) + getFloat(attrValDict["900G04-0101 Local I/O"][-1]) ) / division_factor ) + (Total_Remote_Serial)
            if IO_Racks_Location == "Yes - Only Remote":
                LM900R12R_0200 = Total_Remote_Serial
        if lmPLCCont.Rows[index]["LM_CE_Power_Input_Type"] in ["DC",""]:
            LM900P24_0301 = 2 + (1 * LM900R08_0200) + (2 * LM900R08R_0200) + (1 * LM900R12_0200) + (2 * LM900R12R_0200)

        l = attrValDict.get("LM900R08_0200",list())
        l.append(LM900R08_0200)
        attrValDict["LM900R08_0200"] = l
        l = attrValDict.get("LM900R08R_0200",list())
        l.append(LM900R08R_0200)
        attrValDict["LM900R08R_0200"]= l

        l = attrValDict.get("LM900R12_0200",list())
        l.append(LM900R12_0200)
        attrValDict["LM900R12_0200"]=l

        l = attrValDict.get("LM_900P24_0301",list())
        l.append(LM900P24_0301)
        attrValDict["LM_900P24_0301"]=l

        l = attrValDict.get("LM900R12R_0200",list())
        l.append(LM900R12R_0200)
        attrValDict["LM900R12R_0200"]=l
        for row1 in lmGenQues.Rows:
            index1 = row1.RowIndex
            ot = lmGenQues.Rows[index1]["LM_to_ELMM_ControlEdge_PLC_Operating_temperature"]
            Trace.Write("OT:{0}".format(ot))
            if ot == "0 to 60 DegC or Marine application":
                Trace.Write("HII")
                l = attrValDict.get("900SP1-0200",list())
                l.append(getFloat(0 if attrValDict.get("LM900R08_0200") is None else attrValDict["LM900R08_0200"][-1]) + getFloat(0 if attrValDict.get("LM900R08R_0200") is None else attrValDict["LM900R08R_0200"][-1]) + getFloat(0 if attrValDict.get("LM900R12_0200") is None else attrValDict["LM900R12_0200"][-1]) + getFloat(0 if attrValDict.get("LM900R12R_0200") is None else attrValDict["LM900R12R_0200"][-1]))
                attrValDict["900SP1-0200"] = l
                if lmGenQues.Rows[index1]["Is_Honeywell_Providing_FTE_Cables"] in ["Yes"] :
                    if lmGenQues.Rows[index1]["Average_Cable_Length_For_PLC_Uplink"] == '2m':
                        LM51305482_102 = 2
                        LM51305482_202 = 2
                    if lmGenQues.Rows[index1]["Average_Cable_Length_For_PLC_Uplink"] == '5m':
                        LM51305482_105 = 2
                        LM51305482_205 = 2
                    if lmGenQues.Rows[index1]["Average_Cable_Length_For_PLC_Uplink"] == '10m':
                        LM51305482_110 = 2
                        LM51305482_210 = 2
                    if lmGenQues.Rows[index1]["Average_Cable_Length_For_PLC_Uplink"] == '20m':
                        LM51305482_120 = 2
                        LM51305482_220 = 2
                    if lmPLCCont.Rows[index]['LM_average_Cable_length_for_IO_network_connection'] == '2m':
                        if lmGenQues.Rows[index1]["Is_Honeywell_Providing_FTE_Cables"] in ["Yes"] and lmPLCCont.Rows[index]['LM_select_IO_network_topology'] == 'Star':
                            LM51305482_102 = math.ceil(getFloat(attrValDict["900SP1-0200"][-1]) + 2.0 + LM51305482_102)
                        if lmGenQues.Rows[index1]["Is_Honeywell_Providing_FTE_Cables"] in ["Yes"] and lmPLCCont.Rows[index]['LM_select_IO_network_topology'] == 'Ring':
                            LM51305482_102 = math.ceil(getFloat(attrValDict["900SP1-0200"][-1]) + 1.0 + LM51305482_102)
                        if lmGenQues.Rows[index1]["Is_Honeywell_Providing_FTE_Cables"] in ["Yes"] and lmPLCCont.Rows[index]['LM_select_type_of_Switch_for_the_IO_network'] == 'Multimode Redundant':
                            LM51305482_202 = math.ceil(getFloat(attrValDict["900SP1-0200"][-1]) + 2.0 + LM51305482_202)
                        if lmGenQues.Rows[index1]["Is_Honeywell_Providing_FTE_Cables"] in ["Yes"] and lmPLCCont.Rows[index]['LM_select_type_of_Switch_for_the_IO_network'] == 'Single Mode Redundant':
                            LM51305482_202 = math.ceil(getFloat(attrValDict["900SP1-0200"][-1]) + 2.0 + LM51305482_202)
                    if lmPLCCont.Rows[index]['LM_average_Cable_length_for_IO_network_connection'] == '5m':
                        if lmGenQues.Rows[index1]["Is_Honeywell_Providing_FTE_Cables"] in ["Yes"] and lmPLCCont.Rows[index]['LM_select_IO_network_topology'] == 'Star':
                            LM51305482_105 = math.ceil(getFloat(attrValDict["900SP1-0200"][-1]) + 2.0 + LM51305482_105)
                        if lmGenQues.Rows[index1]["Is_Honeywell_Providing_FTE_Cables"] in ["Yes"] and lmPLCCont.Rows[index]['LM_select_IO_network_topology'] == 'Ring':
                            LM51305482_105 = math.ceil(getFloat(attrValDict["900SP1-0200"][-1]) + 1.0 + LM51305482_105)
                        if lmGenQues.Rows[index1]["Is_Honeywell_Providing_FTE_Cables"] in ["Yes"] and lmPLCCont.Rows[index]['LM_select_type_of_Switch_for_the_IO_network'] == 'Multimode Redundant':
                            LM51305482_205 = math.ceil(getFloat(attrValDict["900SP1-0200"][-1]) + 2.0 + LM51305482_205)
                        if lmGenQues.Rows[index1]["Is_Honeywell_Providing_FTE_Cables"] in ["Yes"] and lmPLCCont.Rows[index]['LM_select_type_of_Switch_for_the_IO_network'] == 'Single Mode Redundant':
                            LM51305482_205 = math.ceil(getFloat(attrValDict["900SP1-0200"][-1]) + 2.0 + LM51305482_205)
                    if lmPLCCont.Rows[index]['LM_average_Cable_length_for_IO_network_connection'] == '10m':
                        if lmGenQues.Rows[index1]["Is_Honeywell_Providing_FTE_Cables"] in ["Yes"] and lmPLCCont.Rows[index]['LM_select_IO_network_topology'] == 'Star':
                            LM51305482_110 = math.ceil(getFloat(attrValDict["900SP1-0200"][-1]) + 2.0 + LM51305482_110)
                            Trace.Write("lmPLCCont.Rows[index]['LM_average_Cable_length_for_IO_network_connection']:{0}".format(lmPLCCont.Rows[index]['LM_average_Cable_length_for_IO_network_connection']))
                        if lmGenQues.Rows[index1]["Is_Honeywell_Providing_FTE_Cables"] in ["Yes"] and lmPLCCont.Rows[index]['LM_select_IO_network_topology'] == 'Ring':
                            LM51305482_110 = math.ceil(getFloat(attrValDict["900SP1-0200"][-1]) + 1.0 + LM51305482_110)
                        if lmGenQues.Rows[index1]["Is_Honeywell_Providing_FTE_Cables"] in ["Yes"] and lmPLCCont.Rows[index]['LM_select_type_of_Switch_for_the_IO_network'] == 'Multimode Redundant':
                            LM51305482_210 = math.ceil(getFloat(attrValDict["900SP1-0200"][-1]) + 2.0 + LM51305482_210)
                        if lmGenQues.Rows[index1]["Is_Honeywell_Providing_FTE_Cables"] in ["Yes"] and lmPLCCont.Rows[index]['LM_select_type_of_Switch_for_the_IO_network'] == 'Single Mode Redundant':
                            LM51305482_210 = math.ceil(getFloat(attrValDict["900SP1-0200"][-1]) + 2.0 + LM51305482_210)
                    if lmPLCCont.Rows[index]['LM_average_Cable_length_for_IO_network_connection'] == '20m':
                        if lmGenQues.Rows[index1]["Is_Honeywell_Providing_FTE_Cables"] in ["Yes"] and lmPLCCont.Rows[index]['LM_select_IO_network_topology'] == 'Star':
                            LM51305482_120 = math.ceil(getFloat(attrValDict["900SP1-0200"][-1]) + 2.0 + LM51305482_120)
                        if lmGenQues.Rows[index1]["Is_Honeywell_Providing_FTE_Cables"] in ["Yes"] and lmPLCCont.Rows[index]['LM_select_IO_network_topology'] == 'Ring':
                            LM51305482_120 = math.ceil(getFloat(attrValDict["900SP1-0200"][-1]) + 1.0 + LM51305482_120)
                        if lmGenQues.Rows[index1]["Is_Honeywell_Providing_FTE_Cables"] in ["Yes"] and lmPLCCont.Rows[index]['LM_select_type_of_Switch_for_the_IO_network'] == 'Multimode Redundant':
                            LM51305482_220 = math.ceil(getFloat(attrValDict["900SP1-0200"][-1]) + 2.0 + LM51305482_220)
                        if lmGenQues.Rows[index1]["Is_Honeywell_Providing_FTE_Cables"] in ["Yes"] and lmPLCCont.Rows[index]['LM_select_type_of_Switch_for_the_IO_network'] == 'Single Mode Redundant':
                            LM51305482_220 = math.ceil(getFloat(attrValDict["900SP1-0200"][-1]) + 2.0 + LM51305482_220)
            if ot == "Extended -40 to 70 DegC":
                Trace.Write("HII")
                l = attrValDict.get("900SP1-0300",list())
                l.append(getFloat(0 if attrValDict.get("LM900R08_0200") is None else attrValDict["LM900R08_0200"][-1]) + getFloat(0 if attrValDict.get("LM900R08R_0200") is None else attrValDict["LM900R08R_0200"][-1]) + getFloat(0 if attrValDict.get("LM900R12_0200") is None else attrValDict["LM900R12_0200"][-1]) + getFloat(0 if attrValDict.get("LM900R12R_0200") is None else attrValDict["LM900R12R_0200"][-1]))
                attrValDict["900SP1-0300"] = l
                if lmGenQues.Rows[index1]["Is_Honeywell_Providing_FTE_Cables"] in ["Yes"] :
                    if lmGenQues.Rows[index1]["Average_Cable_Length_For_PLC_Uplink"] == '2m':
                        LM51305482_102 = 2
                        LM51305482_202 = 2
                    if lmGenQues.Rows[index1]["Average_Cable_Length_For_PLC_Uplink"] == '5m':
                        LM51305482_105 = 2
                        LM51305482_205 = 2
                    if lmGenQues.Rows[index1]["Average_Cable_Length_For_PLC_Uplink"] == '10m':
                        LM51305482_110 = 2
                        LM51305482_210 = 2
                    if lmGenQues.Rows[index1]["Average_Cable_Length_For_PLC_Uplink"] == '20m':
                        LM51305482_120 = 2
                        LM51305482_220 = 2
                    if lmPLCCont.Rows[index]['LM_average_Cable_length_for_IO_network_connection'] == '2m':
                        if lmGenQues.Rows[index1]["Is_Honeywell_Providing_FTE_Cables"] in ["Yes"] and lmPLCCont.Rows[index]['LM_select_IO_network_topology'] == 'Star':
                            LM51305482_102 = math.ceil(getFloat(attrValDict["900SP1-0300"][-1]) + 2.0 + LM51305482_102)
                        if lmGenQues.Rows[index1]["Is_Honeywell_Providing_FTE_Cables"] in ["Yes"] and lmPLCCont.Rows[index]['LM_select_IO_network_topology'] == 'Ring':
                            LM51305482_102 = math.ceil(getFloat(attrValDict["900SP1-0300"][-1]) + 1.0 + LM51305482_102)
                        if lmGenQues.Rows[index1]["Is_Honeywell_Providing_FTE_Cables"] in ["Yes"] and lmPLCCont.Rows[index]['LM_select_type_of_Switch_for_the_IO_network'] == 'Multimode Redundant':
                            LM51305482_202 = math.ceil(getFloat(attrValDict["900SP1-0300"][-1]) + 2.0 + LM51305482_202)
                        if lmGenQues.Rows[index1]["Is_Honeywell_Providing_FTE_Cables"] in ["Yes"] and lmPLCCont.Rows[index]['LM_select_type_of_Switch_for_the_IO_network'] == 'Single Mode Redundant':
                            LM51305482_202 = math.ceil(getFloat(attrValDict["900SP1-0300"][-1]) + 2.0 + LM51305482_202)
                    if lmPLCCont.Rows[index]['LM_average_Cable_length_for_IO_network_connection'] == '5m':
                        if lmGenQues.Rows[index1]["Is_Honeywell_Providing_FTE_Cables"] in ["Yes"] and lmPLCCont.Rows[index]['LM_select_IO_network_topology'] == 'Star':
                            LM51305482_105 = math.ceil(getFloat(attrValDict["900SP1-0300"][-1]) + 2.0 + LM51305482_105)
                        if lmGenQues.Rows[index1]["Is_Honeywell_Providing_FTE_Cables"] in ["Yes"] and lmPLCCont.Rows[index]['LM_select_IO_network_topology'] == 'Ring':
                            LM51305482_105 = math.ceil(getFloat(attrValDict["900SP1-0300"][-1]) + 1.0 + LM51305482_105)
                        if lmGenQues.Rows[index1]["Is_Honeywell_Providing_FTE_Cables"] in ["Yes"] and lmPLCCont.Rows[index]['LM_select_type_of_Switch_for_the_IO_network'] == 'Multimode Redundant':
                            LM51305482_205 = math.ceil(getFloat(attrValDict["900SP1-0300"][-1]) + 2.0 + LM51305482_205)
                        if lmGenQues.Rows[index1]["Is_Honeywell_Providing_FTE_Cables"] in ["Yes"] and lmPLCCont.Rows[index]['LM_select_type_of_Switch_for_the_IO_network'] == 'Single Mode Redundant':
                            LM51305482_205 = math.ceil(getFloat(attrValDict["900SP1-0300"][-1]) + 2.0 + LM51305482_205)
                    if lmPLCCont.Rows[index]['LM_average_Cable_length_for_IO_network_connection'] == '10m':
                        if lmGenQues.Rows[index1]["Is_Honeywell_Providing_FTE_Cables"] in ["Yes"] and lmPLCCont.Rows[index]['LM_select_IO_network_topology'] == 'Star':
                            LM51305482_110 = math.ceil(getFloat(attrValDict["900SP1-0300"][-1]) + 2.0 + LM51305482_110)
                            Trace.Write("lmPLCCont.Rows[index]['LM_average_Cable_length_for_IO_network_connection']:{0}".format(lmPLCCont.Rows[index]['LM_average_Cable_length_for_IO_network_connection']))
                        if lmGenQues.Rows[index1]["Is_Honeywell_Providing_FTE_Cables"] in ["Yes"] and lmPLCCont.Rows[index]['LM_select_IO_network_topology'] == 'Ring':
                            LM51305482_110 = math.ceil(getFloat(attrValDict["900SP1-0300"][-1]) + 1.0 + LM51305482_110)
                        if lmGenQues.Rows[index1]["Is_Honeywell_Providing_FTE_Cables"] in ["Yes"] and lmPLCCont.Rows[index]['LM_select_type_of_Switch_for_the_IO_network'] == 'Multimode Redundant':
                            LM51305482_210 = math.ceil(getFloat(attrValDict["900SP1-0300"][-1]) + 2.0 + LM51305482_210)
                        if lmGenQues.Rows[index1]["Is_Honeywell_Providing_FTE_Cables"] in ["Yes"] and lmPLCCont.Rows[index]['LM_select_type_of_Switch_for_the_IO_network'] == 'Single Mode Redundant':
                            LM51305482_210 = math.ceil(getFloat(attrValDict["900SP1-0300"][-1]) + 2.0 + LM51305482_210)
                    if lmPLCCont.Rows[index]['LM_average_Cable_length_for_IO_network_connection'] == '20m':
                        if lmGenQues.Rows[index1]["Is_Honeywell_Providing_FTE_Cables"] in ["Yes"] and lmPLCCont.Rows[index]['LM_select_IO_network_topology'] == 'Star':
                            LM51305482_120 = math.ceil(getFloat(attrValDict["900SP1-0300"][-1]) + 2.0 + LM51305482_120)
                        if lmGenQues.Rows[index1]["Is_Honeywell_Providing_FTE_Cables"] in ["Yes"] and lmPLCCont.Rows[index]['LM_select_IO_network_topology'] == 'Ring':
                            LM51305482_120 = math.ceil(getFloat(attrValDict["900SP1-0300"][-1]) + 1.0 + LM51305482_120)
                        if lmGenQues.Rows[index1]["Is_Honeywell_Providing_FTE_Cables"] in ["Yes"] and lmPLCCont.Rows[index]['LM_select_type_of_Switch_for_the_IO_network'] == 'Multimode Redundant':
                            LM51305482_220 = math.ceil(getFloat(attrValDict["900SP1-0300"][-1]) + 2.0 + LM51305482_220)
                        if lmGenQues.Rows[index1]["Is_Honeywell_Providing_FTE_Cables"] in ["Yes"] and lmPLCCont.Rows[index]['LM_select_type_of_Switch_for_the_IO_network'] == 'Single Mode Redundant':
                            LM51305482_220 = math.ceil(getFloat(attrValDict["900SP1-0300"][-1]) + 2.0 + LM51305482_220)

        l = attrValDict.get("LM51305482_102",list())
        l.append(LM51305482_102)
        attrValDict["LM51305482_102"]=l

        l = attrValDict.get("LM51305482_202",list())
        l.append(LM51305482_202)
        attrValDict["LM51305482_202"]=l

        l = attrValDict.get("LM51305482_105",list())
        l.append(LM51305482_105)
        attrValDict["LM51305482_105"]=l

        l = attrValDict.get("LM51305482_205",list())
        l.append(LM51305482_205)
        attrValDict["LM51305482_205"]=l

        l = attrValDict.get("LM51305482_110",list())
        l.append(LM51305482_110)
        attrValDict["LM51305482_110"]=l

        l = attrValDict.get("LM51305482_210",list())
        l.append(LM51305482_210)
        attrValDict["LM51305482_210"]=l

        l = attrValDict.get("LM51305482_120",list())
        l.append(LM51305482_120)
        attrValDict["LM51305482_120"]=l

        l = attrValDict.get("LM51305482_220",list())
        l.append(LM51305482_220)
        attrValDict["LM51305482_220"]=l

        for row1 in lmGenQues.Rows:
            index1 = row1.RowIndex
            if lmGenQues.Rows[index1]["LM_to_ELMM_ControlEdge_PLC_Operating_temperature"] == "0 to 60 DegC or Marine application":
                if row['LM_do_you_have_additional_space_in_the_cabinet_room_to_mount_the_CE_System'] in ["No", ""] and row['LM_are_the_IO_Racks_remotely_located'] != "Yes - Only Remote" and getFloat(attrValDict["900SP1-0200"][-1]) <= 6:
                    THIRDPARTY_CABINET = 1
                if row['LM_do_you_have_additional_space_in_the_cabinet_room_to_mount_the_CE_System'] in ["No", ""] and row['LM_are_the_IO_Racks_remotely_located'] != "Yes - Only Remote" and getFloat(attrValDict["900SP1-0200"][-1]) > 6:
                    THIRDPARTY_CABINET = 2
            if lmGenQues.Rows[index1]["LM_to_ELMM_ControlEdge_PLC_Operating_temperature"] == "Extended -40 to 70 DegC":
                if row['LM_do_you_have_additional_space_in_the_cabinet_room_to_mount_the_CE_System'] in ["No", ""] and row['LM_are_the_IO_Racks_remotely_located'] != "Yes - Only Remote" and getFloat(attrValDict["900SP1-0300"][-1]) <= 6:
                    THIRDPARTY_CABINET = 1
                if row['LM_do_you_have_additional_space_in_the_cabinet_room_to_mount_the_CE_System'] in ["No", ""] and row['LM_are_the_IO_Racks_remotely_located'] != "Yes - Only Remote" and getFloat(attrValDict["900SP1-0300"][-1]) > 6:
                    THIRDPARTY_CABINET = 2
        #if row['LM_do_you_have_additional_space_in_the_cabinet_room_to_mount_the_CE_System'] in ["No", ""] and row['LM_are_the_IO_Racks_remotely_located'] != "Yes - Only Remote" and getFloat(attrValDict["900SP1-0300"][-1]) <= 6:
        #    THIRDPARTY_CABINET = 1
        #if row['LM_do_you_have_additional_space_in_the_cabinet_room_to_mount_the_CE_System'] in ["No", ""] and row['LM_are_the_IO_Racks_remotely_located'] != "Yes - Only Remote" and getFloat(attrValDict["900SP1-0300"][-1]) > 6:
        #    THIRDPARTY_CABINET = 2

        l = attrValDict.get("ThridParty_Cabinet",list())
        l.append(THIRDPARTY_CABINET)
        attrValDict["ThridParty_Cabinet"] = l

        Switch= "Multimode Redundant" if lmPLCCont.Rows[index]["LM_select_type_of_Switch_for_the_IO_network"]=="" else lmPLCCont.Rows[index]["LM_select_type_of_Switch_for_the_IO_network"]
        PLC_Remote= 0 if lmRemoteIO.Rows[index]["no_of_PLC_Remote_IO_group_0_16"] =="" else getInt(lmRemoteIO.Rows[index]["no_of_PLC_Remote_IO_group_0_16"])
        Trace.Write('---------------')
        Trace.Write(RestClient.SerializeToJson(attrValDict))
        #Trace.Write(IO_Racks_Location+'-'+Switch+'attrValDict["900SP1-0300"]-'+str(attrValDict["900SP1-0300"][-1])+'-'+str(Total_Remote_Serial)+'-'+str(PLC_Remote))
        for row1 in lmGenQues.Rows:
            index1 = row1.RowIndex
            ot = lmGenQues.Rows[index1]["LM_to_ELMM_ControlEdge_PLC_Operating_temperature"]
            Trace.Write("OT1:{0}".format(ot))
            if ot == "0 to 60 DegC or Marine application":
                Trace.Write("HII")
                res = Calcualte_BOM_IO_Switch(IO_Racks_Location,Switch,str(math.ceil(attrValDict["900SP1-0200"][-1])),str(Total_Remote_Serial),str(PLC_Remote))
            if ot == "Extended -40 to 70 DegC":
                res = Calcualte_BOM_IO_Switch(IO_Racks_Location,Switch,str(math.ceil(attrValDict["900SP1-0300"][-1])),str(Total_Remote_Serial),str(PLC_Remote))
                Trace.Write('RES:{0}'.format(str(res)))
        #res = Calcualte_BOM_IO_Switch(IO_Racks_Location,Switch,str(math.ceil(attrValDict["900SP1-0300"][-1])),str(Total_Remote_Serial),str(PLC_Remote))
        if res != None:
            if res.QTY_50008930_001 > 0:
                l = attrValDict.get("LM_50008930_001",list())
                l.append(getInt(res.QTY_50008930_001))
                attrValDict["LM_50008930_001"] = l
            if res.QTY_50008930_002 > 0:
                l = attrValDict.get("LM_50008930_002",list())
                l.append(getInt(res.QTY_50008930_002))
                attrValDict["LM_50008930_002"] = l
            if res.QTY_50008930_003 > 0:
                l = attrValDict.get("LM_50008930_003",list())
                l.append(getInt(res.QTY_50008930_003))
                attrValDict["LM_50008930_003"] = l
            if res.QTY_50008930_004 > 0:
                l = attrValDict.get("LM_50008930_004",list())
                l.append(getInt(res.QTY_50008930_004))
                attrValDict["LM_50008930_004"] = l
    Trace.Write("MigrationUtil4")
    Trace.Write(RestClient.SerializeToJson(attrValDict))
def populateSparePartCabinetSummary(product, partsList):
    sparePartsCabinetDict = dict()
    sparePartsCon = getContainer(product,"Spare_Parts")
    for row in sparePartsCon.Rows:
        if row["Spare_Parts_Quantity"] > 0:
            if row["Spare_Parts_Part_Number"] not in partsList:
                partsList.add(row["Spare_Parts_Part_Number"])
            sparePartsCabinetDict[row["Spare_Parts_Part_Number"]] = row["Spare_Parts_Quantity"]
    
    sparePartsCabinetCon = getContainer(product,"Spare_Parts_Rolled_PS")
    for row in sparePartsCabinetCon.Rows:
        if row["Quantity"] > 0:
            if row["Part_Number"] not in partsList:
                partsList.add(row["Part_Number"])
            sparePartsCabinetDict[row["Part_Number"]] = row["Quantity"]
    return sparePartsCabinetDict