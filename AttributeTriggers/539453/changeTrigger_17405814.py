#Attribute 'SM_Labor_Execution_Year' Change Trigger 
#Populate each selected container row with the 'Execution Year' value
laborRows = Product.GetContainerByName('System_Network_Engineering_Labor_Container').Rows
execYear = TagParserProduct.ParseString('<* Value(System_Network_Labor_Execution_Year) *>')
updateFlag = 0
for row in laborRows:
    if row.IsSelected:
        row.GetColumnByName('Execution Year').Value = execYear
        updateFlag = 1

if updateFlag:
    ScriptExecutor.Execute('PS_Labor_Part_Summary')