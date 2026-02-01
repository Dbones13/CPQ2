gesLocation = Product.Attr('MSE GES Location').GetValue()
updatePrice = 0
if gesLocation not in ("None",""):
    laborRows = Product.GetContainerByName('MSE_Additional_Labor_Container')
    gesPerc = Product.Attr('MSE_Addi_Labor_GES_%').GetValue()
    for row in laborRows.Rows:
        gesPerc=float(gesPerc)
        if row.IsSelected:
            row.GetColumnByName('GES Eng % Split').Value = str(gesPerc)
            row.GetColumnByName('FO Eng % Split').Value = str(100-(gesPerc))
            updatePrice = 1
        #row.IsSelected=False
    laborRows.Calculate()
if updatePrice:
    ScriptExecutor.Execute('PS_Labor_Part_Summary')
#ScriptExecutor.Execute('PS_OWS_Error_Msg')
Product.Attr('MSE_Addi_Labor_GES_%').AssignValue('')