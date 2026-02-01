def assignLeadTime(Quote):
	quoteRepriceDate = Quote.GetCustomField('Quote Reprice Date').Content
	convertedQuoteRepriceDate =UserPersonalizationHelper.CovertToDate(quoteRepriceDate)
	salesArea = Quote.GetCustomField('Sales Area').Content
	transit_query = SqlHelper.GetFirst("Select TRANSIT_TIME from TRANSIT_TIME(nolock) where SALES_ORG = '{0}'".format(salesArea))
	if transit_query:
		transitTime = transit_query.TRANSIT_TIME
	else:
		transitTime = 0
	for item in Quote.Items:
		transitTime,serviceDays = 0, 0
		query = SqlHelper.GetFirst("Select SERVICE_DAYS from LEAD_TIME(nolock) where SALES_ORG = '{0}' and MATERIAL = '{1}'".format(salesArea, item.PartNumber))
		if query:
			serviceDays = query.SERVICE_DAYS
			if serviceDays:
				totalDays = int(serviceDays) + int(transitTime)
				item['QI_LeadTime'].Value = totalDays
		else:
			item['QI_LeadTime'].Value = 0
		leadTime =item['QI_LeadTime'].Value
		deliveryDate = convertedQuoteRepriceDate.AddDays(leadTime)
		item['QI_LT_Delivery_Date'].Value = deliveryDate
assignLeadTime(Quote)
