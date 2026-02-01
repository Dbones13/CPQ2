#Attribute 'CE RTU Engineering Execution Country' Change Trigger 
#Populate each selected container row with the 'Execution Country' value
laborRows = Product.GetContainerByName('CE RTU Engineering Labor Container').Rows
execCountry = TagParserProduct.ParseString('<* Value(CE RTU Engineering Execution Country) *>')
updateFlag = 0
for row in laborRows:
    if row.IsSelected:
        row.GetColumnByName('Execution Country').Value = execCountry
        updateFlag = 1
if updateFlag:
    ScriptExecutor.Execute('PS_Refresh_Labor_Containers_Data')
ScriptExecutor.Execute('PS_Show_RTU_Error_Deliverables')