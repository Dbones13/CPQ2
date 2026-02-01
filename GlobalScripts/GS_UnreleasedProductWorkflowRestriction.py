if Session["prevent_execution"] != "true":
	def getCFValue(field):
		return Quote.GetCustomField(field).Content

	quoteType = getCFValue('Quote Type')
	get_RAFR1 = getCFValue('EGAP_RAFR1_Ques')
	validParts= []
	Quote.GetCustomField("RQUP_partList").Content = ''

	validParts = set([item.PartNumber for item in Quote.Items if item["QI_CrossDistributionStatus"].Value == '05 PreRelease'])

	if validParts:
		Quote.GetCustomField("RQUP_partList").Content = str(', '.join(validParts))

	invaildParts =Quote.GetCustomField("RQUP_partList").Content
	if invaildParts:
		if quoteType == 'Projects' and get_RAFR1 == 'No':
			if not Quote.Messages.Contains(Translation.Get('message.UnreleasedProductRestriction').format(invaildParts)):
				Quote.Messages.Add(Translation.Get('message.UnreleasedProductRestriction').format(invaildParts))
		elif  quoteType != 'Projects':
			if not Quote.Messages.Contains(Translation.Get('message.UnreleasedProduct').format(invaildParts)):
				Quote.Messages.Add(Translation.Get('message.UnreleasedProduct').format(invaildParts))