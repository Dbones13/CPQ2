MSIDSystemNumber = dict()
msidContainer = Product.GetContainerByName("Migration_MSID_Selection_Container")
for row in msidContainer.Rows:
    MSIDSystemNumber[str(row['System_Number'])]= row['MSID']
Quote.GetCustomField('MSID/System Number').Content =str(MSIDSystemNumber)