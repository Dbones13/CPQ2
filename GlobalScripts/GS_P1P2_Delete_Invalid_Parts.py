p1p2invalid = Product.GetContainerByName("SC_P1P2_Invalid_Parts")
m = []
for row in p1p2invalid.Rows:
    if row.IsSelected:
        m.append(row.RowIndex)
m.reverse()
for i in m:
    p1p2invalid.DeleteRow(i)
p1p2invalid.Calculate()