Cybervalid = Product.GetContainerByName("SC_GN_AT_Models_Scope_Cont")
m = []
for row in Cybervalid.Rows:
    if row.IsSelected:
        m.append(row.RowIndex)
m.reverse()
for i in m:
    Cybervalid.DeleteRow(i)
Cybervalid.Calculate()
ScriptExecutor.Execute('PS_GN_Error_Message')   
#Change product status as incomplete
Product.Attr('SC_Product_Status').AssignValue("0")