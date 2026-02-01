def market_customer_r2q(Quote):
	isR2Qquote  = True if Quote.GetCustomField("isR2QRequest").Content else False
	discount = 0
	if isR2Qquote:
		Log.Info("R2Q_Custbudgetcalculation")
		quoteTotalTable = Quote.QuoteTables["Quote_Details"]
		row = quoteTotalTable.Rows[0]
		Log.Info("Max_Quote_Discount_Amount===> "+str(row['Max_Quote_Discount_Amount']))
		#if  row["Max_Quote_Discount_Amount"]!='' and float(row["Max_Quote_Discount_Amount"])>0:
		if Quote.GetCustomField("SellPricestrategy").Content=='Market Price':
			row['Quote_WTW_Margin_Percent']=40
			percent= 40
			cost= row["Quote_WTW_Cost"]
			sellPrice= (100 * cost) / (100 - percent)
			discount= row['Quote_List_Price'] - sellPrice - row['MPA_Discount_Amount']
			Log.Info("WTW Margin===> "+str(row['Quote_WTW_Margin_Percent']))
		else:
			if Quote.GetCustomField("CustomerBudget").Content:
				sellPrice = int(Quote.GetCustomField("CustomerBudget").Content)
				row['Quote_Sell_Price']=sellPrice
				sellPrice = row["Quote_Sell_Price"]
				discount= row['Quote_List_Price'] - (sellPrice - row['GAS_ETO_Price']) - row['MPA_Discount_Amount']
				Log.Info("SellPrice===> "+str(row["Quote_Sell_Price"]))
		if discount !=0:
			newpercent = (discount * 100) / row["Max_Quote_Discount_Amount"] if row["Max_Quote_Discount_Amount"] >0 else 0.00
			row["New_Discount"] = newpercent
			#quoteTotalTable.Save()
			#Log.Info("R2Q_Custbudgetcalculationend")
			#quoteTotalTable.Save()
			#Quote.ExecuteAction(3221)
			#Log.Info("R2Q_Custbudgetcalculationend")
			#Quote.Calculate(17)
		quoteTotalTable.Save()
		Log.Info("R2Q_Custbudgetcalculationend")