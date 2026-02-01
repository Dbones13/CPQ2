#Populate each selected container row with the 'Execution Year' value
laborRows = Product.GetContainerByName('IS_Labor_Container').Rows
execYear = TagParserProduct.ParseString('<* Value(IS_Labor_Execution_Year) *>')
updateFlag = 0
for row in laborRows:
    if row.IsSelected:
        row.GetColumnByName('Execution Year').Value = execYear
        updateFlag = 1
    #row.IsSelected = False
if updateFlag:
    ScriptExecutor.Execute('PS_IS_Update_Labor_Cost')
Product.Attr('IS_Labor_Execution_Year').SelectDisplayValue('')