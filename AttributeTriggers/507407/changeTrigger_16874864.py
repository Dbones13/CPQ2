gesLocation = Product.Attr('FGC_GES_Location').GetValue()
updatePrice = 0
if gesLocation not in ("None",""):
    laborRows = Product.GetContainerByName('FGC_Additional_Labour_Container').Rows
    gesPerc = Product.Attr('FGC_Addi_Labor_GES_%').GetValue()
    for row in laborRows:
        gesPerc=float(gesPerc)
        if row.IsSelected:
            row.GetColumnByName('GES Eng % Split').Value = str(gesPerc)
            row.GetColumnByName('FO Eng % Split').Value = str(100-(gesPerc))
            updateFlag = 1
    	#row.IsSelected = False

if updatePrice:
    ScriptExecutor.Execute('PS_FGC_Update_Labor_Cost')
ScriptExecutor.Execute('FGC_Error_message')
Product.Attr('FDA_Addi_Labor_GES_%').AssignValue('')