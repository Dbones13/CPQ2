#PS_PM_Labor_Pricing_in_Quote
def getFloat(Var):
	return float(Var) if Var else 0.00

partsNumbers = {}
labor_cont = Product.GetContainerByName('Labor_PM_PriceCost_Cont')

for material in labor_cont.Rows:
	qty = getFloat(material["Qty"])
	if qty == 0.0:
		continue
	system = partsNumbers[material["Part Number"]] = {}
	total_cost = getFloat(material["Total Cost"])
	if total_cost != 0.0:
		system["QI_GESRegionalCost"] = total_cost / qty
	total_list_price = getFloat(material["Total List Price"])
	if total_list_price != 0.0:
		system["QI_LaorPartsListPrice"] = total_list_price / qty
	total_wtw_cost = getFloat(material["Total WTW Cost"])
	if total_wtw_cost != 0.0:
		system["QI_UnitWTWCost"] = total_wtw_cost / qty
	total_mpa_price = getFloat(material["Total MPA Price"])
	if total_mpa_price != 0.0:
		system["QI_MPA_Price"] = total_mpa_price / qty

#This adds values from the dictionary to the fields in the quote line item
parentItemGuid = ''
for item in arg.QuoteItemCollection:
	if item.PartNumber == 'PRJT':
			parentItemGuid = item.QuoteItemGuid
	elif parentItemGuid == item.ParentItemGuid and item.PartNumber in partsNumbers:
		partData = partsNumbers.get(item.PartNumber,None)
		if partData:
			for each in partData:
				if each == 'QI_GESRegionalCost':
					item.QI_GESRegionalCost.Value = getFloat(partData[each])
				elif each == 'QI_LaorPartsListPrice':
					item.QI_LaorPartsListPrice.Value = getFloat(partData[each])
				elif each == 'QI_UnitWTWCost':
					item.QI_FoWTWCost.Value = getFloat(partData[each])
				elif each == 'QI_MPA_Price':
					item.QI_MPA_Price.Value = getFloat(partData[each])