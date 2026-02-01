def changeStatus(Quote):
	Quote.ChangeQuoteStatus('Preparing')

def BackToPreparing(Quote):
	status = Quote.OrderStatus.Name
	if status == "Awaiting Approval":
		newCurrency = Quote.GetCustomField("CF_NewCurrency").Content
		currency = Quote.GetCustomField("Currency").Content
		if newCurrency and newCurrency != currency:
			changeStatus(Quote)
	elif status == "Ready for Approval":
		changeStatus(Quote)
	ScriptExecutor.Execute('CPQ_SF_CreateUpdateOpportunity')