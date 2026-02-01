tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]
if 'Scope Summary' in tabs:
    hif_Cont = Product.GetContainerByName("SC_WEP_Entitlement_HIF")
    ifs_Cont = Product.GetContainerByName("SC_WEP_Entitlement_IFS")
    halo_Cont = Product.GetContainerByName("SC_WEP_Entitlement_Halo")
    training_Cont = Product.GetContainerByName("SC_WEP_Entitlement_Training")
    tna_Cont = Product.GetContainerByName("SC_WEP_Entitlement_TNA")
    om_Cont = Product.GetContainerByName("SC_WEP_Entitlement_OM")
    ocp_Cont = Product.GetContainerByName("SC_WEP_Entitlement_OCP")

    entitlement_Cont = Product.GetContainerByName("SC_WEP_Offering_Entitlement")
    entitlement_Cont.Rows.Clear()

    if hif_Cont.Rows.Count:
        for row in hif_Cont.Rows:
            if row.IsSelected == True:
                et_row = entitlement_Cont.AddNewRow(False)
                et_row["Offering_Name"] = "Honeywell Integrated Field App"
                et_row["Entitlements"] = row["Entitlement"]
                et_row["Service_Product"] = Product.Attr('SC_WEP_ServiceProduct_HIF').GetValue()
                et_row['ServiceProductEntitlementPair'] = et_row["Service_Product"]  + '|' + row['Entitlement']
    if ifs_Cont.Rows.Count:
        for row in ifs_Cont.Rows:
            if row.IsSelected == True:
                et_row = entitlement_Cont.AddNewRow(False)
                et_row["Offering_Name"] = "Immersive Field Simulator"
                et_row["Entitlements"] = row["Entitlement"]
                et_row["Service_Product"] = Product.Attr('SC_WEP_ServiceProduct_IFS').GetValue()
                et_row['ServiceProductEntitlementPair'] = et_row["Service_Product"]  + '|' + row['Entitlement']
    if halo_Cont.Rows.Count:
        for row in halo_Cont.Rows:
            if row.IsSelected == True:
                et_row = entitlement_Cont.AddNewRow(False)
                et_row["Offering_Name"] = "HALO OA"
                et_row["Entitlements"] = row["Entitlement"]
                et_row["Service_Product"] = Product.Attr('SC_WEP_ServiceProduct_Halo').GetValue()
                et_row['ServiceProductEntitlementPair'] = et_row["Service_Product"]  + '|' + row['Entitlement']
    if training_Cont.Rows.Count:
        for row in training_Cont.Rows:
            if row.IsSelected == True:
                et_row = entitlement_Cont.AddNewRow(False)
                et_row["Offering_Name"] = "Training"
                et_row["Entitlements"] = row["Entitlement"]
                et_row["Service_Product"] = Product.Attr('SC_WEP_ServiceProduct_Training').GetValue()
                et_row['ServiceProductEntitlementPair'] = et_row["Service_Product"]  + '|' + row['Entitlement']
    if tna_Cont.Rows.Count:
        for row in tna_Cont.Rows:
            if row.IsSelected == True:
                et_row = entitlement_Cont.AddNewRow(False)
                et_row["Offering_Name"] = "Training Needs Assessment"
                et_row["Entitlements"] = row["Entitlement"]
                et_row["Service_Product"] = Product.Attr('SC_WEP_ServiceProduct_TNA').GetValue()
                et_row['ServiceProductEntitlementPair'] = et_row["Service_Product"]  + '|' + row['Entitlement']
    if om_Cont.Rows.Count:
        for row in om_Cont.Rows:
            if row.IsSelected == True:
                et_row = entitlement_Cont.AddNewRow(False)
                et_row["Offering_Name"] = "Operations and Maintenance"
                et_row["Entitlements"] = row["Entitlement"]
                et_row["Service_Product"] = Product.Attr('SC_WEP_ServiceProduct_OM').GetValue()
                et_row['ServiceProductEntitlementPair'] = et_row["Service_Product"]  + '|' + row['Entitlement']
    if ocp_Cont.Rows.Count:
        for row in ocp_Cont.Rows:
            if row.IsSelected == True:
                et_row = entitlement_Cont.AddNewRow(False)
                et_row["Offering_Name"] = "Outcome Competency Program"
                et_row["Entitlements"] = row["Entitlement"]
                et_row["Service_Product"] = Product.Attr('SC_WEP_ServiceProduct_OCP').GetValue()
                et_row['ServiceProductEntitlementPair'] = et_row["Service_Product"]  + '|' + row['Entitlement']