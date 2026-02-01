phdConts=['AR_HCI_PHD_ProjectInputs1','AR_HCI_PHD_ProjectInputs2','HCI_PHD_NewDisplaysforInsight','HCI_PHD_MigratedDisplaysforInsight','HCI_PHD_ExcelReports','HCI_PHD_CrystalReports','HCI_PHD_SSRS_Reports','HCI_PHD_Hardware','HCI_PHD_VirtualCalculations','HCI_PHD_USMConfiguration']
for conts in phdConts:
    prdCont=Product.GetContainerByName(conts)
    if prdCont.Rows.Count==0:
        prdCont.AddNewRow(False)