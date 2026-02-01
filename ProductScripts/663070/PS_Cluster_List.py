check = Product.Attr("Enterprise_flag_check").GetValue()
if check == "True":
    cont = Product.GetContainerByName("List of Locations/Clusters/Network Groups")
    if cont.Rows.Count > 0:
        enterprise = ""
        for row in cont.Rows:
            enterprise = "| ".join((enterprise,(str(row.RowIndex)+"#"+row["List of Locations/Clusters/ Network Groups"])))
        Product.Attr("Location server list").AssignValue(enterprise[1:])