#Attribute 'FGC_Additional_Labour_Container' Change Trigger 
#Populate each selected container row with the 'Execution Year' value
laborRows = Product.GetContainerByName('FGC_Additional_Labour_Container').Rows
execYear = TagParserProduct.ParseString('<* Value(FGC_Addi_Labor_Execution_Year) *>')
updateFlag = 0
for row in laborRows:
    if row.IsSelected:
        row.GetColumnByName('Execution Year').Value = execYear
        updateFlag = 1
    #row.IsSelected = False
if updateFlag:
    ScriptExecutor.Execute('PS_FGC_Update_Labor_Cost')
Product.Attr('FGC_Addi_Labor_Execution_Year').SelectDisplayValue('')