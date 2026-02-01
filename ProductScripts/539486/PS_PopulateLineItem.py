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

contGen = Product.GetContainerByName("Generic_System_Mig_Uploaded_Parts_Cont")
lineItemContainer = Product.GetContainerByName("MSID_Added_Parts_Common_Container")
#lineItemContainer.Clear()
partQtyMap = {}
rowsToDelete = []

for row in contGen.Rows:
	qty = row["Final Quantity"] if row["Final Quantity"] else 0
	if float(qty):
		if row["PartNumber"] in partQtyMap:
			partQtyMap[row["PartNumber"] ] = str(int(float(partQtyMap[row["PartNumber"] ]) + float(qty)))
		else:
			partQtyMap[row["PartNumber"] ]= qty

for li_row in lineItemContainer.Rows:
    pn = li_row["PartNumber"]
    newQTY =  partQtyMap.get(pn,0)
    if newQTY:
        li_row["Quantity"] = str(newQTY)
        del partQtyMap[pn]
    else:
        if li_row["IsChildRow"] == "Yes":
            rowsToDelete.append(li_row.RowIndex)

for part,qty in partQtyMap.items():
    childRow = lineItemContainer.AddNewRow()
    childRow["PartNumber"] = part
    childRow["Quantity"] = str(qty)
    childRow["IsChildRow"] = "Yes"
    childRow.IsSelected = True

for rowIndex in rowsToDelete[::-1]:
    lineItemContainer.DeleteRow(rowIndex)

for row in lineItemContainer.Rows:
	row.IsSelected = True
	updateChildAttributes(row, Product)
lineItemContainer.Calculate()