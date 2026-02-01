BGPvalid = Product.GetContainerByName("SC_BGP_Models_Scope_Cont")

m = []
for row in BGPvalid.Rows:
    if row.IsSelected:
        m.append(row.RowIndex)
m.reverse()
for i in m:
    BGPvalid.DeleteRow(i)
    BGPvalid.Calculate()
ScriptExecutor.Execute('PS_BGP_Error_Message')
#Change product status as incomplete
Product.Attr('SC_Product_Status').AssignValue("0")