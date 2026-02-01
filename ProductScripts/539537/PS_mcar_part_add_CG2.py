if Product.Attr('PERF_ExecuteScripts').GetValue()=='SCRIPT_RUN':
	import GS_PS_Exp_Ent_BOM
	import GS_C300_MCAR_calcs,GS_SerC_Part_Calcs
	import GS_C300_AMP_A_Calcs,GS_C300_Series_C_Turbomachinery_cabinet_bays
	import GS_C300_USCA_intermediate_Calcs,GS_C300_SeriesC_Cabinet_Calcs_2
	import GS_C300_SeriesC_Cabinet_Calcs,GS_C300_SeriesC_Cabinet_Calcs_1
	import GS_C300_CGRG_Cabinet_Cals, GS_C300_SeriesC_cabinet_bays_Cal
	import GS_C300_Calc_Module,GS_C300_markII_umc_calcs,GS_Get_Set_AtvQty
	#PMIO Parts calculation dependent scripts
	import GS_C300_IO_Calc, GS_C300_IO_Calc2 #GS_SerC_Part_Calcs

	cab_bays_kit1,cab_bays_kit2,cab_bays_kit3,cab_bays_kit4,cab_bays_kit5,cab_bays_kit6,cab_bays_kit7,cab_bays_kit8=GS_C300_SeriesC_cabinet_bays_Cal.cab_bays_kit(Product)
	family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
	if family=="Series C" or family=="Turbomachinery":
		if cab_bays_kit5>0:
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","50182411-500",cab_bays_kit5)
		else:
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","50182411-500",0)
		if cab_bays_kit6>0:
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","50182411-700",cab_bays_kit6)
		else:
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","50182411-700",0)
		if cab_bays_kit7>0:
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","50182411-200",cab_bays_kit7)
		else:
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","50182411-200",0)
		if cab_bays_kit8>0:
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","50182411-600",cab_bays_kit8)
		else:
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","50182411-600",0)