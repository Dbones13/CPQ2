#Attribute 'TGE_Engineering_Labor_Container' Change Trigger 
#Populate each selected container row with the 'Execution Country' value
laborRows = Product.GetContainerByName('TGE_Engineering_Labor_Container')
execCountry = Product.Attr('TGE_Labor_Execution_Country').GetValue()
updatePrice = 0
for row in laborRows.Rows:
    if row.IsSelected:
        row.GetColumnByName('Execution Country').Value = execCountry
        updatePrice = 1
    #row.IsSelected=False
laborRows.Calculate()
if updatePrice:
    ScriptExecutor.Execute('PS_Populate_TGE_Labor_Price_Cost')
Product.Attr('TGE_Labor_Execution_Country').SelectDisplayValue('')
ScriptExecutor.Execute('PS_TGE_Error_Msg')