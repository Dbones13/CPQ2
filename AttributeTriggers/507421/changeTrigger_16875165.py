laborRows = Product.GetContainerByName('OWS_Engineering_Labor_Container')
execCountry=Product.Attr('OWS_Labor_Execution_Country').GetValue()
updatePrice = 0
for row in laborRows.Rows:
    if row.IsSelected:
        row.GetColumnByName('Execution Country').Value = execCountry
        updatePrice = 1
    #row.IsSelected=False
laborRows.Calculate()
if updatePrice:
    ScriptExecutor.Execute('PS_Populate_OWS_Labor_Price_Cost')
Product.Attr('OWS_Labor_Execution_Country').SelectDisplayValue('')