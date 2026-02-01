def AssignNewvalue(modeAttr):
	Trace.Write('C300_RG_UPC_Id_Modifier_old===else')
	Product.Attr('C300_RG_UPC_Id_Modifier_old').AssignValue(modeAttr)
modeAttr = Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
modeAttrold = Product.Attr('C300_RG_UPC_Id_Modifier_old').GetValue()
UPC_Cab_Count = Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
if Product.Attr("SerC_IO_Mounting_Solution").GetValue() == "Universal Process Cab - 1.3M" and Product.Attr("C300_RG_UPC_Specify_Id_Modifier").GetValue() == "Yes":
	if modeAttr and len(modeAttr)>=6 and modeAttr[5] in ['t','T'] and UPC_Cab_Count and int(UPC_Cab_Count)>7:
		Product.Messages.Add('Single Mode x4 is not supported as Number of UPC is more than 7, Please add number of UPC less than 8 to configure Daisy Chain')
		Product.Attr('C300_RG_UPC_Id_Modifier').AssignValue(modeAttrold)
	else:
		AssignNewvalue(modeAttr)
else:
	AssignNewvalue(modeAttr)