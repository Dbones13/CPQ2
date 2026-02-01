if Session["prevent_execution"] != "true":
	#CC_CI_Update_PLSG_and_PLSGDesc
	def getItemAttrValue(Item):
		resDict = dict()
		for attribute in Item.SelectedAttributes:
			resDict[attribute.Name] = attribute.Values[0].Display
		return resDict

	query = "SELECT PLSG, PLSGDesc FROM HPS_PRODUCTS_MASTER WHERE PartNumber = '{}'"
	result = SqlHelper.GetFirst(query.format(Item.PartNumber))
	defaultPLSG = ''
	defaultPLSGDesc = ''
	if not result and Item.ProductTypeName  != 'Write-In':
		resDict = getItemAttrValue(Item)
		defaultPLSG = resDict.get('Product line sub group', '')
		defaultPLSGDesc = resDict.get('PLSG description', '')
	if Item.ProductTypeName  != 'Write-In':
		Item.QI_PLSG.Value = result.PLSG if result else defaultPLSG
		Item.QI_PLSGDesc.Value = result.PLSGDesc if result else defaultPLSGDesc

	if Item.ParentItemGuid == '' and Item.PartNumber in ('Experion Station Upgrade', 'Experion Server Upgrade', 'Experion Controller Upgrade'):
		for item in Quote.Items:
			if item.ParentItemGuid==Item.QuoteItemGuid:
				for attr in item.SelectedAttributes:
					if attr.Name=="ItemQuantity":
						for value in attr.Values:
							item.Quantity= float(Item.Quantity) * float(value.Display)
						break