def getListofPartsToBeOmit():
	partsToBeOmit = []
	res = SqlHelper.GetList("SELECT parts from Document_ToBe_Omit_Parts where Filter = 'dummy'")
	if res is not None:
		for row in res:
			partsToBeOmit.append(row.parts)
	return partsToBeOmit

partsTobeOmit = getListofPartsToBeOmit()

i = 1
for item in Quote.Items:
	if item.PartNumber not in partsTobeOmit:
		item['Orderable_ItemId'].Value = str(i)
		i +=1