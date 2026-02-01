#Refresh Renewal Asset Summary container
tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]
productType = Product.Attr('SC_Product_Type').GetValue()
if productType == "Renewal" and 'Scope Summary' in tabs:
    cont = Product.GetContainerByName('ES_Asset_Summary')
    if cont.Rows.Count > 0:
        cont.Rows[0].Calculate()
    CY_AssetDetails_Cont = Product.GetContainerByName("Asset_details_ServiceProd")
    if CY_AssetDetails_Cont.Rows.Count > 0:
        CY_AssetDetails_Cont.Rows[0].Columns['List Price'].HeaderLabel = 'CY List Price'