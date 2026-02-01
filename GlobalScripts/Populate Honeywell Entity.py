if Quote.GetCustomField('Honeywell Entity Name').Content == '':
	bookingCountry = Quote.GetCustomField("Booking Country").Content
	query = "select Entity_Name,Default_Entity from Country_Entity_Mapping where Country='{}'".format(bookingCountry)
	res = SqlHelper.GetList(query)
	if res:
		Quote.CustomFields.SelectValueByValueCode("Honeywell Entity Name" , res[0].Default_Entity)
		Quote.CustomFields.DisallowAllValuesExceptByValueCodes("Honeywell Entity Name" , Array[type('str')]([r.Entity_Name for r in res]))