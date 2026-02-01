def fnQuoteExpiry():
	expiryDate = Quote.GetCustomField('Quote Expiration Date').Content
	sts_change = False
	if expiryDate:
		expiryDate = UserPersonalizationHelper.CovertToDate(expiryDate)
		if Quote.OrderStatus.Name == 'Submitted to Customer':
			if expiryDate > DateTime.Now:
				Quote.ChangeQuoteStatus('Submitted to Customer')
				sts_change = True
			else:
				Quote.ChangeQuoteStatus('Expired')
				sts_change = True
		else:
			if expiryDate < DateTime.Now:
				Quote.ChangeQuoteStatus('Expired')
				sts_change = True
		if sts_change:
			ScriptExecutor.Execute('CPQ_SF_CreateUpdateOpportunity')

quote_type = Quote.GetCustomField('Quote Type').Content
qt_status = Quote.OrderStatus.Name
if quote_type == 'Parts and Spot' and qt_status == 'Submitted to Customer':
	fnQuoteExpiry()
elif quote_type not in ('Parts and Spot', 'Projects'):
	fnQuoteExpiry()