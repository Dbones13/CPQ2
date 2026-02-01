#Populate each selected container row with the 'Execution Country' value
laborRows = Product.GetContainerByName('Experion HS Engineering Labor Container').Rows
execCountry = TagParserProduct.ParseString('<* Value(Experion HS Execution Country) *>')
updateFlag = 0
for row in laborRows:
    if row.IsSelected:
        row.GetColumnByName('Execution Country').Value = execCountry
        updateFlag = 1
if updateFlag:
    ScriptExecutor.Execute('PS_Labor_Part_Summary')
ScriptExecutor.Execute('Show_Experion_HS_Error_Deliverables')