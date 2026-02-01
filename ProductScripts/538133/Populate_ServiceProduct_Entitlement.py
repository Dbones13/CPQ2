partDetailsCont = Product.GetContainerByName('SC_P1P2_Parts_Details')
sericeEntitlementCont1 = Product.GetContainerByName('SC_P1P2_ServiceProduct_Entitlement_1')
sericeEntitlementCont1.Rows.Clear()
p1 = 0
p2 = 0
p1hot = 0

if partDetailsCont.Rows.Count:
    for row in partDetailsCont.Rows:
        if row['Service_Product'] == 'Parts Holding P1' and p1 == 0:
            s1row = sericeEntitlementCont1.AddNewRow(False)
            s1row['Service Product'] = 'Parts Holding P1'
            s1row['Entitlement'] = 'P1 - On-Site Cold Parts'
            p1 += 1
        elif row['Service_Product'] == 'Parts Holding P2' and p2 == 0:
            s1row = sericeEntitlementCont1.AddNewRow(False)
            s1row['Service Product'] = 'Parts Holding P2'
            s1row['Entitlement'] = 'P2 - Off-Site Spare Parts'
            p2 += 1
        elif row['Service_Product'] == 'Parts Holding P1 Hot' and p1hot == 0:
            s1row = sericeEntitlementCont1.AddNewRow(False)
            s1row['Service Product'] = 'Parts Holding P1 Hot'
            s1row['Entitlement'] = 'P1 - On-Site Hot Parts'
            p1hot += 1

sericeEntitlementCont1.Calculate()