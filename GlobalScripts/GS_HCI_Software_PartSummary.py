def populatePartsInChild(product, container):
	#lineItemContainer = product.GetContainerByName("MSID_Added_Parts_Common_Container")
	lineItemContainer = product.GetContainerByName("Trace_Software_Added_Parts_Common_Container")
	lineItemContainer.Clear()
	for row in container.Rows:
		qty = row["Quantity"] if row["Quantity"] else 0
		prod = SqlHelper.GetFirst("select PRODUCT_ID from products where PRODUCT_CATALOG_CODE='{}'".format(str(row["PartNumber"])))
		if float(qty) and prod:
			#Trace.Write("-final->"+str(prod.PRODUCT_ID))
			childRow = lineItemContainer.AddNewRow(False)
			childRow["PartNumber"] = row["PartNumber"]
			childRow["Quantity"] = str(int(row["Quantity"]) + int(row["Adj Quantity"]))
			childRow["PLSG"] = row["PLSG"] if row["PLSG"] else ""
			childRow["PartDescription"] = row["PartDescription"] if row["PartDescription"] else ""
			childRow["plsgDescription"] = row["plsgDescription"] if row["plsgDescription"] else ""
			childRow["Comments"] = row["Comments"] if row["Comments"] else ""
	lineItemContainer.Calculate()
	for row in lineItemContainer.Rows:
		row.IsSelected = True
		row.Calculate()
		updateChildAttributes(row)
	lineItemContainer.Calculate()

def updateChildAttributes(row):
	if not row.Product:
		return
	for attr in filter(lambda a : a.DisplayType != "Container", row.Product.Attributes):
		if attr.Name == "ItemQuantity":
			attr.AssignValue(row["Quantity"])
	row.ApplyProductChanges()

#trace = Product.GetContainerByName("Trace_Software_Added_Parts_Common_Container")
#trace.Clear()
#con = Product.GetContainerByName("Trace_Software_Added_Parts_Common_Container")
#con = Product.GetContainerByName("HCI_PHD_PartSummary_Cont")
#populatePartsInChild(Product, con)