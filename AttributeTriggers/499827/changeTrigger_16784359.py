#Attribute 'Project_Execution_Country' Change Trigger
#Populate each selected container row with the 'Execution Country' value
laborCont = Product.GetContainerByName('Project_management_Labor_Container')
execCountry = TagParserProduct.ParseString('<* Value(Project_Execution_Country) *>')
updatePrice =0
for row in laborCont.Rows:
    if row.IsSelected:
        row.GetColumnByName('Execution Country').Value = execCountry
        #row.Calculate()
        updatePrice = 1
if updatePrice:
    ScriptExecutor.Execute('PS_Refresh_PM_Labor_Container')
ScriptExecutor.Execute('Error_Message')