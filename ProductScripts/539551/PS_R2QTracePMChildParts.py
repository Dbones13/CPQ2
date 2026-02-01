isR2Qquote = True if Quote.GetCustomField("isR2QRequest").Content else False
if isR2Qquote:
    import math
    from ProductUtil import getContainer

    def log_dict(d):
        Trace.Write(RestClient.SerializeToJson(d))
        return RestClient.SerializeToJson(d)

    def getFloat(var):
        if var:
            return float(var)
        return 0

    def addFinalHours(totalDict, key, value):
        totalDict[key] = getFloat(totalDict.get(key, 0)) + getFloat(value)

    def migrationAttrDict(product):
        migrationAttrDict = dict()
        return migrationAttrDict

    def getPartDetailDict(partsList):
        resDict = dict()
        query = "select PRODUCT_CATALOG_CODE, PRODUCT_NAME, PLSG, PLSGDesc from products p join HPS_PRODUCTS_MASTER hpm ON p.PRODUCT_CATALOG_CODE = hpm.PartNumber where PRODUCT_CATALOG_CODE in ('{0}') UNION select PRODUCT_CATALOG_CODE, PRODUCT_NAME, PLSG, PLSGDesc from Migration_Third_Party_Products where PRODUCT_CATALOG_CODE in ('{0}')"
        query = query.format("','".join(partsList))
        res = SqlHelper.GetList(query)
        for r in res:
            resDict[r.PRODUCT_CATALOG_CODE] = [r.PRODUCT_NAME, r.PLSG, r.PLSGDesc]
        return resDict

    def getPartsToBeAdded(msidprd, attributeValueDict):
        partNumbersToBeAdded = {
           # "PM": dict(),
            "Trace": dict(),
        }
        partsList = set()
        attr_map = dict()
        for av in msidprd.Attr('Trace_Software_Parts_Summary_PN').SelectedValues:
            attr_map[av.Display] = av.Quantity
        partNumbersToBeAdded["Trace"] = attr_map
        partsList = set(attr_map.keys())
        return partNumbersToBeAdded, partsList

    def getUserInputMap(container):
        userInputMap = dict()
        for row in container.Rows:
            data = {
                'adjQty': row['Adj Quantity'],
                'comment': row['Comments']
            }
            userInputMap[row['PartNumber']] = data
        return userInputMap

    def populatePartsInChild(product, container):
        lineItemContainer = product.GetContainerByName("MSID_Added_Parts_Common_Container")
        lineItemContainer.Clear()
        for row in container.Rows:
            qty = row["Final Quantity"] if row["Final Quantity"] else 0
            if float(qty):
                childRow = lineItemContainer.AddNewRow(False)
                childRow["PartNumber"] = row["PartNumber"]
                childRow["Quantity"] = str(int(float(qty)))
        lineItemContainer.Calculate()
        for row in lineItemContainer.Rows:
            row.IsSelected = True
            row.Calculate()
            updateChildAttributes(row)
        lineItemContainer.Calculate()

    def updateChildAttributes(row):
        if not row.Product:
            return
        for attr in filter(lambda a: a.DisplayType != "Container", row.Product.Attributes):
            if attr.Name == "ItemQuantity":
                attr.AssignValue(row["Quantity"])
        row.ApplyProductChanges()

    # Begin execution
    attributeValueDict = migrationAttrDict(Product)
    migration_new_cont = Product.GetContainerByName('CONT_Migration_MSID_Selection')

    for migrationnew in migration_new_cont.Rows:
        if migrationnew.Product.Attr('MIgration_Scope_Choices').GetValue() != "HW/SW":
            msidprd = migrationnew.Product
            subprd_cont = msidprd.GetContainerByName('CONT_MSID_SUBPRD')
            for row in subprd_cont.Rows:
                if row['Selected_Products'] == 'Trace Software':
                    trace_subproduct = row.Product
                    partNumbersToBeAdded, partsList = getPartsToBeAdded(trace_subproduct, attributeValueDict)

                    def getLaborContainerData(container, productKey):
                        for row in container.Rows:
                            if row["Deliverable"] not in ('Total', 'Off-Site', 'On-Site'):
                                if row["FO_Eng"]:
                                    foQty = round((getFloat(row["Final_Hrs"]) * getFloat(row["FO_Eng_Percentage_Split"]) / 100))
                                    addFinalHours(partNumbersToBeAdded[productKey], row["FO_Eng"], foQty)
                                if row["FO_Eng"] not in partsList:
                                    partsList.add(row["FO_Eng"])
                                if row["GES_Eng"] and row["GES_Eng_Percentage_Split"] != '0':
                                    gesQty = round((getFloat(row["Final_Hrs"]) * getFloat(row["GES_Eng_Percentage_Split"]) / 100))
                                    addFinalHours(partNumbersToBeAdded[productKey], row["GES_Eng"], gesQty)
                                if row["GES_Eng"] not in partsList:
                                    partsList.add(row["GES_Eng"])

                    traceCon = getContainer(msidprd, "Trace_Software_Labor_con")
                    getLaborContainerData(traceCon, "Trace")

                    '''projectManagementCon = getContainer(msidprd, "Trace_Project_Management_Labor_con")
                    for row in projectManagementCon.Rows:
                        if row["Deliverable"] not in ('Total', 'Off-Site', 'On-Site'):
                            if row["FO_Eng"]:
                                foQty = round((getFloat(row["Final_Hrs"]) * getFloat(row["FO_Eng_Percentage_Split"]) / 100))
                                addFinalHours(partNumbersToBeAdded["PM"], row["FO_Eng"], foQty)
                            if row["FO_Eng"] not in partsList:
                                partsList.add(row["FO_Eng"])
                            if row["GES_Eng"] and row["GES_Eng_Percentage_Split"] != '0':
                                gesQty = round((getFloat(row["Final_Hrs"]) * getFloat(row["GES_Eng_Percentage_Split"]) / 100))
                                addFinalHours(partNumbersToBeAdded["PM"], row["GES_Eng"], gesQty)
                            if row["GES_Eng"] not in partsList:
                                partsList.add(row["GES_Eng"])'''

                    Trace.Write(RestClient.SerializeToJson(partNumbersToBeAdded))

                    containerNameMapping = {
                       # "PM": getContainer(msidprd, "MSID_PM_Added_Parts_Common_Container"),
                        "Trace": getContainer(msidprd, "Trace_Software_Added_Parts_Common_Container")
                    }

                    partDetailsDict = getPartDetailDict(partsList)

                    for productKey, parts in partNumbersToBeAdded.items():
                        container = containerNameMapping[productKey]
                        userInputMap = getUserInputMap(container)
                        container.Clear()
                        for part, qty in parts.items():
                            if qty > 0.00 and qty != '':
                                row = container.AddNewRow(False)
                                row['PartNumber'] = part
                                row['Quantity'] = str(qty)
                                adjQty = 0
                                comment = ''
                                if userInputMap.get(part):
                                    adjQty = getFloat(userInputMap[part]['adjQty'])
                                    comment = userInputMap[part]['comment']
                                row['Adj Quantity'] = str(adjQty)
                                row['Final Quantity'] = str(getFloat(qty) + adjQty)
                                row['Comments'] = comment
                                if partDetailsDict.get(part):
                                    row['PartDescription'] = partDetailsDict[part][0]
                                    row['PLSG'] = partDetailsDict[part][1]
                                    row['plsgDescription'] = partDetailsDict[part][2]
                        container.Calculate()

                    x = log_dict(attributeValueDict)

                    con = msidprd.GetContainerByName("Trace_Software_Added_Parts_Common_Container")
                    if con.Rows.Count > 0:
                        populatePartsInChild(trace_subproduct, con)
