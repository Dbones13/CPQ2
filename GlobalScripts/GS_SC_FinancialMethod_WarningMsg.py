from GS_SC_ErrorMessages import MessageHandler
MsgHandler = MessageHandler(Quote)
pp=Quote.GetCustomField('SC_CF_Error_Msg').Content
if TagParserQuote.ParseString("<*CTX( Quote.CustomField(Quote Type) )*>") in ['Contract Renewal']:
	if (Quote.GetCustomField('Total Sell Price(USD)').Content[:3])=="USD":
		total_sell_price=(Quote.GetCustomField('Total Sell Price(USD)').Content[4:]).replace(",", "")
	else:
		total_sell_price = Quote.GetCustomField("Total Sell Price(USD)").Content.replace(",", "")
	kk = MsgHandler.DeleteMessageByName("FIN_APP_VALIDATION")
	if float(total_sell_price) > 500000 and Quote.GetCustomField("SC_CF_FIN_APPROVAL_METHOD").Content != 'eGap':
		kk = MsgHandler.AddMessage("FIN_APP_VALIDATION", "Info", "Approval method should eGAP as the total amount is greater or equal to $5M", 2)
	elif float(total_sell_price) > 0 and float(total_sell_price) < 500000 and Quote.GetCustomField("SC_CF_FIN_APPROVAL_METHOD").Content != 'SEA':
		kk = MsgHandler.AddMessage("FIN_APP_VALIDATION", "Info", "Approval method should be SEA as the total amount is less than $5M", 2)
	else:
		kk = MsgHandler.DeleteMessageByName("FIN_APP_VALIDATION")
'''
if TagParserQuote.ParseString("<*CTX( Quote.CustomField(Quote Type) )*>") in ['Contract Renewal']:
    Quote.Messages.Clear()
    Quote.GetCustomField("SC_CF_FIN_APP_VALIDATION").Content = ''
    total_sell_price = Quote.GetCustomField("Total Sell Price(USD)").Content.replace(",", "")
    if float(total_sell_price) > 500000 and Quote.GetCustomField("SC_CF_FIN_APPROVAL_METHOD").Content != 'eGap':
        Quote.GetCustomField("SC_CF_FIN_APP_VALIDATION").Content = 'Warning: The approval method should be eGap as the total sell price is greater than $500k'
    elif float(total_sell_price) < 500000 and Quote.GetCustomField("SC_CF_FIN_APPROVAL_METHOD").Content != 'SEA':
        Quote.GetCustomField("SC_CF_FIN_APP_VALIDATION").Content = 'Warning: The approval method should be SEA as the total sell price is less than $500k'
    elif float(total_sell_price) > 500000 and Quote.GetCustomField("SC_CF_FIN_APPROVAL_METHOD").Content == 'eGap':
        Quote.GetCustomField("SC_CF_FIN_APP_VALIDATION").Content = ''
    elif float(total_sell_price) < 500000 and Quote.GetCustomField("SC_CF_FIN_APPROVAL_METHOD").Content == 'SEA':
        Quote.GetCustomField("SC_CF_FIN_APP_VALIDATION").Content = ''
'''