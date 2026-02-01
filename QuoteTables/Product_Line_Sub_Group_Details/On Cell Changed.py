import GS_QuoteTotalTablesUtil as util

i = 0
while i < len(EventArgs.Cells):
    cell = EventArgs.Cells[i]
    Trace.Write('Column: {0}, value: {1}, display value: {2}, old value: {3}'.format(cell.ColumnName,cell.Value, cell.DisplayValue, EventArgs.OldValues[i]))

    row = cell.Row
    
    if cell.ColumnName == "Labour_MPA_Discount":
        product_line = row['Product_Line_Sub_Group']
        product_line_item_data = SqlHelper.GetList("select * from CartItemCustomFields where cart_id = '{}' and QI_PLSG = '{}' and QI_ProductCostCategory = 'Honeywell Labor'".format(Quote.QuoteId, product_line))
        if not product_line_item_data:
            row[cell.ColumnName] = EventArgs.OldValues[i]
        row["Modified_PLSG"] = row['Product_Line_Sub_Group']

    allowedDiscount = 100

    if row["PLSG_Max_Discount_Amount"]:
        #CXCPQ-42168:06/13/2023:start
        #allowedDiscount = (row["PLSG_Max_Discount_Amount"] * 100 ) / row['PLSG_Target_Sell_Price']
        allowedDiscount = (row["PLSG_Max_Discount_Amount"] * 100 ) / (row['PLSG_Target_Sell_Price']-row['PLSG_GAS_ETO_Price'])
        #CXCPQ-42168:06/13/2023:End

    if cell.ColumnName == "Sell_Price_Discount_Percent":
        percent = cell.Value
    elif cell.ColumnName == "Sell_Price_Discount_Amount" and row['PLSG_Target_Sell_Price']:
        #CXCPQ-42168:06/13/2023:start
        #percent = (cell.Value * 100) / row['PLSG_Target_Sell_Price']
        percent = (cell.Value * 100) / (row['PLSG_Target_Sell_Price']-row['PLSG_GAS_ETO_Price'])
        #CXCPQ-42168:06/13/2023:End
    elif cell.ColumnName == "PLSG_Sell_Price" and row['PLSG_Target_Sell_Price']:
        #CXCPQ-42168:06/13/2023:start
        #percent = ((row['PLSG_List_Price'] - row["PLSG_Sell_Price"] - row['MPA_Discount_Amount']) * 100) / row['PLSG_Target_Sell_Price']
        percent = ((row['PLSG_List_Price'] - row["PLSG_Sell_Price"] - row['MPA_Discount_Amount']) * 100) / (row['PLSG_Target_Sell_Price']-row['PLSG_GAS_ETO_Price'])
        #CXCPQ-42168:06/13/2023:End
    if percent <= allowedDiscount:
		row["New_Discount"] = percent
		row["Modified_PLSG"] = row['Product_Line_Sub_Group']
        #util.applyDiscountToItems(Quote , 'QI_PLSG' , row['Product_Line_Sub_Group'] , percent)
    else:
        Quote.Messages.Add('Max Discount allowed is {}.'.format(row['PLSG_Max_Discount_Amount']))
        row[cell.ColumnName] = EventArgs.OldValues[i]
    i += 1