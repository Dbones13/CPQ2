#########################
#
# GS_PLC_UOC_MinMax
# Enforcing MIn MAx for attrivutes for PLC and UOC
#
# Dan Bragdon 02/09/2022
#
######################

import ProductUtil as pu

def validateEntry(EventArgs , Product):
    container = EventArgs.Container
    changedCell = EventArgs.ChangedCell
    oldValue = changedCell.OldValue
    newValue = changedCell.NewValue
    changedColumn = changedCell.ColumnName
    rowIndex = changedCell.RowIndex

    query = "select * from PLC_UOC_ATTRIBUTE_MINMAX where Cont_ColumnName = '{0}' and (Min > {1} or Max < {1}) and container_name = '{2}'".format(changedColumn ,newValue, container.Name)
    #Trace.Write("Query = " +str(query))
    res = SqlHelper.GetFirst(query)

    if res:
        if newValue and res.Max and float(newValue) > float(res.Max):
            pu.addMessage(Product , 'Max value allowed is {}'.format(res.Max))
        elif newValue and res.Max and float(newValue) < float(res.Min):
            pu.addMessage(Product , 'Min value allowed is {}'.format(res.Min))
        resetColumnValue(container , changedColumn , oldValue , rowIndex)

def resetColumnValue(container , columnName , oldValue , rowIndex):
    for row in container.Rows:
        if row.RowIndex == rowIndex:
            row[columnName] = str(oldValue)