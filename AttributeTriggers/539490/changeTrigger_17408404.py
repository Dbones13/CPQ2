#Attribute 'Experion_mx_Labor_Execution_Country_adc' Change Trigger 
#Populate each selected container row with the 'Execution Country' value
laborRows = Product.GetContainerByName('Experion_mx_labor_Additional_Cust_Deliverables_con').Rows
execCountry = TagParserProduct.ParseString('<* Value(Experion_mx_Labor_Execution_Country_adc) *>')
for row in laborRows:
    if row.IsSelected:
        row.GetColumnByName('Execution Country').Value = execCountry
ScriptExecutor.Execute('PS_Populate_Prices')