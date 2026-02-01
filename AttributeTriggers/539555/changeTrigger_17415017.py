#Populate each selected container row with the 'Execution Year' value
laborRows = Product.GetContainerByName('Gas_MeterSuite_Additional_Labor_Container')
execYear = TagParserProduct.ParseString('<* Value(GAS_MeterSuite_Addi_Labor_Execution_Year) *>')
updateFlag = 0
for Row in laborRows.Rows:
    if Row.IsSelected:
        Row.GetColumnByName('Execution Year').Value = execYear
        updateFlag = 1
    #Row.IsSelected=False
laborRows.Calculate()
if updateFlag:
    ScriptExecutor.Execute('PS_GMS_Update_Labor_Cost')
Product.Attr('GAS_MeterSuite_Addi_Labor_Execution_Year').SelectDisplayValue('')