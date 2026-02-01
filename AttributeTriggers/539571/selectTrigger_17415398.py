if Product.Attr('C300_RG_UPC_CNM').GetValue() != '':
    UPC = Product.Attr('C300_RG_UPC_CNM').SelectedValue.ValueCode
    if UPC == 'N':
        Product.DisallowAttrValues('C300_RG_UPC_CNM_Exp_Module', 'Y')
        Product.SelectAttrValues('C300_RG_UPC_CNM_Exp_Module', 'N')