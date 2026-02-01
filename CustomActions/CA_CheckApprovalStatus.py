from GS_CheckApprovalStatus import check_approval_status
check_approval_status(Quote)
if Quote.GetCustomField('Is_pendingApprovalProcess').Content == '1':
    WorkflowContext.BreakWorkflowExecution = True
    if not Quote.Messages.Contains(Translation.Get('message.RevisionApprovalStatus')):
        Quote.Messages.Add(Translation.Get('message.RevisionApprovalStatus'))