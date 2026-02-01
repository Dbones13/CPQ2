#Attribute 'MSE_Engineering_Labor_Container' Change Trigger 
#Populate each selected container row with the 'Execution Country' value
laborRows = Product.GetContainerByName('MSC_Engineering_Labor_Container')
execCountry = Product.Attr('MSC_Engineering_Labor_Execution_Country').GetValue()
updatePrice = 0
for row in laborRows.Rows:
    if row.IsSelected:
        row.GetColumnByName('Execution Country').Value = execCountry
        updatePrice = 1
    #row.IsSelected=False
laborRows.Calculate()
if updatePrice:
    ScriptExecutor.Execute('PS_Refresh_MSC_Labor_Container')
Product.Attr('MSC_Engineering_Labor_Execution_Country').SelectDisplayValue('')