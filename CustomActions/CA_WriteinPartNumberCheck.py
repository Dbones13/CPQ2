writeinPartMissing = False
for prod in Quote.GetItemsByProductTypeSystemId('Write-In_cpq'):
	if prod.ProductName =='WriteIn':
		if prod.QI_WriteinMaterial.Value == '':
			writeinPartMissing = True
			break
if writeinPartMissing:
	WorkflowContext.BreakWorkflowExecution = True
	if not Quote.Messages.Contains(Translation.Get('message.writeinPartMissing')):
		Quote.Messages.Add(Translation.Get('message.writeinPartMissing'))