Session["calculate"] = "yes"
def outer_function():
	ParentProduct = TagParserProduct.ParseString('<*CTX( Product.RootProduct.PartNumber )*>')
	return ParentProduct
if Param.name == 'Honeywell Enterprise Data Management':
	Session["calculate"] = "yes"
	#val = Product.Attr('HCI_PHD_Scope').GetValue()
	#Product.Attr('HCI_PHD_Scope').SelectDisplayValue('Expansion')
	#Product.Attr('HCI_PHD_Scope').SelectDisplayValue(val)
	ApiResponse = ApiResponseFactory.JsonResponse(outer_function())
elif Param.name in ['HCI Labor Config','PHD Labor','Uniformance Insight Labor']:
	ApiResponse = ApiResponseFactory.JsonResponse(outer_function())