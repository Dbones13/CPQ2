tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]
if 'Scope Summary' in tabs:
    partDetailsCont = Product.GetContainerByName('SC_P1P2_Parts_Details')
    sericeEntitlementCont = Product.GetContainerByName('SC_P1P2_ServiceProduct_Entitlement')
    sericeEntitlementCont.Rows.Clear()
    p1 = 0
    p2 = 0
    p1hot = 0

    if partDetailsCont.Rows.Count:
        for row in partDetailsCont.Rows:
            if row['Service_Product'] == 'Parts Holding P1' and p1 == 0:
                srow = sericeEntitlementCont.AddNewRow(False)
                srow['Service Product'] = 'Parts Holding P1'
                srow['Entitlement'] = 'P1 - On-Site Cold Parts'
                srow['ServiceProductEntitlementPair'] = srow['Service Product'] + '|' + srow['Entitlement']
                p1 += 1
            elif row['Service_Product'] == 'Parts Holding P2' and p2 == 0:
                srow = sericeEntitlementCont.AddNewRow(False)
                srow['Service Product'] = 'Parts Holding P2'
                srow['Entitlement'] = 'P2 - Off-Site Spare Parts'
                srow['ServiceProductEntitlementPair'] = srow['Service Product'] + '|' + srow['Entitlement']
                p2 += 1
            elif row['Service_Product'] == 'Parts Holding P1 Hot' and p1hot == 0:
                srow = sericeEntitlementCont.AddNewRow(False)
                srow['Service Product'] = 'Parts Holding P1 Hot'
                srow['Entitlement'] = 'P1 - On-Site Hot Parts'
                srow['ServiceProductEntitlementPair'] = srow['Service Product'] + '|' + srow['Entitlement']
                p1hot += 1

    cy_part_replace = Product.Attr('SC_P1P2_Parts_Ext_Price').GetValue() if Product.Attr('SC_P1P2_Parts_Ext_Price').GetValue() != "" else "0"
    py_part_replace = Product.Attr('SC_P1P2_PY_Parts_Ext_Price').GetValue() if Product.Attr('SC_P1P2_PY_Parts_Ext_Price').GetValue() != "" else "0"
    if Product.Attr("SC_P1P2_AutoUpdate_Editable_Ext").GetValue() == "&nbsp":
        srow = sericeEntitlementCont.AddNewRow(False)
        srow['Service Product'] = 'Parts Replacement'
        srow['Entitlement'] = 'Parts Replacement'
        srow['ServiceProductEntitlementPair'] = srow['Service Product'] + '|' + srow['Entitlement']
    elif Product.Attr("SC_P1P2_AutoUpdate_Editable_Ext").GetValue() != "&nbsp" and (float(cy_part_replace) != 0 or float(py_part_replace) != 0):
        srow = sericeEntitlementCont.AddNewRow(False)
        srow['Service Product'] = 'Parts Replacement'
        srow['Entitlement'] = 'Parts Replacement'
        srow['ServiceProductEntitlementPair'] = srow['Service Product'] + '|' + srow['Entitlement']

    sericeEntitlementCont.Calculate()