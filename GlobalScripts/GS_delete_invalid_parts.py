tbl = Quote.QuoteTables['FME_Invalid_Parts']
if tbl.Rows.Count:
	quote_items = [str(i.PartNumber) for i in Quote.Items]
	for row in tbl.Rows:
		if row["Part_Number"] in quote_items:
			tbl.DeleteRow(row.Id)