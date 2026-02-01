laborRows = Product.GetContainerByName('IS_Labor_Container').Rows
execCountry = Product.Attr('IS_Labor_Execution_Country').GetValue()
updatePrice = 0
for row in laborRows:
    if row.IsSelected:
        row.GetColumnByName('Execution Country').Value = execCountry
        updatePrice = 1
    #row.IsSelected = False
if updatePrice:
    ScriptExecutor.Execute('PS_IS_Update_Labor_Cost')
Product.Attr('IS_Labor_Execution_Country').SelectDisplayValue('')