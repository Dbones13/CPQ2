#Populate each selected container row with the 'Execution Year' value
laborRows = Product.GetContainerByName('Virtualization_Additional_Custom_Deliverables').Rows
execCountry = TagParserProduct.ParseString('<* Value(Virtualization_Labor_Execution_Country_adc) *>')
for row in laborRows:
    if row.IsSelected:
        row.GetColumnByName('Execution Country').Value = execCountry
#ScriptExecutor.Execute('PS_Populate_Prices')
#laborRows.Calculate()