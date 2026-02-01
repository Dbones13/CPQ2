Cyberinvalid = Product.GetContainerByName("SC_GN_AT_Invalid_Cont")
m = []
for row in Cyberinvalid.Rows:
    if row.IsSelected:
        m.append(row.RowIndex)
m.reverse()
for i in m:
    Cyberinvalid.DeleteRow(i)
Cyberinvalid.Calculate()
#Change product status as incomplete
Product.Attr('SC_Product_Status').AssignValue("0")