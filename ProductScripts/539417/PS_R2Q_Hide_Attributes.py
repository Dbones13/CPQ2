isR2Qquote = True if Quote.GetCustomField("isR2QRequest").Content =='Yes' else False
if isR2Qquote:
	Product.Attr('R2QRequest').AssignValue('Yes')
	Product.Attr("R2Q_QuoteNumber").AssignValue(str(Quote.CompositeNumber))