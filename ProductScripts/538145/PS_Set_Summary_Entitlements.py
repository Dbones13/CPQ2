if Product.Name != "Service Contract Products":
    Summary_Entitlement = Product.GetContainerByName("SC_Trace_ServiceProduct_Entitlement")
    if Summary_Entitlement.Rows.Count:
        Summary_Entitlement.Rows.Clear()
    Optional_Entitlements = Product.GetContainerByName("SC_Select_Optional_Entitlements")

    licenseType = Product.Attr("SC_License_type").GetValue()
    entitlement_query = SqlHelper.GetList("select Entitlement,ServiceProduct,IsMandatory from CT_SC_ENTITLEMENTS_DATA where Product_Type='Trace'")

    if licenseType == "Term":
        if entitlement_query is not None:
            for row in entitlement_query:
                if row.ServiceProduct == "Trace Subscription Service" and row.IsMandatory == "TRUE":
                    new_row = Summary_Entitlement.AddNewRow(False)
                    new_row["Service_Product"] = row.ServiceProduct
                    new_row["Entitlement"] = row.Entitlement
                    new_row["Type"] = "Mandatory"
                    new_row["ServiceProductEntitlementPair"] = new_row["Service_Product"] + '|' + new_row["Entitlement"]
    if licenseType == "Perpetual":
        if entitlement_query is not None:
            for row in entitlement_query:
                if row.ServiceProduct == "Trace Software Support" and row.IsMandatory == "TRUE":
                    new_row = Summary_Entitlement.AddNewRow(False)
                    new_row["Service_Product"] = row.ServiceProduct
                    new_row["Entitlement"] = row.Entitlement
                    new_row["Type"] = "Mandatory"
                    new_row["ServiceProductEntitlementPair"] = new_row["Service_Product"] + '|' + new_row["Entitlement"]

    if Optional_Entitlements.Rows.Count:
        for row in Optional_Entitlements.Rows:
            if row.IsSelected == True:
                new_row = Summary_Entitlement.AddNewRow(False)
                new_row["Service_Product"] = row["Service_Product_Line_Item"]
                new_row["Entitlement"] = row["Entitlement"]
                new_row["Type"] = "Optional"
                new_row["ServiceProductEntitlementPair"] = new_row["Service_Product"] + '|' + new_row["Entitlement"]
    Summary_Entitlement.Calculate()