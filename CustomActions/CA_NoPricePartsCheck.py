ScriptExecutor.ExecuteGlobal('GS_CheckNoPriceProducts')
if Quote.GetCustomField('NoPriceParts').Content != '':
    WorkflowContext.BreakWorkflowExecution = True