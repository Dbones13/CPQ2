#Attribute 'Project_Execution_Year' Change Trigger 
#Populate each selected container row with the 'Execution Year' value
laborRows = Product.GetContainerByName('PLE_Labor_Container').Rows
execYear = TagParserProduct.ParseString('<* Value(PLE_Execution_Year) *>')
updatePrice = 0
for row in laborRows:
    if row.IsSelected:
        row.GetColumnByName('Execution Year').Value = execYear
        updatePrice = 1
if updatePrice:
    ScriptExecutor.Execute('PS_Refresh_PLE_Labor_Container')
#laborRows.Calculate()
ScriptExecutor.Execute('Error_Message')