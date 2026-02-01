RGDist = Product.Attr('SerC_RG_Distance_for_SeriesC_Remote_Group').GetValue()
if RGDist == '10.0 KM':
    Product.DisallowAttrValues('SerC_RG_CN100/_FOE_Fiber_Type', 'Multi Mode')