def addRow(EventArgs,Product):
    newrow = EventArgs.NewRow
    index = newrow.RowIndex + 1
    newrow.Product.Attr('Generic_System_Migration_System_Name').AssignValue("Generic System " + str(index))
    newrow.ApplyProductChanges()
    newrow.Calculate()

def copyRow(EventArgs,Product):
    cont_name=EventArgs.Container.Name
    cont = Product.GetContainerByName(cont_name)
    for row in cont.Rows:
        index = row.RowIndex+1
        row['Product Name'] = 'Generic System '+str(index)
        row.Product.Attr('Generic_System_Migration_System_Name').AssignValue(row['Product Name'])
        row.ApplyProductChanges()
        row.Calculate()
def deleteRow(EventArgs,Product):
    cont_name=EventArgs.Container.Name
    cont = Product.GetContainerByName(cont_name)
    for row in cont.Rows:
        index = row.RowIndex+1
        row['Product Name'] = 'Generic System '+str(index)
        row.Product.Attr('Generic_System_Migration_System_Name').AssignValue(row['Product Name'])
        row.ApplyProductChanges()
        row.Calculate()