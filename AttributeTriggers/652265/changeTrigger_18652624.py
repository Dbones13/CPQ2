contList = ['Winest Labor Container', 'Winest Additional Labor Container']
execCountry = TagParserProduct.ParseString('<* Value(Winest Labor Execution Year) *>')
updateFlag = 0
for cont in contList:
	laborRows = Product.GetContainerByName(cont).Rows
	for row in laborRows:
		if row.IsSelected:
			row.GetColumnByName('Execution Year').Value = execCountry
			updateFlag = 1
if updateFlag:
	ScriptExecutor.Execute('PS_Refresh_Labor_Containers_Data')
ScriptExecutor.Execute('PS_Show_Error_Deliverables')