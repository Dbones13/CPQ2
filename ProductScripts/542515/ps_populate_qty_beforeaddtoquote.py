HONProductCon = Product.GetContainerByName("Generic_System_BOM_Part_Cont")
for row in HONProductCon.Rows:
    row.Product.Attr("ItemQuantity").AssignValue(str(row['Quantity']))
    row.Calculate()