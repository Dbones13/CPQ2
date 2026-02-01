def readonlyQuoteTableColumn(table,column):
	table.GetColumnByName(column).AccessLevel = table.AccessLevel.ReadOnly

def readonlyQuoteTableColList(quote):
	Quote_Details = quote.QuoteTables["Quote_Details"]
	Product_Line_Details = quote.QuoteTables["Product_Line_Details"]
	Product_Line_Sub_Group_Details = quote.QuoteTables["Product_Line_Sub_Group_Details"]
	Product_Type_Details = quote.QuoteTables["Product_Type_Details"]
	readonlyQuoteTableColumn(Quote_Details,"PROS_Guidance_Recommended_Price")
	readonlyQuoteTableColumn(Product_Line_Details,"PROS_Guidance_Recommended_Price")
	readonlyQuoteTableColumn(Product_Line_Sub_Group_Details,"PROS_Guidance_Recommended_Price")
	readonlyQuoteTableColumn(Product_Type_Details,"PROS_Guidance_Recommended_Price")

def hideQuoteTableColumn(table,column):
	table.GetColumnByName(column).AccessLevel = table.AccessLevel.Hidden
def user_epga(quote,User):
	BookingLOB=quote.GetCustomField("Quote Tab Booking LOB").Content
	QuoteType=quote.GetCustomField("Quote Type").Content
	MPA = quote.GetCustomField("MPA").Content

	if (BookingLOB in ("LSS", "PAS", "HCP", "PMC")) and QuoteType == "Projects" and User.BelongsToPermissionGroup('Estimator-ProsGuidanceAccess') and MPA =='':
		readonlyQuoteTableColList(quote)
		if BookingLOB == "PMC":
			quote.GetCustomField('PROS Guidance Recommendation').Visible = True
		else:
			quote.GetCustomField('PROS Guidance Recommendation').Visible = False
	elif BookingLOB == "PMC" and QuoteType in ("Parts and Spot", "Products") and User.BelongsToPermissionGroup('Estimator-ProsGuidanceAccess') and MPA =='':
		readonlyQuoteTableColList(quote)
		quote.GetCustomField('PROS Guidance Recommendation').Visible = True
def hideqtcolumn(quote):
	Quote_Details = quote.QuoteTables["Quote_Details"]
	Product_Line_Details = quote.QuoteTables["Product_Line_Details"]
	Product_Line_Sub_Group_Details = quote.QuoteTables["Product_Line_Sub_Group_Details"]
	Product_Type_Details = quote.QuoteTables["Product_Type_Details"]
	hideQuoteTableColumn(Quote_Details,"PROS_Guidance_Recommended_Price")
	hideQuoteTableColumn(Product_Line_Details,"PROS_Guidance_Recommended_Price")
	hideQuoteTableColumn(Product_Line_Sub_Group_Details,"PROS_Guidance_Recommended_Price")
	hideQuoteTableColumn(Product_Type_Details,"PROS_Guidance_Recommended_Price")
	#quote.GetCustomField('PROS Guidance Recommendation').Visible = False