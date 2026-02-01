if Product.Attr('PERF_ExecuteScripts').GetValue()=='SCRIPT_RUN':
	import System.Decimal as D
	import GS_PS_Exp_Ent_BOM as GP_EEB
	import GS_C300_BOM_Rail_IO_Part_calcs,GS_C300_RG_UPC_Calc2
	import GS_C300_Cal_Parts,GS_C300_Cal_Parts1,GS_C300_Cal_Parts2,GS_C300_Cal_Parts3,GS_C300_Cal_Parts4,GS_C300_Cal_Parts5,GS_C300_Cal_Parts6
	import GS_Get_Set_AtvQty, GS_C300_BOM_UIO, GS_C300_BOM_MARK, GS_C300_BOM_Enhance1, GS_C300_BOM_Enhance2, GS_C300_BOM_Enhance3
	import GS_C300_MCAR_calcs, GS_SerC_parts,GS_C300_RG_UPC_Calc,GS_C300_RG_UPC_Calc3,GS_C300_RG_UPC_parts_2
	import GS_C300_Calc_Module,GS_C300_RG_UPC_parts,GS_Part_C300_CNM_Calc,GS_C300_RG_Label,GS_C300_UMC_Parts
	Product.ExecuteRulesOnce = True
	Product.Attr("RG_HN").AssignValue('0')
	Product.Attr("RG_HN2").AssignValue('0')
	Product.Attr("qty_hpsc").AssignValue('0')
	#CXCPQ-40211
	IOComp_SUMDION = GS_C300_BOM_Rail_IO_Part_calcs.IOComponents(Product)
	MDUR18,MDUN12,TUIO11,TUIO01,Amp_A1 = IOComp_SUMDION.C300_Rail()
	GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-MDUR18",MDUR18)
	GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-MDUN12",MDUN12)
	GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-TUIO11",TUIO11)
	GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-TUIO01",TUIO01)
	mib=Product.Attr('MIB Configuration Required?').GetValue()
	io_family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
	io_mounting=Product.Attr('SerC_IO_Mounting_Solution').GetValue()
	Num_Cabinet = Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
	id_modifier=Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
	Specify_id=Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
	FTA=Product.Attr('C300_RG_UPC_FTA').GetValue()
	CN_Hive=Product.Attr('C300_RG_UPC_CN100_IO_HIVE').GetValue()
	CNM=Product.Attr('C300_RG_UPC_CNM').GetValue()
	CNM_Module=Product.Attr('C300_RG_UPC_CNM_Exp_Module').GetValue()
	Uplink_sfp=Product.Attr('C300_RG_UPC_CNM_Uplink_SFP_Type').GetValue()
	Fiber_Optic_Extender=Product.Attr('C300_RG_UPC_Fiber_Optic_Extender').GetValue()
	val=0
	GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","ICF1150I-MSTT-HPSC",0)
	GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","51454240-302",0)
	GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-TION13",0)
	GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-PEIM01",0)
	#GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-MCC003",0)
	#GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-INWE01",0)
	GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","50159943-003",0)
	GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","50182312-001",0)
	GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","FS-CCI-HSE-02",0)
	GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-324",0)
	GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","51202699-200",0)
	GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","51202684-200",0)
	GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","50185149-001",0)
	GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","50154548-004",0)
	GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-303",0)
	GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","51202676-100",0)
	GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","51509194-500",0)

	if io_family=='Series C':
		if io_mounting=='Universal Process Cab - 1.3M':
			#CXCPQ-45842, #CXCPQ-45051, #CXCPQ-45306, #CXCPQ-46094,#CXCPQ-45353, #46093 by Shivani
			qty_51454240302=GS_C300_RG_UPC_Calc.getC300UpsCals(Product)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","51454240-302",qty_51454240302)
			Qty_50159943_003=GS_C300_RG_UPC_Calc.getC30UpsCals_50159943_003(Product)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","50159943-003",Qty_50159943_003)
			Qty_50182312_001=GS_C300_RG_UPC_Calc.get50182312_001(Product)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","50182312-001",Qty_50182312_001)
			Qty_Hse=GS_C300_RG_UPC_Calc.getCCI_HSC(Product)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","FS-CCI-HSE-02",Qty_Hse)
			Qty_324=GS_C300_RG_UPC_Calc2.get51156387_324(Product)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-324",Qty_324)
			var12=GS_C300_RG_UPC_parts.getpart_CC_TEIM01(Product)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-TEIM01",var12)
			#CXCPQ-46123,#CXCPQ-45890 by Ravika Pupneja
			CCTION13_qty=GS_C300_RG_UPC_Calc.getC300UpsCals_CCTION13(Product)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-TION13",CCTION13_qty)
			CCPEIM01_qty=GS_C300_RG_UPC_Calc.getC300UpsCals_CCPEIM01(Product)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-PEIM01",CCPEIM01_qty)
			#CXCPQ-45886 by Ravika Pupneja
			#CXCPQ-45498,45497 by Ravika Pupneja
			qty_51202684_200=GS_C300_RG_UPC_Calc2.getC300UpsCals_51202684_51202699(Product)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","51202684-200",qty_51202684_200)
			qty_51202699_200=GS_C300_RG_UPC_Calc2.getC300UpsCals_51202684_51202699(Product)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","51202699-200",qty_51202699_200)
			qty_51202676_100=GS_C300_RG_UPC_Calc3.getC300UpsCals_51202676_100(Product)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","51202676-100",qty_51202676_100)
			qty_51509194_500=GS_C300_RG_UPC_Calc3.getC300UpsCals_51509194_500(Product)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","51509194-500",qty_51509194_500)
			qty_51156387_303=GS_C300_RG_UPC_Calc3.getC300UpsCals_51156387_303(Product)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-303",qty_51156387_303)
			qty_50154548_004=GS_C300_RG_UPC_Calc3.getC300UpsCals_50154548_004(Product)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","50154548-004",qty_50154548_004)
			qty_50185149_001=GS_C300_RG_UPC_Calc3.getC300UpsCals_50185149_001(Product)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","50185149-001",qty_50185149_001)
			#CXCPQ-46099, #CXCPQ-45328,#CXCPQ-43815 by Deepika
			var=GS_C300_RG_UPC_Calc.getpartposition(Product)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","ICF1150I-MSTT-HPSC",var)
			var1=GS_C300_RG_UPC_Calc.getpart_51156387_317(Product)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-317",var1)
			var3,var4=GS_C300_RG_UPC_Calc.getpart_4600135(Product)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","4600135",var3)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","4600120",var4)
			#var10=GS_C300_RG_UPC_parts.getpart_CC_UGIA01(Product) Commented because CXCPQ-99652 defect
			#GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-UGIA01",var10)
			#1K. #CXCPQ-46120,#2K. #CXCPQ-45380,#3K. #CXCPQ-46096,#4K. #CXCPQ-43821,#5K. #CXCPQ-46097
			val_1=GS_C300_RG_UPC_Calc.getC300UPC_46120(Product)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","50143176-100",val_1)
			val_2=GS_C300_RG_UPC_Calc.getC300UPC_45380(Product)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","51156389-300",val_2)
			val_3=GS_C300_RG_UPC_Calc.getC300UPC_46096(Product)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","TC-SWHS01",val_3)
			val_4=GS_C300_RG_UPC_Calc.getC300UPC_43821(Product)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","50154548-010",val_4)
			val_5=GS_C300_RG_UPC_Calc.getC300UPC_46097(Product)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","TC-SWHS02",val_5)
			#7K. #CXCPQ-45315,#8K. #CXCPQ-45013,#9K. #CXCPQ-45335,#10K. #CXCPQ-45309
			val_7=GS_C300_RG_UPC_Calc.getC300UPC_45315(Product)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-305",val_7)
			val_8=GS_C300_RG_UPC_Calc.getC300UPC_45013(Product)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","50154761-001",val_8)
			val_9=GS_C300_RG_UPC_Calc.getC300UPC_45335(Product)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-319",val_9)
			val_10=GS_C300_RG_UPC_Calc.getC300UPC_45309(Product)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-300",val_10)
			#11K. #CXCPQ-45499,#12K. #CXCPQ-45897,#13K. #CXCPQ-45319,#14K. #CXCPQ-45324,#15K. #CXCPQ-45376
			val_12=GS_C300_RG_UPC_Calc2.getC300UPC_45897(Product)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-SICC-1011/X15",val_12)
			val_13=GS_C300_RG_UPC_Calc2.getC300UPC_45319(Product)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-308",val_13)
			val_14=GS_C300_RG_UPC_Calc2.getC300UPC_45324(Product)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-314",val_14)
			val_15=GS_C300_RG_UPC_Calc2.getC300UPC_45376(Product)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-331",val_15)
			#CXCPQ-45316,#CXCPQ-45336,#CXCPQ-45310,#CXCPQ-45050,#CXCPQ-45371,#CXCPQ-45322, #CXCPQ-45332
			var2=GS_C300_RG_UPC_Calc.getpart_51156387_307(Product)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-307",var2)
			var5=GS_C300_RG_UPC_Calc.getpart_51156387_321(Product)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-321",var5)
			var6=GS_C300_RG_UPC_parts_2.getpart_51156387_302(Product)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-302",var6)
			var7=GS_C300_RG_UPC_parts.getpart_50159943_002(Product)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","50159943-002",var7)
			var8=GS_C300_RG_UPC_parts.getpart_51156387_329(Product)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-329",var8)
			var9=GS_C300_RG_UPC_parts.getpart_51156387_310(Product)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-310",var9)
			var10=GS_C300_RG_UPC_parts.getpart_51156387_318(Product)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-318",var10)
			#0K. #CXCPQ-43663
			val=int(Num_Cabinet) * 1
			Qty_50159943_004 = GS_C300_RG_UPC_Calc3.getC300UpsCals_50159943_004(Product)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","50152846-200",val)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","50154751-002",val)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","50154751-003",val)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","FC-MCAR-03",val)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","51121576-104",val)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","51121576-200",val)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","51454240-202",val)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","51156760-100",val)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","51156388-200",val)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","50159943-004",val)
		else:
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","50152846-200",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","50154751-002",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","50154751-003",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","FC-MCAR-03",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","51121576-104",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","51121576-200",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","51454240-202",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","51156760-100",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","51156388-200",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","50159943-004",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-317",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","ICF1150I-MSTT-HPSC",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","4600135",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","4600120",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-307",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-321",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-302",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","50159943-002",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-329",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-310",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-318",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-TEIM01",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-UGIA01",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","50143176-100",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","51156389-300",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","TC-SWHS01",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","50154548-010",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","TC-SWHS02",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-305",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","50154761-001",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-319",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-300",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-SICC-1011/X15",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-308",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-314",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-331",0)
	else:
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-321",0)
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-307",0)
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","50159943-002",0)
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-329",0)
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-310",0)
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","51156387-318",0)
		##GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-TUIO31",0)
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-UGIA01",0)
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-TEIM01",0)

	## Sprint-22 :- N
	#CXCPQ-44166
	MARK = GS_C300_BOM_MARK.IOComponents(Product)
	DC_PUIO31,DC_TUIO41,DC_TUIO31 = MARK.C300_Rail()
	if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series-C Mark II":
		if DC_PUIO31 > 0:
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-PUIO31",DC_PUIO31)
		else:
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-PUIO31",0)
		if DC_TUIO41 > 0:
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","DC-TUIO41",DC_TUIO41)
		else:
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","DC-TUIO41",0)
		if DC_TUIO31 > 0:
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","DC-TUIO31",DC_TUIO31)
		else:
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","DC-TUIO31",0)
	#CXCPQ-44457
	if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series-C Mark II":
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-PAOH01",0)
	MARK1 = GS_C300_BOM_Enhance1.IOComponents(Product)
	CC_PAOH01,DC_TAOX11,DC_TAOX01 = MARK1.C300_Mark()
	if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series-C Mark II":
		if CC_PAOH01 > 0:
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-PAOH01",CC_PAOH01)
		if DC_TAOX11 > 0:
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","DC-TAOX11",DC_TAOX11)
		else:
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","DC-TAOX11",0)
		if DC_TAOX01 > 0:
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","DC-TAOX01",DC_TAOX01)
		else:
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","DC-TAOX01",0)
	#CXCPQ-44473
	MARK2 = GS_C300_BOM_Enhance2.IOComponents(Product)
	CC_PDIL01,DC_TDIL11,DC_TDIL01 = MARK2.C300_Mark2()
	if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series-C Mark II":
		if CC_PDIL01 > 0:
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-PDIL01",CC_PDIL01)
		else:
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-PDIL01",0)
		if DC_TDIL11 > 0:
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","DC-TDIL11",DC_TDIL11)
		else:
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","DC-TDIL11",0)
		if DC_TDIL01 > 0:
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","DC-TDIL01",DC_TDIL01)
		else:
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","DC-TDIL01",0)
	#CXCPQ-44340
	if io_family in ("Series-C Mark II","Series C"):
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-PAIH02",0)
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-PAIX02",0)
	MARK3 = GS_C300_BOM_Enhance3.IOComponents(Product)
	CC_PAIH02,CC_PAIX02,DC_TAID01,DC_TAID11 = MARK3.C300_Mark3()
	if io_family in ("Series-C Mark II","Series C"):
		if CC_PAIH02 > 0:
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-PAIH02",CC_PAIH02)
		if CC_PAIX02 > 0:
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-PAIX02",CC_PAIX02)
	if io_family == "Series-C Mark II":
		if DC_TAID01 > 0:
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","DC-TAID01",DC_TAID01)
		else:
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","DC-TAID01",0)
		if DC_TAID11 > 0:
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","DC-TAID11",DC_TAID11)
		else:
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","DC-TAID11",0)
	## UMC parts
	'''if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series C" and Product.Attr('Ser_RG_Universal_Marshalling_Cabinet').GetValue()=="Yes":
		#CXCPQ-46424
		qty_UPTA01 = GS_C300_UMC_Parts.get_UPTA01(Product)
		if qty_UPTA01>0:
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-UPTA01",qty_UPTA01)
		#CXCPQ-46430,CXCPQ-46433
		qty_UAIA01, qty_UAOA01 = GS_C300_UMC_Parts.get_UAIA01(Product)
		if qty_UAIA01>0:
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-UAIA01",qty_UAIA01)
		if qty_UAOA01>0:
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-UAOA01",qty_UAOA01)
		#CXCPQ-46091,CXCPQ-43585
		qty_UDOR01, qty_UDIR01 = GS_C300_UMC_Parts.get_RLY(Product)
		if qty_UDOR01>0:
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-UDOR01",qty_UDOR01)
		if qty_UDIR01>0:
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-UDIR01",qty_UDIR01)'''
	#39961,39298,39294,39843#44037#44050
	OK4 = GS_C300_Cal_Parts6.IOComponents(Product)
	PAIN01,PAIH51,TAIX61,TAIX51 = OK4.C300_Mark2()
	OK2 = GS_C300_Cal_Parts4.IOComponents(Product)
	PAON01,PAOH51,TAOX61,TAOX51 = OK2.C300_Mark2()
	CC_PAIN01,CC_TAIN11,CC_TAIN01,CC_PAIH51,CC_TAIX61,CC_TAIX51,CC_PAON01,CC_TAON11,CC_TAON01,CC_PAOH51,CC_TAOX61,CC_TAOX51=GS_C300_Cal_Parts.part_qty_IO(Product)
	if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series-C Mark II" and  PAIN01 > 0:
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-PAIN01",PAIN01)
	elif Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series C" and CC_PAIN01 > 0:
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-PAIN01",CC_PAIN01)
	else:
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-PAIN01",0)
	if  Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series-C Mark II" and PAIH51 > 0:
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-PAIH51",PAIH51)
	elif Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series C" and CC_PAIH51 > 0:
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-PAIH51",CC_PAIH51)
	else:
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-PAIH51",0)
	if  Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series-C Mark II" and TAIX61 > 0:
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","DC-TAIX61",TAIX61)
	else:
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","DC-TAIX61",0)
	if  Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series-C Mark II" and TAIX51 > 0:
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","DC-TAIX51",TAIX51)
	else:
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","DC-TAIX51",0)
	#if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series C":
	if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series C" and CC_TAIN11 > 0:
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-TAIN11",CC_TAIN11)
	else:
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-TAIN11",0)
	if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series C" and CC_TAIN01 > 0:
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-TAIN01",CC_TAIN01)
	else:
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-TAIN01",0)
	if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series C" and CC_TAIX61 > 0:
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-TAIX61",CC_TAIX61)
	else:
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-TAIX61",0)
	if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series C" and CC_TAIX51 > 0:
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-TAIX51",CC_TAIX51)
	else:
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-TAIX51",0)
	if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series C" and CC_PAON01 > 0:
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-PAON01",CC_PAON01)
	elif Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series-C Mark II" and PAON01 > 0:
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-PAON01",PAON01)
	else:
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-PAON01",0)
	if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series C" and CC_TAON11 > 0:
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-TAON11",CC_TAON11)
	else:
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-TAON11",0)
	if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series C" and CC_TAON01 > 0:
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-TAON01",CC_TAON01)
	else:
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-TAON01",0)
	if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series C" and CC_PAOH51 > 0:
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-PAOH51",CC_PAOH51)
	elif Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series-C Mark II" and PAOH51 > 0:
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-PAOH51",PAOH51)
	else:
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-PAOH51",0)
	if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series C" and CC_TAOX61 > 0:
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-TAOX61",CC_TAOX61)
	else:
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-TAOX61",0)
	if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series C" and CC_TAOX51 > 0:
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-TAOX51",CC_TAOX51)
	else:
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-TAOX51",0)
	if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series-C Mark II" and TAOX61 > 0:
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","DC-TAOX61",TAOX61)
	else:
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","DC-TAOX61",0)
	if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series-C Mark II" and TAOX51 > 0:
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","DC-TAOX51",TAOX51)
	else:
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","DC-TAOX51",0)
	#44150
	#if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series-C Mark II":
	OK1 = GS_C300_Cal_Parts3.IOComponents(Product)
	PDOD51,TDOD61,TDOD51 = OK1.C300_Mark2()
	if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series-C Mark II" and PDOD51 > 0:
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","DC-PDOD51",PDOD51)
	else:
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","DC-PDOD51",0)
	if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series-C Mark II" and TDOD61 > 0:
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","DC-TDOD61",TDOD61)
	else:
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","DC-TDOD61",0)
	if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series-C Mark II" and TDOD51 > 0:
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","DC-TDOD51",TDOD51)
	else:
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","DC-TDOD51",0)
	#44049
	if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series-C Mark II" and Product.Attr('Dummy_RG_IO_Mounting_Solution').GetValue()!="Universal Process Cab - 1.3M":
		OK3 = GS_C300_Cal_Parts5.IOComponents(Product)
		CC_PAIL51,DC_TAIL51 = OK3.C300_Mark2()
		if CC_PAIL51 > 0:
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-PAIL51",CC_PAIL51)
		else:
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-PAIL51",0)
		if DC_TAIL51 > 0:
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","DC-TAIL51",DC_TAIL51)
		else:
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","DC-TAIL51",0)
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-TAIL51",0)
	#39951
	if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series C":
		OK5 = GS_C300_Cal_Parts1.IOComponents(Product)
		CC_PAIL511,CC_TAIL511 = OK5.C300_Mark2()
		var16=GS_C300_RG_UPC_parts.get_CC_TAIL51(Product)
		if CC_PAIL511 > 0:
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-PAIL51",CC_PAIL511)
		'''else:
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-PAIL51",0)'''
		#CXCPQ-45898
		if CC_TAIL511 > 0 or (var16>0 and io_mounting=='Universal Process Cab - 1.3M') :
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-TAIL51",int(CC_TAIL511)+int(var16))
		else:
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-TAIL51",0)
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","DC-TAIL51",0)

	#CXCPQ-40869
	'''if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series C":
		#MCTAMR04,MCTAMT04,MCTAMT14,MUKLAM03,MUTMCN01=GS_C300_Cal_Parts.getpartsseriesc(Product)
		MCTAMR04,MCTAMT04,MCTAMT14,MUKLAM03=GS_C300_Cal_Parts.getpartsseriesc(Product)
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-TAMR04",MCTAMR04)
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-TAMT04",MCTAMT04)
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-TAMT14",MCTAMT14)
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-KLAM03",MUKLAM03)
		#GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-TMCN01",MUTMCN01)'''
	'''Moved to PS_SerC_C300_RG_Parts_2
	#CXCPQ-41510
	L21= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','L21')
	L61= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','L61')
	J31= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','J31')
	K31= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','K31')
	J41= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','J41')
	K41= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','K41')
	J51= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','K51')
	K51= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','K51')
	J71= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','J71')
	K71= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','K71')
	J81= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','J81')
	K81= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','K81')
	J91= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','J91')
	K91= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','K91')
	O11= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','O11')
	M21= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','M21')
	N21= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','N21')
	M31= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','M31')
	N31= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','N31')
	O41= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','O41')
	O71= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','O71')
	O81= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','O81')
	R21= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','R21')
	M51= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','M51')
	N51= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','N51')
	M61= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','M61')
	N61= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','N61')
	M91= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','M91')
	N91= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','N91')
	P11= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','P11')
	Q11= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','Q11')
	P31= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','P31')
	Q31= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','Q31')
	family_type_NEW = Product.Attr('SerC_CG_IO_Family_Type').GetValue()
	Universal1=Product.Attr('Ser_RG_Universal_Marshalling_Cabinet').GetValue()
	if family_type_NEW == "Series C" and Universal1== 'No':
		MTL4510 = D.Ceiling((O41+O81)/4)
		GP_EEB.setAtvQty(Product,"Series_C_RG_Third_Party_Part_Summary","MTL4510",MTL4510)
		MTL4511 = (O71+R21)
		GP_EEB.setAtvQty(Product,"Series_C_RG_Third_Party_Part_Summary","MTL4511",MTL4511)
		MTL4516 = D.Ceiling((M51+N51+M91+N91)/2)
		GP_EEB.setAtvQty(Product,"Series_C_RG_Third_Party_Part_Summary","MTL4516",MTL4516)
		MTL4517 = D.Ceiling((M61+N61+P11+Q11)/2)
		GP_EEB.setAtvQty(Product,"Series_C_RG_Third_Party_Part_Summary","MTL4517",MTL4517)
		MTL4521 = (P31+Q31)
		GP_EEB.setAtvQty(Product,"Series_C_RG_Third_Party_Part_Summary","MTL4521",MTL4521)
		MTL4541 = (J31+K31+J71+K71)
		GP_EEB.setAtvQty(Product,"Series_C_RG_Third_Party_Part_Summary","MTL4541",MTL4541)
		MTL4544 = D.Ceiling((L21+J41+K41+L61+J81+K81)/2)
		GP_EEB.setAtvQty(Product,"Series_C_RG_Third_Party_Part_Summary","MTL4544",MTL4544)
		MTL4546C = (M21+N21)
		GP_EEB.setAtvQty(Product,"Series_C_RG_Third_Party_Part_Summary","MTL4546C",MTL4546C)
		MTL4549C = D.Ceiling((O11+M31+N31)/2)
		GP_EEB.setAtvQty(Product,"Series_C_RG_Third_Party_Part_Summary","MTL4549C",MTL4549C)
		MTL4575 = (J51+K51+J91+K91)
		GP_EEB.setAtvQty(Product,"Series_C_RG_Third_Party_Part_Summary","MTL4575",MTL4575)
	else:
		GP_EEB.setAtvQty(Product,"Series_C_RG_Third_Party_Part_Summary","MTL4510",0)
		GP_EEB.setAtvQty(Product,"Series_C_RG_Third_Party_Part_Summary","MTL4511",0)
		GP_EEB.setAtvQty(Product,"Series_C_RG_Third_Party_Part_Summary","MTL4516",0)
		GP_EEB.setAtvQty(Product,"Series_C_RG_Third_Party_Part_Summary","MTL4517",0)
		GP_EEB.setAtvQty(Product,"Series_C_RG_Third_Party_Part_Summary","MTL4521",0)
		GP_EEB.setAtvQty(Product,"Series_C_RG_Third_Party_Part_Summary","MTL4541",0)
		GP_EEB.setAtvQty(Product,"Series_C_RG_Third_Party_Part_Summary","MTL4544",0)
		GP_EEB.setAtvQty(Product,"Series_C_RG_Third_Party_Part_Summary","MTL4546C",0)
		GP_EEB.setAtvQty(Product,"Series_C_RG_Third_Party_Part_Summary","MTL4549C",0)
		GP_EEB.setAtvQty(Product,"Series_C_RG_Third_Party_Part_Summary","MTL4575",0)
	#CXCPQ-41344
	W73= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','W73')
	V13= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','V13')
	V53= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','V53')
	V43= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','V43')
	V83= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','V83')
	IO_Family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
	Universal=Product.Attr('Ser_RG_Universal_Marshalling_Cabinet').GetValue()
	if IO_Family=='Series C' and Universal=='No':
		CC_GAOX21 = W73
		CC_GDIL21 = V13 + V53
		CC_GDIL01 = 2* (V43 + V83)
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-GAOX21",CC_GAOX21)
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-GDIL21",CC_GDIL21)
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-GDIL01",CC_GDIL01)
	else:
		CC_GAOX21 =CC_GDIL21 = CC_GDIL01 = 0
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-GAOX21",CC_GAOX21)
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-GDIL21",CC_GDIL21)
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-GDIL01",CC_GDIL01)
	#CXCPQ-41347
	V21= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','V21')
	V31= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','V31')
	V22= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','V22')
	V32= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','V32')
	V61= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','V61')
	V71= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','V71')
	V62= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','V62')
	V72= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','V72')
	W81= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','W81')
	W91= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','W91')
	W82= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','W82')
	W92= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','W92')
	if IO_Family=='Series C' and Universal=='No':
		CC_GDIL11 = (V21+V31+ V22+V32+V61+V71+V62+V72)
		CC_GAOX11 = (W81+W91+W82+W92)
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-GDIL11",CC_GDIL11)
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-GAOX11",CC_GAOX11)
	else:
		CC_GDIL11=CC_GAOX11 = 0
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-GDIL11",CC_GDIL11)
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-GAOX11",CC_GAOX11)
	#CXCPQ-41491
	V43= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','V43')
	V83= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','V83')
	V91= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','V91')
	V92= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','V92')
	if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series C" and Product.Attr('Ser_RG_Universal_Marshalling_Cabinet').GetValue() == "No":
		CC_SDXX01 = (2*V43) + (2*V83) + (2*V91) + V92
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-SDXX01",CC_SDXX01)
	else:
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-SDXX01",0)'''
	#CXCPQ-41226
	Y21= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','Y21')
	Y22= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','Y22')
	Y31= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','Y31')
	Y32= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','Y32')
	Y23= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','Y23')
	Y33= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','Y33')
	W11= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','W11')
	W21= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','W21')
	W31= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','W31')
	W12= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','W12')
	W22= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','W22')
	W32= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','W32')
	W41= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','W41')
	W51= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','W51')
	W61= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','W61')
	W42= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','W42')
	W52= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','W52')
	W62= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','W62')
	W23= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','W23')
	Z91= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','Z91')
	if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series C":
		CC_TAID11 = Y21 + Y22+ Y31 + Y32
		CC_TAID01 = Y23+ Y33
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-TAID11",CC_TAID11)
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-TAID01",CC_TAID01)
	else:
		CC_TAID11 = CC_TAID01 = 0
	if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series C" and Product.Attr('Ser_RG_Universal_Marshalling_Cabinet').GetValue() == "No":
		CC_GAIX11 = (W11+W21+W31) + (W12+W22+W32) + (W41+W51+W61) + (W42+W52+W62)
		CC_GAIX21 = Z91 + W23
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-GAIX11",CC_GAIX11)
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-GAIX21",CC_GAIX21)

	Product.Attr("C300_RG_Total_IO_Load").AssignValue(str(GS_C300_Calc_Module.getTotalLoadIO(Product)))
	Product.Attr("C300_RG_Total_IO_Point_Load").AssignValue(str(GS_C300_Calc_Module.getTotalIoPointLoad(Product)))
	Product.Messages.Add("Total Load IO = {}".format(GS_C300_Calc_Module.getTotalLoadIO(Product)))
	Product.Messages.Add("Total IO point Load = {}.".format(GS_C300_Calc_Module.getTotalIoPointLoad(Product)))
	#CXCPQ-39151
	GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","8939-HN",0)
	GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","8937-HN2",0)
	qty_8939_HN, qty_8937_HN2, qty_A2, qty_A3 = GS_SerC_parts.Get_RG_IOTA(Product)
	if qty_8939_HN > 0:
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","8939-HN",qty_8939_HN)
		Product.Attr("RG_HN").AssignValue(str(qty_A3))
	if qty_8937_HN2 > 0:
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","8937-HN2",qty_8937_HN2)
		Product.Attr("RG_HN2").AssignValue(str(qty_A2))
	#CXCPQ-39268 #CXCPQ-39288
	GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-SDRX01",0)
	GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","DC-SDRX01",0)
	#GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","ICF1150I-SSCT-HPSC",0)
	GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","51155436-100",0)
	GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","51156323-100",0)
	qty_SDRX, qty_HPSC, qty_100 = GS_SerC_parts.RG_iota(Product)
	if qty_SDRX > 0 and io_family != "Series-C Mark II":
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-SDRX01",qty_SDRX)
	elif qty_SDRX > 0:
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","DC-SDRX01",qty_SDRX)
	if qty_HPSC > 0:
		if Product.Attr('Dummy_RG_IO_Mounting_Solution').GetValue()!="Universal Process Cab - 1.3M":
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","ICF1150I-SSCT-HPSC",qty_HPSC)
			Product.Attr("qty_hpsc").AssignValue(str(qty_HPSC))
	if qty_100 > 0 and io_family != "Series-C Mark II":
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","51155436-100",qty_100)
	elif qty_100 > 0:
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","51156323-100",qty_100)

	FOE_Module_qty_Case_1_2 = 0
	FOE_Module_qty_Case_3 = 0
	if io_family=='Series C' and io_mounting=='Universal Process Cab - 1.3M' and int(Num_Cabinet)>0 and CN_Hive in ('None', None, '') and Fiber_Optic_Extender == 'Single Mode x2':
		FOE_Module_qty_Case_1_2= GS_Get_Set_AtvQty.getAtvQty(Product,"Series_C_RG_Part_Summary","ICF1150I-SSCT-HPSC")
	elif io_family=='Series C' and io_mounting=='Universal Process Cab - 1.3M' and int(Num_Cabinet)>0 and CN_Hive in ('None', None, '') and Fiber_Optic_Extender == 'Single Mode x4':
		FOE_Module_qty_Case_1_2 = 2
	elif io_family=='Series C' and io_mounting=='Universal Process Cab - 1.3M' and int(Num_Cabinet)>0 and CN_Hive in ('None', None, '') and Fiber_Optic_Extender == 'Multi Mode x2':
		FOE_Module_qty_Case_3= GS_Get_Set_AtvQty.getAtvQty(Product,"Series_C_RG_Part_Summary","ICF1150I-MSTT-HPSC")
	Product.Attr('Control_Group_FOE_Module_qty').AssignValue(str(FOE_Module_qty_Case_1_2))
	Product.Attr('Control_Group_FOE_Module_qty_case3').AssignValue(str(FOE_Module_qty_Case_3))
	Product.ApplyRules()
	Product.ExecuteRulesOnce = False