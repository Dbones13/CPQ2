import GS_R2Q_FunctionalUtil
ProductType = Quote.GetCustomField('ProductType').Content
if ProductType not in ('Cyber','HCI'):
	Quote.ExecuteAction(3213)
if ProductType in ('Cyber','HCI'):
	try:
		Quote.GetCustomField('EGAP_Highest_Price_Margin_Approval_Level').Content='0'
		Retval=ScriptExecutor.Execute("GS_R2Q_ApprovalcheckLSS", {})
		Trace.Write('afterlsscheck -'+str(Quote.GetCustomField('EGAP_Highest_Approval_Level_for_the_Quote').Content))
		if Retval:
			ScriptExecutor.Execute("GS_ApprovalTabContent", {"Approval": "Getapproval"})
	except Exception as ex:
		msg = 'Error Occured, {"ErrorCode": "Approval", "ErrorDescription": "Failed at: Approval Workflow"}'
		GS_R2Q_FunctionalUtil.UpdateStatusMessage(Quote, "Error", "Notification", msg)
		raise
try:
	ScriptExecutor.Execute('GS_R2Q_CPQ_TO_SFDC_DOC')
except Exception as ex:
	msg = 'Error Occured, {"ErrorCode": "DocumentGeneration", "ErrorDescription": "Failed at: Proposal Generation"}'
	GS_R2Q_FunctionalUtil.UpdateStatusMessage(Quote, "Error", "Notification", msg)
	raise