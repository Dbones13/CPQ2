def updateChildAttributes(row):
    if not row.Product:
        return
    for attr in filter(lambda a : a.DisplayType != "Container", row.Product.Attributes):
        if attr.Name == "ItemQuantity":
            attr.AssignValue(row["Quantity"])
    row.ApplyProductChanges()

def populatePartsInChild(product, container):
    #lineItemContainer = product.GetContainerByName("MSID_Added_Parts_Common_Container")
    lineItemContainer = product.GetContainerByName("Trace_Software_Added_Parts_Common_Container")
    lineItemContainer.Rows.Clear()
    for row in container.Rows:
        qty = row["FinalHours"] if row["FinalHours"] else 0
        prodPLSG = SqlHelper.GetFirst(""" SELECT p.PRODUCT_NAME, hpm.PLSG, hpm.PLSGDesc FROM products p JOIN HPS_PRODUCTS_MASTER hpm ON p.PRODUCT_CATALOG_CODE = hpm.PartNumber WHERE PRODUCT_CATALOG_CODE = '{}' """.format(str(row["LaborResource"])))
        partsDict = [i for i in lineItemContainer.Rows if i['PartNumber'] == row["LaborResource"]]
        if float(qty) and prodPLSG:
            if len(partsDict) == 0:
                childRow = lineItemContainer.AddNewRow(False)
                childRow["PartNumber"] = row["LaborResource"]
                Trace.Write('fin hrs-'+str(str(row["FinalHours"])))
                childRow["Quantity"] = row["FinalHours"] if str(row["FinalHours"]) else 0
                childRow["PLSG"] = prodPLSG.PLSG
                childRow["PartDescription"] = prodPLSG.PRODUCT_NAME
                childRow["plsgDescription"] = prodPLSG.PLSGDesc
                childRow["Comments"] = row["Comment"]
            else:
                for updaterow in partsDict:
                    if updaterow['PartNumber']  == row["LaborResource"]:
                        updaterow["Quantity"] = str(float(updaterow["Quantity"])+float(qty))
    lineItemContainer.Calculate()
    for row in lineItemContainer.Rows:
        row.IsSelected = True
        row.Calculate()
        updateChildAttributes(row)
    lineItemContainer.Calculate()

controw = Product.GetContainerByName('AR_HCI_LABOR_CONTAINER')
populatePartsInChild(Product, controw)
lineItemContainer = Product.GetContainerByName("Trace_Software_Added_Parts_Common_Container")
guid_list = [data.UniqueIdentifier for data in lineItemContainer.Rows]
Session['HCI_Labor_Guid'] = guid_list