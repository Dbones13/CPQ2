import GS_ItemCalculations as ic
if Quote.GetCustomField('Quote Type').Content not in ("Contract New", "Contract Renewal") and Quote.GetCustomField("MPA Price Plan").Content:
	for item in Quote.Items:
		if item.ProductName != 'TPC_Product':
			ic.applyMPA(Quote , item)