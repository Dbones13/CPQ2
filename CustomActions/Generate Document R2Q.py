#Quote.GetCustomField('EGAP_Highest_Price_Margin_Approval_Level').Content='0'
#ScriptExecutor.Execute("GS_ApprovalTabContent", {"Approval": "Getapproval"})
#ScriptExecutor.Execute("CPQ_SF_CreateUpdateOpportunity")
#if Quote.GetCustomField("EGAP_Highest_Approval_Level_for_the_Quote").Content  in ['','NA','0','No Approval']:
Session['generatedoc']="True"
Quote.ExecuteAction(3231)
ScriptExecutor.Execute('GS_R2Q_CPQ_TO_SFDC_DOC')
Session['generatedoc']=""