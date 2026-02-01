R2Q_powersystem = Product.Attr('SerC_CG_R2Q_Power_System_Vendor').GetValue()
if R2Q_powersystem:
	Product.Attr('SerC_CG_Power_System_Vendor').SelectDisplayValue(R2Q_powersystem)