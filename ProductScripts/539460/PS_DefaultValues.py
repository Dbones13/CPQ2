if Quote.GetCustomField("isR2QRequest").Content =='Yes':
	Product.Attr('R2QRequest').AssignValue('Yes')
	Product.Attr("R2Q_QuoteNumber").AssignValue(str(Quote.CompositeNumber))
	if(Product.Attr('xPM_Select_the_migration_scenario').GetValue() != 'xPM to EHPM'):
		TagParserProduct.ParseString('<*CTX( Container(xPM_Migration_Config_Cont).Column(xPM_Number_of_Red_EHPM_Non_Exp_connected).SetPermission(Editable)) *>')