def getInt(val):
    try:
        return int(val)
    except:
        return 0

conAttrDict = {
    "Labor_parameter_ai" : ["SM_IO_Count_Analog_Input_Cont"],
    "Labor_parameter_ao" : ["SM_IO_Count_Analog_Output_Cont"],
    "Labor_parameter_di" : ["SM_IO_Count_Digital_Input_Cont", "SM_CG_DI_RLY_NMR_Cont"],
    "Labor_parameter_do" : ["SM_IO_Count_Digital_Output_Cont", "SM_CG_DO_RLY_NMR_Cont"],
}
isColumns = {"Red (IS)", "Non Red (IS)"}
rgContTotalString = "<*CTX( Container(SM_RemoteGroup_Cont).Sum({}) )*>"
isTotal = 0
rgTotalIo = 0
for attr, conNames in conAttrDict.items():
    total = 0
    for conName in conNames:
        con = Product.GetContainerByName(conName)
        for row in con.Rows:
            for col in filter(lambda col:col.Name != "Rank" and not col.Name.endswith("Type"), row.Columns):
                if col.Name in isColumns:
                    isTotal += getInt(col.Value)
                total += getInt(col.Value)
    rgTotal = TagParserProduct.ParseString(rgContTotalString.format(attr))
    rgTotalIo += getInt(rgTotal)
    Product.Attr(attr).AssignValue(str(getInt(rgTotal) + total))

Product.Attr("doc_parameter_remote_io").AssignValue(str(rgTotalIo))

rgIsValue = TagParserProduct.ParseString(rgContTotalString.format("Labor_parameter_is"))
if getInt(rgIsValue) + isTotal > 0:
    Product.Attr("Labor_parameter_is").AssignValue("1")
else:
    Product.Attr("Labor_parameter_is").AssignValue("0")