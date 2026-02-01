if Quote.GetCustomField('IsR2QRequest').Content == 'Yes':
	import datetime
	from GS_R2Q_Product_Attribute_ContColms import MigrationProductsAttributesContainerColumns as PRD
	
	current_year = datetime.datetime.now().year
	yearlist = [str(current_year + n) for n in range(0,3)]
	yearRemovelist = [year.ValueCode for year in Product.Attr("Project_Execution_Year").Values if year.ValueCode not in yearlist]
	
	pole = Quote.GetCustomField('R2Q_Booking_Pole').Content

	countryRemoveList = [country.ValueCode for country in Product.Attr("R2Q_Alternate_Execution_Country").Values if country.ValueCode not in PRD.products[Product.Name].get(pole, [])]
	langremovelist = ["German"]
	Product.DisallowAttrValues('R2Q_PRJT_Proposal Language', *langremovelist)
	Product.DisallowAttrValues('Project_Execution_Year', *yearRemovelist)
	Product.DisallowAttrValues("R2Q_Alternate_Execution_Country", *countryRemoveList)
	proposal = Product.Attr('R2Q_PRJT_Proposal Language').GetValue()
	quoteprop = Quote.GetCustomField("R2Q_PRJT_Proposal Language").Content
	if proposal != quoteprop : 
		Quote.GetCustomField("R2Q_PRJT_Proposal Language").Content = Product.Attr('R2Q_PRJT_Proposal Language').GetValue()
	if Product.Attr('Sell Price Strategy').SelectedValue.Display != 'Customer Budget':
		Product.Attr('Customer_Budget_TextField').Access = AttributeAccess.Hidden
		Product.Attr('Customer_Budget_USD').Access = AttributeAccess.Hidden
	else:
		Product.Attr('Customer_Budget_USD').Access = AttributeAccess.ReadOnly
	allowlist = [country.ValueCode for country in Product.Attr("R2Q_Alternate_Execution_Country").Values if country.ValueCode in PRD.products[Product.Name].get(pole, [])]
	alncntry_length = len(allowlist)
	if Product.Attr("R2Q_Alternate_Execution_Country").GetValue() != Quote.GetCustomField("R2Q_Alternate_Execution_Country").Content and alncntry_length !=1:
		Product.Attributes.GetByName('R2Q_Alternate_Execution_Country').SelectDisplayValue("None")
	else:
		if alncntry_length == 1:
			Product.Attributes.GetByName('R2Q_Alternate_Execution_Country').SelectDisplayValue(allowlist[0])
		else:
			Product.Attributes.GetByName('R2Q_Alternate_Execution_Country').SelectDisplayValue(Quote.GetCustomField("R2Q_Alternate_Execution_Country").Content)
else:
	Product.DisallowAttr('Customer_Budget_USD')