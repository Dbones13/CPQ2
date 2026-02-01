a=Product.GetContainerByName('PMC_Generic_System_Cont')
for row in a.Rows:
    HONProductCon = row.Product.GetContainerByName("Generic_System_BOM_Part_Cont")
    if HONProductCon:
    	for row2 in HONProductCon.Rows:
    		row2.Product.Attr("ItemQuantity").AssignValue(str(row2['Quantity']))
    		row2.Calculate()

a=Product.GetContainerByName('CE_System_Cont')
for row in a.Rows:
    if row.Product.Name in('Experion LX Generic','MasterLogic-50 Generic','MasterLogic-200 Generic'):
        HONProductCon = row.Product.GetContainerByName("Generic_System_BOM_Part_Cont")
        for row2 in HONProductCon.Rows:
            row2.Product.Attr("ItemQuantity").AssignValue(str(row2['Quantity']))
            row2.Calculate()