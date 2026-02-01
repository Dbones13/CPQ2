gesLocation = Product.Attr('IS_GES_Location').GetValue()
updatePrice = 0
if gesLocation not in ("None",""):
    laborRows = Product.GetContainerByName('IS_Additional_Labor_Container').Rows
    gesPerc = Product.Attr('IS_Addi_Labor_GES_%').GetValue()
    for row in laborRows:
        gesPerc=float(gesPerc)
        if row.IsSelected:
            row.GetColumnByName('GES Eng % Split').Value = str(gesPerc)
            row.GetColumnByName('FO Eng % Split').Value = str(100-(gesPerc))
            updateFlag = 1
        #row.IsSelected = False

if updatePrice:
    ScriptExecutor.Execute('PS_IS_Update_Labor_Cost')
ScriptExecutor.Execute('PS_IS_Error_Message')
Product.Attr('IS_Addi_Labor_GES_%').AssignValue('')