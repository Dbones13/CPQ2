#Populate each selected container row with the 'Execution Country' value
laborRows = Product.GetContainerByName('Virtualization_Labor_Deliverable').Rows
execCountry = TagParserProduct.ParseString('<* Value(Virtualization_Labor_Execution_Country) *>')
for row in laborRows:
    if row.IsSelected:
        row.GetColumnByName('Execution Country').Value = execCountry
#ScriptExecutor.Execute('PS_Populate_Prices')