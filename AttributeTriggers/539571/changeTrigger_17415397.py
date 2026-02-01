if Product.Attr('C300_RG_UPC_Ext_FDAP_Comm_Supp').GetValue() != '':
    RG_UPC = Product.Attr('C300_RG_UPC_Ext_FDAP_Comm_Supp').SelectedValue.ValueCode
    if RG_UPC == 'M':
        Product.DisallowAttrValues('C300_RG_UPC_Fiber_Optic_Extender', 'Single Mode x2', 'Single Mode x4')
    elif RG_UPC == 'S':
        Product.DisallowAttrValues('C300_RG_UPC_Fiber_Optic_Extender', 'Multi Mode x2')