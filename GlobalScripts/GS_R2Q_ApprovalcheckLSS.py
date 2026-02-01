from GS_Curr_ExchRate_Mod import fn_get_curr_exchrate
def check_quote_approval():
	if Quote.GetCustomField("R2QFlag").Content in ('yes', 'Yes', 'YES', 'True', 'true', 'True') and Quote.GetCustomField("CF_ApprovalTabBookingLOB").Content in ('LSS','HCP'):
		
		quoteDetails = Quote.QuoteTables["Quote_Details"]

		if quoteDetails.Rows.Count:
			row = quoteDetails.Rows[0]
			sellPrice = row["Walk_away_Sales_Price"]
			Quote_Currency = Quote.GetCustomField("SC_CF_CURRENCY").Content
			exchange_rate = fn_get_curr_exchrate(Quote_Currency, "USD")
			if sellPrice:
				sellPrice = round(float(sellPrice)*exchange_rate,2)
			TargetPrice = row["Recommended_Target_Price"]
			DiscountAmount = row["Quote_Discount_Amount"]
			wtwMargin = row["Quote_WTW_Margin_Percent"]
			if Quote.GetCustomField("CF_ApprovalTabBookingLOB").Content in ('LSS'):
				if 2000000 >= sellPrice >= TargetPrice:
					Quote.GetCustomField("Is_Quote_Approval_Exempted").Content = "Yes"
					Quote.GetCustomField('EGAP_Highest_Price_Margin_Approval_Level').Content = "No Approval"
					Quote.GetCustomField('EGAP_Highest_Approval_Level_for_the_Quote').Content = "No Approval"
					Quote.Messages.Add('Approval Exemption for R2Q Quote: Sell Price up to $2M and Pricing as per MPA discount or as per Recommended discount schedule, then quote approval is exempted.')
					Quote.SetGlobal('msgshow','True')
					Quote.Save(False)
					Log.Info(Quote.GetGlobal('msgshow'))
					Log.Info("GS_R2Q_ApprovalcheckLSS")
					return False
			elif Quote.GetCustomField("CF_ApprovalTabBookingLOB").Content in ('HCP'):
				Trace.Write('HCP QUOTE APPROVAL SELL PRICE -'+str(sellPrice)+'---'+str(wtwMargin)+'--'+str(Quote.GetCustomField('Is_Quote_Approval_Exempted').Content))
				Quote.GetCustomField("Is_Quote_Approval_Exempted").Content = 'No'
				Log.Info('Approval lss -->'+str([sellPrice,wtwMargin]))
				if sellPrice < 1000000 and float(wtwMargin)> 35.00:
					Trace.Write('exemption is opted---')
					Quote.GetCustomField("Is_Quote_Approval_Exempted").Content = "Yes"
					#Quote.GetCustomField('EGAP_Highest_Price_Margin_Approval_Level').Content = "No Approval"
					Quote.GetCustomField('EGAP_Highest_Approval_Level_for_the_Quote').Content = "No Approval"
					Quote.Messages.Add('Approval Exemption for R2Q Quote: Sell Price is less than 1M and margin exceeds 35 % then quote approval is exempted.')
					Quote.SetGlobal('msgshow','True')
					Quote.Save(False)
					return True

	return True  # Ensure False is returned if conditions are not met

# Call the function if needed
Result = check_quote_approval()