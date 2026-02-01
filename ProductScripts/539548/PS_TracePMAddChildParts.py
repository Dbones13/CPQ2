def populateChildPartForMSID2(product):
    partContainers = ["MSID_PM_Added_Parts_Common_Container"]
    contProductMap = {"MSID_PM_Added_Parts_Common_Container": "Project Management"}
    productContainer = product.GetContainerByName("Trace_Product_Container_hidden")

    if productContainer.Rows.Count == 0:
        productContainer.AddNewRow()
    for container in partContainers:
        for selectedRow in selectedProducts.Rows:
            if selectedRow.Product.Name == 'Trace Software':
                cont = selectedRow.Product.GetContainerByName(container)
        productRow = productContainer.Rows.GetByColumnName("Product Name", contProductMap[container])
        if not productRow:
            continue
        populatePartsInChild2(productRow, cont)

def populatePartsInChild2(productRow, container):
    product = productRow.Product
    lineItemContainer = product.GetContainerByName("MSID_Added_Parts_Common_Container")
    lineItemContainer.Clear()
    for row in container.Rows:
        qty = row["Final Quantity"] if row["Final Quantity"] else 0
        Log.Info("TracePartQTY" + str(qty))
        Trace.Write("TracePartQTY" + str(qty))
        if float(qty):
            childRow = lineItemContainer.AddNewRow()
            childRow["PartNumber"] = row["PartNumber"]
            childRow["Quantity"] = str(int(float(row["Final Quantity"])))
        Trace.Write("selectedrow" + str(row.IsSelected))
    Trace.Write("Lineitemcontainer" + str(lineItemContainer.Rows.Count))
    for i in lineItemContainer.Rows:
        Trace.Write("Partnumber" + i['PartNumber'])
    
    #lineItemContainer.Calculate()
    lineItemContainer.MakeAllRowsSelected()
    for row in lineItemContainer.Rows:
        Trace.Write("lineselectedrow" + str(row.IsSelected))
        updateChildAttributes(row)
    lineItemContainer.Calculate()
    productRow.ApplyProductChanges()



def updateChildAttributes(row):
    if not row.Product:
        return
    for attr in filter(lambda a : a.DisplayType != "Container", row.Product.Attributes):
        if attr.Name == "ItemQuantity":
            attr.AssignValue(row["Quantity"])
    row.ApplyProductChanges()
selectedProducts = Product.GetContainerByName('CONT_MSID_SUBPRD')
for selectedRow in selectedProducts.Rows:
    if selectedRow.Product.Name == 'Trace Software' and selectedProducts.Rows.Count > 1:
        populateChildPartForMSID2(Product)