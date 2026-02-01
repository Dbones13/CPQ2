#Attribute 'ARO_RESS_Engineering_Labor_Container' Change Trigger 
#Populate each selected container row with the 'Execution Country' value
laborRows = Product.GetContainerByName('DVM_Engineering_Labor_Container').Rows
execCountry = Product.Attr('DVM_Engineering_Labor_Execution_Country').GetValue()
updatePrice = 0
for row in laborRows:
    if row.IsSelected:
        row.GetColumnByName('Execution Country').Value = execCountry
        updatePrice = 1
if updatePrice:
    ScriptExecutor.Execute('PS_Refresh_DVM_Labor_Container')
ScriptExecutor.Execute('PS_DVM_Error_Msg')