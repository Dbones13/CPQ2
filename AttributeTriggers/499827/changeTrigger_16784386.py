#Attribute 'Project_Execution_Country' Change Trigger 
#Populate each selected container row with the 'Execution Country' value
laborCont = Product.GetContainerByName('PM_Additional_Custom_Deliverables_Labor_Container')
execCountry = TagParserProduct.ParseString('<* Value(Project_Additional_Execution_Country) *>')
updatePrice = 0
for row in laborCont.Rows:
    if row.IsSelected:
        row.GetColumnByName('Execution Country').Value = execCountry
        updatePrice = 1
if updatePrice:
    ScriptExecutor.Execute('PS_Refresh_Custom_Deliverables_Labor_Container')
ScriptExecutor.Execute('Error_Message')