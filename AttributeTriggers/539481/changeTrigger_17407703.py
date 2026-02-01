#Attribute 'MIQ_ACD_Execution_Country' Change Trigger 
#Populate each selected container row with the 'Execution Country' value
laborRows = Product.GetContainerByName('MIQ Additional Custom Deliverables').Rows
execCountry = TagParserProduct.ParseString('<* Value(MIQ_ACD_Execution_Country) *>')
updateFlag = 0
for row in laborRows:
    if row.IsSelected:
        row.GetColumnByName('Execution Country').Value = execCountry
        updateFlag = 1
if updateFlag:
    ScriptExecutor.Execute('PS_Labor_Part_Summary')