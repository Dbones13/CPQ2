gesLocation = Product.Attr('FDA GES Location').GetValue()
updatePrice = 0
if gesLocation not in ("None",""):
    laborRows = Product.GetContainerByName('FDA_Additional_Labor_Container').Rows
    gesPerc = Product.Attr('FDA_Addi_Labor_GES_%').GetValue()
    for row in laborRows:
        gesPerc=float(gesPerc)
        if row.IsSelected:
            row.GetColumnByName('GES Eng % Split').Value = str(gesPerc)
            row.GetColumnByName('FO Eng % Split').Value = str(100-(gesPerc))
            updatePrice = 1
        #row.IsSelected = False

if updatePrice:
    ScriptExecutor.Execute('PS_FDA_Update_Labor_Cost')
ScriptExecutor.Execute('PS_FDA_Error_Message')
Product.Attr('FDA_Addi_Labor_GES_%').AssignValue('')