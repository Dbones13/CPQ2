UPC_Fiber_Optic_Extender = Product.Attr('C300_RG_UPC_Fiber_Optic_Extender').GetValue()
UPC_Fiber_Optic_Extender_old = Product.Attr('hdn_C300_RG_UPC_Fiber_Optic_Extender').GetValue()
UPC_Cab_Count = Product.Attr('C300_RG_UPC_Cab_Count').GetValue() if Product.Attr('C300_RG_UPC_Cab_Count').GetValue() != '' else 0
if int(UPC_Cab_Count)>7  and UPC_Fiber_Optic_Extender == 'Single Mode x4':
	Product.Messages.Add('Single Mode x4 is not supported as Number of UPC is more than 7, Please add number of UPC less than 8 to configure Daisy Chain')
	Product.Attr('C300_RG_UPC_Fiber_Optic_Extender').SelectValue(UPC_Fiber_Optic_Extender_old)
else:
	Product.Attr('hdn_C300_RG_UPC_Fiber_Optic_Extender').SelectValue(UPC_Fiber_Optic_Extender)
if UPC_Fiber_Optic_Extender == 'None':
	Product.ResetAttr('C300_RG_UPC_CN100_IO_HIVE')