def UpdateRevisionData(Quote):
    if Quote.GetCustomField("IsRevisionEditing").Content == '1' and Quote.GetCustomField('Change Proposal Type').Content != '1':
        Quote.Messages.Add("PLEASE SELECT REVISED PROPOSAL TYPE FIELD BEFORE CREATING REVISION")
        Quote.GetCustomField("IsRevisionEditing").Content = '0'

    jsonString = Quote.GetCustomField('Revision Parent Data').Content
    if jsonString:
        json = RestClient.DeserializeJson(jsonString)
        revision = json["Booking Revision"]
        userId = json["UserId"]
        quoteId  = json["QuoteId"]
        IsR2QRequest=json["IsR2QRequest"]
        R2QFlag=json["R2QFlag"]
        if Quote.GetCustomField('firstEdit').Content == "True":
            Quote.GetCustomField('IsPrimary').Content='0'
        if quoteId != Quote.QuoteId or userId != Quote.UserId:
            Quote.CustomFields.SelectValueByValueCode("EGAP_Proposal_Type" , str(json["RevisionProposalType"]))
            Quote.GetCustomField("EGAP_Do_Want_to_Chanage_Ans_of_Func_Ques").Editable = True
            Quote.GetCustomField('EGAP_Do_Want_to_Chanage_Ans_of_Func_Ques').Content = "No"
            Quote.CustomFields.AssignValue('Parent Firm Revision' , "Revision - {}".format(str(revision)))
            Quote.CustomFields.AssignValue('Booking Revision' , "Revision - {}".format(str(revision)))
            Quote.CustomFields.AssignValue('Change Proposal Type' , '0')
            Quote.CustomFields.AssignValue('IsR2QRequest' , str(IsR2QRequest))
            Quote.CustomFields.AssignValue('R2QFlag' , str(R2QFlag))
            setQuestions = False
            if str(json["RevisionProposalType"]) in ('Firm','Booking') and str(json["CurrentProposalType"]) in ('Budgetary') and Quote.GetCustomField("Quote Type").Content not in ('Contract New', 'Contract Renewal') and "RevisionExecute" in json and json["RevisionExecute"] == 'No':
                Quote.GetCustomField('EGAP_Ques_CR5a').Content = "No"
                Quote.GetCustomField('EGAP_Ques_CR5b').Content = "No"
                Quote.GetCustomField('EGAP_CFR1_Ques').Content = "Yes"
                Quote.GetCustomField('EGAP_CFR2_Ques').Content = "Yes"
                Quote.GetCustomField('EGAP_CFR3_Ques').Content = "Yes"
                Quote.GetCustomField('EGAP_CFR4_Ques').Content = "Yes"
                Quote.GetCustomField('EGAP_CFR5_Ques').Content = "Yes"
                Quote.GetCustomField('EGAP_CFR6_Ques').Content = "Yes" if  Quote.GetCustomField('Opportunity Type').Content == 'Change Order' else "No"
                Quote.GetCustomField('EGAP_MFR1_Ques').Content = "Yes"
                Quote.GetCustomField('EGAP_RAFR1_Ques').Content = "Yes"
                Quote.GetCustomField('EGAP_RAFR3_Ques').Content = "Yes"
                Quote.GetCustomField('EGAP_RAFR4_Ques').Content = "Yes"
                Quote.GetCustomField('EGAP_IQ_Ques_1').Content = "Yes"
                Quote.GetCustomField('EGAP_IQ_Ques_18').Content = "Yes"
                setQuestions = True

            stage_qt = ['Pending Order Confirmation', 'Approved', 'Booked', 'Accepted by Customer', 'Submitted to Customer', 'Pending Contract Change Processing', 'Order Confirmation Pending', 'Order Created with Errors', 'Pending Project Creation', 'Project Created']
            if str(json["Quote_Status"]) in stage_qt and (str(json["Approval_Level"]) not in ('No Approval', 'No P&M Approval') or str(json["RevisionProposalType"]) == 'Booking'):
                Quote.GetCustomField('IS_PARENT_REVISION_APPROVED').Content = 'Yes'
                if Quote.GetCustomField("Booking LOB").Content == 'HCP' and Quote.GetCustomField("Quote Type").Content == 'Parts and Spot':
                    Quote.GetCustomField('IS_PARENT_REVISION_APPROVED').Content = 'No'
            else:
                Quote.GetCustomField('IS_PARENT_REVISION_APPROVED').Content = 'No'
        for item in Quote.MainItems:
            if item.PartNumber == 'PRJT R2Q':
                item.Delete()
        if setQuestions:
            json["RevisionExecute"] = "Yes"
            Quote.CustomFields.AssignValue('Revision Parent Data' , RestClient.SerializeToJson(json))
            Quote.Save(False)

UpdateRevisionData(Quote)
Quote.GetCustomField('firstEdit').Content = "False"