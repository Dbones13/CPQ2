if Product.Attributes.GetByName("SC_Product_Type").GetValue() == "New":
    cont = Product.GetContainerByName('CBM_Pricing_Container')
    CBMCycle = (Product.Attributes.GetByName("CBM_PM/CBM_Cycles").GetValue())
    for row in cont.Rows:
        ProductFam = row.Product.Attr('CBM_PRODUCT_FAMILY').GetValue()
        Trace.Write(ProductFam)
        AssetType = row.Product.Attr('CBM_ASSET_TYPE').GetValue()
        Count = row['Count']
        AnnPrice = row['Annual Price']
        Task = row['Tasks']
        Main = row['Local Preventive Maintenance Tasks']
        LevelOff = row['Level']
        row['HDPY_ProductFamily'] = ProductFam
        row['HDPY_AssetType'] = AssetType
        row['HDPY_Count'] = Count
        row['HDPY_LevelOffering'] = LevelOff
        row['HDPY_PMCBM'] = CBMCycle
        row['HDPY_ListPrice'] = AnnPrice
        row['HDPY_Task'] = Task
        row['HDPY_Preventive'] = Main
    cont.Calculate()
elif Product.Attributes.GetByName("SC_Product_Type").GetValue() == "Renewal":
    cont = Product.GetContainerByName('CBM_Pricing_Container')
    CBMCycle = (Product.Attributes.GetByName("CBM_PM/CBM_Cycles").GetValue())
    for row in cont.Rows:
        ProductFam = row.Product.Attr('CBM_PRODUCT_FAMILY').GetValue()
        AssetType = row.Product.Attr('CBM_ASSET_TYPE').GetValue()
        Count = row['CY_Count']
        AnnPrice = row['CY_ListPrice']
        Task = row['CY_Task']
        Main = row['CY_Preventive']
        LevelOff = row['Level']
        row['HDPY_ProductFamily'] = ProductFam
        row['HDPY_AssetType'] = AssetType
        row['HDPY_Count'] = Count
        row['HDPY_LevelOffering'] = LevelOff
        row['HDPY_PMCBM'] = CBMCycle
        row['HDPY_ListPrice'] = AnnPrice
        row['HDPY_Task'] = Task
        row['HDPY_Preventive'] = Main
    cont.Calculate()