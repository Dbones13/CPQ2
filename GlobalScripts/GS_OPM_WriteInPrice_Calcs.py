if Session["prevent_execution"] != "true":
	# Initialize variables
	opm_lp = 0
	opm_dis = 0
	sesp_lp = 0
	sesp_dis = 0

	# Calculate opm_lp, opm_dis, sesp_lp, sesp_dis in one loop
	for item in Quote.MainItems:
		if item.ProductName == "OPM":
			opm_lp = item.ListPrice * 0.05
			opm_dis = item.QI_MPA_Discount_Percent.Value
		elif item.ProductName == "Non-SESP Exp Upgrade":
			sesp_lp = item.ListPrice * 0.05
			sesp_dis = item.QI_MPA_Discount_Percent.Value

	# Calculate totals
	opm_tot = opm_lp - (opm_lp * (opm_dis / 100))
	sesp_tot = sesp_lp - (sesp_lp * (sesp_dis / 100))
	writeIn_lp = opm_tot + sesp_tot

	children_to_update = {
		child: writeIn_lp
		for item in Quote.MainItems
		if item.ProductName == "OPM"
		for child in item.Children
		if child.PartNumber == "Write-in Site Support Labor"
	}

	# Update ListPrice for the children in the dictionary
	for child, price in children_to_update.items():
		child.ListPrice = price