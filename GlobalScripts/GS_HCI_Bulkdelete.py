def deletecontainerrow(contname):
    for name in contname:
        deleteindex = []
        getrow = Product.GetContainerByName(name)
        deleteindex = [row.RowIndex for row in getrow.Rows if row.IsSelected]
        deleteindex.reverse()
        for delrow in deleteindex:
            getrow.DeleteRow(delrow)
    return ''
    


productname = Product.Name 
if(productname == 'HCI Labor Upload'):
    deletecontainerrow(['AR_HCI_LABOR_CONTAINER'])
    if Product.GetContainerByName('AR_HCI_LABOR_CONTAINER').Rows.Count>0:
        from GS_HCI_LABOR_CommonModule import HCIModule
        HCIMod = HCIModule(Quote, Product)
        cont = Product.GetContainerByName('AR_HCI_LABOR_CONTAINER')
        HCIMod.addupdateTotalRow(cont)
elif(productname in ['PHD Labor','Uniformance Insight Labor']):
    deletecontainerrow(['HCI_PHD_EngineeringLabour','HCI_PHD_ProjectManagement','HCI_PHD_ProjectManagement2','HCI_PHD_AdditionalDeliverables'])
elif(productname == 'AFM Labor'):
    deletecontainerrow(['HCI_PHD_ProjectManagement','HCI_PHD_ProjectManagement2','HCI_PHD_AdditionalDeliverables'])