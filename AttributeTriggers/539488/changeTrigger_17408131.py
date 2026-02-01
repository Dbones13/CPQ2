#Populate each selected container row with the 'Execution Year' value
laborRows = Product.GetContainerByName('MS_ASE_Engineering_Labor_Container')
execYear = TagParserProduct.ParseString('<* Value(MS_ASE_Labor_Execution_Year) *>')
updateFlag = 0
for row in laborRows.Rows:
    if row.IsSelected:
        row.GetColumnByName('Execution Year').Value = execYear
        updateFlag = 1
    #row.IsSelected=False
laborRows.Calculate()
if updateFlag:
    ScriptExecutor.Execute('PS_Labor_Part_Summary')
Product.Attr('MS_ASE_Labor_Execution_Year').SelectDisplayValue('')