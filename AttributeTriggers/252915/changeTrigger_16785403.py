def getContainer(Name):
    return Product.GetContainerByName(Name)

count = int(Product.Attr("LSS_PLC_Number_of_ControlEdge_UOC_vUOC_confi_req").GetValue())
cont = getContainer("LSS_UOC_connection_transpose")
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