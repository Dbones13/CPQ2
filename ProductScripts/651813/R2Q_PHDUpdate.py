if Quote.GetCustomField('isR2QRequest').Content == 'Yes' and Product.Attributes.GetByName('AR_HCI_PHDSectionVisible').GetValue() == 'Yes':
    getprdRow= Product.GetContainerByName('HCI_PHD_Selected_Products').Rows
    def chk(i,col):
      Trace.Write('--columval'+str([col,i.GetColumnByName(col).DisplayValue]))
      displayval= 'Yes' if i.GetColumnByName(col).DisplayValue == 'Yes' else 'No'
      i.GetColumnByName(col).SetAttributeValue(displayval)
    for prdRow in getprdRow:
        if prdRow['Product']=='PHD Labor':
            for i in prdRow.Product.GetContainerByName('HCI_PHD_Tech_Scope').Rows:
                getrow = Product.GetContainerByName('HCI_PHD_Tech_Scope').Rows[i.RowIndex]
                i.GetColumnByName('System to be interfaced to').ReferencingAttribute.SelectDisplayValue(getrow['System to be interfaced to'])
                i['Number of Connections']= getrow['Number of Connections']
                i['Number of Collected Tags']= getrow['Number of Collected Tags']
                i.GetColumnByName('Interface Connectivity Complexity').SetAttributeValue(getrow['Interface Connectivity Complexity'] )
                i.GetColumnByName('Tag configuration Complexity').SetAttributeValue(getrow['Tag configuration Complexity'])
                i['Interface Connectivity Complexity'] = getrow['Interface Connectivity Complexity']
                i['Tag configuration Complexity'] = getrow['Tag configuration Complexity']
            phdConts=['AR_HCI_PHD_ProjectInputs1','AR_HCI_PHD_ProjectInputs2','HCI_PHD_NewDisplaysforInsight','HCI_PHD_ExcelReports']
            for cnt in phdConts:
                if cnt == 'AR_HCI_PHD_ProjectInputs1':
                    for i in prdRow.Product.GetContainerByName(cnt).Rows:
                        getrow = Product.GetContainerByName(cnt).Rows[0]
                        i.GetColumnByName('Upgrade/Update-PHD').SetAttributeValue(getrow['Upgrade/Update-PHD'])
                        i.GetColumnByName('Upgrade/Update-Third Party Historian').SetAttributeValue(getrow['Upgrade/Update-Third Party Historian'])
                        i.GetColumnByName('Scope of Work').SetAttributeValue('Yes')
                        chk(i,'Scope of Work')
                        chk(i,'Build and Configure')
                        chk(i,'Material Ordering')
                        chk(i,'Upgrade/Update-PHD')
                        chk(i,'Upgrade/Update-Third Party Historian')
                        chk(i,'Staging Area Hardware and LAN Setup')
                elif cnt == 'AR_HCI_PHD_ProjectInputs2':
                    for i in prdRow.Product.GetContainerByName(cnt).Rows:
                        getrow = Product.GetContainerByName(cnt).Rows[0]
                        i.GetColumnByName('Graphics and Reports').SetAttributeValue(getrow['Graphics and Reports'])
                        i.GetColumnByName('Test Environment Installation and Setup').SetAttributeValue(getrow['Test Environment Installation and Setup'])
                        i.GetColumnByName('On-Site Installation').SetAttributeValue(getrow['On-Site Installation'])
                        chk(i,'On-Site Installation')
                        chk(i,'Post-Go-Live Activities')
                        chk(i,'Post Delivery Support')
                        chk(i,'USM Implementation')
                        chk(i,'Test Environment Installation and Setup')
                        chk(i,'Graphics and Reports')
                prdRow.Product.Attributes.GetByName('HCI_PHD_IsReports').AssignValue('No')
                if Product.GetContainerByName('AR_HCI_PHD_ProjectInputs2').Rows[0]['Graphics and Reports'] == 'Yes':
                    Trace.Write('yes in reports')
                    prdRow.Product.Attributes.GetByName('HCI_PHD_IsReports').AssignValue('Yes')
                    if cnt == 'HCI_PHD_NewDisplaysforInsight':
                        for i in prdRow.Product.GetContainerByName(cnt).Rows:
                            getrow = Product.GetContainerByName(cnt).Rows[0]
                            Trace.Write('vals--'+str(getrow['New Displays for Insight']))
                            i['New Displays for Insight']= getrow['New Displays for Insight']
                            i['Number of simple displays'] = (getrow['Number of simple displays'])
                            i['Number of medium displays'] = (getrow['Number of medium displays'])
                            i['Number of complex displays']= (getrow['Number of complex displays'])
                    elif cnt == 'HCI_PHD_ExcelReports':
                        for i in prdRow.Product.GetContainerByName(cnt).Rows:
                            getrow = Product.GetContainerByName(cnt).Rows[0]
                            i['Reports']= (getrow['Reports'])
                            i['Number of simple reports'] = (getrow['Number of simple reports'])
                            i['Number of medium reports'] = (getrow['Number of medium reports'])
                            i['Number of complex reports']= (getrow['Number of complex reports'])  

                '''if prdRow.Product.GetContainerByName('HCI_PHD_VirtualCalculations').Rows>0:
                    getrowvirtual = prdRow.Product.GetContainerByName('HCI_PHD_VirtualCalculations').Rows[0]
                else:
                    getrowvirtual = prdRow.Product.GetContainerByName('HCI_PHD_VirtualCalculations').AddNewRow(False)
                getrowvirtual['Virtual Calculations'] = '8'
                getrowvirtual['Number of simple virtual calculations'] = '5'
                getrowvirtual['Number of medium virtual calculations'] = '2'
                getrowvirtual['Number of complex virtual calculations'] = '1' '''


            prdRow.Product.Attributes.GetByName('HCI_NoOf3rdPartyClients').AssignValue(str(Product.Attributes.GetByName('HCI_NoOf3rdPartyClients').GetValue()))