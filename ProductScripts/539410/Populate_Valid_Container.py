partsQty = dict()
validPartsCon = Product.GetContainerByName("PU_Valid_Parts")

if validPartsCon.Rows.Count > 0:
    for row in validPartsCon.Rows:
        partsQty[row.UniqueIdentifier] = {"Qty" : int(row["Quantity"]), "desc" : str(row["ExtendedDescription"]), "Cost" : row["Unit Cost Price"],"TariffPCT":row["Tariff PCT"]}

for item in Quote.Items:
    if partsQty.get(item.QuoteItemGuid):
        item.Quantity = partsQty[item.QuoteItemGuid]["Qty"]
        item.QI_ExtendedDescription.Value = partsQty[item.QuoteItemGuid]["desc"]
        item.QI_ETO_COST.Value = 0 if partsQty[item.QuoteItemGuid]["Cost"] == '' else int(partsQty[item.QuoteItemGuid]["Cost"])
        item.QI_REGIONAL_ETO_COST.Value = item.QI_ETO_COST.Value * item.Quantity
        item.QI_Tariff_PCT.Value= 0 if partsQty[item.QuoteItemGuid]["TariffPCT"] == '' else float(partsQty[item.QuoteItemGuid]["TariffPCT"])
Quote.Calculate()