if Product.Attr('PERF_ExecuteScripts').GetValue()=='SCRIPT_RUN':
	import GS_PS_Exp_Ent_BOM
	import GS_C300_SeriesC_cabinet_bays_Cal
	#PMIO calculation dependent scripts

	cab_bays_kit1,cab_bays_kit2,cab_bays_kit3,cab_bays_kit4,cab_bays_kit5,cab_bays_kit6,cab_bays_kit7,cab_bays_kit8=GS_C300_SeriesC_cabinet_bays_Cal.cab_bays_kit(Product)
	io_family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
	if io_family=="Series C":
		if cab_bays_kit5>0:
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","50182411-500",cab_bays_kit5)
		else:
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","50182411-500",0)
		if cab_bays_kit6>0:
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","50182411-700",cab_bays_kit6)
		else:
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","50182411-700",0)
		if cab_bays_kit7>0:
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","50182411-200",cab_bays_kit7)
		else:
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","50182411-200",0)
		if cab_bays_kit8>0:
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","50182411-600",cab_bays_kit8)
		else:
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","50182411-600",0)