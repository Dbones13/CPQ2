def getContainer(product, name):
    return product.GetContainerByName(name)
def DeleteQuoteItem(parentItemGUID, table):
    item_delete = []
    for row in table.Rows:
        if str(row['MIgration_GUID'])  == str(parentItemGUID):
            Trace.Write('--------------')
            Trace.Write(str(parentItemGUID))
            item_delete.append(row.Id)
    c=sorted(item_delete, reverse=True)
    for r in c:
        table.DeleteRow(r)
    table.Save()
def populateQuoteTable(parentItemGUID, guid, attr, attr_value, table):
    row = table.AddNewRow()
    row["MIgration_GUID"] = parentItemGUID
    row["MSID_GUID"] = guid
    row["Attribute"] = attr
    row["Attribute_Value"] = ",".join(attr_value) if str(type(attr_value)) == "<type 'list'>" else str(attr_value)
parentItemGUID = ''
for i in arg.QuoteItemCollection:
    parentItemGUID = i.ParentItemGuid
table = Quote.QuoteTables["Migration_Document_Data"]
DeleteQuoteItem(parentItemGUID, table)
cont = getContainer(Product, "IAA Inputs_Cont")
for row in cont.Rows:
    guid = row["IAA_List_individual_MSIDs/ESIDs"]
    attr = row["IAA_Assessment_Type"]
    attr_value = row["IAA_Quantity"]
    populateQuoteTable(parentItemGUID, guid, attr, attr_value, table)

cont1 = getContainer(Product, "IAA Inputs_Cont_2")
for row in cont1.Rows:
    guid = " "
    attr = row["Name"]
    attr_value = row["Quantity"]
    populateQuoteTable(parentItemGUID, guid, attr, attr_value, table)

contprice = getContainer(Product, "IAA Pricing")
for row in contprice.Rows:
    guid = " "
    attr = row["Name"]
    attr_value = row["Price"]
    populateQuoteTable(parentItemGUID, guid, attr, attr_value, table)

table.Save()