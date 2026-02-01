Cybervalid = Product.GetContainerByName("SC_Cyber_Models_Scope_Cont")
m = []
for row in Cybervalid.Rows:
    if row.IsSelected:
        m.append(row.RowIndex)
m.reverse()
for i in m:
    Cybervalid.DeleteRow(i)
Cybervalid.Calculate()
ScriptExecutor.Execute('PS_Cyber_Error_Message')   
#Change product status as incomplete
Product.Attr('SC_Product_Status').AssignValue("0")