#Attribute 'Labor_Execution_Country' Change Trigger 
#Populate each selected container row with the 'Execution Country' value
laborRows = Product.GetContainerByName('Labor_Container').Rows
execCountry = TagParserProduct.ParseString('<* Value(Labor_Execution_Country) *>')
updatePrice = 0
for row in laborRows:
    if row.IsSelected:
        row.GetColumnByName('Execution Country').Value = execCountry
        updatePrice = 1
if updatePrice:
    ScriptExecutor.Execute('PS_Refresh_Labor_Container')
ScriptExecutor.Execute('Error_Message')