msidSelectionCon = Product.GetContainerByName('Migration_MSID_Selection_Container')
productContainer = Product.GetContainerByName('Migration_MSID_System_Number_Table')
msidSelection =False
productSelection =False
msidRow = ''
productRow = ''
for row in msidSelectionCon.Rows:
    if row.IsSelected:
        msidSelection= True
        msidRow = row
        break
for row in productContainer.Rows:
    if row.IsSelected:
        productSelection = True
        productRow = row
        break
if msidSelection== True and productSelection ==True:
    msidRow.Product.Attr('Migration_MSID_System_Number').AssignValue(productRow['Migration_MSID_System_Number'])
    msidRow.IsSelected = True
    productContainer.Clear()