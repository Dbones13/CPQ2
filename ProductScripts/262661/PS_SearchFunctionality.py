cyberPartCon = Product.GetContainerByName("Cyber_Parts_Container")
addcyberPartCon = Product.GetContainerByName("Add_Cyber_Parts_Container")
cyberPartCon.Rows.Clear()

selectedVC = dict()
for row in addcyberPartCon.Rows:
    if row.IsSelected:
        selectedVC[row["Product"]] = row["Quantity"]

def getAttrValue(Name):
    return Product.Attr(Name).GetValue()


def populateCyberParts(part):
    Row = cyberPartCon.AddNewRow()
    Row["Product"] = part.Product
    Row["Description"] = part.Description
    Row["Quantity"] = "1"

    qty = selectedVC.get(Row["Product"])
    if qty:
        Row.IsSelected = True
        Row["Quantity"] = qty

cyberPart = getAttrValue("VC_SearchByVCModel")
description = getAttrValue("VC_SearchByDescription")

query = "select Distinct Product,Description from CYBER_PARTS where "

if cyberPart != '':
    Trace.Write("cyberPart")
    query += "Product like '%{}%' AND ".format(cyberPart)

if description != '':
    Trace.Write("description")
    query += "Description like '%{}%' AND ".format(description)

if cyberPart != '' or description != '':
    query = query[:-5]
else:
    query = query[:-7]
Trace.Write("query = " + str(query))

cyberPartData = SqlHelper.GetList(query)

if cyberPartData is not None:
    for part in cyberPartData:
        populateCyberParts(part)

cyberPartCon.Calculate()