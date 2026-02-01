#Populate each selected container row with the 'Execution Country' value
laborRows = Product.GetContainerByName('MS_ASE_Additional_Labour_Container')
execCountry = Product.Attr('MS_ASE_Addi_Labor_Execution_Country').GetValue()
updatePrice = 0
for row in laborRows.Rows:
    if row.IsSelected:
        row.GetColumnByName('Execution Country').Value = execCountry
        updatePrice = 1
        #row.IsSelected=False
    laborRows.Calculate()
if updatePrice:
    ScriptExecutor.Execute('PS_Labor_Part_Summary')
Product.Attr('MS_ASE_Addi_Labor_Execution_Country').SelectDisplayValue('')