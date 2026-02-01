def getInt(num):
    if num:
        return int(num)
    return 0

def disallowCgList(disallowLs):
    options = {"CG1","CG2","CG3","CG4","CG5","CG6","CG7","CG8","CG9","CG10"}
    con = Product.GetContainerByName("RTU_CG_Labor_Cont")
    for row in con.Rows:
        row.Product.AllowAttrValues("RTU_Similar_Control_Groups", *options)
        row.Product.DisallowAttrValues("RTU_Similar_Control_Groups",*disallowList)
        row.ApplyProductChanges()
        row.Calculate()
        break

def checkCgSimilar(curCgData, newCgData):
    if str(newCgData["RTU_Similar_Control_Groups"]) not in ("", "NA"):
        Trace.Write("PS_RestrictSimilarCG : CG already similiar to other")
        return False
    for key, value in curCgData.items():
        Trace.Write(value)
        if key not in ("IOCount","RTU_Similar_Control_Groups") and newCgData[key] != value:
            Trace.Write("PS_RestrictSimilarCG : variables not matched")
            return False
    if newCgData["IOCount"] * .95 > curCgData["IOCount"] or newCgData["IOCount"] * 1.05 < curCgData["IOCount"]:
        Trace.Write("PS_RestrictSimilarCG : IOCount not matched")
        return False
    return True

con = Product.GetContainerByName("RTU_CG_Cabinet_Cont")
currentCgData = dict()
for row in con.Rows:
    currentCgData["Cabinet_Type"] = row["Cabinet_Type"]
    currentCgData["Cabinet_Spare_space"] = row["Cabinet_Spare_space"]
    currentCgData["Integrated_Marshalling_Cabinet"] = row["Integrated_Marshalling_Cabinet"]
con = Product.GetContainerByName("RTU_CG_Controller_Cont")

for row in con.Rows:
    currentCgData["Power_Supply_Type"] = row["Power_Supply_Type"]
currentCgData["IOCount"] = 0
con = Product.GetContainerByName("RTU_CG_IO_Container")
for row in con.Rows:
    currentCgData["IOCount"] += getInt(row["Non_HART_Analog_Input"])
    currentCgData["IOCount"] += getInt(row["HART_Analog_Input"])
    currentCgData["IOCount"] += getInt(row["Non_HART_Analog_Output"])
    currentCgData["IOCount"] += getInt(row["HART_Analog_Output"])
    currentCgData["IOCount"] += getInt(row["Digital_Input"])
    currentCgData["IOCount"] += getInt(row["Digital_Output"])
    currentCgData["IOCount"] += getInt(row["Pulse_Input"])
    currentCgData["IOCount"] += getInt(row["FIM_Analog_Input"])
    currentCgData["IOCount"] += getInt(row["Field_ISA100_Wireless_Devices"])
cgData = Product.Attr("RTU_ControlGroupsData")
cgData = RestClient.DeserializeJson(cgData.GetValue())

cgIndex = Product.Attr("RTU_CG_Index").GetValue()
cgIndex = int(cgIndex) if cgIndex else 0
disallowList = {"CG1","CG2","CG3","CG4","CG5","CG6","CG7","CG8","CG9","CG10"}

if cgIndex == 0:
    disallowCgList(disallowList)
    TagParserProduct.ParseString('<*CTX( Container(RTU_CG_Labor_Cont).Column(RTU_Similar_Control_Groups).SetPermission(Hidden) )*>')
    Trace.Write("PS_RestrictSimilarCG : Index 0 should hide column")
else:
    for i, data in enumerate(cgData):
        if i != cgIndex and checkCgSimilar(currentCgData, data):
            Trace.Write("PS_RestrictSimilarCG : Should be allowed CG{}".format(i+1))
            disallowList.discard("CG{}".format(i+1))
    disallowCgList(disallowList)
    TagParserProduct.ParseString('<*CTX( Container(RTU_CG_Labor_Cont).Column(RTU_Similar_Control_Groups).SetPermission(Editable) )*>')