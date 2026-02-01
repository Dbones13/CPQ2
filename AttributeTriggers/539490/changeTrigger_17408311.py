def getContainer(Name):
    return Product.GetContainerByName(Name)


if Product.Attr("MX_Platform_Type").GetValue() == "Physical":
    count = int(Product.Attr("MX_number_of_operator_station").GetValue())
    cont = getContainer("MX_Operator_station_transpose")
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