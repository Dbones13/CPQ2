#Populate each selected container row with the 'Execution Year' value
laborRows = Product.GetContainerByName('MSE_Engineering_Labor_Container')
execYear = TagParserProduct.ParseString('<* Value(MSE_Engineering_Labor_Execution_Year) *>')
updateFlag = 0
for row in laborRows.Rows:
    if row.IsSelected:
        row.GetColumnByName('Execution Year').Value = execYear
        updateFlag = 1
    #row.IsSelected=False
laborRows.Calculate()
if updateFlag:
    ScriptExecutor.Execute('PS_Refresh_MSE_Labor_Container')
Product.Attr('MSE_Engineering_Labor_Execution_Year').SelectDisplayValue('')