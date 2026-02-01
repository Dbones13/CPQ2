#import GS_CalculateTotals
partsQty = dict()
validPartsCon = Product.GetContainerByName("PU_Valid_Parts")

if validPartsCon.Rows.Count > 0:
    for row in validPartsCon.Rows:
        partsQty[row.UniqueIdentifier] = {"Qty" : int(row["Quantity"]), "desc" : str(row["ExtendedDescription"]), "Cost" : row["Unit Cost Price"],"TariffPCT":row["Tariff PCT"]}
        #partsQty[row.UniqueIdentifier] = {"desc" : str(row["ExtendedDescription"])}

for item in Quote.Items:
    if partsQty.get(item.QuoteItemGuid):
        item.Quantity = partsQty[item.QuoteItemGuid]["Qty"]
        item.QI_ExtendedDescription.Value = partsQty[item.QuoteItemGuid]["desc"]
        item.QI_ETO_COST.Value = 0 if partsQty[item.QuoteItemGuid]["Cost"] == '' else int(partsQty[item.QuoteItemGuid]["Cost"])
        item.QI_REGIONAL_ETO_COST.Value = item.QI_ETO_COST.Value * item.Quantity
        item.QI_Tariff_PCT.Value= 0 if partsQty[item.QuoteItemGuid]["TariffPCT"] == '' else float(partsQty[item.QuoteItemGuid]["TariffPCT"])
        '''if item.QI_Tariff_PCT.Value:
                item.QI_Tariff_Amount.Value = (item.ExtendedAmount * item.QI_Tariff_PCT.Value)/100
        item.QI_Sell_Price_Inc_Tariff.Value = item.ExtendedAmount + item.QI_Tariff_Amount.Value
totalDict=GS_CalculateTotals.calculateQuoteTotals(Quote)
quoteTotalTable = Quote.QuoteTables["Quote_Details"]

if quoteTotalTable.Rows.Count != 0:
    row = quoteTotalTable.Rows[0]
    row['Total_Tariff_Amount'] 	= totalDict.get('totalTariffAmount' , 0)
    row['Quote_Sell_Price_Incl_Tariff'] = totalDict.get('totalSellPriceInclTariff', 0)
    Quote.GetCustomField('Total_Sell_Price_Incl_Tariff').Content=UserPersonalizationHelper.ToUserFormat(row['Quote_Sell_Price_Incl_Tariff'])
    Quote.GetCustomField('Total_Tariff_Amount').Content=UserPersonalizationHelper.ToUserFormat(row['Total_Tariff_Amount'])'''
Quote.Calculate()