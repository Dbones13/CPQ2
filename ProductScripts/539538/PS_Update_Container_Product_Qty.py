cont = Product.GetContainerByName('Experion_HS_PartSummary_Cont')
if cont.Rows.Count > 0:
    for row in cont.Rows:
        row.IsSelected = True
        row.Calculate()
        for attr in filter(lambda a : a.DisplayType != "Container", row.Product.Attributes):
            if attr.Name == "ItemQuantity":
                attr.AssignValue(row["Final_Quantity"])
        row.ApplyProductChanges()
    cont.Calculate()