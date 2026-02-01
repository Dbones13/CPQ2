gesLocation = Product.Attr('TGE_GES Location').GetValue()
updatePrice = 0
if gesLocation not in ("None",""):
    laborRows = Product.GetContainerByName('TGE_Additional_Labour_Container')
    gesPerc = Product.Attr('TGE_Addi_Labor_GES_%').GetValue()
    for row in laborRows.Rows:
        gesPerc=float(gesPerc)
        if row.IsSelected:
            row.GetColumnByName('GES Eng % Split').Value = str(gesPerc)
            row.GetColumnByName('FO Eng % Split').Value = str(100-(gesPerc))
            updatePrice = 1
        #row.IsSelected=False
    laborRows.Calculate()
if updatePrice:
    ScriptExecutor.Execute('PS_Populate_TGE_Labor_Price_Cost')
ScriptExecutor.Execute('PS_TGE_Error_Msg')
Product.Attr('TGE_Addi_Labor_GES_%').AssignValue('')