gesLocation = Product.Attr('PRMS GES Location').GetValue()
updatePrice = 0
if gesLocation not in ("None",""):
    laborRows = Product.GetContainerByName('PRMS_Additional_Labor_Container')
    gesPerc = Product.Attr('PRMS_Addi_Labor_GES_%').GetValue()
    for row in laborRows.Rows:
        gesPerc=float(gesPerc)
        if row.IsSelected:
            row.GetColumnByName('GES Eng % Split').Value = str(gesPerc)
            row.GetColumnByName('FO Eng % Split').Value = str(100-(gesPerc))
            updateFlag = 1
        #row.IsSelected=False
laborRows.Calculate()
if updatePrice:
    ScriptExecutor.Execute('PS_PRMS_Update_Labor_Cost')
ScriptExecutor.Execute('PS_PRMS_Error_message')
Product.Attr('PRMS_Addi_Labor_GES_%').AssignValue('')