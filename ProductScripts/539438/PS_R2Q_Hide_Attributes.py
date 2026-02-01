if Quote.GetCustomField("isR2QRequest").Content =='Yes':
	Product.Attr('R2QRequest').AssignValue('Yes')
	Product.Attr("R2Q_QuoteNumber").AssignValue(str(Quote.CompositeNumber))