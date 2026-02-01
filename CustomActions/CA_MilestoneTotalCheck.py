paymentMileStone = Quote.QuoteTables["Payment_MileStones"]
if ( ( Quote.GetCustomField("Quote Tab Booking LOB").Content in ("PMC","HCP") and  Quote.GetCustomField("Quote Type").Content == "Parts and Spot") or (Quote.GetCustomField("Quote Tab Booking LOB").Content in ('LSS','PAS','HCP') and  Quote.GetCustomField("Quote Type").Content == "Projects")):
    if paymentMileStone.Rows.Count > 0 and float(Quote.GetCustomField("Milestone_total").Content or 0) != 100 :
        WorkflowContext.BreakWorkflowExecution = True
        if not Quote.Messages.Contains(Translation.Get('Message.MilestoneTotalCheck')):
            Quote.Messages.Add(Translation.Get('Message.MilestoneTotalCheck'))