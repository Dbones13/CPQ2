p1p2valid = Product.GetContainerByName("SC_P1P2_Parts_Details")
m = []
for row in p1p2valid.Rows:
    if row.IsSelected:
        m.append(row.RowIndex)
m.reverse()
for i in m:
    p1p2valid.DeleteRow(i)
p1p2valid.Calculate()
ScriptExecutor.Execute('P1P2_Part_Details_ErrorMessage')
if len(m)>0:
    Product.Attr('SC_Product_Status').AssignValue("0")
Product.ApplyRules()