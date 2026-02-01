import GS_APIGEE_Integration_Util

excel_Url, header = GS_APIGEE_Integration_Util.GetR2QAPIGEEAuthDetails()
Log.Info('outside = GS_R2Q_Submit_API Param check-->> first '+JsonHelper.Serialize(Param))

try:
	Log.Info('else = GS_R2Q_Submit_API Param check-->> 2 '+str(Param))
	ScriptName = Param.ScriptName
	QuoteNumber = Param.QuoteNumber
	Cartid  = Param.CartId
	RevisionNumber = Param.RevisionNumber
	ActionName = Param.ActionName
	Module = Param.Modulename
	Quote.SetGlobal('PerformanceUpload', "Yes")
	ScriptExecutor.ExecuteGlobal(ScriptName,{'ActionName':ActionName, 'QuoteNumber':QuoteNumber, 'CartId': Cartid,'RevisionNumber': RevisionNumber,'UserName':str(User.UserName),'Module':Module})
except Exception as ex:
	final_request_body={'QuoteNumber':str(Param.QuoteNumber),'CartId':str(Param.CartId),'RevisionNumber': str(Param.RevisionNumber),'UserName':str(User.UserName),'Module':"New/Expansion",'Action':'Update','Status':'Fail','Action_List':[{'ActionName':str(Param.ActionName),'ScriptName':str(Param.ScriptName),'ErrorMessage':str(ex)}]}
	Log.Info('GS_R2Q_Submit_API Error-->>'+str(final_request_body))
	RestClient.Post(excel_Url, RestClient.SerializeToJson(str(final_request_body)),header)
	Log.Info('GS_R2Q_Submit_API Error-->>'+str(ex))