check = Product.Attr("Enterprise_flag_check").GetValue()
if check == "True":
    Enterprise_Groups_list=""
    cluster1=""
    cluster2=""
    cluster3=""
    cluster4=""
    cluster5=""
    cluster6=""
    cluster7=""
    cluster8=""
    cluster9=""
    cluster10=""
    for row in Product.GetContainerByName("CE_System_Cont").Rows:
        system_Product = row.Product
        if system_Product.Name=="Experion Enterprise System":
            Enterprise_Groups_list = system_Product.Attributes.GetByName("Enterprise Groups list").GetValue()
            for row1 in system_Product.GetContainerByName("Experion_Enterprise_Cont").Rows:
                clusterProduct = row1.Product
                if row1.RowIndex == 0:
                    cluster1=clusterProduct.Attributes.GetByName("Location server list").GetValue()
                elif row1.RowIndex == 1:
                    cluster2=clusterProduct.Attributes.GetByName("Location server list").GetValue()
                elif row1.RowIndex == 2:
                    cluster3=clusterProduct.Attributes.GetByName("Location server list").GetValue()
                elif row1.RowIndex == 3:
                    cluster4=clusterProduct.Attributes.GetByName("Location server list").GetValue()
                elif row1.RowIndex == 4:
                    cluster5=clusterProduct.Attributes.GetByName("Location server list").GetValue()
                elif row1.RowIndex == 5:
                    cluster6=clusterProduct.Attributes.GetByName("Location server list").GetValue()
                elif row1.RowIndex == 6:
                    cluster7=clusterProduct.Attributes.GetByName("Location server list").GetValue()
                elif row1.RowIndex == 7:
                    cluster8=clusterProduct.Attributes.GetByName("Location server list").GetValue()
                elif row1.RowIndex == 8:
                    cluster9=clusterProduct.Attributes.GetByName("Location server list").GetValue()
                elif row1.RowIndex == 9:
                    cluster10=clusterProduct.Attributes.GetByName("Location server list").GetValue()
            break

    for row in Product.GetContainerByName("CE_System_Cont").Rows:
        system_Product = row.Product
        if system_Product.Name in ("Safety Manager ESD","Safety Manager BMS","Safety Manager HIPPS","Safety Manager FGS","Electrical Substation Data Collector","C300 System","Field Device Manager","eServer System","ARO, RESS & ERG System"):
            system_Product.Attr("Enterprise_Groups_list").AssignValue(Enterprise_Groups_list)
            system_Product.Attr("cluster1").AssignValue(cluster1)
            system_Product.Attr("cluster2").AssignValue(cluster2)
            system_Product.Attr("cluster3").AssignValue(cluster3)
            system_Product.Attr("cluster4").AssignValue(cluster4)
            system_Product.Attr("cluster5").AssignValue(cluster5)
            system_Product.Attr("cluster6").AssignValue(cluster6)
            system_Product.Attr("cluster7").AssignValue(cluster7)
            system_Product.Attr("cluster8").AssignValue(cluster8)
            system_Product.Attr("cluster9").AssignValue(cluster9)
            system_Product.Attr("cluster10").AssignValue(cluster10)
            row.ApplyProductChanges()
            row.Product.ApplyRules()