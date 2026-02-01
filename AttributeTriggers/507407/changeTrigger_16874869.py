laborRows = Product.GetContainerByName('FGC_Engineering_Labor_Container').Rows
execCountry = Product.Attr('FGC_Labor_Execution_Country').GetValue()
updatePrice = 0
for row in laborRows:
    if row.IsSelected:
        row.GetColumnByName('Execution Country').Value = execCountry
        updatePrice = 1
    #row.IsSelected = False
if updatePrice:
    ScriptExecutor.Execute('PS_FGC_Update_Labor_Cost')
Product.Attr('FGC_Labor_Execution_Country').SelectDisplayValue('')