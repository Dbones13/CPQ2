if Quote.GetCustomField("isR2QRequest").Content =='Yes':
	Product.Attr('R2QRequest').AssignValue('Yes')
	Product.Attr("R2Q_QuoteNumber").AssignValue(str(Quote.CompositeNumber))
	Product.Attr('FDM_Upgrade_Select_desired_FDM_release').SelectDisplayValue('FDM R520')
	Product.Attr('FDM_Upgrade_What_is_the_current_release').SelectDisplayValue('FDM R500')