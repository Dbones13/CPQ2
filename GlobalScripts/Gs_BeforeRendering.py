'''if Session["prevent_execution"] == "true":
	Session["prevent_execution"] = "false"
	Quote.Calculate(2)
if str(Quote.GetCustomField("Q_CF_PROJFLAG").Content) == 'TRUE':
	for actions in Quote.Actions:
		if str(actions.Name) == 'Place order to ERP':
			Quote.ExecuteAction(actions.Id)
			Quote.GetCustomField("Q_CF_PROJFLAG").Content = ''
			Quote.Save(False)
			break
#ScriptExecutor.Execute('GS_GetQuoteStatus')'''