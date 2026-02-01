def getFloat(Var):
    if Var:
        return float(Var)
    return 0

def getAttrVal(attributename):
	return Product.Attr(attributename).GetValue()

checkEBR = False
upgradeCont = Product.GetContainerByName('EBR_Upgrade')
if (upgradeCont.Rows.Count) > 0:
    row = upgradeCont.Rows[0]
    checkEBR = getFloat(row['EBR_Qty_of_EBR_Upgrade_for_Server']) > 0 or  getFloat(row['EBR_Qty_of_EBR_Upgrade_for_Workstation']) >0 or  getFloat(row['EBR_Qty_of_EBR_Upgrade_for_Virtual_Node']) > 0

if not checkEBR:
    checkEBR = getFloat(getAttrVal('Attr_New/AdditionalServer')) > 0 or  getFloat(getAttrVal('Attr_NewAddWorkstation')) >0 or  getFloat(getAttrVal('Attr_NewAddVirtual_Node')) > 0

Product.Attributes.GetByName('IncompleteEBRCheck').AssignValue(str(checkEBR))