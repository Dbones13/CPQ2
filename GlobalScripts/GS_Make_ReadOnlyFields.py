from GS_CommonModule import GetQuoteTable,setAccessReadonly,hideQuoteTableColumn

def readonly(Quote):
	setAccessReadonly(GetQuoteTable(Quote,'Quote_Details'))
	setAccessReadonly(GetQuoteTable(Quote,'Product_Line_Details'))
	setAccessReadonly(GetQuoteTable(Quote,'Product_Line_Sub_Group_Details'))
	setAccessReadonly(GetQuoteTable(Quote,'Product_Type_Details'))
	setAccessReadonly(GetQuoteTable(Quote,'Cash_Outflow'))
	setAccessReadonly(GetQuoteTable(Quote,'EGAP_Project_Milestone'))
	setAccessReadonly(GetQuoteTable(Quote,'Payment_MileStones'))

def hidecol(Quote, User):
	productTypeTable =  GetQuoteTable(Quote,"Product_Type_Details")
	productLineSubGroupDetails = GetQuoteTable(Quote,"Product_Line_Sub_Group_Details")
	productlineDetails =  GetQuoteTable(Quote,"Product_Line_Details")
	quoteDetails =  GetQuoteTable(Quote,"Quote_Details")
	hideQuoteTableColumn(quoteDetails,"Negotiation_Limit")
	hideQuoteTableColumn(quoteDetails,"Walk_away_Sales_Price")

	if not User.BelongsToPermissionGroup('PMC WTW Cost Access Group'):
		hideQuoteTableColumn(quoteDetails,"Quote_WTW_Cost")
		hideQuoteTableColumn(quoteDetails,"Quote_WTW_Margin_Percent")
		hideQuoteTableColumn(quoteDetails,"Quote_WTW_Margin_Amount")
		hideQuoteTableColumn(productTypeTable,"WTW_Cost")
		hideQuoteTableColumn(productLineSubGroupDetails,"PLSG_WTW_Cost")
		hideQuoteTableColumn(productlineDetails,"PL_WTW_Cost")