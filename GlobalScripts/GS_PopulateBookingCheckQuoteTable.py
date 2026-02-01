import math
exchangeRate    = Quote.GetCustomField('Exchange Rate').Content if Quote.GetCustomField('Exchange Rate').Content.strip() != '' else 1
quoteDetails = Quote.QuoteTables["Quote_Details"]
bookingCheck = Quote.QuoteTables["EGAP_Booking_Check"]
if quoteDetails.Rows.Count:
	row = quoteDetails.Rows[0]
	CFQ  = Quote.GetCustomField('EGAP_Cash_Flow_Quality').Content.replace('%','') if Quote.GetCustomField('EGAP_Cash_Flow_Quality').Content.strip() != '' else 0.0
	CFQ = float(CFQ)
	strCFQ  = "{}%".format(CFQ)
	sellPriceLocal  = row["Quote_Sell_Price_Incl_Tariff"]
	sellPriceUSD    = sellPriceLocal/float(exchangeRate)
	regionalMarginPercent  = row["Quote_Regional_Margin_Percent"]
	wTWMarginPercent       = row["Quote_WTW_Margin_Percent"]
	cf_proposal_Type = Quote.GetCustomField('EGAP_Proposal_Type')
	cf_parentFirmRevision = Quote.GetCustomField('Parent Firm Revision')
	netCheck = 0
	cf_bookingQuoteApprovalRequirement = Quote.GetCustomField('EGAP_Booking_Quote_Approval_Requirement')
	cf_isBookingGateKeeperApprovalRequired = Quote.GetCustomField('EGAP_IS_BookingGateKeeperApprovalRequired')
	cf_doWanttoChanageAnsofFuncQues = Quote.GetCustomField('EGAP_Do_Want_to_Chanage_Ans_of_Func_Ques')
	#Start - Changes added for Defect-CXCPQ-56944 By Leo
	negotiationLimit = row['Negotiation_Limit']
	sellPriceLocal_book  = row["Quote_Sell_Price_Incl_Tariff"]-row['Negotiation_Limit']
	sellPriceUSD_book = row["Quote_Sell_Price_Incl_Tariff"]-row['Negotiation_Limit']
	margin_percent =sellPriceLocal_book- row['Quote_Regional_Cost']
	quoteWTWCost = row['Quote_WTW_Cost']
	regionalMarginPercent = wtwMarginPercentage = 0
	wtwMargin = sellPriceLocal_book - quoteWTWCost
	if sellPriceLocal_book >0:
		regionalMarginPercent = (margin_percent/sellPriceLocal_book)*100
		wtwMarginPercentage = (wtwMargin/sellPriceLocal_book)*100
	exchangeRate    = float(Quote.GetCustomField('Exchange Rate').Content) if Quote.GetCustomField('Exchange Rate').Content else 0.0
	#End - Changes added for Defect-CXCPQ-56944 By Leo

	#Start - Changes added for Defect CXCPQ-45492 By Ashokkumar
                                                                                                                                                     
	IS_PARENT_REVISION_APPROVED = Quote.GetCustomField('IS_PARENT_REVISION_APPROVED').Content if Quote.GetCustomField("IS_PARENT_REVISION_APPROVED") is not None else ''
	#End - Changes added for Defect CXCPQ-45492 By Ashokkumar

	if cf_doWanttoChanageAnsofFuncQues.Content.strip() == '':
		cf_doWanttoChanageAnsofFuncQues.Content = 'No'
	if Quote.OrderStatus.Name in ['Approved', 'Submitted to Customer'] and cf_proposal_Type.Content == 'Firm':
		if bookingCheck.Rows.Count > 0:
			for row in bookingCheck.Rows:
				if row["Field_Details"] == "CFQ":
					row["Approved_Firm_Quote"] = strCFQ
				elif row["Field_Details"] == "Sales Price (USD)":
					row["Approved_Firm_Quote"] = round(sellPriceUSD_book/exchangeRate,2)
				elif row["Field_Details"] == "Sales Price (Local)":
					row["Approved_Firm_Quote"] = round(sellPriceLocal_book,2)
                                                                                  
                                                                           
				elif row["Field_Details"] == "Regional Margin %":
					row["Approved_Firm_Quote"] = "{}%".format(round(regionalMarginPercent,2))
				elif row["Field_Details"] == "WTW Margin %":
					row["Approved_Firm_Quote"] = "{}%".format(round(wtwMarginPercentage,2))
				elif row["Field_Details"] == "Functional Questions":
					row["Approved_Firm_Quote"] = 'NA'
		else:
			data = [{"Field_Details":"CFQ","Approved_Firm_Quote":strCFQ,"Rule_Description":"Cash Flow Quality (CFQ) percentage remains the same or increases by any amount, and"},{"Field_Details":"Sales Price (USD)","Approved_Firm_Quote":round(sellPriceUSD,2),"Rule_Description":"Sales Price in US Dollars remains the same or increases by any amount or decreases by no more than 5%, and"},{"Field_Details":"Sales Price (Local)","Approved_Firm_Quote":round(sellPriceLocal,2),"Rule_Description":"Sales Price in local currency remains the same or increases by any amount, and"},{"Field_Details":"Regional Margin %","Approved_Firm_Quote":"{}%".format(round(regionalMarginPercent,2)),"Rule_Description":"Regional Margin % remains the same or increases by any amount or decreases by no more than 3%, and"},{"Field_Details":"WTW Margin %","Approved_Firm_Quote":"{}%".format(round(wTWMarginPercent,2)),"Rule_Description":"WTW Margin % remains the same or increases by any amount or decreases by no more than 3%, and"},{"Field_Details":"Functional Questions","Approved_Firm_Quote":"NA","Rule_Description":"All answers to Functional Review questions, Cash Risk questions and Controllership questions remains unchanged"}]
			for rec in data:
				row = bookingCheck.AddNewRow()
				for field, val in rec.items():
					row[field] = val
	elif IS_PARENT_REVISION_APPROVED == 'Yes' and cf_parentFirmRevision.Content != '' and cf_proposal_Type.Content == 'Booking':
		cf_IsBookingCheckVisible = Quote.GetCustomField('EGAP_IS_Booking_Check_Visible')
		cf_IsBookingCheckVisible.Content = 'Yes'
		Quote.GetCustomField("Parent Firm Revision").Visible = True
		Quote.GetCustomField("EGAP_Do_Want_to_Chanage_Ans_of_Func_Ques").Visible = True
		Quote.GetCustomField("Parent Firm Revision").Editable = False
		Quote.Save(False) # don't remove Save "custom filed save is required".
		if bookingCheck.Rows.Count > 0:
			data = [{"Field_Details":"CFQ"},{"Field_Details":"Sales Price (USD)"},{"Field_Details":"Sales Price (Local)"},{"Field_Details":"Regional Margin %"},{"Field_Details":"WTW Margin %"},{"Field_Details":"Functional Questions"}]
			url = RequestContext.Url.Host
			domain = TagParserQuote.ParseString('<*DOMAIN*>')
			green = "<img src='https://{}/mt/{}/images/highMarginPicture.gif' title='Green'>".format(url,domain)
			red = "<img src='https://{}/mt/{}/images/lowMarginPicture.gif' title='Red'>".format(url,domain)
			for row in bookingCheck.Rows:
				if row["Field_Details"] == "CFQ":
					row["Booking_Quote_Updates"] = strCFQ
					firmQuoteCFQ = row["Approved_Firm_Quote"].replace('%','')
					firmQuoteCFQ = float(firmQuoteCFQ)/100
					if firmQuoteCFQ >= 0:
						roundUpValue = round(CFQ/100,4)
						roundDownValue = round(firmQuoteCFQ,4)
						diff = roundUpValue - roundDownValue
					else:
						roundDownValue = round(CFQ/100,4)
						roundUpValue = round(firmQuoteCFQ,4)
						diff = roundDownValue - roundUpValue
					diff *= 100
					row["Difference"] = str("{}%".format(round(diff,2)))
					row["Check"] = red
					if round(diff,4) >= 0:
						row["Check"] = green
						netCheck += 1
				elif row["Field_Details"] == "Sales Price (USD)":
					firmSellPriceUSD = float(row["Approved_Firm_Quote"])
					sellPriceUSD = round(sellPriceUSD_book,2)
					row["Booking_Quote_Updates"] = round(sellPriceUSD / exchangeRate,2)
					if firmSellPriceUSD >0:
						diff = (((sellPriceUSD/ exchangeRate)/firmSellPriceUSD) - 1)*100
					diff = (((sellPriceUSD/ exchangeRate)/firmSellPriceUSD) - 1)*100
					row["Difference"] = str("{}%".format(round(diff,2)))
					row["Check"] = red
					if diff > -5:
						row["Check"] = green
						netCheck += 1
				elif row["Field_Details"] == "Sales Price (Local)":
					firmSellPriceLocal = float(row["Approved_Firm_Quote"])
					sellPriceLocal = round(sellPriceLocal_book,2)
					row["Booking_Quote_Updates"] = sellPriceLocal
					diff = sellPriceLocal - firmSellPriceLocal
					row["Difference"] = str(round(diff))
					row["Check"] = red
					if diff>=0:
						row["Check"] = green
						netCheck += 1
				elif row["Field_Details"] == "Regional Margin %":
					firmRegionalMarginPercent = float(row["Approved_Firm_Quote"].replace('%',''))
					regionalMarginPercent = round(regionalMarginPercent,2)
					row["Booking_Quote_Updates"] = "{}%".format(regionalMarginPercent)
					diff = regionalMarginPercent - firmRegionalMarginPercent
					row["Difference"] = str("{}%".format(round(diff,2)))
					row["Check"] = red
					if diff > -3:
						row["Check"] = green
						netCheck += 1
				elif row["Field_Details"] == "WTW Margin %":
					firmwTWMarginPercent = float(row["Approved_Firm_Quote"].replace('%',''))
					wTWMarginPercent = round(wtwMarginPercentage,2)
					row["Booking_Quote_Updates"] = "{}%".format(wTWMarginPercent)
					diff = wTWMarginPercent - firmwTWMarginPercent
					row["Difference"] = str("{}%".format(round(diff,2)))
					row["Check"] = red
					if diff > -3:
						row["Check"] = green
						netCheck += 1
				elif row["Field_Details"] == "Functional Questions":
					row["Booking_Quote_Updates"] = 'No Change'
					row["Difference"] = 'No Change'
					if cf_doWanttoChanageAnsofFuncQues.Content == 'Yes':
						cf_doWanttoChanageAnsofFuncQues.Editable = False
						row["Booking_Quote_Updates"] = 'Change'
						row["Difference"] = 'Change'
						row["Check"] = red
					if row["Difference"] == 'No Change':
						row["Check"] = green
						netCheck += 1
	if cf_proposal_Type.Content == 'Booking' and not(Quote.GetCustomField('Booking LOB').Content == 'HCP' and Quote.GetCustomField("Quote Type").Content == 'Parts and Spot'):
		Approvers = Quote.QuoteTables['EGAP_Approvers']
		cf_isBookingGateKeeperApprovalRequired.Content = str(False)
		cf_bookingQuoteApprovalRequirement.Content = 'This Quote requires all new approvals'
		if netCheck == 6:
			cf_isBookingGateKeeperApprovalRequired.Content = str(True)
			cf_bookingQuoteApprovalRequirement.Content = 'This Quote requires only Booking Gatekeeper approval'
			Approvers.Rows.Clear()
		if Quote.GetCustomField('IsApprovalNotRequired').Content == '1':
			cf_isBookingGateKeeperApprovalRequired.Content = str(True)
			cf_bookingQuoteApprovalRequirement.Content = 'This quote does not require approval as per approval exemption criteria however Booking Gate Keeper approval is required for this quote.'
			Approvers.Rows.Clear()

		for row in Approvers.Rows:
			if row['EGAP_Approver_Title'] == 'Booking Gatekeeper':
				row['EGAP_Reason'] = cf_bookingQuoteApprovalRequirement.Content
				break
		else:
			row = Approvers.AddNewRow()
			row['EGAP_Approver_Title'] = 'Booking Gatekeeper'
			row['EGAP_Reason'] = cf_bookingQuoteApprovalRequirement.Content
			
		Approvers.Save()
	bookingCheck.Save()