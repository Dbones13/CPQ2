def getContainer(Name):
    return Product.GetContainerByName(Name)

if Product.Attr("Virtualization_Platform_Options").GetValue() == "Premium Platforms-Dell Servers":
    flag = ''
    count = int(Product.Attr("Virtualization_Number_of_Clusters_in_the_network").GetValue())
    if count > 0:
        cont = getContainer("Virtualization_cluster_transpose")
        rowCount = cont.Rows.Count
        if rowCount > 0:
            for row in cont.Rows:
                if (int(row["Virtualization_Number_of_A_VxRail_E660_Servers"]) <3 and int(row["Virtualization_Number_of_B_VxRail_E660_Servers"]) <3) or ( int(row["Virtualization_Number_of_A_VxRail_E660_Servers"]) + int(row["Virtualization_Number_of_B_VxRail_E660_Servers"]) ) > 9:
                    flag = "VirtualizationIncomplete"
                    break


            Product.Attr('Virtualization_Incomplete').AssignValue(flag)