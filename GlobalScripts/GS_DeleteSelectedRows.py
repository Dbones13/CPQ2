Write = Product.GetContainerByName("WriteInProduct")
m = []
for row in Write.Rows:
    if row.IsSelected:
        m.append(row.RowIndex)
m.reverse()
for i in m:
    Write.DeleteRow(i)
    Write.Calculate()