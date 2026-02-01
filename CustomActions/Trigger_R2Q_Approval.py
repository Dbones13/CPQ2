Quote.GetCustomField('EGAP_Highest_Price_Margin_Approval_Level').Content='0'
#Retval=ScriptExecutor.Execute("GS_R2Q_ApprovalcheckLSS", {})
#if Retval:
	#ScriptExecutor.Execute("GS_ApprovalTabContent", {"Approval": "Getapproval"})
#Quote.ExecuteAction(3231)
#ScriptExecutor.Execute('GS_R2Q_CPQ_TO_SFDC_DOC')