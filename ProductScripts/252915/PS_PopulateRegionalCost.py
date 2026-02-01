def getContainer(Name):
    return Product.GetContainerByName(Name)
opmEngineeringCon = getContainer("MSID_Labor_OPM_Engineering")
partsNumbers = dict()
for row in opmEngineeringCon.Rows:
    if row["Manual_Entry"] == "Yes":
        partsNumbers[row["FO_Eng"]] = row["Regional_Cost"]

if partsNumbers:
    for item in Quote.Items:
        if item.PartNumber in partsNumbers:
            item.QI_Manual_labor_Regional_Cost.Value = float(partsNumbers[item.PartNumber])