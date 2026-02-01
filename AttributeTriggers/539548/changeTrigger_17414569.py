#Populate each selected container row with the 'Execution Country' value Janhavi Tanna : CXCPQ-60159 :start 
laborRows = Product.GetContainerByName('MSID_Labor_ELEPIU_con')
execCountry = TagParserProduct.ParseString('<*Value(ELEPIU_Execution_Country) *>')
for row in laborRows.Rows:
    if row.IsSelected:
        row.GetColumnByName('Execution_Country').Value = execCountry
        #row.IsSelected=False
laborRows.Calculate()
#ScriptExecutor.Execute('PS_Populate_Prices')
ScriptExecutor.Execute('PS_PopulateGESCost')
Product.Attr('ELEPIU_Execution_Country').SelectDisplayValue('')
#Janhavi Tanna : CXCPQ-60159 :End