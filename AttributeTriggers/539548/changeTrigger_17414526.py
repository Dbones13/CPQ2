laborRows = Product.GetContainerByName('MSID_Labor_Generic_System4_Cont').Rows
execCountry = TagParserProduct.ParseString('<* Value(Generic4_Execution_Country) *>')
for row in laborRows:
    if row.IsSelected:
        row.GetColumnByName('Execution_Country').Value = execCountry
        Product.Attr('Generic4_Execution_Country').SelectValue('No Option Selected')
        #row.IsSelected=False
#ScriptExecutor.Execute('PS_Populate_Prices')