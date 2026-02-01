addcyberPartCon = Product.GetContainerByName("Add_Cyber_Parts_Container")
cyberPartsList = []
for row in addcyberPartCon.Rows:
    if row["Product"] not in cyberPartsList:
        cyberPartsList.append(row["Product"])
for item in Quote.MainItems:
    if item.PartNumber in cyberPartsList:
        item.Delete()
        break