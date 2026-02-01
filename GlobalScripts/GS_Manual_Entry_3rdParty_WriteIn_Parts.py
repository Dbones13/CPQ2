def Manual_Entry_3rdParty(cartitem):
	#check if cartitem.Partnumber  exists in WriteInProducts
    writeInProduct = SqlHelper.GetFirst("SELECT Description from WriteInProducts(nolock) where Product = '"+cartitem.PartNumber +"'")
    Trace.Write("writeinproduct"+str(cartitem.PartNumber))
    if writeInProduct is None:
        info = SqlHelper.GetFirst("SELECT ProductLine, ProductLineDescription, ProductLineSubGroupDescription, ProductLineSubGroup, UnitofMeasure from ThirdPartyWriteinParts")
        if info:
            cartitem.QI_ProductLine.Value = info.ProductLine
            cartitem.QI_ProductLineDesc.Value = info.ProductLineDescription
            cartitem.QI_PLSG.Value = info.ProductLineSubGroup
            cartitem.QI_PLSGDesc.Value = info.ProductLineSubGroupDescription
            cartitem.QI_UoM.Value = info.UnitofMeasure