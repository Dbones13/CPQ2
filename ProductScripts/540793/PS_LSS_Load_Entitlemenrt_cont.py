tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]
Service = Product.Attr('SC_HWOS_Service_Product').GetValue()
Entitlement = SqlHelper.GetList("select Entitlement,IsMandatory from CT_SC_ENTITLEMENTS_DATA where IsMandatory = 'TRUE' and ServiceProduct = '{}'".format(Service))
#if Product.Attr('SC_Product_Type').GetValue() is not None and Product.Attr('SC_Product_Type').GetValue() == 'Renewal' and 'Scope Summary' in tabs:
if Product.Attr('SC_Product_Type').GetValue() is not None and 'Scope Summary' in tabs:
    if Product.Name == 'Local Support Standby' and Entitlement :
        SC_LSS_Summary_Entitlement_Cont = Product.GetContainerByName('SC_LSS_Summary_Entitlement_Cont')
        SC_LSS_Summary_Entitlement_Cont.Rows.Clear()
        for row in Entitlement:
            i = SC_LSS_Summary_Entitlement_Cont.AddNewRow()
            i['Service_Product'] = Service
            i['Entitlement'] = row.Entitlement
            i['Type'] = 'Mandatory'