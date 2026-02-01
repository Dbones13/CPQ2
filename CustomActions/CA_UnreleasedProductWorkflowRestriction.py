unreleased_Parts = Quote.GetCustomField("Unreleased_partList").Content
if unreleased_Parts and Quote.GetCustomField("Quote Type").Content == 'Projects' and Quote.GetCustomField("EGAP_RAFR1_Ques").Content == 'No' and Quote.GetCustomField('EGAP_Proposal_Type').Content != 'Budgetary':
    Quote.Messages.Add("Issue in Product Cross Distribution Status is 05 PreRelease & RAFR1 is set as 'No'. Please answer the RQUP question RAFR1 as 'Yes' in the functional review question tab."+str(unreleased_Parts))
    WorkflowContext.BreakWorkflowExecution = True