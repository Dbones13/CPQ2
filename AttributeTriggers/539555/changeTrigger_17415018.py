#Populate each selected container row with the 'Execution Year' value
laborRows = Product.GetContainerByName('Gas_MeterSuite_Engineering_Labor_Container')
execYear = TagParserProduct.ParseString('<* Value(GAS_MeterSuite_Labor_Execution_Year) *>')
updateFlag = 0
for row in laborRows.Rows:
    if row.IsSelected:
        row.GetColumnByName('Execution Year').Value = execYear
        updateFlag = 1
    #row.IsSelected=False
laborRows.Calculate()
if updateFlag:
    ScriptExecutor.Execute('PS_GMS_Update_Labor_Cost')
Product.Attr('GAS_MeterSuite_Labor_Execution_Year').SelectDisplayValue('')