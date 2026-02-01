#Attribute 'FDM_Execution_Country' Change Trigger 
#Populate each selected container row with the 'Execution Country' value
laborRows = Product.GetContainerByName('FDM Engineering Labor Container').Rows
execCountry = TagParserProduct.ParseString('<* Value(FDM_Execution_Country) *>')
updateFlag = 0
for row in laborRows:
    if row.IsSelected:
        row.GetColumnByName('Execution Country').Value = execCountry
        updateFlag = 1
if updateFlag:
    ScriptExecutor.Execute('PS_Labor_Part_Summary')
ScriptExecutor.Execute('PS_Show_FDM_Error_Deliverables')