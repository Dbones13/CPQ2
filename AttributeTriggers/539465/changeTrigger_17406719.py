laborRows = Product.GetContainerByName('CE RTU Engineering Labor Container').Rows
execYear = TagParserProduct.ParseString('<* Value(CE RTU Engineering Execution Year) *>')
for row in laborRows:
    if row.IsSelected:
        row.GetColumnByName('Execution Year').Value = execYear
ScriptExecutor.Execute('PS_Refresh_Labor_Containers_Data')
#laborRows.Calculate()
ScriptExecutor.Execute('PS_Show_RTU_Error_Deliverables')