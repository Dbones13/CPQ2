#Populate each selected container row with the 'Execution Year' value
laborCont = Product.GetContainerByName('Experion HS Additional Custom Deliverables')
execYear = TagParserProduct.ParseString('<* Value(Experion_HS_Execution Year) *>')
updateFlag = 0
for row in laborCont.Rows:
    if row.IsSelected:
        row.GetColumnByName('Execution Year').Value = execYear
        updateFlag = 1
if updateFlag:
    ScriptExecutor.Execute('PS_Labor_Part_Summary')
laborCont.Calculate()
ScriptExecutor.Execute('Show_Experion_HS_Error_Deliverables')