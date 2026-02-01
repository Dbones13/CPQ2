printer_attrs = ['LaserJet Printer - Monochrome (0-99)','Colour A4 printer', 'B_W_A3_printer', 'Colour_A3_printer']
for attr in printer_attrs:
	if Product.Attr('Printer Required?').GetValue() == 'Yes':
		Product.AllowAttr(attr)
		Product.Attr(attr).AssignValue("0")
	else:
		Product.DisallowAttr(attr)