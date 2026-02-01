def row_count_frequency(Inv_Freq):
    if Inv_Freq == 'Adhoc':
        row_count = 1
       	return row_count
    if Inv_Freq == 'Yearly':
        row_count = 1
        return row_count
    elif Inv_Freq == 'Bi-Monthly':
        row_count = 12/2
        return row_count
    elif Inv_Freq == 'Every 4 weeks':
        row_count = 52/4
        return row_count
    elif Inv_Freq == 'Every 4 months':
        row_count = 12/4
        return row_count
    elif Inv_Freq == 'Monthly':
        row_count = 12
        return row_count
    elif Inv_Freq == 'Quarterly':
        row_count = 12/3
        return row_count
    elif Inv_Freq == 'Semi-Annual':
        row_count = 12/6
        return row_count

Inv_Freq = Quote.GetCustomField('SC_CF_INV_FREQUENCY').Content
row_count = row_count_frequency(Inv_Freq)

sell_price_lst = []
for item in Quote.MainItems:
    if 'Year' in item.PartNumber:
        sell_price_lst.append(item.ExtendedAmount)

#Total_SP = Quote.GetCustomField('Total Sell Price(USD)').Content 
#Total_Sell_Price = float(Total_SP[4:].replace(',',''))
def updateMileStoneTable(tRow,cName,nVal,cRowId):
    table = Quote.QuoteTables["SC_Milestone_Table"]
    if cName == 'Percentage_Amount':
        if Inv_Freq == 'Adhoc':
            remVal = 100 - nVal
            for row in table.Rows:
                if row.Id!=cRowId:
                    pass
                    #row['Percentage_Amount'] = int(remVal/(table.Rows.Count - 1))
                row['Value'] = (row['Percentage_Amount']*sum(sell_price_lst))/100
        else:
            sell_price = tRow['Yearly_Price']
            year = tRow['Years']
            remVal = 100 - nVal
            for row in table.Rows:
                if sell_price == row['Yearly_Price'] and year == row['Years']:
                    if row.Id!=cRowId:
                        row['Percentage_Amount'] = int(remVal/(row_count - 1))
                    row['Value'] = (row['Percentage_Amount']*sell_price)/100
    elif cName == 'Value':
        if Inv_Freq == 'Adhoc':
            remVal = sum(sell_price_lst) - nVal
            for row in table.Rows:
                if row.Id!=cRowId:
                    pass
                    #row['Value'] = int(remVal/(table.Rows.Count - 1))
                row['Percentage_Amount'] = (row['Value']/sum(sell_price_lst))*100
        else:
            sell_price = tRow['Yearly_Price']
            year = tRow['Years']
            remVal = sell_price - nVal
            for row in table.Rows:
                if sell_price == row['Yearly_Price'] and year == row['Years']:
                    if row.Id!=cRowId:
                        row['Value'] = int(remVal/(row_count - 1))
                    row['Percentage_Amount'] = (row['Value']/sell_price)*100
    table.Save()
	#Quote.save()

if len(EventArgs.Cells)>0:
    columnName = EventArgs.Cells[0].ColumnName
    currentRow = EventArgs.Cells[0].Row
    newValue = EventArgs.Cells[0].Value
    currentRowId = currentRow.Id
    updateMileStoneTable(currentRow,columnName,newValue,currentRowId)
