if Quote.GetCustomField('Quote Type').Content in ('Contract New','Contract Renewal'):
    qCurrency = Quote.GetCustomField('SC_CF_CURRENCY').Content if Quote.GetCustomField('SC_CF_PRICE_TOGGLE').Content != 'USD' else 'USD'
    qSign = Quote.SelectedMarket.CurrencySign if Quote.GetCustomField('SC_CF_PRICE_TOGGLE').Content != 'USD' else '$'
    exRate = float(Quote.GetCustomField('SC_CF_EXCHANGE_RATE').Content)
    
    #Jagruti - 22/05/2024 - Assigned value zero when product is not added
    Quote.GetCustomField('Honeywell List Price').Content = '0'
    Quote.GetCustomField('Honeywell List Price(USD)').Content = '0'
    Quote.GetCustomField('Total Sell Price(CW)').Content = '0'
    Quote.GetCustomField('Total Sell Price(USD)').Content = '0'
    Quote.GetCustomField('Total Discount Percent(CW)').Content = '0'
    Quote.GetCustomField("SC_CF_IS_STATUS_CHECK").Content = '0'

    for item in Quote.Items:
        if item.PartNumber == 'Service Contract':
            #Quote.GetCustomField('Honeywell List Price').Content = str(round(item.ExtendedListPrice,2))
            #Quote.GetCustomField('Honeywell List Price(USD)').Content = 'USD ' + str(round(item.ExtendedListPrice/exRate,2))
            #Quote.GetCustomField('Total Sell Price(USD)').Content = 'USD ' + str(round(item.ExtendedAmount/exRate,2))
            #Quote.GetCustomField('Total Sell Price(CW)').Content = str(round(item.ExtendedAmount,2))
            
            Quote.GetCustomField('Honeywell List Price').Content = Quote.GetCustomField('SC_CF_CURRENCY').Content +' '+ UserPersonalizationHelper.ToUserFormat(round(item.ExtendedListPrice,2))
            Quote.GetCustomField('Honeywell List Price(USD)').Content = "USD"+' '+UserPersonalizationHelper.ToUserFormat(float(item.ExtendedListPrice/exRate))
            Quote.GetCustomField('Total Sell Price(CW)').Content = Quote.GetCustomField('SC_CF_CURRENCY').Content + '  ' +UserPersonalizationHelper.ToUserFormat(float(item.ExtendedAmount))
            Quote.GetCustomField('Total Sell Price(USD)').Content = "USD"+' '+UserPersonalizationHelper.ToUserFormat(float(item.ExtendedAmount/exRate))
            Quote.GetCustomField('Total Discount Percent(CW)').Content = UserPersonalizationHelper.ToUserFormat(float(item.QI_SC_Total_Discount_Percent.Value))

        #item.QI_SC_ListPrice.Value = qCurrency + ' ' +  '{0:.2f}'.format(round(item.ExtendedListPrice/exRate,2) if qCurrency == '$' else round(item.ExtendedListPrice,2))
        #item.QI_SC_SellPrice.Value = qCurrency + ' ' +  '{0:.2f}'.format(round(item.ExtendedAmount/exRate,2) if qCurrency == '$' else round(item.ExtendedAmount,2))
        #item.QI_SC_CostPrice.Value = qCurrency + ' ' +  '{0:.2f}'.format(round(item.QI_SC_Cost.Value/exRate,2) if qCurrency == '$' else round(item.QI_SC_Cost.Value,2))
        #item.QI_SC_WTWCost.Value = qCurrency + ' ' +  '{0:.2f}'.format(round(item.QI_ExtendedWTWCost.Value/exRate,2) if qCurrency == '$' else round(item.QI_ExtendedWTWCost.Value,2))
        #item.QI_SC_Target_Sell_Price.Value = (item.ExtendedListPrice + item.QI_MPA_Discount_Amount.Value)/exRate
        #item.QI_SC_Scope_Change.Value = ((item.QI_SC_ScopeAdditionPrice.Value * (item.ExtendedAmount/item.ListPrice)) if item.ListPrice > 0 else 0) + ((item.QI_SC_ScopeReductionPrice.Value * (item.QI_SC_Previous_Year_Sell_Price.Value/item.QI_SC_Previous_Year_List_Price.Value)) if item.QI_SC_Previous_Year_List_Price.Value > 0 else 0)
        #item.QI_SC_Price_Impact.Value = item.ExtendedAmount - (item.QI_SC_Scope_Change.Value + item.QI_SC_Previous_Year_Sell_Price.Value)
        #item.QI_SC_Scope_Impact.Value = qCurrency + ' ' +  '{0:.2f}'.format(round((item.ExtendedAmount - (item.QI_SC_Scope_Change.Value + item.QI_SC_Previous_Year_Sell_Price.Value))/exRate,2) if qCurrency == 'USD' else round((item.ExtendedAmount - (item.QI_SC_Scope_Change.Value + item.QI_SC_Previous_Year_Sell_Price.Value)),2))

        list_price = UserPersonalizationHelper.ToUserFormat(round(item.ExtendedListPrice/exRate,2)) if qCurrency == 'USD' else UserPersonalizationHelper.ToUserFormat(round(item.ExtendedListPrice,2))
        sell_price = UserPersonalizationHelper.ToUserFormat(round(item.ExtendedAmount/exRate,2)) if qCurrency == 'USD' else UserPersonalizationHelper.ToUserFormat(round(item.ExtendedAmount,2))
        cost_price = UserPersonalizationHelper.ToUserFormat(round(item.QI_SC_Cost.Value/exRate,2)) if qCurrency == 'USD' else UserPersonalizationHelper.ToUserFormat(round(item.QI_SC_Cost.Value,2))
        wtw_price = UserPersonalizationHelper.ToUserFormat(round(item.QI_ExtendedWTWCost.Value/exRate,2)) if qCurrency == 'USD' else UserPersonalizationHelper.ToUserFormat(round(item.QI_ExtendedWTWCost.Value,2))

        item.QI_SC_ListPrice.Value = qSign + ' ' +  list_price
        item.QI_SC_SellPrice.Value = qSign + ' ' +  sell_price
        item.QI_SC_CostPrice.Value = qSign + ' ' +  cost_price
        item.QI_SC_WTWCost.Value = qSign + ' ' +  wtw_price
        item.QI_SC_Target_Sell_Price.Value = item.ExtendedListPrice - item.QI_MPA_Discount_Amount.Value

        if Quote.GetCustomField('Quote Type').Content in ('Contract New'):
            item.QI_SC_Scope_Impact.Value = item.QI_SC_SellPrice.Value

        if item.PartNumber == 'Parts Management':
            Quote.GetCustomField("SC_CF_IS_STATUS_CHECK").Content = '1'

    #Quote.Save(False)