noOfMSID = Product.Attr('Migration_Number_Of_MSID').GetValue()
noOfMSID = int(noOfMSID) if noOfMSID else 0

msidCont = Product.GetContainerByName('Migration_MSID_Selection_Container')

for i in range(noOfMSID):
    msidCont.AddNewRow(False)