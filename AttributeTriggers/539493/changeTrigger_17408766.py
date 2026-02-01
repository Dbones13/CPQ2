laborRows = Product.GetContainerByName('MSE_Engineering_Labor_Container')
execCountry=Product.Attr('MSE_Engineering_Labor_Execution_Country').GetValue()
updatePrice = 0
for row in laborRows.Rows:
    if row.IsSelected:
        row.GetColumnByName('Execution Country').Value = execCountry
        updatePrice = 1
    #row.IsSelected=False
laborRows.Calculate()
if updatePrice:
    ScriptExecutor.Execute('PS_Refresh_MSE_Labor_Container')
Product.Attr('MSE_Engineering_Labor_Execution_Country').SelectDisplayValue('')