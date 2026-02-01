if (Quote.GetCustomField("Quote Tab Booking LOB").Content == "LSS" and  Quote.GetCustomField("Quote Type").Content == "Projects"):
    approversQT = Quote.QuoteTables["EGAP_Approvers"]
    if approversQT.Rows.Count > 0:
        WorkflowContext.BreakWorkflowExecution = True
        if not Quote.Messages.Contains(Translation.Get('Message.ApprovalRequired')):
            Quote.Messages.Add(Translation.Get('Message.ApprovalRequired'))