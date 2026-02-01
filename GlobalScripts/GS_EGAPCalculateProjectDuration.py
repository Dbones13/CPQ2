if Session["prevent_execution"] != "true":
    #Nilesh- created module of the same script and called it here. dt 28102024-
	#from GS_EGAPCalculateProjectDuration_Module import CalculateProjectDuration
	#CalculateProjectDuration(TagParserQuote,Quote)
	
	import math
	from datetime import date

	def numOfDays(date1, date2):
		return (date2-date1).days

	#jagruti --added code for service contract--

	def parseDate(TagParserQuote, Quote, fieldName):
		if Quote.GetCustomField(fieldName).Content != "":
			y = UserPersonalizationHelper.CovertToDate(Quote.GetCustomField(fieldName).Content).Year # .Day
			m = UserPersonalizationHelper.CovertToDate(Quote.GetCustomField(fieldName).Content).Month
			d = UserPersonalizationHelper.CovertToDate(Quote.GetCustomField(fieldName).Content).Day
			return int(y), int(m), int(d)

	#Start CXCPQ-69656 - Jagruti - 24/11/2023
	if Quote.GetCustomField('Quote Type').Content  in ['Contract Renewal','Contract New']:
		CurrAnnulStartDate = Quote.GetCustomField('SC_CF_CURANNDELSTDT')
		CurrAnnulEndDate = Quote.GetCustomField('SC_CF_CURANNDELENDT')
		Term_Duration_Months = Quote.GetCustomField('SC_CF_Term_duration_Months')
		days = 0
		if CurrAnnulStartDate.Content.strip() != '' and CurrAnnulEndDate.Content.strip() != '':
			yy1, mm1, dd1 = parseDate(TagParserQuote, Quote, 'SC_CF_CURANNDELSTDT')
			yy2, mm2, dd2 = parseDate(TagParserQuote, Quote, 'SC_CF_CURANNDELENDT')
			ddate1 = date(yy1, mm1, dd1)
			ddate2 = date(yy2, mm2, dd2)
			ddays = float(numOfDays(ddate1, ddate2))
			Term_Duration_Months.Content = str(int(round(ddays/30.436875,0)))
			#Trace.Write('*****'+Term_Duration_Months.Content)
		else:
			Term_Duration_Months.Content = ''
	
	#End

	cf_contractStartDate = Quote.GetCustomField('EGAP_Contract_Start_Date')
	cf_contractEndDate = Quote.GetCustomField('EGAP_Contract_End_Date')
	cf_projectDurationMonths = Quote.GetCustomField('EGAP_Project_Duration_Months')
	cf_projectDurationWeeks = Quote.GetCustomField('EGAP_Project_Duration_Weeks')
	#jagruti --added code for service contract--
	cf_projectDurationYears = Quote.GetCustomField('SC_CF_CONTRACTDURYR')

	d = 0
	if cf_contractStartDate.Content.strip() != '' and cf_contractEndDate.Content.strip() != '':
		y1, m1, d1 = parseDate(TagParserQuote, Quote, 'EGAP_Contract_Start_Date')
		y2, m2, d2 = parseDate(TagParserQuote, Quote, 'EGAP_Contract_End_Date')
		date1 = date(y1, m1, d1)
		date2 = date(y2, m2, d2)
		d = float(numOfDays(date1, date2))
		#jagruti --added code for service contract--
		#cf_projectDurationMonths.Content = str(int(math.ceil(d/30.417)))
		cf_projectDurationWeeks.Content = str(int(math.ceil(d/7.0)))
		#Start - CCXCPQ-60167 - Jagruti Chandratre - 21/8/2023 - for contract duration(Months) custom field
		if Quote.GetCustomField('Quote Type').Content in ['Contract New','Contract Renewal'] and Quote.GetCustomField('Booking LOB').Content == "LSS":
			cf_projectDurationMonths.Content = str(int(round(d/30.436875,0)))
		else:
			cf_projectDurationMonths.Content = str(int(round(d/30,0)))
		'''
		START - This code belongs to Service Contract Project for Contract Duration(Years) Calculations - CCXCPQ-60167 - Jagruti Chandratre - 10/8/2023
		'''
		years = str(int(math.ceil(d// 365.2425)))
		years_r = d % 365.2425
		days_r = int(math.ceil(years_r % 30.436875))
		if days_r <= 15:
			months = str(int(math.ceil(years_r // 30.436875)))
		else:
			months = str(int(math.ceil(years_r // 30.436875)) + 1)
			if int(months) == 12:
				years = str(int(years)+1)
				months = str(0)
		Quote.GetCustomField('SC_CF_CONTRACTDURYR').Content = years + "." + months + " years"
		#Trace.Write("duration in years ---> " + str(years + "." + months + " years") + " <<>> " + str(cf_projectDurationYears.Content) )
		''' END '''
	else:
		cf_projectDurationYears.Content = ''
		cf_projectDurationMonths.Content = ''
		cf_projectDurationWeeks.Content = ''
	'''Calculate Credit Terms in months'''
	paymentTerms = Quote.GetCustomField("Payment Terms")
	cf_creditTermsMonths = Quote.GetCustomField("EGAP_Credit_Terms_Months")
	cf_creditTermsMonths.Content = '0'

	if paymentTerms.Content.strip() != '' and paymentTerms.Content.strip() != 'COD':

	#if paymentTerms.Content.strip() != '' and paymentTerms.Content.strip() != 'COD'and Quote.GetCustomField('Quote Type').Content not in ('Contract New','Contract Renewal'):
		cf_creditTermsMonths.Content = str(int(round(float(paymentTerms.Content.split(' ')[0])/30.0)))
		creditPaymentTerms = int(paymentTerms.Content.split(' ')[0])
		quesCR1a = Quote.GetCustomField('EGAP_Ques_CR1a')
		Quote.GetCustomField('EGAP_Risk_Count_CR1a').Content = '0'
		if quesCR1a.Content == 'Yes' or creditPaymentTerms >= 60:
			Quote.GetCustomField('EGAP_Risk_Count_CR1a').Content = '1'
