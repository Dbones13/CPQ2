partsQty = dict()
validPartsCon = Product.GetContainerByName("Winest_Labor_PriceCost_Cont")
if validPartsCon.Rows.Count > 0:
    for row in validPartsCon.Rows:
        partsQty[row.UniqueIdentifier] = [row['Year'], row['Qty']]
    Trace.Write("PS_TransferDataToQuote dictionary: " + str(partsQty))

for item in arg.QuoteItemCollection:
    Trace.Write("QuoteItemGuid for " + str(item.PartNumber) + " : " + str(item.QuoteItemGuid))
    if item.QuoteItemGuid in partsQty:
        item['QI_Year'].Value = partsQty[item.QuoteItemGuid][0] if partsQty[item.QuoteItemGuid][0] != 'No Multi-year' else ''
        item.Quantity = float(partsQty[item.QuoteItemGuid][1])
        item['QI_Winest_Import'].Value = 'True'
Quote.Calculate()