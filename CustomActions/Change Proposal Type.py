Quote.GetCustomField("Change Proposal Type").Content = "1"
Quote.GetCustomField("Revised proposal type").Visible = True
if Quote.GetCustomField('Quote Type').Content == 'Contract Renewal':
    Quote.GetCustomField("Revised proposal type").Content = 'Firm'
    Quote.Save(False)
WorkflowContext.RedirectToURL = "/quotation/Cart.aspx"