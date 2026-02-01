#Attribute 'Project_Execution_Year' Change Trigger 
#Populate each selected container row with the 'Execution Year' value
laborCont = Product.GetContainerByName('Project_management_Labor_Container')
execYear = TagParserProduct.ParseString('<* Value(Project_Execution_Year) *>')
updatePrice = 0
for row in laborCont.Rows:
    if row.IsSelected:
        row.GetColumnByName('Execution Year').Value = execYear
        #row.Calculate()
        updatePrice = 1
if updatePrice:
    ScriptExecutor.Execute('PS_Refresh_PM_Labor_Container')
ScriptExecutor.Execute('Error_Message')