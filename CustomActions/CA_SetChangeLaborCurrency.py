parts = SqlHelper.GetFirst("SELECT CATALOGCODE from CART_ITEM where CART_ID = '"+str(Quote.QuoteId)+"' and USERID = '"+str(Quote.UserId)+"' and CATALOGCODE LIKE '%SVC-%'")
if parts:
	Quote.GetCustomField('ChangeLaborCurrency').Content = 'True'