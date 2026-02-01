laborRows = Product.GetContainerByName('MSID_Labor_Generic_System3_Cont').Rows
execCountry = TagParserProduct.ParseString('<* Value(Generic3_Execution_Country) *>')
for row in laborRows:
    if row.IsSelected:
        row.GetColumnByName('Execution_Country').Value = execCountry
        Product.Attr('Generic3_Execution_Country').SelectValue('No Option Selected')
        #row.IsSelected=False
#ScriptExecutor.Execute('PS_Populate_Prices')