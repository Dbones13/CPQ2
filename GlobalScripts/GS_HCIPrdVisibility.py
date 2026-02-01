selectedPrdScope = Product.Attr('AR_HCI_SCOPE').GetValue()
showPrdList = ''
if selectedPrdScope and Product.GetContainerByName('AR_HCI_SUBPRD').Rows.Count == 0:
	if selectedPrdScope == 'Software + Labor':
		if Product.Attr('AR_HCI_GES Location').GetValue()!='':
			showPrdList = ['Honeywell Enterprise Data Management']
	else:
		showPrdList = ['Honeywell Enterprise Data Management']

Trace.Write(str(showPrdList))
ApiResponse = ApiResponseFactory.JsonResponse(showPrdList)