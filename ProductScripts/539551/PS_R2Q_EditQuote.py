import GS_R2Q_FunctionalUtil
#import GS_R2Q_AUDIT_TABLE
import GS_APIGEE_Integration_Util

Log.Info('PS_EditQuote --  Started --')
def ErrorHandling(action, error_code, error_desc):
	try:
		if action.isdigit():
			Quote.ExecuteAction(int(action))
		else:
			ScriptExecutor.Execute(action)
	except Exception as ex:
		Log.Write("Exception occured as follows:
{0}".format(ex))
		error_details = {"ErrorCode": error_code, "ErrorDescription": "Failed at: "+str(error_desc)}
		msg = 'Error Occured, '+str(error_details)
		GS_R2Q_FunctionalUtil.UpdateStatusMessage(Quote, "Error", "Notification", msg)
		raise

if Quote.GetCustomField("isR2QRequest").Content == 'Yes' and Quote.GetCustomField("R2Q_Save").Content == 'Submit' and Quote.GetGlobal('VrtMappingFlag') != "True" and Quote.GetGlobal('R2Q_UpdateProduct') != "True":
	Session['editsession']="True"
	Session['r2qreprice']="True"
	excel_Url, header = GS_APIGEE_Integration_Util.GetR2QAPIGEEAuthDetails()
	final_request_body={'QuoteNumber': str(Quote.CompositeNumber),'CartId':str(Quote.QuoteId),'RevisionNumber': str(Quote.RevisionNumber),'UserName':str(User.UserName),'Module': 'Migration','Action': 'New', 'Action_List': []}
	if Product.Attr('MSID_Selected_Products').GetValue().Contains("Virtualization System"):
		final_request_body['Action_List'].append({'ActionName':'Virtualization System','ScriptName':'GS_R2Q_VirtualizationSystem_Parts'})
	#ScriptExecutor.Execute('GS_R2Q_Travel_and_living_cost')
	#final_request_body['Action_List'].append({'ActionName':'Travel and Living','ScriptName':'GS_R2Q_Travel_and_living_cost'})
	final_request_body['Action_List'].append({'ActionName':'UpdateProduct','ScriptName':'GS_R2Q_UpdateProduct'})
	final_request_body['Action_List'].append({'ActionName':'Reprice','ScriptName':'GS_R2QPRJT_Reprice_Documentations'})
	final_request_body['Action_List'].append({'ActionName':'Document Generation','ScriptName':'GS_R2Q_DocumentGeneration'})
	Log.Write('final_request_body -->>'+str(final_request_body))
	RestClient.Post(excel_Url, RestClient.SerializeToJson(str(final_request_body)),header)
	Log.Info('R2Q_Save value: '+str(Quote.GetCustomField("R2Q_Save").Content))
	Log.Info('PS_EditQuote --  Ended--')
