import GS_MigrationUtil as mu

#mu.populateContainer(EventArgs , Product)
#mu.validateEntry(EventArgs , Product)

#container = EventArgs.Container
#changedCell = EventArgs.ChangedCell
#changedColumn = changedCell.ColumnName
#rowIndex = changedCell.RowIndex
#newValue = changedCell.NewValue
#oldValue = changedCell.OldValue

newValue = int(Product.Attr('ATT_LM_QTY_OF_LMPAIR_TOBE_MIGRATED').GetValue())

#if changedColumn == "ATT_LM_QTY_OF_LMPAIR_TOBE_MIGRATED":
if int(newValue) > 0:
    conYN = Product.GetContainerByName("LM_to_ELMM_ControlEdge_PLC_Cont")
    row_count = conYN.Rows.Count
    if row_count < newValue:
        for _ in range(row_count, newValue):
            conYN.AddNewRow(False)
    elif row_count > newValue:
        delete = row_count
        for _ in range(newValue, row_count):
            delete -= 1
            conYN.DeleteRow(delete)
            #conYN.DeleteRow(row_count - 1)
if int(newValue) > 0:
    Localio = Product.GetContainerByName("LM_to_ELMM_ControlEdge_PLC_Local_IO_Cont")
    Localio_count = Localio.Rows.Count
    if Localio_count < newValue:
        for _ in range(Localio_count, newValue):
            Localio.AddNewRow(False)
    elif Localio_count > newValue:
        delete = Localio_count
        for _ in range(newValue, Localio_count):
            delete -= 1
            Localio.DeleteRow(delete)
            #Localio.DeleteRow(Localio_count - 1)
if int(newValue) > 0:
    Remoteio = Product.GetContainerByName("LM_to_ELMM_ControlEdge_PLC_Remote_IO_Cont")
    Remoteio_count = Remoteio.Rows.Count
    if Remoteio_count < newValue:
        for _ in range(Remoteio_count, newValue):
            Remoteio.AddNewRow(False)
    elif Remoteio_count > newValue:
        delete = Remoteio_count
        for _ in range(newValue, Remoteio_count):
            delete -= 1
            Remoteio.DeleteRow(delete)
            #Remoteio.DeleteRow(Remoteio_count - 1)
if int(newValue) > 0:
    MigrationAddition = Product.GetContainerByName("LM_to_ELMM_Migration_Additional_IO_Cont")
    MigrationAddition_count = MigrationAddition.Rows.Count
    if MigrationAddition_count < newValue:
        for _ in range(MigrationAddition_count, newValue):
            MigrationAddition.AddNewRow(False)
    elif MigrationAddition_count > newValue:
        delete = MigrationAddition_count
        for _ in range(newValue, MigrationAddition_count):
            delete -= 1
            MigrationAddition.DeleteRow(delete)
            #MigrationAddition.DeleteRow(MigrationAddition_count - 1)
else:
    conYN = Product.GetContainerByName("LM_to_ELMM_ControlEdge_PLC_Cont").Rows.Clear()
    Localio = Product.GetContainerByName("LM_to_ELMM_ControlEdge_PLC_Local_IO_Cont").Rows.Clear()
    Remoteio = Product.GetContainerByName("LM_to_ELMM_ControlEdge_PLC_Remote_IO_Cont").Rows.Clear()
    MigrationAddition = Product.GetContainerByName("LM_to_ELMM_Migration_Additional_IO_Cont").Rows.Clear()
isR2Qquote = True if Quote.GetCustomField("isR2QRequest").Content else False
def setAttrValue(Container,Column):
	for row in Product.GetContainerByName(Container).Rows:
            row.GetColumnByName(Column).SetAttributeValue('5m')
if isR2Qquote:
    setAttrValue('LM_to_ELMM_ControlEdge_PLC_Cont','LM_average_Cable_length_for_IO_network_connection')
	
'''localFlag = 0
    remoteFlag = 0
    for row in conYN.Rows:
        if row["LM_are_the_IO_Racks_remotely_located"] == "Yes - Only Remote":
            remoteFlag += 1
        elif row["LM_are_the_IO_Racks_remotely_located"] in ("No",""): 
            localFlag += 1
if int(remoteFlag) == int(newValue):
    Product.Attr("LM_to_ELMM_Local_Remote_Flag").SelectValue("Hide Local")
elif int(localFlag) == int(newValue):
    Product.Attr("LM_to_ELMM_Local_Remote_Flag").SelectValue("Hide Remote")
else:
Product.Attr("LM_to_ELMM_Local_Remote_Flag").SelectValue("No Hide")'''