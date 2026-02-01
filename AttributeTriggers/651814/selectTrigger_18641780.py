if Quote.GetCustomField('IsR2QRequest').Content != 'Yes':
	Product.Attr("Calculation_Button").Access = AttributeAccess.ReadOnly