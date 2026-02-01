#Attribute 'SM_Labor_Execution_Country' Change Trigger 
#Populate each selected container row with the 'Execution Country' value
laborRows = Product.GetContainerByName('SM_Additional_Custom_Deliverables_Labor_Container').Rows
execCountry = TagParserProduct.ParseString('<* Value(SM_Labor_Execution_Country_adc) *>')
for row in laborRows:
    if row.IsSelected:
        row.GetColumnByName('Execution Country').Value = execCountry
ScriptExecutor.Execute('PS_Populate_Prices')