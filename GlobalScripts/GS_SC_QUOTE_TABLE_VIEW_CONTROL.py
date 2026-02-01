def SC_QUOTE_TABLE_VIEW_CONTROL(quote):
## Added logic to Hide Service Contracts Quote table for other Quote types - Hilarian 30/08/2023
	def setAccessHidden(table):
		table.AccessLevel = table.AccessLevel.Hidden

	def editableQuoteTableColumn(table,column):
		table.GetColumnByName(column).AccessLevel = table.AccessLevel.Editable

	def readonlyQuoteTableColumn(table,column):
		table.GetColumnByName(column).AccessLevel = table.AccessLevel.ReadOnly

	def hideQuoteTableColumn(table,column):
		table.GetColumnByName(column).AccessLevel = table.AccessLevel.Hidden
	Tables_To_Hide = []

	#Tables_To_Hide = ["Migration_Document_Data","Service_Materials_Table_Excel_Pull","Quote_Details","Product_Line_Details","Product_Line_Sub_Group_Details","Product_Type_Details"]

	Tables_To_Hide = ["Migration_Document_Data","Service_Materials_Table_Excel_Pull","Product_Line_Details","Quote_Details","Product_Line_Sub_Group_Details","Product_Type_Details","FME_Invalid_Parts"]
	Trace.Write('-----------insidegs-------------')
	Contract = ['Contract New','Contract Renewal']
	if quote.GetCustomField('Quote Type').Content in Contract:
		Log.Write('-----------insidegs-------------')
		Trace.Write('-----------insidegs-------------')
		if quote.GetCustomField('SC_CF_PRICE_TOGGLE').Content == '':
			quote.GetCustomField('SC_CF_PRICE_TOGGLE').Content= 'Quote Currency'
		for i in Tables_To_Hide:
			tabletohidden = quote.QuoteTables[i]
			setAccessHidden(tabletohidden)
		#Upate Market discount columns based on selected agreement type
		qt = quote.QuoteTables['Quote_Details']
		agreementType=quote.GetCustomField('SC_CF_AGREEMENT_TYPE').Content.strip()
		if agreementType in ["", "None"]:
			agreementType = "MPA"
		qt.GetColumnByName('MPA_Discount_Percent').Label = agreementType + "/ Market Discount, %"
		qt.GetColumnByName('MPA_Discount_Amount').Label = agreementType + "/ Market Discount Amount"
		#set columns visibliity
		row = qt.Rows[0]
		for cell in row.Cells:
			if cell.ColumnName in ['PROS_Guidance_Recommended_Price','Target_Sell_Price', 'Recommended_Target_Price', 'Max_Quote_Discount_Amount', 'Total_Sell_Price_incl_appl_Fees_', 'GAS_ETO_Price']:
				hideQuoteTableColumn(qt, cell.ColumnName)
			elif cell.ColumnName == 'Negotiation_Limit' and quote.OrderStatus.Name == 'Preparing':
				editableQuoteTableColumn(qt, cell.ColumnName)
			else:
				readonlyQuoteTableColumn(qt, cell.ColumnName)