#Attribute 'Experion_mx_Labor_Execution_Year_adc' Change Trigger 
#Populate each selected container row with the 'Execution Year' value
laborRows = Product.GetContainerByName('Experion_mx_labor_Additional_Cust_Deliverables_con').Rows
execYear = TagParserProduct.ParseString('<* Value(Experion_mx_Labor_Execution_Year_adc) *>')
for row in laborRows:
    if row.IsSelected:
        row.GetColumnByName('Execution Year').Value = execYear
ScriptExecutor.Execute('PS_Populate_Prices')
laborRows.Calculate()