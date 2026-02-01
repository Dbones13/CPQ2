query = "select * from MSID_SIT_DB where MSID = '{}'".format(Product.Attr('Migration_MSID_Choices').GetValue())
res = SqlHelper.GetList(query)

dataDict = dict()

for r in res:
    keyValueDict = dataDict.get(r.ContName , dict())
    keyValueDict[r.ContColumnValue] = r.SIT_DB
    dataDict[r.ContName] = keyValueDict

for containerName , columnDataDict in dataDict.items():
    container = Product.GetContainerByName(containerName)
    if container.Rows.Count == 1:
        addedRow = container.AddNewRow()
        for columnName , value in columnDataDict.items():
            addedRow.SetColumnValue(columnName , value)