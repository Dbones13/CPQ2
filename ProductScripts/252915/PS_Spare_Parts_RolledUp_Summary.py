def getContainer(Name):
    return Product.GetContainerByName(Name)


selectedProducts = list()
for row in getContainer("MSID_Product_Container").Rows:
    selectedProducts.append(row["Product Name"])

if 'Spare Parts' in selectedProducts:
    Con_SP_tobePopulated=Product.GetContainerByName('Spare_Parts_Rolled_PS')
    MSID_SP_Con=Product.GetContainerByName('MSID_Spare_Parts_Container').Rows
    PS_PN_DICT=dict()
    PS_Description_DICT=dict()
    PS_Price_DICT=dict()
    Con_SP_tobePopulated.Clear()
    for row in MSID_SP_Con:
        SP_Summary_Con=row.Product.GetContainerByName('Spare_Parts_Cabinet_PartSummary').Rows
        QTY=0 if row["Qty"]=="" else int(row["Qty"])
        for row2 in SP_Summary_Con:
            if row2["Price"] != "No":
                l = PS_PN_DICT.get(row2["PartNumber"],0)
                PS_PN_DICT[row2["PartNumber"]]=l+(int(row2["Quantity"])*QTY)
                PS_Description_DICT[row2["PartNumber"]]=row2["Part_Number_Description"]
                PS_Price_DICT[row2["PartNumber"]]=row2["Price"]
    for PN in PS_PN_DICT:
        PS_PN_DICT[PN]
        ConRow=Con_SP_tobePopulated.AddNewRow(True)
        ConRow["Part_Number"]=PN
        ConRow["Quantity"]=str(PS_PN_DICT[PN])
        ConRow["Description"]=PS_Description_DICT[PN]
        ConRow["Price"]=PS_Price_DICT[PN]