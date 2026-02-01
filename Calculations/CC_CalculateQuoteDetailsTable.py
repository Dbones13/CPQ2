if Session["prevent_execution"] != "XXX" and Quote.GetGlobal('PerformanceUpload') != 'Yes':
	import GS_CalculateTotals
	totalDict = GS_CalculateTotals.calculateQuoteTotals(Quote)

	quoteTotalTable = Quote.QuoteTables["Quote_Details"]

	if quoteTotalTable.Rows.Count == 0:
		row = quoteTotalTable.AddNewRow()
	else:
		row = quoteTotalTable.Rows[0]

	row['Quote_List_Price'] 			= totalDict.get('totalListPrice' , 0)
	row['Quote_Regional_Cost'] 			= totalDict.get('totalCost' , 0)
	row['Quote_WTW_Cost'] 				= totalDict.get('totalWTWCost',0)
	row['Quote_Sell_Price']				= totalDict.get('totalExtendedAmount',0) + totalDict.get("totalETOPrice" , 0)
	row['MPA_Discount_Amount'] 			= totalDict.get('mpaDiscountAmount' , 0)
	row['Quote_Discount_Amount'] 		= totalDict.get('additionalDiscountAmount' , 0)
	row['Quote_Regional_Margin_Amount'] = totalDict.get('totalRegionalMargin' , 0)
	row['PROS_Guidance_Recommended_Price'] = totalDict.get('PROSRecommendedPrice' , 0)
	row['Quote_WTW_Margin_Amount']      = totalDict.get('totalExtendedAmount',0) - totalDict.get('totalWTWCost' , 0)
	row['Total_Tariff_Amount'] 			= totalDict.get('totalTariffAmount' , 0)
	row['Quote_Sell_Price_Incl_Tariff'] = totalDict.get('totalSellPriceInclTariff', 0)
	row['Target_Sell_Price']			= totalDict.get('totalListPrice' , 0) + totalDict.get("totalETOPrice" , 0) - totalDict.get('mpaDiscountAmount' , 0)
	row['GAS_ETO_Price']                = totalDict.get("totalETOPrice" , 0)
    
	if totalDict.get('totalListPrice' , 0):
		row['MPA_Discount_percent'] = (totalDict.get('mpaDiscountAmount' , 0) * 100) / totalDict.get('totalListPrice' , 0)
	if row['Target_Sell_Price']:
		row['Quote_Discount_Percent'] = (totalDict.get('additionalDiscountAmount' , 0) * 100) / row['Target_Sell_Price']
	if totalDict.get('totalExtendedAmount' , 0):
		row['Quote_Regional_Margin_Percent'] = (totalDict.get('totalRegionalMargin' , 0) * 100) / totalDict.get('totalExtendedAmount' , 0)
		row['Quote_WTW_Margin_Percent'] = ((totalDict.get('totalExtendedAmount',0) - totalDict.get('totalWTWCost' , 0)) * 100) / totalDict.get('totalExtendedAmount' , 0)
	if Quote.GetCustomField("Booking LOB").Content in ('PAS','LSS','HCP'):
		from GS_CommonConfig import CL_CommonSettings as CS
		minOrderFee = UserPersonalizationHelper.ConvertToNumber(Quote.GetCustomField('Minimum Order Fee').Content) if Quote.GetCustomField('Minimum Order Fee').Content.strip() else 0.0
		row['Total_Sell_Price_incl_appl_Fees_'] = row['Quote_Sell_Price'] + minOrderFee + float(CS.setdefaultvalue["QI_Expedite_Fees"])
		row['Quote_WTW_Margin_Percent'] = ((row['Quote_Sell_Price'] - totalDict.get('totalWTWCost' , 0)) * 100) / row['Quote_Sell_Price']
		Quote.GetCustomField('TotalwtwMarginPercent').Content=str(round(row['Quote_WTW_Margin_Percent'],2))
		Quote.GetCustomField('Total Sell Price').Content=UserPersonalizationHelper.ToUserFormat(row['Quote_Sell_Price'])
		Quote.GetCustomField('Total_Sell_Price_Updated').Content=UserPersonalizationHelper.ToUserFormat(row['Total_Sell_Price_incl_appl_Fees_'])
		Trace.Write("---reg mar%---"+str(row['Quote_Regional_Margin_Percent'])+"-----WTW marg %---"+str(row['Quote_WTW_Margin_Percent']))
	quoteTotalTable.Save()
	#Quote.CalculateAndSaveCustomFields()
Session["ItemGUID"]=[]