def getCFValue(quote,field):
    return Quote.GetCustomField(field).Content

if (getCFValue(Quote,'Minimum Order fee Waiver reason') or getCFValue(Quote, 'Expedite Fee Waiver Reason') ) and not (getCFValue(Quote,'LOB_Approver_Name')):
    WorkflowContext.BreakWorkflowExecution = True
    if not Quote.Messages.Contains(Translation.Get('Error.ApproverNameEmpty')):
        Quote.Messages.Add(Translation.Get('Error.ApproverNameEmpty'))

