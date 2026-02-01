def getContainer(Name):
    return Product.GetContainerByName(Name)
count = int(Product.Attr("VS_Number_of_Clusters_in_the_network").GetValue()) if Product.Attr('VS_Number_of_Clusters_in_the_network').GetValue().isdigit() else 0
Trace.Write("cluster_count="+str(count))
cont = getContainer("Virtualization_cluster_transpose")
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
Trace.Write("cluster_count1="+str(Product.Attr('VS_Number_of_Clusters_in_the_network').GetValue()))