IsR2QRequest = Quote.GetCustomField("isR2QRequest").Content
Proposal_Type=Quote.GetCustomField('EGAP_Proposal_Type').Content
if IsR2QRequest != 'Yes':
	if Product.Attr('PERF_ExecuteScripts').GetValue()=='SCRIPT_RUN':
		import GS_C300_BOM_Enhance3
		import System.Decimal as D
		import GS_PS_Exp_Ent_BOM as GP_EEB
		import GS_Get_Set_AtvQty
		import C300_PIMO_PARTS_CALCS
		from GS_C300_PMIO_Cal import partCalc
		from math import ceil
		import GS_C300_Cal_Parts
		import GS_C300_IO_Calc, GS_C300_Calc_Module, GS_C300_CN100_cal,GS_Part_C300_CNM_Calc,GS_C300_RG_UPC_Calc3
		
		Product.ExecuteRulesOnce = True


		#CXCPQ-41491
		V43= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','V43')
		V83= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','V83')
		V91= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','V91')
		V92= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','V92')
		if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series C" and Product.Attr('Ser_RG_Universal_Marshalling_Cabinet').GetValue() == "No":
			CC_SDXX01 = V43 + V83 + V91 + V92
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-SDXX01",CC_SDXX01)
		#CXCPQ-50470
		elif Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Turbomachinery":
			CC_SDXX01 = V43 + V83 + V91 + V92
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-SDXX01",CC_SDXX01)
		else:
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-SDXX01",0)
		if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series-C Mark II" or Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series C":
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-TAIX01",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-TAIX11",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","DC-TAIX11",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","DC-TAIX01",0)
		MARK4 = GS_C300_BOM_Enhance3.IOComponents(Product)
		CC_TAIX01,CC_TAIX11,DC_TAIX11,DC_TAIX01 = MARK4.C300_Mark4()
		if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series-C Mark II" or Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series C":
			if CC_TAIX01 > 0:
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-TAIX01",CC_TAIX01)
			if CC_TAIX11 > 0:
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-TAIX11",CC_TAIX11)
			if DC_TAIX11 > 0:
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","DC-TAIX11",DC_TAIX11)
			if DC_TAIX01 > 0:
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","DC-TAIX01",DC_TAIX01)
	
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
			CC_GDIL01 = V43 + V83
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-GAOX21",CC_GAOX21)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-GDIL21",CC_GDIL21)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-GDIL01",CC_GDIL01)
		#CXCPQ-50471
		elif IO_Family=="Turbomachinery":
			CC_GAOX21 = W73
			CC_GDIL21 = V13 + V53
			CC_GDIL01 = V43 + V83
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
		#CXCPQ-50472
		elif IO_Family=="Turbomachinery":
			CC_GDIL11 = (V21+V31+ V22+V32+V61+V71+V62+V72)
			CC_GAOX11 = (W81+W91+W82+W92)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-GDIL11",CC_GDIL11)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-GAOX11",CC_GAOX11)
		else:
			CC_GDIL11=CC_GAOX11 = 0
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-GDIL11",CC_GDIL11)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-GAOX11",CC_GAOX11)

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
		IO_Mounting_Solution = Product.Attr('Dummy_RG_IO_Mounting_Solution').GetValue()
		Universal1=Product.Attr('Ser_RG_Universal_Marshalling_Cabinet').GetValue()
		if family_type_NEW == "Series C" and Universal1== 'No' and IO_Mounting_Solution == "Cabinet":
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
		#CXCPQ-50473
		elif family_type_NEW == "Turbomachinery":
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

		if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series C":
			MC_PHAO01,MC_PAIH03,BC_THAI11,MC_PSTX03,MC_PD0Y22,BU_TDOC02,MC_PDIY22,MC_TAOY25,MC_GHAO21,MC_TAIH22,MC_TDOY22,MC_TDOY23,MC_TAIH12,MC_TAIH02,MC_TDIY22,MC_TAOY55,MC_TDOY62,MC_TDOY63,MC_TAIH52,MC_TAIH62,MC_TDIY62,BC_GHAI11,MC_GAIH13,MC_GAIH14,MC_PAIH01,MC_TAIH04,MC_TAIH14,MC_TAIH54,MC_PAIL02,MC_TAIL02,MC_PAOY22,MC_THAO11,MC_GHAO11,MC_TAOY22,MC_TAOY52,MC_PRHM01,MC_TRPA01,MC_GRMT01,MU_CMSC03,MC_PLAM02,MC_TAMT14,MC_TAMR04,MC_TAMT04,MC_TLPA02,MU_KLAM03,MC_GPRD02,MU_KDPRYY,MU_KGPRXX=C300_PIMO_PARTS_CALCS.PMIO_Parts(Product)
			MCTAMR04,MCTAMT04,MCTAMT14,MUKLAM03=GS_C300_Cal_Parts.getpartsseriesc(Product)#,MUTMCN01
			A=MCTAMR04+MC_TAMR04
			B=MCTAMT04+MC_TAMT04
			C=MCTAMT14+MC_TAMT14
			D=MUKLAM03+MU_KLAM03
			Length_of_PS_PDP_Cable=Product.Attr('Length_of_PS_PDP_Cable').GetValue()
			Length_of_GI_IS_FTA_PDP_Cable=Product.Attr('Length_of_GI_IS_FTA_PDP_Cable').GetValue()
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-PHAO01",MC_PHAO01)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-PAIH03",MC_PAIH03)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","BC-THAI11",BC_THAI11)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-PSTX03",MC_PSTX03)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-PDOY22",MC_PD0Y22)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","BU-TDOC02",BU_TDOC02)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-PDIY22",MC_PDIY22)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-TAOY25",MC_TAOY25)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-GHAO21",MC_GHAO21)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-TAIH22",MC_TAIH22)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-TDOY22",MC_TDOY22)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-TDOY23",MC_TDOY23)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-TAIH12",MC_TAIH12)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-TAIH02",MC_TAIH02)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-TDIY22",MC_TDIY22)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-TAOY55",MC_TAOY55)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-TDOY62",MC_TDOY62)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-TDOY63",MC_TDOY63)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-TAIH52",MC_TAIH52)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-TAIH62",MC_TAIH62)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-TDIY62",MC_TDIY62)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","BC-GHAI11",BC_GHAI11)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-GAIH13",MC_GAIH13)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-GAIH14",MC_GAIH14)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-PHAI01",MC_PAIH01)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-TAIH04",MC_TAIH04)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-TAIH14",MC_TAIH14)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-TAIH54",MC_TAIH54)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-PAIL02",MC_PAIL02)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-TAIL02",MC_TAIL02)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-PAOY22",MC_PAOY22)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-THAO11",MC_THAO11)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-GHAO11",MC_GHAO11)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-TAOY22",MC_TAOY22)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-TAOY52",MC_TAOY52)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-PRHM01",MC_PRHM01)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-TRPA01",MC_TRPA01)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-GRMT01",MC_GRMT01)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-CMSC03",MU_CMSC03)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-PLAM02",MC_PLAM02)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-TLPA02",MC_TLPA02)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-GPRD02",MC_GPRD02)
			#GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-KDPR05",MU_KDPR05)
			#GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-KDPR10",MU_KDPR10)
			#GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-KDPR00",MU_KDPRInCab)

			if Length_of_GI_IS_FTA_PDP_Cable == 'InCab':
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-KGPR00",MU_KGPRXX)
			else:
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-KGPR00",0)
			if Length_of_GI_IS_FTA_PDP_Cable == '5M':
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-KGPR05",MU_KGPRXX)
			else:
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-KGPR05",0)
			if Length_of_GI_IS_FTA_PDP_Cable == '10M':
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-KGPR10",MU_KGPRXX)
			else:
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-KGPR10",0)
			if Length_of_PS_PDP_Cable == 'InCab':
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-KDPR00",MU_KDPRYY)
			else:
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-KDPR00",0)
			if Length_of_PS_PDP_Cable == '5M':
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-KDPR05",MU_KDPRYY)
			else:
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-KDPR05",0)
			if Length_of_PS_PDP_Cable == '10M':
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-KDPR10",MU_KDPRYY)
			else:
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-KDPR10",0)
			if Length_of_PS_PDP_Cable == '15M':
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-KDPR15",MU_KDPRYY)
			else:
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-KDPR15",0)
			if Length_of_PS_PDP_Cable == '20M':
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-KDPR20",MU_KDPRYY)
			else:
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-KDPR20",0)
			if Length_of_PS_PDP_Cable == '25M':
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-KDPR25",MU_KDPRYY)
			else:
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-KDPR25",0)
			if Length_of_PS_PDP_Cable == '30M':
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-KDPR30",MU_KDPRYY)
			else:
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-KDPR30",0)
			if Length_of_PS_PDP_Cable == '35M':
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-KDPR35",MU_KDPRYY)
			else:
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-KDPR35",0)
			if Length_of_PS_PDP_Cable == '40M':
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-KDPR40",MU_KDPRYY)
			else:
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-KDPR40",0)
			if Length_of_PS_PDP_Cable == '50M':
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-KDPR50",MU_KDPRYY)
			else:
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-KDPR50",0)
		else:
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-PHAO01",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-PAIH03",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","BC-THAI11",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-PSTX03",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-PDOY22",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","BU-TDOC02",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-PDIY22",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-TAOY25",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-GHAO21",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-TAIH22",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-TDOY22",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-TDOY23",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-TAIH12",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-TAIH02",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-TDIY22",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-TAOY55",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-TDOY62",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-TDOY63",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-TAIH52",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-TAIH62",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-TDIY62",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","BC-GHAI11",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-GAIH13",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-GAIH14",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-PHAI01",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-TAIH04",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-TAIH14",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-TAIH54",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-PAIL02",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-TAIL02",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-PAOY22",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-THAO11",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-GHAO11",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-TAOY22",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-TAOY52",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-PRHM01",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-TRPA01",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-GRMT01",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-CMSC03",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-PLAM02",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-TLPA02",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-GPRD02",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-KGPR00",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-KGPR05",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-KGPR10",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-KDPR00",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-KDPR05",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-KDPR10",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-KDPR15",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-KDPR20",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-KDPR25",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-KDPR30",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-KDPR35",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-KDPR40",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-KDPR50",0)
		if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series C":
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-TAMT14",C)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-TAMR04",A)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-TAMT04",B)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-KLAM03",D)
			#GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-TMCN01",MUTMCN01)
		#The below if condition is not required for Turbomachinery it may be required for series-c mark II
		elif Product.Attr('SerC_CG_IO_Family_Type').GetValue() != "Turbomachinery":
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-TAMT14",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-TAMR04",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-TAMT04",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-KLAM03",0)
			#GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MU-TMCN01",0)

		totalLoadIO = GS_C300_Calc_Module.getTotalLoadIO_PMIO(Product)
		Product.Attr("C300_RG_PMIO_Total_IO_Load").AssignValue(str(totalLoadIO))
		GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-IOLX02",0)

		hn = Product.Attr("CG_PMIO_HN").GetValue()
		hn = int(hn) if hn else 0
		X = ceil(hn / 2.0)
		G = ceil(X / 2.0)
		V = X - G
		if Product.Attr('SerC_CG_PM_IO_Solution_required').GetValue() == "Yes":
			Product.Messages.Add("Total PMIO Load IO is {}.".format(totalLoadIO))
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","MC-IOLX02",ceil(totalLoadIO/40.0))
			if Product.Attr("SerC_RG_Fiber_Optic_IO_Link_Extender_Type_for_PMIO").GetValue() == "Multi Mode":
				GP_EEB.addAtvQty(Product,"Series_C_RG_Part_Summary","CC-KFSGR5",2 * G)
				GP_EEB.addAtvQty(Product,"Series_C_RG_Part_Summary","CC-KFSVR5",2 * V)

		#For PMIO Calc
		r = partCalc(Product)
		for part in r:
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary",part,r[part])

		#CXCPQ-41456
		IOType=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
		if IOType=="Series C":
			CCSDOR01,CCKREB=GS_C300_Cal_Parts.getparts41456(Product)
			Cable=Product.Attr('SerC_RG_DO_Relay_Extension_Cable_Length').GetValue()
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-SDOR01",CCSDOR01)
			if Cable=="0.5M" and CCKREB>0:
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-KREBR5",CCKREB)
			else:
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-KREBR5",0)
			if Cable=="1M" and CCKREB>0:
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-KREB01",CCKREB)
			else:
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-KREB01",0)
			if Cable=="2M" and CCKREB>0:
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-KREB02",CCKREB)
			else:
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-KREB02",0)
			if Cable=="5M" and CCKREB>0:
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-KREB05",CCKREB)
			else:
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-KREB05",0)
			if Cable=="10M" and CCKREB>0:
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-KREB10",CCKREB)
			else:
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-KREB10",0)
			#CXCPQ-55753
			if Cable=="20M" and CCKREB>0:
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-KREB20",CCKREB)
			else:
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-KREB20",0)
			if Cable=="30M" and CCKREB>0:
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-KREB30",CCKREB)
			else:
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-KREB30",0)
			if Cable=="40M" and CCKREB>0:
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-KREB40",CCKREB)
			else:
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-KREB40",0)
			if Cable=="50M" and CCKREB>0:
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-KREB50",CCKREB)
			else:
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-KREB50",0)
		#CXCPQ-50468
		elif Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Turbomachinery":
			Cable=Product.Attr('SerC_RG_DO_Relay_Extension_Cable_Length').GetValue()
			Z61= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','Z61')
			Z62= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','Z62')
			Z63= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','Z63')
			Z71= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','Z71')
			Z72= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','Z72')
			Z73= GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','Z73')
			Sum_Z = Z61 + Z62 + Z63 + Z71 + Z72 + Z73
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-SDOR01",Sum_Z)
			if Cable=="0.5M":
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-KREBR5",Sum_Z)
			else:
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-KREBR5",0)
			if Cable=="1M":
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-KREB01",Sum_Z)
			else:
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-KREB01",0)
			if Cable=="2M":
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-KREB02",Sum_Z)
			else:
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-KREB02",0)
			if Cable=="5M":
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-KREB05",Sum_Z)
			else:
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-KREB05",0)
			if Cable=="10M":
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-KREB10",Sum_Z)
			else:
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-KREB10",0)
			#CXCPQ-57859
			if Cable=="20M":
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-KREB20",Sum_Z)
			else:
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-KREB20",0)
			if Cable=="30M":
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-KREB30",Sum_Z)
			else:
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-KREB30",0)
			if Cable=="40M":
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-KREB40",Sum_Z)
			else:
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-KREB40",0)
			if Cable=="50M":
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-KREB50",Sum_Z)
			else:
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-KREB50",0)
		"""
		#commented by rajagopal as it creates problem for series c mark II
		else:
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-SDOR01",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-KREBR5",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-KREB01",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-KREB02",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-KREB05",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-KREB10",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-KREB20",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-KREB30",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-KREB40",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-KREB50",0)"""
		#52186
		io_mounting=Product.Attr('SerC_IO_Mounting_Solution').GetValue()
		Trace.Write("1111")
		result=GS_C300_CN100_cal.Controller(Product)
		qty11=GS_C300_RG_UPC_Calc3.getpartCCINAM01(Product)
		qty12=GS_C300_RG_UPC_Calc3.getpartCCIION01(Product)
		Trace.Write("222"+str(result))
		if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series C":
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-IION01",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-TION11",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-INAM01",0)
			if io_mounting!="Universal Process Cab - 1.3M" and  Product.Attr('SerC_CG_Type_of_Controller_Required').GetValue() == "C300 CEE":
				if Product.Attr('SerC_RG_CN100_I/O_HOVE').GetValue() == "Redundant":
					Trace.Write("555")
					GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-IION01",2*(result))
					GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-TION11",result)
					GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-INAM01",2*(result))
				if Product.Attr('SerC_RG_CN100_I/O_HOVE').GetValue() == "Non Redundant":
					GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-IION01",result)
					GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-TION11",result)
					GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-INAM01",result)
			if io_mounting=='Universal Process Cab - 1.3M':
				if qty11>0:
					GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-INAM01",qty11)
				if qty12>0:
					GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-IION01",qty12)


		Product.ApplyRules()
		Product.ExecuteRulesOnce = False
else:
	if Product.Attr('PERF_ExecuteScripts').GetValue()=='SCRIPT_RUN':
		import GS_C300_BOM_Enhance3
		import System.Decimal as D
		import GS_PS_Exp_Ent_BOM as GP_EEB
		import GS_Get_Set_AtvQty
		import C300_PIMO_PARTS_CALCS
		from GS_C300_PMIO_Cal import partCalc
		from math import ceil
		import GS_C300_Cal_Parts
		import GS_C300_IO_Calc, GS_C300_Calc_Module, GS_C300_CN100_cal,GS_Part_C300_CNM_Calc,GS_C300_RG_UPC_Calc3
		
		Product.ExecuteRulesOnce = True
		if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series-C Mark II" or Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series C":
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-TAIX01",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-TAIX11",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","DC-TAIX11",0)
			GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","DC-TAIX01",0)
		MARK4 = GS_C300_BOM_Enhance3.IOComponents(Product)
		CC_TAIX01,CC_TAIX11,DC_TAIX11,DC_TAIX01 = MARK4.C300_Mark4()
		if Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series-C Mark II" or Product.Attr('SerC_CG_IO_Family_Type').GetValue() == "Series C":
			if CC_TAIX01 > 0:
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-TAIX01",CC_TAIX01)
			if CC_TAIX11 > 0:
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","CC-TAIX11",CC_TAIX11)
			if DC_TAIX11 > 0:
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","DC-TAIX11",DC_TAIX11)
			if DC_TAIX01 > 0:
				GP_EEB.setAtvQty(Product,"Series_C_RG_Part_Summary","DC-TAIX01",DC_TAIX01)
		Product.ApplyRules()
		Product.ExecuteRulesOnce = False