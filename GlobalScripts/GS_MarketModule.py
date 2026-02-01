from GS_CommonModule import getCFValue,setCFValue

def getMarketInfo(quote, currency):
	entitlement = getCFValue(quote , "Entitlement")
	salesArea = getCFValue(quote ,"Sales Area")
	lob = getCFValue(quote ,"Quote Tab Booking LOB")
	type = 'List' if getCFValue(quote ,"Quote Type") in 'Parts and Spot' else 'Systems'
	marketCode=''
	'''if (salesArea in ('583P','333P') and currency in ('NOK','EUR')) or salesArea in ('2504','2386'):
		marketCode = '{}{}'.format(salesArea , currency)
	elif lob in ("CCC") and salesArea in ('827P','482P','728P','1020'):
		marketCode = '{} {}'.format(salesArea , currency)
	else:
		 marketCode = '{}_{}'.format(salesArea , currency)'''
	QueryMarket=SqlHelper.GetFirst("select market_code, market_id from market_defn md JOIN PriceBookTableDefn pd on md.market_id=pd.MarketId where market_code in('{}_{}','{}{}','{} {}')".format(salesArea,currency,salesArea,currency,salesArea,currency))
	if QueryMarket:
		 marketCode = QueryMarket.market_code
	return marketCode, entitlement, type

def setMarket(quote, marketCode):
	if quote.SelectedMarket.MarketCode != marketCode:
		quote.SetMarket(marketCode)

def getPriceBookId(marketCode, entitlement, type):
	query  = "select Id from PriceBookTableDefn pd join market_defn md on pd.MarketId = md.market_id where market_code = '{}'".format(marketCode)
	if entitlement:
		query += " and name like '%{} {}'".format('Flex' if 'Flex' in entitlement else 'Plus',type)
	else:
		query += " and name like '%{}%' and Level = 1".format(type)
	res = SqlHelper.GetFirst(query)
	return res.Id if res else 0


def setPriceBookId(quote, newPricebookId):
	if quote.PricebookId != newPricebookId:
		quote.PricebookId = newPricebookId

def marketinit(Quote):
	currency = getCFValue(Quote ,"CF_NewCurrency")
	if currency:
		setCFValue(Quote, "Currency", currency)
		marketCode, entitlement, type = getMarketInfo(Quote, currency)
		setMarket(Quote, marketCode)
		new_setpricebook(Quote)
        # newPricebookId = getPriceBookId(marketCode, entitlement, type)
		# setPriceBookId(Quote, newPricebookId)

def setExchangeRate(Quote):
	res = SqlHelper.GetFirst("SELECT Exchange_Rate FROM Currency_ExchangeRate_Mapping WHERE From_Currency = 'USD' AND To_Currency = '"+str(Quote.GetCustomField('Currency').Content)+"'")
	Quote.GetCustomField('Exchange Rate').Content = res.Exchange_Rate

def new_setpricebook(Quote):
	newPricebookId = getPriceBookId(Quote.SelectedMarket.MarketCode, getCFValue(Quote , "Entitlement"), 'List' if getCFValue(Quote ,"Quote Type") in 'Parts and Spot' else 'Systems')
	setPriceBookId(Quote, newPricebookId)