def getCFValue(name):
    return Quote.GetCustomField(name).Content

def populateRevisionDataField():

    revisionData = dict()
    revisionData["Booking Revision"] = str(Quote.RevisionNumber)
    revisionData["RevisionProposalType"] = getCFValue("Revised proposal type")
    revisionData["CurrentProposalType"] = getCFValue("EGAP_Proposal_Type")
    revisionData["Approval_Level"] = getCFValue("EGAP_Highest_Price_Margin_Approval_Level")
    revisionData["Quote_Status"] = str(Quote.OrderStatus.Name)
    revisionData["UserId"] = Quote.UserId
    revisionData["QuoteId"] = Quote.QuoteId
    revisionData["IsR2QRequest"] = "No"
    revisionData["R2QFlag"] = "No"
    revisionData["RevisionExecute"] = "No"

    Quote.CustomFields.AssignValue('Revision Parent Data' , RestClient.SerializeToJson(revisionData))
    Quote.Save(False)

if (getCFValue("Quote Type") in ('Projects','Contract New','Contract Renewal') and getCFValue("Booking LOB") in ('LSS', 'PAS')) or (getCFValue("Quote Type") in ('Projects','Parts and Spot') and getCFValue("Booking LOB") in ('CCC','HCP')):
    if getCFValue("Revised proposal type") == '':
        WorkflowContext.BreakWorkflowExecution = True
        WorkflowContext.ChangeQuoteStatus = False
        Quote.GetCustomField("IsRevisionEditing").Content = '1'
        Quote.Save(False)
    else:
        Quote.GetCustomField("IsRevisionEditing").Content = '0'
        populateRevisionDataField()

    #from GS_UpdateRevisionData import UpdateRevisionData
    #UpdateRevisionData(Quote)