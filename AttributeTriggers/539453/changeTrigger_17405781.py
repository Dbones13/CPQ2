#Attribute 'HMI_Engineering_Labor_Execution_Country' Change Trigger 
#Populate each selected container row with the 'Execution Country' value
laborRows = Product.GetContainerByName('HMI_Engineering_Labor_Container').Rows
execCountry = TagParserProduct.ParseString('<* Value(HMI_Engineering_Labor_Execution_Country) *>')
updateFlag = 0
for row in laborRows:
    if row.IsSelected:
        row.GetColumnByName('Execution Country').Value = execCountry
        updateFlag = 1
#ScriptExecutor.Execute('PS_Populate_Prices')
if updateFlag:
    ScriptExecutor.Execute('PS_Labor_Part_Summary')