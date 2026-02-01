entitlement = Product.GetContainerByName("SC_MES_Entitlements")
entitlement.Rows.Clear()
optional_entitlement = Product.GetContainerByName("SC_MES_Optional_Entitlement")
serprod = Product.Attr("SC_MES_Service_Product").GetValue()

entitlementQuery = SqlHelper.GetList("select Entitlement from CT_SC_ENTITLEMENTS_DATA where Product_Type = 'MES Performix' and IsMandatory = 'TRUE' and ServiceProduct = '{}'".format(serprod))
if entitlementQuery is not None:
    for ent in entitlementQuery:
        newrow = entitlement.AddNewRow(False)
        newrow["Entitlement"] = ent.Entitlement
        newrow["Type"] = "Mandatory"

for row in optional_entitlement.Rows:
    if row.IsSelected == True:
        newrow = entitlement.AddNewRow(False)
        newrow["Entitlement"] = row["Entitlement"]
        newrow["Type"] = "Optional"