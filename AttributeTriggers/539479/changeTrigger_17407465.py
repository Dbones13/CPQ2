#Attribute 'C300_Engineering_Labor_Container' Change Trigger 
#Populate each selected container row with the 'Execution Year' value
laborRows = Product.GetContainerByName('C300_Engineering_Labor_Container').Rows
execYear = Product.Attr('C300_Engineering_Execution_Year').GetValue()
updatePrice = 0
for row in laborRows:
    if row.IsSelected:
        row.GetColumnByName('Execution Year').Value = execYear
        updatePrice = 1
if updatePrice:
    ScriptExecutor.Execute('PS_Refresh_C300_Labor_Container')