cabinet_percent = Product.Attr('SerC_RG_Percentage_SSM_Cabinet (0-100%)').GetValue()
if cabinet_percent:
	Product.Attr('SeriesC_RG_Percentage').AssignValue(cabinet_percent)