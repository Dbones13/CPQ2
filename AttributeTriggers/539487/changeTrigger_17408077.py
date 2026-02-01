#Populate each selected container row with the 'Execution Country' value
laborRows = Product.GetContainerByName('PRMS_Additional_Labor_Container')
execCountry = Product.Attr('PRMS_Addi_Labor_Execution_Country').GetValue()
updatePrice = 0
for row in laborRows.Rows:
    if row.IsSelected:
        row.GetColumnByName('Execution Country').Value = execCountry
        updatePrice = 1
        #row.IsSelected=False
laborRows.Calculate()
if updatePrice:
    ScriptExecutor.Execute('PS_PRMS_Update_Labor_Cost')
Product.Attr('PRMS_Addi_Labor_Execution_Country').SelectDisplayValue('')