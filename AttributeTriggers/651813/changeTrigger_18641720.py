if Product.Attributes.GetByName('R2QRequest').GetValue() != 'Yes':
    noOfSys=Product.Attributes.GetByName('AR_HCI_No_GES_ENG').GetValue()
    noOfSys = int(noOfSys) if noOfSys else 0
    cont=Product.GetContainerByName('HCI_PHD_GES_Eng')
    cont.Clear()
    for i in range(0,noOfSys):
        row=cont.AddNewRow(False)
        row['Engineer']='GES Eng '+str(i+1)
        row.GetColumnByName('Activity Type').ReferencingAttribute.SelectDisplayValue('ADV GES Sr Eng-IN')
        row['Number of trips per engineer']='1'