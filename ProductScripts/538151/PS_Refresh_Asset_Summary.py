#Refresh Renewal Asset Summary container
tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]
productType = Product.Attr('SC_Product_Type').GetValue()
if productType == "Renewal" and 'Enabled Services' in tabs:
    cont = Product.GetContainerByName('ES_Asset_Summary')
    if cont.Rows.Count:
        cont.Rows[0].Calculate()
    CY_AssetDetails_Cont = Product.GetContainerByName("Asset_details_ServiceProd")
    if CY_AssetDetails_Cont.Rows.Count:
        CY_AssetDetails_Cont.Rows[0].Columns['List Price'].HeaderLabel = 'CY List Price'
elif productType == "Renewal" and 'Scope Summary' in tabs:
    cont2 = Product.GetContainerByName('Asset_details_ServiceProd_ReadOnly')
    if cont2.Rows.Count:
        cont2.Rows[0].Columns['List Price'].HeaderLabel = 'List Price '