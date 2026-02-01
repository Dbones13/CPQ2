def R2qrecall(Quote,editval,mir2qedi):
    #isR2Qquote = True if Quote.GetCustomField("isR2QRequest").Content else False
    #checkproduct = Quote.GetGlobal('checkproduct')
    if  editval=='True':
        if mir2qedi=='True':
            Quote.ExecuteAction(3202)
        '''if checkproduct == 'Migration':
            ScriptExecutor.Execute('GS_R2Q_Travel_and_living_cost')'''
        ScriptExecutor.Execute('GS_R2Q_Calculatereprice')
        Quote.ExecuteAction(3202)
        Quote.Save(False)
        #Quote.ExecuteAction(3235)
        Quote.ExecuteAction(3215)
        Log.Info('ExecuteAction3232 --  Script End --')