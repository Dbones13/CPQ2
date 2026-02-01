from ProductUtil import getContainer
selectedProducts = list()
for row in getContainer(Product,"MSID_Product_Container").Rows:
    selectedProducts.append(row["Product Name"])
if "OPM" in selectedProducts and Product.Tabs.GetByName('OPM').IsSelected:
    con = getContainer(Product,'OPM_Migration_platforms')
    rowIndex = con.AddNewRow(True).RowIndex
    con.DeleteRow(rowIndex)
    con.Calculate()