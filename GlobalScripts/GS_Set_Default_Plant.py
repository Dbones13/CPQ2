def Set_Default_Plant(Quote):
	bookingLOB = Quote.GetCustomField("Booking LOB").Content
	quoteType = Quote.GetCustomField('Quote Type').Content
	cfPlant = Quote.GetCustomField('CF_Plant')
	salesOrg = Quote.GetCustomField("Sales Area").Content
	bookingCountry = Quote.GetCustomField("Booking Country").Content
	pn = SqlHelper.GetFirst("Select PLANT_NAME from COUNTRY_SORG_PLANT_MAPPING(NOLOCK) where PLANT_CODE = '6649' ORDER BY CpqTableEntryId DESC")

	# CXCPQ-67442: CF_PLANT should be visible only for PMC Parts & Spot
	if bookingLOB == "PMC" and quoteType == 'Parts and Spot':
		cfPlant.Visible = True
		# CXCPQ-59003: Populate default plant code based on SalesOrg and Booking country
		if not cfPlant:
			query = ("SELECT DISTINCT CSPM.PLANT_NAME PLANT_NAME FROM COUNTRY_SORG_PLANT_MAPPING CSPM, V_COUNTRY CA WHERE CSPM.SALES_ORG_CODE='{}' AND CSPM.COUNTRY_CODE=CA.COUNTRY_ABREV2 AND CA.COUNTRY_NAME='{}'".format(salesOrg, bookingCountry))
			res = SqlHelper.GetList(query)
			if res and len(res) > 0:
				Quote.GetCustomField('CF_Plant').Content=res[0].PLANT_NAME

	elif bookingLOB=="HCP" and pn:
		cfPlant.Visible = False
		Quote.GetCustomField('CF_Plant').Content=str(pn.PLANT_NAME)

	else: #added logic for Service contracts CXCPQ-92041 and CXCPQ-88100
		if bookingLOB == "LSS" and (quoteType in ('Contract Renewal','Contract New')) and salesOrg=="736P" and bookingCountry=="India" and Quote.OrderStatus.Name in ("Accepted by Customer","GCC Handover","ERP Contract Created","Booked"):# display
			cfPlant.Visible = True
			if not cfPlant.Content:
				Quote.GetCustomField('CF_Plant').Content=SqlHelper.GetFirst("select * from sc_hardcode_values where name = 'SC_India_Default_Plant'").Value #Default to plant code 7766
		else:
			cfPlant.Visible = False
#Set_Default_Plant(Quote)