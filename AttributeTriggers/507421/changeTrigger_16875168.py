#Populate each selected container row with the 'Execution Year' value
laborRows = Product.GetContainerByName('OWS_Additional_Labour_Container')
execYear = TagParserProduct.ParseString('<*Value(OWS_Addi_Labor_Execution_Year) *>')
updateFlag = 0
for Row in laborRows.Rows:
    if Row.IsSelected:
        Row.GetColumnByName('Execution Year').Value = execYear
        updateFlag = 1
    #Row.IsSelected=False
laborRows.Calculate()
if updateFlag:
    ScriptExecutor.Execute('PS_Populate_OWS_Labor_Price_Cost')
Product.Attr('OWS_Addi_Labor_Execution_Year').SelectDisplayValue('')