Product.Attr('R2QRequest').AssignValue('Yes')
Product.Attr("R2Q_QuoteNumber").AssignValue(str(Quote.CompositeNumber))
Product.Attr('C300_Implementation_Methodology').SelectDisplayValue('Standard Build Estimate')
Product.Attr('C300_Process_Type').SelectDisplayValue('None')
Product.Attr('Number_of_Peer_PCDI').AssignValue('0')
Product.Attr('Number_of_Peer_CDA').AssignValue('0')
Product.Attr('Number_of_SCADA_Node_Types_for_C300').AssignValue('0')
Product.Attr('Enter_total_count_of_Typicals/Prototypes (0-500)').AssignValue('0')
Product.Attr("Input_Quality (User Requirement Specification)").AssignValue("Function Plan available(One revision) 40 %")
Product.AllowAttr('No_of_Complex_SCMs_per_Unit (0-100)')
Product.Attr('No_of_Complex_SCMs_per_Unit (0-100)').AssignValue('1')
Product.AllowAttr('No_of_Complex_Operations_per_Product (0-100)')
Product.Attr('No_of_Complex_Operations_per_Product (0-100)').AssignValue('1')
#Product.AllowAttr('Percentage_for_Pre-FAT(0-100%)')
#Product.Attr('Percentage_for_Pre-FAT(0-100%)').AssignValue('100')
Product.Attr('C300_Marshalling_cabinet_count (0-500)').AssignValue('0')
Product.Attr('Number_of_Third_Party_Soft_IO_(Serial/SCADA)').AssignValue('0')
loc_dict = {"IN":"GES India","CN":"GES China","RO":"GES Romania","UZ":"GES Uzbekistan","None":"None","null":"None"}
gesloc = Quote.GetGlobal('ExGesLocation')
if gesloc is not None and gesloc != "":
	ges_location = loc_dict.get(gesloc)
	Product.Attr('C300_GES_Location').SelectDisplayValue(ges_location)
else:
	Product.Attr('C300_GES_Location').SelectDisplayValue('None')
#Session["curr_ges_loc"] = ""