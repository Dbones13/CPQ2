from GS_PMC_ApprovalMatrix import PMC_Approval
from GS_PopulateEGAPApproversQuoteTable_Helper import *
from GS_EGAPAPPROVER_MODULE import EGAP_aprover_module
quoteType = Quote.GetCustomField('Quote Type').Content
if ((quoteType in ('Projects','Contract New','Contract Renewal') and Quote.OrderStatus.Name =='Preparing') or (quoteType in ('Parts and Spot') and Quote.OrderStatus.Name =='Preparing' and Quote.GetCustomField("CF_ApprovalTabBookingLOB").Content == 'CCC') or (Quote.OrderStatus.Name =='Preparing' and Quote.GetCustomField("CF_ApprovalTabBookingLOB").Content == 'HCP')):
	if Quote.Items.Count > 0:
		EGAP_aprover_module(Quote,quoteType,TagParserQuote)
	else:
		quoteTables = ['EGAP_Revenue_Margin', 'EGAP_Labor_and_Engineering_Service', 'EGAP_Approvers', 'EGAP_Third_Party_Content', 'EGAP_Net_Cash_Balance', 'EGAP_CFQ_Baseline', 'EGAP_CFQ']
		for quoteTable in quoteTables:
			qt = Quote.QuoteTables[quoteTable]
			qt.Rows.Clear()
		customFields = ['EGAP_Highest_Cash_Risk_Approval_Level', 'EGAP_No_eGap', 'EGAP_Highest_Price_Margin_Approval_Level', 'EGAP_Approval_Level_when_Price_Discount_Exceeds_Threshold_Discount', 'EGAP_Cash_Flow_Quality', 'EGAP_Approval_Level_when_Cash_Flow_negative_position_GT_100k', 'EGAP_Lowest_Cum_CF_in_any_Single_Month_USD', 'EGAP_Highest_Approval_Level_for_the_Quote', 'EGAP_Cross_Margin', 'EGAP_Cashflow_Health','CF_MaxApprovalLevel','EGAP_Months_Negative_Cumulative_Cash_Flows','EGAP_Max_Consec_Months_Neg_Cum_Cash_Flows','EGAP_Revenue_Impact_Change_in_Currency_USD']
		for cf in customFields:
			Quote.GetCustomField(cf).Content = ''
	if Quote.GetCustomField("Booking LOB").Content == 'CCC':
		Quote.GetCustomField("EGAP_Advance_Payment_Milestone_Billing_Ques").Content = 'No'
		# if float(Quote.QuoteTables["Quote_Details"].Rows[0]["Quote_Discount_Percent"]) in (0,0.0):
			# Quote.GetCustomField('EGAP_Highest_Price_Margin_Approval_Level').Content = 'No Approval'
			# Quote.GetCustomField('EGAP_Highest_Approval_Level_for_the_Quote').Content = 'Functional Approvals Only' if int(Quote.QuoteTables["EGAP_Approvers"].Rows.Count) > 0 else 'No Approval'
	msg = "This quote does not require approval as per approval exemption criteria."
	if Quote.GetCustomField('EGAP_Highest_Approval_Level_for_the_Quote').Content == 'No Approval' and Quote.GetCustomField("Booking LOB").Content in ('LSS', 'PAS','HCP') and quoteType in ['Projects','Parts and Spot'] and Quote.GetCustomField('EGAP_Proposal_Type').Content.strip() != 'Booking':
		qt_apr = Quote.QuoteTables["EGAP_Approvers"]
		qt_apr.Rows.Clear()
		if not Quote.Messages.Contains(msg):
			Quote.Messages.Add(msg)
	elif Quote.GetCustomField('EGAP_Highest_Approval_Level_for_the_Quote').Content == 'No Approval' and Quote.GetCustomField("Booking LOB").Content == 'HCP' and quoteType == 'Parts and Spot' and Quote.GetCustomField('EGAP_Proposal_Type').Content.strip() != 'Booking':
		qt_apr = Quote.QuoteTables["EGAP_Approvers"]
		qt_apr.Rows.Clear()
		if not Quote.Messages.Contains(msg):
			Quote.Messages.Add(msg)
	elif Quote.GetCustomField("Booking LOB").Content == 'HCP' and Quote.GetCustomField('EGAP_Highest_Approval_Level_for_the_Quote').Content == 'No Approval' and quoteType in ['Projects','Parts and Spot'] and Quote.GetCustomField('EGAP_Proposal_Type').Content.strip() == 'Booking':
			apr_obj = Quote.QuoteTables["EGAP_Approvers"]
			aprvr_row = apr_obj.Rows[0]
			Approver_Title = aprvr_row["EGAP_Approver_Title"]
			EGAP_Reason = aprvr_row["EGAP_Reason"]
			apr_obj.Rows.Clear()
			row = apr_obj.AddNewRow()
			row["EGAP_Approver_Title"]=Approver_Title
			row["EGAP_Reason"]=EGAP_Reason
	elif Quote.GetCustomField("Booking LOB").Content in ('LSS', 'PAS', 'CCC') and quoteType == 'Projects':
		if Quote.Messages.Contains(msg):
			Quote.Messages.Remove(msg)
'''elif (quoteType in ('Parts and Spot') and Quote.OrderStatus.Name =='Preparing' and Quote.GetCustomField("CF_ApprovalTabBookingLOB").Content == 'LSS'):
	Quote.GetCustomField("IsApprovalNotRequired").Content = '0'
	Quote.GetCustomField("CF_MaxApprovalLevel").Content = ''
	Quote.GetCustomField("EGAP_Highest_Price_Margin_Approval_Level").Content = ''
	Quote.QuoteTables["EGAP_Approvers"].Rows.Clear()'''
if Quote.GetCustomField("Booking LOB").Content == 'PMC':
	PMC_Approval(Quote, UserPersonalizationHelper, TagParserQuote)
