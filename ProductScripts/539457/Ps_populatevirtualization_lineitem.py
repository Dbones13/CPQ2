def updateChildAttributes(row, productRow):
	if not row.Product:
		return
	for attr in filter(lambda a : a.DisplayType != "Container", row.Product.Attributes):
		if attr.Name == "ItemQuantity":
			attr.AssignValue(row["Quantity"])
			continue
		value = getAttrValue(attr.Name, row.Product.PartNumber, productRow.Product.Name)
		if value:
			value = value[0] if type(value) == type([]) else value
			if attr.DisplayType == "FreeInputNoMatching":
				attr.AssignValue(value)
				continue
			attr.SelectValue(value)

contGen = Product.GetContainerByName("Virtualization_partsummary_cont")
lineItemContainer = Product.GetContainerByName("MSID_Added_Parts_Common_Container")
lineItemContainer.Clear()
for row in contGen.Rows:
	qty = row["CE_Final_Quantity"] if row["CE_Final_Quantity"] else 0
	if float(qty):
		childRow = lineItemContainer.AddNewRow()
		childRow["PartNumber"] = row["partnumber"]
		childRow["Quantity"] = str(int(float(row["CE_Final_Quantity"])))
for row in lineItemContainer.Rows:
	row.IsSelected = True
	updateChildAttributes(row, Product)
lineItemContainer.Calculate()