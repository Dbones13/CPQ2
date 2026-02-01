def GetQuoteTable(Name):
	return Quote.QuoteTables[Name]

def getCFValue(cfName):
	return Quote.GetCustomField(cfName).Content

def setAccessReadonly(table):
	table.AccessLevel = table.AccessLevel.ReadOnly
	table.Save()

# def setAccessEditable(table):
#     table.AccessLevel = table.AccessLevel.Editable

def hideQuoteTableColumn(table,column):
	table.GetColumnByName(column).AccessLevel = table.AccessLevel.Hidden

# def set_SC_PricingSummary_Cells_ReadOnly():
#     table =  Quote.QuoteTables["Pricing_Summary"]
#     sYear  = str(UserPersonalizationHelper.CovertToDate(Quote.GetCustomField("EGAP_Contract_Start_Date").Content).Year)
#     for row in table.Rows:
#         if sYear not in row['Year']:
#             for cell in row.Cells:
#                 Trace.Write(cell.ColumnName)
#                 if cell.ColumnName in ('MPA_Discount_', 'Other_Discount_'):
#                     cell.AccessLevel =  cell.AccessLevel.ReadOnly
#                 elif cell.ColumnName in ('Escalation'):
#                     cell.AccessLevel =  cell.AccessLevel.Editable
#         else:
#             for cell in row.Cells:
#                 if cell.ColumnName in ('Escalation'):
#                     cell.AccessLevel =  cell.AccessLevel.ReadOnly
#                     break
#     table.Save()

if Quote.OrderStatus.Name != 'Preparing':
	setAccessReadonly(GetQuoteTable('Quote_Details'))
	setAccessReadonly(GetQuoteTable('Product_Line_Details'))
	setAccessReadonly(GetQuoteTable('Product_Line_Sub_Group_Details'))
	setAccessReadonly(GetQuoteTable('Product_Type_Details'))
	setAccessReadonly(GetQuoteTable('Cash_Outflow'))
	setAccessReadonly(GetQuoteTable('EGAP_Project_Milestone'))
	setAccessReadonly(GetQuoteTable('Payment_MileStones'))

productTypeTable =  GetQuoteTable("Product_Type_Details")
productLineSubGroupDetails = GetQuoteTable("Product_Line_Sub_Group_Details")
productlineDetails =  GetQuoteTable("Product_Line_Details")
quoteDetails =  GetQuoteTable("Quote_Details")

if getCFValue("Booking LOB") == "PMC" and getCFValue("Quote Type") == "Parts and Spot":
	hideQuoteTableColumn(quoteDetails,"Negotiation_Limit")
	hideQuoteTableColumn(quoteDetails,"Walk_away_Sales_Price")

	if not User.BelongsToPermissionGroup('PMC WTW Cost Access Group'):
		hideQuoteTableColumn(quoteDetails,"Quote_WTW_Cost")
		hideQuoteTableColumn(quoteDetails,"Quote_WTW_Margin_Percent")
		hideQuoteTableColumn(quoteDetails,"Quote_WTW_Margin_Amount")
		hideQuoteTableColumn(productTypeTable,"WTW_Cost")
		hideQuoteTableColumn(productLineSubGroupDetails,"PLSG_WTW_Cost")
		hideQuoteTableColumn(productlineDetails,"PL_WTW_Cost")