Ent = Product.GetContainerByName('SC_BGP_Optional_Ent_Cont')
Ent.Clear()
Service = Product.Attr('SC_BGP_Serv_Product').GetValue()
S = []
S = Service.split(", ")
for SP in S:
    a = SqlHelper.GetList("select distinct Top 1000 Entitlement,IsMandatory,ProductCode,EntitlementCode from CT_SC_ENTITLEMENTS_DATA where ServiceProduct = '{}' and IsMandatory = 'FALSE'".format(SP))
    for row in a:
        if row.IsMandatory == 'FALSE':
            i = Ent.AddNewRow()
            i['Service_Product'] = str(SP)
            i['Optional_Entitlement'] = row.Entitlement
            i['ProductCode'] = row.ProductCode
            i['EntitlementCode'] = row.EntitlementCode
Ent.Calculate()
#Change product status as incomplete
Product.Attr('SC_Product_Status').AssignValue("0")