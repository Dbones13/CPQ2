#Populate each selected container row with the 'Execution Year' value
laborCont = Product.GetContainerByName('Generic Engineering Labor Container')
execYear = TagParserProduct.ParseString('<* Value(Generic_Execution_Year) *>')
updateFlag = 0
for row in laborCont.Rows:
    if row.IsSelected:
        row.GetColumnByName('Execution Year').Value = execYear
        updateFlag = 1
if updateFlag:
    ScriptExecutor.Execute('PS_Labor_Part_Summary')
laborCont.Calculate()
ScriptExecutor.Execute('PS_Show_Generic_Error_Deliverables')