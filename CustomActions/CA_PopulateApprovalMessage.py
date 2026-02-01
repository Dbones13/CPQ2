if Quote.GetCustomField('R2QFlag').Content == 'Yes' and Quote.GetCustomField("CF_ApprovalTabBookingLOB").Content == 'HCP':
 	ScriptExecutor.ExecuteGlobal('GS_FunctionalQuestionsSetDefaultAnswer')
 	ScriptExecutor.ExecuteGlobal('GS_PopulateEGAPApproversQuoteTable')
 	ScriptExecutor.ExecuteGlobal('GS_PopulateBookingCheckQuoteTable')
 	#ScriptExecutor.ExecuteGlobal('GS_ApprovalMessage')