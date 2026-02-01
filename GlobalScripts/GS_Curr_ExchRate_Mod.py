#CXCPQ-59003: Added exchange rates conversion module
def getFloat(val):
	if val:
		try:
			return float(val)
		except:
			return 0
	return 0

def fn_get_curr_exchrate(p_from_curr,p_to_curr):
    if p_from_curr=='USD' or p_to_curr=='USD': 
        # If either of the currency is USD
        query = SqlHelper.GetFirst("select Exchange_Rate from Currency_ExchangeRate_Mapping where From_Currency = '{}' and To_Currency = '{}'".format(p_from_curr,p_to_curr))
        if query is not None:
            return getFloat(query.Exchange_Rate)
        else:
            return 0 #Exchange rate not defined for p_from_curr - p_to_curr currency pair.
    else:
        #Cross Currency Conversions: p_from_curr--> USD_rate and USD_rate-->p_to_curr
        query1 = SqlHelper.GetFirst("select Exchange_Rate from Currency_ExchangeRate_Mapping where From_Currency = '{}' and To_Currency = '{}'".format(p_from_curr,'USD'))
        query2 = SqlHelper.GetFirst("select Exchange_Rate from Currency_ExchangeRate_Mapping where From_Currency = '{}' and To_Currency = '{}'".format('USD',p_to_curr))
        if query1 is not None and query2 is not None:
            return getFloat(query1.Exchange_Rate) * getFloat(query2.Exchange_Rate)
        else:
            return 0 #currency rate is not defined for p_from_curr-USD or USD-p_to_curr pair