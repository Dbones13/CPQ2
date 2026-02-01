if Session["prevent_execution"] != "true" and (Quote.GetCustomField('CF_Plant_Prevent_Calc').Content != 'true' or Quote.GetCustomField('Booking LOB').Content != 'PMC'):
	import GS_CalculateTotals as ct

	total = ct.calculateTotalListPrice(Quote)
	Quote.GetCustomField('Total List Price').Content=str(total)