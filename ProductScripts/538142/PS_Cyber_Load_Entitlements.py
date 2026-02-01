#SC_Product_Type = Product.Attr('SC_Product_Type').GetValue()
#if SC_Product_Type == 'New':
Ent_Model = Product.GetContainerByName('SC_Cyber_Product_Entitlement_Cont')
Opt_Ent = Product.GetContainerByName('SC_Cyber_Optional_Ent_Cont')
Service = Product.Attr('SC_Cyber_Service_Product').GetValue()
S = []
S = Service.split(", ")
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