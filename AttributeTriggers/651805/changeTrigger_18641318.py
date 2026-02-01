selectAll=Product.Attr('AR_HCI_SELECTALL').GetValue()
for row in Product.GetContainerByName("HCI_PHD_EngineeringLabour").Rows:
    if row['Header']!='Header' and row['Deliverable']!='Total':
        if selectAll:
            row.IsSelected = True
        else:
            row.IsSelected = False
contList=['HCI_PHD_ProjectManagement','HCI_PHD_ProjectManagement2','HCI_PHD_AdditionalDeliverables']
for cont in contList:
    for row in Product.GetContainerByName(cont).Rows:
        if row['Deliverable']!='Total':
            if selectAll:
                row.IsSelected = True
            else:
                row.IsSelected = False