#Attribute 'SM_Labor_Execution_Year' Change Trigger 
#Populate each selected container row with the 'Execution Year' value
laborRows = Product.GetContainerByName('SM_SSE_Engineering_Labor_Container').Rows
execYear = TagParserProduct.ParseString('<* Value(SM_Labor_Execution_Year) *>')
for row in laborRows:
    if row.IsSelected:
        row.GetColumnByName('Execution Year').Value = execYear
#ScriptExecutor.Execute('PS_Populate_Prices')
#laborRows.Calculate()

laborRows1 = Product.GetContainerByName('SM Safety System - ESD/FGS/BMS/HIPPS Container').Rows
#execYear1 = TagParserProduct.ParseString('<* Value(SM_Labor_Execution_Year) *>')
for row in laborRows1:
    if row.IsSelected:
        row.GetColumnByName('Execution Year').Value = execYear
#ScriptExecutor.Execute('PS_Populate_Prices')
#laborRows1.Calculate()