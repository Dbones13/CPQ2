def getCFValue(quote , field):
	return quote.GetCustomField(field).Content

def setCFValue(quote, CF_Name, CF_Value):
	quote.GetCustomField(CF_Name).Content = CF_Value

def getMarketInfo(quote, currency):
	entitlement = getCFValue(quote , "Entitlement")
	salesArea = getCFValue(quote ,"Sales Area")
 	lob = getCFValue(quote ,"Quote Tab Booking LOB")
 	typ = 'List' if getCFValue(quote ,"Quote Type") in 'Parts and Spot' else 'Systems'
 	if (salesArea in ('333P') and currency in ('EUR')) or salesArea in ('2504','2386'):
 		marketCode = '{}{}'.format(salesArea , currency)
	elif (salesArea in ('583P') and currency in ('NOK')):
 		marketCode = '{}{}'.format(salesArea , currency)
 	elif lob in ("CCC") and salesArea in ('827P','482P','728P','1020'):
 		marketCode = '{}{}'.format(salesArea , currency)
 	elif salesArea == '1109' and currency == 'USD':
 		marketCode = '{}{}'.format(salesArea , currency)
 	else:
		marketCode = '{}_{}'.format(salesArea , currency)
 	'''QueryMarket=SqlHelper.GetFirst("select market_code from market_defn where market_code in('{}_{}','{}{}','{} {}')".format(salesArea,currency,salesArea,currency,salesArea,currency))
 	if QueryMarket:
		marketCode = QueryMarket.market_code''' #Commented to enable market code previous selection. Need to work with Suriya on this.
         
 	return marketCode, entitlement, typ

def setMarket(quote, marketCode):
	if quote.SelectedMarket.MarketCode != marketCode:
		quote.SetMarket(marketCode)

def getPriceBookId(marketCode, entitlement, typ):
	query  = "select Id from PriceBookTableDefn pd join market_defn md on pd.MarketId = md.market_id where market_code = '{}'".format(marketCode)
	if entitlement:
		query += " and name like '%{} {}'".format('Flex' if 'Flex' in entitlement else 'Plus',typ)
	else:
		query += " and name like '%{}%' and Level = 1".format(typ)
	res = SqlHelper.GetFirst(query)
	return res.Id if res else 0


def setPriceBookId(quote, newPricebookId):
	if quote.PricebookId != newPricebookId:
		quote.PricebookId = newPricebookId
	#quote.Save(False)

currency = getCFValue(Quote ,"Currency")
if not currency:
	currency = getCFValue(Quote ,"CF_NewCurrency")
	setCFValue(Quote, "Currency", currency)
marketCode, entitlement, typ = getMarketInfo(Quote, currency)
setMarket(Quote, marketCode)
newPricebookId = getPriceBookId(marketCode, entitlement, typ)
setPriceBookId(Quote, newPricebookId)
#Quote.RefreshActions()