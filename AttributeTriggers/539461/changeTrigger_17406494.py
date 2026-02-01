#Attribute 'UOC_CD_LD_Engineering_Execution_Year' Change Trigger 
#Populate each selected container row with the 'Execution Year' value
laborRows = Product.GetContainerByName('CE UOC Additional Custom Deliverables').Rows
execYear = TagParserProduct.ParseString('<*VALUE(UOC_CD_LD_Engineering_Execution Year)*>')
updateFlag = 0
for row in laborRows:
    if row.IsSelected:
        row.GetColumnByName('Execution Year').Value = execYear
        updateFlag = 1
if updateFlag:
    ScriptExecutor.Execute('PS_Refresh_Labor_Containers_Data')
#ScriptExecutor.Execute('PS_Refresh_Labor_Containers_Data')
#laborRows.Calculate()