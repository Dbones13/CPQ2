if Quote.GetCustomField('Quote Type').Content in ('Contract New','Contract Renewal'):
	for item in Quote.MainItems:
		if item.ExtendedListPrice !=0:
			mpaDiscount = (item.ExtendedListPrice * item.QI_MPA_Discount_Percent.Value) / 100
			if (item.QI_SC_ExpectedTotalDiscountAmount.Value != 0) and (item.QI_SC_ExpectedTotalDiscountAmount.Value<=item.ListPrice):
				amount = float(item.QI_SC_ExpectedTotalDiscountAmount.Value)
				mpaDiscount = (item.ExtendedListPrice * item.QI_MPA_Discount_Percent.Value) / 100
				additionalDiscount = amount - mpaDiscount
				additionaldiscountpercentage  = (additionalDiscount*100)/item.ExtendedListPrice
				item.QI_Additional_Discount_Percent.Value = additionaldiscountpercentage
				item.DiscountAmount = item.QI_SC_ExpectedTotalDiscountAmount.Value
				item.DiscountPercent = (100 * item.DiscountAmount) / item.ExtendedListPrice
				item.QI_SC_Total_Discount_Percent.Value = item.DiscountPercent
				item.QI_SC_Total_Discount_Price.Value = (Quote.SelectedMarket.CurrencySign if Quote.GetCustomField('SC_CF_PRICE_TOGGLE').Content != 'USD' else '$') + ' ' + (UserPersonalizationHelper.ToUserFormat(round(item.DiscountAmount/float(Quote.GetCustomField('SC_CF_EXCHANGE_RATE').Content),2)) if Quote.GetCustomField('SC_CF_PRICE_TOGGLE').Content == 'USD' else UserPersonalizationHelper.ToUserFormat(round(item.DiscountAmount,2)))
				item.QI_SC_ExpectedTotalDiscountAmount.Value = 0
			else:
				item.QI_SC_ExpectedTotalDiscountAmount.Value = 0