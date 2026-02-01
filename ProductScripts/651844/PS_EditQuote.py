Log.Info('PS_EditQuote --  Started --')

if Quote.GetCustomField('R2Q_Save').Content == 'Submit':
	#Customer_Budget
	Session['editsession']="True"
	QuoteHelper.Edit(str(Session['R2Q_CompositeNumber']))
	'''ScriptExecutor.Execute('GS_R2Q_Calculatereprice')
	Quote.ExecuteAction(3221)
	Quote.ExecuteAction(3232)'''