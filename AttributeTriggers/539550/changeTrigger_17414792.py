#Attribute 'PMD_CD_LaborDeliverables_Execution Country' Change Trigger 
#Populate each selected container row with the 'Execution Country' value
laborRows = Product.GetContainerByName('PMD Labor Additional Custom Deliverable')
execYear = TagParserProduct.ParseString('<*VALUE(PMD_CD_LaborDeliverables_Execution Country)*>')
for row in laborRows.Rows:
    if row.IsSelected:
        row.GetColumnByName('Execution Country').Value = execYear
        row.GetColumnByName('UpdatedYear').Value = execYear
laborRows.Calculate()
ScriptExecutor.Execute('Show_PMD_Error_Deliverables')