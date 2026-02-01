def getInt(Var):
    if Var:
        return int(Var)
    return 0
def getContainer(Name):
    return Product.GetContainerByName(Name)

containerConfig = getContainer('FSC_to_SM_IO_Series_1_&_2_FSC_IO_configurations')
totalSys = Product.Attr('ATT_FSCtoSMIOMigrationTotalFSC').GetValue()
oldValue = containerConfig.Rows.Count
newValue = 0 if totalSys == '' else int(totalSys)
containerGeneral = getContainer("FSC_to_SM_IO_Migration_General_Information2")
if newValue <=10:
    if newValue == 0:
        containerConfig.Rows.Clear()
        Product.GetContainerByName('FSC_SM_IO_SIC_Cable').Rows.Clear()
        Product.Attr('ATT_FSCtoSMIOMigrationTotalFSC').AssignValue('0')
    elif newValue > oldValue:
        difference = (newValue - oldValue)
        Trace.Write("newValue > oldValue")
        for i in range(difference):
            row = containerConfig.AddNewRow(False)
    elif newValue < oldValue:
        difference = oldValue - newValue
        Trace.Write("newValue < oldValue")
        for i in range(oldValue, newValue, -1):
            containerConfig.DeleteRow(i-1)
    if newValue != 0:
        sic_cont = Product.GetContainerByName('FSC_SM_IO_SIC_Cable')
        if sic_cont.Rows.Count == 0:
            values=['3 mts','5 mts','6 mts','8 mts','10 mts','15 mts','20 mts','25 mts','30 mts']
            for value in values:
                new_row = sic_cont.AddNewRow(False)
                new_row.GetColumnByName('Length').SetAttributeValue(value)
                new_row["Length"] = value

else:
    Product.Attr('ATT_FSCtoSMIOMigrationTotalFSC').AssignValue(str(oldValue))