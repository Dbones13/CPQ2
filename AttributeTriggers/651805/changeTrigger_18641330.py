noOfSys=Product.Attributes.GetByName('HCI_PHD_NoSysInterfared').GetValue()
noOfSys = int(noOfSys) if noOfSys else 0
cont=Product.GetContainerByName('HCI_PHD_Tech_Scope')
cont.Clear()
for i in range(0,noOfSys):
    row=cont.AddNewRow(False)
    row.GetColumnByName('System to be interfaced to').ReferencingAttribute.SelectDisplayValue('Type A RDI:  Experion Link (Experion or TPS DCS)')
    row['Number of Connections']='1'
    row['Number of Collected Tags']='1000'