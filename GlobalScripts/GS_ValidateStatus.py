if Quote.OrderStatus.Name == "Pending Project Creation":
    if Quote.GetCustomField('CF_ProjectId').Content != "" and Quote.GetCustomField('CF_ProjectId').Content != None:
        Quote.ChangeQuoteStatus('Project Created')

if Quote.OrderStatus.Name == "Pending Order Confirmation":
    if Quote.OrderId != None:
        Quote.ExecuteAction(1923)

