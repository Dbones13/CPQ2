if Quote.GetCustomField("Quote Type").Content == 'Projects':
	tb = Quote.QuoteTables["EGAP_Project_Milestone"]
	#Trace.Write(tb.Rows.Count)
	if tb.Rows.Count == 0:
		 Quote.GetCustomField("check1").Content = ''
	elif tb.Rows.Count > 0 and Quote.GetCustomField("check1").Content == '':
		for row in tb.Rows:
			if row["EGAP_Proposed_Milestones"] =="Milestone 1":
					row["EGAP_Customer_Signoff_Required"]= "Yes"
					row["EGAP_Milestone_with_Bank_Guarantee"]= "Yes"
		Quote.GetCustomField("check1").Content = "Yes"