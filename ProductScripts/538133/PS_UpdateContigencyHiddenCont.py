contigency_hidden_cont = Product.GetContainerByName("SC_P1P2_Contigency_Cost_Hidden")
contigency_cont = Product.GetContainerByName("SC_P1P2_Contigency_Cost")
if contigency_cont.Rows.Count:
    for row in contigency_cont.Rows:
        for hiddenrow in contigency_hidden_cont.Rows:
            if row["Service_Product"] == hiddenrow["Service_Product"]:
                hiddenrow["CY_Cost"] = row["CY_Cost"]
                hiddenrow.Calculate()
    contigency_hidden_cont.Calculate()