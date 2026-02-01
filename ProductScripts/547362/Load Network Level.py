if Quote.GetCustomField('IsR2QRequest').Content:
	Product.Attr("R2QRequest").AssignValue("Yes")
	Product.Attr("R2Q_QuoteNumber").AssignValue(str(Quote.CompositeNumber))
	Product.DisallowAttr('Calculation_Button')

network_level = Product.GetContainerByName('Network Level Container')
newRow = network_level.AddNewRow()
newRow['Network Level'] = 'L3.0 Network'
newRow = network_level.AddNewRow()
newRow['Network Level'] = 'L3.5 Network'