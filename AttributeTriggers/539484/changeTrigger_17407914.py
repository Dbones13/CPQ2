#Populate each selected container row with the 'Execution Year' value
laborRows = Product.GetContainerByName('TGE_Engineering_Labor_Container')
execYear = TagParserProduct.ParseString('<* Value(TGE_Executtion year) *>')
updateFlag = 0
for row in laborRows.Rows:
    if row.IsSelected:
        row.GetColumnByName('Execution Year').Value = execYear
        updateFlag = 1
    #row.IsSelected=False
laborRows.Calculate()
if updateFlag:
    ScriptExecutor.Execute('PS_Populate_TGE_Labor_Price_Cost')
Product.Attr('TGE_Executtion year').SelectDisplayValue('')
ScriptExecutor.Execute('PS_TGE_Error_Msg')