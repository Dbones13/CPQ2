mesinvalid = Product.GetContainerByName("SC_MES_Invalid_Models")
m = []
for row in mesinvalid.Rows:
    if row.IsSelected:
        m.append(row.RowIndex)
m.reverse()
for i in m:
    mesinvalid.DeleteRow(i)
    mesinvalid.Calculate()