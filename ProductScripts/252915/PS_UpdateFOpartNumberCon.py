if Quote.GetCustomField('ChangeLaborCurrency').Content == 'True':
    Log.Write("Price change script executed")
    ScriptExecutor.Execute('GS_PopulatePartNumberContainer', {'Product': Product})
    ScriptExecutor.Execute('GS_PopulateGESCost', {'Product': Product})