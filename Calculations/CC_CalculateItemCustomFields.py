def filterRecord(Part_number=None, MRP_indicator=None, FixedVender=None, records=None):
	if records is None:
		return []
	if Part_number is not None:
		return [i for i in records if i.Material == Part_number]
	if MRP_indicator is not None:
		return [i for i in records if i.MRP_Indicator == MRP_indicator]
	if FixedVender is not None:
		return [i for i in records if i.Fixed_vendor == FixedVender]
	return []

if Session["prevent_execution"] != "true":
	salesArea = Quote.GetCustomField('Sales Area').Content
	publishedLeadTime = 0
	quoteRepriceDate = Quote.GetCustomField('Quote Reprice Date').Content
	try:
		convertedQuoteRepriceDate = UserPersonalizationHelper.CovertToDate(quoteRepriceDate)
	except Exception as e:
		convertedQuoteRepriceDate = None
		Trace.Write("Error while converting reprice date: " + str(e))

	totalExpedite = 0.0
	exchangeRate = float(Quote.GetCustomField('Exchange Rate').Content.strip() or '1.0')
	factoryData = Quote.GetCustomField("CF_Factory_Data_Applicable").Content
	quote_expiry_date = str(Quote.EffectiveDate.Date).split(' ')[0]

	# Caching transit times to avoid repeated database calls
	transitTimeQuery = "Select SALES_ORG, TRANSIT_TIME from TRANSIT_TIME where SALES_ORG = '{0}'".format(salesArea)
	transitTimes = {row.SALES_ORG: row.TRANSIT_TIME for row in SqlHelper.GetList(transitTimeQuery)}
	transitTime = transitTimes.get(salesArea, 0)

	# Caching service days to avoid repeated database calls
	serviceDaysQuery = "Select MATERIAL, SERVICE_DAYS from LEAD_TIME where SALES_ORG = '{0}'".format(salesArea)
	serviceDays = {row.MATERIAL: row.SERVICE_DAYS for row in SqlHelper.GetList(serviceDaysQuery)}

	for item in Quote.Items:
		transitTime, serviceDaysForItem = 0, 0
		serviceDaysForItem = serviceDays.get(item.PartNumber, 0)
		leadTime = int(serviceDaysForItem) + int(transitTime)
		item['QI_LeadTime'].Value = leadTime
		if leadTime > publishedLeadTime:
			publishedLeadTime = leadTime
		if convertedQuoteRepriceDate:
			deliveryDate = convertedQuoteRepriceDate.AddDays(leadTime)
			item['QI_LT_Delivery_Date'].Value = deliveryDate
		isValid = (item['QI_Customer_Requested_Date'].Value and 
				item['QI_LT_Delivery_Date'].Value and 
				DateTime.Compare(item['QI_LT_Delivery_Date'].Value, item['QI_Customer_Requested_Date'].Value) > 0)
		if (item['QI_Expedite_Reason'].Value and 
			isValid and 
			Quote.GetCustomField("Expedite Fee Waiver").Content != 'True' and 
			not Quote.GetCustomField("Expedite Fee Waiver Reason").Content):
			unitSellPrice = float(item.NetPrice) / exchangeRate
			expedite_fee = 0
			value = 0.1 * unitSellPrice
			if value < 500:
				expedite_fee = 500 * exchangeRate * item.Quantity
			else:
				expedite_fee = value * item.Quantity
			item['QI_Expedite_Fees'].Value = round(expedite_fee, 2)
		else:
			item['QI_Expedite_Fees'].Value = 0
		totalExpedite += item['QI_Expedite_Fees'].Value

		'''if factoryData == "Y":
			query = ("Select * from CT_VENDOR_INFORMATION WHERE Valid_from <= '{}' and Valid_to >= '{}' and Material = '{}'"
					.format(quote_expiry_date, quote_expiry_date, item.PartNumber))
			result = SqlHelper.GetList(query)
			if item.AsMainItem and len(list(item.AsMainItem.Children)) == 0 and result:
				if len(result) > 1:
					result2 = filterRecord(FixedVender='X', records=result)
					if result2:
						selected_record = result2[0]
					else:
						result3 = filterRecord(MRP_indicator='1', records=result)
						if result3:
							selected_record = result3[0]
						else:
							selected_record = result[0]
				else:
					selected_record = result[0]
				item.QI_FactoryCode.Value = selected_record.Vendor
				item.QI_FactoryName.Value = selected_record.Vendor_Name
			else:
				item.QI_FactoryCode.Value = ""
				item.QI_FactoryName.Value = ""

	Quote.GetCustomField('Published Lead Time').Content = str(publishedLeadTime)
	Quote.GetCustomField('Expedite Fee').Content = str(totalExpedite)'''