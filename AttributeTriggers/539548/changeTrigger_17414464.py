#Populate each selected container row with the 'Execution Country' value
laborRows = Product.GetContainerByName('3rd_Party_PLC_UOC_Labor').Rows
execCountry = TagParserProduct.ParseString('<* Value(3rd_Party_PLC_UOC_Labor_Execution_country) *>')
for row in laborRows:
    if row.IsSelected:
        row.GetColumnByName('Execution_Country').Value = execCountry
#ScriptExecutor.Execute('PS_Populate_Prices')