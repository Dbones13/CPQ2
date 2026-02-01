import GS_APIGEE_Integration_Util
excel_Url, header = GS_APIGEE_Integration_Util.GetR2QAPIGEEAuthDetails()
try:
    QuoteNumber = Param.QuoteNumber
    Quote = QuoteHelper.Edit(QuoteNumber)
    if Quote.GetCustomField('R2Q_Save').Content == 'Submit':
        Quote.GetCustomField('EGAP_Highest_Price_Margin_Approval_Level').Content='0'
        Retval=ScriptExecutor.Execute("GS_R2Q_ApprovalcheckLSS", {})
        if Retval:
            ScriptExecutor.Execute("GS_ApprovalTabContent", {"Approval": "Getapproval"})
        Quote.ExecuteAction(3215)
        Log.Info('GS_R2Q_DocumentGeneration Success-->>')
        final_request_body={'QuoteNumber':str(QuoteNumber),'CartId':str(Param.CartId),'RevisionNumber': str(Param.RevisionNumber),'UserName':str(User.UserName),'Module':Param.Modulename,'Action':'Update','Status':'Success','Action_List':[{'ActionName':'Document Generation','ScriptName':'GS_R2Q_DocumentGeneration'}]}
        res = RestClient.Post(excel_Url, RestClient.SerializeToJson(str(final_request_body)),header)
        Log.Info('GS_R2Q_DocumentGeneration =>> Req: {} -- Res: {}'.format(final_request_body, res))
except Exception as ex:
    Log.Info('GS_R2QPRJT_DocumentGeneration Fail-->>'+str(ex))
    final_request_body={'QuoteNumber':str(QuoteNumber),'CartId':str(Param.CartId),'RevisionNumber': str(Param.RevisionNumber),'UserName':str(User.UserName),'Module':Param.Modulename,'Action':'Update','Status':'Fail','Action_List':[{'ActionName':'Document Generation','ScriptName':'GS_R2Q_DocumentGeneration','ErrorMessage':str(ex)}]}
    res =  RestClient.Post(excel_Url, RestClient.SerializeToJson(str(final_request_body)),header)
    Log.Info('GS_R2Q_DocumentGeneration =>> Req: {} -- Res: {}'.format(final_request_body, res))