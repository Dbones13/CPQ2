Numof = Product.Attr("ATT_LM_ADDITIONALSWITCHES").GetValue()
if int(Numof) > 0 :
	Product.AllowAttr('ATT_LM_ELMM_ADDITIONAL_SWITCH')
else:
    Product.DisallowAttr('ATT_LM_ELMM_ADDITIONAL_SWITCH')