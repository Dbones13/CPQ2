if Quote.GetCustomField('isR2QRequest').Content == 'Yes':
	Product.Attr('R2QRequest').AssignValue('Yes')
else:
	Product.Attr('R2QRequest').AssignValue('')