tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]

def getExecutionCountry():
    marketCode = Quote.SelectedMarket.MarketCode
    salesOrg = marketCode.partition('_')[0]
    currency = marketCode.partition('_')[2]
    query = SqlHelper.GetFirst("select Execution_County from NEW_EXECUTION_COUNTRY_SALES_ORG_MAPPING where Sales_Area = '{}' and Currency = '{}'".format(salesOrg,currency))
    if query is not None:
        return query.Execution_County
    else:
        return ''

if 'Labor Deliverables' in tabs and Quote:
    executionCountry = getExecutionCountry()
    #Trace.Write("executionCountry:{}".format(executionCountry))
    if executionCountry != '':
        if not Product.Attr("Hardware_Engineering_Execution_Country").GetValue():
            Product.Attr("Hardware_Engineering_Execution_Country").SelectDisplayValue(executionCountry, True)