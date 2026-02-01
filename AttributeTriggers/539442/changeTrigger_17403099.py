switch_configuration = Product.Attr('ELCN_Select_Switch_configuration_required').GetValue()
if switch_configuration == "None required from Honeywell" :
    Product.DisallowAttr('ATT_ELCN_Qty_of_NGs_more_than_100mts')
    Product.DisallowAttr('ELCN_Select_type_of_fiber_optic_switch')
elif switch_configuration == "Responsible – Alternate configuration" or switch_configuration == "Non Responsible – Alternate configuration"  :
    Product.AllowAttr('ATT_ELCN_Qty_of_NGs_more_than_100mts')
    Product.AllowAttr('ELCN_Select_type_of_fiber_optic_switch')