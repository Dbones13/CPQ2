def hideAttr(attrList):
	for attr in attrList:
		Product.Attr(attr).Access = AttributeAccess.Hidden

nonR2QAttr = ["Header_02_open","C300_GES_Location"]

Product.Attr('R2QRequest').AssignValue('Yes')
Product.Attr("R2Q_QuoteNumber").AssignValue(str(Quote.CompositeNumber))
#Product.Attr('C300_GES_Location').SelectDisplayValue(Product.Attr('MSID_GES_Location').GetValue())
hideAttr(nonR2QAttr)