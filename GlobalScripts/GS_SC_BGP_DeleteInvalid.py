bgpinvalid = Product.GetContainerByName("SC_BGP_Invalid_Cont")
m = []
for row in bgpinvalid.Rows:
    if row.IsSelected:
        m.append(row.RowIndex)
m.reverse()
for i in m:
    bgpinvalid.DeleteRow(i)
    bgpinvalid.Calculate()
#Change product status as incomplete
Product.Attr('SC_Product_Status').AssignValue("0")