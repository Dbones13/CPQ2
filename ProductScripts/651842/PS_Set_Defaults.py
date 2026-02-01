Product.Attr('R2QRequest').AssignValue('Yes')
Product.Attr("R2Q_QuoteNumber").AssignValue(str(Quote.CompositeNumber))
loc_dict = {"IN":"GES India","CN":"GES China","RO":"GES Romania","UZ":"GES Uzbekistan","None":"None","null":"None"}
gesloc = Quote.GetGlobal('ExGesLocation')
if gesloc is not None and gesloc != "":
	ges_location = loc_dict.get(gesloc)
	Product.Attr('SCADA_Ges_Location_Labour').SelectDisplayValue(ges_location)
	#Trace.Write("scadageslocation"+str(Product.Attr('SCADA_Ges_Location_Labour').GetValue()))
else:
	Product.Attr('SCADA_Ges_Location_Labour').SelectDisplayValue('None')
	#Trace.Write("scadageslocationnone"+str(Product.Attr('SCADA_Ges_Location_Labour').GetValue()))
container = Product.GetContainerByName('Scada_CCR_Unit_Cont')
if container.Rows.Count > 0:
	setDefault = True
	container.AddNewRow('R2Q_CCR_cpq',False)