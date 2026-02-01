SESP_Models_Cont = Product.GetContainerByName('SC_Entitlements')
Labor_Cont = Product.GetContainerByName('SC_Labor_Summary_Container_SESP')
Service = Product.Attr('SC_Service_Product').GetValue()

for row1 in  SESP_Models_Cont.Rows:
    if row1.IsSelected == True:
        i = Labor_Cont.AddNewRow(False)
        i['Service_Product'] = Service
        i['Entitlement'] = row1['Entitlement']