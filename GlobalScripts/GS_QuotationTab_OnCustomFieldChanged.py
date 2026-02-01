if Quote.GetCustomField('EGAP_Proposal_Type').Label == sender.Label:
    Quote.CustomFields.Disallow('Parent Firm Revision','EGAP_Do_Want_to_Chanage_Ans_of_Func_Ques')
    if arg.NewValue == 'Booking':
        Quote.CustomFields.Allow('Parent Firm Revision')
        Quote.GetCustomField('Parent Firm Revision').Editable = False
        if Quote.GetCustomField('EGAP_IS_Booking_Check_Visible').Content == 'Yes':
            Quote.CustomFields.Allow('EGAP_Do_Want_to_Chanage_Ans_of_Func_Ques')