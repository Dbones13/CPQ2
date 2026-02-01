for item in Quote.MainItems:
	if Quote.GetCustomField('ChangeLaborCurrency').Content == 'True':
		if item.PartNumber == 'Migration':
			product = item.EditConfiguration()
			ScriptExecutor.Execute('GS_PopulatePartNumberContainer', {'Product': Product})
			ScriptExecutor.Execute('GS_PopulateGESCost', {'Product': Product})
			product.UpdateQuote()