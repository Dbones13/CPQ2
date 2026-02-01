if Product.Attr('R2QRequest').GetValue() != 'Yes':
	from GS_CyberProductModule import CyberProduct

	cyber = CyberProduct(Quote, Product, TagParserQuote)
	cont = Product.GetContainerByName('Cyber_Labor_Project_Management')
	for row in cont.Rows:
		if row["Deliverable"] != 'Total':
			cyber.populateCost(row)
	cont.Calculate()
	cyber.populateActivityListPricing('Cyber_Labor_Project_Management')
	cyber.project_management_total()