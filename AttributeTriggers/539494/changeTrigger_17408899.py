def getContainer(Name):
    return Product.GetContainerByName(Name)


if Product.Attr("MXP_Platform_Type").GetValue() == "Physical":
    count = int(Product.Attr("MXP_Number_of_Operator_Station").GetValue())
    cont = getContainer("MXP_Operator_station_transpose")
    rowCount = cont.Rows.Count

    if rowCount < count:
        for i in range(rowCount,count):
            r = cont.AddNewRow(False)
        cont.Calculate()
    elif rowCount > count:
        flag = 0
        for i in range(count,rowCount):
            flag += 1
            cont.DeleteRow(rowCount-flag)
        cont.Calculate()
ScriptExecutor.Execute('PS_Rae_Operator_Parts')