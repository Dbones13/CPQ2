'''Quote.Calculate(17)
#CXCPQ-65110: Added condition to improve the performance. calculateCosts not required to run for PMC Parts and Spot Quote and for VC products defined in FME_PARTS table.
import GS_ItemCalculations
BookingLob = Quote.GetCustomField("Booking LOB").Content
Quotetype = Quote.GetCustomField("Quote Type").Content
for Item in Quote.Items:
	if Item.Description == 'Write-In Standard Warranty System':
		if (BookingLob != "PMC" or Quotetype != "Parts and Spot") and Quotetype not in ('Contract New','Contract Renewal'):
			if Item.ProductName!='Productized Skid Quote Item': #For productized skid Items cost is fetched from SAP
				qry = SqlHelper.GetFirst("SELECT 1 as flag from FME_PARTS WHERE PARTNUMBER = '{}'".format(str(Item.PartNumber)))
				if qry is None: #	CXCPQ-69436: Added Qry condition to avoid conflict with  K&E VC materials
					GS_ItemCalculations.calculateCosts(Quote , BookingLob, Quotetype, Item,TagParserQuote)
					Trace.Write('ifff')
		#CXCPQ-80164 : [PMC] Unit WTW cost should be equal to Unit Regional Cost at Quote Line items
		elif (BookingLob == "PMC" and Quotetype == "Parts and Spot"):
			GS_ItemCalculations.calculateCosts(Quote , BookingLob, Quotetype, Item,TagParserQuote)
		Trace.Write("Item.PartNumber3 =="+str(Item.PartNumber)+"==cost=="+str(Item.Cost))
		Item.ExtendedCost = Item.Quantity * Item.Cost
		Item["QI_RegionalMargin"].Value = Item.ExtendedAmount - Item.ExtendedCost
		Item["QI_WTWMargin"].Value = Item.ExtendedAmount - Item["QI_ExtendedWTWCost"].Value
		if Item.ExtendedAmount != 0.00:
			if Item.ExtendedAmount < Item.ExtendedCost:
				Item["QI_RegionalMarginPercent"].Value = 0.0
				Item["QI_WTWMarginPercent"].Value = 0.0
			else:
				Item["QI_RegionalMarginPercent"].Value = (Item["QI_RegionalMargin"].Value / Item.ExtendedAmount) * 100
				Item["QI_WTWMarginPercent"].Value = (Item["QI_WTWMargin"].Value / Item.ExtendedAmount) * 100
		Trace.Write("Item.PartNumber4 =="+str(Item.PartNumber)+"==cost=="+str(Item.Cost))
		#Updates the Quote Tables
		product_line_details = Quote.QuoteTables["Product_Line_Details"]
		product_line_subgroup_details = Quote.QuoteTables["Product_Line_Sub_Group_Details"]
		qtptype = Quote.QuoteTables["Product_Type_Details"]

		extended_cost = Item.ExtendedCost
		extended_wtw_cost = Item.QI_ExtendedWTWCost.Value
		regional_margin = Item.QI_RegionalMargin.Value

		for row in product_line_details.Rows:
			if row['Product_Line_PL_Description'] == 'Non Revenue Generating Project Cost - Warranty and Unpriced Extended Warranty':
				row['PL_Regional_Cost'] = extended_cost
				row['PL_WTW_Cost'] = extended_wtw_cost
				row['PL_Regional_Margin'] = regional_margin

		for row in product_line_subgroup_details.Rows:
			if row['PLSG_Description'] == 'Non Revenue Generating Project Cost - Warranty and Unpriced Extended Warranty':
				row['PLSG_Regional_Cost'] = extended_cost
				row['PLSG_WTW_Cost'] = extended_wtw_cost

		for row in qtptype.Rows:
			if row['Product_Type'] == 'Standard Warranty':
				row['Regional_Cost'] = extended_cost
				row['WTW_Cost'] = extended_wtw_cost
'''
Quote.Calculate()