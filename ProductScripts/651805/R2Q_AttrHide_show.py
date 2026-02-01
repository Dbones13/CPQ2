if Quote.GetCustomField('R2QFlag').Content == 'Yes':
    scopeDict2={}
    if Product.GetContainerByName('AR_HCI_PHD_ProjectInputs2').Rows.Count>0:
        contRows=Product.GetContainerByName('AR_HCI_PHD_ProjectInputs2').Rows[0].Columns
        for col in contRows:
            scopeDict2[col.Name]=col.Value
        if scopeDict2['USM Implementation']=='No':
            Product.DisallowAttr('HCI_PHD_USMConfiguration')
        else:
            Product.AllowAttr('HCI_PHD_USMConfiguration')
        Trace.Write('-scopedict2-'+str(scopeDict2['Graphics and Reports']))
        if scopeDict2['Graphics and Reports']=='No':
            Product.DisallowAttr('HCI_PHD_NewDisplaysforInsight')
            Product.DisallowAttr('HCI_PHD_ExcelReports')
            Product.DisallowAttr('HCI_PHD_MigratedDisplaysforInsight')
            Product.DisallowAttr('HCI_PHD_CrystalReports')
            Product.DisallowAttr('HCI_PHD_SSRS_Reports')
        else:
            Product.AllowAttr('HCI_PHD_NewDisplaysforInsight')
            Product.AllowAttr('HCI_PHD_ExcelReports')
            Product.AllowAttr('HCI_PHD_MigratedDisplaysforInsight')
            Product.AllowAttr('HCI_PHD_CrystalReports')
            Product.AllowAttr('HCI_PHD_SSRS_Reports')