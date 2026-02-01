if (Product.Attr('R2QRequest').GetValue() == 'Yes' and Quote.GetCustomField("R2Q_Save").Content == "Submit") or Product.Attr('R2QRequest').GetValue() != 'Yes':
	import GS_LoadPartSummary
	GS_LoadPartSummary.main(Product)
	from GS_FinalizedActivities import PopulateFinalizedActivities
	PopulateFinalizedActivities(Product)
	Product.Attr('CyberChildFlag').AssignValue('True')
	Product.Attr('calculate_value_set').AssignValue('')