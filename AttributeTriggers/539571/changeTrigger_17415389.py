def AssignNewvalue(UPC_Cab_Count):
	Trace.Write('UPC_Cab_Count=UPC_Cab_Count===else')
	Product.Attr('hdn_C300_RG_UPC_Cab_Count').AssignValue(UPC_Cab_Count)

UPC_Cab_Count = Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
UPC_Cab_Count_old = Product.Attr('hdn_C300_RG_UPC_Cab_Count').GetValue()
UPC_Fiber_Optic_Extender = Product.Attr('C300_RG_UPC_Fiber_Optic_Extender').GetValue()
Trace.Write('UPC_Cab_Count=UPC_Fiber_Optic_Extender==='+str(UPC_Fiber_Optic_Extender))
Trace.Write('UPC_Cab_Count=UPC_Cab_Count==='+str(UPC_Cab_Count))
if UPC_Cab_Count and int(UPC_Cab_Count)>7  and UPC_Fiber_Optic_Extender == 'Single Mode x4':
	Trace.Write('UPC_Cab_Count=UPC_Cab_Count===if')
	Product.Messages.Add('Single Mode x4 is not supported as Number of UPC is more than 7, Please add number of UPC less than 8 to configure Daisy Chain')
	Product.Attr('C300_RG_UPC_Cab_Count').AssignValue(UPC_Cab_Count_old)
elif Product.Attr("SerC_IO_Mounting_Solution").GetValue() == "Universal Process Cab - 1.3M" and Product.Attr("C300_RG_UPC_Specify_Id_Modifier").GetValue() == "Yes":
	modeAttr = Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
	if modeAttr and len(modeAttr)>=6 and modeAttr[5] in ['t','T'] and UPC_Cab_Count and int(UPC_Cab_Count)>7:
		Product.Messages.Add('Single Mode x4 is not supported as Number of UPC is more than 7, Please add number of UPC less than 8 to configure Daisy Chain')
		Product.Attr('C300_RG_UPC_Cab_Count').AssignValue(UPC_Cab_Count_old)
	else:
		AssignNewvalue(UPC_Cab_Count)
else:
	AssignNewvalue(UPC_Cab_Count)