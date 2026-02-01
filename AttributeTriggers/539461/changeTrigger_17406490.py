#Attribute 'UOC_CD_LD_Engineering_Execution_Year' Change Trigger 
#Populate each selected container row with the 'Execution Year' value
laborRows = Product.GetContainerByName('CE UOC Additional Custom Deliverables')
execCount = TagParserProduct.ParseString('<*VALUE(UOC_CD_LaborDeliverables_Execution Country)*>')
updateFlag = 0
for row in laborRows.Rows:
    if row.IsSelected:
        row.GetColumnByName('Execution Country').Value = execCount
        updateFlag = 1
if updateFlag:
    ScriptExecutor.Execute('PS_Refresh_Labor_Containers_Data')
#ScriptExecutor.Execute('PS_Refresh_Labor_Containers_Data')
#laborRows.Calculate()