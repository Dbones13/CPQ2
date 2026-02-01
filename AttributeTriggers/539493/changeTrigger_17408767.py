#Populate each selected container row with the 'Execution Country' value
laborRows = Product.GetContainerByName('MSE_Additional_Labor_Container')
execCountry = Product.Attr('MSE_Addi_Labor_Execution_Country').GetValue()
updatePrice = 0
for row in laborRows.Rows:
    if row.IsSelected:
        row.GetColumnByName('Execution Country').Value = execCountry
        updatePrice = 1
        #row.IsSelected=False
    laborRows.Calculate()
if updatePrice:
    ScriptExecutor.Execute('PS_Labor_Part_Summary')
Product.Attr('MSE_Addi_Labor_Execution_Country').SelectDisplayValue('')