#Attribute 'LMS_Labor_Container' Change Trigger 
#Populate each selected container row with the 'Execution Country' value
laborRows = Product.GetContainerByName('LMS_Additional_Labor_Container')
execCountry = Product.Attr('LMS_Ad_Labor_Execution_Country').GetValue()
Trace.Write(execCountry)
updatePrice = 0
for row in laborRows.Rows:
    if row.IsSelected:
        Trace.Write(row)
        row.GetColumnByName('Execution Country').Value = execCountry
        updatePrice = 1
        #row.IsSelected=False
laborRows.Calculate()
if updatePrice:
    #ScriptExecutor.Execute('PS_Refresh_LMS_Labor_Container')
    ScriptExecutor.Execute('PS_LMS_Update_Labor_Cost')
Product.Attr('LMS_Ad_Labor_Execution_Country').SelectDisplayValue('')