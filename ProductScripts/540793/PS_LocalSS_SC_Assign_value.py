if Product.Name=="Local Support Standby":
    Product.Attr('SC_HWOS_Service_Product').AssignValue("Local Support Standby")
    Product.Attr('SC_HWOS_Service_Product').Access= AttributeAccess.ReadOnly
    Product.Attr('SC_LSS_Entitlements').AssignValue("Local Support Standby")
    Product.Attr('SC_LSS_Entitlements').Access= AttributeAccess.ReadOnly
    Product.Attr('SC_LSS_Service_Product').AssignValue("Local Support Standby")
    Product.Attr('SC_LSS_Service_Product').Access= AttributeAccess.ReadOnly