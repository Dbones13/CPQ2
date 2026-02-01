#Populate each selected container row with the 'Execution Year' value
laborRows = Product.GetContainerByName('PSW_Labor_Container')
execYear = TagParserProduct.ParseString('<* Value(PSW_ Execution_Year) *>')
updateFlag = 0
for row in laborRows.Rows:
    if row.IsSelected:
        row.GetColumnByName('Execution Year').Value = execYear
        updateFlag = 1
    #row.IsSelected=False
laborRows.Calculate()
if updateFlag:
    ScriptExecutor.Execute('PS_PSW_Update_Labor_Cost')
Product.Attr('PSW_ Execution_Year').SelectDisplayValue('')