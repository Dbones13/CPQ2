#CXCPQ-44061 Below function used to display ETO or Yspec table on product configurator. This script is called from header template. When a new Gas/Marine product is created, add the product to PMC_GASETO_YSPEC_MARINE_PRODUCTS table.
#CXCPQ-98038 Start
if Product.Attr("Special Options?").SelectedValue.ValueCode == 'N':
	Quote.SetGlobal('G_ETO_json_Data','{"ETOSPEC":[]}')
	Quote.SetGlobal('G_ETO_Row_CNT','0')
#CXCPQ-98038 End
query = "select PartNumber,family_code from PMC_GASETO_YSPEC_MARINE_PRODUCTS where PartNumber = '{}'".format(Product.PartNumber)
result = SqlHelper.GetFirst(query)
if  result is not None:
    #CXCPQ-52824: 06/15/2023: Added Elster Product condition
	if (result.family_code=='Gas Products' or result.family_code=='Instrumentation' or result.family_code=='Field Instruments' or result.family_code=='Elster Product'):
		#Returns true when partnumber belongs to either Gas/ Marine Instrumentation/Field Instruments/ Elster family
		ret=['True',result.family_code]
	else:
		ret=['False','']
else:
	ret=['False','']
#Send the response to the API Called
ApiResponse = ApiResponseFactory.JsonResponse(ret)