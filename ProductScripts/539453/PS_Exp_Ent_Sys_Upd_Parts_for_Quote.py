cont = Product.GetContainerByName('Exp_Ent_Sys_Part_Summary_Cont')
if cont.Rows.Count > 0:
	for row in cont.Rows:
		update=False
		if int(row["Final_Quantity"]) > 0:
			if row.IsSelected == False:
				row.IsSelected = True
				row.Calculate()
				update=True
			if row.Product.Attributes.GetByName('ItemQuantity'):
				if int(row["Final_Quantity"]) !=  row.Product.Attr('ItemQuantity').GetValue():
					row.Product.Attr('ItemQuantity').AssignValue(row["Final_Quantity"])
					update=True
			else:
				Product.ErrorMessages.Add('Item Quantity missing from part number {}, please contact the Admin'.format(row.Product.PartNumber))
			if update == True:
				row.ApplyProductChanges
		else:
			if row.IsSelected == True:
				row.IsSelected = False
	cont.Calculate()