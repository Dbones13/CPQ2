check = Product.Attr("Enterprise_flag_check").GetValue()
if check == "True":
    cont = Product.GetContainerByName("Experion_Enterprise_Cont")
    if cont.Rows.Count > 0:
        enterprise = ""
        for row in cont.Rows:
            enterprise = "| ".join((enterprise,(str(row.RowIndex)+"#" + row["Experion Enterprise Group Name"])))
        Product.Attr("Enterprise Groups list").AssignValue(enterprise[2:])