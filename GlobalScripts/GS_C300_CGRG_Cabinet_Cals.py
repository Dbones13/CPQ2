import GS_Get_Set_AtvQty
import GS_C300_MCAR_calcs
#import GS_C300_SeriesC_Cabinet_Calcs
#CBDS01=float(TagParserProduct.ParseString('<* GetAtvQty(Series_C_CG_Part_Summary:CC-CBDS01) *>'))
#CBDD01=float(TagParserProduct.ParseString('<* GetAtvQty(Series_C_CG_Part_Summary:CC-CBDD01) *>'))
#part300=float(TagParserProduct.ParseString('<* GetAtvQty(Series_C_CG_Part_Summary:51454314-300) *>'))
#CASS11=float(TagParserProduct.ParseString('<* GetAtvQty(Series_C_CG_Part_Summary:CC-CASS11) *>'))
#part600=float(TagParserProduct.ParseString('<* GetAtvQty(Series_C_CG_Part_Summary:51454314-600) *>'))
#part200=float(TagParserProduct.ParseString('<* GetAtvQty(Series_C_CG_Part_Summary:51454314-200) *>'))
#part100=float(TagParserProduct.ParseString('<* GetAtvQty(Series_C_CG_Part_Summary:51454314-100) *>'))
#CADS11=float(TagParserProduct.ParseString('<* GetAtvQty(Series_C_CG_Part_Summary:CC-CADS11) *>'))
#part400=float(TagParserProduct.ParseString('<* GetAtvQty(Series_C_CG_Part_Summary:51454314-400) *>'))
#part500=float(TagParserProduct.ParseString('<* GetAtvQty(Series_C_CG_Part_Summary:51454314-500) *>'))
#CADS11,part600,part400,part500,CBDS01,part200,CASS11,part300,part100,CBDD01,X,Y,Z,K,L,C1,C2,C3,C4=GS_C300_MCAR_calcs.cab_c(Product)
#QTY_A,QTY_B,QTY_C,QTY_D,QTY_E1,QTY_E2,Val_A,Val_B,Val_C=GS_C300_SeriesC_Cabinet_Calcs.C300_calcs_part(Product)

#CXCPQ-47603
def C300_Cabinet(Product,CBDS01,CBDD01,CASS12,CADS12):
	CBD_S01=CBDS01
	Trace.Write('CBD_S01 :'+str(CBD_S01))
	CBD_D01=CBDD01
	Trace.Write('CBD_D01 :'+str(CBD_D01))
	CAS_S12=CASS12
	CAD_S12=CADS12
	Qty_476031=Qty_476032=0
	if Product.Name=="Series-C Control Group":
		#cg_part1=Product.GetContainerByName('Series_C_CG_Part_Summary_Cont')
		family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
		mounting_sol=Product.Attr('SerC_CG_IO_Mounting_Solution').GetValue()
		marshling_cab=Product.Attr('SerC_CG_Integrated_Marshalling_Cabinet').GetValue()
		cab_ac=Product.Attr('SerC_CG_Cabinet_Access').GetValue()
		cab_typ=Product.Attr('SerC_CG_Cabinet_Type_03').GetValue()
		mArsh_lay=Product.Attr('SerC_Integrated_Marshalling_Cabinet').GetValue()
		
		if family!='Series C' and mounting_sol!='Cabinet' and marshling_cab!='No' and (cab_ac!='Dual Access' or cab_ac!='Single Access') and cab_typ!='Normal Cabinet':
			return 0,0
		if family=="Series C":
			if mounting_sol=='Cabinet' and marshling_cab=='No' and cab_ac=='Single Access' and cab_typ=='Normal Cabinet':
				Qty_476031= (int(CBD_S01))*1
			elif mounting_sol=='Cabinet' and cab_ac=='Single Access' and cab_typ=='Generic Cabinet':
				Qty_476031= (int(CAS_S12))*1
			elif mounting_sol=='Cabinet' and marshling_cab=='No' and cab_ac=='Dual Access' and cab_typ=='Normal Cabinet':
				Qty_476032= (int(CBD_D01))*1
			elif mounting_sol=='Cabinet' and cab_ac=='Dual Access' and cab_typ=='Generic Cabinet':
				Qty_476032= (int(CAD_S12))*1
	elif Product.Name=="Series-C Remote Group":
		#rg_part1=Product.GetContainerByName('Series_C_RG_Part_Summary_Cont')
		family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
		mounting_sol=Product.Attr('SerC_IO_Mounting_Solution').GetValue()
		marshling_cab=Product.Attr('SerC_RG_Integrated_Marshalling_Cabinet').GetValue()
		cab_ac=Product.Attr('SerC_RG_Cabinet_Access').GetValue()
		cab_typ=Product.Attr('SerC_RG_Cabinet_Type').GetValue()
		mArsh_lay=Product.Attr('SerC_RG_Integrated_Marshalling_Cabinet_Layout_Type').GetValue()
		
		if family!='Series C' and mounting_sol!='Cabinet' and marshling_cab!='No' and (cab_ac!='Dual Access' or cab_ac!='Single Access') and cab_typ!='Normal Cabinet':
			return 0,0
		if family=="Series C":
			if mounting_sol=='Cabinet' and marshling_cab=='No' and cab_ac=='Single Access' and cab_typ =='Normal Cabinet':
				Qty_476031= (int(CBD_S01))*1
			elif mounting_sol=='Cabinet' and cab_ac=='Single Access' and cab_typ =='Generic Cabinet':
				Qty_476031= (int(CAS_S12))*1
			elif mounting_sol=='Cabinet' and marshling_cab=='No' and cab_ac=='Dual Access' and cab_typ =='Normal Cabinet':
				Qty_476032= (int(CBD_D01))*1
			elif mounting_sol=='Cabinet' and cab_ac=='Dual Access' and cab_typ == 'Generic Cabinet':
				Qty_476032= (int(CAD_S12))*1
	return Qty_476031,Qty_476032
#FinalQty = C300_Cabinet(Product,CBDS01,CBDD01)
#Trace.Write('FinalQty : ' + str(FinalQty))

#CXCPQ-47620
def C300_Cabinet1(Product):
	CADS11,part600,part400,part500,CBDS01,CASS12,part200,CASS11,part300,part100,CBDD01,CADS12,X,Y,Z,K,L,C1,C2,C3,C4,C8SS01=GS_C300_MCAR_calcs.cab_c(Product) #CXCPQ-116603
	CASS= int(GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','CASS'))
	CADS= int(GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','CADS'))
	CBD_S01=CBDS01
	Trace.Write('CBD_S01 :'+str(CBD_S01))
	CBD_SS12=CASS12
	Trace.Write('CBD_SS12 :'+str(CBD_SS12))
	Cab_300=part300
	Trace.Write('Cab_300 :'+str(Cab_300))
	Cab_S11=CASS
	Trace.Write('Cab_S11 :'+str(Cab_S11))
	Cab_600=part600
	Trace.Write('Cab_600 :'+str(Cab_600))
	Cab_200=part200
	Trace.Write('Cab_200 :'+str(Cab_200))
	CBD_D01=CBDD01
	Trace.Write('CBD_D01 :'+str(CBD_D01))
	CBD_DS12=CADS12
	Trace.Write('CBD_DS12 :'+str(CBD_DS12))
	Cab_100=part100
	Trace.Write('Cab_100 :'+str(Cab_100))
	Cab_D11=CADS
	Trace.Write('Cab_D11 :'+str(Cab_D11))
	Cab_400=part400
	Trace.Write('Cab_400 :'+str(Cab_400))
	Cab_500=part500
	Trace.Write('Cab_500 :'+str(Cab_500))
	Qty_47620=0
	if Product.Name=="Series-C Control Group":
		family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
		mounting_sol=Product.Attr('SerC_CG_IO_Mounting_Solution').GetValue()
		cab_ac=Product.Attr('SerC_CG_Cabinet_Access').GetValue()
		cab_typ=Product.Attr('SerC_CG_Cabinet_Type_03').GetValue()
		Integrated_marshalling=Product.Attr('SerC_CG_Integrated_Marshalling_Cabinet').GetValue()

		if family=="Series C":
			if mounting_sol=='Cabinet' and (cab_ac=='Dual Access' or cab_ac=='Single Access') and (cab_typ=='Normal Cabinet' or cab_typ=='Alternate Cabinet' or cab_typ=='Generic Cabinet'):
				Qty_47620= ((int(CBD_S01) or int(Cab_300) or int(Cab_S11) or int(Cab_600) or int(Cab_200) or int(CBD_SS12) )*1) or ((int(CBD_D01) or int(Cab_100) or int(Cab_D11) or int(Cab_400) or int(Cab_500) or int(CBD_DS12))* 2)
				Trace.Write('Qty_47620 :'+str(Qty_47620))

	elif Product.Name=="Series-C Remote Group":
		family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
		mounting_sol=Product.Attr('SerC_IO_Mounting_Solution').GetValue()
		cab_ac=Product.Attr('SerC_RG_Cabinet_Access').GetValue()
		cab_typ=Product.Attr('SerC_RG_Cabinet_Type').GetValue()

		if family=="Series C":
			if mounting_sol=='Cabinet' and (cab_ac=='Dual Access' or cab_ac=='Single Access') and (cab_typ=='Normal Cabinet' or cab_typ=='Alternate Cabinet' or cab_typ=='Generic Cabinet'):
				Qty_47620= ((int(CBD_S01) or int(Cab_300) or int(Cab_S11) or int(Cab_600) or int(Cab_200) or int(CBD_SS12))*1) or ((int(CBD_D01) or int(Cab_100) or int(Cab_D11) or int(Cab_400) or int(Cab_500) or int(CBD_DS12))* 2)
				Trace.Write('Qty_47620 :'+str(Qty_47620))
	return Qty_47620
#FinalQty = C300_Cabinet1(Product)
#Trace.Write('K....FinalQty : ' + str(FinalQty))

#CXCPQ-35489
def C300_Cabinet2(Product,CBDS01,CASS12,part300,part200,CBDD01,CADS12,part100):
	CBD_S01=CBDS01
	Trace.Write('CBD_S01 :'+str(CBD_S01))
	CBD_SS12=CASS12
	Trace.Write('CBD_SS12 :'+str(CBD_SS12))
	Cab_300=part300
	Trace.Write('Cab_300 :'+str(Cab_300))
	Cab_200=part200
	Trace.Write('Cab_200 :'+str(Cab_200))
	CBD_D01=CBDD01
	Trace.Write('CBD_D01 :'+str(CBD_D01))
	CBD_DS12=CADS12
	Trace.Write('CBD_DS12 :'+str(CBD_DS12))
	Cab_100=part100
	Trace.Write('Cab_100 :'+str(Cab_100))
	Qty_354891=Qty_3548911=0
	Qty_354892=Qty_3548922=0
	Qty_83004=Qty_830044=0
	Qty_83157=Qty_831577=0
	if Product.Name=="Series-C Control Group":
		family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
		mounting_sol=Product.Attr('SerC_CG_IO_Mounting_Solution').GetValue()
		cab_ac=Product.Attr('SerC_CG_Cabinet_Access').GetValue()
		cab_typ=Product.Attr('SerC_CG_Cabinet_Type_03').GetValue()
		cab_plinth=Product.Attr('SerC_CG_Cabinet_Base_(Plinth)').GetValue()
		cab_base=Product.Attr('SerC_CG_Cabinet_Base_Size').GetValue()
		if family!='Series C' and mounting_sol!='Cabinet' and (cab_ac!='Dual Access' or cab_ac!='Single Access') and (cab_typ!='Normal Cabinet' or cab_typ!='Generic Cabinet') and cab_plinth!='Yes':
			return 0,0,0,0
		if family=="Series C":
			if mounting_sol=='Cabinet' and cab_ac=='Single Access' and cab_typ=='Normal Cabinet' and cab_plinth=='Yes' and cab_base=='100mm':
				Qty_354891= (int(CBD_S01) or int(Cab_300))*1
			elif mounting_sol=='Cabinet' and cab_ac=='Single Access' and cab_typ=='Normal Cabinet' and cab_plinth=='Yes' and cab_base=='200mm':
				Qty_3548911= (int(CBD_S01) or int(Cab_300))*1
			elif mounting_sol=='Cabinet' and cab_ac=='Single Access' and cab_typ=='Generic Cabinet' and cab_plinth=='Yes' and cab_base=='100mm':
				Qty_83004= (int(CBD_SS12))*1
			elif mounting_sol=='Cabinet' and cab_ac=='Single Access' and cab_typ=='Generic Cabinet' and cab_plinth=='Yes' and cab_base=='200mm':
				Qty_830044= (int(CBD_SS12))*1
			elif mounting_sol=='Cabinet' and cab_ac=='Dual Access' and cab_typ=='Generic Cabinet' and cab_plinth=='Yes' and cab_base=='100mm':
				Qty_83157= (int(CBD_DS12))*1
			elif mounting_sol=='Cabinet' and cab_ac=='Dual Access' and cab_typ=='Generic Cabinet' and cab_plinth=='Yes' and cab_base=='200mm':
				Qty_831577= (int(CBD_DS12))*1
			elif mounting_sol=='Cabinet' and cab_ac=='Dual Access' and cab_typ=='Normal Cabinet' and cab_plinth=='Yes' and cab_base=='100mm':
				Qty_354892= (int(CBD_D01) or int(Cab_100) or int(Cab_200))*1
			elif mounting_sol=='Cabinet' and cab_ac=='Dual Access' and cab_typ=='Normal Cabinet' and cab_plinth=='Yes' and cab_base=='200mm':
				Qty_3548922= (int(CBD_D01) or int(Cab_100) or int(Cab_200))*1
	elif Product.Name=="Series-C Remote Group":
		family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
		mounting_sol=Product.Attr('SerC_IO_Mounting_Solution').GetValue()
		cab_ac=Product.Attr('SerC_RG_Cabinet_Access').GetValue()
		cab_typ=Product.Attr('SerC_RG_Cabinet_Type').GetValue()
		cab_plinth=Product.Attr('SerC_RG_Cabinet_Base_(Plinth)').GetValue()
		cab_base=Product.Attr('SerC_RG_Cabinet_Base_Size').GetValue()
		if family!='Series C' and mounting_sol!='Cabinet' and (cab_ac!='Dual Access' or cab_ac!='Single Access') and (cab_typ!='Normal Cabinet' or cab_typ!='Generic Cabinet') and cab_plinth!='Yes':
			return 0,0,0,0
		if family=="Series C":
			if mounting_sol=='Cabinet' and cab_ac=='Single Access' and cab_typ=='Normal Cabinet' and cab_plinth=='Yes' and cab_base=='100mm':
				Qty_354891= (int(CBD_S01) or int(Cab_300))*1
			elif mounting_sol=='Cabinet' and cab_ac=='Single Access' and cab_typ=='Normal Cabinet' and cab_plinth=='Yes' and cab_base=='200mm':
				Qty_3548911= (int(CBD_S01) or int(Cab_300))*1
			elif mounting_sol=='Cabinet' and cab_ac=='Single Access' and cab_typ=='Generic Cabinet' and cab_plinth=='Yes' and cab_base=='100mm':
				Qty_83004= (int(CBD_SS12))*1
			elif mounting_sol=='Cabinet' and cab_ac=='Single Access' and cab_typ=='Generic Cabinet' and cab_plinth=='Yes' and cab_base=='200mm':
				Qty_830044= (int(CBD_SS12))*1
			elif mounting_sol=='Cabinet' and cab_ac=='Dual Access' and cab_typ=='Generic Cabinet' and cab_plinth=='Yes' and cab_base=='100mm':
				Qty_83157= (int(CBD_DS12))*1
			elif mounting_sol=='Cabinet' and cab_ac=='Dual Access' and cab_typ=='Generic Cabinet' and cab_plinth=='Yes' and cab_base=='200mm':
				Qty_831577= (int(CBD_DS12))*1
			elif mounting_sol=='Cabinet' and cab_ac=='Dual Access' and cab_typ=='Normal Cabinet' and cab_plinth=='Yes' and cab_base=='100mm':
				Qty_354892= (int(CBD_D01) or int(Cab_100) or int(Cab_200))*1
			elif mounting_sol=='Cabinet' and cab_ac=='Dual Access' and cab_typ=='Normal Cabinet' and cab_plinth=='Yes' and cab_base=='200mm':
				Qty_3548922= (int(CBD_D01) or int(Cab_100) or int(Cab_200))*1
	return Qty_354891,Qty_3548911,Qty_354892,Qty_3548922,Qty_83004,Qty_830044,Qty_83157,Qty_831577
#FinalQty = C300_Cabinet2(Product,CBDS01,part300,part200,CBDD01,part100)
#Trace.Write('FinalQty : ' + str(FinalQty))

#CXCPQ-35488
def C300_Cabinet3(Product,CBDS01,CASS12,part300,part200,CBDD01,CADS12,part100):
	CBD_S01=CBDS01
	Trace.Write('CBD_S01 :'+str(CBD_S01))
	CBD_SS12=CASS12
	Trace.Write('CBD_SS12 :'+str(CBD_SS12))
	Cab_300=part300
	Trace.Write('Cab_300 :'+str(Cab_300))
	Cab_200=part200
	Trace.Write('Cab_200 :'+str(Cab_200))
	CBD_D01=CBDD01
	Trace.Write('CBD_D01 :'+str(CBD_D01))
	CBD_DS12=CADS12
	Trace.Write('CBD_DS12 :'+str(CBD_DS12))
	Cab_100=part100
	Trace.Write('Cab_100 :'+str(Cab_100))
	Qty_35488=0
	Qty_354882=0
	if Product.Name=="Series-C Control Group":
		family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
		mounting_sol=Product.Attr('SerC_CG_IO_Mounting_Solution').GetValue()
		cab_ac=Product.Attr('SerC_CG_Cabinet_Access').GetValue()
		cab_typ=Product.Attr('SerC_CG_Cabinet_Type_03').GetValue()
		cab_color=Product.Attr('SerC_CG_Cabinet_Color_Default').GetValue()

		if family!='Series C' and mounting_sol!='Cabinet' and (cab_ac!='Dual Access' or cab_ac!='Single Access') and (cab_typ!='Normal Cabinet' or cab_typ!='Generic Cabinet') and (cab_color!='Gray-RAL 7032' or cab_color!='Custom'):
			return 0,0
		if family=="Series C":
			if mounting_sol=='Cabinet' and (cab_ac=='Single Access' or cab_ac=='Dual Access') and (cab_typ=='Normal Cabinet' or cab_typ=='Generic Cabinet') and cab_color=='Gray-RAL 7032':
				Qty_35488= (int(CBD_S01) or int(Cab_300) or int(CBD_D01) or int(Cab_100) or int(Cab_200) or int(CBD_SS12) or int(CBD_DS12))*1
				Trace.Write('Qty_35488 :'+str(Qty_35488))
			elif mounting_sol=='Cabinet' and (cab_ac=='Single Access' or cab_ac=='Dual Access') and (cab_typ=='Normal Cabinet' or cab_typ=='Generic Cabinet') and cab_color=='Custom':
				Qty_354882= (int(CBD_S01) or int(Cab_300) or int(CBD_D01) or int(Cab_100) or int(Cab_200) or int(CBD_SS12) or int(CBD_DS12))*1
				Trace.Write('Qty_354882 :'+str(Qty_354882))

	elif Product.Name=="Series-C Remote Group":
		family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
		mounting_sol=Product.Attr('SerC_IO_Mounting_Solution').GetValue()
		cab_ac=Product.Attr('SerC_RG_Cabinet_Access').GetValue()
		cab_typ=Product.Attr('SerC_RG_Cabinet_Type').GetValue()
		cab_color=Product.Attr('SerC_RG_Cabinet_Color_Default').GetValue()

		if family!='Series C' and mounting_sol!='Cabinet' and (cab_ac!='Dual Access' or cab_ac!='Single Access') and (cab_typ!='Normal Cabinet' or cab_typ!='Generic Cabinet') and (cab_color!='Gray-RAL 7032' or cab_color!='Custom'):
			return 0,0
		if family=="Series C":
			if mounting_sol=='Cabinet' and (cab_ac=='Single Access' or cab_ac=='Dual Access') and (cab_typ=='Normal Cabinet' or cab_typ=='Generic Cabinet') and cab_color=='Gray-RAL 7032':
				Qty_35488= (int(CBD_S01) or int(Cab_300) or int(CBD_D01) or int(Cab_100) or int(Cab_200) or int(CBD_SS12) or int(CBD_DS12))*1
				Trace.Write('Qty_35488 :'+str(Qty_35488))
			elif mounting_sol=='Cabinet' and (cab_ac=='Single Access' or cab_ac=='Dual Access') and (cab_typ=='Normal Cabinet' or cab_typ=='Generic Cabinet') and cab_color=='Custom':
				Qty_354882= (int(CBD_S01) or int(Cab_300) or int(CBD_D01) or int(Cab_100) or int(Cab_200) or int(CBD_SS12) or int(CBD_DS12))*1
				Trace.Write('Qty_354882 :'+str(Qty_354882))
	return Qty_35488,Qty_354882
#FinalQty = C300_Cabinet3(Product,CBDS01,part300,part200,CBDD01,part100)
#Trace.Write('FinalQty : ' + str(FinalQty))

#CXCPQ-34706
def C300_Cabinet4(Product,CBDS01,CASS12,part300,part200,CBDD01,CADS12,part100):
	CBD_S01=CBDS01
	Trace.Write('CBD_S01 :'+str(CBD_S01))
	CBD_SS12=CASS12
	Trace.Write('CBD_SS12 :'+str(CBD_SS12))
	Cab_300=part300
	Trace.Write('Cab_300 :'+str(Cab_300))
	Cab_200=part200
	Trace.Write('Cab_200 :'+str(Cab_200))
	CBD_D01=CBDD01
	Trace.Write('CBD_D01 :'+str(CBD_D01))
	CBD_DS12=CADS12
	Trace.Write('CBD_DS12 :'+str(CBD_DS12))
	Cab_100=part100
	Trace.Write('Cab_100 :'+str(Cab_100))
	Qty_34706=0
	Qty_347062=0
	Qty_82979=0
	Qty_829792=0
	if Product.Name=="Series-C Control Group":
		family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
		mounting_sol=Product.Attr('SerC_CG_IO_Mounting_Solution').GetValue()
		cab_ac=Product.Attr('SerC_CG_Cabinet_Access').GetValue()
		cab_typ=Product.Attr('SerC_CG_Cabinet_Type_03').GetValue()
		keylock=Product.Attr('SerC_CG_Cabinet_Door_Keylock _Default').GetValue()

		if family!='Series C' and mounting_sol!='Cabinet' and (cab_ac!='Dual Access' or cab_ac!='Single Access') and cab_typ!='Normal Cabinet' and (keylock!='Standard' or keylock!='Pushbutton'):
			return 0,0
		if family=="Series C":
			if mounting_sol=='Cabinet' and cab_ac=='Single Access'and cab_typ=='Normal Cabinet' and keylock=='Standard':
				Qty_34706= (int(CBD_S01) or int(Cab_300))*1
				Trace.Write('Qty_34706 :'+str(Qty_34706))
			elif mounting_sol=='Cabinet' and cab_ac=='Single Access'and cab_typ=='Normal Cabinet' and keylock=='Pushbutton':
				Qty_347062= (int(CBD_S01) or int(Cab_300))*1
				Trace.Write('Qty_347062 :'+str(Qty_347062))
			elif mounting_sol=='Cabinet' and cab_ac=='Single Access'and cab_typ=='Generic Cabinet' and keylock=='Standard':
				Qty_82979= (int(CBD_SS12))*1
				Trace.Write('Qty_82979 :'+str(Qty_82979))
			elif mounting_sol=='Cabinet' and cab_ac=='Single Access'and cab_typ=='Generic Cabinet' and keylock=='Pushbutton':
				Qty_829792= (int(CBD_SS12))*1
				Trace.Write('Qty_829792 :'+str(Qty_829792))
			elif mounting_sol=='Cabinet' and cab_ac=='Dual Access'and cab_typ=='Normal Cabinet' and keylock=='Standard':
				Qty_34706= (int(CBD_D01) or int(Cab_200) or int(Cab_100))*2
				Trace.Write('Qty_34706 :'+str(Qty_34706))
			elif mounting_sol=='Cabinet' and cab_ac=='Dual Access'and cab_typ=='Normal Cabinet' and keylock=='Pushbutton':
				Qty_347062= (int(CBD_D01) or int(Cab_200) or int(Cab_100))*2
				Trace.Write('Qty_347062 :'+str(Qty_347062))
			elif mounting_sol=='Cabinet' and cab_ac=='Dual Access'and cab_typ=='Generic Cabinet' and keylock=='Standard':
				Qty_82979= (int(CBD_DS12))*2
				Trace.Write('Qty_82979 :'+str(Qty_82979))
			elif mounting_sol=='Cabinet' and cab_ac=='Dual Access'and cab_typ=='Generic Cabinet' and keylock=='Pushbutton':
				Qty_829792= (int(CBD_DS12))*2
				Trace.Write('Qty_829792 :'+str(Qty_829792))

	elif Product.Name=="Series-C Remote Group":
		family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
		mounting_sol=Product.Attr('SerC_IO_Mounting_Solution').GetValue()
		cab_ac=Product.Attr('SerC_RG_Cabinet_Access').GetValue()
		cab_typ=Product.Attr('SerC_RG_Cabinet_Type').GetValue()
		keylock=Product.Attr('SerC_RG_Cabinet_Door_Keylock_Default').GetValue()

		if family!='Series C' and mounting_sol!='Cabinet' and (cab_ac!='Dual Access' or cab_ac!='Single Access') and cab_typ!='Normal Cabinet' and (keylock!='Standard' or keylock!='Pushbutton'):
			return 0,0
		if family=="Series C":
			if mounting_sol=='Cabinet' and cab_ac=='Single Access'and cab_typ=='Normal Cabinet' and keylock=='Standard':
				Qty_34706= (int(CBD_S01) or int(Cab_300))*1
				Trace.Write('Qty_34706 :'+str(Qty_34706))
			elif mounting_sol=='Cabinet' and cab_ac=='Single Access'and cab_typ=='Normal Cabinet' and keylock=='Pushbutton':
				Qty_347062= (int(CBD_S01) or int(Cab_300))*1
				Trace.Write('Qty_347062 :'+str(Qty_347062))
			elif mounting_sol=='Cabinet' and cab_ac=='Single Access'and cab_typ=='Generic Cabinet' and keylock=='Standard':
				Qty_82979= (int(CBD_SS12))*1
				Trace.Write('Qty_82979 :'+str(Qty_82979))
			elif mounting_sol=='Cabinet' and cab_ac=='Single Access'and cab_typ=='Generic Cabinet' and keylock=='Pushbutton':
				Qty_829792= (int(CBD_SS12))*1
				Trace.Write('Qty_829792 :'+str(Qty_829792))
			elif mounting_sol=='Cabinet' and cab_ac=='Dual Access'and cab_typ=='Normal Cabinet' and keylock=='Standard':
				Qty_34706= (int(CBD_D01) or int(Cab_200) or int(Cab_100))*2
				Trace.Write('Qty_34706 :'+str(Qty_34706))
			elif mounting_sol=='Cabinet' and cab_ac=='Dual Access'and cab_typ=='Normal Cabinet' and keylock=='Pushbutton':
				Qty_347062= (int(CBD_D01) or int(Cab_200) or int(Cab_100))*2
				Trace.Write('Qty_347062 :'+str(Qty_347062))
			elif mounting_sol=='Cabinet' and cab_ac=='Dual Access'and cab_typ=='Generic Cabinet' and keylock=='Standard':
				Qty_82979= (int(CBD_DS12))*2
				Trace.Write('Qty_82979 :'+str(Qty_82979))
			elif mounting_sol=='Cabinet' and cab_ac=='Dual Access'and cab_typ=='Generic Cabinet' and keylock=='Pushbutton':
				Qty_829792= (int(CBD_DS12))*2
				Trace.Write('Qty_829792 :'+str(Qty_829792))
	return Qty_34706,Qty_347062,Qty_82979,Qty_829792
#FinalQty = C300_Cabinet4(Product,CBDS01,part300,part200,CBDD01,part100)
#Trace.Write('FinalQty : ' + str(FinalQty))

#CXCPQ-45657
def C300_Cabinet5(Product):
	CADS11,part600,part400,part500,CBDS01,CASS12,part200,CASS11,part300,part100,CBDD01,CADS12,X,Y,Z,K,L,C1,C2,C3,C4,C8SS01=GS_C300_MCAR_calcs.cab_c(Product) #CXCPQ-116603
	CASS= int(GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','CASS'))
	CADS= int(GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','CADS'))
	CBD_S01=CBDS01
	Trace.Write('CBD_S01 :'+str(CBD_S01))
	Cab_300=part300
	Trace.Write('Cab_300 :'+str(Cab_300))
	Cab_S11=CASS
	Trace.Write('Cab_S11 :'+str(Cab_S11))
	Cab_600=part600
	Trace.Write('Cab_600 :'+str(Cab_600))
	Cab_200=part200
	Trace.Write('Cab_200 :'+str(Cab_200))
	CBD_D01=CBDD01
	Trace.Write('CBD_D01 :'+str(CBD_D01))
	Cab_100=part100
	Trace.Write('Cab_100 :'+str(Cab_100))
	Cab_D11=CADS
	Trace.Write('Cab_D11 :'+str(Cab_D11))
	Cab_400=part400
	Trace.Write('Cab_400 :'+str(Cab_400))
	Cab_500=part500
	Trace.Write('Cab_500 :'+str(Cab_500))
	CAS_S12=CASS12
	CAD_S12=CADS12
	Qty_45657=0
	Qty_456572=0
	if Product.Name=="Series-C Control Group":
		family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
		mounting_sol=Product.Attr('SerC_CG_IO_Mounting_Solution').GetValue()
		cab_ac=Product.Attr('SerC_CG_Cabinet_Access').GetValue()
		cab_typ=Product.Attr('SerC_CG_Cabinet_Type_03').GetValue()

		if family=="Series C":
			if mounting_sol=='Cabinet' and (cab_ac=='Single Access' or cab_ac=='Dual Access') and cab_typ in ['Normal Cabinet','Alternate Cabinet','Generic Cabinet']:
				Qty_45657= (int(CBD_S01) or int(CBD_D01) or int(Cab_100) or int(Cab_200) or int(Cab_300) or int(Cab_400) or int(Cab_500) or int(Cab_600) or int(Cab_S11) or int(Cab_D11) or int(CAS_S12) or int(CAD_S12))*1
				Trace.Write('Qty_45657 :'+str(Qty_45657))
				
				Qty_456572= (int(CBD_S01) or int(CBD_D01) or int(Cab_100) or int(Cab_200) or int(Cab_300) or int(Cab_400) or int(Cab_500) or int(Cab_600) or int(Cab_S11) or int(Cab_D11) or int(CAS_S12) or int(CAD_S12))*1
				Trace.Write('Qty_456572 :'+str(Qty_456572))

	elif Product.Name=="Series-C Remote Group":
		family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
		mounting_sol=Product.Attr('SerC_IO_Mounting_Solution').GetValue()
		cab_ac=Product.Attr('SerC_RG_Cabinet_Access').GetValue()
		cab_typ=Product.Attr('SerC_RG_Cabinet_Type').GetValue()

		if family=="Series C":
			if mounting_sol=='Cabinet' and (cab_ac=='Single Access' or cab_ac=='Dual Access') and cab_typ in ['Normal Cabinet','Alternate Cabinet','Generic Cabinet']:
				Qty_45657= (int(CBD_S01) or int(CBD_D01) or int(Cab_100) or int(Cab_200) or int(Cab_300) or int(Cab_400) or int(Cab_500) or int(Cab_600) or int(Cab_S11) or int(Cab_D11) or int(CAS_S12) or int(CAD_S12))*1
				#Trace.Write('Qty_45657 :'+str(Qty_45657))
				Qty_456572= (int(CBD_S01) or int(CBD_D01) or int(Cab_100) or int(Cab_200) or int(Cab_300) or int(Cab_400) or int(Cab_500) or int(Cab_600) or int(Cab_S11) or int(Cab_D11) or int(CAS_S12) or int(CAD_S12))*1
				#Trace.Write('Qty_456572 :'+str(Qty_456572))
	return Qty_45657,Qty_456572
#FinalQty = C300_Cabinet5(Product)
#Trace.Write('FinalQty : ' + str(FinalQty))

#CXCPQ-45708
def C300_Cabinet6(Product,QTY_A,QTY_D):
	Cab_300=QTY_A
	Trace.Write('Cab_300 :'+str(Cab_300))
	Cab_400=QTY_D
	Trace.Write('Cab_400 :'+str(Cab_400))
	Qty_45708=0
	Qty_457082=0
	if Product.Name=="Series-C Control Group":
		family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
		mounting_sol=Product.Attr('SerC_CG_IO_Mounting_Solution').GetValue()
		mounting_panel=Product.Attr('SerC_CG_Mounting_Panel_Type').GetValue()
		Terminal_side=Product.Attr('SerC_CG_Terminal_Block_Mounting_Side').GetValue()
		
		if family!='Series C' and mounting_sol!='Mounting Panel' and (mounting_panel!='2 Column Wide Full Size' or mounting_panel!='2 Column Wide Half Size') and (Terminal_side!='Right' or Terminal_side!='Left'):
			return 0,0
		if family=="Series C":
			if mounting_sol=='Mounting Panel' and mounting_panel=='2 Column Wide Full Size' and Terminal_side=='Right':
				Qty_45708= int(Cab_300)*1
				Trace.Write('Qty_45708 :'+str(Qty_45708))
			if mounting_sol=='Mounting Panel' and mounting_panel=='2 Column Wide Full Size' and Terminal_side=='Left':
				Qty_457082= int(Cab_300)*1
				Trace.Write('Qty_457082 :'+str(Qty_457082))
			if mounting_sol=='Mounting Panel' and mounting_panel=='2 Column Wide Half Size' and Terminal_side=='Right':
				Qty_45708= int(Cab_400)*1
				Trace.Write('Qty_45708 :'+str(Qty_45708))
			if mounting_sol=='Mounting Panel' and mounting_panel=='2 Column Wide Half Size' and Terminal_side=='Left':
				Qty_457082= int(Cab_400)*1
				Trace.Write('Qty_457082 :'+str(Qty_457082))
	elif Product.Name=="Series-C Remote Group":
		family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
		mounting_sol=Product.Attr('SerC_IO_Mounting_Solution').GetValue()
		mounting_panel=Product.Attr('Ser_C_RG_Mounting_Panel_Type').GetValue()
		Terminal_side=Product.Attr('SerC_RG_TerminalBlockMounting_Side_For_MountingPnl').GetValue()
		
		if family!='Series C' and mounting_sol!='Mounting Panel' and (mounting_panel!='2 Column Wide Full Size' or mounting_panel!='2 Column Wide Half Size') and (Terminal_side!='Right' or Terminal_side!='Left'):
			return 0,0
		if family=="Series C":
			if mounting_sol=='Mounting Panel' and mounting_panel=='2 Column Wide Full Size' and Terminal_side=='Right':
				Qty_45708= (int(Cab_300))*1
				Trace.Write('Qty_45708 :'+str(Qty_45708))
			if mounting_sol=='Mounting Panel' and mounting_panel=='2 Column Wide Full Size' and Terminal_side=='Left':
				Qty_457082= (int(Cab_300))*1
				Trace.Write('Qty_457082 :'+str(Qty_457082))
			if mounting_sol=='Mounting Panel' and mounting_panel=='2 Column Wide Half Size' and Terminal_side=='Right':
				Qty_45708= (int(Cab_400))*1
				Trace.Write('Qty_45708 :'+str(Qty_45708))
			if mounting_sol=='Mounting Panel' and mounting_panel=='2 Column Wide Half Size' and Terminal_side=='Left':
				Qty_457082= (int(Cab_400))*1
				Trace.Write('Qty_457082 :'+str(Qty_457082))
	return Qty_45708,Qty_457082
#FinalQty = C300_Cabinet6(Product,QTY_A,QTY_D)
#Trace.Write('FinalQty : ' + str(FinalQty))

#CXCPQ-35487
def C300_Cabinet7(Product):
	CADS11,part600,part400,part500,CBDS01,CASS12,part200,CASS11,part300,part100,CBDD01,CADS12,X,Y,Z,K,L,C1,C2,C3,C4,C8SS01=GS_C300_MCAR_calcs.cab_c(Product) #CXCPQ-116603
	CASS= int(GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','CASS'))
	CADS= int(GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','CADS'))
	CBD_S01=CBDS01 or C8SS01
	Trace.Write('CBD_S01 :'+str(CBD_S01))
	Cab_300=part300
	Trace.Write('Cab_300 :'+str(Cab_300))
	Cab_S11=CASS
	Trace.Write('Cab_S11 :'+str(Cab_S11))
	Cab_600=part600
	Trace.Write('Cab_600 :'+str(Cab_600))
	Cab_200=part200
	Trace.Write('Cab_200 :'+str(Cab_200))
	Cab_100=part100
	Trace.Write('Cab_100 :'+str(Cab_100))
	Cab_D11=CADS
	Trace.Write('Cab_D11 :'+str(Cab_D11))
	Cab_400=part400
	Trace.Write('Cab_400 :'+str(Cab_400))
	Cab_500=part500
	Trace.Write('Cab_500 :'+str(Cab_500))
	CAS_S12=CASS12
	CAD_S12=CADS12
	Qty_35487=0
	
	if Product.Name=="Series-C Control Group":
		family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
		mounting_sol=Product.Attr('SerC_CG_IO_Mounting_Solution').GetValue()
		cab_ac=Product.Attr('SerC_CG_Cabinet_Access').GetValue()
		cab_typ=Product.Attr('SerC_CG_Cabinet_Type_03').GetValue()
		cab_light=Product.Attr('SerC_CG_Cabinet_Light_Default').GetValue()
		CBD_D01 = int(GS_Get_Set_AtvQty.getAtvQty(Product,'Series_C_CG_Part_Summary','CC-C8DS01')) if CBDD01 == 0 else CBDD01
		Trace.Write('CBD_D01 :'+str(CBD_D01))

		if family=="Series C":
			if mounting_sol=='Cabinet' and cab_ac=='Single Access' and cab_typ in ['Normal Cabinet','Alternate Cabinet','Generic Cabinet'] and cab_light=='Yes':
				Qty_35487= (int(CBD_S01) or int(Cab_300) or int(Cab_S11) or int(Cab_600) or int(CAS_S12))*1
				Trace.Write('Qty_35487 :'+str(Qty_35487))
			elif mounting_sol=='Cabinet' and cab_ac=='Dual Access' and cab_typ in ['Normal Cabinet','Alternate Cabinet','Generic Cabinet'] and cab_light=='Yes':
				Qty_35487= (int(CBD_D01) or int(Cab_100) or int(Cab_200) or int(Cab_D11) or int(Cab_400) or int(Cab_500) or int(CAD_S12))* 2
				Trace.Write('Qty_35487 :'+str(Qty_35487))

	elif Product.Name=="Series-C Remote Group":
		family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
		mounting_sol=Product.Attr('SerC_IO_Mounting_Solution').GetValue()
		cab_ac=Product.Attr('SerC_RG_Cabinet_Access').GetValue()
		cab_typ=Product.Attr('SerC_RG_Cabinet_Type').GetValue()
		cab_light=Product.Attr('SerC_RG_Cabinet_Light_Default').GetValue()
		CBD_D01 = int(GS_Get_Set_AtvQty.getAtvQty(Product,'Series_C_RG_Part_Summary','CC-C8DS01')) if CBDD01 == 0 else CBDD01
		Trace.Write('CBD_D01 :'+str(CBD_D01))

		if family=="Series C":
			if mounting_sol=='Cabinet' and cab_ac=='Single Access' and cab_typ in ['Normal Cabinet','Alternate Cabinet','Generic Cabinet'] and cab_light=='Yes':
				Qty_35487= (int(CBD_S01) or int(Cab_300) or int(Cab_S11) or int(Cab_600) or int(CAS_S12))*1
				Trace.Write('Qty_35487 :'+str(Qty_35487))
			elif mounting_sol=='Cabinet' and cab_ac=='Dual Access' and cab_typ in ['Normal Cabinet','Alternate Cabinet','Generic Cabinet'] and cab_light=='Yes':
				Qty_35487= (int(CBD_D01) or int(Cab_100) or int(Cab_200) or int(Cab_D11) or int(Cab_400) or int(Cab_500) or int(CAD_S12))* 2
				Trace.Write('Qty_35487 :'+str(Qty_35487))
	return Qty_35487
#FinalQty = C300_Cabinet7(Product)
#Trace.Write('FinalQty : ' + str(FinalQty))

#CXCPQ-47590
def C300_Cabinet8(Product):
	CADS11,part600,part400,part500,CBDS01,CASS12,part200,CASS11,part300,part100,CBDD01,CADS12,X,Y,Z,K,L,C1,C2,C3,C4,C8SS01=GS_C300_MCAR_calcs.cab_c(Product) #CXCPQ-116603
	CASS= int(GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','CASS'))
	CADS= int(GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','CADS'))
	Cab_S11=CASS
	Trace.Write('Cab_S11 :'+str(Cab_S11))
	Cab_D11=CADS
	Trace.Write('Cab_D11 :'+str(Cab_D11))
	Cab_600=part600
	Trace.Write('Cab_600 :'+str(Cab_600))
	Cab_400=part400
	Trace.Write('Cab_400 :'+str(Cab_400))
	Cab_500=part500
	Trace.Write('Cab_500 :'+str(Cab_500))
	Qty_47590=0
	Qty_475902=0
	Qty_475903=0
	Qty_475904=0
	if Product.Name=="Series-C Control Group":
		family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
		mounting_sol=Product.Attr('SerC_CG_IO_Mounting_Solution').GetValue()
		cab_ac=Product.Attr('SerC_CG_Cabinet_Access').GetValue()
		cab_typ=Product.Attr('SerC_CG_Cabinet_Type_03').GetValue()
		cab_plinth=Product.Attr('SerC_CG_Cabinet_Base_(Plinth)').GetValue()
		cab_base=Product.Attr('SerC_CG_Cabinet_Base_Size').GetValue()

		if family=="Series C":
			if mounting_sol=='Cabinet' and cab_ac=='Single Access' and cab_typ=='Alternate Cabinet' and cab_plinth=='Yes' and cab_base=='100mm':
				Qty_47590= (int(Cab_S11) or int(Cab_600))*1
				Trace.Write('Qty_47590_186-200 :'+str(Qty_47590))
			if mounting_sol=='Cabinet' and cab_ac=='Single Access' and cab_typ=='Alternate Cabinet' and cab_plinth=='Yes' and cab_base=='200mm':
				Qty_475902= (int(Cab_S11) or int(Cab_600))*1
				Trace.Write('Qty_475902_187-200 :'+str(Qty_475902))
			if mounting_sol=='Cabinet' and cab_ac=='Dual Access' and cab_typ=='Alternate Cabinet' and cab_plinth=='Yes' and cab_base=='100mm':
				Qty_475903= (int(Cab_D11) or int(Cab_400) or int(Cab_500))*1
				Trace.Write('Qty_475903_186-100 :'+str(Qty_475903))
			if mounting_sol=='Cabinet' and cab_ac=='Dual Access' and cab_typ=='Alternate Cabinet' and cab_plinth=='Yes' and cab_base=='200mm':
				Qty_475904= (int(Cab_D11) or int(Cab_400) or int(Cab_500))*1
				Trace.Write('Qty_475904_187-100 :'+str(Qty_475904))
	elif Product.Name=="Series-C Remote Group":
		family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
		mounting_sol=Product.Attr('SerC_IO_Mounting_Solution').GetValue()
		cab_ac=Product.Attr('SerC_RG_Cabinet_Access').GetValue()
		cab_typ=Product.Attr('SerC_RG_Cabinet_Type').GetValue()
		cab_plinth=Product.Attr('SerC_RG_Cabinet_Base_(Plinth)').GetValue()
		cab_base=Product.Attr('SerC_RG_Cabinet_Base_Size').GetValue()

		if family=="Series C":
			if mounting_sol=='Cabinet' and cab_ac=='Single Access' and cab_typ=='Alternate Cabinet' and cab_plinth=='Yes' and cab_base=='100mm':
				Qty_47590= (int(Cab_S11) or int(Cab_600))*1
				Trace.Write('Qty_47590_186-200 :'+str(Qty_47590))
			if mounting_sol=='Cabinet' and cab_ac=='Single Access' and cab_typ=='Alternate Cabinet' and cab_plinth=='Yes' and cab_base=='200mm':
				Qty_475902= (int(Cab_S11) or int(Cab_600))*1
				Trace.Write('Qty_475902_187-200 :'+str(Qty_475902))
			if mounting_sol=='Cabinet' and cab_ac=='Dual Access' and cab_typ=='Alternate Cabinet' and cab_plinth=='Yes' and cab_base=='100mm':
				Qty_475903= (int(Cab_D11) or int(Cab_400) or int(Cab_500))*1
				Trace.Write('Qty_475903_186-100 :'+str(Qty_475903))
			if mounting_sol=='Cabinet' and cab_ac=='Dual Access' and cab_typ=='Alternate Cabinet' and cab_plinth=='Yes' and cab_base=='200mm':
				Qty_475904= (int(Cab_D11) or int(Cab_400) or int(Cab_500))*1
				Trace.Write('Qty_475904_187-100 :'+str(Qty_475904))
	return Qty_47590,Qty_475902,Qty_475903,Qty_475904
#FinalQty = C300_Cabinet8(Product)
#Trace.Write('FinalQty : ' + str(FinalQty))