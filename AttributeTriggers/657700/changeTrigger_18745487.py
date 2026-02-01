Ent = Product.GetContainerByName('SC_Cyber_Optional_Ent_Cont')
Service = Product.Attr('SC_Cyber_Service_Product').GetValue()
S = []
S = Service.split(", ")
#Selected_Ent = Product.Attr('Selected_Entitlement').GetValue()
Selected_list = ""

if Ent.Rows.Count:
    for ent_row in Ent.Rows:
        if ent_row.IsSelected == True:
            Selected_list += str(ent_row['Service_Product'])+"|"+str(ent_row['Optional_Entitlement'])+"|"
Trace.Write("SP: "+str(S))
Trace.Write("Selected_list-->"+str(Selected_list))
Ent.Clear()
for SP in S:
    a = SqlHelper.GetList("select distinct Top 1000 Entitlement,IsMandatory from CT_SC_ENTITLEMENTS_DATA where ServiceProduct = '{}' and IsMandatory = 'FALSE'".format(SP))
    for row in a:
        if row.Entitlement in Selected_list and SP in Selected_list:
            Trace.Write("Entitle-->"+str(row.Entitlement)+"..SP-->"+str(SP))
            i = Ent.AddNewRow()
            i['Service_Product'] = str(SP)
            i['Optional_Entitlement'] = row.Entitlement
            i.IsSelected = True
        else:
            Trace.Write("Else!!!")
            Trace.Write("Entitle-->"+str(row.Entitlement)+"..SP-->"+str(SP))
            i = Ent.AddNewRow()
            i['Service_Product'] = str(SP)
            i['Optional_Entitlement'] = row.Entitlement

Ent.Calculate()
ScriptExecutor.Execute('PS_ServiceProduct_Entitlement_error')