if Quote.GetGlobal('PerformanceUpload') != 'Yes':
	"""
	PLSG = {}
	PLSGDesc = {}
	getparts =SqlHelper.GetList("SELECT ci.CATALOGCODE, hp.PLSG, hp.PLSGDesc  FROM CART_ITEM ci  JOIN HPS_PRODUCTS_MASTER hp ON ci.CATALOGCODE = hp.PartNumber  WHERE ci.CART_ID = '"+str(Quote.QuoteId)+"' AND ci.USERID = '"+str(Quote.UserId)+"'")
	if getparts:
		PLSG = {item.CATALOGCODE: item.PLSG for item in getparts}
		PLSGDesc = {item.CATALOGCODE: item.PLSGDesc for item in getparts}
	"""
	for Item in Quote.MainItems:
		"""
		if Item.PartNumber in PLSG:
			Item['QI_PLSG'].Value = PLSG[Item.PartNumber]
		if Item.PartNumber in PLSGDesc:
			Item['QI_PLSGDesc'].Value = PLSGDesc[Item.PartNumber]
		"""
		if Item.ParentItemGuid == '' and Item.PartNumber in ('Experion Station Upgrade', 'Experion Server Upgrade', 'Experion Controller Upgrade'):
			for item in Item.AsMainItem.Children:
				for attr in item.SelectedAttributes:
					if attr.Name=="ItemQuantity":
						for value in attr.Values:
							item.Quantity= float(Item.Quantity) * float(value.Display)
						break