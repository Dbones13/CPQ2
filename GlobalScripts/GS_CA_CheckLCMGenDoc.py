if Quote.GetCustomField("CF_Multiyear_Project").Content == "Yes":
	ScriptExecutor.ExecuteGlobal('GS_LCMReport_Proposal')
	ScriptExecutor.ExecuteGlobal('GS_RefreshTPC')