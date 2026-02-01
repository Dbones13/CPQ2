if (Quote.GetCustomField('IsR2QRequest').Content == 'Yes' and Quote.GetCustomField('R2Q_Save').Content == 'Submit') or (Quote.GetCustomField('R2QFlag').Content == 'Yes' and Quote.GetCustomField('IsR2QRequest').Content!= 'Yes'):
    Log.Info('PS_EditQuote HCI --  Started --')
    Session['editsession']="True"
    #Session['r2qreprice']="True"
    QuoteHelper.Edit(str(Session['R2Q_CompositeNumber']))
    #Quote.ExecuteAction(3203)
    Quote.ExecuteAction(3202)
    ScriptExecutor.Execute('GS_R2Q_Calculatereprice')
    Quote.ExecuteAction(3202)
    #Quote.Calculate(1)
    Quote.Save(False)
    if Quote.GetCustomField('IsR2QRequest').Content == 'Yes':
        Quote.ExecuteAction(3215)