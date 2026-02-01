def DeleteQuoteTableItem(quoteItemGuids):
	table = Quote.QuoteTables["Migration_Document_Data"]
	item_delete = [row.Id for row in table.Rows if row['MIgration_GUID'] and row['MIgration_GUID'] not in quoteItemGuids]

	for r in sorted(item_delete, reverse=True):
		table.DeleteRow(r)
	table.Save()

quoteType = Quote.GetCustomField("Quote Type").Content
lob = Quote.GetCustomField("Booking LOB").Content

quoteItemGuids = []
if lob == "LSS":
	if quoteType == 'Projects':
		quoteItemGuids = [x.QuoteItemGuid for x in Quote.MainItems if x.PartNumber == 'IAA -Project']
	elif quoteType == 'Parts and Spot':
		quoteItemGuids = [x.QuoteItemGuid for x in Quote.MainItems if x.PartNumber == 'IAA -Spot']

	DeleteQuoteTableItem(quoteItemGuids)