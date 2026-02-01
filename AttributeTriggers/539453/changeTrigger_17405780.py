#Attribute 'SM_Labor_Execution_Year' Change Trigger 
#Populate each selected container row with the 'Execution Year' value
laborRows = Product.GetContainerByName('HMI_Engineering_Labor_Container').Rows
execYear = TagParserProduct.ParseString('<* Value(HMI_Engineering_Labor_Execution_Year) *>')
updateFlag = 0
for row in laborRows:
    if row.IsSelected:
        row.GetColumnByName('Execution Year').Value = execYear
        updateFlag = 1
if updateFlag:
    ScriptExecutor.Execute('PS_Labor_Part_Summary')
#ScriptExecutor.Execute('PS_Populate_Prices')
#laborRows.Calculate()