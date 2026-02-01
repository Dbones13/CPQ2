#Attribute 'CE PMD Engineering Execution Country' Change Trigger 
#Populate each selected container row with the 'Execution Country' value
laborRows = Product.GetContainerByName('PMD Engineering Labor Container').Rows
execCountry = TagParserProduct.ParseString('<* Value(CE PMD Engineering Execution Country) *>')
for row in laborRows:
    if row.IsSelected:
        row.GetColumnByName('Execution Country').Value = execCountry
ScriptExecutor.Execute('Show_PMD_Error_Deliverables')