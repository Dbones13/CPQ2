selectAll=Product.Attr('AR_HCI_SELECTALL').GetValue()
contList=['HCI_PHD_ProjectManagement','HCI_PHD_ProjectManagement2','HCI_PHD_AdditionalDeliverables']
for cont in contList:
    for row in Product.GetContainerByName(cont).Rows:
        if row['Deliverable']!='Total':
            if selectAll:
                row.IsSelected = True
            else:
                row.IsSelected = False