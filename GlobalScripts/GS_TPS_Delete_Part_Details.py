tpsValid = Product.GetContainerByName("SC_TPS_Models_Scope")
m = []
for row in tpsValid.Rows:
    if row.IsSelected:
        m.append(row.RowIndex)
m.reverse()
for i in m:
    tpsValid.DeleteRow(i)
    tpsValid.Calculate()
ScriptExecutor.Execute('PS_Populate_Entitlements_Cont')
ScriptExecutor.Execute('PS_Populate_TPS_Manual')
if tpsValid.Rows.Count > 0:
    #Change Product status as incomplete
    Product.Attr('SC_Product_Status').AssignValue("0")
else:
    #clear data from the scope summary containers
    for cont in ['SC_ScopeSummary_entitlement_cont', 'SC_TPS_Entitlements_Scope_summary']:
        Product.GetContainerByName(cont).Rows.Clear()
    Product.Attr('SC_Product_Status').AssignValue('')