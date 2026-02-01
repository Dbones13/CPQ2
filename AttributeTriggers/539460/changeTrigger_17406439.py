def populateHeaders(product):
    containerDict = getContainerDict(product)
    minMaxDict = getMinMaxDict()
    for container , columns in minMaxDict.items():
        if container in containerDict:
            row = containerDict[container]
            for colData in columns:
                col = row.GetColumnByName(colData[0])
                if col and not col.HeaderLabel.endswith("({} - {})".format(int(colData[1]) if str(type(colData[1])) != "<type 'DBNull'>" else 0, int(colData[2]) if str(type(colData[2])) != "<type 'DBNull'>" else 0))  and col.Name != 'Graphics_Migration_For_existing_US_GUS_DSP_what_percentage_of_Standard_Builds_will_be_used?':
                    col.HeaderLabel = "{} ({} - {})".format(col.HeaderLabel , int(colData[1]) if str(type(colData[1])) != "<type 'DBNull'>" else 0, int(colData[2]) if str(type(colData[2])) != "<type 'DBNull'>" else 0)

NoOfMig = Product.Attr('xPM_NIMsconf').GetValue()
newValue = 0 if NoOfMig == '' else int(NoOfMig)
container = Product.GetContainerByName('ENB_Migration_Config_Cont')
oldValue = container.Rows.Count
Trace.Write("oldValue = " +str(oldValue) + " newValue = " +str(newValue))
if newValue <=10:
    if newValue == 0:
        Product.GetContainerByName('ENB_Migration_Config_Cont').Rows.Clear()
        Product.Attr('xPM_NIMsconf').AssignValue(str(0))
    elif newValue > oldValue:
        difference = (newValue - oldValue)
        for i in range(difference):
            row = container.AddNewRow()
    elif newValue < oldValue:
        difference = oldValue - newValue
        for i in range(oldValue, newValue, -1):
            Product.GetContainerByName('ENB_Migration_Config_Cont').DeleteRow(i-1)
else:
    Product.Attr('xPM_NIMsconf').AssignValue(str(0))
    Product.GetContainerByName('ENB_Migration_Config_Cont').Rows.Clear()
    Trace.Write("1....oldValue = " +str(oldValue) + " newValue = " +str(newValue))