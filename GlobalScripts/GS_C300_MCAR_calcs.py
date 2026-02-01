import System.Decimal as D
import GS_C300_IO_Calc,C300_PIMO_PARTS_CALCS
import GS_C300_BOM_MARK,GS_Get_Set_AtvQty,GS_C300_Cal_Parts
#CXCPQ-43394,,CXCPQ-43393,,CXCPQ-43392,CXCPQ-43242,CXCPQ-51548
def mcar_cals(Product):
	SUM_HI=SUM_LO=Sum1=Sum3=Sum4=Sum2=SUM_HI_Mod=SUM_LO_Mod=SUM_LO1=SUM_HI1=Sum11=Sum22=Sum33=Sum44=SUM_LO11=SUM_HI11=SUM_HIC=SUM_LOC=SUM1=SUM2=SUM_D=par12var=0
	HI=LO=LL=C1=SUM_D1=tcntqnt=qntpcnt=0
	MC_PHAO01,MC_PAIH03,BC_THAI11,MC_PSTX03,MC_PD0Y22,BU_TDOC02,MC_PDIY22,MC_TAOY25,MC_GHAO21,MC_TAIH22,MC_TDOY22,MC_TDOY23,MC_TAIH12,MC_TAIH02,MC_TDIY22,MC_TAOY55,MC_TDOY62,MC_TDOY63,MC_TAIH52,MC_TAIH62,MC_TDIY62,BC_GHAI11,MC_GAIH13,MC_GAIH14,MC_PAIH01,MC_TAIH04,MC_TAIH14,MC_TAIH54,MC_PAIL02,MC_TAIL02,MC_PAOY22,MC_THAO11,MC_GHAO11,MC_TAOY22,MC_TAOY52,MC_PRHM01,MC_TRPA01,MC_GRMT01,MU_CMSC03,MC_PLAM02,MC_TAMT14,MC_TAMR04,MC_TAMT04,MC_TLPA02,MU_KLAM03,MC_GPRD02,MU_KDPRYY,MU_KGPRXX=C300_PIMO_PARTS_CALCS.PMIO_Parts(Product)
	sumpmio=int(MC_TAMT14)+int(MC_TAMR04)+int(MC_TAMT04)
	if Product.Name=="Series-C Control Group":
		a,b,qntpcnt=GS_C300_Cal_Parts.getPartCCPCNTQty(Product)
		controllerType = Product.Attr("SerC_CG_Controller_Type").GetValue()
		if controllerType == "Redundant":
			qntpcnt = qntpcnt * 2
		cg_part=Product.GetContainerByName('Series_C_CG_Part_Summary_Cont')
		cg_part1=Product.GetContainerByName('Series_C_CG_Part_Summary_Cont_3rd_Party')
		family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
		mounting_sol=Product.Attr('SerC_CG_IO_Mounting_Solution').GetValue()
		marshling_cab=Product.Attr('SerC_CG_Integrated_Marshalling_Cabinet').GetValue()
		mArsh_lay=Product.Attr('SerC_Integrated_Marshalling_Cabinet').GetValue()
	elif Product.Name=="Series-C Remote Group":
		cg_part=Product.GetContainerByName('Series_C_RG_Part_Summary_Cont')
		cg_part1=Product.GetContainerByName('Series_C_RG_Part_Summary_Cont_3rd_Party')
		family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
		mounting_sol=Product.Attr('SerC_IO_Mounting_Solution').GetValue()
		marshling_cab=Product.Attr('SerC_RG_Integrated_Marshalling_Cabinet').GetValue()
		mArsh_lay=Product.Attr('SerC_RG_Integrated_Marshalling_Cabinet_Layout_Type').GetValue()
	#for High volt cals
	if Product.Name=="Series-C Control Group" or Product.Name=="Series-C Remote Group":
		cont_re=Product.Attr('SerC_CG_Type_of_Controller_Required').GetValue()
		parts12=['None']
		parts9=['None']
		parts6=['None']
		part12D=['None']
		parts_l6=['None']
		parts_l9=['None']
		parts_l12=['None']
		parts_l18=['None']
		par12=['None']
		tcnt=['None']
		if family=='Series C':
			#for High volt cals
			parts12=['CC-TDI120','CC-TDI230','CC-TDI151','CC-TDOR11','CC-SDOR01']
			parts9=['CC-TDI110','CC-TDI220']
			parts6=["CC-TDOR01"]
			part12D=['MC-TAMT04','MC-TAMR04','MC-TAMT14']
		elif family=="Turbomachinery":
			parts12=['CC-TDI120','CC-TDI230','CC-TDI151','CC-TDOR11','CC-SDOR01']
			parts9=['CC-TDI110','CC-TDI220']
			parts6=["CC-TDOR01"]
			part12D=['MC-TAMT04','MC-TAMR04','MC-TAMT14']
			#for Low volt cals
			par12=['F860N']
			parts_l6=['CC-TAIX01','CC-TAIX51','CC-TAID01','CC-TAIN01','CC-TAOX01','CC-TAOX51','CC-TAON01','CC-SDRX01','CC-TCF901','CC-TAIM01']
			parts_l9=['CC-TDIL01','CC-TDIL51','CC-TDOB01','CC-TDOD51','CC-TAIL51','CC-TUIO31','CC-TION11','CC-TNWC01']
			tcnt=['CC-TCNT01']
			parts_l12=['CC-TAIX11','CC-TAIX61','CC-TAID11','CC-TAIN11','CC-TAOX11','CC-TAOX61','CC-TAON11','CC-TDIL11','CC-TDIL61','CC-TDOB11','CC-TDOD61','CC-TUIO01','CC-TPIX11','CC-TUIO41']
			parts_l18=['CC-TSV211','CC-TSP411','CC-TUIO11']
		if cont_re=="C300 CEE" and family=='Series C':
			Trace.Write("test1")
			#for Low volt cals
			parts_l6=['CC-TAIX01','CC-TAIX51','CC-TAID01','CC-TAIN01','CC-TAOX01','CC-TAOX51','CC-TAON01','CC-TFB402','CC-TPOX01','CC-SDRX01','CC-TCF901','CC-TAIM01']
			parts_l9=['CC-TDIL01','CC-TDIL51','CC-TDOB01','CC-TDOD51','CC-TAIL51','CC-TUIO31','CC-TEIM01','CC-TION11','CC-TNWC01']
			tcnt=['CC-TCNT01']
			parts_l12=['CC-TAIX11','CC-TAIX61','CC-TAID11','CC-TAIN11','CC-TAOX11','CC-TAOX61','CC-TAON11','CC-TDIL11','CC-TDIL61','CC-TDOB11','CC-TDOD61','CC-TFB412','CC-TFB811','F860','CC-TUIO01','CC-TPIX11','CC-TUIO41']
			par12=['F860']
			parts_l18=['CC-TSV211','CC-TSP411','CC-TUIO11']
		elif cont_re=="CN100 CEE":
			Trace.Write("test2")
			par12=['F860N']
			parts_l6=['CC-TAIX01','CC-TAIX51','CC-TAID01','CC-TAIN01','CC-TAOX01','CC-TAOX51','CC-TAON01','CC-TAIM01']
			parts_l9=['CC-TDIL01','CC-TDIL51','CC-TDOB01','CC-TDOD51','CC-TAIL51','CC-TUIO31','CC-TION11','CC-TNWC01']
			tcnt=['CC-TCNT']
			parts_l12=['CC-TAIX11','CC-TAIX61','CC-TAID11','CC-TAIN11','CC-TAOX11','CC-TAOX61','CC-TAON11','CC-TDIL11','CC-TDIL61','CC-TDOB11','CC-TDOD61','CC-TPIX11','CC-TUIO41']
			parts_l18=['CC-TSV211NA','CC-TSP411NA','CC-TUIO11NA']
		elif cont_re=="CN100 I/O HIVE - C300 CEE" or cont_re=="Control HIVE - Physical" or cont_re=="Control HIVE - Virtual":
			Trace.Write("test3")
			par12=['F860N']
			tcnt=['CC-TCNT']
			parts_l6=['CC-TAIX01','CC-TAIX51','CC-TAID01','CC-TAIN01','CC-TAOX01','CC-TAOX51','CC-TAON01','CC-TAIM01']
			parts_l9=['CC-TDIL01','CC-TDIL51','CC-TDOB01','CC-TDOD51','CC-TAIL51','CC-TUIO31','CC-TION11','CC-TNWC01']
			parts_l12=['CC-TAIX11','CC-TAIX61','CC-TAID11','CC-TAIN11','CC-TAOX11','CC-TAOX61','CC-TAON11','CC-TDIL11','CC-TDIL61','CC-TDOB11','CC-TDOD61','CC-TUIO01','CC-TPIX11','CC-TUIO41']
			parts_l18=['CC-TUIO11']
		if family=="Series C" or family=="Turbomachinery":
			Trace.Write("Testing")
			for row1 in cg_part1.Rows:
				if row1.GetColumnByName("PartNumber").Value in tcnt:
					tcntqnt =int(qntpcnt) if qntpcnt !='' else 0
				if row1.GetColumnByName("PartNumber").Value in par12:
					par12var +=int(row1.GetColumnByName("Part_Qty").Value)
			for row in cg_part.Rows:
				#Trace.Write(row.GetColumnByName("PartNumber").Value)
				if row.GetColumnByName("PartNumber").Value in parts6:
					Sum1 +=int(row.GetColumnByName("Part_Qty").Value)
					Trace.Write("sum11 "+str(Sum1))
				if row.GetColumnByName("PartNumber").Value in parts9:
					Sum2 +=int(row.GetColumnByName("Part_Qty").Value)
					Trace.Write(Sum2)
				if row.GetColumnByName("PartNumber").Value in parts12:
					Sum3 +=int(row.GetColumnByName("Part_Qty").Value)
					Trace.Write(Sum3)
				#for Low volt cals
				if row.GetColumnByName("PartNumber").Value in parts_l6:
					Sum11 +=int(row.GetColumnByName("Part_Qty").Value)
					Trace.Write("sum11 "+str(Sum11))
				if row.GetColumnByName("PartNumber").Value in parts_l9:
					Sum22 +=int(row.GetColumnByName("Part_Qty").Value)
					Trace.Write("Sum22 "+str(Sum22))
				if row.GetColumnByName("PartNumber").Value in parts_l12:
					Sum33 +=int(row.GetColumnByName("Part_Qty").Value)
					Trace.Write("Sum33 "+str(Sum33))
				if row.GetColumnByName("PartNumber").Value in parts_l18:
					Sum44 +=int(row.GetColumnByName("Part_Qty").Value)
					Trace.Write("Sum44 "+str(Sum44))
				if row.GetColumnByName("PartNumber").Value in part12D:
					SUM1 +=int(row.GetColumnByName("Part_Qty").Value)
					Trace.Write("SUM1 "+str(SUM1))
			SUM_HI=D.Ceiling(((Sum2*9)+(Sum3*12)+(Sum1*6))/36.0)
			Trace.Write("lahu---------....sum hi : "+str(SUM_HI))
			HI=(Sum2*9)+(Sum3*12)+(Sum1*6)
			SUM_LO=D.Ceiling((((Sum22+tcntqnt)*9)+(Sum33*12)+(Sum11*6)+(Sum44*18)+(par12var*12))/36.0)
			Trace.Write("lahu---------....sum Loi : "+str(SUM_LO))
			LO=((Sum22+tcntqnt)*9)+(Sum33*12)+(Sum11*6)+(Sum44*18)+(par12var*12)
			Trace.Write("lahu---------....Loi : "+str(LO))
			SUM_HI_Mod=((Sum2*9)+(Sum3*12)+(Sum1*6))%66
			SUM_LO_Mod=(((Sum22+tcntqnt)*9)+(Sum33*12)+(Sum11*6)+(Sum44*18)+(par12var*12))%66
			SUM_HIC =int(((Sum2*9)+(Sum3*12)+(Sum1*6))/66)
			SUM_LOC =int((((Sum22+tcntqnt)*9)+(Sum33*12)+(Sum11*6)+(Sum44*18)+(par12var*12))/66)
			SUM_D =D.Ceiling(((SUM1-sumpmio)*12)/36.0)
			LL=(SUM1*12)
			Trace.Write("LL-------... "+str(LL))
			if SUM_HI_Mod >0:
				SUM_HI1= SUM_HIC +1
			else:
				SUM_HI1=SUM_HIC
			if SUM_LO_Mod >0:
				SUM_LO1 = SUM_LOC +1
			else:
				SUM_LO1=SUM_LOC
			if SUM_HI_Mod >36:
				SUM_HI11= SUM_HIC +1
			else:
				SUM_HI11=SUM_HIC
			if SUM_LO_Mod >36:
				SUM_LO11 = SUM_LOC +1
			else:
				SUM_LO11=SUM_LOC
			Trace.Write("SUM_HI1 "+str(SUM_HI))
			#Conditions for part qnt
			if family=='Turbomachinery' or ((mounting_sol=="Cabinet" and marshling_cab!="Yes") or (mounting_sol=="Mounting Panel") or (mounting_sol=="Cabinet" and marshling_cab=="Yes" and mArsh_lay=="Top To Bottom") or(mounting_sol=="Cabinet" and marshling_cab=="Yes" and mArsh_lay=="Front To Back")):
				SUM_D =SUM_D
			else:
				SUM_D =0
			if family=='Turbomachinery' or ((mounting_sol=="Cabinet" and marshling_cab!="Yes") or (mounting_sol=="Mounting Panel") or (mounting_sol=="Cabinet" and marshling_cab=="Yes" and mArsh_lay=="Top To Bottom")):
				SUM_HI= SUM_HI
				SUM_LO= SUM_LO
			else:
				SUM_HI= 0
				SUM_LO= 0
			if (mounting_sol=="Cabinet" and marshling_cab=="Yes" and mArsh_lay=="Front To Back"):
				SUM_HI1=SUM_HI1
				SUM_LO1=SUM_LO1
				SUM_HI11=SUM_HI11
				SUM_LO11=SUM_LO11
			else:
				SUM_HI1=0
				SUM_LO1=0
				SUM_HI11=0
				SUM_LO11=0
	GS_Get_Set_AtvQty.setAtvQty(Product, 'SerC_IO_Params', 'A_for_C', SUM_HI)
	GS_Get_Set_AtvQty.setAtvQty(Product, 'SerC_IO_Params', 'B_for_C', SUM_LO)
	GS_Get_Set_AtvQty.setAtvQty(Product, 'SerC_IO_Params', 'E_for_C', SUM_HI1)
	GS_Get_Set_AtvQty.setAtvQty(Product, 'SerC_IO_Params', 'F_for_C', SUM_LO1)
	GS_Get_Set_AtvQty.setAtvQty(Product, 'SerC_IO_Params', 'G_for_C', SUM_HI11)
	GS_Get_Set_AtvQty.setAtvQty(Product, 'SerC_IO_Params', 'H_for_C', SUM_LO11)
	return SUM_HI,SUM_LO,SUM_HI1,SUM_LO1,SUM_HI11,SUM_LO11,SUM_D,HI,LO,LL
#CXCPQ-43393,CXCPQ-51548
def MCARW1(Product):
	SUM_G=sum1=sum2=GI=0
	cg_part1=Product.GetContainerByName('Series_C_CG_Part_Summary_Cont')
	rg_part1=Product.GetContainerByName('Series_C_RG_Part_Summary_Cont')
	#for High volt cals
	part6=['CC-GAIX21','CC-GAOX21','CC-GDIL21']
	part12=['CC-GAIX11','CC-GAOX11','CC-GDIL11','CC-GDIL01','CC-SDXX01','CC-GDOL11']
	if Product.Name=="Series-C Control Group":
		family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
		mounting_sol=Product.Attr('SerC_CG_IO_Mounting_Solution').GetValue()
		marshling_cab=Product.Attr('SerC_CG_Integrated_Marshalling_Cabinet').GetValue()
		mArsh_lay=Product.Attr('SerC_Integrated_Marshalling_Cabinet').GetValue()
		#for G volt cals
		if family=="Series C" or family=='Turbomachinery':
			for row in cg_part1.Rows:
				#Trace.Write(row.GetColumnByName("PartNumber").Value)
				if row.GetColumnByName("PartNumber").Value in part6:
					sum1 +=int(row.GetColumnByName("Part_Qty").Value)
				if row.GetColumnByName("PartNumber").Value in part12:
					sum2 +=int(row.GetColumnByName("Part_Qty").Value)
			GI=((sum1*6)+(sum2*12))
			if family=='Turbomachinery' or ((mounting_sol=="Cabinet" and marshling_cab=="No") or (mounting_sol=="Cabinet" and marshling_cab=="Yes" and (mArsh_lay=="Top To Bottom" or mArsh_lay=="Front To Back"))):
				SUM_G=D.Ceiling(((sum1*6)+(sum2*12))/36.0)
	elif Product.Name=="Series-C Remote Group":
		family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
		mounting_sol=Product.Attr('SerC_IO_Mounting_Solution').GetValue()
		marshling_cab=Product.Attr('SerC_RG_Integrated_Marshalling_Cabinet').GetValue()
		mArsh_lay=Product.Attr('SerC_RG_Integrated_Marshalling_Cabinet_Layout_Type').GetValue()
		#for G volt cals
		if family=="Series C" or family=='Turbomachinery':
			for row in rg_part1.Rows:
				#Trace.Write(row.GetColumnByName("PartNumber").Value)
				if row.GetColumnByName("PartNumber").Value in part6:
					sum1 +=int(row.GetColumnByName("Part_Qty").Value)
				if row.GetColumnByName("PartNumber").Value in part12:
					sum2 +=int(row.GetColumnByName("Part_Qty").Value)
			GI=((sum1*6)+(sum2*12))
			if family=='Turbomachinery' or ((mounting_sol=="Cabinet" and marshling_cab=="No") or (mounting_sol=="Cabinet" and marshling_cab=="Yes" and (mArsh_lay=="Top To Bottom" or mArsh_lay=="Front To Back"))):
				SUM_G=D.Ceiling(((sum1*6)+(sum2*12))/36.0)
	return SUM_G,GI
#CXCPQ-43395,CXCPQ-51548
def MCC003(Product):
	C,GI=MCARW1(Product)
	Trace.Write(C)
	Trace.Write(GI)
	SUM_HI,SUM_LO,SUM_HI1,SUM_LO1,SUM_HI11,SUM_LO11,SUM_D,HI,LO,LL=mcar_cals(Product)
	Trace.Write("SUM_LO "+str(SUM_LO))
	MCC003=0
	if Product.Name=="Series-C Control Group":
		iota=Product.Attr('SerC_CG_IOTA_Carrier_Cover').GetValue()
		family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
		mounting_sol=Product.Attr('SerC_CG_IO_Mounting_Solution').GetValue()
		marshling_cab=Product.Attr('SerC_CG_Integrated_Marshalling_Cabinet').GetValue()
		mArsh_lay=Product.Attr('SerC_Integrated_Marshalling_Cabinet').GetValue()
		if (mounting_sol=="Cabinet" and marshling_cab=="Yes" and mArsh_lay=="Front To Back"):
			SUM_D1=SUM_D
			C1=C
		else:
			SUM_D1=0
			C1=0
		if iota=="Yes" and (family=="Series C"):
			MCC003=D.Ceiling((((SUM_HI*36)+(SUM_HI11*30)+(SUM_HI1*36))-HI)/3.0)+D.Ceiling((((SUM_LO*36)+(SUM_LO11*30)+(SUM_LO1*36))-LO)/3.0)+ D.Ceiling(((C1 *36) - GI)/3.0) + D.Ceiling(((SUM_D1 *36) - LL)/3.0)
			#Trace.Write("Happy "+str(D.Ceiling(((C*36) - GI)/3.0)))
		elif iota=="Yes" and family=='Turbomachinery':
			MCC003=D.Ceiling(((SUM_HI*36) - HI)/3.0) + D.Ceiling(((SUM_LO*36)- LO)/3.0)+D.Ceiling(((C*36) - GI)/3.0) + D.Ceiling(((SUM_D*36) - LL)/3.0)
	elif Product.Name=="Series-C Remote Group":
		iota=Product.Attr('SerC_CG_IOTA_Carrier_Cover').GetValue()
		family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
		mounting_sol=Product.Attr('SerC_IO_Mounting_Solution').GetValue()
		marshling_cab=Product.Attr('SerC_RG_Integrated_Marshalling_Cabinet').GetValue()
		mArsh_lay=Product.Attr('SerC_RG_Integrated_Marshalling_Cabinet_Layout_Type').GetValue()
		if (mounting_sol=="Cabinet" and marshling_cab=="Yes" and mArsh_lay=="Front To Back"):
			SUM_D1=SUM_D
			C1=C
		else:
			SUM_D1=0
			C1=0
		if iota=="Yes" and (family=="Series C"):
			MCC003=D.Ceiling((((SUM_HI*36)+(SUM_HI11*30)+(SUM_HI1*36))-HI)/3.0)+D.Ceiling((((SUM_LO*36)+(SUM_LO11*30)+(SUM_LO1*36))-LO)/3.0)+ D.Ceiling(((C1 *36) - GI)/3.0) + D.Ceiling(((SUM_D1 *36) - LL)/3.0)
		elif iota=="Yes" and family=='Turbomachinery':
			MCC003=D.Ceiling(((SUM_HI*36) - HI)/3.0) + D.Ceiling(((SUM_LO*36)- LO)/3.0)+D.Ceiling(((C*36) - GI)/3.0) + D.Ceiling(((SUM_D*36) - LL)/3.0)
	GS_Get_Set_AtvQty.setAtvQty(Product, 'SerC_IO_Params', 'C_for_C', C1)
	GS_Get_Set_AtvQty.setAtvQty(Product, 'SerC_IO_Params', 'D_for_C', SUM_D1)
	return MCC003

#CXCPQ-47390 start
def cab_c(Product):
	Cab_part=['CC-PWRN01', 'CC-PWRR01', 'CC-PWRB01', 'CC-PWR401', 'CC-PWN401', 'CU-PWMN20', 'CU-PWMR20', 'CU-PWPN20', 'CU-PWPR20']
	x=y=X=Y=Z=K=L=C1=C2=C3=C4=sum1=sum2=CADS=CASS=0
	CADS11=part600=part400=part500=CBDS01=part200=CASS11=part300=part100=CBDD01=CASS12=CADS12=C8SS01=0 #CXCPQ-116603
	SUM_G,GI=MCARW1(Product)
	SUM_HI,SUM_LO,SUM_HI1,SUM_LO1,SUM_HI11,SUM_LO11,SUM_D,HI,LO,LL=mcar_cals(Product)
	if Product.Name=="Series-C Control Group":
		cg_part1=Product.GetContainerByName('Series_C_CG_Part_Summary_Cont')
		family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
		mounting_sol=Product.Attr('SerC_CG_IO_Mounting_Solution').GetValue()
		marshling_cab=Product.Attr('SerC_CG_Integrated_Marshalling_Cabinet').GetValue()
		cab_ac=Product.Attr('SerC_CG_Cabinet_Access').GetValue()
		cab_typ=Product.Attr('SerC_CG_Cabinet_Type_03').GetValue()
		mArsh_lay=Product.Attr('SerC_Integrated_Marshalling_Cabinet').GetValue()
		
		#CXCPQ-116603 
		cab_door_default = Product.Attr('SerC_CG_Cabinet_Doors_Default').GetValue()
		cab_keylock_default = Product.Attr('SerC_CG_Cabinet_Door_Keylock _Default').GetValue()
		cab_hinge = Product.Attr('SerC_CG_Cabinet_Hinge_Type').GetValue()
		cab_color = Product.Attr('SerC_CG_Cabinet_Color_Default').GetValue()
		#CXCPQ-116603
	elif Product.Name=="Series-C Remote Group":
		cg_part1=Product.GetContainerByName('Series_C_RG_Part_Summary_Cont')
		family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
		mounting_sol=Product.Attr('SerC_IO_Mounting_Solution').GetValue()
		marshling_cab=Product.Attr('SerC_RG_Integrated_Marshalling_Cabinet').GetValue()
		cab_ac=Product.Attr('SerC_RG_Cabinet_Access').GetValue()
		cab_typ=Product.Attr('SerC_RG_Cabinet_Type').GetValue()
		mArsh_lay=Product.Attr('SerC_RG_Integrated_Marshalling_Cabinet_Layout_Type').GetValue()
		
		#CXCPQ-116603
		cab_door_default = Product.Attr('SerC_RG_Cabinet_Doors_Default').GetValue()
		cab_keylock_default = Product.Attr('SerC_RG_Cabinet_Door_Keylock_Default').GetValue()
		cab_hinge = Product.Attr('SerC_RG_Cabinet_Hinge_Type_Default').GetValue()
		cab_color = Product.Attr('SerC_RG_Cabinet_Color_Default').GetValue()
		#CXCPQ-116603

	if Product.Name=="Series-C Control Group" or Product.Name=="Series-C Remote Group":
		if family=="Series C" and (mounting_sol=='Cabinet' or mounting_sol=='Mounting Panel'):
			#cab-c Calcs
			#CXCPQ-47390
			x= SUM_HI % 2
			y= SUM_LO % 2
			Trace.Write("eveb--"+str([x,y]))
			if x > 0:
				X = SUM_HI+1
			else:
				X = SUM_HI
			if y > 0:
				Y = SUM_LO+1
			else:
				Y = SUM_LO
			Trace.Write("Z---"+str([X,Y,SUM_HI1,SUM_LO1])+"--K--"+str([SUM_HI11,SUM_LO11]))
			Z=X+Y+SUM_HI1+SUM_LO1
			K=SUM_HI11+SUM_LO11
			L= SUM_D
			Trace.Write("c1---"+str([Z,K,L])+"--C2--"+str(SUM_G))
			C1=D.Ceiling((Z+K+L)/6.0)
			C2=D.Ceiling(SUM_G /4.0)
			C3=D.Ceiling((Z+K+L)/3.0)+D.Ceiling(SUM_G /2.0)
			C4= C1+C2
			for row in cg_part1.Rows:
				#Trace.Write(row.GetColumnByName("PartNumber").Value)
				if row.GetColumnByName("PartNumber").Value in Cab_part:
					sum1 +=int(row.GetColumnByName("Part_Qty").Value)
			sum2= D.Ceiling(sum1/2.0)
			if mounting_sol=='Cabinet' and marshling_cab=='No' and cab_ac=='Dual Access'and cab_typ=='Alternate Cabinet': #CXCPQ-47449
				CADS11=max(sum2,D.Ceiling((C1+C2)/2.0))
				CADS=max(sum2,D.Ceiling((C1+C2)/2.0))
				CADS11= (int(CADS11)% 4)
				Trace.Write("CADS11 "+str(CADS11))
				if CADS11==1:
					CADS11=1
				else:
					CADS11=0
				Trace.Write("CADS11 "+str(CADS11))
			elif mounting_sol=='Cabinet' and marshling_cab=='Yes' and cab_ac=='Single Access'and cab_typ=='Alternate Cabinet' and mArsh_lay=='Top To Bottom': #CXCPQ-47451
				part600=max(sum1,C3)
			elif mounting_sol=='Cabinet' and marshling_cab=='Yes' and cab_ac=='Dual Access'and cab_typ=='Alternate Cabinet' and mArsh_lay=='Front To Back': #CXCPQ-47453
				part400=max(sum1,C4)
			elif mounting_sol=='Cabinet' and marshling_cab=='Yes' and cab_ac=='Dual Access'and cab_typ=='Alternate Cabinet' and mArsh_lay=='Top To Bottom': #CXCPQ-47454
				part500= max(sum2,D.Ceiling(C3/2.0))
			elif mounting_sol=='Cabinet' and marshling_cab=='No' and cab_ac=='Single Access'and cab_typ=='Normal Cabinet': #CXCPQ-39368
				CBDS01= max(sum1,(C1+C2))
				if cab_door_default == "Standard" and cab_keylock_default == "Standard" and cab_hinge == "130 Degree" and cab_color == "Gray-RAL 7035" : #CXCPQ-116603
					C8SS01 = max(sum1,(C1+C2))
					CBDS01 = 0
			elif mounting_sol=='Cabinet' and cab_ac=='Single Access'and cab_typ=='Generic Cabinet': #CXCPQ-82263
				CASS12= max(sum1,(C1+C2))
			elif mounting_sol=='Cabinet' and marshling_cab=='Yes' and cab_ac=='Dual Access'and cab_typ=='Normal Cabinet' and mArsh_lay=='Top To Bottom': #CXCPQ-47422
				part200=  max(sum2,D.Ceiling(C3/2.0))
			elif mounting_sol=='Cabinet' and marshling_cab=='No' and cab_ac=='Single Access'and cab_typ=='Alternate Cabinet': #CXCPQ-47448
				CASS11= max(sum1,(C1+C2))
				CASS= max(sum1,(C1+C2))
				CASS11= (int(CASS11)% 4)
				if CASS11==1:
					CASS11=1
				else:
					CASS11=0
			elif mounting_sol=='Cabinet' and marshling_cab=='Yes' and cab_ac=='Single Access'and cab_typ=='Normal Cabinet' and mArsh_lay=='Top To Bottom': #CXCPQ-47395
				part300= max(sum1,C3)
			elif mounting_sol=='Cabinet' and marshling_cab=='Yes' and cab_ac=='Dual Access'and cab_typ=='Normal Cabinet' and mArsh_lay=='Front To Back': #CXCPQ-47418
				part100=  max(sum1,C4)
			elif mounting_sol=='Cabinet' and marshling_cab=='No' and cab_ac=='Dual Access'and cab_typ=='Normal Cabinet' and (cab_door_default != "Standard" or cab_keylock_default != "Standard" or cab_hinge != "130 Degree" or cab_color != "Gray-RAL 7035"): #CXCPQ-34704
				CBDD01= max(sum2,D.Ceiling((C1+C2)/2.0))
			elif mounting_sol=='Cabinet' and cab_ac=='Dual Access'and cab_typ=='Generic Cabinet': #CXCPQ-82264
				CADS12= max(sum2,D.Ceiling((C1+C2)/2.0))
	GS_Get_Set_AtvQty.setAtvQty(Product, 'SerC_IO_Params', 'CADS', CADS)
	GS_Get_Set_AtvQty.setAtvQty(Product, 'SerC_IO_Params', 'CASS', CASS)
	return CADS11,part600,part400,part500,CBDS01,CASS12,part200,CASS11,part300,part100,CBDD01,CADS12,X,Y,Z,K,L,C1,C2,C3,C4,C8SS01 #CXCPQ-116603

#CXCPQ-44774
def mcar_calsmark(Product):
	params = GS_C300_IO_Calc.getIOCount(Product, 'SerC_IO_Params', ['Z51', 'Z52', 'Z53'])
	Z51=int(params['Z51'])
	Z52=int(params['Z52'])
	Z53=int(params['Z53'])
	#Changes Done By RDT (Ravika Pupneja)---CCEECOMMBR-6721
	Z41= int(GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','Z41'))
	Z42= int(GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','Z42'))
	Z43= int(GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','Z43'))
	W31= int(GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','W31'))
	W32= int(GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','W32'))
	W33= int(GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','W33'))
	W41= int(GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','W41'))
	W42= int(GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','W42'))
	W43= int(GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','W43'))
	X61_V1= int(GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','X61_V1'))
	X61_V2= int(GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','X61_V2'))
	X62_V1= int(GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','X62_V1'))
	X62_V2= int(GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','X62_V2'))
	X63_V1= int(GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','X63_V1'))
	X63_V2= int(GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','X63_V2'))
	X71_V1= int(GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','X71_V1'))
	X71_V2= int(GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','X71_V2'))
	X72_V1= int(GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','X72_V1'))
	X72_V2= int(GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','X72_V2'))
	X73_V1= int(GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','X73_V1'))
	X73_V2= int(GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','X73_V2'))
	X81_V1= int(GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','X81_V1'))
	X81_V2= int(GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','X81_V2'))
	X82_V1= int(GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','X82_V1'))
	X82_V2= int(GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','X82_V2'))
	X83_V1= int(GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','X83_V1'))
	X83_V2= int(GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','X83_V2'))
	A=B=Sum1=Sum3=Sum2=Sum11=Sum22=Sum33=Sum44=C=DD=E=F=G=H=I=Sum=0
	#for High volt cals
	parts12=['DC-TDI120','DC-TDI230','DC-TDI151','DC-TDOR11','DC-SDOR01']
	parts9=['DC-TDI110','DC-TDI220']
	parts6=["DC-TDOR01"]
	#for Low volt cals
	parts_l6=['DC-TAIX01','DC-TAIX51','DC-TAID01','DC-TAIN01','DC-TAOX01','DC-TAOX51','DC-TAON01','DC-TFB403','DC-TPOX01','DC-SDRX01','DC-TCF902']
	parts_l9=['DC-TDIL01','DC-TDIL51','DC-TAIL51','DC-TEIM01','DC-TION11','DC-TCNT01']
	parts_l12=['DC-TAIX11','DC-TAIX61','DC-TAID11','DC-TAIN11','DC-TAOX11','DC-TAOX61','DC-TAON11','DC-TDIL11','DC-TDIL61','DC-TFB413','DC-TFB813','DC-TUIO01']
	parts_l18=['DC-TUIO11']
	if Product.Name=="Series-C Control Group":
		C300_part=Product.GetContainerByName('Series_C_CG_Part_Summary_Cont')
		family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
		currnt=Product.Attr('SerC_CG_Current_required_for_each_DO').GetValue() if Product.Attr('SerC_CG_Current_required_for_each_DO').GetValue() !='' else 0
		Trace.Write(family)
	elif Product.Name=="Series-C Remote Group":
		C300_part=Product.GetContainerByName('Series_C_RG_Part_Summary_Cont')
		family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
		currnt=Product.Attr('SerC_CG_Current_required_for_each_DO1').GetValue() if Product.Attr('SerC_CG_Current_required_for_each_DO1').GetValue() !='' else 0
	if Product.Name=="Series-C Control Group" or Product.Name=="Series-C Remote Group":
		if family=='Series-C Mark II':
			for row in C300_part.Rows:
				#Trace.Write(row.GetColumnByName("PartNumber").Value)
				if row.GetColumnByName("PartNumber").Value in parts6:
					Sum1 +=int(row.GetColumnByName("Part_Qty").Value)
				if row.GetColumnByName("PartNumber").Value in parts9:
					Sum2 +=int(row.GetColumnByName("Part_Qty").Value)
				if row.GetColumnByName("PartNumber").Value in parts12:
					Sum3 +=int(row.GetColumnByName("Part_Qty").Value)
				#for Low volt cals
				if row.GetColumnByName("PartNumber").Value in parts_l6:
					Sum11 +=int(row.GetColumnByName("Part_Qty").Value)
				if row.GetColumnByName("PartNumber").Value in parts_l9:
					Sum22 +=int(row.GetColumnByName("Part_Qty").Value)
				if row.GetColumnByName("PartNumber").Value in parts_l12:
					Sum33 +=int(row.GetColumnByName("Part_Qty").Value)
				if row.GetColumnByName("PartNumber").Value in parts_l18:
					Sum44 +=int(row.GetColumnByName("Part_Qty").Value)
				#Changes Done By RDT (Ravika Pupneja)---CCEECOMMBR-6594 and 6721
				if row.GetColumnByName("PartNumber").Value =="DC-TDOD61":
					C= max(D.Ceiling(((W41+W42)*int(currnt))/3200),D.Ceiling((W41+W42)/3.0))+ D.Ceiling((W31+W32)/3.0)
				if row.GetColumnByName("PartNumber").Value =="DC-TDOD51":
					DD= max(D.Ceiling(((W43)*int(currnt))/3200),D.Ceiling((W43)/4.0))+ D.Ceiling((W33)/4.0)
				if row.GetColumnByName("PartNumber").Value =="DC-TDOB11":
					E= max(D.Ceiling(((Z51+Z52)*int(currnt))/3200),D.Ceiling((Z51+Z52)/3.0)) + D.Ceiling((Z41+Z42)/3.0)
				if row.GetColumnByName("PartNumber").Value =="DC-TDOB01":
					F= max(D.Ceiling(((Z53)*int(currnt))/3200),D.Ceiling((Z53)/4.0)) + D.Ceiling((Z43)/4.0)
				if row.GetColumnByName("PartNumber").Value =="DC-TUIO41":
					G= max(D.Ceiling((X61_V1+X61_V2+X62_V1+X62_V2+X63_V1+X63_V2+X71_V1+X71_V2+X72_V1+X72_V2+X73_V1+X73_V2)/3000.0),D.Ceiling(int(row.GetColumnByName("Part_Qty").Value)/3.0))
				if row.GetColumnByName("PartNumber").Value =="DC-TUIO31":
					H= max(D.Ceiling((X81_V1+X81_V2+X82_V1+X82_V2+X83_V1+X83_V2)/3000.0),D.Ceiling(int(row.GetColumnByName("Part_Qty").Value)/4.0))
				if row.GetColumnByName("PartNumber").Value =="DC-TPIX11":
					I= max(D.Ceiling((int(row.GetColumnByName("Part_Qty").Value)*1.52)/3.0),D.Ceiling(int(row.GetColumnByName("Part_Qty").Value)/3.0))
			A=D.Ceiling(((Sum2*9)+(Sum3*12)+(Sum1*6))/36.0)
			B=D.Ceiling(((Sum11*6)+(Sum22*9)+(Sum33*12)+(Sum44*18))/36.0)
			Sum =int(A)+int(B)+int(C)+int(DD)+int(E)+int(F)+int(G)+int(H)+int(I)
	return A,B,C,DD,E,F,G,H,I,Sum

#CXCPQ-47807,CXCPQ-47806,CXCPQ-47808
def cabmarkII(Product):
	Thermo_qnt1=Thermo_qnt2=Thermo_qnt3=Thermo_qnt4=0
	CBDD01=CBDS01=cab100=cab200=cab9_2=power1=power2=0
	if Product.Name=="Series-C Control Group":
		C300_part=Product.GetContainerByName('Series_C_CG_Part_Summary_Cont')
		family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
		cab_ac=Product.Attr('SerC_CG_Cabinet_Access').GetValue()
		light_D=Product.Attr('SerC_CG_Cabinet_Light_Default').GetValue()
		Cab_therm=Product.Attr('SerC_CG_Cabinet_Thermostat_Default').GetValue()
		Trace.Write(Cab_therm)
		power_Def=Product.Attr('SerC_CG_Power_Entry_Default').GetValue()
	elif Product.Name=="Series-C Remote Group":
		C300_part=Product.GetContainerByName('Series_C_RG_Part_Summary_Cont')
		family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
		cab_ac=Product.Attr('SerC_RG_Cabinet_Access').GetValue()
		light_D=Product.Attr('SerC_RG_Cabinet_Light_Default').GetValue()
		Cab_therm=Product.Attr('SerC_RG_Cabinet_Thermostat_Default').GetValue()
		power_Def=Product.Attr('SerC_RG_Power_Entry_Default').GetValue()
	if Product.Name=="Series-C Control Group" or Product.Name=="Series-C Remote Group":
		if family=='Series-C Mark II':
			for row in C300_part.Rows:
				#Trace.Write(row.GetColumnByName("PartNumber").Value)
				if row.GetColumnByName("PartNumber").Value in ["CC-CBDD01"]:
					CBDD01=int(row.GetColumnByName("Part_Qty").Value)
				if row.GetColumnByName("PartNumber").Value in ["CC-CBDS01"]:
					CBDS01=int(row.GetColumnByName("Part_Qty").Value)
			cab9_2=CBDD01+CBDS01
			if cab_ac=="Dual Access" and Cab_therm=="Yes":
				Thermo_qnt2=2*CBDD01
			elif cab_ac=="Single Access" and Cab_therm=="Yes":
				Thermo_qnt2=1*CBDS01
			if cab_ac=="Dual Access" and power_Def=="Double Pole":
				power2=2*CBDD01
			elif cab_ac=="Single Access" and power_Def=="Double Pole":
				power2=1*CBDS01
			if cab_ac=="Dual Access":
				cab200=1*CBDD01
			elif cab_ac=="Single Access":
				cab100=1*CBDS01
			if cab_ac=="Dual Access" and light_D=="Yes":
				Thermo_qnt4=2*CBDD01
			elif cab_ac=="Single Access" and light_D=="Yes":
				Thermo_qnt4=1*CBDS01
	return Thermo_qnt2,Thermo_qnt4,cab9_2,power2,cab200,cab100
#CXCPQ-51436
def cab_51436(Product):
	Cab_part=['CC-PWRN01', 'CC-PWRR01', 'CC-PWRB01']
	x=y=X=Y=Z=L=C1=C2=sum1=sum2=0
	CBDS01=CBDD01=RF_4=RR_3=RFR_2=RF_6=RR_5=RFR_5=Std_5=Gray_200=Custom_100=0
	Single_S1=Single_D1=Dual_S1=Dual_D1=Single_130=Single_180=Dual_130=Dual_180=0
	SUM_G,GI=MCARW1(Product)
	SUM_HI,SUM_LO,SUM_HI1,SUM_LO1,SUM_HI11,SUM_LO11,SUM_D,HI,LO,LL=mcar_cals(Product)
	if Product.Name=="Series-C Control Group":
		cg_part1=Product.GetContainerByName('Series_C_CG_Part_Summary_Cont')
		family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
		cab_ac=Product.Attr('SerC_CG_Cabinet_Access').GetValue()
		Cabinet_Door_Default=Product.Attr('SerC_CG_Cabinet_Doors_Default').GetValue()
		Color_Default=Product.Attr('SerC_CG_Cabinet_Color_Default').GetValue()
		Cabinet_Hinge_Type=Product.Attr('SerC_CG_Cabinet_Hinge_Type').GetValue()
	elif Product.Name=="Series-C Remote Group":
		cg_part1=Product.GetContainerByName('Series_C_RG_Part_Summary_Cont')
		family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
		cab_ac=Product.Attr('SerC_RG_Cabinet_Access').GetValue()
		Cabinet_Door_Default=Product.Attr('SerC_RG_Cabinet_Doors_Default').GetValue()
		Color_Default=Product.Attr('SerC_RG_Cabinet_Color_Default').GetValue()
		Cabinet_Hinge_Type=Product.Attr('SerC_RG_Cabinet_Hinge_Type_Default').GetValue()
	if Product.Name=="Series-C Control Group" or Product.Name=="Series-C Remote Group":
		if family=="Turbomachinery":
			#cab-c Calcs
			#CXCPQ-51436
			x= SUM_HI % 2
			y= SUM_LO % 2
			if x > 0:
				X = SUM_HI+1
			else:
				X = SUM_HI
			if y > 0:
				Y = SUM_LO+1
			else:
				Y = SUM_LO
			Z=X+Y
			L= SUM_D
			C1=D.Ceiling((Z+L)/6.0)
			C2=D.Ceiling(SUM_G /4.0)
			for row in cg_part1.Rows:
				#Trace.Write(row.GetColumnByName("PartNumber").Value)
				if row.GetColumnByName("PartNumber").Value in Cab_part:
					sum1 +=int(row.GetColumnByName("Part_Qty").Value)
			sum2= D.Ceiling(sum1/2.0)
			if cab_ac=='Dual Access': #CXCPQ-51502
				CBDD01= max(sum2,D.Ceiling((C1+C2)/2.0))
			elif cab_ac=='Single Access': #CXCPQ-51473
				CBDS01= max(sum1,(C1+C2))
			if cab_ac=='Dual Access' and Cabinet_Door_Default=='Reverse Front': #CXCPQ-51520
				RF_4= int(CBDD01)*1
			elif cab_ac=='Dual Access' and Cabinet_Door_Default=='Reverse Rear': #CXCPQ-51520
				RR_3= int(CBDD01)*1
			elif cab_ac=='Dual Access' and Cabinet_Door_Default=='Reverse Front & Rear': #CXCPQ-51520
				RFR_2= int(CBDD01)*1
			if cab_ac=='Single Access' and Cabinet_Door_Default=='Reverse Front': #CXCPQ-51519
				RF_6= int(CBDS01)*1
			elif cab_ac=='Single Access' and Cabinet_Door_Default=='Reverse Rear': #CXCPQ-51519
				RR_5= int(CBDS01)*1
			elif cab_ac=='Single Access' and Cabinet_Door_Default=='Reverse Front & Rear': #CXCPQ-51519
				RFR_5= int(CBDS01)*1
			elif cab_ac=='Single Access' and Cabinet_Door_Default=='Standard': #CXCPQ-51519
				Std_5= int(CBDS01)*1
			if (cab_ac=='Single Access' or cab_ac=='Dual Access') and Color_Default=='Gray-RAL 7032': #CXCPQ-51514
				Gray_200= (int(CBDD01) or int(CBDS01))*1
			elif (cab_ac=='Single Access' or cab_ac=='Dual Access') and Color_Default=='Custom': #CXCPQ-51514
				Custom_100= (int(CBDD01) or int(CBDS01))*1
			if cab_ac=='Single Access' and (Cabinet_Door_Default=='Standard' or Cabinet_Door_Default == 'Reverse Front' or Cabinet_Door_Default=='Reverse Rear' or Cabinet_Door_Default=='Reverse Front & Rear'): #CXCPQ-51516
				Single_S1= int(CBDS01)*1
			elif cab_ac=='Single Access' and Cabinet_Door_Default=='Double': #CXCPQ-51516
				Single_D1= int(CBDS01)*1
			elif cab_ac=='Dual Access' and (Cabinet_Door_Default=='Standard' or Cabinet_Door_Default == 'Reverse Front' or Cabinet_Door_Default=='Reverse Rear' or Cabinet_Door_Default=='Reverse Front & Rear'): #CXCPQ-51516
				Dual_S1= int(CBDD01)*2
			elif cab_ac=='Dual Access' and Cabinet_Door_Default=='Double': #CXCPQ-51516
				Dual_D1= int(CBDD01)*2
			if cab_ac=='Single Access' and Cabinet_Hinge_Type=='130 Degree': #CXCPQ-51525
				Single_130= int(CBDS01)*1
			elif cab_ac=='Single Access' and Cabinet_Hinge_Type=='180 Degree': #CXCPQ-51525
				Single_180= int(CBDS01)*1
			elif cab_ac=='Dual Access' and Cabinet_Hinge_Type=='130 Degree': #CXCPQ-51525
				Dual_130= int(CBDD01)*2
			elif cab_ac=='Dual Access' and Cabinet_Hinge_Type=='180 Degree': #CXCPQ-51525
				Dual_180= int(CBDD01)*2
	return CBDS01,CBDD01,RF_4,RR_3,RFR_2,RF_6,RR_5,RFR_5,Std_5,Gray_200,Custom_100,Single_S1,Single_D1,Dual_S1,Dual_D1,Single_130,Single_180,Dual_130,Dual_180,X,Y,Z,L,C1,C2