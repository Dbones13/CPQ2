'''import GS_CheckInvalidQty as check
check.CheckForInvalidQty(Quote)
if Quote.GetCustomField('InvalidQty').Content != '' or Quote.GetCustomField('InvalidMinDeliveryQty').Content != '':
    WorkflowContext.BreakWorkflowExecution = True'''
