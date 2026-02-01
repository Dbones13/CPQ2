fieldbus_attr = ["FIM_Type","FIM_Percent_Installed_Spare_Fieldbus_IO","FIM_Num_Devices_Open_Loop","FIM_Num_Devices_Close_Loop","FIM_Num_Close_Loop_per_Segment","FIM_Num_FF_Temp_Mux_per_Segment","FIM_Num_of_MOVs_per_Segment","FIM_FF_IOs_with_Power_conditioner","FIM_Power_Conditioner_Scope","SerC_CG_FIM_FF_IO_Cont","Header_09_close","Header_09_open"]

if Product.Attr('SerC_CG_Foundation_Fieldbus_Interface_required').GetValue() == "Yes":
	for attr in fieldbus_attr:
		Product.AllowAttr(attr)
	Product.Attr('FIM_Type').SelectValue('FIM8')
	Product.Attr('FIM_Percent_Installed_Spare_Fieldbus_IO').AssignValue('0')
	Product.Attr('FIM_Num_Devices_Open_Loop').AssignValue('10')
	Product.Attr('FIM_Num_Devices_Close_Loop').AssignValue('10')
	Product.Attr('FIM_Num_Close_Loop_per_Segment').AssignValue('4')
	Product.Attr('FIM_Num_FF_Temp_Mux_per_Segment').AssignValue('8')
	Product.Attr('FIM_Num_of_MOVs_per_Segment').AssignValue('6')
	Product.ParseString('<*CTX( Container(SerC_CG_FIM_FF_IO_Cont).Column(Future_Red_wo_C300).SetPermission(Hidden) )*>')
	Product.ParseString('<*CTX( Container(SerC_CG_FIM_FF_IO_Cont).Column(Future_Red_C300).SetPermission(Hidden) )*>')
	Fim_Cont = Product.GetContainerByName("SerC_CG_FIM_FF_IO_Cont")
	if Fim_Cont.Rows.Count == 0:
		Fim_Cont.LoadFromDatabase("SELECT IO_Type, Identifiers FROM FIM_FF_IO WHERE Container_Name = 'SerC_CG_FIM_FF_IO_Cont'",'Code')
else:
    Product.GetContainerByName("SerC_CG_FIM_FF_IO_Cont").Rows.Clear()
    for attr in fieldbus_attr:
		Product.DisallowAttr(attr)