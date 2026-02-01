#Attribute 'PMD_CD_LD_Engineering_Execution_Year' Change Trigger 
#Populate each selected container row with the 'Execution Year' value
laborRows = Product.GetContainerByName('PMD Labor Additional Custom Deliverable')
execYear = TagParserProduct.ParseString('<*VALUE(PMD_CD_LD_Engineering_Execution_Year)*>')
for row in laborRows.Rows:
    if row.IsSelected:
        row.GetColumnByName('Execution Year').Value = execYear
laborRows.Calculate()
ScriptExecutor.Execute('Show_PMD_Error_Deliverables')