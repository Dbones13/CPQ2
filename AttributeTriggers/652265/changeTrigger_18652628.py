def buildDict(prodAttr, outDict = dict()):
	for v in prodAttr.Values:
		if v.ValueCode != 'None':
			outDict[v.ValueCode] = v.Display
	return outDict

contList = ['Winest Labor Container','Winest Additional Labor Container']
loc_map = {"GES India":"IN","GES China":"CN","GES Romania":"RO","GES Uzbekistan":"UZ","GES Egypt":"EG"}
service_material_dict = buildDict(Product.Attr('Winest Service Material'))
loc = TagParserProduct.ParseString('<* Value(Winest GES Location) *>')
updateFlag = 0
for cont in contList:
	laborRows = Product.GetContainerByName(cont).Rows
	for row in laborRows:
		if row.IsSelected:
			if "GES" in row.GetColumnByName('Service Material').Value:
				material = str(row.GetColumnByName('Service Material').Value)[:-2] + loc_map[loc]
				row.GetColumnByName('Material Number').Value = material
				row.GetColumnByName('Service Material').SetAttributeValue(service_material_dict[material])
				row.GetColumnByName('Service Material').Value = material
				updateFlag = 1
if updateFlag:
	ScriptExecutor.Execute('PS_Refresh_Labor_Containers_Data')
ScriptExecutor.Execute('PS_Show_Error_Deliverables')