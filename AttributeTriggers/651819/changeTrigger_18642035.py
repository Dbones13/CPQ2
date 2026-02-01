gesloc =Product.Attr('MSID_GES_Location').GetValue()
if gesloc:
	Product.Attr("C300_GES_Location").SelectDisplayValue(str(gesloc))