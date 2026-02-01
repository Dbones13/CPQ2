#Populate each selected container row with the 'Execution Country' value
laborRows = Product.GetContainerByName('MSID_Labor_Virtualization_con').Rows
execCountry = TagParserProduct.ParseString('<* Value(Virtualization_Execution_Country) *>')
for row in laborRows:
    if row.IsSelected:
        row.GetColumnByName('Execution_Country').Value = execCountry
#ScriptExecutor.Execute('PS_Populate_Prices')