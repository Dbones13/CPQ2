def refreshContainer(Product):
    cont = ""
    if Product.Name == "Series-C Control Group":
        cont = Product.GetContainerByName('Series_C_CG_Part_Summary_Cont')
    elif Product.Name == "Series-C Remote Group":
        cont = Product.GetContainerByName('Series_C_RG_Part_Summary_Cont')
    if cont:
        if cont.Rows.Count > 0:
            for row in cont.Rows:
                if int(row["Final_Quantity"]) > 0:
                    row.IsSelected = True
                    row.Calculate()
                    for attr in filter(lambda a : a.DisplayType != "Container", row.Product.Attributes):
                        if attr.Name == "ItemQuantity":
                            attr.AssignValue(row["Final_Quantity"])
                    row.ApplyProductChanges()
                else:
                    row.IsSelected = False
            cont.Calculate()