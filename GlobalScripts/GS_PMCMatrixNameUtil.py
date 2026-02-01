# Utility for fetching detail from quote ---->H542830 (start)
def PMC_MatrixName(Quote):
    LOB = "PMC"
    LimitType = "Discount"
    if Quote.GetCustomField("PMC Type").Content in ["Product", "Spares"]:
        PMCType = "Product"
        PMCProductFamily = Quote.GetCustomField("PMC Product Family").Content
        PMCProductLine = Quote.GetCustomField("PMC Product Line").Content
    else:
        PMCType = Quote.GetCustomField("PMC Type").Content
        PMCProductFamily = ""
        PMCProductLine = ""

    SqlQuery1 = "SELECT PMCMatrixName FROM PMC_Approval_Matrix_Name WHERE PMCRequestType = '{0}' AND PMCProductFamily = '{1}' AND PMCProductLine = '{2}'".format(PMCType,PMCProductFamily,PMCProductLine)
    MatrixName = SqlHelper.GetFirst(SqlQuery1)
    return MatrixName #---->H542830 (end)

# PMC Approval Highest Approval Level Update Logic ---->H541049 (start)
def PMC_MaxApprovalLogic(Quote,TSP,MatrixApprovalLevel,QuoteApprovalLevel):
    if int(MatrixApprovalLevel[0]) > int(QuoteApprovalLevel):
                QuoteApprovalLevel = MatrixApprovalLevel
    if Quote.GetCustomField("PMC Type").Content == "Spares":
        if int(QuoteApprovalLevel[0]) < 4:
            QuoteApprovalLevel = '4C'
    if TSP >= 250000 and Quote.GetCustomField("PMC Type").Content != "Spares":
        table = Quote.QuoteTables["Payment_MileStones"]
        Total_Percent = 0
        for i in table.Rows:
            if i["Milestone"] in ["Advance Payment"]:
                Total_Percent += i["_Amount"]
        if (Total_Percent < 10 and table.Rows.Count > 0) or Quote.GetCustomField("Milestone").Content == 'Exclude':
            if int(QuoteApprovalLevel[0]) < 4:
                QuoteApprovalLevel = '4C'
    return QuoteApprovalLevel #---->H541049 (end)

# PMC Approval Payment Milestone Message Update Logic ---->H542830 (start)
def PMC_PaymentMilestoneMessageLogic(Quote,TSP,ApprovalLevel):
    if TSP >= 250000 and Quote.GetCustomField("PMC Type").Content != "Spares":
        table = Quote.QuoteTables["Payment_MileStones"]
        Total_Percent = 0
        for i in table.Rows:
            if i["Milestone"] in ["Advance Payment"]:
                Total_Percent += i["_Amount"]
        if (Total_Percent < 10 and table.Rows.Count > 0) or Quote.GetCustomField("Milestone").Content == 'Exclude':
            AddMessage = 'This quote requires Level {} approval because Advanced Payment is < 10% or Advanced Payment is not included in the Payment Milestones or Milestone as "Exclude”.'.format(ApprovalLevel)
            Quote.Messages.Add(AddMessage) #---->H542830 (end)

# PMC Logic to send 10% Advance Payment message to SFDC Field ---->H541049 (start)
def PMC_MilestoneMessage(Quote,UserPersonalizationHelper):
    TSP = UserPersonalizationHelper.ConvertToNumber(Quote.GetCustomField("Total Sell Price").Content)
    exchangeRate = Quote.GetCustomField("Exchange Rate").Content
    TSP_USD = TSP / float(exchangeRate)
    Message = ''
    AP_rows = 0
    if TSP_USD >= 250000:
        table = Quote.QuoteTables["Payment_MileStones"]
        Total_Percent = 0
        for i in table.Rows:
            if i["Milestone"] in ["Advance Payment"]:
                Total_Percent += i["_Amount"]
                AP_rows += 1
        if AP_rows == 0:
            Message = 'No - No Advance Payment'
        if Total_Percent >= 10:
            Message = 'Yes - 10% (or more) Advance Payment'
        if AP_rows != 0 and Total_Percent < 10:
            Message = 'Yes - less than 10% (Advance payment)'
    else:
        Message = 'NA - Not Applicable'
    return Message #---->H541049 (end)