#Attribute 'SM_Labor_Execution_Country' Change Trigger 
#Populate each selected container row with the 'Execution Country' value
laborRows = Product.GetContainerByName('SM_SSE_Engineering_Labor_Container').Rows
execCountry = TagParserProduct.ParseString('<* Value(SM_Labor_Execution_Country) *>')
for row in laborRows:
    if row.IsSelected:
        row.GetColumnByName('Execution Country').Value = execCountry
ScriptExecutor.Execute('PS_Populate_Prices')

laborRows1 = Product.GetContainerByName('SM Safety System - ESD/FGS/BMS/HIPPS Container').Rows
execCountry = TagParserProduct.ParseString('<* Value(SM_Labor_Execution_Country) *>')
for row in laborRows1:
    if row.IsSelected:
        row.GetColumnByName('Execution Country').Value = execCountry
ScriptExecutor.Execute('PS_Populate_Prices')