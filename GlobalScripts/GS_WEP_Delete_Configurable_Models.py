configvalid = Product.GetContainerByName("SC_WEP_Configurable_Models_Training")
m = []
for row in configvalid.Rows:
    if row.IsSelected:
        m.append(row.RowIndex)
m.reverse()
for i in m:
    configvalid.DeleteRow(i)
    configvalid.Calculate()
ScriptExecutor.Execute('PS_Training_Error_Message')
if len(m)>0:
    Product.Attr('SC_Product_Status').AssignValue("0")