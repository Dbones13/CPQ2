#Attribute 'HC900_Execution_Year' Change Trigger 
#Populate each selected container row with the 'Execution Year' value
laborCont = Product.GetContainerByName('HC900 Engineering Labor Container')
execYear = TagParserProduct.ParseString('<* Value(HC900_Execution_Year) *>')
updateFlag = 0
for row in laborCont.Rows:
    if row.IsSelected:
        row.GetColumnByName('Execution Year').Value = execYear
        updateFlag = 1
if updateFlag:
    ScriptExecutor.Execute('PS_Labor_Part_Summary')
laborCont.Calculate()
ScriptExecutor.Execute('PS_Show_HC900_Error_Deliverables')