def populateRow(row , item ,itemNumber , itemType , documentType=''):
    row['Item_Number'] = itemNumber
    partNumber = item.PartNumber if item['QI_FME'].Value == '' else item['QI_FME'].Value
    FlagValue = False
    quuery = SqlHelper.GetFirst("Select Family_Code FROM PMC_GASETO_YSPEC_MARINE_PRODUCTS WHERE PartNumber = '{}'".format(item.PartNumber))
    if quuery is not None:
        if quuery.Family_Code is not None:
            if quuery.Family_Code == 'Gas Products':
                FlagValue = True
    if FlagValue == True and item.QI_Short_FME_Code.Value != "":
        row['Part_Number'] = item.QI_Short_FME_Code.Value
    else:
        row['Part_Number'] = partNumber
    if item.ProductName == "WriteIn":
        row['Item_Description'] = item.QI_ExtendedDescription.Value
    else:
        row['Item_Description'] = item.Description
    row['Quantity'] = item.Quantity
    row['Item_Type'] = itemType
    if FlagValue == True:
        row['Unit_Price'] = round(item.QI_NetPrice_With_ETO.Value/item.Quantity,2)
        row['Total_Price'] = item.QI_NetPrice_With_ETO.Value
    else:
        row['Unit_Price'] = item.NetPrice
        row['Total_Price'] = item.ExtendedAmount
    row['Unit_List_Price'] = item.ListPrice
    row['List_Price'] = item.ExtendedListPrice
    row['Document_Type'] = documentType
    row['Surcharge_Price'] = item['QI_Tariff_Amount'].Value if item['QI_Tariff_Amount'] else 0.00 
    row['Total_Sell_Price'] = item.QI_NetPrice_With_ETO.Value if item.QI_NetPrice_With_ETO.Value else item['QI_Sell_Price_Inc_Tariff'].Value
    #row['Total_Sell_Price'] = item['QI_Sell_Price_Inc_Tariff'].Value if item['QI_Sell_Price_Inc_Tariff'] else 0.00
def populateNewRow(table , row , rolledUpNumber):
    newRow = table.AddNewRow()
    for cell in row.Cells:
        newRow[cell.ColumnName] = cell.Value
    newRow['ItemNumber'] = rolledUpNumber