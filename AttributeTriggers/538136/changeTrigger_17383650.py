if 1:
    from GS_SC_CBM_PRICING_CALCULATIONS import reset_values
    Trace.Write("$$$$$$$$$$$$$$Product Family Changed$$$$$$$$$$$$$$$")
    Trace.Write(Product.Attr('CBM_PRODUCT_FAMILY').GetValue())
    Product.ResetAttr('CBM_ASSET_TYPE')
    reset_values(Product)