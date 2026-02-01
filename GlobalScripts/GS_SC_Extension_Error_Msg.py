def Extension_Func(Quote):
    if Quote.GetCustomField('Quote Type').Content == 'Contract Renewal':
        from GS_SC_ErrorMessages import MessageHandler
        MsgHandler = MessageHandler(Quote)
        MsgHandler.DeleteMessageByName("Term_Duration_Error_Msg")
        if Quote.GetCustomField("SC_CF_IS_CONTRACT_EXTENSION").Content == 'True':
            one_month = UserPersonalizationHelper.CovertToDate(Quote.GetCustomField('SC_CF_CURANNDELSTDT').Content).AddMonths(1).AddDays(-1)
            two_month = UserPersonalizationHelper.CovertToDate(Quote.GetCustomField('SC_CF_CURANNDELSTDT').Content).AddMonths(2).AddDays(-1)
            three_month = UserPersonalizationHelper.CovertToDate(Quote.GetCustomField('SC_CF_CURANNDELSTDT').Content).AddMonths(3).AddDays(-1)
            if UserPersonalizationHelper.CovertToDate(Quote.GetCustomField("SC_CF_CURANNDELENDT").Content) not in [one_month,two_month,three_month]:
                Error_msg = "Kindly review the current annual deliverable dates, extension period can be 1 month, 2 months or maximum up to 3 months."
                MsgHandler.AddMessage("Term_Duration_Error_Msg", "Error",Error_msg,2)
                return 0
            else:
                return 1