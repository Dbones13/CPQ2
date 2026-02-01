laborRows = Product.GetContainerByName('PSW_Labor_Container')
execCountry = Product.Attr('PSW_Labor_Excecution_Country').GetValue()
updatePrice = 0
for row in laborRows.Rows:
    if row.IsSelected:
        row.GetColumnByName('Execution Country').Value = execCountry
        updatePrice = 1
    #row.IsSelected=False
laborRows.Calculate()
if updatePrice:
    ScriptExecutor.Execute('PS_PSW_Update_Labor_Cost')
Product.Attr('PSW_Labor_Excecution_Country').SelectDisplayValue('')