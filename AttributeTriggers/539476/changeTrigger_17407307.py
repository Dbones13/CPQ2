#Attribute 'FDM_ACD_Execution_Year' Change Trigger 
#Populate each selected container row with the 'Execution Year' value
laborRows = Product.GetContainerByName('FDM Additional Custom Deliverables')
execYear = TagParserProduct.ParseString('<* Value(FDM_ACD_Execution_Year) *>')
updateFlag = 0
for row in laborRows.Rows:
    if row.IsSelected:
        row.GetColumnByName('Execution Year').Value = execYear
        updateFlag = 1
if updateFlag:
    ScriptExecutor.Execute('PS_Labor_Part_Summary')
laborRows.Calculate()
ScriptExecutor.Execute('PS_Show_FDM_Error_Deliverables')