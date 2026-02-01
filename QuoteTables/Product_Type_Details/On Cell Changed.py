import GS_QuoteTotalTablesUtil as util

i = 0
while i < len(EventArgs.Cells):
    cell = EventArgs.Cells[i]
    Trace.Write('Column: {0}, value: {1}, display value: {2}, old value: {3}'.format(cell.ColumnName,cell.Value, cell.DisplayValue, EventArgs.OldValues[i]))

    row = cell.Row
    
    if cell.ColumnName == "Labour_MPA_Discount":
        product_line = row['Product_Type']
        product_line_item_data = SqlHelper.GetList("select * from CartItemCustomFields where cart_id = '{}' and QI_ProductCostCategory = '{}' and QI_ProductCostCategory = 'Honeywell Labor'".format(Quote.QuoteId, product_line))
        if not product_line_item_data:
            row[cell.ColumnName] = EventArgs.OldValues[i]
            row["Modified_PT"]=row['Product_Type']

    if cell.ColumnName == "Sell_Price_Discount_Percent":
        percent = cell.Value
        #CXCPQ-42168:06/13/2023:start
        #discount = (row['Target_Sell_Price'] * percent)/100
        discount = ((row['Target_Sell_Price']-row['GAS_ETO_Price']) * percent)/100
        #CXCPQ-42168:06/13/2023:End
    elif cell.ColumnName == "Sell_Price_Discount_Amount":
        discount = cell.Value
    elif cell.ColumnName == "Sell_Price":
        sellPrice = cell.Value
        #CXCPQ-42168:06/13/2023:start
        #discount = row['List_Price'] - sellPrice - row['MPA_Discount_Amount']
        discount = row['List_Price'] - (sellPrice-row['GAS_ETO_Price']) - row['MPA_Discount_Amount']
        #CXCPQ-42168:06/13/2023:End

    if row["Max_Discount_Amount"] and discount <= row["Max_Discount_Amount"]:
        percent = (discount * 100) / row["Max_Discount_Amount"]
        row["New_Discount"] = percent
        row["Modified_PT"]=row['Product_Type']
        #util.applyProductTypeDiscountToItems(Quote , row['Product_Type'] , percent)
    else:
        #CXCPQ-42168:06/13/2023:Updated Quote Message
        #Quote.Messages.Add('Maximum discount limit exceeded. Any quote line item cannot have a -ve sell price. Minimum sell price for {} product type can be {}.'.format(row['Product_Type'] , round(row['Target_Sell_Price'] - row["Max_Discount_Amount"]),2))
        Quote.Messages.Add('Maximum discount limit exceeded. Any quote line item cannot have a -ve sell price. Minimum sell price for {} product type can be {}.'.format(row['Product_Type'] , round(row['Target_Sell_Price'] -row['GAS_ETO_Price']- row["Max_Discount_Amount"]),2))
        row[cell.ColumnName] = EventArgs.OldValues[i]
    i += 1