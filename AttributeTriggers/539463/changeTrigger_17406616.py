#Populate each selected container row with the 'Execution Country' value
laborRows = Product.GetContainerByName('PCD Engineering Labor Container').Rows
execCountry = TagParserProduct.ParseString('<* Value(PCD_Execution_Country) *>')
updateFlag = 0
for row in laborRows:
    if row.IsSelected:
        row.GetColumnByName('Execution Country').Value = execCountry
        updateFlag = 1
if updateFlag:
    ScriptExecutor.Execute('PS_Labor_Part_Summary')
ScriptExecutor.Execute('PS_Show_PCD_Error_Deliverables')