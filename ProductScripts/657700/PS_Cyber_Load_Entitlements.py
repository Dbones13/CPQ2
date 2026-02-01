#SC_Product_Type = Product.Attr('SC_Product_Type').GetValue()
#if SC_Product_Type == 'New':
Ent_Model = Product.GetContainerByName('SC_GN_AT_Product_Entitlement_Cont')
Opt_Ent = Product.GetContainerByName('SC_GN_AT_Optional_Ent_Cont')
Service = Product.GetContainerByName('SC_GN_AT_Service_Product_Cont') 
S = []
for SP_row in Service.Rows:
    if SP_row.IsSelected == True:
        S.append(str(SP_row['Service_Product']))

Ent_Model.Clear()
for Service in  S:
    a = SqlHelper.GetList("select Entitlement,IsMandatory from CT_SC_ENTITLEMENTS_DATA where IsMandatory = 'TRUE' and ServiceProduct = '{}'".format(Service))
    for row in a:
        i = Ent_Model.AddNewRow()
        i['Service_Product'] = Service
        i['Entitlement'] = row.Entitlement
        i['Type'] = 'Mandatory'
        i['ServiceProductEntitlementPair'] = i['Service_Product'] + '|' + i['Entitlement']
for row1 in  Opt_Ent.Rows:
    if row1.IsSelected == True:
        i = Ent_Model.AddNewRow()
        i['Service_Product'] = row1['Service_Product']
        i['Entitlement'] = row1['Optional_Entitlement']
        i['Type'] = 'Optional'
        i['ServiceProductEntitlementPair'] = i['Service_Product'] + '|' + i['Entitlement']
Ent_Model.Calculate()
ScriptExecutor.Execute('SC_GN_PS_ServiceProduct_Entitlement_error')