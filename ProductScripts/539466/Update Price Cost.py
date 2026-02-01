price = Product.Attr("Price")
cost = Product.Attr("cost")
QuoteType= Quote.GetCustomField("Quote Type").Content
usdPrice = Product.Attr("USD Price").GetValue()
usdPrice = float(usdPrice) if usdPrice else 0

usdCost = Product.Attr("USD cost").GetValue()
usdCost = float(usdCost) if usdCost else 0

exchangeRate = Quote.GetCustomField("Exchange Rate").Content
exchangeRate = float(exchangeRate) if exchangeRate else 1
if (Quote.GetCustomField("CF_NewCurrency").Content !='' and Quote.GetCustomField("CF_NewCurrency").Content != Quote.GetCustomField("Currency").Content) and QuoteType=="Projects":
    price.AssignValue(str(round(usdPrice * exchangeRate, 2)))
    cost.AssignValue(str(round(usdCost * exchangeRate, 2)))
else:
    if price.GetValue() and cost.GetValue():
        price.AssignValue(str(round(float(price.GetValue()), 2)))
        cost.AssignValue(str(round(float(cost.GetValue()), 2)))