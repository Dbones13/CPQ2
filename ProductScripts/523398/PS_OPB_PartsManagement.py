SC_Cont = Product.GetContainerByName('Service Contract Modules')
if SC_Cont.Rows.Count:
    for row in SC_Cont.Rows:
        if row['Module'] == 'Parts Management' and row['Type'] == 'Renewal':
            contName = row.Product.GetContainerByName('SC_P1P2_Parts_Details')
            serviceEntitlementCont1 = row.Product.GetContainerByName('SC_P1P2_ServiceProduct_Entitlement_1')
            serviceEntitlementCont1.Rows.Clear()
            p1 = 0
            p2 = 0
            p1hot = 0

            if contName.Rows.Count:
                for partrow in contName.Rows:
                    if partrow['Service_Product'] == 'Parts Holding P1' and p1 == 0:
                        s1row = serviceEntitlementCont1.AddNewRow(False)
                        s1row['Service Product'] = 'Parts Holding P1'
                        s1row['Entitlement'] = 'P1 - On-Site Cold Parts'
                        p1 += 1
                    elif partrow['Service_Product'] == 'Parts Holding P2' and p2 == 0:
                        s1row = serviceEntitlementCont1.AddNewRow(False)
                        s1row['Service Product'] = 'Parts Holding P2'
                        s1row['Entitlement'] = 'P2 - Off-Site Spare Parts'
                        p2 += 1
                    elif partrow['Service_Product'] == 'Parts Holding P1 Hot' and p1hot == 0:
                        s1row = serviceEntitlementCont1.AddNewRow(False)
                        s1row['Service Product'] = 'Parts Holding P1 Hot'
                        s1row['Entitlement'] = 'P1 - On-Site Hot Parts'
                        p1hot += 1

            serviceEntitlementCont1.Calculate()
            if True:
                contigency_cont = row.Product.GetContainerByName("SC_P1P2_Contigency_Cost")
                splist = []
                m=[]
                for row1 in serviceEntitlementCont1.Rows:
                    flag = False
                    for row2 in contigency_cont.Rows:
                        if row1["Service Product"] == row2["Service_Product"]:
                            flag = True
                            break
                    if flag == False:
                        controw = contigency_cont.AddNewRow(False)
                        controw["Service_Product"] = row1["Service Product"]
                        controw.Calculate()
                    splist.append(row1["Service Product"])
                for controw in contigency_cont.Rows:
                    if controw["Service_Product"] not in splist:
                        m.append(row.RowIndex)
                m.reverse()
                for i in m:
                    contigency_cont.DeleteRow(i)
                    contigency_cont.Calculate()
            row.Product.Attr('SC_P1P2_PartsUsageMethod').SelectValue('1 Year Pricing')
            row.Product.ApplyRules()