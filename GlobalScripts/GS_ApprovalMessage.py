if Session["prevent_execution"] != "true":
	import GS_CommonModule as CM
	from GS_PMCMatrixNameUtil import PMC_MatrixName, PMC_PaymentMilestoneMessageLogic
	def removeMessages(Quote, proposalType='', oldMessage=''):
		if proposalType == 'Parts & Spots':
			Quote.Messages.Clear()
		else:
			approvalLevels = range(7)
			for level in approvalLevels:
				Message = 'This quote requires L{} approval. Please click on "Request Approval" action to proceed further.'.format(level)
				#Trace.Write("Delete:{}".format(Message))
				Quote.Messages.Remove(Message)
			Quote.Messages.Remove('This Quote requires approval from all approvers as per the Approver Table.')
			Quote.Messages.Remove("This quote does not require approval as per approval exemption criteria.")
			if proposalType == 'Booking':
				Quote.Messages.Remove('This Quote requires only Booking Gatekeeper approval')
				Quote.Messages.Remove('Quote does not require approval as per approval exemption criteria however Booking Gate Keeper approval is required for this quote.')

	'''def Quotemessage(Quote):
		x = []
		if Quote.GetCustomField('Quote Type').Content in ["Parts and Spot", "Projects"]:
			for i in Quote.MainItems:
				txt = str(i.QI_SalesText.Value.encode("ascii", "replace").replace('?', '')).strip()
				if txt:
					x.append(txt)
		if len(x) and not (Quote.Messages.Contains('Your Quote has ERP texts in one or more-line items. Please check before submitting for approval')):
			Trace.Write('value++++++++++++++++'+str(x))
			Quote.Messages.Add(
				'Your Quote has ERP texts in one or more-line items. Please check before submitting for approval')''' #Performance Improvement by suriya

	quoteType = CM.getCFValue(Quote, "Quote Type")
	Entitlement=CM.getCFValue(Quote, "Entitlement")
	LOB       = CM.getCFValue(Quote, "Booking LOB")
	exchangeRate    = CM.getCFValue(Quote, "Exchange Rate")
	otherCondition = {'Max_Approval_Level':'None', 'Booking_Gatekepper':'', 'EGAP_Approvers': 0}
	isApprovalRequired = 0
	if Quote.OrderStatus.Name == "Preparing" and Quote.Items.Count > 0 and LOB in ['LSS', 'PAS', 'CCC','HCP']:
		if CM.getCFValue(Quote,"CF_MaxApprovalLevel")=='':
			ScriptExecutor.Execute('GS_ApprovalTabContent', {"Approval": "getstatus"})
		Trace.Write('--expemt-'+Quote.GetCustomField("Is_Quote_Approval_Exempted").Content)
		level = CM.getCFValue(Quote, 'CF_MaxApprovalLevel')
		quoteDetails = Quote.QuoteTables["Quote_Details"]
		if quoteDetails.Rows.Count > 0:
			row = quoteDetails.Rows[0]
			sellPrice       = row["Quote_Sell_Price_Incl_Tariff"] / float(exchangeRate)
			discount        = row["Quote_Discount_Percent"]
			if (quoteType in ('Projects','Contract New','Contract Renewal')) or (quoteType == 'Parts and Spot' and LOB == 'CCC') or (LOB == 'HCP'):
				isApprovalRequired = TagParserQuote.ParseString("[AND]([NEQ](<*CTX( Quote.CustomField(IsApprovalNotRequired) )*>,1), [OR]([NEQ](<*CTX( Quote.CustomField(CF_MaxApprovalLevel) )*>,),[GT](<* TABLE ( SELECT count(*) FROM QT__EGAP_Approvers WHERE cartid = '<*CTX( Quote.CartId )*>' and ownerid = '<*CTX( Quote.OwnerId )*>') *>,0)),[NEQ](<*CTX(Quote.CustomField(EGAP_Highest_Price_Margin_Approval_Level))*>,No Approval))")
				if (quoteType in ('Contract New', 'Contract Renewal')) and LOB == 'LSS':
					Quote.GetCustomField(
						'EGAP_Highest_Price_Margin_Approval_Level').Content = level
				elif LOB == 'HCP' and Quote.GetCustomField("Is_Quote_Approval_Exempted").Content == "Yes":
					isApprovalRequired = 0
					# Quote.GetCustomField('EGAP_Highest_Price_Margin_Approval_Level').Content = "No Approval"
					Quote.GetCustomField('EGAP_Highest_Approval_Level_for_the_Quote').Content =  "No Approval"
				sellPrice       = row["Walk_away_Sales_Price"] / float(exchangeRate)
				quoteWTWCost = row['Quote_WTW_Cost'] / float(exchangeRate)
				wtwMargin = sellPrice - quoteWTWCost
				discount = round((wtwMargin/sellPrice)*100,2) if sellPrice > 0 else 0
				cf_proposalType = CM.getCFValue(Quote, "EGAP_Proposal_Type")
				proposalType = cf_proposalType
				limitType = "Wall-to-Wall Margin"
				if cf_proposalType in ['Firm', 'Booking']:
					proposalType = 'Firm & Booking'
				quoteTableApprovers = Quote.QuoteTables['EGAP_Approvers']
				if quoteTableApprovers.Rows.Count > 0:
					otherCondition['EGAP_Approvers'] = quoteTableApprovers.Rows.Count
			else:
				proposalType = "Parts & Spots"
				limitType = "Discount"
				cf_proposalType = proposalType
			bookingCountry = CM.getCFValue(Quote,"Booking Country")
			sfdcquotetype  = CM.getCFValue(Quote,"SFDC_Quote_Type")
			Approval_Level  = CM.GetApprovalLevel(quoteType, LOB, sellPrice, discount, proposalType, limitType,bookingCountry,sfdcquotetype)
			if Approval_Level and Approval_Level.ApprovalLevel:
				level = "L{}".format(Approval_Level.ApprovalLevel)
				if proposalType == "Parts & Spots" or (quoteType == 'Parts and Spot' and LOB == 'HCP'):
					'''New Approval Message'''
					otherCondition['Max_Approval_Level'] = level
					CM.setCFValue(Quote, "CF_MaxApprovalLevel", level)
				else:
					if Approval_Level.ApprovalLevel in ['No P&M Approval', 'Functional Approvals Only', 'No Approval']:
						CM.setCFValue(Quote, "EGAP_No_eGap", "No eGap")
					else:
						CM.setCFValue(Quote, "EGAP_No_eGap", "")
						CM.setCFValue(Quote, "CF_MaxApprovalLevel", Approval_Level.ApprovalLevel)
						otherCondition['Max_Approval_Level'] = Approval_Level.ApprovalLevel
			if cf_proposalType == 'Booking' and quoteTableApprovers.Rows.Count > 0:
				otherCondition['Booking_Gatekepper'] = False
				cf_bookingQuoteApprovalRequirement = CM.getCFValue(Quote, "EGAP_Booking_Quote_Approval_Requirement")
				query = "Select EGAP_Reason from QT__EGAP_Approvers where ownerid={} and cartid={} and  EGAP_Approver_Title='{}'".format(Quote.UserId,Quote.QuoteId, 'Booking Gatekeeper')
				qtResult = SqlHelper.GetFirst(query)
				gatekeeperMessages = ['This Quote requires only Booking Gatekeeper approval', 'Quote does not require approval as per approval exemption criteria however Booking Gate Keeper approval is required for this quote.']
				if qtResult is not None:
					if qtResult.EGAP_Reason in gatekeeperMessages:
						otherCondition['Booking_Gatekepper'] = True
						otherCondition['Max_Approval_Level'] = 'None'
				if cf_bookingQuoteApprovalRequirement in gatekeeperMessages:
					otherCondition['Booking_Gatekepper'] = True
					otherCondition['Max_Approval_Level'] = 'None'
			level = ''
			query = "Select Quote_Type, LOB, Proposal_Type, EGAP_Approvers, Other_Condition, Message from Approval_Message Where Quote_Type='{}' and LOB='{}' and Proposal_Type='{}'"
			res = SqlHelper.GetList(query.format(quoteType, LOB, cf_proposalType))
			if len(res) > 0:
				if quoteType == 'Parts and Spot':
					level = CM.getCFValue(Quote , 'CF_MaxApprovalLevel') if LOB !='HCP' else CM.getCFValue(Quote , 'EGAP_Highest_Approval_Level_for_the_Quote')
					if level.strip() != '':
						level = "L{}".format(level) if level[0] != 'L' else level
					oldMessage = Translation.Get("ApprovalEscalation.Notification").format(level)
					removeMessages(Quote, proposalType, oldMessage)
				else:
					level = CM.getCFValue(Quote , 'EGAP_Highest_Approval_Level_for_the_Quote')
					if level.strip() != '':
						level = "L{}".format(level) if level[0] != 'L' else level
					removeMessages(Quote, cf_proposalType)

			proposalType = Quote.GetCustomField('EGAP_Proposal_Type').Content if Quote.GetCustomField('EGAP_Proposal_Type').Content.strip() !='' else ''
			
			if int(isApprovalRequired) == 0 and len(res) > 0 and quoteType == 'Projects':
				msg = "This quote does not require approval as per approval exemption criteria."
				if proposalType == 'Booking':
					msg = "This quote does not require approval as per approval exemption criteria however Booking Gate Keeper approval is required for this quote."
				# elif LOB == 'CCC' and float(Quote.QuoteTables["Quote_Details"].Rows[0]["Quote_Discount_Percent"]) in(0,0.0):
					# Quote.GetCustomField('EGAP_Highest_Price_Margin_Approval_Level').Content = "No Approval"
					# Quote.GetCustomField('EGAP_Highest_Approval_Level_for_the_Quote').Content = 'Functional Approvals Only' if float(Quote.QuoteTables["EGAP_Approvers"].Rows.Count) > 0 else 'No Approval'
					# msg = 'This quote does not require approval'
				elif LOB == 'HCP' and Quote.QuoteTables["EGAP_Approvers"].Rows.Count == 0:
					# Quote.GetCustomField('EGAP_Highest_Price_Margin_Approval_Level').Content = "No Approval"
					Quote.GetCustomField('EGAP_Highest_Approval_Level_for_the_Quote').Content = 'No Approval'
				else:
					Trace.Write('in no approvals ')
					hpm = Quote.GetCustomField('EGAP_Highest_Price_Margin_Approval_Level').Content
					level = 0 if CM.getCFValue(Quote , 'CF_MaxApprovalLevel') == 'No Approval' else CM.getCFValue(Quote , 'CF_MaxApprovalLevel')
					if int(level) > 0 and Quote.GetCustomField('Is_Quote_Approval_Exempted').Content != 'Yes':
						Quote.GetCustomField('EGAP_Highest_Approval_Level_for_the_Quote').Content = level
						Quote.GetCustomField('EGAP_Highest_Price_Margin_Approval_Level').Content = level
					elif int(level) > 0 and Quote.GetCustomField('Is_Quote_Approval_Exempted').Content == 'Yes':
						Quote.GetCustomField('EGAP_Highest_Approval_Level_for_the_Quote').Content = 'No Approval'
						Quote.GetCustomField('EGAP_Highest_Price_Margin_Approval_Level').Content = level
					else:
						Quote.GetCustomField('EGAP_Highest_Price_Margin_Approval_Level').Content = 'Functional Approvals Only' if float(Quote.QuoteTables["EGAP_Approvers"].Rows.Count) > 0 else 'No Approval'
						Quote.GetCustomField('EGAP_Highest_Approval_Level_for_the_Quote').Content = 'Functional Approvals Only' if float(Quote.QuoteTables["EGAP_Approvers"].Rows.Count) > 0 else 'No Approval'
					if LOB == "HCP" and hpm != '' and str(hpm) != 'Functional Approvals Only':
						Quote.GetCustomField('EGAP_Highest_Price_Margin_Approval_Level').Content = hpm
				if not Quote.Messages.Contains(msg):
					Quote.Messages.Add(msg)
			elif LOB == "HCP" and int(isApprovalRequired) == 0 and len(res) > 0 and quoteType == 'Parts and Spot':
				msg = "This quote does not require approval as per approval exemption criteria."
				if proposalType == 'Booking':
					msg = "This quote does not require approval as per approval exemption criteria however Booking Gate Keeper approval is required for this quote."
				else:
					Trace.Write('in no approvals p&s ')
					hpm = Quote.GetCustomField('EGAP_Highest_Price_Margin_Approval_Level').Content
					Quote.GetCustomField('EGAP_Highest_Price_Margin_Approval_Level').Content = 'Functional Approvals Only' if float(Quote.QuoteTables["EGAP_Approvers"].Rows.Count) > 0 else 'No Approval'
					Quote.GetCustomField('EGAP_Highest_Approval_Level_for_the_Quote').Content = 'Functional Approvals Only' if float(Quote.QuoteTables["EGAP_Approvers"].Rows.Count) > 0 else 'No Approval'
					if hpm != '' and str(hpm) != 'Functional Approvals Only':
						Quote.GetCustomField('EGAP_Highest_Price_Margin_Approval_Level').Content = hpm
				if not Quote.Messages.Contains(msg):
					Quote.Messages.Add(msg)
			else:
				for row in res:
					Message  = ''
					value    = ''
					operator = ''
					if row.Other_Condition != '':
						key, value , operator = row.Other_Condition.split(',')
						dictValue = otherCondition.get(key, '')
					if row.Proposal_Type  == 'Parts & Spots':
						if operator == '!=' :
							if dictValue != value and level != '':
								Message = row.Message.format(level)
					elif cf_proposalType == row.Proposal_Type  and  row.EGAP_Approvers == 'FALSE':
						if value == 'False':
							value = False
						elif value == 'True':
							value = True
						if operator == '==' :
							if dictValue == value:
								Message = row.Message
						elif operator == '!=' :
							if dictValue != value and level != '':
								Message = row.Message.format(level)
					elif cf_proposalType == row.Proposal_Type  and  row.EGAP_Approvers == 'TRUE':
						dictValue = otherCondition.get('EGAP_Approvers', 0)
						if dictValue > 0:
							priceMarginApprovalLevel = CM.getCFValue(Quote , 'EGAP_Highest_Price_Margin_Approval_Level')
							if priceMarginApprovalLevel != 'No Approval':
								Message = row.Message
								Trace.Write("Hema Executed")
					if not Quote.Messages.Contains(Message) and Message != '' and 'No Approval' not in Message:
						Trace.Write("kash Executed")
						Quote.Messages.Add(Message)
		if not Quote.Messages.Contains('Your Quote may have ERP texts in one or more-line items. Please check before submitting for approval') and (quoteType not in ('Contract New', 'Contract Renewal') and LOB == 'LSS'):
			Quote.Messages.Add("Your Quote may have ERP texts in one or more-line items. Please check before submitting for approval")
		
		if Quote.ContainsAnyProductByPartNumber("Migration") and quoteType == "Projects" and LOB in ['LSS', 'PAS', 'CCC','HCP'] and Entitlement not in ['None','']:
			if not Quote.Messages.Contains("Check  SESP entitlement validity as SESP pricing is applied on the quote"):
				Quote.Messages.Add("Check  SESP entitlement validity as SESP pricing is applied on the quote")
		elif Quote.Messages.Contains("Check  SESP entitlement validity as SESP pricing is applied on the quote"):
			Quote.Messages.Remove("Check  SESP entitlement validity as SESP pricing is applied on the quote")

	
	# PMC Approval Message Update Logic ------> H542830 (start) '''
	if Quote.OrderStatus.Name == "Preparing" and LOB == 'PMC' and quoteType in ['Projects','Parts and Spot']:
		for msg in Quote.Messages:
			if msg.Contains("This quote requires Level"):
				Quote.Messages.Remove(str(msg))
				break
		LimitType = "Discount"
		BookingCountry = ""
		TSP = UserPersonalizationHelper.ConvertToNumber(Quote.GetCustomField("Total Sell Price").Content)
		# CXCPQ-80277 --- Start
		ListPrice_Discount_check = False
		for item in Quote.Items:
			if item['QI_Additional_Discount_Percent'].Value > 0:
				ListPrice_Discount_check = True
				break

		#QLP = float(TagParserQuote.ParseString("<* GetFirstFromQuoteTable( Quote_Details, Quote_List_Price) *>"))
		#QSP = float(TagParserQuote.ParseString("<* GetFirstFromQuoteTable( Quote_Details, Quote_Sell_Price) *>"))
		#QSP = QSP - float(TagParserQuote.ParseString("<* GetFirstFromQuoteTable( Quote_Details, GAS_ETO_Price) *>"))
		quoteDetails = Quote.QuoteTables["Quote_Details"]
		row = quoteDetails.Rows[0]
		QLP = float(row["Quote_List_Price"])
		QSP = float(row["Quote_Sell_Price"]) - float(row["GAS_ETO_Price"])
		if QLP > 0 and ListPrice_Discount_check:
			TDP = UserPersonalizationHelper.ConvertToNumber(str(((QLP - QSP) / QLP) * 100))
		else:
			TDP = 0
		# CXCPQ-80277 --- END

		exchangeRate = Quote.GetCustomField("Exchange Rate").Content
		TSP_USD = TSP / float(exchangeRate)

		MatrixName = PMC_MatrixName(Quote)

		SqlMessageLst = "SELECT Distinct Message FROM SEA_APPROVAL_DISCOUNT_MATRIX WHERE LOB = 'PMC' AND Message <> ''"
		Messages = SqlHelper.GetList(SqlMessageLst)
		for i in Messages:
			Quote.Messages.Remove(i.Message)

		if MatrixName:
			PMCApprovalMatrixName = MatrixName.PMCMatrixName
			if TDP > 0.01:
				if (Quote.GetCustomField("Booking Country").Content).lower() == "india":
					BookingCountry = 'india'
					SqlQuery2 = "SELECT TOP 1000 ApprovalLevel, Message FROM SEA_APPROVAL_DISCOUNT_MATRIX WHERE LOB = '{0}' AND LimitType = '{1}' AND BookingCountry = '{2}' AND PMCMatrixName = '{3}' AND CAST(MinimumSellPrice as int) <= {4} AND CAST(MaximumSellPrice as int) > {4} AND CAST(MinimumLimit as float) < {5} AND CAST(MaximumLimit as float) >= {5}".format(LOB,LimitType,BookingCountry,PMCApprovalMatrixName,TSP_USD,TDP)
				else:
					BookingCountry = ''
					SqlQuery2 = "SELECT TOP 1000 ApprovalLevel, Message FROM SEA_APPROVAL_DISCOUNT_MATRIX WHERE LOB = '{0}' AND LimitType = '{1}' AND (BookingCountry = '{2}' OR BookingCountry Is null) AND PMCMatrixName = '{3}' AND CAST(MinimumSellPrice as int) <= {4} AND CAST(MaximumSellPrice as int) > {4} AND CAST(MinimumLimit as float) < {5} AND CAST(MaximumLimit as float) >= {5}".format(LOB,LimitType,BookingCountry,PMCApprovalMatrixName,TSP_USD,TDP)
			else:
				if (Quote.GetCustomField("Booking Country").Content).lower() == "india":
					BookingCountry = 'india'
					SqlQuery2 = "SELECT TOP 1000 ApprovalLevel, Message FROM SEA_APPROVAL_DISCOUNT_MATRIX WHERE LOB = '{0}' AND LimitType = '{1}' AND BookingCountry = '{2}' AND PMCMatrixName = '{3}' AND CAST(MinimumSellPrice as int) <= {4} AND CAST(MaximumSellPrice as int) > {4} AND CAST(MinimumLimit as float) = {5}".format(LOB,LimitType,BookingCountry,PMCApprovalMatrixName,TSP_USD,TDP)
				else:
					BookingCountry = ''
					SqlQuery2 = "SELECT TOP 1000 ApprovalLevel, Message FROM SEA_APPROVAL_DISCOUNT_MATRIX WHERE LOB = '{0}' AND LimitType = '{1}' AND (BookingCountry = '{2}' OR BookingCountry Is null) AND PMCMatrixName = '{3}' AND CAST(MinimumSellPrice as int) <= {4} AND CAST(MaximumSellPrice as int) > {4} AND CAST(MinimumLimit as float) = {5}".format(LOB,LimitType,BookingCountry,PMCApprovalMatrixName,TSP_USD,TDP)
				
			ApprovalLevel = SqlHelper.GetFirst(SqlQuery2)

			isApprovalLevelNA = ''
			ApprovalMessage = ''
			if ApprovalLevel:
				isApprovalLevelNA = ApprovalLevel.ApprovalLevel
				ApprovalMessage = ApprovalLevel.Message
			if isApprovalLevelNA == 'NA':
				Quote.Messages.Add(ApprovalMessage)
			Approvalrequired = Quote.GetCustomField("EGAP_Highest_Approval_Level_for_the_Quote").Content
			allapprovalLevels = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0C', '1C', '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C']
			allapprovalLevels.append('NA')
			allapprovalLevels.append('')
			for level in allapprovalLevels:
				Message = 'This quote requires Level {} approval. Please click on "Request Approval" action to proceed further.'.format(level)
				Quote.Messages.Remove(Message)
				Message = 'This quote requires Level {} approval because Advanced Payment is < 10% or Advanced Payment is not included in the Payment Milestones or Milestone as "Exclude”.'.format(level)
				Quote.Messages.Remove(Message)
			PMC_PaymentMilestoneMessageLogic(Quote,TSP_USD,Approvalrequired)
			dyn_msg = "This quote requires Level {} approval. Please click on "Request Approval" action to proceed further.".format(Approvalrequired)
			if Quote.GetCustomField("EGAP_Highest_Approval_Level_for_the_Quote").Content != '' and Quote.GetCustomField("EGAP_Highest_Approval_Level_for_the_Quote").Content != 'NA' and Quote.GetCustomField("EGAP_Highest_Approval_Level_for_the_Quote").Content != '0':
				Quote.Messages.Add(dyn_msg)   #------> H542830 (start)

if Quote.GetCustomField('Quote Type').Content=="Projects":
	x=TagParserQuote.ParseString('<*CTX( Quote.HasIncompleteItems )*>')
	if x=="1" and not (Quote.Messages.Contains('one or more configuration is Incomplete, Estimator to revisit & complete the configuration')):
		Quote.Messages.Add("one or more configuration is Incomplete, Estimator to revisit & complete the configuration")
from GS_CommonConfig import CL_CommonSettings as CS
if Quote.Items.Count == 0:
    Quote.Messages.Clear()
elif Quote.Items.Count > 0 and CS.RQUP_Dict["Modules"]=='':
    Quote.Messages.Remove(Translation.Get('message.UnreleasedProductRestriction').format(str(Quote.GetCustomField("RQUP_partList").Content)))
    #Quote.Messages.Remove('This Quote contains Unreleased Product (ELCN). User should answer the RQUP question RAFR1 as "Yes" in the functional review question tab.')

#Added by Ravika-CXCPQ-106059
AccId=Quote.GetCustomField("AccountId").Content
SFDC_URL= 'https://honeywellprocess.lightning.force.com'
API_URL='/lightning/r/Report/00OHs00000EiICxMAN/view?fv0={} target="_blank"> Generate Entitlement Report'.format(AccId)
URL='<a href='+SFDC_URL+API_URL+'</a>'
Quote.GetCustomField("Entitlement Report").Content = URL
Quote.RefreshActions()