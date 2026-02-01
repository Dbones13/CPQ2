#Populate each selected container row with the 'Execution Year' value
laborRows = Product.GetContainerByName('IS_Additional_Labor_Container')
execYear = TagParserProduct.ParseString('<* Value(IS_Addi_Labor_Execution_Year) *>')
updateFlag = 0
for row in laborRows.Rows:
    if row.IsSelected:
        row.GetColumnByName('Execution Year').Value = execYear
        updateFlag = 1
    #row.IsSelected = False
laborRows.Calculate()
if updateFlag:
    ScriptExecutor.Execute('PS_IS_Update_Labor_Cost')
Product.Attr('IS_Addi_Labor_Execution_Year').SelectDisplayValue('')