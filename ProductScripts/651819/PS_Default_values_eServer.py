Product.Attr('R2QRequest').AssignValue('Yes')
Product.Attr("R2Q_QuoteNumber").AssignValue(str(Quote.CompositeNumber))
loc_dict = {"IN":"GES India","CN":"GES China","RO":"GES Romania","UZ":"GES Uzbekistan","None":"None","null":"None"}
if Session["curr_ges_loc"]:
	ges_location = loc_dict.get(Session["curr_ges_loc"])
	Product.Attr('C300_GES_Location').SelectDisplayValue(ges_location)
	#Trace.Write("geslocation"+str(Product.Attr('C300_GES_Location').GetValue())+"session"+str(Session["curr_ges_loc"])+"ges_location"+str(ges_location))
else:
	Product.Attr('C300_GES_Location').SelectDisplayValue('None')
#Session["curr_ges_loc"] = ""