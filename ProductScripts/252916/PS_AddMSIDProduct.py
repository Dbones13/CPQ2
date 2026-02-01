def getContainer(containerName):
    return Product.GetContainerByName(containerName)

msidContianer = getContainer('Migration_MSID_Selection_Container');

if msidContianer.Rows.Count == 0:
    newRow = msidContianer.AddNewRow()