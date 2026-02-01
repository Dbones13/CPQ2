#Populate each selected container row with the 'Execution Year' value
laborRows = Product.GetContainerByName('TGE_Additional_Labour_Container')
execYear = TagParserProduct.ParseString('<* Value(TGE_Addi_Labor_Execution_Year) *>')
updateFlag = 0
for Row in laborRows.Rows:
    if Row.IsSelected:
        Row.GetColumnByName('Execution Year').Value = execYear
        updateFlag = 1
    #Row.IsSelected=False
laborRows.Calculate()
if updateFlag:
    ScriptExecutor.Execute('PS_Populate_TGE_Labor_Price_Cost')
Product.Attr('TGE_Addi_Labor_Execution_Year').SelectDisplayValue('')
ScriptExecutor.Execute('PS_TGE_Error_Msg')