#Attribute 'PAGA_Labor_Container' Change Trigger 
#Populate each selected container row with the 'Execution Country' value
laborRows = Product.GetContainerByName('PAGA_Labor_Container')
execCountry = Product.Attr('PAGA_Labor_Excecution_Country').GetValue()
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
    ScriptExecutor.Execute('PS_Refresh_PAGA_Labor_Container')
Product.Attr('PAGA_Labor_Excecution_Country').SelectDisplayValue('')