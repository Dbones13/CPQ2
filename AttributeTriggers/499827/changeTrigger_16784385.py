laborCont = Product.GetContainerByName('PM_Additional_Custom_Deliverables_Labor_Container')
execYear = TagParserProduct.ParseString('<* Value(Project_Additional_Year) *>')
updatePrice = 0
for row in laborCont.Rows:
    if row.IsSelected:
        row.GetColumnByName('Execution Year').Value = execYear
        #row.Calculate()
        updatePrice = 1
if updatePrice:
    ScriptExecutor.Execute('PS_Refresh_Custom_Deliverables_Labor_Container')
ScriptExecutor.Execute('Error_Message')