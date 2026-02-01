def getContainer(Name):
    return Product.GetContainerByName(Name)

if Product.Attr("Virtualization_Platform_Options").GetValue() == "Premium Platforms Gen 3 - Performance A/B":
    count = int(Product.Attr("Virtualization_Number_of_Clusters_in_the_network").GetValue())
    Start = int(Product.Attr("Virtualization_Enter_the_starting_Cluster_Number").GetValue())
    if count > 0:
        cont = getContainer("Virtualization_cluster_transpose")
        rowCount = cont.Rows.Count
        if rowCount > 0:
            check = cont.Rows[0]["Cluster"]
            checkStart = check[-2:]
            if int(checkStart) != Start:
                cont.Rows.Clear()
                rowCount = 0

        if rowCount < count:
            for i in range(rowCount,count):
                r = cont.AddNewRow(False)
                if (i+Start) > 9:
                    r["Cluster"] = "Cluster#"+str(i+Start)
                else:
                    r["Cluster"] = "Cluster#0"+str(i+Start)
            cont.Calculate()
        elif rowCount > count:
            flag = 0
            for i in range(count,rowCount):
                flag += 1
                cont.DeleteRow(rowCount-flag)
            cont.Calculate()