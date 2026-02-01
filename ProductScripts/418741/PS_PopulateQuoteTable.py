def getContainer(product, name):
    return product.GetContainerByName(name)

def populateQuoteTable(guid, attr, attr_value, table):
    row = table.AddNewRow()
    row["MSID_GUID"] = guid
    row["Attribute"] = attr
    row["Attribute_Value"] = ",".join(attr_value) if str(type(attr_value)) == "<type 'list'>" else str(attr_value)


table = Quote.QuoteTables["Migration_Document_Data"]
table.Rows.Clear()
cont = getContainer(Product, "IAA Inputs_Cont")
for row in cont.Rows:
    guid = row["IAA_List_individual_MSIDs/ESIDs"]
    attr = row["IAA_Assessment_Type"]
    attr_value = row["IAA_Quantity"]
    populateQuoteTable(guid, attr, attr_value, table)
    
cont1 = getContainer(Product, "IAA Inputs_Cont_2")
for row in cont1.Rows:
    guid = " "
    attr = row["Name"]
    attr_value = row["Quantity"]
    populateQuoteTable(guid, attr, attr_value, table)
    
table.Save()