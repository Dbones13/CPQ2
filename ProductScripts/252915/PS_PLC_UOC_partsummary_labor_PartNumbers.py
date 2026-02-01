import GS_PS_Exp_Ent_BOM
from ProductUtil import getContainer

def getFloat(var):
    if var:
        return float(var)
    return 0
container = getContainer(Product, "3rd_Party_PLC_UOC_Labor")
gesLocation = Product.Attr("MSID_GES_Location").GetValue()
activeServiceContract = Product.Attr("MSID_Active_Service_Contract").GetValue()
def addFinalHours(totalDict, key, value):
    totalDict[key] = getFloat(totalDict.get(key, 0)) + getFloat(value)
gesPartQty = 0
foPartQty = 0
partNumbersToBeAdded = dict()
for row in container.Rows:
    if row["Deliverable"] not in ('Total','Off-Site','On-Site'):
        Trace.Write(row["Final_Hrs"])
        if row["FO_Eng"]:
            foQty = round((getFloat(row["Final_Hrs"]) * getFloat(row["FO_Eng_Percentage_Split"]) / 100))
            addFinalHours(partNumbersToBeAdded,row["FO_Eng"],foQty)
            foPartQty = foPartQty + foQty
        if row["GES_Eng"] != '' and row["GES_Eng_Percentage_Split"] != '0':
            gesQty = round((getFloat(row["Final_Hrs"]) * getFloat(row["GES_Eng_Percentage_Split"]) / 100))
            gesPartQty = gesPartQty + gesQty
            addFinalHours(partNumbersToBeAdded,row["GES_Eng"],gesQty)
for partNumber in partNumbersToBeAdded:
    GS_PS_Exp_Ent_BOM.setAtvQty(Product, "PLC_UOC_BOM_Items", partNumber, partNumbersToBeAdded[partNumber])
