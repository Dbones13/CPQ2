if Item.ProductSystemId == 'Write-In_Tariff_cpq':
    if Item.ExtendedAmount != 0:
        Item['QI_WTWMargin'].Value = (Item.ExtendedAmount - Item['QI_ExtendedWTWCost'].Value)
        Item['QI_RegionalMarginPercent'].Value = (Item.ExtendedAmount - Item.ExtendedCost)/Item.ExtendedAmount * 100
        Item['QI_RegionalMargin'].Value = (Item.ExtendedAmount - Item.ExtendedCost)
        Item['QI_WTWMarginPercent'].Value = (Item.ExtendedAmount - Item['QI_ExtendedWTWCost'].Value)/Item.ExtendedAmount * 100