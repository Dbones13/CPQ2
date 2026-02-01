a= Product.Attr('SC_Product_Type').GetValue()

if a=="Renewal":
    sespinvalid = Product.GetContainerByName("SC_Invalid_Models_Renewal")

if a=="New":
    sespinvalid = Product.GetContainerByName("SC_Invalid_Models")



m = []
for row in sespinvalid.Rows:
    if row.IsSelected:
        m.append(row.RowIndex)
m.reverse()
for i in m:
    sespinvalid.DeleteRow(i)
    sespinvalid.Calculate()
Product.Attr('SC_Product_Status').AssignValue("0")