#Attribute 'MSC_Engineering_Labor_Container' Change Trigger 
#Populate each selected container row with the 'Execution Year' value
laborRows = Product.GetContainerByName('MSC_Engineering_Labor_Container')
#execYear = Product.Attr('MSC_Engineering_Labor_Execution_Year').GetValue()
execYear = TagParserProduct.ParseString('<*Value(MSC_Engineering_Labor_Execution_Year) *>')
updatePrice = 0
for row in laborRows.Rows:
    if row.IsSelected:
        row.GetColumnByName('Execution Year').Value = execYear
        updatePrice = 1
    #row.IsSelected=False
laborRows.Calculate()
if updatePrice:
    ScriptExecutor.Execute('PS_Refresh_MSC_Labor_Container')
Product.Attr('MSC_Engineering_Labor_Execution_Year').SelectDisplayValue('')