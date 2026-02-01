if Quote.GetCustomField("isR2QRequest").Content == 'Yes':
	Product.ParseString('<* ExecuteScript(PS_SetReadOnlyAccess) *>')
	Product.Attr('Calculation_Button').Allowed = False
else:
	Product.Attr('Calculation_Button').Allowed = True