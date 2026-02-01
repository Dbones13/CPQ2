#Attribute 'C300_Additional_Custom_Deliverables_Container' Change Trigger 
#Populate each selected container row with the 'Execution Country' value
laborRows = Product.GetContainerByName('DVM_Additional_Labour_Container').Rows
execCountry = Product.Attr('DVM_Project_Additional_Execution_Country').GetValue()
updateFlag = 0
for row in laborRows:
    if row.IsSelected:
        row.GetColumnByName('Execution Country').Value = execCountry
        updateFlag = 1
if updateFlag:
    ScriptExecutor.Execute('PS_Labor_Part_Summary')
ScriptExecutor.Execute('PS_DVM_Error_Msg')