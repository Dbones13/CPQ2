# CXCPQ-72564 - Start
# Fetch the Quote number from the request body
bodyData = RestClient.DeserializeJson(RequestContext.Body)
quoteNumber = str(bodyData["QuoteNumber"])

# Reprice & Save the Quote
Quote = QuoteHelper.Edit(quoteNumber)
status = Quote.OrderStatus.Name
Quote.ChangeQuoteStatus('Preparing')
Quote.Calculate(2)
Quote.Calculate()
#Quote.ChangeQuoteStatus('Awaiting Approval')
Quote.ChangeQuoteStatus(status)
Quote.Save()
# CXCPQ-72564 - end