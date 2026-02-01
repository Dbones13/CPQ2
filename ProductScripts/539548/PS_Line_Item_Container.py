cont = Product.GetContainerByName('CONT_MSID_SUBPRD')
needToAdd_IOhidden = False
needToAdd_FSChidden = False
for row in cont.Rows:
    if row['Selected_Products'] == 'FSC to SM IO Migration':
        needToAdd_IOhidden = True
    if row['Selected_Products'] == 'FSC to SM':
        needToAdd_FSChidden = True

producthiddenContainer = Product.GetContainerByName('MSID_Product_Container_FSC_IO_hidden')
hiddenContainer = Product.GetContainerByName('MSID_Product_Container_FSC_hidden')
if needToAdd_IOhidden and producthiddenContainer.Rows.Count == 0:
    newRowfsc = producthiddenContainer.AddNewRow('FSC_to_SM_IO_Audit_cpq')
    newRowfsc['Product Name'] = "FSC to SM IO Audit"
if needToAdd_FSChidden and hiddenContainer.Rows.Count == 0:
    newRowfsc = hiddenContainer.AddNewRow('FSC_to_SM_Audit_cpq')
    newRowfsc['Product Name'] = "FSC to SM Audit"

if needToAdd_IOhidden == False and producthiddenContainer.Rows.Count:
    Product.GetContainerByName('MSID_Product_Container_FSC_IO_hidden').Rows.Clear()
if needToAdd_FSChidden == False and hiddenContainer.Rows.Count:
    Product.GetContainerByName('MSID_Product_Container_FSC_hidden').Rows.Clear()