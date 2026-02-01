#########################
#
# GS_PMD_MinMax
# Enforcing MIn MAx for attrivutes for PLC and UOC
#
# Satya Dasari 03/04/2022
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

    query = "select * from PMD_System_Attribute_MinMax where Cont_ColumnName = '{0}' and (Min > {1} or Max < {1})".format(changedColumn ,newValue)
    Trace.Write("Query = " +str(query))
    res = SqlHelper.GetFirst(query)

    if res:
        if newValue and res.Max and float(newValue) > float(res.Max):
            pu.addMessage(Product , 'Max value allowed is {}'.format(res.Max))
        elif newValue and res.Max and float(newValue) < float(res.Min):
            pu.addMessage(Product , 'Min value allowed is {}'.format(res.Min))
        resetColumnValue(container , changedColumn , oldValue , rowIndex)

def validateEntry_without_column(EventArgs , Product):
    container = EventArgs.Container
    changedCell = EventArgs.ChangedCell
    oldValue = changedCell.OldValue
    newValue = changedCell.NewValue
    changedColumn = changedCell.ColumnName
    rowIndex = changedCell.RowIndex

    query = "select * from PMD_System_Attribute_MinMax where  (Min > {0} or Max < {0})".format(newValue)
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