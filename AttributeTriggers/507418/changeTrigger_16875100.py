#Attribute 'PAGA_Additional_Labour_Container' Change Trigger 
#Populate each selected container row with the 'Execution Year' value
laborRows = Product.GetContainerByName('PAGA_Additional_Labour_Container')
execYear = TagParserProduct.ParseString('<* Value(PAGA_Ad_ExecutionYear) *>')
updateFlag = 0
for row in laborRows.Rows:
    if row.IsSelected:
        row.GetColumnByName('Execution Year').Value = execYear
        updateFlag = 1
        #row.IsSelected=False
laborRows.Calculate()
if updateFlag:
    ScriptExecutor.Execute('PS_PAGA_Update_Labor_Cost')
Product.Attr('PAGA_Ad_ExecutionYear').SelectDisplayValue('')