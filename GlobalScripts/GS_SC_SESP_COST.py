def BurdenRateCostValue(Quote):
    quoteCurrency = Quote.SelectedMarket.CurrencyCode
    Country           = Quote.GetCustomField('Opportunity Tab Booking Country').Content
    query             = SqlHelper.GetFirst("select Currency,Burden_Rate from CT_SC_LABOR_RESOURCETYPE where PartNumber='SVC-EST2-FD' and Country='{}'".format(Country))
    currencyCode = query.Currency
    if quoteCurrency != currencyCode:
        if quoteCurrency == "USD":
            extRateValue_query = SqlHelper.GetFirst("SELECT Exchange_Rate FROM Currency_ExchangeRate_Mapping WHERE From_Currency = '{}' AND To_Currency = '{}' ".format(str(currencyCode),str(Quote.GetCustomField('SC_CF_CURRENCY').Content))).Exchange_Rate
            extRateValue = extRateValue_query if extRateValue_query else 1
            burdenRatePerHour = float(query.Burden_Rate)/8
            conversionrate = burdenRatePerHour * float(extRateValue)
            return conversionrate
        else:
            extRateValue_query_USD = SqlHelper.GetFirst("SELECT Exchange_Rate FROM Currency_ExchangeRate_Mapping WHERE From_Currency = '{}' AND To_Currency = '{}' ".format(str(currencyCode),"USD")).Exchange_Rate
            extRateValue_USD = extRateValue_query_USD if extRateValue_query_USD else 1
            burdenRatePerHour_local = float(query.Burden_Rate)/8
            conversionrate_local = burdenRatePerHour_local * float(extRateValue_USD)
            extRateValue_query = SqlHelper.GetFirst("SELECT Exchange_Rate FROM Currency_ExchangeRate_Mapping WHERE From_Currency = '{}' AND To_Currency = '{}' ".format("USD",str(Quote.GetCustomField('SC_CF_CURRENCY').Content))).Exchange_Rate
            extRateValue = extRateValue_query if extRateValue_query else 1
            conversionrate = conversionrate_local*float(extRateValue)
            return conversionrate
    else:
        extRateValue = 1
        burdenRatePerHour = float(query.Burden_Rate)/8  
        conversionrate = burdenRatePerHour * float(extRateValue)
        return conversionrate