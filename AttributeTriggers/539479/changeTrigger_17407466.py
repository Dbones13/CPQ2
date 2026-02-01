#Attribute 'C300_Engineering_Execution_Country' Change Trigger 
#Populate each selected container row with the 'Execution Country' value
laborRows = Product.GetContainerByName('C300_Engineering_Labor_Container').Rows
execCountry = Product.Attr('C300_Engineering_Execution_Country').GetValue()
updatePrice = 0
for row in laborRows:
    if row.IsSelected:
        row.GetColumnByName('Execution Country').Value = execCountry
        updatePrice = 1
if updatePrice:
    ScriptExecutor.Execute('PS_Refresh_C300_Labor_Container')