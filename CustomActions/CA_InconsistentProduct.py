inconsistentFlag = TagParserQuote.ParseString('[AND]([EQ](<*CTX( Quote.HasIncompleteItems )*>,1),[EQ](<* QuoteProperty (Booking LOB) *>,PMC))')
if inconsistentFlag == '1':
    WorkflowContext.BreakWorkflowExecution = True
    if not Quote.Messages.Contains(Translation.Get('message.InconsistentProduct')):
        Quote.Messages.Add(Translation.Get('message.InconsistentProduct'))