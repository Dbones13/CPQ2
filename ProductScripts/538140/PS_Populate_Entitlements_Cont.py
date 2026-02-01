EntCont = Product.GetContainerByName('SC_TPS_Entitlements')
EntCont.Rows.Clear()
ValidModelsCont = Product.GetContainerByName('SC_TPS_Models_Scope')

tps_hw = 0
tps_labor = 0
tps_sw_sub = 0


if ValidModelsCont.Rows.Count:
    for row in ValidModelsCont.Rows:
        if row['Entitlement'] == "Third Party Hardware" and tps_hw == 0:
            EntRow = EntCont.AddNewRow(False)
            EntRow['Entitlement'] = "Third Party Hardware"
            tps_hw += 1
        if row['Entitlement'] == "Third Party Labour" and tps_labor == 0:
            EntRow = EntCont.AddNewRow(False)
            EntRow['Entitlement'] = "Third Party Labour"
            tps_labor += 1
        if row['Entitlement'] == "Third Party Software/Subscription" and tps_sw_sub == 0:
            EntRow = EntCont.AddNewRow(False)
            EntRow['Entitlement'] = "Third Party Software/Subscription"
            tps_sw_sub += 1