if Product.Attributes.GetByName('R2QRequest').GetValue() != 'Yes':
    noOfSys=Product.Attributes.GetByName('AR_HCI_No_FO_ENG').GetValue()
    noOfSys = int(noOfSys) if noOfSys else 0
    cont=Product.GetContainerByName('HCI_PHD_Fo_Eng')
    cont.Clear()
    for i in range(0,noOfSys):
        row=cont.AddNewRow(False)
        row['Engineer']='FO Eng '+str(i+1)
        row.GetColumnByName('Activity Type').ReferencingAttribute.SelectDisplayValue('PHD Sr Eng')
        row.GetColumnByName('Execution Country').ReferencingAttribute.SelectDisplayValue('United States')