tpsValid = Product.GetContainerByName("SC_Local_Support_Standby_validModel")
m = []
for row in tpsValid.Rows:
    if row.IsSelected:
        m.append(row.RowIndex)
m.reverse()
for i in m:
    tpsValid.DeleteRow(i)
    tpsValid.Calculate()