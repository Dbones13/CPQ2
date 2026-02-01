#--------------------------------------------------------------------------------
#					Change History Log
#--------------------------------------------------------------------------------
# Description: Custom action to generate and send documents to SFDC for R2Q parts and spot.
#--------------------------------------------------------------------------------
# Date 			Name					    Version   Comment
# 05-07-2023	Saswat Kumar Mishra			23		  Initial Creation

#-- H541049 : CXCPQ-52047 : start
import GS_R2Q_FunctionalUtil
from GS_R2Q_Integration_Messages import CL_R2Q_Integration_SuccessMessages as Success, CL_R2Q_Integration_ErrorMessages as Error

try:
    #Fetch the status
    if Quote.GetCustomField("Quote Type").Content == 'Parts and Spot' and Quote.GetCustomField("CF_R2Q_AutomationFlag").Content == 'Y':
        Quote.Save()
    status = TagParserQuote.ParseString('<*CTX( Quote.Status.Name )*>')
    #If status is Approved and valid parts and spot quote then generate the documents
    if Quote.GetCustomField("Quote Type").Content == 'Parts and Spot' and status == 'Approved' and Quote.GetCustomField("CF_R2Q_AutomationFlag").Content == 'Y':
        GS_R2Q_FunctionalUtil.R2QDocumentGeneration(Quote)
        Quote.ChangeQuoteStatus('Submitted to Customer')
        for action in Quote.Actions:
            if action.Name == "Make Quote Primary":
                Quote.ExecuteAction(action.Id)
                break
        ScriptExecutor.Execute('CPQ_SF_CreateUpdateOpportunity')
        Quote.Save()
        if Quote.OrderStatus.Name == "Submitted to Customer":
            GS_R2Q_FunctionalUtil.UpdateStatusMessage(Quote, "Final", "Action", Success.Submitted)
        else:
            GS_R2Q_FunctionalUtil.UpdateStatusMessage(Quote, "Error", "Notification", "Error occured during changing the status to Submitted to Customer.")
    ##If status is Rejected and valid parts and spot quote then send the notification to SFDC
    elif Quote.GetCustomField("Quote Type").Content == 'Parts and Spot' and status == 'Rejected' and Quote.GetCustomField("CF_R2Q_AutomationFlag").Content == 'Y':
        GS_R2Q_FunctionalUtil.UpdateStatusMessage(Quote, "Approval-Rejection", "Action", Error.Rejected)

except Exception as e:
    Log.Write("Exception occured as follows:
{0}".format(e))
    GS_R2Q_FunctionalUtil.UpdateStatusMessage(Quote, "System Error", "Notification", str(e)) #-- H541049 : CXCPQ-52047 : end