MSIDSystemNumberList= SqlHelper.GetList(TagParserQuote.ParseString("Select MSID, SystemId from MSID where Account_Name = '<*CTX( Quote.CustomField(Account Name))*>' and (EntitlementType = '<*CTX( Quote.CustomField(Entitlement))*>' or EntitlementType is null) and MSID not in ('<*GI(hello)*>')"))
MSIDSystemTable = Quote.QuoteTables["MSID_System_Number_Summary"]
MSIDSystemTable.Rows.Clear()
if MSIDSystemNumberList:
    for data in MSIDSystemNumberList:
        if data.SystemId:
            row = MSIDSystemTable.AddNewRow()
            row["MSID"] = data.MSID
            row["System_Number"] = data.SystemId

isMPAApplied = Quote.GetCustomField('MPA').Content
reason = Quote.GetCustomField("EGAP_Reason_For_Deviation_Milestone_Billing_Ques").Content
quoteType = Quote.GetCustomField("Quote Type").Content
if isMPAApplied and not reason:
    Quote.GetCustomField("EGAP_Advance_Payment_Milestone_Billing_Ques").Content = 'No'
    Quote.GetCustomField("EGAP_Reason_For_Deviation_Milestone_Billing_Ques").Content = 'Contractual Agreement'
elif quoteType in ['Contract New', 'Contract Renewal']:
    Quote.GetCustomField("EGAP_Advance_Payment_Milestone_Billing_Ques").Content = 'No'
    Quote.GetCustomField("EGAP_Reason_For_Deviation_Milestone_Billing_Ques").Content = 'No Deviation'
    
if isMPAApplied in (None, '') and Quote.GetCustomField('Milestone').Content in ['Custom'] and Quote.GetCustomField('Booking LOB').Content in ['LSS']:
	#Quote.GetCustomField("do_proposed_milestones_deviate_negatively").Content = 'Yes'
	Quote.GetCustomField('do_proposed_milestones_deviate_negatively').Visible = True
else:
	Quote.GetCustomField('do_proposed_milestones_deviate_negatively').Visible = False