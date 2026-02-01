gesLocation = Product.Attr('GAS MeterSuite GES Location').GetValue()
updatePrice = 0
if gesLocation not in ("None",""):
    laborRows = Product.GetContainerByName('Gas_MeterSuite_Additional_Labor_Container')
    gesPerc = Product.Attr('GAS_MeterSuite_Addi_Labor_GES_%').GetValue()
    for row in laborRows.Rows:
        gesPerc=float(gesPerc)
        if row.IsSelected:
            row.GetColumnByName('GES Eng % Split').Value = str(gesPerc)
            row.GetColumnByName('FO Eng % Split').Value = str(100-(gesPerc))
            updatePrice = 1
        #row.IsSelected=False
    laborRows.Calculate()
if updatePrice:
    ScriptExecutor.Execute('PS_GMS_Update_Labor_Cost')
ScriptExecutor.Execute('PS_GMS_Error_Message')
Product.Attr('GAS_MeterSuite_Addi_Labor_GES_%').AssignValue('')