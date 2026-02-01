Addswitch = Product.Attr("ATT_LM_ELMM_HONEYWELL_PROVIDE_FTE").GetValue()
if Addswitch != 'Yes':
    Product.DisallowAttr('LM_to_ELMM Cable Length')
else:
    Product.AllowAttr('LM_to_ELMM Cable Length')