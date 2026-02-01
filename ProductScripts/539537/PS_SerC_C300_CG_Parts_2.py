if Product.Attr('PERF_ExecuteScripts').GetValue()=='SCRIPT_RUN' or Product.Tabs.GetByName('Part Summary').IsSelected:
	import System.Decimal as D
	import GS_PS_Exp_Ent_BOM as GS_EEB
	import GS_Get_Set_AtvQty
	import C300_PIMO_PARTS_CALCS,GS_C300_Cal_Parts
	from GS_C300_PMIO_Cal import partCalc
	from math import ceil
	import GS_C300_IO_Calc, GS_C300_Calc_Module, GS_SerC_parts
	import GS_C300_BOM_Enhance3
	Product.ExecuteRulesOnce = True

	Product.Attr("PCNT02_Val").AssignValue('0')
	Product.Attr("PCNT05_Val").AssignValue('0')
	Product.Attr("TION_Val").AssignValue('0')

	TION = GS_Get_Set_AtvQty.getAtvQty(Product, 'Series_C_CG_Part_Summary', 'CC-TION11')
	Product.Attr("TION_Val").AssignValue(str(TION))
	#CXCPQ-41344
	W73= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','W73')
	V13= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','V13')
	V53= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','V53')
	V43= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','V43')
	V83= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','V83')
	IO_Family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
	Universal=Product.Attr('SerC_CG_Universal_Marshalling_Cabinet').GetValue()

	if IO_Family=="Series C" and Universal =='No':
		CC_GAOX21 = W73
		CC_GDIL21 = V13 + V53
		CC_GDIL01 = V43 + V83
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-GAOX21",CC_GAOX21)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-GDIL21",CC_GDIL21)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-GDIL01",CC_GDIL01)
	#CXCPQ-50471
	elif IO_Family=="Turbomachinery":
		CC_GAOX21 = W73
		CC_GDIL21 = V13 + V53
		CC_GDIL01 = V43 + V83
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-GAOX21",CC_GAOX21)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-GDIL21",CC_GDIL21)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-GDIL01",CC_GDIL01)
	else:
		CC_GAOX21 =CC_GDIL21 =CC_GDIL01 = 0
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-GAOX21",CC_GAOX21)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-GDIL21",CC_GDIL21)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-GDIL01",CC_GDIL01)

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
	if IO_Family=="Series C" and Universal =='No':
		CC_GDIL11 = (V21+V31+ V22+V32+V61+V71+V62+V72)
		CC_GAOX11 = (W81+W91+W82+W92)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-GDIL11",CC_GDIL11)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-GAOX11",CC_GAOX11)
	#CXCPQ-50472
	elif IO_Family=="Turbomachinery":
		CC_GDIL11 = (V21+V31+ V22+V32+V61+V71+V62+V72)
		CC_GAOX11 = (W81+W91+W82+W92)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-GDIL11",CC_GDIL11)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-GAOX11",CC_GAOX11)
	else:
		CC_GDIL11 =CC_GAOX11 = 0
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-GDIL11",CC_GDIL11)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-GAOX11",CC_GAOX11)

	family_type = Product.Attributes.GetByName("SerC_CG_IO_Family_Type").GetValue()

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
	#Trace.Write("family_type"+str (family_type))
	Universal1=Product.Attr('SerC_CG_Universal_Marshalling_Cabinet').GetValue()
	Trace.Write("Universal1"+str (Universal1))
	IO_Mounting_Solution = Product.Attr('Dummy_CG_IO_Mounting_Solution').GetValue()
	if family_type == 'Series C' and Universal1== 'No' and IO_Mounting_Solution == "Cabinet":
		MTL4510 = D.Ceiling((O41+O81)/4)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","MTL4510",MTL4510)
		MTL4511 = (O71+R21)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","MTL4511",MTL4511)
		MTL4516 = D.Ceiling((M51+N51+M91+N91)/2)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","MTL4516",MTL4516)
		MTL4517 = D.Ceiling((M61+N61+P11+Q11)/2)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","MTL4517",MTL4517)
		MTL4521 = (P31+Q31)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","MTL4521",MTL4521)
		MTL4541 = (J31+K31+J71+K71)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","MTL4541",MTL4541)
		MTL4544 = D.Ceiling((L21+J41+K41+L61+J81+K81)/2)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","MTL4544",MTL4544)
		MTL4546C = (M21+N21)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","MTL4546C",MTL4546C)
		MTL4549C = D.Ceiling((O11+M31+N31)/2)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","MTL4549C",MTL4549C)
		MTL4575 = (J51+K51+J91+K91)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","MTL4575",MTL4575)
	#CXCPQ-50473
	elif family_type == 'Turbomachinery':
		MTL4510 = D.Ceiling((O41+O81)/4)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","MTL4510",MTL4510)
		MTL4511 = (O71+R21)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","MTL4511",MTL4511)
		MTL4516 = D.Ceiling((M51+N51+M91+N91)/2)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","MTL4516",MTL4516)
		MTL4517 = D.Ceiling((M61+N61+P11+Q11)/2)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","MTL4517",MTL4517)
		MTL4521 = (P31+Q31)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","MTL4521",MTL4521)
		MTL4541 = (J31+K31+J71+K71)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","MTL4541",MTL4541)
		MTL4544 = D.Ceiling((L21+J41+K41+L61+J81+K81)/2)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","MTL4544",MTL4544)
		MTL4546C = (M21+N21)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","MTL4546C",MTL4546C)
		MTL4549C = D.Ceiling((O11+M31+N31)/2)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","MTL4549C",MTL4549C)
		MTL4575 = (J51+K51+J91+K91)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","MTL4575",MTL4575)
	else:
		GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","MTL4510",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","MTL4511",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","MTL4516",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","MTL4517",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","MTL4521",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","MTL4541",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","MTL4544",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","MTL4546C",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","MTL4549C",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Third_Party_Part_Summary","MTL4575",0)

	if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series C":
		MC_PHAO01,MC_PAIH03,BC_THAI11,MC_PSTX03,MC_PD0Y22,BU_TDOC02,MC_PDIY22,MC_TAOY25,MC_GHAO21,MC_TAIH22,MC_TDOY22,MC_TDOY23,MC_TAIH12,MC_TAIH02,MC_TDIY22,MC_TAOY55,MC_TDOY62,MC_TDOY63,MC_TAIH52,MC_TAIH62,MC_TDIY62,BC_GHAI11,MC_GAIH13,MC_GAIH14,MC_PAIH01,MC_TAIH04,MC_TAIH14,MC_TAIH54,MC_PAIL02,MC_TAIL02,MC_PAOY22,MC_THAO11,MC_GHAO11,MC_TAOY22,MC_TAOY52,MC_PRHM01,MC_TRPA01,MC_GRMT01,MU_CMSC03,MC_PLAM02,MC_TAMT14,MC_TAMR04,MC_TAMT04,MC_TLPA02,MU_KLAM03,MC_GPRD02,MU_KDPRYY,MU_KGPRXX=C300_PIMO_PARTS_CALCS.PMIO_Parts(Product)
		MCTAMR04,MCTAMT04,MCTAMT14,MUKLAM03=GS_C300_Cal_Parts.getpartsseriesc(Product)#,MUTMCN01
		A=MCTAMR04+MC_TAMR04
		B=MCTAMT04+MC_TAMT04
		C=MCTAMT14+MC_TAMT14
		D=MUKLAM03+MU_KLAM03
		Length_of_PS_PDP_Cable=Product.Attr('Length_of_PS_PDP_Cable').GetValue()
		Length_of_GI_IS_FTA_PDP_Cable=Product.Attr('Length_of_GI_IS_FTA_PDP_Cable').GetValue()
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-PHAO01",MC_PHAO01)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-PAIH03",MC_PAIH03)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","BC-THAI11",BC_THAI11)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-PSTX03",MC_PSTX03)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-PDOY22",MC_PD0Y22)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","BU-TDOC02",BU_TDOC02)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-PDIY22",MC_PDIY22)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-TAOY25",MC_TAOY25)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-GHAO21",MC_GHAO21)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-TAIH22",MC_TAIH22)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-TDOY22",MC_TDOY22)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-TDOY23",MC_TDOY23)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-TAIH12",MC_TAIH12)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-TAIH02",MC_TAIH02)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-TDIY22",MC_TDIY22)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-TAOY55",MC_TAOY55)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-TDOY62",MC_TDOY62)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-TDOY63",MC_TDOY63)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-TAIH52",MC_TAIH52)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-TAIH62",MC_TAIH62)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-TDIY62",MC_TDIY62)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","BC-GHAI11",BC_GHAI11)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-GAIH13",MC_GAIH13)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-GAIH14",MC_GAIH14)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-PHAI01",MC_PAIH01)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-TAIH04",MC_TAIH04)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-TAIH14",MC_TAIH14)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-TAIH54",MC_TAIH54)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-PAIL02",MC_PAIL02)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-TAIL02",MC_TAIL02)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-PAOY22",MC_PAOY22)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-THAO11",MC_THAO11)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-GHAO11",MC_GHAO11)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-TAOY22",MC_TAOY22)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-TAOY52",MC_TAOY52)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-PRHM01",MC_PRHM01)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-TRPA01",MC_TRPA01)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-GRMT01",MC_GRMT01)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MU-CMSC03",MU_CMSC03)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-PLAM02",MC_PLAM02)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-TLPA02",MC_TLPA02)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-GPRD02",MC_GPRD02)

		if Length_of_GI_IS_FTA_PDP_Cable == 'InCab':
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MU-KGPR00",MU_KGPRXX)
		else:
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MU-KGPR00",0)
		if Length_of_GI_IS_FTA_PDP_Cable == '5M':
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MU-KGPR05",MU_KGPRXX)
		else:
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MU-KGPR05",0)
		if Length_of_GI_IS_FTA_PDP_Cable == '10M':
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MU-KGPR10",MU_KGPRXX)
		else:
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MU-KGPR10",0)
		if Length_of_PS_PDP_Cable == 'InCab':
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MU-KDPR00",MU_KDPRYY)
		else:
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MU-KDPR00",0)
		if Length_of_PS_PDP_Cable == '5M':
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MU-KDPR05",MU_KDPRYY)
		else:
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MU-KDPR05",0)
		if Length_of_PS_PDP_Cable == '10M':
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MU-KDPR10",MU_KDPRYY)
		else:
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MU-KDPR10",0)
		if Length_of_PS_PDP_Cable == '15M':
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MU-KDPR15",MU_KDPRYY)
		else:
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MU-KDPR15",0)
		if Length_of_PS_PDP_Cable == '20M':
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MU-KDPR20",MU_KDPRYY)
		else:
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MU-KDPR20",0)
		if Length_of_PS_PDP_Cable == '25M':
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MU-KDPR25",MU_KDPRYY)
		else:
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MU-KDPR25",0)
		if Length_of_PS_PDP_Cable == '30M':
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MU-KDPR30",MU_KDPRYY)
		else:
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MU-KDPR30",0)
		if Length_of_PS_PDP_Cable == '35M':
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MU-KDPR35",MU_KDPRYY)
		else:
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MU-KDPR35",0)
		if Length_of_PS_PDP_Cable == '40M':
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MU-KDPR40",MU_KDPRYY)
		else:
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MU-KDPR40",0)
		if Length_of_PS_PDP_Cable == '50M':
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MU-KDPR50",MU_KDPRYY)
		else:
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MU-KDPR50",0)
	else:
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-PHAO01",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-PAIH03",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","BC-THAI11",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-PSTX03",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-PDOY22",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","BU-TDOC02",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-PDIY22",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-TAOY25",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-GHAO21",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-TAIH22",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-TDOY22",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-TDOY23",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-TAIH12",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-TAIH02",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-TDIY22",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-TAOY55",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-TDOY62",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-TDOY63",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-TAIH52",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-TAIH62",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-TDIY62",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","BC-GHAI11",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-GAIH13",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-GAIH14",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-PHAI01",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-TAIH04",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-TAIH14",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-TAIH54",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-PAIL02",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-TAIL02",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-PAOY22",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-THAO11",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-GHAO11",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-TAOY22",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-TAOY52",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-PRHM01",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-TRPA01",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-GRMT01",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MU-CMSC03",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-PLAM02",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-TLPA02",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-GPRD02",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MU-KGPR00",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MU-KGPR05",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MU-KGPR10",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MU-KDPR00",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MU-KDPR05",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MU-KDPR10",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MU-KDPR15",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MU-KDPR20",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MU-KDPR25",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MU-KDPR30",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MU-KDPR35",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MU-KDPR40",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MU-KDPR50",0)
	if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series C":
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-TAMT14",C)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-TAMR04",A)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-TAMT04",B)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MU-KLAM03",D)
	elif Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series-C Mark II":
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-TAMT14",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-TAMR04",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MC-TAMT04",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","MU-KLAM03",0)
	if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series-C Mark II" or Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series C":
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-TAIX01",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-TAIX11",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","DC-TAIX11",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","DC-TAIX01",0)
	MARK4 = GS_C300_BOM_Enhance3.IOComponents(Product)
	CC_TAIX01,CC_TAIX11,DC_TAIX11,DC_TAIX01 = MARK4.C300_Mark4()
	if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series-C Mark II" or Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series C":
		if CC_TAIX01 > 0:
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-TAIX01",CC_TAIX01)
		if CC_TAIX11 > 0:
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-TAIX11",CC_TAIX11)
		if DC_TAIX11 > 0:
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","DC-TAIX11",DC_TAIX11)
		if DC_TAIX01 > 0:
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","DC-TAIX01",DC_TAIX01)
	totalLoadIO = GS_C300_Calc_Module.getTotalLoadIO_PMIO(Product)
	Product.Attr("C300_CG_PMIO_Total_IO_Load").AssignValue(str(totalLoadIO))
	controllerType = Product.Attr("SerC_CG_Controller_Type").GetValue()
	controllerModuleType = Product.Attr("SerC_CG_C300_Controller_Module_Type").GetValue()
	if Product.Attr('SerC_CG_PM_IO_Solution_required').GetValue() == "Yes":
		#Product.Messages.Add("Total PMIO Load IO is {}.".format(totalLoadIO))
		for row in Product.GetContainerByName("Series_C_Remote_Groups_Cont").Rows:
			attr = row.Product.Attr("C300_RG_PMIO_Total_IO_Load")
			if attr and attr.GetValue() != "":
				totalLoadIO += float(attr.GetValue())

		qty = ceil(totalLoadIO / 80)

		ioFamily = Product.Attr("SerC_CG_IO_Family_Type").GetValue()
		expRelease = Product.Attr("Experion_PKS_Software_Release").GetValue()
		requiredControllerType = Product.Attr("SerC_CG_Type_of_Controller_Required").GetValue()

		if controllerModuleType == "C300(PCNT02)":
			part = "CC-PCNT02"
			memBlockPart = "CC-SCMB02"
		elif controllerModuleType == "C300(PCNT05)":
			part = "CC-PCNT05"
			memBlockPart = "CC-SCMB05"

		partQty = GS_Get_Set_AtvQty.getAtvQty(Product,'Series_C_CG_Part_Summary',part)
		memblockQty = GS_Get_Set_AtvQty.getAtvQty(Product,'Series_C_CG_Part_Summary',memBlockPart)
		tcntQty = GS_Get_Set_AtvQty.getAtvQty(Product,'Series_C_CG_Part_Summary',"CC-TCNT01")
		swcsQty = GS_Get_Set_AtvQty.getAtvQty(Product,'Series_C_CG_Part_Summary',"TC-SWCS30")

		GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", part, int(partQty) + qty)
		GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", memBlockPart, int(memblockQty) + ceil(qty / 4.0))
		GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "CC-TCNT01", int(tcntQty) + qty)
		GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "TC-SWCS30", int(swcsQty) + qty)
		if controllerType == "Redundant":
			GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", part, int(partQty) + (2 * qty))
			#GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", memBlockPart, int(memblockQty) + ceil(qty / 8.0))
			#GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "TC-SWCS30", int(swcsQty) + ceil(qty / 2.0))
			GS_EEB.setAtvQty(Product, "Series_C_CG_Part_Summary", "CC-TCNT01", int(tcntQty) + (2 * qty))

	#PMIO-PCNT
	if controllerModuleType == "C300(PCNT05)":
		pcntQty05=GS_Get_Set_AtvQty.getAtvQty(Product,"Series_C_CG_Part_Summary","CC-PCNT05")
		Product.Attr("PCNT05_Val").AssignValue(str(pcntQty05))
	elif controllerModuleType == "C300(PCNT02)":
		pcntQty02=GS_Get_Set_AtvQty.getAtvQty(Product,"Series_C_CG_Part_Summary","CC-PCNT02")
		Product.Attr("PCNT02_Val").AssignValue(str(pcntQty02))

	hn, hn2, qty1, qty2, qty3 = GS_SerC_parts.getPmioCgIota(Product)
	if hn > 0:
		GS_EEB.addAtvQty(Product, "Series_C_CG_Part_Summary", "8939-HN", hn)
		GS_EEB.addAtvQty(Product, "Series_C_CG_Part_Summary", "CC-KFSGR5", ceil(ceil(hn/2.0)/2.0))
		GS_EEB.addAtvQty(Product, "Series_C_CG_Part_Summary", "CC-KFSVR5", ceil(hn/2.0) - ceil(ceil(hn/2.0)/2.0))
	if hn2 > 0:
		GS_EEB.addAtvQty(Product, "Series_C_CG_Part_Summary", "8937-HN2", hn2)

	Product.Attr("CG_PMIO_HN").AssignValue(str(hn))
	if qty1 > 0:
		GS_EEB.addAtvQty(Product, "Series_C_CG_Part_Summary", "ICF1150I-SSCT-HPSC", qty1)
	if qty3 > 0:
		GS_EEB.addAtvQty(Product, "Series_C_CG_Part_Summary", "ICF1150I-MSTT-HPSC", qty3)
	if qty2 > 0:
		GS_EEB.addAtvQty(Product, "Series_C_CG_Part_Summary", "51155436-100", qty2)

	#For PMIO Calc
	r = partCalc(Product)
	for part in r:
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary",part,r[part])


	#CXCPQ-41456
	IOType=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
	CCSDOR01,CCKREB=GS_C300_Cal_Parts.getparts41456(Product)
	Cable=Product.Attr('SerC_CG_DO_Relay_Extension_Cable_Length').GetValue()
	if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series C":
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-SDOR01",CCSDOR01)
		if Cable=="0.5M" and CCKREB>0:
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-KREBR5",CCKREB)
		else:
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-KREBR5",0)
		if Cable=="1M" and CCKREB>0:
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-KREB01",CCKREB)
		else:
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-KREB01",0)
		if Cable=="2M" and CCKREB>0:
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-KREB02",CCKREB)
		else:
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-KREB02",0)
		if Cable=="5M" and CCKREB>0:
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-KREB05",CCKREB)
		else:
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-KREB05",0)
		if Cable=="10M" and CCKREB>0:
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-KREB10",CCKREB)
		else:
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-KREB10",0)
		#CXCPQ-55753
		if Cable=="20M" and CCKREB>0:
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-KREB20",CCKREB)
		else:
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-KREB20",0)
		if Cable=="30M" and CCKREB>0:
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-KREB30",CCKREB)
		else:
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-KREB30",0)
		if Cable=="40M" and CCKREB>0:
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-KREB40",CCKREB)
		else:
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-KREB40",0)
		if Cable=="50M" and CCKREB>0:
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-KREB50",CCKREB)
		else:
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-KREB50",0)
	#CXCPQ-50468
	elif Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Turbomachinery":
		Z61= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','Z61')
		Z62= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','Z62')
		Z63= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','Z63')
		Z71= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','Z71')
		Z72= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','Z72')
		Z73= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','Z73')
		Sum_Z = Z61 + Z62 + Z63 + Z71 + Z72 + Z73
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-SDOR01",Sum_Z)
		if Cable=="0.5M":
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-KREBR5",Sum_Z)
		else:
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-KREBR5",0)
		if Cable=="1M":
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-KREB01",Sum_Z)
		else:
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-KREB01",0)
		if Cable=="2M":
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-KREB02",Sum_Z)
		else:
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-KREB02",0)
		if Cable=="5M":
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-KREB05",Sum_Z)
		else:
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-KREB05",0)
		if Cable=="10M":
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-KREB10",Sum_Z)
		else:
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-KREB10",0)
		#CXCPQ-57859
		if Cable=="20M":
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-KREB20",Sum_Z)
		else:
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-KREB20",0)
		if Cable=="30M":
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-KREB30",Sum_Z)
		else:
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-KREB30",0)
		if Cable=="40M":
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-KREB40",Sum_Z)
		else:
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-KREB40",0)
		if Cable=="50M":
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-KREB50",Sum_Z)
		else:
			GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-KREB50",0)
	"""
	#commented by rajagopal as it creates problem for series c mark II
	else:
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-SDOR01",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-KREBR5",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-KREB01",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-KREB02",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-KREB05",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-KREB10",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-KREB20",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-KREB30",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-KREB40",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-KREB50",0) """

	"""#CXCPQ-52347
	parts_dict = GS_SerC_Part_Calcs.getParts52347(Product, {})
	#CXCPQ-54439 - Part calculation of user stories CXCPQ-54003, CXCPQ-54609 are included inside this story
	parts_dict = GS_SerC_Part_Calcs.getParts54439(Product, parts_dict)
	if len(parts_dict) > 0:
		GS_C300_IO_Calc.setIOCount(Product, 'Series_C_CG_Part_Summary', parts_dict)"""

	qyt_SWHS01, qty_SWHS02 = GS_C300_Calc_Module.getSWHSQty(Product)
	GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","TC-SWHS01",qyt_SWHS01)
	GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","TC-SWHS02",qty_SWHS02)
	if Product.Attr('SerC_CG_Controller_Memory_Backup').GetValue() =="No" or (IO_Family=="Series C" and   Product.Attr("SerC_CG_Type_of_Controller_Required").GetValue() != "C300 CEE"):
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-SCMB02",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-SCMB05",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","51454475-100",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","51202330-200",0)
		GS_EEB.setAtvQty(Product,"Series_C_CG_Part_Summary","51202330-300",0)

	Product.ApplyRules()
	Product.ExecuteRulesOnce = False
