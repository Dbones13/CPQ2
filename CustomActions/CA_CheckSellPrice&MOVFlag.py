exchangeRate = Quote.GetCustomField('Exchange Rate').Content if Quote.GetCustomField('Exchange Rate').Content.strip() !='' else 1.0
sellPrice	 = float(UserPersonalizationHelper.ConvertToNumber(Quote.GetCustomField("Total_Sell_Price_Updated").Content))
requiredSellPrice = round(float (0.0 * float(exchangeRate)), 2)

if sellPrice < requiredSellPrice and Quote.GetCustomField("Minimum Order Fee Waiver").Content != 'True' and not(Quote.GetCustomField("Minimum Order fee Waiver reason").Content) :
    WorkflowContext.BreakWorkflowExecution = True
    if not Quote.Messages.Contains(Translation.Get('Errormessage.CheckForMinimumSellprice')):
        Quote.Messages.Add(Translation.Get('Errormessage.CheckForMinimumSellprice'))