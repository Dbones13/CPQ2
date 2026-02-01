def getContainer(Name):
    return Product.GetContainerByName(Name)
'''producthiddenContainer = Product.GetContainerByName('MSID_Product_Container_FSC_IO_hidden')
newRowfsc = producthiddenContainer.AddNewRow('FSC_to_SM_IO_Audit_cpq')
newRowfsc['Product Name'] = "FSC to SM IO Audit"
newRowfsc.ApplyProductChanges()'''


fsctosmgeneralinfo2 = getContainer('FSC_to_SM_IO_Migration_General_Information2')
for row in fsctosmgeneralinfo2.Rows:
    if row.RowIndex > 1:
        break
    row['FSC_to_SM_IO_Migration_3rd_Party_Hardware_per_Audit_Report'] = '0'
fsctosmgeneralinfo2.Calculate()