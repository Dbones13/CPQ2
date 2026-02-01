def getContainer(containerName):
     return Product.GetContainerByName(containerName)
def getContainerColSum(containerName , rowId):
    container = getContainer(containerName)
    sum = 0
    for row in container.Rows:
        if row.RowIndex == rowId:
            for col in row.Columns:
                try:
                    sum += float(row[col.Name])
                except:
                    pass
    return sum > 0
incomplete = []
if Product.Name == "LCN One Time Upgrade":
    if not getContainerColSum("LCN_Design_Inputs_for_TPN_OTU_Upgrade" , 0):
        incomplete.append("LCN_Design_Inputs_for_TPN_OTU_Upgrade")
Product.Attr('Incomplete').AssignValue(",".join(incomplete))