import GS_APIGEE_Integration_Util

Log.Info('GS_R2QPRJT_Reprice Param-->>'+str(Param))
excel_Url, header = GS_APIGEE_Integration_Util.GetR2QAPIGEEAuthDetails()
try:
	QuoteNumber = Param.QuoteNumber
	Quote = QuoteHelper.Edit(QuoteNumber)
	if next((False for item in Quote.MainItems if item.IsComplete == False), True):
		if Quote.GetCustomField('R2Q_Save').Content == 'Submit':
			Quote.SetGlobal('PerformanceUpload', "")
			checkproduct = Quote.GetGlobal('checkproduct')
			Quote.ExecuteAction(3202)
			#if checkproduct == 'Migration':
				#ScriptExecutor.Execute('GS_R2Q_Travel_and_living_cost')
			ScriptExecutor.Execute('GS_R2Q_Calculatereprice')
			Quote.ExecuteAction(3202)
			Quote.Save(False)
			Quote.ExecuteAction(3214)
			Session['r2qreprice']=''
			Log.Info('ExecuteAction3232 --  Script End --')
		final_request_body={'QuoteNumber':str(Param.QuoteNumber),'CartId':str(Param.CartId),'RevisionNumber': str(Param.RevisionNumber),'UserName':str(User.UserName),'Module':'New/Expansion','Action':'Update','Status':'Success','Action_List':[{'ActionName':'Reprice','ScriptName':'GS_R2QPRJT_Reprice_Documentations'}]}
		RestClient.Post(excel_Url, RestClient.SerializeToJson(str(final_request_body)),header)
		Log.Info('GS_R2QPRJT_Reprice Success')
	else:
		Log.Info('GS_R2QPRJT_Reprice Fail-->> Quote has incomplete products')
		final_request_body={'QuoteNumber':str(Param.QuoteNumber),'CartId':str(Param.CartId),'RevisionNumber': str(Param.RevisionNumber),'UserName':str(User.UserName),'Module':'New/Expansion','Action':'Update','Status':'Fail','Action_List':[{'ActionName':'Reprice','ScriptName':'GS_R2QPRJT_Reprice_Documentations','ErrorMessage':'Quote has incomplete products'}]}
		RestClient.Post(excel_Url, RestClient.SerializeToJson(str(final_request_body)),header)
except Exception as ex:
	Log.Info('GS_R2QPRJT_Reprice Fail-->>'+str(ex))
	final_request_body={'QuoteNumber':str(Param.QuoteNumber),'CartId':str(Param.CartId),'RevisionNumber': str(Param.RevisionNumber),'UserName':str(User.UserName),'Module':'New/Expansion','Action':'Update','Status':'Fail','Action_List':[{'ActionName':'Reprice','ScriptName':'GS_R2QPRJT_Reprice_Documentations','ErrorMessage':str(ex)}]}
	RestClient.Post(excel_Url, RestClient.SerializeToJson(str(final_request_body)),header)