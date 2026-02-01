#Populate each selected container row with the 'Execution Year' value
laborRows = Product.GetContainerByName('PRMS_Engineering_Labor_Container')
execYear = TagParserProduct.ParseString('<* Value(PRMS_Labor_Execution_Year) *>')
updateFlag = 0
for row in laborRows.Rows:
    if row.IsSelected:
        row.GetColumnByName('Execution Year').Value = execYear
        updateFlag = 1
    #row.IsSelected=False
laborRows.Calculate()
if updateFlag:
    ScriptExecutor.Execute('PS_PRMS_Update_Labor_Cost')
Product.Attr('PRMS_Labor_Execution_Year').SelectDisplayValue('')