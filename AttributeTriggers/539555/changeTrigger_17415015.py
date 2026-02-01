#Populate each selected container row with the 'Execution Country' value
laborRows = Product.GetContainerByName('Gas_MeterSuite_Additional_Labor_Container')
execCountry = Product.Attr('GAS_MeterSuite_Addi_Labor_Execution_Country').GetValue()
updatePrice = 0
for row in laborRows.Rows:
    if row.IsSelected:
        row.GetColumnByName('Execution Country').Value = execCountry
        updatePrice = 1
        #row.IsSelected=False
    laborRows.Calculate()
if updatePrice:
    ScriptExecutor.Execute('PS_GMS_Update_Labor_Cost')
Product.Attr('GAS_MeterSuite_Addi_Labor_Execution_Country').SelectDisplayValue('')