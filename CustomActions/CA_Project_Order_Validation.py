if ((Quote.GetCustomField("Booking Country").Content.upper() == "UNITED STATES") and (Quote.GetCustomField("Quote Type").Content == "Projects")):
   if ((Quote.GetCustomField("CF_US_TAX1").Content == '') or (Quote.GetCustomField("CF_US_TAX2").Content == '')):
        WorkflowContext.BreakWorkflowExecution = True
        if not Quote.Messages.Contains(Translation.Get('message.USTAX')):
            Quote.Messages.Add(Translation.Get('message.USTAX'))
if not Quote.BillToCustomer and not Quote.ShipToCustomer and not Quote.EndUserCustomer:
    WorkflowContext.BreakWorkflowExecution = True
    if not Quote.Messages.Contains(Translation.Get('message.PartnerInfo')):
        Quote.Messages.Add(Translation.Get('message.PartnerInfo'))
elif Quote.EndUserCustomer.CustomerCode =="" or Quote.BillToCustomer.CustomerCode =="" or Quote.ShipToCustomer.CustomerCode =="":
    WorkflowContext.BreakWorkflowExecution = True
    if not Quote.Messages.Contains(Translation.Get('message.PartnerInfo')):
        Quote.Messages.Add(Translation.Get('message.PartnerInfo'))
if Quote.GetCustomField('SoldToCustomerId').Content=='':
    WorkflowContext.BreakWorkflowExecution = True
    if not Quote.Messages.Contains(Translation.Get('message.PartnerInfo')):
        Quote.Messages.Add(Translation.Get('message.PartnerInfo'))
if Quote.GetCustomField('PurchaseOrderDate').Content=='':
    WorkflowContext.BreakWorkflowExecution = True
    if not Quote.Messages.Contains(Translation.Get('message.PurchaseOrderDate')):
        Quote.Messages.Add(Translation.Get('message.PurchaseOrderDate'))