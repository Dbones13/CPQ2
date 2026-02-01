from GS_PCN_Populate_Write_Ins import updateWriteIn
Product.GetContainerByName('Write-In Entitlements for Cyber').Rows.Clear()
updateWriteIn(Product)