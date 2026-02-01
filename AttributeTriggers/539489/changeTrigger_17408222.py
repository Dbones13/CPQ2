#Attribute 'MSC_Additional_Labour_Container' Change Trigger 
#Populate each selected container row with the 'Execution Country' value
laborRows = Product.GetContainerByName('MSC_Additional_Labour_Container')
execCountry = TagParserProduct.ParseString('<* Value(MSC_Addi_Labor_Execution_Country) *>')
updateFlag = 0
for row in laborRows.Rows:
    if row.IsSelected:
        row.GetColumnByName('Execution Country').Value = execCountry
        updateFlag = 1
        #row.IsSelected=False
	laborRows.Calculate()
if updateFlag:
    ScriptExecutor.Execute('PS_Labor_Part_Summary')
#Product.Attr('MSC_Addi_Labor_Execution_Country').SelectDisplayValue('')