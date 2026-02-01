skidCon = Product.GetContainerByName("PRODUCTIZED _SKID_BOM")
sparts_Con = Product.GetContainerByName("Pskid_SimpleParts_Cont")
sparts_Con.Rows.Clear()
for Vrow in skidCon.Rows:
    if str(Vrow['Type'])=='CP' and  str(Vrow['Error Message'])=='' and str(Vrow['Part Number'])!='':
        new_row = sparts_Con.AddNewRow(False)
        new_row['Partnumber'] = str(Vrow['Part Number'])
        new_row['Part_Qty'] = str(Vrow['Qty'])
        new_row.IsSelected = True
        for attr in filter(lambda a : a.DisplayType != "Container", new_row.Product.Attributes):
            if attr.Name == "ItemQuantity":
                attr.AssignValue(str(Vrow['Qty']))
            new_row.ApplyProductChanges()
        
        new_row.Calculate()