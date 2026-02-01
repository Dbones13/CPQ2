#---------------------------------------------------------------------------------------------------------
#					Change History Log
#---------------------------------------------------------------------------------------------------------
# Description : CPQ should send Quote Line items to SFDC
# JIRA Ref.   : CXCPQ-65799,CXCPQ-65141
# Author      : H542824
# CreatedDate : 17-01-2024
#----------------------------------------------------------------------------------------------------------
# Date 			Name					    Version     Comment
# 17-01-2024	Pratik Sanghani    			4 	        Initial Version
#----------------------------------------------------------------------------------------------------------

if Quote.GetCustomField("Booking LOB").Content == 'PMC':
    #Log.Write("Start of PMC QLI for Quote - "+Quote.CompositeNumber)
    #ScriptExecutor.ExecuteGlobal('GS_PMC_Quote_Lineitem_Sync')
    ScriptExecutor.ExecuteGlobal('GS_PMC_QLI_Sync_MainScript')
    #Log.Write("End of PMC QLI for Quote - "+Quote.CompositeNumber)