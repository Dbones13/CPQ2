tpsInvalid = Product.GetContainerByName("SC_TPS_Invalid_Models")
m = []
for row in tpsInvalid.Rows:
    if row.IsSelected:
        m.append(row.RowIndex)
m.reverse()
for i in m:
    tpsInvalid.DeleteRow(i)
    tpsInvalid.Calculate()