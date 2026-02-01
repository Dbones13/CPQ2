def getInt(num):
    if num:
        return int(num)
    return 0

def getCgData(curRow):
    thisData = dict()
    con = curRow.Product.GetContainerByName("RTU_CG_Cabinet_Cont")
    row = con.Rows[0]
    thisData["Cabinet_Type"] = row["Cabinet_Type"]
    thisData["Cabinet_Spare_space"] = row["Cabinet_Spare_space"]
    thisData["Integrated_Marshalling_Cabinet"] = row["Integrated_Marshalling_Cabinet"]
    con = curRow.Product.GetContainerByName("RTU_CG_Controller_Cont")
    row = con.Rows[0]
    thisData["Power_Supply_Type"] = row["Power_Supply_Type"]

    thisData["IOCount"] = 0
    con = curRow.Product.GetContainerByName("RTU_CG_IO_Container")
    for row in con.Rows:
        thisData["IOCount"] += getInt(row["Non_HART_Analog_Input"])
        thisData["IOCount"] += getInt(row["HART_Analog_Input"])
        thisData["IOCount"] += getInt(row["Non_HART_Analog_Output"])
        thisData["IOCount"] += getInt(row["HART_Analog_Output"])
        thisData["IOCount"] += getInt(row["Digital_Input"])
        thisData["IOCount"] += getInt(row["Digital_Output"])
        thisData["IOCount"] += getInt(row["Pulse_Input"])
        thisData["IOCount"] += getInt(row["FIM_Analog_Input"])
        thisData["IOCount"] += getInt(row["Field_ISA100_Wireless_Devices"])

    con = curRow.Product.GetContainerByName("RTU_CG_Labor_Cont")
    for row in con.Rows:
        thisData["RTU_Similar_Control_Groups"] = row["RTU_Similar_Control_Groups"]
        Trace.Write("checkingg---->"+str(row["RTU_Similar_Control_Groups"]))
        break
    return thisData


cgData = Product.Attr("RTU_ControlGroupsData")
con = Product.GetContainerByName("RTU_ControlGroup_Cont")
data = list()
for row in con.Rows:
    data.append(getCgData(row))
cgData.AssignValue(RestClient.SerializeToJson(data))