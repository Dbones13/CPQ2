#Populate each selected container row with the 'Execution Country' value
laborRows = Product.GetContainerByName('FDA_Additional_Labor_Container').Rows
execCountry = Product.Attr('FDA_Addi_Labor_Execution_Country').GetValue()
updatePrice = 0
for row in laborRows:
    if row.IsSelected:
        row.GetColumnByName('Execution Country').Value = execCountry
        updatePrice = 1
    #row.IsSelected = False
if updatePrice:
    ScriptExecutor.Execute('PS_FDA_Update_Labor_Cost')
Product.Attr('FDA_Addi_Labor_Execution_Country').SelectDisplayValue('')