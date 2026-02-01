# CXCPQ-73528 ------ Start
if Quote.GetCustomField("Booking LOB").Content == "PMC" and Quote.GetCustomField("Quote Type").Content == "Projects":
    # Quote.Messages.Remove("Please use offline DRF process to request PMC Project approvals.")
    Quote.Messages.Clear()
    Quote.Messages.Add("Please use offline DRF process to request PMC Project approvals.")
    WorkflowContext.BreakWorkflowExecution = True   # CXCPQ-73528 ------ end