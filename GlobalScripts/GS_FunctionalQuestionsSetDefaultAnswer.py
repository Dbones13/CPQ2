from datetime import date
from GS_PopulateEGAPApproversQuoteTable_Helper import *
def numOfDays(date1, date2):
	return (date2-date1).days

def parseDate(TagParserQuote, fieldName):
	y = TagParserQuote.ParseString("<*CTX( Quote.CustomField({}).Format(yyyy))*>".format(fieldName))
	m = TagParserQuote.ParseString("<*CTX( Quote.CustomField({}).Format(MM))*>".format(fieldName))
	d = TagParserQuote.ParseString("<*CTX( Quote.CustomField({}).Format(dd))*>".format(fieldName))
	return int(y), int(m), int(d)

def setCustomFieldsEditable(Quote, fieldsList, isEditable):
	for field in fieldsList:
		if ((field == 'EGAP_ETR_Number' and Quote.GetCustomField('EGAP_CFR4_Ques').Content == 'Yes') or (field == 'EGAP_RAFR1_RQUP_Number' and Quote.GetCustomField('EGAP_RAFR1_Ques').Content == 'Yes')or (field == 'EGAP_RAFR2_RQUP_Number' and Quote.GetCustomField('EGAP_RAFR2_Ques').Content == 'Yes') or (field == 'EGAP_CFR6_Ques' and Quote.GetCustomField('Opportunity Type').Content == 'Change Order')):
			Quote.GetCustomField(field).Editable = isEditable
		elif field not in ['EGAP_ETR_Number', 'EGAP_RAFR1_RQUP_Number', 'EGAP_RAFR2_RQUP_Number','EGAP_CFR6_Ques']:
			Quote.GetCustomField(field).Editable = isEditable

def functionalQuest_permission(fieldsList):
	changeAnsOfFuncQues = Quote.GetCustomField('EGAP_Do_Want_to_Chanage_Ans_of_Func_Ques')
	cf_IsBookingCheckVisible = Quote.GetCustomField('EGAP_IS_Booking_Check_Visible')
	fieldsList.append('EGAP_ETR_Number')
	fieldsList.append('EGAP_RAFR1_RQUP_Number')
	fieldsList.append('EGAP_RAFR2_RQUP_Number')
	fieldsList.append('EGAP_CTFR7_Ques')
	if Quote.OrderStatus.Name != 'Preparing':
		setCustomFieldsEditable(Quote, fieldsList, False)
	elif cf_IsBookingCheckVisible.Content == 'Yes':
		if changeAnsOfFuncQues.Content == 'Yes':
			setCustomFieldsEditable(Quote, fieldsList, True)
		else:
			setCustomFieldsEditable(Quote, fieldsList, False)

quoteType = Quote.GetCustomField("Quote Type").Content
LOB = Quote.GetCustomField('Booking LOB').Content
fieldsList = ['EGAP_Ques_CR1a','EGAP_Ques_CR1b','EGAP_Ques_CR3a','EGAP_Ques_CR3b','EGAP_Ques_CR3c','EGAP_Ques_CR3d','EGAP_Ques_CR4a','EGAP_Ques_CR4b','EGAP_Ques_CR4c','EGAP_Ques_CR5a','EGAP_Ques_CR5b','EGAP_Ques_CR5c','EGAP_Ques_CR6a','EGAP_Ques_CR6b','EGAP_Ques_CR7a','EGAP_Ques_CR8a','EGAP_Ques_CR9a','EGAP_Ques_CR9b','EGAP_IQ_Ques_1','EGAP_IQ_Ques_2','EGAP_IQ_Ques_3','EGAP_IQ_Ques_4','EGAP_CFR1_Ques','EGAP_CFR2_Ques','EGAP_CFR3_Ques','EGAP_CFR4_Ques','EGAP_CFR5_Ques','EGAP_CFR6_Ques','EGAP_MFR1_Ques','EGAP_MFR2_Ques','EGAP_PFR1_Ques','EGAP_RAFR1_Ques','EGAP_RAFR2_Ques','EGAP_RAFR3_Ques','EGAP_RAFR4_Ques','EGAP_RAFR5_Ques','EGAP_CTFR1_Ques','EGAP_CTFR2_Ques','EGAP_CTFR3_Ques','EGAP_CTFR4_Ques','EGAP_CTFR5_Ques','EGAP_CTFR6_Ques','EGAP_CTFR8_Ques','EGAP_CAR_Ques_1','EGAP_CAR_Ques_2','EGAP_CAR_Ques_3','EGAP_CAR_Ques_4','EGAP_CAR_Ques_5','EGAP_CAR_Ques_6','EGAP_CAR_Ques_7','EGAP_CAR_Ques_8','EGAP_CAR_Ques_9','EGAP_CTFR10_Ques','EGAP_CTFR11_Ques','EGAP_CTFR12_Ques','EGAP_IQ_Ques_15','EGAP_IQ_Ques_16','EGAP_IQ_Ques_17']
if LOB == 'CCC':
	Quote.GetCustomField('EGAP_CFD_Cash_Flow_Quality').Content = '0'
if quoteType in ['Projects','Contract New', 'Contract Renewal'] and Quote.Items.Count>0:
	for field in fieldsList:
		quoteCustomField = Quote.GetCustomField(field)
		if field in ('EGAP_Ques_CR3a','EGAP_Ques_CR4a','EGAP_Ques_CR4b','EGAP_PFR1_Ques','EGAP_RAFR1_Ques','EGAP_CAR_Ques_3','EGAP_CAR_Ques_4','EGAP_CAR_Ques_5','EGAP_CAR_Ques_6','EGAP_CAR_Ques_7','EGAP_IQ_Ques_1','EGAP_IQ_Ques_2','EGAP_IQ_Ques_3','EGAP_IQ_Ques_4') and LOB == 'CCC':
			Quote.GetCustomField(field).Content = 'No'
		elif quoteCustomField.Content.strip() == '':
			Quote.GetCustomField(field).Content = TagParserQuote.ParseString(quoteCustomField.CalculationFormula)

	cfDict = dict()
	if quoteType in ['Contract New', 'Contract Renewal']:
		#MFR1 and RAFR3 are not applicable to Service contract, the default value of these question should be "No" and questions should be hidden
		hiddenQnDict = {'EGAP_MFR1_Ques':'No', 'EGAP_RAFR3_Ques':'No'}
		for cf in hiddenQnDict.keys():
			Quote.GetCustomField(cf).Visible = False
			Quote.GetCustomField(cf).Content = hiddenQnDict[cf]
		cfDict = {'EGAP_RAFR2_Ques':'No', 'EGAP_Ques_CR3a':'No'}
	elif quoteType == 'Projects':
		cfDict = {'EGAP_MFR1_Ques':'Yes', 'EGAP_RAFR3_Ques':'Yes', 'EGAP_RAFR2_Ques':'Yes', 'EGAP_Ques_CR3a':'Yes'}
	for cf in cfDict.keys():
		if Quote.GetCustomField(cf).Content == '':
			Quote.GetCustomField(cf).Content = cfDict[cf]
	if LOB == 'CCC':
		Quote.GetCustomField('EGAP_RAFR1_Ques').Content = 'No'
		# Quote.GetCustomField('EGAP_Cashflow_Health').Content = 'In Balance'
	question = Quote.GetCustomField('EGAP_Ques_CR1a')
	creditPaymentTerms = Quote.GetCustomField('Payment Terms').Content
	if creditPaymentTerms is not None and creditPaymentTerms.strip() != '' and creditPaymentTerms.strip() != 'COD':
		creditPaymentTerms = int(creditPaymentTerms.split(' ')[0])
	else:
		creditPaymentTerms = 0
	Quote.GetCustomField('EGAP_Risk_Count_CR1a').Content = '0'
	Quote.GetCustomField('EGAP_Risk_Count_CR1b').Content = '0'
	question1 = Quote.GetCustomField('EGAP_Ques_CR1b')
	if question.Content == 'Yes' or creditPaymentTerms >= 60:
		Quote.GetCustomField('EGAP_Risk_Count_CR1a').Content = Quote.GetCustomField('EGAP_Risk_Count_CR1b').Content = '1'

	questionA = Quote.GetCustomField('EGAP_Ques_CR3a')
	questionB = Quote.GetCustomField('EGAP_Ques_CR3b')
	questionC = Quote.GetCustomField('EGAP_Ques_CR3c')
	questionD = Quote.GetCustomField('EGAP_Ques_CR3d')
	CFQ = Quote.GetCustomField('EGAP_Cash_Flow_Quality')
	advancePayment =  Quote.GetCustomField('EGAP_Advance_Payment_Milestone_Billing_Ques')
	CFQPercentage = 0
	if CFQ.Content is not None and CFQ.Content.strip() != '':
		CFQPercentage = float(CFQ.Content.replace('%',''))
	Quote.GetCustomField('EGAP_Risk_Count_CR3a').Content = Quote.GetCustomField('EGAP_Risk_Count_CR3b').Content = Quote.GetCustomField('EGAP_Risk_Count_CR3c').Content = Quote.GetCustomField('EGAP_Risk_Count_CR3d').Content = '0'
	walkAwayPrice = TagParserQuote.ParseString('<*CTX( Number(<*Round (<* GetFirstFromQuoteTable(Quote_Details,Walk_away_Sales_Price) *>,0)*>).Format )*>')
	walkAwayPrice = int(walkAwayPrice.replace(',','')) if walkAwayPrice else 0
	if questionA.Content == 'Yes' or (advancePayment.Content == 'Yes' and quoteType != 'Projects'):
		Quote.GetCustomField('EGAP_Risk_Count_CR3a').Content = Quote.GetCustomField('EGAP_Risk_Count_CR3b').Content = Quote.GetCustomField('EGAP_Risk_Count_CR3c').Content = Quote.GetCustomField('EGAP_Risk_Count_CR3d').Content = '4'
	elif LOB == 'PAS' and advancePayment.Content == 'Yes':
		if walkAwayPrice <= 500000:
			Quote.GetCustomField('EGAP_Risk_Count_CR3a').Content = Quote.GetCustomField('EGAP_Risk_Count_CR3b').Content = Quote.GetCustomField('EGAP_Risk_Count_CR3c').Content =Quote.GetCustomField('EGAP_Risk_Count_CR3d').Content ='3'
		else:
			Quote.GetCustomField('EGAP_Risk_Count_CR3a').Content = Quote.GetCustomField('EGAP_Risk_Count_CR3b').Content = Quote.GetCustomField('EGAP_Risk_Count_CR3c').Content = Quote.GetCustomField('EGAP_Risk_Count_CR3d').Content = '4'
	elif LOB in ['CCC']:
		if  questionB.Content == 'Yes':
			Quote.GetCustomField('EGAP_Risk_Count_CR3a').Content = Quote.GetCustomField('EGAP_Risk_Count_CR3b').Content = Quote.GetCustomField('EGAP_Risk_Count_CR3c').Content = Quote.GetCustomField('EGAP_Risk_Count_CR3d').Content = '1'
		else:
			Quote.GetCustomField('EGAP_Risk_Count_CR3a').Content = Quote.GetCustomField('EGAP_Risk_Count_CR3b').Content = Quote.GetCustomField('EGAP_Risk_Count_CR3c').Content = Quote.GetCustomField('EGAP_Risk_Count_CR3d').Content = '0'
	elif LOB != 'PAS' and advancePayment.Content == 'Yes':
		Quote.GetCustomField('EGAP_Risk_Count_CR3a').Content = Quote.GetCustomField('EGAP_Risk_Count_CR3b').Content = Quote.GetCustomField('EGAP_Risk_Count_CR3c').Content = Quote.GetCustomField('EGAP_Risk_Count_CR3d').Content = '4'
	elif questionB.Content == 'Yes' or CFQPercentage < 1.0:
		Quote.GetCustomField('EGAP_Risk_Count_CR3a').Content = Quote.GetCustomField('EGAP_Risk_Count_CR3b').Content = Quote.GetCustomField('EGAP_Risk_Count_CR3c').Content = Quote.GetCustomField('EGAP_Risk_Count_CR3d').Content = '1'
	questionA = Quote.GetCustomField('EGAP_Ques_CR4a')
	questionB = Quote.GetCustomField('EGAP_Ques_CR4b')
	questionC = Quote.GetCustomField('EGAP_Ques_CR4c')
	currency  = Quote.GetCustomField('Currency')
	functionalCurrency = Quote.GetCustomField('Functional Currency of Entity')
	Quote.GetCustomField('EGAP_Risk_Count_CR4a').Content = Quote.GetCustomField('EGAP_Risk_Count_CR4b').Content = Quote.GetCustomField('EGAP_Risk_Count_CR4c').Content = '0'
	if questionA.Content == 'No' and questionB.Content == 'No' and questionC.Content == 'Yes':
		Quote.GetCustomField('EGAP_Risk_Count_CR4a').Content = Quote.GetCustomField('EGAP_Risk_Count_CR4b').Content = Quote.GetCustomField('EGAP_Risk_Count_CR4c').Content = '1'

	questionA = Quote.GetCustomField('EGAP_Ques_CR5a')
	questionB = Quote.GetCustomField('EGAP_Ques_CR5b')
	questionC = Quote.GetCustomField('EGAP_Ques_CR5c')
	Quote.GetCustomField('EGAP_Risk_Count_CR5a').Content = Quote.GetCustomField('EGAP_Risk_Count_CR5b').Content = Quote.GetCustomField('EGAP_Risk_Count_CR5c').Content = '0'

	contractStartDate = Quote.GetCustomField('EGAP_Contract_Start_Date')
	contractEndDate = Quote.GetCustomField('EGAP_Contract_End_Date')
	d = 0
	if contractStartDate.Content.strip() != '' and contractEndDate.Content.strip() != '':
		y1, m1, d1 = parseDate(TagParserQuote, 'EGAP_Contract_Start_Date')
		y2, m2, d2 = parseDate(TagParserQuote, 'EGAP_Contract_End_Date')
		date1 = date(y1, m1, d1)
		date2 = date(y2, m2, d2)
		d = float(numOfDays(date1, date2))

	if ((d/30.417) > 12 and questionA.Content == questionB.Content and questionA.Content == 'No'):
		Quote.GetCustomField('EGAP_Risk_Count_CR5a').Content = Quote.GetCustomField('EGAP_Risk_Count_CR5b').Content = Quote.GetCustomField('EGAP_Risk_Count_CR5c').Content = '1'


	questionA = Quote.GetCustomField('EGAP_Ques_CR6a')
	questionB = Quote.GetCustomField('EGAP_Ques_CR6b')
	Quote.GetCustomField('EGAP_Risk_Count_CR6a').Content = Quote.GetCustomField('EGAP_Risk_Count_CR6b').Content = '0'
	if questionA.Content == 'Yes' or questionB.Content == 'Yes':
		Quote.GetCustomField('EGAP_Risk_Count_CR6a').Content = Quote.GetCustomField('EGAP_Risk_Count_CR6b').Content = '1'

	questionA = Quote.GetCustomField('EGAP_Ques_CR7a')
	Quote.GetCustomField('EGAP_Risk_Count_CR7a').Content = '0'
	if questionA.Content == 'Yes':
		Quote.GetCustomField('EGAP_Risk_Count_CR7a').Content = '1'

	questionA = Quote.GetCustomField('EGAP_Ques_CR8a')
	Quote.GetCustomField('EGAP_Risk_Count_CR8a').Content = '0'
	if questionA.Content == 'Yes':
		Quote.GetCustomField('EGAP_Risk_Count_CR8a').Content = '1'

	questionA = Quote.GetCustomField('EGAP_Ques_CR9a')
	questionB = Quote.GetCustomField('EGAP_Ques_CR9b')
	Quote.GetCustomField('EGAP_Risk_Count_CR9a').Content = Quote.GetCustomField('EGAP_Risk_Count_CR9b').Content = '0'
	if questionA.Content == 'Yes' and questionB.Content == 'Yes':
		Quote.GetCustomField('EGAP_Risk_Count_CR9a').Content = Quote.GetCustomField('EGAP_Risk_Count_CR9b').Content = '1'

	riskCountList = ['EGAP_Risk_Count_CR1a','EGAP_Risk_Count_CR3a','EGAP_Risk_Count_CR4a','EGAP_Risk_Count_CR5a','EGAP_Risk_Count_CR6a','EGAP_Risk_Count_CR7a','EGAP_Risk_Count_CR8a','EGAP_Risk_Count_CR9a']
	sum = 0
	for riskCount in riskCountList:
		sum += int(Quote.GetCustomField(riskCount).Content or 0)
	Quote.GetCustomField('EGAP_Total_Number_Of_Risk_Factors').Content = str(sum)

	questionCFR4  = Quote.GetCustomField('EGAP_CFR4_Ques')
	Quote.GetCustomField('EGAP_ETR_Number').Editable = False
	Quote.GetCustomField('EGAP_ETR_Number').Required = False
	if questionCFR4.Content == 'Yes':
		Quote.GetCustomField('EGAP_ETR_Number').Editable = True
		#Quote.GetCustomField('EGAP_ETR_Number').Required = True
	questionCTFR6 = Quote.GetCustomField('EGAP_CTFR6_Ques')
	Quote.GetCustomField('EGAP_CTFR7_Ques').Editable = Quote.GetCustomField('EGAP_CTFR8_Ques').Editable = False
	if questionCTFR6.Content == 'Yes':
		Quote.GetCustomField('EGAP_CTFR7_Ques').Editable = Quote.GetCustomField('EGAP_CTFR8_Ques').Editable = True
	questionRAFR1  = Quote.GetCustomField('EGAP_RAFR1_Ques')
	questionRAFR3  = Quote.GetCustomField('EGAP_RAFR3_Ques')
	Quote.GetCustomField('EGAP_RAFR1_RQUP_Number').Editable = False
	Quote.GetCustomField('EGAP_RAFR1_RQUP_Number').Required = False
	if questionRAFR1.Content == 'Yes':
		Quote.GetCustomField('EGAP_RAFR1_RQUP_Number').Editable = True
		#Quote.GetCustomField('EGAP_RAFR1_RQUP_Number').Required = True
	questionRAFR2  = Quote.GetCustomField('EGAP_RAFR2_Ques')
	Quote.GetCustomField('EGAP_RAFR2_RQUP_Number').Editable = False
	Quote.GetCustomField('EGAP_RAFR2_RQUP_Number').Required = False
	if questionRAFR2.Content == 'Yes':
		Quote.GetCustomField('EGAP_RAFR2_RQUP_Number').Editable = True
	#Hide MFR2,CFR3 questions and rules if Walk Away Price > 100000
	if quoteType == 'Projects':
		exchangeRate = float(Quote.GetCustomField('Exchange Rate').Content)
		walkAwayPrice /= exchangeRate
	else:
		Qcurrency = Quote.GetCustomField('SC_CF_CURRENCY').Content
		exRate = float(Quote.GetCustomField('SC_CF_EXCHANGE_RATE').Content)
		ListPrice=0.0
		for items in filter(lambda y : y.ProductName =='Service Contract Products' , Quote.MainItems):
			ListPrice = items.ExtendedAmount
		if Qcurrency == 'USD':
			TotalCV = round(ListPrice,2)
		else:
			TotalCV = round(ListPrice/exRate,2)
		walkAwayPrice = TotalCV
		exchangeRate = exRate
	Quote.CustomFields.Allow('EGAP_MFR2_Ques', 'EGAP_MFR2_Ques_Rule', 'EGAP_CFR3_Ques', 'EGAP_CFR3_Ques_Rule')
	if walkAwayPrice > 100000:
		Quote.CustomFields.Disallow('EGAP_MFR2_Ques', 'EGAP_MFR2_Ques_Rule', 'EGAP_CFR3_Ques', 'EGAP_CFR3_Ques_Rule')

	isMPAApplied = Quote.GetCustomField('MPA Price Plan').Content.strip()
	MPAValue = Quote.GetCustomField('SC_CF_AGREEMENT_TYPE').Content
	'''Hide the PFR1 custom field If MPA is not applied'''
	if (quoteType == 'Projects' and isMPAApplied !='') or (quoteType != 'Projects' and MPAValue in ['MPA','ISA','LPA']): # As a part of CXCPQ-107719 this story removed the condition.
		Quote.CustomFields.Allow('EGAP_PFR1_Ques')
		if Quote.GetCustomField('EGAP_PFR1_Ques').Content == '':
			Quote.GetCustomField('EGAP_PFR1_Ques').Content = Quote.GetCustomField('EGAP_PFR1_Ques').CalculationFormula
	else:
		Quote.CustomFields.Disallow('EGAP_PFR1_Ques')
	IsCashRiskQuestionsVisible = Quote.GetCustomField('IsCashRiskQuestionsVisible')
	IsCashRiskQuestionsVisible.Content = '1'
	if quoteType == 'Projects':
		ContractDuration = d/30.417
	else:
		projDuration = Quote.GetCustomField("EGAP_Project_Duration_Months").Content.strip()
		ContractDuration = int(projDuration) if projDuration != '' else 0
	if ((isMPAApplied !='' and quoteType == 'Projects') or MPAValue == 'MPA') or walkAwayPrice <= 100000 or ContractDuration < 3:
		IsCashRiskQuestionsVisible.Content = '0'
		Quote.GetCustomField('EGAP_Ques_CR3a').Content = 'No'
	'''Hide EGAP_CTFR7_Ques and EGAP_CTFR8_Ques if EGAP_CTFR6_Ques is No'''
	CTFR6 = Quote.GetCustomField('EGAP_CTFR6_Ques').Content
	Quote.CustomFields.Allow('EGAP_CTFR7_Ques', 'EGAP_CTFR8_Ques')
	if CTFR6 == 'No':
		Quote.GetCustomField('EGAP_CTFR8_Ques').Content = 'No'
		Quote.CustomFields.Disallow('EGAP_CTFR7_Ques', 'EGAP_CTFR8_Ques')

	'''Hide/Show functional questions based on the custom field (EGAP_Do_Want_to_Chanage_Ans_of_Func_Ques) value and Quote status '''
	functionalQuest_permission(fieldsList)
	'''R&O assessment'''
	Quote.GetCustomField("IS_RandO_AssesmentRequired").Content = '0'
	proposalType = Quote.GetCustomField("EGAP_Proposal_Type").Content
	if proposalType != 'Budgetary' and walkAwayPrice > 500000:
		Quote.GetCustomField("IS_RandO_AssesmentRequired").Content = '1'

	'''Populating the Approval Not Required Flag'''
	IsApprovalNotRequired = '0'
	Is_Quote_Approval_Exempted = 'No'
	LOB = Quote.GetCustomField('Booking LOB').Content
	if Quote.Items.Count > 0 :#and LOB == 'PAS':
		projectType = Quote.GetCustomField('EGAP_Project_Type').Content
		quoteDetailsQT  = Quote.QuoteTables["Quote_Details"]
		quoteDetails    = quoteDetailsQT.Rows[0]
		sellPrice = quoteDetails['Quote_Sell_Price']
		negotiationLimit = quoteDetails['Negotiation_Limit']
		quoteDiscountPercent = quoteDetails['Quote_Discount_Percent']
		if quoteType == 'Projects':
			walkAwaySellPrice = sellPrice - negotiationLimit
			MPA = Quote.GetCustomField('MPA Price Plan').Content if Quote.GetCustomField('MPA Price Plan').Content.strip() !='' else 'None'
		else:
			walkAwaySellPrice = sellPrice
			MPA = MPAValue if MPAValue.strip() !='' else 'None'
		transferPrice = quoteDetails['Quote_Regional_Cost']
		regionalMargin = walkAwaySellPrice - transferPrice
		regionalMarginPercent = wtwMarginPercentage = 0
		quoteWTWCost = quoteDetails['Quote_WTW_Cost']
		wtwMargin = walkAwaySellPrice - quoteWTWCost
		if walkAwaySellPrice >0:
			regionalMarginPercent = (regionalMargin/walkAwaySellPrice)*100
			wtwMarginPercentage = (wtwMargin/walkAwaySellPrice)*100
		recommendedTargetPrice = quoteDetails['Recommended_Target_Price']
		recommendedTargetPriceUSD = recommendedTargetPrice/exchangeRate
		walkAwaySellPriceUSD = walkAwaySellPrice/exchangeRate
		if MPA == 'None':
			excessDiscount = 0
		else:
			excessDiscount = 0 if recommendedTargetPrice <= 1 else (recommendedTargetPriceUSD-walkAwaySellPriceUSD)/recommendedTargetPriceUSD
			excessDiscount *= 100
		cTFR2Ques = Quote.GetCustomField('EGAP_CTFR2_Ques').Content
		cTFR1Ques = Quote.GetCustomField('EGAP_CTFR1_Ques').Content
		mFR2Ques  = Quote.GetCustomField('EGAP_MFR2_Ques').Content
		cFR3Ques  = Quote.GetCustomField('EGAP_CFR3_Ques').Content
		cFR1Ques  = Quote.GetCustomField('EGAP_CFR1_Ques').Content
		cFR5Ques  = Quote.GetCustomField('EGAP_CFR5_Ques').Content
		cFR6Ques  = Quote.GetCustomField('EGAP_CFR6_Ques').Content
		iOQues15 = Quote.GetCustomField('EGAP_IQ_Ques_15').Content

		hWSWPLSG = []
		hWSWSellPrice = 0
		otherSellPrice = 0
		if quoteType == 'Projects':
			sqlResult = SqlHelper.GetList("Select distinct SAP_PL_PLSG, Cost_Category, LOB, Sub_LOB from SAP_PLSG_LOB_Mapping where Cost_Category in ('Honeywell Software')")
			if sqlResult is not None:
				for row in sqlResult:
					hWSWPLSG.append(row.SAP_PL_PLSG)
			pLSGDetails = Quote.QuoteTables['Product_Line_Sub_Group_Details']
			for row in pLSGDetails.Rows:
				pLSG = row['Product_Line_Sub_Group']
				if pLSG in hWSWPLSG:
					hWSWSellPrice += float(row['PLSG_Target_Sell_Price'])
				else:
					otherSellPrice += float(row['PLSG_Target_Sell_Price'])
		hWSWSellPriceinUSD = round(float(hWSWSellPrice)/exchangeRate) if exchangeRate > 0 else hWSWSellPrice
		otherSellPriceSellPriceinUSD = round(float(otherSellPrice)/exchangeRate) if exchangeRate > 0 else otherSellPrice

		is_r2q_request = Quote.GetCustomField('ISR2QRequest').Content
		sellPrice = walkAwayPrice
		quoteWTWCost = quoteWTWCost
		wtwMargin = sellPrice - quoteWTWCost
		quoteDiscount = round((wtwMargin/sellPrice)*100,2) if sellPrice > 0 else 0

		if quoteType in ['Projects']:
			if LOB == 'PAS':
				if projectType == 'Fixed Price' and walkAwaySellPriceUSD <= 100000 and regionalMarginPercent > 35  and questionRAFR1.Content == 'No'  and cTFR1Ques == 'No' and mFR2Ques in('Yes','') and cFR3Ques in('Yes','') and cFR1Ques == 'No' and cFR5Ques == 'No' and ((Quote.GetCustomField('Opportunity Type').Content == 'Change Order' and cFR6Ques == 'No') or (Quote.GetCustomField('Opportunity Type').Content != 'Change Order')):
					IsApprovalNotRequired = '1'
					Is_Quote_Approval_Exempted = 'Yes'
				elif projectType == 'Time & Material Only' and walkAwaySellPriceUSD <= 5000000  and regionalMarginPercent > 50  and questionRAFR1.Content == 'No' and cTFR2Ques == 'No' and cTFR1Ques == 'No' and mFR2Ques in('Yes','') and cFR3Ques in('Yes','') and cFR1Ques == 'No' and cFR5Ques == 'No' and ((Quote.GetCustomField('Opportunity Type').Content == 'Change Order' and cFR6Ques == 'No') or (Quote.GetCustomField('Opportunity Type').Content != 'Change Order')):
					IsApprovalNotRequired = '1'
					Is_Quote_Approval_Exempted = 'Yes'
				if hWSWSellPriceinUSD > 0 and otherSellPriceSellPriceinUSD == 0 and walkAwaySellPriceUSD <= 250000 and regionalMarginPercent >= 5 and excessDiscount <= 5 and cTFR1Ques == 'No' and cFR1Ques == 'No' and cFR5Ques == 'No' and ((Quote.GetCustomField('Opportunity Type').Content == 'Change Order' and cFR6Ques == 'No') or (Quote.GetCustomField('Opportunity Type').Content != 'Change Order')):
					IsApprovalNotRequired = '1'
					Is_Quote_Approval_Exempted = 'Yes'
			elif LOB == 'HCP':
					regionalMarginPercent,thirdpartymarkup = None,None
					BGPzeroQuantity = check_swbgp(Quote)
					# Trace.Write('1426--'+str(BGPzeroQuantity))
					HWMatQuery=SqlHelper.GetFirst("SELECT Sell_Price,Regional_Cost FROM {} WHERE cartid = {} AND ownerId ={} and Product_Type ='Honeywell Material' and Sell_Price != 0".format('QT__Product_Type_Details',Quote.QuoteId, Quote.UserId))
					if HWMatQuery and HWMatQuery.Sell_Price > 0:
						regionalMarginPercent=float((HWMatQuery.Sell_Price-HWMatQuery.Regional_Cost)/HWMatQuery.Sell_Price)*100

					thirdpartQuery=SqlHelper.GetFirst("SELECT Sell_Price,Regional_Cost FROM {} WHERE cartid = {} AND ownerId ={} and Sell_Price != 0 and (Product_Type ='Third-Party Material' or Product_Type ='Third-Party Labor')".format('QT__Product_Type_Details',Quote.QuoteId, Quote.UserId))
					if thirdpartQuery and thirdpartQuery.Regional_Cost > 0:
						thirdpartymarkup = ((thirdpartQuery.Sell_Price-thirdpartQuery.Regional_Cost)/thirdpartQuery.Regional_Cost)*100

					thirdPartyHoninUSD, thirdPartyMaterialTP, trueThirdPartyinUSD = 0, 0, 0

					thirdPartyContent = False if thirdpartymarkup and thirdpartymarkup < 20 else True
					regionalMarginPercentContent=False if regionalMarginPercent and regionalMarginPercent < 30 else True

					query=SqlHelper.GetList("Select SAP_PLSG_Description,Third_Party_Category,SAP_PL_PLSG from SAP_PLSG_LOB_MAPPING where Third_Party_Category = 'True Third Party' or Third_Party_Category ='Third Party Hon'")
					PLSG_TP_Categor_Map={}
					for i in query:
						PLSG_TP_Categor_Map[i.SAP_PL_PLSG]= str(i.Third_Party_Category)
					for item in Quote.MainItems:
						if(item['QI_PLSG'].Value):
							if item['QI_PLSG'].Value and str(item['QI_PLSG'].Value) in PLSG_TP_Categor_Map.keys():
								if PLSG_TP_Categor_Map[str(item['QI_PLSG'].Value)] == 'True Third Party':
									trueThirdPartyinUSD = trueThirdPartyinUSD + item.ExtendedCost
								else:
									thirdPartyHoninUSD= thirdPartyHoninUSD + item.ExtendedCost
					thirdPartyMaterialTP = thirdPartyHoninUSD + trueThirdPartyinUSD
					
					if (cTFR1Ques == 'No' and questionRAFR1.Content == 'No' and cFR1Ques == 'No' and cFR5Ques == 'No' and cFR6Ques == 'No' and thirdPartyMaterialTP<=250000 and regionalMarginPercentContent and thirdPartyContent and trueThirdPartyinUSD<250000 and BGPzeroQuantity!= 'false' and iOQues15 == 'No' and isMPAApplied!= '' and int(quoteDiscountPercent) <= 0 and ((Quote.GetCustomField('Is Payment milestones are negatively deviating from standard milestone?').Content == 'No' and Quote.GetCustomField('Payment Milestones as per Standard/MPA?').Content == 'No') or (Quote.GetCustomField('Payment Milestones as per Standard/MPA?').Content == 'Yes'))) or (is_r2q_request == 'Yes' and walkAwaySellPrice < 1000000 and quoteDiscount > 35) :
						IsApprovalNotRequired = '1'
						Is_Quote_Approval_Exempted = 'Yes'
						# Quote.GetCustomField('EGAP_Highest_Price_Margin_Approval_Level').Content = "No Approval"
						# Quote.GetCustomField('EGAP_Highest_Approval_Level_for_the_Quote').Content = "No Approval"
			elif LOB == 'LSS':
				if walkAwaySellPriceUSD <= 250000 and regionalMarginPercent > 50  and questionRAFR1.Content == 'No' and cTFR1Ques == 'No' and cFR1Ques == 'No' and cFR5Ques == 'No':
					if ((Quote.GetCustomField('Opportunity Type').Content == 'Change Order' and cFR6Ques == 'No') or (Quote.GetCustomField('Opportunity Type').Content != 'Change Order')):
						IsApprovalNotRequired = '1'
						Is_Quote_Approval_Exempted = 'Yes'
					#Quote.GetCustomField('EGAP_Highest_Approval_Level_for_the_Quote').Content = "No Approval"
					# Quote.GetCustomField('EGAP_Highest_Approval_Level_for_the_Quote').Content = "No Approval"
					#Quote.GetCustomField('EGAP_Highest_Price_Margin_Approval_Level').Content = "No Approval"
			#Quote.GetCustomField('CF_MaxApprovalLevel').Content = ""
			# Log.Info("am in Noapproval2==>"+str(Quote.GetCustomField('EGAP_Highest_Price_Margin_Approval_Level').Content))
			if str(IsApprovalNotRequired) == '0' and LOB in("LSS", "PAS", "HCP", "CCC") and Quote.GetCustomField('EGAP_Highest_Price_Margin_Approval_Level').Content == 'No Approval':
				# Log.Info("am in Noapproval")
				IsApprovalNotRequired='1'
				# Is_Quote_Approval_Exempted = 'Yes'
			Quote.GetCustomField('IsApprovalNotRequired').Content = IsApprovalNotRequired
			Quote.GetCustomField('IsApprovalNotRequired_FQ').Content = IsApprovalNotRequired
			Quote.GetCustomField('Is_Quote_Approval_Exempted').Content = Is_Quote_Approval_Exempted
			# if Is_Quote_Approval_Exempted == 'Yes':
				# Quote.GetCustomField('EGAP_Highest_Approval_Level_for_the_Quote').Content = "No Approval"
	'''Hide functional questions based on LOB'''
	if LOB == "LSS":
		Quote.CustomFields.Disallow('EGAP_CFR3_Ques', 'EGAP_MFR2_Ques', 'EGAP_IQ_Ques_1', 'EGAP_IQ_Ques_2', 'EGAP_IQ_Ques_3')
	elif LOB == "PAS":
		Quote.CustomFields.Disallow('EGAP_CTFR5_Ques', 'EGAP_IQ_Ques_4')
	elif LOB == "HCP":
		Quote.CustomFields.Disallow('EGAP_MFR2_Ques')
	elif LOB == "PMC" or LOB == "CCC":
		Quote.CustomFields.Disallow('EGAP_CTFR5_Ques')
if LOB == "HCP" or (quoteType=='Projects' and (LOB == "LSS" or LOB == "PAS")):
    iOQues19 = Quote.GetCustomField('EGAP_IQ_Ques_19').Content
    iOQues20 = Quote.GetCustomField('EGAP_IQ_Ques_20').Content
    if not iOQues19:
        Quote.GetCustomField('EGAP_IQ_Ques_19').Content="Yes"
        iOQues19="Yes"
    if iOQues19=="Yes" and iOQues20=="":
        Quote.CustomFields.Allow('EGAP_IQ_Ques_20')
        Quote.GetCustomField('EGAP_IQ_Ques_20').Content="No"
    elif iOQues19!="Yes":
        Quote.CustomFields.Disallow('EGAP_IQ_Ques_20')
else:
    Quote.CustomFields.Disallow('EGAP_IQ_Ques_19','EGAP_IQ_Ques_20')
if quoteType in ('Projects','Parts and Spot'):
    if quoteType=='Projects':
        if LOB in("HCP","CCC"):
            Quote.CustomFields.Disallow('EGAP_IQ_Ques_1')
        elif LOB != "HCP":
            Quote.CustomFields.Disallow('EGAP_IQ_Ques_15', 'EGAP_IQ_Ques_16')
    Quote.CustomFields.Disallow('EGAP_IQ_Ques_2', 'EGAP_IQ_Ques_3', 'EGAP_IQ_Ques_4','EGAP_IQ_Ques_17','EGAP_RAFR2_Ques','EGAP_RAFR2_RQUP_Number','EGAP_RAFR2_Ques_Rule','EGAP_RAFR2_RQUP_Number_Rule')
    if LOB in('PAS','LSS','CCC','HCP') and Quote.GetCustomField('EGAP_Proposal_Type').Content == 'Budgetary':
        Quote.CustomFields.Disallow('EGAP_Ques_CR7a','EGAP_Ques_CR3b','EGAP_Ques_CR5a','EGAP_Ques_CR5b','EGAP_Ques_CR6a','EGAP_Ques_CR6b','EGAP_Ques_CR8a','EGAP_Risk_Count_CR8a','EGAP_Ques_CR9a','EGAP_Ques_CR9b','EGAP_CFR1_Ques','EGAP_CFR1_Ques_Rule','EGAP_CFR5_Ques','EGAP_CFR5_Ques_Rule','EGAP_CFR6_Ques','EGAP_CFR6_Ques_Rule','EGAP_CFR4_Ques','EGAP_CFR4_Ques_Rule','EGAP_ETR_Number','EGAP_MFR1_Ques','EGAP_MFR1_Ques_Rule','EGAP_RAFR3_Ques','EGAP_RAFR3_Ques_Rule','EGAP_RAFR4_Ques','EGAP_RAFR4_Ques_Rule','EGAP_RAFR1_Ques_Rule','EGAP_RAFR1_RQUP_Number','EGAP_RAFR1_RQUP_Number_Rule')
        Quote.GetCustomField('EGAP_Ques_CR5a').Content = 'Yes'
        Quote.GetCustomField('EGAP_Ques_CR5b').Content = 'Yes'
        fieldsList = ['EGAP_Ques_CR7a','EGAP_Ques_CR3b','EGAP_Ques_CR6a','EGAP_Ques_CR6b','EGAP_Ques_CR8a','EGAP_Ques_CR9a','EGAP_Ques_CR9b','EGAP_CFR1_Ques','EGAP_CFR5_Ques','EGAP_CFR6_Ques','EGAP_CFR4_Ques','EGAP_MFR1_Ques','EGAP_RAFR3_Ques','EGAP_RAFR4_Ques']
        for field in fieldsList:
            Quote.GetCustomField(field).Content = 'No'
        if LOB == 'PAS':
            Quote.CustomFields.Disallow('EGAP_IQ_Ques_1')
            Quote.CustomFields.Disallow('EGAP_CFR3_Ques','EGAP_CFR3_Ques_Rule')
            Quote.GetCustomField('EGAP_IQ_Ques_1').Content = 'No'
            Quote.GetCustomField('EGAP_CFR3_Ques').Content = 'Yes'
        elif LOB == 'CCC':    
            Quote.CustomFields.Allow('EGAP_CFR2_Ques_Rule','EGAP_RAFR1_Ques_Rule','EGAP_RAFR1_RQUP_Number','EGAP_RAFR1_RQUP_Number_Rule')
            Quote.CustomFields.Disallow('EGAP_CFR3_Ques','EGAP_CFR3_Ques_Rule')
            Quote.GetCustomField('EGAP_CFR3_Ques').Content = 'Yes'
        elif LOB in('HCP'):    
            Quote.CustomFields.Disallow('EGAP_CFR3_Ques','EGAP_CFR3_Ques_Rule')
            Quote.GetCustomField('EGAP_CFR3_Ques').Content = 'Yes'
        if LOB != 'CCC':    
            Quote.CustomFields.Disallow('EGAP_CFR2_Ques','EGAP_CFR2_Ques_Rule','EGAP_RAFR1_Ques')
            Quote.GetCustomField('EGAP_CFR2_Ques').Content = 'No'
            Quote.GetCustomField('EGAP_RAFR1_Ques').Content = 'No'
 
if quoteType in ['Parts and Spot'] and LOB == 'CCC' and Quote.Items.Count>0:
	fieldsList = ['EGAP_Ques_CR1a','EGAP_Ques_CR1b','EGAP_Ques_CR3a','EGAP_Ques_CR3b','EGAP_Ques_CR3c','EGAP_Ques_CR3d','EGAP_Ques_CR4a','EGAP_Ques_CR4b','EGAP_Ques_CR4c','EGAP_Ques_CR5a','EGAP_Ques_CR5b','EGAP_Ques_CR5c','EGAP_Ques_CR6a','EGAP_Ques_CR6b','EGAP_Ques_CR7a','EGAP_Ques_CR8a','EGAP_Ques_CR9a','EGAP_Ques_CR9b','EGAP_IQ_Ques_1','EGAP_IQ_Ques_2','EGAP_IQ_Ques_3','EGAP_IQ_Ques_4','EGAP_CFR1_Ques','EGAP_CFR2_Ques','EGAP_CFR3_Ques','EGAP_CFR4_Ques','EGAP_CFR5_Ques','EGAP_CFR6_Ques','EGAP_MFR1_Ques','EGAP_MFR2_Ques','EGAP_PFR1_Ques','EGAP_RAFR1_Ques','EGAP_RAFR2_Ques','EGAP_RAFR3_Ques','EGAP_RAFR4_Ques','EGAP_RAFR5_Ques','EGAP_CTFR1_Ques','EGAP_CTFR2_Ques','EGAP_CTFR3_Ques','EGAP_CTFR4_Ques','EGAP_CTFR5_Ques','EGAP_CTFR6_Ques','EGAP_CTFR8_Ques','EGAP_CAR_Ques_2','EGAP_CAR_Ques_3','EGAP_CAR_Ques_4','EGAP_CAR_Ques_5','EGAP_CAR_Ques_6','EGAP_CAR_Ques_7','EGAP_CAR_Ques_8','EGAP_CAR_Ques_9','EGAP_CTFR10_Ques','EGAP_CTFR11_Ques','EGAP_CTFR12_Ques']
	for field in fieldsList:
		Quote.GetCustomField(field).Content = 'No'

elif LOB == "HCP" and quoteType in ['Parts and Spot']:
	cTFR1Ques = Quote.GetCustomField('EGAP_CTFR1_Ques').Content
	cFR1Ques  = Quote.GetCustomField('EGAP_CFR1_Ques').Content
	cFR5Ques  = Quote.GetCustomField('EGAP_CFR5_Ques').Content
	cFR6Ques  = Quote.GetCustomField('EGAP_CFR6_Ques').Content
	iOQues15 = Quote.GetCustomField('EGAP_IQ_Ques_15').Content
	questionRAFR1  = Quote.GetCustomField('EGAP_RAFR1_Ques')
	IsApprovalNotRequired = '0'
	Is_Quote_Approval_Exempted = 'No'
	functionalQuest_permission(fieldsList)
	Quote.CustomFields.Disallow('EGAP_ETR_Number')
	Quote.CustomFields.Disallow('EGAP_Ques_CR1a','EGAP_Ques_CR1b','EGAP_Ques_CR3a','EGAP_Ques_CR3b','EGAP_Ques_CR3c','EGAP_Ques_CR3d','EGAP_Ques_CR4a','EGAP_Ques_CR4b','EGAP_Ques_CR4c','EGAP_Ques_CR5a','EGAP_Ques_CR5b','EGAP_Ques_CR5c','EGAP_Ques_CR6a','EGAP_Ques_CR6b','EGAP_Ques_CR7a','EGAP_Ques_CR8a','EGAP_Ques_CR9a','EGAP_Ques_CR9b','EGAP_IQ_Ques_1','EGAP_IQ_Ques_2','EGAP_IQ_Ques_3','EGAP_IQ_Ques_4','EGAP_CFR2_Ques','EGAP_CFR3_Ques','EGAP_CFR4_Ques','EGAP_MFR1_Ques','EGAP_MFR2_Ques','EGAP_PFR1_Ques','EGAP_RAFR2_Ques','EGAP_RAFR3_Ques','EGAP_RAFR4_Ques','EGAP_RAFR5_Ques','EGAP_CTFR2_Ques','EGAP_CTFR3_Ques','EGAP_CTFR4_Ques','EGAP_CTFR5_Ques','EGAP_CTFR6_Ques','EGAP_CTFR7_Ques','EGAP_CTFR8_Ques','EGAP_CAR_Ques_1','EGAP_CAR_Ques_2','EGAP_CAR_Ques_3','EGAP_CAR_Ques_4','EGAP_CAR_Ques_5','EGAP_CAR_Ques_6','EGAP_CAR_Ques_7','EGAP_CAR_Ques_8','EGAP_CAR_Ques_9','EGAP_CTFR10_Ques','EGAP_CTFR11_Ques','EGAP_CTFR12_Ques','EGAP_IQ_Ques_16','EGAP_IQ_Ques_17','EGAP_RAFR2_RQUP_Number')
	isMPAApplied = Quote.GetCustomField('MPA Price Plan').Content.strip()
	if Quote.Items.Count > 0 :
		quoteDetails    = Quote.QuoteTables["Quote_Details"].Rows[0]
		sellPrice = quoteDetails['Quote_Sell_Price']
		negotiationLimit = quoteDetails['Negotiation_Limit']
		walkAwaySellPrice = sellPrice - negotiationLimit
		transferPrice = quoteDetails['Quote_Regional_Cost']
		regionalMargin = walkAwaySellPrice - transferPrice
		quoteDiscountPercent = quoteDetails['Quote_Discount_Percent']
		regionalMarginPercent = 0
		BGPzeroQuantity = check_swbgp(Quote)
		if walkAwaySellPrice >0:
			regionalMarginPercent = (regionalMargin/walkAwaySellPrice)*100
		if cTFR1Ques == 'No' and questionRAFR1.Content == 'No' and cFR1Ques == 'No' and cFR5Ques == 'No' and cFR6Ques == 'No' and iOQues15 == 'No' and isMPAApplied!= '' and BGPzeroQuantity!= 'false' and int(quoteDiscountPercent) <= 0 and ((Quote.GetCustomField('Is Payment milestones are negatively deviating from standard milestone?').Content == 'No' and Quote.GetCustomField('Payment Milestones as per Standard/MPA?').Content == 'No') or (Quote.GetCustomField('Payment Milestones as per Standard/MPA?').Content == 'Yes')):
			IsApprovalNotRequired = '1'
			Is_Quote_Approval_Exempted = 'Yes'
			Quote.GetCustomField('EGAP_Highest_Price_Margin_Approval_Level').Content = "No Approval"
		# Trace.Write('Is_Quote_Approval_Exempted------'+str(Is_Quote_Approval_Exempted))

		Quote.GetCustomField('IsApprovalNotRequired').Content = IsApprovalNotRequired
		Quote.GetCustomField('IsApprovalNotRequired_FQ').Content = IsApprovalNotRequired
		Quote.GetCustomField('Is_Quote_Approval_Exempted').Content = Is_Quote_Approval_Exempted
if  Quote.GetGlobal('msgshow')=='True' and Quote.GetCustomField("R2QFlag").Content != "No":
	Quote.GetCustomField("Is_Quote_Approval_Exempted").Content = "Yes"

# Fetch field values
Milestones = Quote.GetCustomField('Payment Milestones').Content
LOB = Quote.GetCustomField('Booking LOB').Content
Q_Type = Quote.GetCustomField('Quote Type').Content
RAFR2 = Quote.GetCustomField('EGAP_RAFR2_Ques').Content
RAFR1 = Quote.GetCustomField('EGAP_RAFR1_Ques').Content
CTFR1 = Quote.GetCustomField('EGAP_CTFR1_Ques').Content
CFR1 = Quote.GetCustomField('EGAP_CFR1_Ques').Content
CFR5 = Quote.GetCustomField('EGAP_CFR5_Ques').Content
CFR6 = Quote.GetCustomField('EGAP_CFR6_Ques').Content
totalDiscount = Quote.GetCustomField('Total Discount Percent').Content
MPAPricePlan = Quote.GetCustomField('MPA Price Plan').Content
agreementType = Quote.GetCustomField('Agreement Type').Content
MPA = Quote.GetCustomField('MPA Commercial').Content
BusinessModel = Quote.GetCustomField('Business Model').Content
isCompetitive = Quote.GetCustomField('EGAP_IQ_Ques_18').Content

Flags = [RAFR2, RAFR1, CTFR1, CFR1, CFR5, CFR6]
mpaQuery2 = SqlHelper.GetFirst("SELECT * FROM MPA_PRICE_PLAN_MAPPING WHERE Price_Plan_Name = '{0}' AND Agreement_Name = '{1}' AND Agreement_Type = '{2}'".format(MPAPricePlan, MPA, agreementType))
Quote.GetCustomField("Is_Quote_Approval_Exempted_due_to_MPA").Content = "No"
if (float(totalDiscount) == 0 and all(flag != 'Yes' for flag in Flags) and Milestones == 'As per MPA' and agreementType == 'Master Purchase Agreement') and negotiationLimit==0 and ((LOB == 'LSS' and Q_Type in ['Projects', 'Contract New', 'Contract Renewal'] ) or (LOB == 'PAS' and Q_Type == 'Projects' and BusinessModel != 'New Construction/ Greenfield'and isCompetitive =='No')):
		Quote.GetCustomField("Is_Quote_Approval_Exempted_due_to_MPA").Content = "Yes"
'''
if Quote.GetCustomField("Is_Quote_Approval_Exempted_due_to_MPA").Content == "Yes" and LOB == 'LSS':
    Quote.GetCustomField("EGAP_Highest_Approval_Level_for_the_Quote").Content = "0"
elif Quote.GetCustomField("Is_Quote_Approval_Exempted_due_to_MPA").Content == "Yes" and LOB == 'PAS':
    Quote.GetCustomField("EGAP_Highest_Approval_Level_for_the_Quote").Content = "2"
'''