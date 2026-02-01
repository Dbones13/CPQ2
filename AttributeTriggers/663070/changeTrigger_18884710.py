if Quote.GetCustomField('R2QFlag').Content != 'Yes':
	Product.Attr('Calculation Button Trigger').AssignValue('Yes')