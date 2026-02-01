import GS_QuoteTotalTablesUtil as util

i = 0
while i < len(EventArgs.Cells):
	cell = EventArgs.Cells[i]
	Trace.Write('Column: {0}, value: {1}, display value: {2}, old value: {3}'.format(cell.ColumnName,cell.Value, cell.DisplayValue, EventArgs.OldValues[i]))

	row = cell.Row

	if cell.ColumnName == "Quote_Discount_Percent":
										   
		percent = cell.Value
		#CXCPQ-42168:06/13/2023:start
		#discount = (row['Target_Sell_Price'] * percent)/100
		discount = ((row['Target_Sell_Price']-row['GAS_ETO_Price']) * percent)/100
								 
		#CXCPQ-42168:06/13/2023:End 
	elif cell.ColumnName == "Quote_Discount_Amount":
		discount = cell.Value
	elif cell.ColumnName == "Quote_Sell_Price" and row['Target_Sell_Price']:
		sellPrice = row["Quote_Sell_Price"]
																						
		#CXCPQ-42168:06/13/2023:start
		#discount = row['Quote_List_Price'] - sellPrice - row['MPA_Discount_Amount']
		discount = row['Quote_List_Price'] - (sellPrice - row['GAS_ETO_Price']) - row['MPA_Discount_Amount']
															   
		#CXCPQ-42168:06/13/2023:End
	elif cell.ColumnName == "Quote_Regional_Margin_Amount":
		margin 	  = cell.Value
		cost      = row["Quote_Regional_Cost"]

		sellPrice = margin + cost
		discount = row['Quote_List_Price'] - sellPrice - row['MPA_Discount_Amount']
	elif cell.ColumnName == "Quote_WTW_Margin_Amount":
		margin 	  = cell.Value
		cost      = row["Quote_WTW_Cost"]

		sellPrice = margin + cost
		discount = row['Quote_List_Price'] - sellPrice - row['MPA_Discount_Amount']
	elif cell.ColumnName == "Quote_WTW_Margin_Percent":
		percent   = cell.Value
		cost      = row["Quote_WTW_Cost"]

		sellPrice = (100 * cost) / (100 - percent)
		discount = row['Quote_List_Price'] - sellPrice - row['MPA_Discount_Amount']
	elif cell.ColumnName == "Quote_Regional_Margin_Percent":
		percent   = cell.Value
		cost      = row["Quote_Regional_Cost"]

		sellPrice = (100 * cost) / (100 - percent)
		discount = row['Quote_List_Price'] - sellPrice - row['MPA_Discount_Amount'] 									 
	if row["Max_Quote_Discount_Amount"] and discount <= row["Max_Quote_Discount_Amount"]:
		percent = (discount * 100) / row["Max_Quote_Discount_Amount"]
														  
		row["New_Discount"] = percent					   
		#util.applyQuoteDiscountToItems(Quote , percent)
	else:
		#CXCPQ-42168:06/13/2023:Updated Quote message
		#Quote.Messages.Add('Maximum discount limit exceeded. Any quote line item cannot have a -ve sell price. Minimum sell price for this quote can be {}.'.format(round(row['Target_Sell_Price'] - row["Max_Quote_Discount_Amount"]),2))
		Quote.Messages.Add('Maximum discount limit exceeded. Any quote line item cannot have a -ve sell price. Minimum sell price for this quote can be {}.'.format(round(row['Target_Sell_Price'] - row['GAS_ETO_Price']- row["Max_Quote_Discount_Amount"]),2))
		row[cell.ColumnName] = EventArgs.OldValues[i]
	i += 1