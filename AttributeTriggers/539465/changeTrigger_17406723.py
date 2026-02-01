laborRows = Product.GetContainerByName('CE RTU Additional Custom Deliverables')
execYear = TagParserProduct.ParseString('<*VALUE(RTU_CD_LD_Engineering_Execution Year)*>')
updateFlag = 0
for row in laborRows.Rows:
    if row.IsSelected:
        row.GetColumnByName('Execution Year').Value = execYear
        updateFlag = 1
if updateFlag:
    ScriptExecutor.Execute('PS_Refresh_Labor_Containers_Data')
#laborRows.Calculate()
ScriptExecutor.Execute('PS_Show_RTU_Error_Deliverables')