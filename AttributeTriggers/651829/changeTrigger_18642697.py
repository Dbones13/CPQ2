gesloc =Product.Attr('MSID_GES_Location').GetValue()
if gesloc:
	Product.Attr("Experion_HS_Ges_Location_Labour").SelectDisplayValue(str(gesloc))