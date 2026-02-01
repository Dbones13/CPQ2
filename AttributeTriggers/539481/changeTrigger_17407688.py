#Attribute 'MIQ_ACD_Execution_Year' Change Trigger 
#Populate each selected container row with the 'Execution Year' value
laborCont = Product.GetContainerByName('MIQ Additional Custom Deliverables')
execYear = TagParserProduct.ParseString('<* Value(MIQ_ACD_Execution_Year) *>')
updateFlag = 0
for row in laborCont.Rows:
    if row.IsSelected:
        row.GetColumnByName('Execution Year').Value = execYear
        updateFlag = 1
if updateFlag:
    ScriptExecutor.Execute('PS_Labor_Part_Summary')
laborCont.Calculate()