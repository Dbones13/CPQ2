#GS_RemoveEGAPApprovers
from Scripting.QuoteTables import AccessLevel
quoteType = Quote.GetCustomField('Quote Type').Content.strip()
proposalType = Quote.GetCustomField("EGAP_Proposal_Type").Content
approvalLeval = Quote.GetCustomField("EGAP_Highest_Price_Margin_Approval_Level").Content
if quoteType in ('Contract New','Contract Renewal'):
    if Quote.Items.Count > 0:
        finApprovalMethod = Quote.GetCustomField('SC_CF_FIN_APPROVAL_METHOD').Content.strip()
        qtEGAPApprovers = Quote.QuoteTables['EGAP_Approvers']
        if (qtEGAPApprovers.Rows.Count > 0 and finApprovalMethod !=  'eGap') or (proposalType == 'Budgetary' and approvalLeval in ['No Approval','0']) :
            qtEGAPApprovers.Rows.Clear()
            Quote.QuoteTables.Item['EGAP_Approvers'].AccessLevel = AccessLevel.Hidden
            Quote.Messages.Add("This quote does not require approval as per approval exemption criteria.")
        else:
            Quote.QuoteTables.Item['EGAP_Approvers'].AccessLevel = AccessLevel.Editable