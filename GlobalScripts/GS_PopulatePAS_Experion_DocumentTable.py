def populateEXPERIONData(Quote):
    hierarchy = {'Level0': "New / Expansion Project", 'Level1': "System Group", 'Level2': "Experion MX System"}
    QT_Table = Quote.QuoteTables["PAS_Document_Data"]
    SM = ''
    for Item in Quote.MainItems:
        if hierarchy["Level2"] == Item.ProductName:
            SM ='Yes'
            newRow = QT_Table.AddNewRow()
            newRow["System_Name"] = Item.ProductName                          
    if SM == 'No':
        for row in QT_Table.Rows:
            if row["System_Name"] == 'Experion MX System':
                rowId = row.Id
                QT_Table.DeleteRow(int(rowId))
    for row in QT_Table.Rows:
        for Item in Quote.MainItems:
            if hierarchy["Level1"] == Item.ProductName:
                row["System_Group"] = Item.PartNumber
    QT_Table.Save()
    if SM != 'Yes':
        return False
    else:
        return True