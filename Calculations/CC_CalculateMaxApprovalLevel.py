"""
import GS_CommonModule as CM

def removeMessages(Quote):
    approvalLevels = range(6)
    for level in approvalLevels:
        Message = 'This quote requires L{} approval. Please click on "Request Approval" action to proceed further.'.format(level)
        Quote.Messages.Remove(Message)

quoteType       = CM.getCFValue(Quote, "Quote Type")
LOB             = CM.getCFValue(Quote, "Booking LOB")
exchangeRate    = CM.getCFValue(Quote, "Exchange Rate")
approvalLevel   = CM.getCFValue(Quote, "CF_MaxApprovalLevel")
oppCategory = CM.getCFValue(Quote, "CF_ApprovalTabOpportunityCategory")
oppCategoryList = ['A','B']
highestApprovalLevel = CM.getCFValue(Quote, "EGAP_Highest_Approval_Level_for_the_Quote")

oldMessage      = Translation.Get("ApprovalEscalation.Notification").format(approvalLevel)
Quote.Messages.Remove(oldMessage)

'''Remove the Old approval messages'''
removeMessages(Quote)

if LOB == 'LSS':
    quoteDetails = Quote.QuoteTables["Quote_Details"]
    if Quote.Items.Count > 0 and quoteDetails.Rows.Count > 0:
        row = quoteDetails.Rows[0]
        sellPrice       = row["Quote_Sell_Price"] / float(exchangeRate)
        discount        = row["Quote_Discount_Percent"]
        if quoteType == 'Projects':
            sellPrice 		= row["Walk_away_Sales_Price"] / float(exchangeRate)
            quoteWTWCost = row['Quote_WTW_Cost'] / float(exchangeRate)
            wtwMargin = sellPrice - quoteWTWCost
            discount = round((wtwMargin/sellPrice)*100,2) if sellPrice > 0 else 0
            #Trace.Write("wtwMargin Percentage :{}%".format(discount))
            #discount = row["Quote_WTW_Margin_Percent"] if row["Quote_WTW_Margin_Percent"] else 0
            cf_proposalType = CM.getCFValue(Quote, "EGAP_Proposal_Type")
            proposalType = cf_proposalType
            limitType = "Wall-to-Wall Margin"
            if cf_proposalType in ['Firm', 'Booking']:
                proposalType = 'Firm & Booking'
        else:
            proposalType = "Parts & Spots"
            limitType = "Discount"
        Approval_Level  = CM.GetApprovalLevel(quoteType, LOB, sellPrice, discount, proposalType, limitType)
        CM.setCFValue(Quote, "CF_MaxApprovalLevel", "")
        CM.setCFValue(Quote, "EGAP_No_eGap", "")
        if Approval_Level and Approval_Level.ApprovalLevel:
            Message = ''
            Message2 = ''
            level = "L{}".format(Approval_Level.ApprovalLevel)
            if  proposalType == 'Parts & Spots':
                CM.setCFValue(Quote, "CF_MaxApprovalLevel", level)
                Message = Translation.Get("ApprovalEscalation.Notification").format(level)
            else:
                if Approval_Level.ApprovalLevel == 'No P&M Approval':
                    CM.setCFValue(Quote, "EGAP_No_eGap", "No eGap")
                quoteTableApprovers = Quote.QuoteTables['EGAP_Approvers']
                if quoteTableApprovers.Rows.Count > 0:
                    query = "Select EGAP_Reason from QT__EGAP_Approvers where ownerid={} and cartid={} and EGAP_Approver_Title='{}'".format(Quote.UserId,Quote.QuoteId, 'Booking GateKeeper')
                    qtResult = SqlHelper.GetFirst(query)
                    if qtResult is not None:
                        oldMsg = 'This Quote requires approval from all approvers as per the Approver Table.'
                        Message = 'This Quote requires only Booking Gatekeeper approval'
                        if qtResult.EGAP_Reason != 'This Quote requires only Booking Gatekeeper approval':
                            oldMsg = 'This Quote requires only Booking Gatekeeper approval'
                            Message = 'This Quote requires approval from all approvers as per the Approver Table.'
                        '''Remove Old Message'''
                        if Quote.Messages.Contains(oldMsg):
                            Quote.Messages.Remove(oldMsg)
                if Approval_Level.ApprovalLevel != 'No P&M Approval' and (Message == '' or Message == 'This Quote requires approval from all approvers as per the Approver Table.'):
                    CM.setCFValue(Quote, "CF_MaxApprovalLevel", Approval_Level.ApprovalLevel)
                    Message2 = Message
                    if quoteType == 'Projects':
                        Message = ''
                        if highestApprovalLevel.strip() != '':
                            level = "L{}".format(highestApprovalLevel)
                            Message = 'This quote requires {} approval. Please click on "Request Approval" action to proceed further.'.format(level)
            if not Quote.Messages.Contains(Message) and Message != '':
                Quote.Messages.Add(Message)
                if not Quote.Messages.Contains(Message2) and Message2 != '':
                    Quote.Messages.Add(Message2)
                Quote.RefreshActions()
"""