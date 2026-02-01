#Populate each selected container row with the 'Execution Year' value
laborRows = Product.GetContainerByName('PRMS_Additional_Labor_Container')
execYear = TagParserProduct.ParseString('<* Value(PRMS_Addi_Labor_Execution_Year) *>')
updateFlag = 0
for Row in laborRows.Rows:
    if Row.IsSelected:
        Row.GetColumnByName('Execution Year').Value = execYear
        updateFlag = 1
        #Row.IsSelected=False
    laborRows.Calculate()
laborRows.Calculate()
if updateFlag:
    ScriptExecutor.Execute('PS_PRMS_Update_Labor_Cost')
Product.Attr('PRMS_Addi_Labor_Execution_Year').SelectDisplayValue('')