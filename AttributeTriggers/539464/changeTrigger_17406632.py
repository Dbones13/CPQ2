'''def getMigrationDefaultValueDict():
    query = "select * from MIGRATION_DEFAULTS"
    res = SqlHelper.GetList(query)

    resDict = dict()
    for r in res:
        resDict[r.COLUMN_NAME] = [r.DEFAULT_VALUE, r.COLUMN_TYPE]
    return resDict

def setDefaultValue(product, configContainer, row, defaultValDict):
    for col in row.Columns:
        valData = defaultValDict.get(col.Name)
        if valData is None :
            continue
        colType = valData[1]
        if colType == 'DROPDOWN':
            col.SetAttributeValue(valData[0])
        elif colType == 'TEXTBOX':
            row.SetColumnValue(col.Name,valData[0])
        elif colType == 'PRODATTR':
            row.Product.Attr(col.Name).SelectDisplayValue(valData[0])
            row.ApplyProductChanges()
        if col.Name == "xPM_Migration_Scenario":
            defaultMigScenario = checkDefaultMigrationScenario(product)
            if defaultMigScenario :
                row.Product.Attr(col.Name).SelectDisplayValue(defaultMigScenario)
                row.ApplyProductChanges()
        row.Calculate()
        
def updateContainerTable(Product, configContainer, newValue):
    defaultValDict = getMigrationDefaultValueDict()
    listToDeleted = []
    if configContainer is not None:
        containerRows = configContainer.Rows.Count
        if newValue == 0:
            configContainer.Rows.Clear()
        elif containerRows > newValue:
            i = 1
            for row in configContainer.Rows:
                if i > newValue:
                    listToDeleted.append(row.RowIndex)
                i += 1
        elif containerRows < newValue:
            newRows =  newValue - containerRows
            while newRows > 0:
                row = configContainer.AddNewRow()
                setDefaultValue(Product, configContainer, row, defaultValDict)
                newRows -= 1
            configContainer.Calculate()
    listToDeleted.sort(reverse=True)
    if len(listToDeleted) > 0:
        for rowIndex in listToDeleted:
            configContainer.DeleteRow(rowIndex)


config_container = Product.GetContainerByName("C200_Migration_Config_Cont")
general_container = Product.GetContainerByName("C200_Migration_General_Qns_Cont")
if general_container.Rows.Count:
    attr_val = general_container.Rows[0]
    Trace.Write("<<<>>>" + attr_val['C200_How_many_C200s_are_we_migrating'])
    NoofConfig = attr_val['C200_How_many_C200s_are_we_migrating']

newValue = 0 if NoofConfig == '' else int(NoofConfig)
updateContainerTable(Product, config_container, newValue)'''