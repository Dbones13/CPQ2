def getContainer(Name):
    return Product.GetContainerByName(Name)


count = int(Product.Attr("MXP_Number_of_Thin_Clients").GetValue())
cont = getContainer("MXP_RAE_Thinclient_transpose")
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