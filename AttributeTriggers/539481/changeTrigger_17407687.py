#Attribute 'MIQ_Execution_Year' Change Trigger 
#Populate each selected container row with the 'Execution Year' value
laborCont = Product.GetContainerByName('MIQ Engineering Labor Container')
execYear = TagParserProduct.ParseString('<* Value(MIQ_Execution_Year) *>')
updateFlag = 0
for row in laborCont.Rows:
    if row.IsSelected:
        row.GetColumnByName('Execution Year').Value = execYear
        updateFlag = 1
if updateFlag:
    ScriptExecutor.Execute('PS_Labor_Part_Summary')
laborCont.Calculate()