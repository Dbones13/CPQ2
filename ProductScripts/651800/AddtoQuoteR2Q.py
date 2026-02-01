if Quote.GetCustomField('R2QFlag').Content == 'Yes':
	from GS_SetDefaultPricePlan import setDefaultMpa
	setDefaultMpa(Quote,TagParserQuote)
Quote.Save(False)

import GS_R2Q_FunctionalUtil
if Quote.GetCustomField("isR2QRequest").Content == 'Yes' and Quote.GetCustomField("R2Q_Save").Content == 'Submit':
	Session['editsession']="True"
	#Session['r2qreprice']="True"
	QuoteHelper.Edit(str(Session['R2Q_CompositeNumber']))
	try:
		Quote.ExecuteAction(3202)
		ScriptExecutor.Execute('GS_R2Q_Calculatereprice')
		Quote.ExecuteAction(3202)
		Quote.Save(False)
	except Exception as ex:
		msg = 'Error Occured, {"ErrorCode": "DiscountPricing", "ErrorDescription": "Failed at: Discounting/Reprice"}'
		GS_R2Q_FunctionalUtil.UpdateStatusMessage(Quote, "Error", "Notification", msg)
		raise
	Quote.ExecuteAction(3215) #Trigger_R2Q_Doc_To_SFDC