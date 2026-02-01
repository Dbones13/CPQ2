def setegapvalues(Quote):
	Quote.GetCustomField("EGAP_Advance_Payment_Milestone_Billing_Ques").Content = 'No'
	Quote.GetCustomField("EGAP_Reason_For_Deviation_Milestone_Billing_Ques").Content = 'Time and Materials'
	Quote.SetGlobal("ProposalType", "Updated")