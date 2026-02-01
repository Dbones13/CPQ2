isR2Qquote = True if Quote.GetCustomField("isR2QRequest").Content else False
if not isR2Qquote:
    ScriptExecutor.ExecuteGlobal('GS_Trace_Software_PartSummary')
    def populatePartsInChild(product, container):
        lineItemContainer = product.GetContainerByName("MSID_Added_Parts_Common_Container")
        lineItemContainer.Clear()
        Trace.Write('1.1')
        for row in container.Rows:
            qty = row["Final Quantity"] if row["Final Quantity"] else 0
            Trace.Write('1.2')
            if float(qty):
                childRow = lineItemContainer.AddNewRow(False)
                childRow["PartNumber"] = row["PartNumber"]
                Trace.Write('1.3')
                childRow["Quantity"] = str(int(float(row["Final Quantity"])))
                Trace.Write('1.4')

        lineItemContainer.Calculate()
        for row in lineItemContainer.Rows:
            row.IsSelected = True
            row.Calculate()
            updateChildAttributes(row)

        lineItemContainer.Calculate()
        #product.ApplyProductChanges()

    def updateChildAttributes(row):
        if not row.Product:
            return
        for attr in filter(lambda a : a.DisplayType != "Container", row.Product.Attributes):
            if attr.Name == "ItemQuantity":
                attr.AssignValue(row["Quantity"])
        row.ApplyProductChanges()
            #value = getAttrValue(attr.Name, row.Product.PartNumber)
            #if value:
                #Trace.Write("{} : {}".format(attr.Name, value))
                #attr.SelectValue(value)

    def populateChildPartForMSID2(product):
        partContainers = [
            "MSID_PM_Added_Parts_Common_Container",
        ]
        contProductMap = {  
            "MSID_PM_Added_Parts_Common_Container": "Project Management",
        }
        productContainer = product.GetContainerByName("Trace_Product_Container_hidden")
        if Product.Attr('Trace_Software_Scope_Choices').GetValue() in ['LABOR', 'HW/SW/LABOR']:
            if productContainer.Rows.Count == 0:
                productContainer.AddNewRow()
            for container in partContainers:
                cont = product.GetContainerByName(container)
                productRow = productContainer.Rows.GetByColumnName("Product Name", contProductMap[container])
                if not productRow:
                    continue
                populatePartsInChild2(productRow, cont)
        else:
            productContainer.Clear()

    def populatePartsInChild2(productRow, container):
        product = productRow.Product
        lineItemContainer = product.GetContainerByName("MSID_Added_Parts_Common_Container")
        lineItemContainer.Clear()
        for row in container.Rows:
            qty = row["Final Quantity"] if row["Final Quantity"] else 0
            if float(qty):
                childRow = lineItemContainer.AddNewRow()
                childRow["PartNumber"] = row["PartNumber"]
                childRow["Quantity"] = str(int(float(row["Final Quantity"])))

        lineItemContainer.Calculate()
        for row in lineItemContainer.Rows:
            row.IsSelected = True
            updateChildAttributes(row)

        lineItemContainer.Calculate()
        productRow.ApplyProductChanges()


    con = Product.GetContainerByName("Trace_Software_Added_Parts_Common_Container")
    populatePartsInChild(Product, con )
    populateChildPartForMSID2(Product)

