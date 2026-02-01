#Attribute 'PAGA_Labor_Container' Change Trigger 
#Populate each selected container row with the 'Execution Year' value
laborRows = Product.GetContainerByName('PAGA_Labor_Container')
execYear = Product.Attr('PAGA_ExecutionYear').GetValue()
updatePrice = 0
for row in laborRows.Rows:
    if row.IsSelected:
        row.GetColumnByName('Execution Year').Value = execYear
        updatePrice = 1
        #row.IsSelected=False
laborRows.Calculate()
if updatePrice:
    ScriptExecutor.Execute('PS_PAGA_Update_Labor_Cost')
Product.Attr('PAGA_ExecutionYear').SelectDisplayValue('')