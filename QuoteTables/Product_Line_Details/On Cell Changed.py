import GS_QuoteTotalTablesUtil as util

i = 0
while i < len(EventArgs.Cells):
    cell = EventArgs.Cells[i]
    Trace.Write('Column: {0}, value: {1}, display value: {2}, old value: {3}'.format(cell.ColumnName,cell.Value, cell.DisplayValue, EventArgs.OldValues[i]))

    row = cell.Row

    allowedDiscount = 100

    if row["PL_Max_Discount_Amount"]:
        #CXCPQ-42168:06/13/2023:start
        #allowedDiscount = (row["PL_Max_Discount_Amount"] * 100 ) / row['PL_Target_Sell_Price']
        allowedDiscount = (row["PL_Max_Discount_Amount"] * 100 ) / (row['PL_Target_Sell_Price'] - row['PL_GAS_ETO_Price'])
        #CXCPQ-42168:06/13/2023:End


    if cell.ColumnName == "Sell_Price_Discount_Percent":
        percent = cell.Value
    if cell.ColumnName == "Sell_Price_Discount_Amount" and row['PL_Target_Sell_Price']:
        #CXCPQ-42168:06/13/2023:start
        #percent = (cell.Value * 100) / row['PL_Target_Sell_Price']
        percent = (cell.Value * 100) / (row['PL_Target_Sell_Price'] - row['PL_GAS_ETO_Price'])
        #CXCPQ-42168:06/13/2023:End
    if cell.ColumnName == "PL_Sell_Price" and row['PL_Target_Sell_Price']:
        #CXCPQ-42168:06/13/2023:start
        #percent = ((row['PL_List_Price'] - row["PL_Sell_Price"] - row['MPA_Discount_Amount']) * 100) / row['PL_Target_Sell_Price']
        percent = ((row['PL_List_Price'] - row["PL_Sell_Price"] - row['MPA_Discount_Amount']) * 100) / (row['PL_Target_Sell_Price'] -row['PL_GAS_ETO_Price'] )
        #CXCPQ-42168:06/13/2023:End
    if percent <= allowedDiscount:
		row["New_Discount"] = percent
		row["Modified_PL"] = row['Product_Line']
		#util.applyDiscountToItems(Quote , 'QI_ProductLine' , row['Product_Line'] , percent)
    else:
        Quote.Messages.Add('Max Discount allowed is {}.'.format(row["PL_Max_Discount_Amount"]))
        row[cell.ColumnName] = EventArgs.OldValues[i]
    i += 1