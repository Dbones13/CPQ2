#Populate each selected container row with the 'Execution Year' value
laborRows = Product.GetContainerByName('Virtualization_Labor_Deliverable').Rows
execYear = TagParserProduct.ParseString('<* Value(Virtualization_Labor_Execution_Year) *>')
for row in laborRows:
    if row.IsSelected:
        row.GetColumnByName('Execution Year').Value = execYear
#ScriptExecutor.Execute('PS_Populate_Prices')
#laborRows.Calculate()