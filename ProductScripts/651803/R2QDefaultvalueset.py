if Quote.GetCustomField('IsR2QRequest').Content:
	Product.Attr("R2QRequest").AssignValue("Yes")
	Product.Attr("R2Q_QuoteNumber").AssignValue(str(Quote.CompositeNumber))
	Product.DisallowAttr('Calculation_Button')
	Product.Attr("Order_Status").AssignValue(str(Quote.OrderStatus.Name))