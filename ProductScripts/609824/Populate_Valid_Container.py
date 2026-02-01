partsQty = dict()
validPartsCon = Product.GetContainerByName("HPS_PU_Valid_Parts")

if validPartsCon.Rows.Count > 0:
    for row in validPartsCon.Rows:
        Quantity = int(row["Quantity"]) if row["Quantity"] !='' else 0
        Unit_Cost = int(row["Unit Cost Price"]) if row["Unit Cost Price"] !='' else 0
        partsQty[row.UniqueIdentifier] = {"Qty" : Quantity, "desc" : str(row["ExtendedDescription"]), "Cost" : Unit_Cost}
for item in Quote.Items:
    if partsQty.get(item.QuoteItemGuid):
        item.Quantity = partsQty[item.QuoteItemGuid]["Qty"]
        item.QI_ExtendedDescription.Value = partsQty[item.QuoteItemGuid]["desc"]
        Trace.Write('COST-->>'+str(partsQty[item.QuoteItemGuid]["Cost"]))
        item.QI_ETO_COST.Value = partsQty[item.QuoteItemGuid]["Cost"]
        item.QI_REGIONAL_ETO_COST.Value = item.QI_ETO_COST.Value * item.Quantity
        #below code added for fix https://honeywell.atlassian.net/browse/CXCPQ-112904
        item.ExtendedListPrice = item.ListPrice * item.Quantity
        item.ExtendedCost = item.Cost * item.Quantity
        item.QI_TOTAL_COST.Value = item.QI_ETO_COST.Value + item.Cost
        item.QI_TOTAL_EXTENDED_COST.Value = item.QI_TOTAL_COST.Value * item.Quantity
        item.NetPrice = item.ListPrice * (1 - item.DiscountPercent / 100)
        item.ExtendedAmount = item.NetPrice * item.Quantity
        item.QI_Target_Sell_Price.Value = item.ExtendedListPrice - float(item.QI_MPA_Discount_Amount.Value)
        if item.QI_Tariff_PCT.Value:
            item.QI_Tariff_Amount.Value = (item.ExtendedAmount * item.QI_Tariff_PCT.Value)/100
        item.QI_Sell_Price_Inc_Tariff.Value = item.ExtendedAmount + item.QI_Tariff_Amount.Value
        item["QI_RegionalMargin"].Value = item.ExtendedAmount - item.QI_TOTAL_EXTENDED_COST.Value
        item.QI_ExtendedWTWCost.Value = float(item['QI_UnitWTWCost'].Value)*item.Quantity
        item["QI_WTWMargin"].Value = item.ExtendedAmount - item["QI_ExtendedWTWCost"].Value
        if item.ExtendedAmount != 0:
            item["QI_RegionalMarginPercent"].Value = (item.QI_RegionalMargin.Value/item.ExtendedAmount) * 100
            item["QI_WTWMarginPercent"].Value = (item["QI_WTWMargin"].Value / item.ExtendedAmount) * 100