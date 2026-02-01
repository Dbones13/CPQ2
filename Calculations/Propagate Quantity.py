def updateChildQty():
	if Item.ParentItemGuid == '' and Item.PartNumber in ['IAA -Project','IAA -Spot','PRJT','Migration']:
		Item.Quantity = 1
	if Item.ParentItemGuid == '' and Item.PartNumber in ['PRJT','Migration']:
		return 0
	for item in Quote.Items:
		if item.ParentItemGuid==Item.QuoteItemGuid:
			for attr in item.SelectedAttributes:
				if attr.Name=="ItemQuantity":
					for value in attr.Values:
						Trace.Write("Child Part number "+item.PartNumber+"Parent "+Item.PartNumber+" Name "+attr.Name+"Child Qty "+value.Display)
						item.Quantity= float(Item.Quantity) * float(value.Display)
					break
			#break
	return 1

if (Quote.GetCustomField('CF_Plant_Prevent_Calc').Content != 'true' or Quote.GetCustomField('Booking LOB').Content != 'PMC'):
	val = updateChildQty()