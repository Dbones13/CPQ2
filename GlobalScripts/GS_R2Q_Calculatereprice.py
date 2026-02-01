import GS_APIGEE_Integration_Util

try:
	discount = 0
	current_date = TagParserQuote.ParseString('<*CTX( Date.Format(MM/dd/yyyy) )*>')
	account_id = Quote.GetCustomField("AccountId").Content
	siebel_row_id = TagParserQuote.ParseString('<* QuoteProperty (Siebel Row Id) *>')
	ProductType = Quote.GetCustomField('ProductType').Content
	BookingType = Quote.GetCustomField('Booking LOB').Content

	query_salesforce = ( "SELECT Agreement_Name FROM MPA_ACCOUNT_MAPPING WHERE Salesforce_ID = '" + account_id + "' AND Agreement_Start_Date <= '" + current_date + "' AND (Agreement_End_Date IS NULL OR Agreement_End_Date >= '" + current_date + "')" )
	results_salesforce = SqlHelper.GetFirst(query_salesforce)

	if results_salesforce:
		Quote.GetCustomField("MPA").Content = results_salesforce.Agreement_Name
	else:
		query_account = ( "SELECT Agreement_Name FROM MPA_ACCOUNT_MAPPING WHERE Account_Number = '" + siebel_row_id + "' AND Agreement_Start_Date <= '" + current_date + "' AND (Agreement_End_Date IS NULL OR Agreement_End_Date >= '" + current_date + "')" )
		results_account = SqlHelper.GetFirst(query_account)
		if results_account:
			Quote.GetCustomField("MPA").Content = results_account.Agreement_Name
	query = TagParserQuote.ParseString("select * from MPA_PRICE_PLAN_MAPPING where Honeywell_Ref = '<*CTX(Quote.CustomField(MPA Honeywell Ref))*>' and Honeywell_Ref !='' and Price_Plan_Status= 'Active' and [IF]([EQ](<*CTX( Quote.CustomField(Quote Type) )*>,Projects)){Price_Plan_Systems_Discount}{Price_Plan_Parts_Discount}[ENDIF] = 'Y' and Price_Plan_Start_Date <= '<*CTX( Date.Format(MM/dd/yyyy) )*>' and ( Price_Plan_End_Date  IS NULL  or Price_Plan_End_Date >= '<*CTX( Date.Format(MM/dd/yyyy) )*>')")
	Log.Info("res calculate reprice:"+str(query))
	#from GS_SetDefaultPricePlan import setDefaultMpa
	#setDefaultMpa(Quote,TagParserQuote)
	Log.Info(str(Quote.GetCustomField("CustomerBudget").Content)+"--R2Q_Custbudgetcalculation--->"+str(Quote.GetCustomField("SellPricestrategy").Content))
	quoteTotalTable = Quote.QuoteTables["Quote_Details"]
	row = quoteTotalTable.Rows[0]
	mpaquote = Quote.GetCustomField("MPA").Content
	Log.Info("MPA price plan " +str(Quote.GetCustomField("MPA Price Plan").Content))
	Log.Info("MPA check => "+str(Quote.GetCustomField("MPA").Content))
	Log.Info("Max_Quote_Discount_Amount===> "+str(row['Max_Quote_Discount_Amount']))
	#if  row["Max_Quote_Discount_Amount"]!='' and float(row["Max_Quote_Discount_Amount"])>0:
	if Quote.GetCustomField("SellPricestrategy").Content=='Market Price' and (mpaquote is None or mpaquote == '') and ProductType == 'New/Expansion' and BookingType == 'PAS':
		row['Quote_WTW_Margin_Percent']=40
		percent= 40
		cost= row["Quote_WTW_Cost"]
		sellPrice= (100 * cost) / (100 - percent)
		discount= row['Quote_List_Price'] - sellPrice - row['MPA_Discount_Amount']
		Log.Info("WTW Margin===> "+str(row['Quote_WTW_Margin_Percent']))
	elif Quote.GetCustomField("SellPricestrategy").Content == 'Customer Budget':
		Trace.Write("SellPricestrategy")
		if Quote.GetCustomField("CustomerBudget").Content:
			Trace.Write("CustomerBudget----"+str(Quote.GetCustomField("CustomerBudget").Content)+'--quotelist price-'+str(row['Quote_List_Price']))
			#sellPrice = int(Quote.GetCustomField("CustomerBudget").Content)
			#row['Quote_Sell_Price']=sellPrice
			row['Quote_Sell_Price']=float(Quote.GetCustomField("CustomerBudget").Content)
			sellPrice = float(Quote.GetCustomField("CustomerBudget").Content)
			discount= row['Quote_List_Price'] - (sellPrice - row['GAS_ETO_Price']) - row['MPA_Discount_Amount']
			Log.Info("GAS_ETO_Price===> "+str(row["GAS_ETO_Price"]))
			Log.Info("Quote_List_Price===> "+str(row["Quote_List_Price"]))
			Log.Info(str(row["Max_Quote_Discount_Amount"])+"---discount===> "+str(discount))
			Log.Info("SellPrice===> "+str(row["Quote_Sell_Price"]))

	Log.Info("discount===> "+str(discount))
	if discount !=0 and row["Max_Quote_Discount_Amount"] > 0:
		newpercent = (discount * 100) / row["Max_Quote_Discount_Amount"]
		row["New_Discount"] = newpercent
		Log.Write("new percent in budget-->" +str(row["New_Discount"]))
	quoteTotalTable.Save()
	Log.Info("R2Q_Custbudgetcalculationend")
except Exception as ex:
    Log.Write("GS_R2Q_Calculatereprice Fail-->>"+str(ex))
    excel_Url, header = GS_APIGEE_Integration_Util.GetR2QAPIGEEAuthDetails()
    final_request_body={'QuoteNumber':str(Quote.CompositeNumber),'CartId':str(Quote.QuoteId),'RevisionNumber': str(Quote.RevisionNumber),'UserName':str(User.UserName),'Module':'New/Expansion','Action':'Update','Status':'Fail','Action_List':[{'ActionName':'Reprice','ScriptName':'GS_R2QPRJT_Reprice_Documentations','ErrorMessage':'GS_R2Q_Calculatereprice_'+str(ex)}]}
    RestClient.Post(excel_Url, RestClient.SerializeToJson(str(final_request_body)),header)