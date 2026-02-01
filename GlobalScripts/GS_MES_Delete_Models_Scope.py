mesvalid = Product.GetContainerByName("SC_MES_Models_Scope")
m = []
for row in mesvalid.Rows:
    if row.IsSelected:
        m.append(row.RowIndex)
m.reverse()
for i in m:
    mesvalid.DeleteRow(i)
    mesvalid.Calculate()
ScriptExecutor.Execute('PS_MES_ErrorMessage')
if len(m)>0:
    Product.Attr('SC_Product_Status').AssignValue("0")