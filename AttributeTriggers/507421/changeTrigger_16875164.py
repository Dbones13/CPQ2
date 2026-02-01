#Populate each selected container row with the 'Execution Year' value
laborRows = Product.GetContainerByName('OWS_Engineering_Labor_Container')
execYear = TagParserProduct.ParseString('<* Value(OWS_Executtion year) *>')
updateFlag = 0
for row in laborRows.Rows:
    if row.IsSelected:
        row.GetColumnByName('Execution Year').Value = execYear
        updateFlag = 1
    #row.IsSelected=False
laborRows.Calculate()
if updateFlag:
    ScriptExecutor.Execute('PS_Populate_OWS_Labor_Price_Cost')
Product.Attr('OWS_Executtion year').SelectDisplayValue('')