def setCost(item,wtwcostfactor_dict):
    if item and item.AsMainItem and item.AsMainItem.VCItemPricingPayload and item.AsMainItem.VCItemPricingPayload.Subtotals:
        for subtotals in item.AsMainItem.VCItemPricingPayload.Subtotals:
            if subtotals.Flag=='B':
                cost=float(subtotals.Value) if subtotals.Value else 0
                item.Cost = cost
                wtwCost= cost / (1 + float(wtwcostfactor_dict.get(item.PartNumber,wtwcostfactor_dict.get(item['QI_PLSG'].Value,0)))) if cost else 0.0
                item['QI_UnitWTWCost'].Value=wtwCost
                item['QI_ExtendedWTWCost'].Value=wtwCost*item.Quantity