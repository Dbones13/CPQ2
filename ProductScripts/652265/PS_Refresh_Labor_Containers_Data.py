from GS_Winest_Labor_Price_Cost import updateLaborCostPrice
if Quote:
	conList = ['Winest Labor Container', 'Winest Additional Labor Container']
	updateLaborCostPrice(Product, Quote, TagParserQuote, conList, Session=dict())