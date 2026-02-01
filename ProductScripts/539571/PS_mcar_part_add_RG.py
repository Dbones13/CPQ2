if Product.Attr('PERF_ExecuteScripts').GetValue()=='SCRIPT_RUN':
	import GS_PS_Exp_Ent_BOM, GS_SerC_Part_Calcs
	import GS_C300_MCAR_calcs
	import GS_C300_AMP_A_Calcs
	import GS_C300_RG_UPC_Calc
	import GS_SerC_CG_RG_Amps
	import GS_C300_RG_UPC_parts
	import GS_C300_USCA_intermediate_Calcs,GS_C300_SeriesC_Cabinet_Calcs_2
	import GS_C300_SeriesC_Cabinet_Calcs,GS_C300_SeriesC_Cabinet_Calcs_1
	import GS_C300_CGRG_Cabinet_Cals,GS_C300_SeriesC_cabinet_bays_Cal,GS_C300_Series_C_Turbomachinery_cabinet_bays
	import GS_C300_Calc_Module,GS_C300_markII_umc_calcs,GS_Get_Set_AtvQty
	#PMIO calculation dependent scripts
	import GS_C300_IO_Calc, GS_C300_IO_Calc2
	IO_Family_Type = Product.Attr('SerC_CG_IO_Family_Type').GetValue()
	percentInstalledSpare = Product.Attr('SerC_RG_Percent_Installed_Spare(0-100%)').GetValue()
	IO_Mounting_Solution = Product.Attr('SerC_IO_Mounting_Solution').GetValue()
	Universal_Marshalling_Cabinet = Product.Attr('Ser_RG_Universal_Marshalling_Cabinet').GetValue()
	contName1 = ''

	Product.ExecuteRulesOnce = True
	qty = int(GS_Get_Set_AtvQty.getAtvQty(Product,'Series_C_RG_Part_Summary','MU-TMCN01'))
	Sum_IsM,Sum_Is1M,Sum_NIsM,Sum_NIs1M=GS_C300_markII_umc_calcs.USCA_Calcs1(Product)
	CC_USCH01_qty=GS_C300_markII_umc_calcs.USCA_Calcs1_digital(Product)
	sic0,sic11,sic22,sic33,sic44,sic55,sic66,sic77=GS_C300_markII_umc_calcs.part_condition(Product)
	sic,sic1,sic2,sic3,sic4,sic5,sic6,sic7=GS_C300_USCA_intermediate_Calcs.part_condition(Product)
	Sum_Is,Sum_NIs,Sum_Is1,Sum_NIs1,Sum_HV=GS_C300_USCA_intermediate_Calcs.USCA_Calcs(Product)
	Turbo1,Turbo2,Turbo3,Turbo4,MU_CULF01,MU_C8TRM1,Q_51199948100,Turbo5,Turbo6,Turbo7=GS_C300_SeriesC_Cabinet_Calcs_2.C300_part1(Product)
	MU_C8SBA1,MU_C8SBA2,MU_C8DBA1,MU_C8DBA2=GS_C300_SeriesC_Cabinet_Calcs_2.C300_part3(Product)
	Q51197165_100,Q51197165_200,Q51199947_175,Q51199947_275,Q51199947_375=GS_C300_SeriesC_Cabinet_Calcs_2.C300_part2(Product)
	MU_C8DSS1,MU_C8SSS1=GS_C300_SeriesC_Cabinet_Calcs_2.C300_part4(Product)
	QTY_F,QTY_G1,QTY_G2,QTY_G3,QTY_H1,QTY_H2,QTY_H3,QTY_H4,QTY_H5,QTY_H6,QTY_H7,QTY_H8=GS_C300_SeriesC_Cabinet_Calcs_1.C300_calcs_part2(Product)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-MCC003",0)
	Trace.Write("IS Sum_Is --------->> "+str(Sum_Is))
	Trace.Write("IS Sum_NIs --------->> "+str(Sum_NIs))
	Val_AA=0

	#11K. #CXCPQ-45499
	io_family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
	io_mounting=Product.Attr('SerC_IO_Mounting_Solution').GetValue()
	val_11new=0
	Val_10new=0
	val_11=GS_C300_RG_UPC_Calc.getC300UPC_45499(Product)
	var10=GS_C300_RG_UPC_parts.getpart_CC_UGIA01(Product)
	if io_family=='Series C':
		if io_mounting=='Universal Process Cab - 1.3M':
			val_11new=int(val_11)
			Val_10new=int(var10)
	#added by Lahu CXCPQ-43242,CXCPQ-43392,CXCPQ-43393,CXCPQ-43394,CXCPQ-43395,CXCPQ-46092
	SUM_HI,SUM_LO,SUM_HI1,SUM_LO1,SUM_HI11,SUM_LO11,SUM_D,HI,LO,LL  = GS_C300_MCAR_calcs.mcar_cals(Product)
	SUM_G,GI=GS_C300_MCAR_calcs.MCARW1(Product)
	mcar=GS_C300_MCAR_calcs.MCC003(Product)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-MCAR01",SUM_HI+SUM_LO+SUM_HI1+SUM_LO1)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-MCAR30",SUM_HI11+SUM_LO11)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-MCARW1",SUM_G)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-TMCN01",SUM_D)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-MCC003",mcar)
	#CXCPQ-51523
	#GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","FC-USCA01",Sum_Is+Sum_NIs+val_11new+Sum_IsM+Sum_NIsM)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","FC-USCA01",Sum_NIs+Sum_NIsM+val_11new)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-UGIA01",Sum_Is+Sum_IsM+Val_10new)

	#CXDEV-8784
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-USCH01",Sum_HV+CC_USCH01_qty)
	#CCEECOMMBR-6722
	#GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","FC-USCA01",(Sum_Is+Sum_NIs+val_11new+Sum_IsM+Sum_NIsM)*16)

	if io_family=='Series C':
		if io_mounting=='Universal Process Cab - 1.3M':
			#CXCPQ-45887 by Ravika Pupneja
			CCMCC003_qty=GS_C300_RG_UPC_Calc.getC300UpsCals_CCMCC003(Product)
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-MCC003",CCMCC003_qty)
	#umc Cabale Part
	#CXCPQ-51523
	#CXDEV-8316
	USCA01_Qty = GS_Get_Set_AtvQty.getAtvQty(Product,"Series_C_RG_Part_Summary",'FC-USCA01')
	UGIA01_Qty = GS_Get_Set_AtvQty.getAtvQty(Product,"Series_C_RG_Part_Summary",'CC-UGIA01')
	USCH01_Qty = GS_Get_Set_AtvQty.getAtvQty(Product,"Series_C_RG_Part_Summary",'CC-USCH01')
	SicCableQty = USCA01_Qty + UGIA01_Qty + USCH01_Qty
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-SICC-1011/LR15",0)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-SICC-1011/L06",0)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-SICC-1011/L10",0)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-SICC-1011/L15",0)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-SICC-1011/L20",0)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-SICC-1011/L25",0)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-SICC-1011/L30",0)
	try:
		SicCabLen = Product.Attr("SeriesC_RG_SICLength").GetValue()
	except:
		SicCabLen = ''

	if SicCabLen == '1500MM':
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-SICC-1011/LR15",SicCableQty)
	elif SicCabLen == '6000MM':
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-SICC-1011/L06",SicCableQty)
	elif SicCabLen == '10000MM':
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-SICC-1011/L10",SicCableQty)
	elif SicCabLen == '15000MM':
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-SICC-1011/L15",SicCableQty)
	elif SicCabLen == '20000MM':
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-SICC-1011/L20",SicCableQty)
	elif SicCabLen == '25000MM':
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-SICC-1011/L25",SicCableQty)
	elif SicCabLen == '30000MM':
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-SICC-1011/L30",SicCableQty)
	# added by Lahu CXCPQ-43242,CXCPQ-43393,CXCPQ-43394,CXCPQ-43395,CXCPQ-46092 END

	#UMC IS/Non Is CXCPQ-47005,CXCPQ-47000,CXCPQ-47013,CXCPQ-47002,CXCPQ-47001,CXCPQ-46993,CXCPQ-47012,CXCPQ-47006,CXCPQ-47003,CXCPQ-47011,CXCPQ-46119,CXCPQ-47004 part start
	var1,var2,var3,var4,var5,var6,var7,var8,var9,var10,var11,var12,var13,var14,var15,var16,var17,var18,var19,var20,var21,var22,var23,var24,var25,var26,var27,var28,var29,var30,var31,var32,var36,var34,var35,var37=GS_C300_USCA_intermediate_Calcs.UmcPart(Product)
	#CXCPQ-51523
	var101,var202,var33,var44,var55,var66,var77,var88,var99,var100,var111,var122,var133,var144,var155,var166,var177,var188,var199,var200,var211,var222,var233,var244,var255,var266,var277,var288,var299,var300,var311,var322,var333,var344,var355,var366=GS_C300_markII_umc_calcs.UmcPart(Product)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MCD-ES-2P-488",var1+var101)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MCD-ES-2P-488IS",var2+var202)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MCS-ES-2I-224",var3+var33)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MCS-ES-2I-224IS",var4+var44)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MCD-PS-2P-488",var5+var55)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MCD-PS-2P-488IS",var6+var66)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MCS-ES-3I-336",var7+var77)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MCS-ES-3I-336IS",var8+var88)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MCS-ES-2P-224",var9+var99)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MCS-ES-2P-224IS",var10+var100)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MCD-ES-3I-720",var11+var111)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MCD-ES-3I-720IS",var12+var122)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MCD-PS-2I-488",var13+var133)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MCD-PS-2I-488IS",var14+var144)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MCD-ES-2I-480",var15+var155)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MCD-ES-2I-480IS",var16+var166)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MCS-PS-2P-192",var17+var177)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MCS-PS-2P-192IS",var18+var188)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MCD-PS-3I-672",var19+var199)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MCD-PS-3I-672IS",var20+var200)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MCS-PS-2I-192",var21+var211)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MCS-PS-2I-192IS",var22+var222)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MCS-PS-3I-288",var23+var233)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MCS-PS-3I-288IS",var24+var244)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MCD-PS-2P-384H",var25+var277)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MCD-PS-2I-384H",var26+var311)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MCD-PS-3I-576H",var27+var344)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MCD-ES-2I-416H",var28+var322)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MCD-ES-2P-416H",var29+var255)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MCD-ES-3I-624H",var30+var300)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MCS-PS-2P-160H",var31+var333)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MCS-PS-2I-160H",var32+var355)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MCS-ES-2P-192H",var36+var299)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MCS-ES-2I-192H",var34+var266)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MCS-ES-3I-288H",var35+var288)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MCS-PS-3I-240H",var37+var366)
	#UMC IS/Non Is CXCPQ-47005,CXCPQ-47000,CXCPQ-47013,CXCPQ-47002,CXCPQ-47001,CXCPQ-46993,CXCPQ-47012,CXCPQ-47006,CXCPQ-47003,CXCPQ-47011,CXCPQ-46119,CXCPQ-47004 part end
	#CXCPQ-47390,CXCPQ-47449,CXCPQ-47451,CXCPQ-47453,CXCPQ-47454,CXCPQ-39368,CXCPQ-47422,CXCPQ-47448,CXCPQ-47395,CXCPQ-47418,CXCPQ-34704 start
	CADS11,part600,part400,part500,CBDS01,CASS12,part200,CASS11,part300,part100,CBDD01,CADS12,X,Y,Z,K,L,C1,C2,C3,C4,C8SS01=GS_C300_MCAR_calcs.cab_c(Product) #CXCPQ-116603
	CBDS011,CBDD011,RF_4,RR_3,RFR_2,RF_6,RR_5,RFR_5,Std_5,Gray_200,Custom_100,Single_S1,Single_D1,Dual_S1,Dual_D1,Single_130,Single_180,Dual_130,Dual_180,Xx,Yy,Zz,Ll,C11,C22=GS_C300_MCAR_calcs.cab_51436(Product)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-CADS11",CADS11)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51454314-600",part600)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51454314-400",part400)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-CBDD01",CBDD01+CBDD011) #CXCPQ-51502
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51454314-500",part500)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-CBDS01",CBDS01+CBDS011) #CXCPQ-51473
	if io_family=='Series C':
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-CASS12",CASS12) # CXCPQ-82263
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-CADS12",CADS12) # CXCPQ-82264
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51454314-200",part200)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-CASS11",CASS11)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51454314-300",part300)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51454314-100",part100)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-C8SS01",C8SS01) #CXCPQ-116603
	"""Product.Messages.Add("Cab C1 is {}".format(C1))
	Product.Messages.Add("Cab C2 is {}".format(C2))
	Product.Messages.Add("Cab C3 is {}".format(C3))
	Product.Messages.Add("Cab C4 is {}".format(C4))"""
	##CXCPQ-47390,CXCPQ-47449,CXCPQ-47451,CXCPQ-47453,CXCPQ-47454,CXCPQ-39368,CXCPQ-47422,CXCPQ-47448,CXCPQ-47395,CXCPQ-47418,CXCPQ-34704 end
	#Product.ApplyRules()
	A,B,C,DD,E,F,G,H,I,Sum=GS_C300_MCAR_calcs.mcar_calsmark(Product)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51454909-100",Sum)
	#CXCPQ-58481
	Qty_R01=GS_Get_Set_AtvQty.getAtvQty(Product,"Series_C_RG_Part_Summary","CC-MCAR01")
	Qty_N01=GS_Get_Set_AtvQty.getAtvQty(Product,"Series_C_RG_Part_Summary","MU-TMCN01")
	QTY_A,QTY_B,QTY_C,QTY_D,QTY_E1,QTY_E2,QTY_E3,QTY_E4,Val_A,Val_B,Val_C=GS_C300_SeriesC_Cabinet_Calcs.C300_calcs_part(Product,Qty_R01,Qty_N01)
	#CXCPQ-47603,47620,35489,35488,34706,45657,45708,35487,47590
	#CXCPQ-47603
	Qty_476031,Qty_476032=GS_C300_CGRG_Cabinet_Cals.C300_Cabinet(Product,CBDS01,CBDD01,CASS12,CADS12)
	Thermo_qnt2,Thermo_qnt4,cab9_2,power2,cab200,cab100=GS_C300_MCAR_calcs.cabmarkII(Product)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51121311-200",int(Qty_476031)+int(cab100)+int(Turbo7))
	#CXCPQ-47807,CXCPQ-47806
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51203157-900",cab9_2)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51121311-100",int(cab200)+int(Qty_476032)+int(Turbo6))
	#CXCPQ-47620,51553
	Qty_47620=GS_C300_CGRG_Cabinet_Cals.C300_Cabinet1(Product)
	if Qty_47620>0 or Turbo3>0 or Turbo4>0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202335-300",Qty_47620+Turbo3+Turbo4)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202335-300",0)

	# CXDEV-8813 - KAOUSALYA ADALA
	if IO_Family_Type == 'Series-C Mark II':
		contName1 = 'C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont1'
		GS_C300_IO_Calc.applyPercentage(Product, percentInstalledSpare, IO_Family_Type, IO_Mounting_Solution, Universal_Marshalling_Cabinet, contName1, '', '')
		parts_dict=dict()
		parts_dict = GS_C300_IO_Calc2.getParts44488(Product, parts_dict)
		if len(parts_dict)>0:
			GS_C300_IO_Calc.setIOCount(Product, 'Series_C_RG_Part_Summary', parts_dict)
		isR2Qquote = True if Quote.GetCustomField("isR2QRequest").Content else False
		if isR2Qquote:
			parts_dict=dict()
			parts_dict = GS_C300_IO_Calc2.getParts44490(Product, parts_dict)
			if len(parts_dict)>0:
				GS_C300_IO_Calc.setIOCount(Product, 'Series_C_RG_Part_Summary', parts_dict)

	#CXCPQ-35489
	Qty_354891,Qty_3548911,Qty_354892,Qty_3548922,Qty_83004,Qty_830044,Qty_83157,Qty_831577=GS_C300_CGRG_Cabinet_Cals.C300_Cabinet2(Product,CBDS01,CASS12,part300,part200,CBDD01,CADS12,part100)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-C8SBA1",Qty_354891+MU_C8SBA1)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-C8SBA2",Qty_3548911+MU_C8SBA2)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-C8DBA1",Qty_354892+MU_C8DBA1)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-C8DBA2",Qty_3548922+MU_C8DBA2)
	#CXCPQ-83004
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-CASBA1",Qty_83004)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-CASBA2",Qty_830044)
	#CXCPQ-83157 - kaousalya
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-CADBA1",Qty_83157)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-CADBA2",Qty_831577)
	#CXCPQ-35488 and #CXCPQ-51514
	Qty_35488,Qty_354882=GS_C300_CGRG_Cabinet_Cals.C300_Cabinet3(Product,CBDS01,CASS12,part300,part200,CBDD01,CADS12,part100)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51197174-200",int(Qty_35488)+int(Gray_200))
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51197174-100",int(Qty_354882)+int(Custom_100))
	#CXCPQ-34706
	Qty_34706,Qty_347062,Qty_82979,Qty_829792=GS_C300_CGRG_Cabinet_Cals.C300_Cabinet4(Product,CBDS01,CASS12,part300,part200,CBDD01,CADS12,part100)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51197165-100",Qty_34706+Q51197165_100)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51197165-200",Qty_347062+Q51197165_200)
	#CXCPQ-82979
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","50185183-100",Qty_82979)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","50185183-200",Qty_829792)
	#CXCPQ-47603
	Qty_476031,Qty_476032=GS_C300_CGRG_Cabinet_Cals.C300_Cabinet(Product,CBDS01,CBDD01,CASS12,CADS12)
	Thermo_qnt2,Thermo_qnt4,cab9_2,power2,cab200,cab100=GS_C300_MCAR_calcs.cabmarkII(Product)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51121311-200",int(Qty_476031)+int(cab100)+int(Turbo7))
	#CXCPQ-47807,CXCPQ-47806
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51203157-900",cab9_2)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51121311-100",int(cab200)+int(Qty_476032)+int(Turbo6))
	#CXCPQ-45657
	Qty_45657,Qty_456572=GS_C300_CGRG_Cabinet_Cals.C300_Cabinet5(Product)
	if Qty_45657>0 or Qty_456572>0 or cab9_2>0 or Turbo5>0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51198959-200",int(Qty_45657)+int(cab9_2)+int(Turbo5))
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51199607-900",Qty_456572+Turbo5)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51198959-200",0)
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51199607-900",0)
	#CXCPQ-45708+Turbo5
	Qty_45708,Qty_457082=GS_C300_CGRG_Cabinet_Cals.C300_Cabinet6(Product,QTY_A,QTY_D)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51154857-300",Qty_45708)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51154857-400",Qty_457082)
	#CXCPQ-35487
	Qty_35487=GS_C300_CGRG_Cabinet_Cals.C300_Cabinet7(Product)
	if Qty_35487>0 or Thermo_qnt4>0 or MU_CULF01>0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-CULF01",int(Qty_35487)+int(Thermo_qnt4)+int(MU_CULF01))
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-CULF01",0)
	#CXCPQ-47590 and #59246
	Qty_47590,Qty_475902,Qty_475903,Qty_475904=GS_C300_CGRG_Cabinet_Cals.C300_Cabinet8(Product)
	if Qty_47590>0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51454186-200",Qty_47590)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51454186-200",0)
	if Qty_475902>0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51454187-200",Qty_475902)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51454187-200",0)
	if Qty_475903>0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51454186-100",Qty_475903)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51454186-100",0)
	if Qty_475904>0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51454187-100",Qty_475904)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51454187-100",0)
	#45796 Added by Shivani
	Qty100=GS_C300_SeriesC_cabinet_bays_Cal.Cab_qty100(Product)
	if Qty100>0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51109524-100",Qty100)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51109524-100",0)
	#49226 Shivani
	'''A=GS_C300_SeriesC_cabinet_bays_Cal.cab_bays400(Product)
	if A>0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51196958-400",A)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51196958-400",0)'''
	#45766,51571,51568 Shivani
	Turbo_Cab_qty3,Turbo_Cab_qty4=GS_C300_Series_C_Turbomachinery_cabinet_bays.Turbo_Cab_qty2(Product)
	Turbo_Cab_qty1,Turbo_Cab_qty2=GS_C300_Series_C_Turbomachinery_cabinet_bays.Turbo_Cab_qty1(Product)
	cab_bays_kit1,cab_bays_kit2,cab_bays_kit3,cab_bays_kit4,cab_bays_kit5,cab_bays_kit6,cab_bays_kit7,cab_bays_kit8=GS_C300_SeriesC_cabinet_bays_Cal.cab_bays_kit(Product)
	if IO_Family_Type=="Series C" or IO_Family_Type=="Turbomachinery":
		if cab_bays_kit1>0 or Turbo_Cab_qty3>0:
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51109524-500",cab_bays_kit1+Turbo_Cab_qty3)
		else:
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51109524-500",0)
		if cab_bays_kit2>0 or Turbo_Cab_qty4>0:
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51109524-700",cab_bays_kit2+Turbo_Cab_qty4)
		else:
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51109524-700",0)
		if cab_bays_kit3>0 or Turbo_Cab_qty1>0:
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51109524-200",cab_bays_kit3+Turbo_Cab_qty1)
		else:
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51109524-200",0)
		if cab_bays_kit4>0 or Turbo_Cab_qty2>0:
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51109524-600",cab_bays_kit4+Turbo_Cab_qty2)
		else:
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51109524-600",0)
	#45767 Shivani
	F1=GS_C300_SeriesC_cabinet_bays_Cal.shipping_bays(Product)
	if Product.Name=="Series-C Remote Group":
		Crate_Type=Product.Attr('Crate Type').GetValue()
		Trace.Write(Crate_Type)
		Crate_Design=Product.Attr('Crate Design').GetValue()
		Trace.Write(Crate_Design)
		family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
		Trace.Write(family)
		mounting_sol=Product.Attr('SerC_IO_Mounting_Solution').GetValue()
		if IO_Family_Type=="Series C":
			if F1>0 and mounting_sol=="Mounting Panel"  :
				if Crate_Type=="Domestic/Truck" and Crate_Design=="Standard":
					GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-SP0000",F1)
				else:
					GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-SP0000",0)
				if Crate_Type=="Domestic/Truck" and Crate_Design=="Premium":
					GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-PP0000",F1)
				else:
					GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-PP0000",0)
				if Crate_Type=="Air" and Crate_Design=="Standard":
					GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT4A00",F1)
				else:
					GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT4A00",0)
				if Crate_Type=="Air" and Crate_Design=="Premium":
					GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT4A01",F1)
				else:
					GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT4A01",0)
				if Crate_Type=="Ocean" and Crate_Design=="Standard":
					GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT4000",F1)
				else:
					GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT4000",0)
				if Crate_Type=="Ocean" and Crate_Design=="Premium":
					GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT4001",F1)
				else:
					GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT4001",0)
			elif F1>0 and mounting_sol=="Universal Process Cab - 1.3M"  :
				if Crate_Type=="Domestic/Truck" and Crate_Design=="Standard":
					GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-SP0000",F1)
				else:
					GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-SP0000",0)
				if Crate_Type=="Domestic/Truck" and Crate_Design=="Premium":
					GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-PP0000",F1)
				else:
					GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-PP0000",0)
				if Crate_Type=="Air" and Crate_Design=="Standard":
					GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT4A00",F1)
				else:
					GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT4A00",0)
				if Crate_Type=="Air" and Crate_Design=="Premium":
					GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT4A01",F1)
				else:
					GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT4A01",0)
				if Crate_Type=="Ocean" and Crate_Design=="Standard":
					GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT4000",F1)
				else:
					GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT4000",0)
				if Crate_Type=="Ocean" and Crate_Design=="Premium":
					GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT4001",F1)
				else:
					GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CF-CT4001",0)

	#45771 Shivani
	F1=GS_C300_SeriesC_cabinet_bays_Cal.cab_bays66(Product)
	if F1>0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","4605466",F1)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","4605466",0)

	#CXCPQ-47465
	Qty_47465_bay2,Qty_47465_bay3,Qty_47465_bay4=GS_C300_SeriesC_cabinet_bays_Cal.Cab_Bay234(Product)
	if Qty_47465_bay2>0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-CASS21",Qty_47465_bay2)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-CASS21",0)
	if Qty_47465_bay3>0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-CASS31",Qty_47465_bay3)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-CASS31",0)
	if Qty_47465_bay4>0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-CASS41",Qty_47465_bay4)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-CASS41",0)

	#CXCPQ-34705
	Qty_34705=GS_C300_SeriesC_cabinet_bays_Cal.Cab_Bay_34705(Product)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-C8SSS1",Qty_34705+MU_C8SSS1)
	#CXCPQ-83002,83003
	if IO_Family_Type == 'Series C':
		Qty_83002,Qty_83003=GS_C300_SeriesC_cabinet_bays_Cal.Cab_Bay_83002(Product)
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-CASSS1",0)
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-CADSS1",0)
		if Qty_83002>0:
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-CASSS1",Qty_83002)
		if Qty_83003>0:
			GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-CADSS1",Qty_83003)

	#mark II mcar CXCPQ-44774
	A,B,C,DD,E,F,G,H,I,Sum=GS_C300_MCAR_calcs.mcar_calsmark(Product)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51454909-100",Sum)
	#CXCPQ-45701,45699,47614,45702
	#QTY_A,QTY_B,QTY_C,QTY_D,QTY_E1,QTY_E2,Val_A,Val_B,Val_C=GS_C300_SeriesC_Cabinet_Calcs.C300_calcs_part(Product)
	mounting_sol=Product.Attr('SerC_IO_Mounting_Solution').GetValue()
	#45701
	if QTY_A>0 and mounting_sol=='Mounting Panel':
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51454345-300",QTY_A)
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51154898-300",QTY_A)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51454345-300",0)
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51154898-300",0)
	#45699
	if QTY_B>0 and mounting_sol=='Mounting Panel':
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51454345-200",QTY_B)
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51154898-200",QTY_B)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51454345-200",0)
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51154898-200",0)
	#45698
	if Val_A>0 and mounting_sol=='Mounting Panel':
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51454345-100",Val_A)
		Val_AA=Val_A
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51154898-100",Val_AA)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51454345-100",0)
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51154898-100",0)
	#45706
	if Val_B>0 and mounting_sol=='Mounting Panel':
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51154857-100",Val_B)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51154857-100",0)
	if Val_C>0 and mounting_sol=='Mounting Panel':
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51154857-200",Val_C)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51154857-200",0)
	#47614#CXCPQ-47808
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51403902-100",int(QTY_C)+int(power2)+int(Turbo1)+int(Turbo2))
	#45702
	if QTY_D>0 and mounting_sol=='Mounting Panel':
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51454345-400",QTY_D)
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51154898-400",QTY_D)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51454345-400",0)
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51154898-400",0)
	#34707 and #CXCPQ-51525
	if (QTY_E1>0 and mounting_sol=='Cabinet') or Single_130>0 or Dual_130>0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51197168-100",int(QTY_E1)+int(Single_130)+int(Dual_130)) #51525
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51197168-100",0)
	if (QTY_E2>0 and mounting_sol=='Cabinet') or Single_180>0 or Dual_180>0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51197168-200",int(QTY_E2)+int(Single_180)+int(Dual_180)) #51525
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51197168-200",0)
	#CXCPQ-82919
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","50185186-100",0)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","50185186-200",0)
	if QTY_E3>0 and mounting_sol=='Cabinet':
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","50185186-100",QTY_E3)
	if QTY_E4>0 and mounting_sol=='Cabinet':
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","50185186-200",QTY_E4)
	#47585,51528
	QTY_F,QTY_G1,QTY_G2,QTY_G3,QTY_H1,QTY_H2,QTY_H3,QTY_H4,QTY_H5,QTY_H6,QTY_H7,QTY_H8=GS_C300_SeriesC_Cabinet_Calcs_1.C300_calcs_part2(Product)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-C8DSS1",QTY_F+MU_C8DSS1)

	#35490
	if QTY_G1>0 and mounting_sol=='Cabinet':
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51197150-400",QTY_G1)
	elif RF_4>0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51197150-400",RF_4) #CXCPQ-51520
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51197150-400",0)
	if QTY_G2>0 and mounting_sol=='Cabinet':
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51197150-300",QTY_G2)
	elif RR_3>0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51197150-300",RR_3) #CXCPQ-51520
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51197150-300",0)
	if QTY_G3>0 and mounting_sol=='Cabinet':
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51197150-200",QTY_G3)
	elif RFR_2>0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51197150-200",RFR_2) #CXCPQ-51520
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51197150-200",0)
	#35486 and 51516
	if (QTY_H1>0 and mounting_sol=='Cabinet') or Single_S1>0 or Dual_S1>0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-C8DRS1",int(QTY_H1)+int(Single_S1)+int(Dual_S1))  #51516
	elif QTY_H3>0 and mounting_sol=='Cabinet':
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-C8DRS1",QTY_H3)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-C8DRS1",0)
	if (QTY_H2>0 and mounting_sol=='Cabinet') or Single_D1>0 or Dual_D1>0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-C8DRD1",int(QTY_H2)+int(Single_D1)+int(Dual_D1)) #51516
	elif QTY_H4>0 and mounting_sol=='Cabinet':
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-C8DRD1",QTY_H4)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-C8DRD1",0)
	#82272
	if QTY_H5>0 and mounting_sol=='Cabinet':
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-CADRS1",QTY_H5)
	elif QTY_H7>0 and mounting_sol=='Cabinet':
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-CADRS1",QTY_H7)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-CADRS1",0)
	if QTY_H6>0 and mounting_sol=='Cabinet':
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-CADRD1",QTY_H6) 
	elif QTY_H8>0 and mounting_sol=='Cabinet':
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-CADRD1",QTY_H8)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-CADRD1",0)
	#47519
	QTY_I,QTY_I1,QTY_I2=GS_C300_SeriesC_Cabinet_Calcs_1.C300_calcs_part3(Product)
	if QTY_I>0 and mounting_sol=='Cabinet':
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-CADS41",QTY_I)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-CADS41",0)
	if QTY_I1>0 and mounting_sol=='Cabinet':
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-CADS31",QTY_I1)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-CADS31",0)
	if QTY_I2>0 and mounting_sol=='Cabinet':
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-CADS21",QTY_I2)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-CADS21",0)
	#CXCPQ-34702
	QTY1,QTY2=GS_C300_SeriesC_Cabinet_Calcs_1.C300_calcs_part4(Product)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-C8TRM1",int(QTY1)+int(Thermo_qnt2)+int(QTY2)+int(MU_C8TRM1))
	#CXCPQ-34703
	qty1,qty2=GS_C300_SeriesC_Cabinet_Calcs_1.C300_calcs_part5(Product)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51197150-500",int(qty1)+int(RR_5)+int(RFR_5)+int(Std_5)) #CXCPQ-51519
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51197150-600",int(qty2)+int(RF_6)) #CXCPQ-51519
	#CXCPQ-34708,51530
	qty1,qty3,qty4,qty5,qty6,qty7,qty8,qty9,qty10,qty11,qty12,qty13=GS_C300_SeriesC_Cabinet_Calcs_1.C300_calcs_part6(Product, Quote)
	Cabinet_access=Product.Attr('SerC_RG_Cabinet_Access').GetValue()
	if Cabinet_access=='Single Access':
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51199948-100",qty1+Q_51199948100)
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51199947-175",qty3+Q51199947_175)
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51199947-275",qty4+Q51199947_275)
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51199947-375",qty5+Q51199947_375)
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202397-100",qty6)
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51154692-100",qty7)
	elif Cabinet_access=='Dual Access':
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51199948-100",qty8+Q_51199948100)
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51199947-175",qty9+Q51199947_175)
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51199947-275",qty10+Q51199947_275)
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51199947-375",qty11+Q51199947_375)
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51202397-100",qty12)
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_RG_Part_Summary","51154692-200",qty13)
	# Calculate cabinet parts
	GS_C300_Calc_Module.populateCabinetParts(Product)
	GS_SerC_CG_RG_Amps.generic_type_markII(Product)

	#cabinet bay qty
	B, D, E, F = GS_C300_Calc_Module.getBayQuantities(Product)
	if IO_Family_Type == "Series-C Mark II":
		Product.Messages.Add("Bay Qty B = {}, D = {}, E = {}, F = {}".format(B, D, E, F))
	AA,BB,CC,DD,EE,FF = GS_C300_SeriesC_cabinet_bays_Cal.cab_bays(Product)
	Product.Messages.Add("Bay Qty of A = {}, B = {},C = {}, D = {}, E = {}, F = {}".format(AA, BB, CC, DD, EE, FF))
	AA,BB,CC,DD,EE,FF = GS_C300_Series_C_Turbomachinery_cabinet_bays.Turbo_cab_bays(Product)
	#Product.Messages.Add("Bay Qty of A = {}, B = {},C = {}, D = {}, E = {}, F = {}".format(AA, BB, CC, DD, EE, FF))

	AmP_A=GS_C300_AMP_A_Calcs.AMP_A(Product)
	Trace.Write("AmP_A "+str(AmP_A))
	#Product.Messages.Add("Total Amp A is {}".format(AmP_A))


	#PMIO Parts Calculation
	#CXCPQ-52347
	parts_dict = GS_SerC_Part_Calcs.getParts52347(Product, {})
	#CXCPQ-54439 - Part calculation of user stories CXCPQ-54003, CXCPQ-54609 are included inside this story
	parts_dict = GS_SerC_Part_Calcs.getParts54439(Product, parts_dict)
	if len(parts_dict) > 0:
		GS_C300_IO_Calc.setIOCount(Product, 'Series_C_RG_Part_Summary', parts_dict)

	Product.ApplyRules()
	Product.ExecuteRulesOnce = False