#Attribute 'SCADA_Labor_Execution_Year' Change Trigger 
#Populate each selected container row with the 'Execution Year' value
laborRows = Product.GetContainerByName('SCADA_Engineering_Labor_Container').Rows
execYear = TagParserProduct.ParseString('<* Value(SCADA_Labor_Execution_Year) *>')
for row in laborRows:
    if row.IsSelected:
        row.GetColumnByName('Execution Year').Value = execYear
ScriptExecutor.Execute('PS_Populate_Prices')
#laborRows.Calculate()