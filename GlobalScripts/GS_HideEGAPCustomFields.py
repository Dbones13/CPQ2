def GetQuoteTable(Name):
	return Quote.QuoteTables[Name]

def hideQuoteTableColumn(table,column):
	table.GetColumnByName(column).AccessLevel = table.AccessLevel.Hidden

def hideDropdownValues(customField,hiddenValueList):
	for value in customField.AttributeValues:
		if value.DisplayValue in hiddenValueList:
			value.Allowed = False

quoteDetails =  GetQuoteTable("Quote_Details")

bookingLOB = Quote.GetCustomField("Quote Tab Booking LOB")
quoteType = Quote.GetCustomField("Quote Type").Content
quoteTableCountryOfOrigin = GetQuoteTable('Country_of_Origin')
quoteTablePaymentMileStones = GetQuoteTable('Payment_MileStones')

if quoteType not in ("Contract New","Contract Renewal", "Projects") and bookingLOB.Content in ("PMC", "LSS"):
	Quote.CustomFields.Disallow('EGAP_Proposal_Type','EGAP_Project_Type','EGAP_Contract_Start_Date','EGAP_Contract_End_Date','EGAP_Project_Duration_Months','EGAP_Project_Duration_Weeks','Functional Currency of Entity')

if bookingLOB.Content == "LSS" and quoteType not in ("Projects", "Contract New","Contract Renewal"):
	Quote.CustomFields.Disallow('Warranty','Delivery Terms- Additional Info','Final Destination','Holding charges/Order change fee','Document Format','PMC BOM')
	quoteTableCountryOfOrigin.AccessLevel = quoteTableCountryOfOrigin.AccessLevel.Hidden
	quoteTablePaymentMileStones.AccessLevel = quoteTablePaymentMileStones.AccessLevel.Hidden
	hideQuoteTableColumn(quoteDetails,"Negotiation_Limit")
	hideQuoteTableColumn(quoteDetails,"Walk_away_Sales_Price")

paymentTerms = Quote.GetCustomField("Payment Terms")
if quoteType == 'Projects':
	hideDropdownValues(paymentTerms,['COD'])
elif quoteType == 'Parts and Spot':
	hideDropdownValues(paymentTerms,['0', '15', '75', '120', '150', 'COD'])