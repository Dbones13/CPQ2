#45842 By Shivani Kothari
def getC300UpsCals(Product):
	Specify_id=Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
	id_modifier=Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
	cab_cnt=Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
	LLAI_cnt=Product.Attr('C300_RG_UPC_LLAI_Count').GetValue()
	var=0
	if Specify_id=='Yes' and len(id_modifier)>16:
		if id_modifier[16]=='5'or id_modifier[16]=='6'or id_modifier[16]=='7'or id_modifier[16]=='8':
			var=int(cab_cnt)*1
	if Specify_id=='No':
		if LLAI_cnt=='5' or LLAI_cnt=='6' or  LLAI_cnt=='7'	 or LLAI_cnt=='8' :
			var=int(cab_cnt)*1
	return var
#45051 
def getC30UpsCals_50159943_003(Product):
	Specify_id=Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
	id_modifier=Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
	cab_cnt=Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
	FTA=Product.Attr('C300_RG_UPC_FTA').GetValue()
	var=0
	if Specify_id=='Yes'and len(id_modifier)>14:
		if (id_modifier[12]=='N'and id_modifier[13]=='0'and id_modifier[14]=='0')or (id_modifier[12]=='N' and id_modifier[13]=='0' and id_modifier[14]=='2') or (id_modifier[12]=='N' and id_modifier[13]=='0' and id_modifier[14]=='4')or (id_modifier[12]=='N' and id_modifier[13]=='0' and id_modifier[14]=='6') or (id_modifier[12]=='N' and id_modifier[13]=='2' and id_modifier[14]=='0')or (id_modifier[12]=='N' and id_modifier[13]=='2' and id_modifier[14]=='2') or (id_modifier[12]=='N' and id_modifier[13]=='2' and id_modifier[14]=='4')or (id_modifier[12]=='N' and id_modifier[13]=='2' and id_modifier[14]=='6') or (id_modifier[12]=='N' and id_modifier[13]=='4' and id_modifier[14]=='0')or (id_modifier[12]=='N' and id_modifier[13]=='4' and id_modifier[14]=='2') :
			var=int(cab_cnt)*1
		if (id_modifier[12]=='N' and id_modifier[13]=='4' and id_modifier[14]=='4')or (id_modifier[12]=='N' and id_modifier[13]=='4'and id_modifier[14]=='6') or (id_modifier[12]=='N' and id_modifier[13]=='6' and id_modifier[14]=='0')or (id_modifier[12]=='N' and id_modifier[13]=='6' and id_modifier[14]=='2') or (id_modifier[12]=='N' and id_modifier[13]=='6' and id_modifier[14]=='4')or (id_modifier[12]=='N' and id_modifier[13]=='6' and id_modifier[14]=='6') or (id_modifier[12]=='G' and id_modifier[13]=='0')or (id_modifier[12]=='G' and id_modifier[13]=='2') or (id_modifier[12]=='G' and id_modifier[13]=='4')or (id_modifier[12]=='G' and id_modifier[13]=='6'):
			var=int(cab_cnt)*1
	if Specify_id=='No':
		if FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' or FTA=='Universal Marshalling, GI only (0-6)' :
			var=int(cab_cnt)*1
	Trace.Write("var= "+str(var))
	return var
#45306
def get50182312_001(Product):
	Specify_id=Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
	id_modifier=Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
	cab_cnt=Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
	CN_Hive=Product.Attr('C300_RG_UPC_CN100_IO_HIVE').GetValue()
	CNM=Product.Attr('C300_RG_UPC_CNM').GetValue()
	CNM_Module=Product.Attr('C300_RG_UPC_CNM_Exp_Module').GetValue()
	Uplink_sfp=Product.Attr('C300_RG_UPC_CNM_Uplink_SFP_Type').GetValue()
	var=0
	if Specify_id=='Yes' and len(id_modifier)>9:
		if (id_modifier[4]=='H'and id_modifier[7]=='Y'and id_modifier[8]=='Y'and id_modifier[9]=='C') or (id_modifier[4]=='R'and id_modifier[7]=='Y'and id_modifier[8]=='Y'and id_modifier[9]=='C') or (id_modifier[4]=='A'and id_modifier[7]=='Y'and id_modifier[8]=='Y'and id_modifier[9]=='C') or (id_modifier[4]=='B'and id_modifier[7]=='Y'and id_modifier[8]=='Y'and id_modifier[9]=='C') or (id_modifier[4]=='H'and id_modifier[7]=='Y'and id_modifier[8]=='N'and id_modifier[9]=='C')or (id_modifier[4]=='R'and id_modifier[7]=='Y'and id_modifier[8]=='N'and id_modifier[9]=='C')or (id_modifier[4]=='A'and id_modifier[7]=='Y'and id_modifier[8]=='N'and id_modifier[9]=='C') or (id_modifier[4]=='B'and id_modifier[7]=='Y'and id_modifier[8]=='N'and id_modifier[9]=='C'):
			var=int(cab_cnt)*2
	if Specify_id=='No':
		if (CN_Hive=="Non-Redundant with SM SFP" and CNM=="Red Pair CNM" and CNM_Module=="No Expansion Module" and Uplink_sfp=="Red Pair CNM with SM 1G SFP, 10Km") or (CN_Hive=="Redundant with SM SFP" and CNM=="Red Pair CNM" and CNM_Module=="No Expansion Module" and Uplink_sfp=="Red Pair CNM with SM 1G SFP, 10Km") or (CN_Hive=="Non-Redundant" and CNM=="Red Pair CNM" and CNM_Module=="No Expansion Module" and Uplink_sfp=="Red Pair CNM with SM 1G SFP, 10Km") or (CN_Hive=="Redundant" and CNM=="Red Pair CNM" and CNM_Module=="No Expansion Module" and Uplink_sfp=="Red Pair CNM with SM 1G SFP, 10Km") or (CN_Hive=="Non-Redundant with SM SFP" and CNM=="Red Pair CNM" and CNM_Module=="2x Expansion Modules" and Uplink_sfp=="Red Pair CNM with SM 1G SFP, 10Km") or (CN_Hive=="Redundant with SM SFP" and CNM=="Red Pair CNM" and CNM_Module=="2x Expansion Modules" and Uplink_sfp=="Red Pair CNM with SM 1G SFP, 10Km") or (CN_Hive=="Non-Redundant" and CNM=="Red Pair CNM" and CNM_Module=="2x Expansion Modules" and Uplink_sfp=="Red Pair CNM with SM 1G SFP, 10Km") or (CN_Hive=="Redundant" and CNM=="Red Pair CNM" and CNM_Module=="2x Expansion Modules" and Uplink_sfp=="Red Pair CNM with SM 1G SFP, 10Km")	 :
			var=int(cab_cnt)*2
	return var
#46094
def getCCI_HSC(Product):
	Specify_id=Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
	id_modifier=Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
	cab_cnt=Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
	CN_Hive=Product.Attr('C300_RG_UPC_CN100_IO_HIVE').GetValue()
	CNM=Product.Attr('C300_RG_UPC_CNM').GetValue()
	CNM_Module=Product.Attr('C300_RG_UPC_CNM_Exp_Module').GetValue()
	Uplink_sfp=Product.Attr('C300_RG_UPC_CNM_Uplink_SFP_Type').GetValue()
	
	
	var=0
	if Specify_id=='Yes' and len(id_modifier)>7:
		if (id_modifier[4]=='H'and id_modifier[7]=='Y') or (id_modifier[4]=='M'and id_modifier[7]=='Y') or (id_modifier[4]=='A'and id_modifier[7]=='Y') or (id_modifier[4]=='R'and id_modifier[7]=='Y') or (id_modifier[4]=='T'and id_modifier[7]=='Y') or (id_modifier[4]=='B'and id_modifier[7]=='Y') :
			var=int(cab_cnt)*1
	if Specify_id=='No':
		if (CN_Hive=="Non-Redundant with SM SFP" and CNM=="Red Pair CNM") or(CN_Hive=="Redundant with SM SFP" and CNM=="Red Pair CNM") or (CN_Hive=="Non-Redundant" and CNM=="Red Pair CNM") or (CN_Hive=="Non-Redundant with MM SFP" and CNM=="Red Pair CNM") or (CN_Hive=="Redundant with MM SFP" and CNM=="Red Pair CNM") or (CN_Hive=="Redundant" and CNM=="Red Pair CNM"):
			var=int(cab_cnt)*1
	return var

#CXCPQ-46123 by Ravika Pupneja
def getC300UpsCals_CCTION13(Product):
	Specify_id=Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
	id_modifier=Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
	cab_cnt=Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
	CN100=Product.Attr('C300_RG_UPC_CN100_IO_HIVE').GetValue()
	qty=0
	if Specify_id=='Yes' and len(id_modifier)> 4:
		if id_modifier[4]=='H' or id_modifier[4]=='M' or id_modifier[4]=='A' or id_modifier[4]=='R' or id_modifier[4]=='T' or id_modifier[4]=='B':
			qty=int(cab_cnt)*1
	if Specify_id=='No':
		if CN100=='Non-Redundant with SM SFP' or CN100=='Non-Redundant with MM SFP' or	CN100=='Non-Redundant'	or CN100=='Redundant with SM SFP' or CN100=='Redundant with MM SFP'or CN100=='Redundant':
			qty=int(cab_cnt)*1
	return qty


def getC300UpsCals_CCPEIM01(Product):

	Specify_id=Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
	id_modifier=Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
	cab_cnt=Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
	CN100=Product.Attr('C300_RG_UPC_CN100_IO_HIVE').GetValue()
	CNM=Product.Attr('C300_RG_UPC_CNM').GetValue()
	EIM=Product.Attr('C300_RG_UPC_EIM').GetValue()
	
	qty=0
	if Specify_id=='Yes' and len(id_modifier)> 10:
		if (id_modifier[4] == 'H'and id_modifier[7] == 'Y' and id_modifier[10] == 'Y') or (id_modifier[4]== 'M' and id_modifier[7] == 'Y' and id_modifier[10] == 'Y') or (id_modifier[4] == 'A'and id_modifier[7] == 'Y' and id_modifier[10] == 'Y') or (id_modifier[4] == 'R' and id_modifier[7] == 'Y' and id_modifier[10] == 'Y') or (id_modifier[4] == 'T' and id_modifier[7] == 'Y' and id_modifier[10] == 'Y') or (id_modifier[4] == 'B' and id_modifier[7] == 'Y' and id_modifier[10] == 'Y'):
			qty=int(cab_cnt)*2
	if Specify_id=='No':
		if (CN100 == 'Non-Redundant with SM SFP' and CNM == 'Red Pair CNM' and EIM == 'Yes, Red pair EIM') or (CN100 == 'Non-Redundant with MM SFP' and CNM == 'Red Pair CNM' and EIM == 'Yes, Red pair EIM')or (CN100 == 'Non-Redundant' and CNM =='Red Pair CNM' and EIM == 'Yes, Red pair EIM') or (CN100=='Redundant with SM SFP' and CNM =='Red Pair CNM' and EIM == 'Yes, Red pair EIM') or (CN100 =='Redundant with MM SFP'and CNM =='Red Pair CNM' and EIM == 'Yes, Red pair EIM') or (CN100 == 'Redundant'and CNM == 'Red Pair CNM' and EIM == 'Yes, Red pair EIM'):
			qty=int(cab_cnt)*2
	return qty


def getC300UpsCals_CCMCC003(Product):

	Specify_id=Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
	id_modifier=Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
	cab_cnt=Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
	UIO_Cnt=Product.Attr('C300_RG_UPC_Universal_IO_Count').GetValue()
	UIO2_Red=Product.Attr('C300_RG_UPC_UIO2_Redundancy').GetValue()

	qty=0
	i,j= 14,15

	if len(id_modifier)==26:
		i,j=15,16
	if len(id_modifier)==27:
		i,j=16,17

	if Specify_id=='Yes' and len(id_modifier)> 15:
			if (id_modifier[i] == '3' and id_modifier[j] == 'R'):
				qty=int(cab_cnt)*8
			if (id_modifier[i] == '3' and id_modifier[j]== 'N'):
				qty=int(cab_cnt)*9
			if (id_modifier[i] == '6' and id_modifier[j]== 'R'):
				qty=int(cab_cnt)*4
			if (id_modifier[i] == '6' and id_modifier[j]== 'N'):
				qty=int(cab_cnt)*6
			if (id_modifier[i] == '9' and id_modifier[j]== 'N'):
				qty=int(cab_cnt)*3

	if Specify_id=='No':
		if (UIO_Cnt == '32' and UIO2_Red == 'Redundant'):
			qty=int(cab_cnt)*8
		if (UIO_Cnt == '32' and UIO2_Red == 'Non-Redundant'):
			qty=int(cab_cnt)*9
		if (UIO_Cnt == '64' and UIO2_Red == 'Redundant'):
			qty=int(cab_cnt)*4
		if (UIO_Cnt == '64' and UIO2_Red == 'Non-Redundant'):
			qty=int(cab_cnt)*6
		if (UIO_Cnt == '96' and UIO2_Red == 'Non-Redundant'):
			qty=int(cab_cnt)*3
		
	return qty

def getC300UpsCals_CCINWE01(Product):

	Specify_id=Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
	id_modifier=Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
	cab_cnt=Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
	CN100=Product.Attr('C300_RG_UPC_CN100_IO_HIVE').GetValue()
	CNM=Product.Attr('C300_RG_UPC_CNM').GetValue()
	CNM_Exp=Product.Attr('C300_RG_UPC_CNM_Exp_Module').GetValue()
	
	qty=0
	if Specify_id=='Yes' and len(id_modifier)> 8 :
		if (id_modifier[4] == 'H'and id_modifier[7] == 'Y' and id_modifier[8] == 'Y') or (id_modifier[4]== 'M' and id_modifier[7] == 'Y' and id_modifier[8] == 'Y') or (id_modifier[4] == 'A'and id_modifier[7] == 'Y' and id_modifier[8] == 'Y') or (id_modifier[4] == 'R' and id_modifier[7] == 'Y' and id_modifier[8] == 'Y') or (id_modifier[4] == 'T' and id_modifier[7] == 'Y' and id_modifier[8] == 'Y') or (id_modifier[4] == 'B' and id_modifier[7] == 'Y' and id_modifier[8] == 'Y'):
			qty=int(cab_cnt)*2
	if Specify_id=='No':
		if (CN100 == 'Non-Redundant with SM SFP' and CNM == 'Red Pair CNM' and CNM_Exp == '2x Expansion Modules') or (CN100 == 'Non-Redundant with MM SFP' and CNM == 'Red Pair CNM' and CNM_Exp == '2x Expansion Modules')or (CN100 == 'Non-Redundant' and CNM =='Red Pair CNM' and CNM_Exp == '2x Expansion Modules') or (CN100=='Redundant with SM SFP' and CNM =='Red Pair CNM' and CNM_Exp == '2x Expansion Modules') or (CN100 =='Redundant with MM SFP'and CNM =='Red Pair CNM' and CNM_Exp == '2x Expansion Modules') or (CN100 == 'Redundant'and CNM == 'Red Pair CNM' and CNM_Exp == '2x Expansion Modules'):
			qty=int(cab_cnt)*2
	return qty

#1K. #CXCPQ-46120
def getC300UPC_46120(Product):
	MIB = Product.Attr('MIB Configuration Required?').GetValue()
	IO_Family = Product.Attr('SerC_CG_IO_Family_Type').GetValue()
	IO_Mount = Product.Attr('SerC_IO_Mounting_Solution').GetValue()
	ID_Specify = Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
	ID_Modify = Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
	Num_Cabinet = Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
	STT_count = Product.Attr('C300_RG_UPC_STT650_Count').GetValue()
	#CXCPQ-46120
	val_1=0
	i=17
	if len(ID_Modify)>25:
		i= 18
	if len(ID_Modify)>26:
		i=19
	
	if ID_Specify=='Yes' and len(ID_Modify)> 17:
		if ID_Modify[i]=='1':
			val_1=int(Num_Cabinet) * 1
	elif ID_Specify=='No':
		if STT_count=='1':
			val_1=int(Num_Cabinet) * 1
	return int(val_1)

#2K. #CXCPQ-45380 and CXCPQ-64023
def getC300UPC_45380(Product):
	MIB = Product.Attr('MIB Configuration Required?').GetValue()
	IO_Family = Product.Attr('SerC_CG_IO_Family_Type').GetValue()
	IO_Mount = Product.Attr('SerC_IO_Mounting_Solution').GetValue()
	ID_Specify = Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
	ID_Modify = Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
	Num_Cabinet = Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
	Supply_Type = Product.Attr('C300_RG_UPC_Pwr_Supp_Type').GetValue()
	val_2=0
	i=19
	if len(ID_Modify)>25:
		i= 20
	if len(ID_Modify)>26:
		i=21
	if ID_Specify=='Yes' and len(ID_Modify)> 19:
		if ID_Modify[i]=='A' or ID_Modify[i]=='R' or ID_Modify[i]=='Q':
			val_2=int(Num_Cabinet) * 1
	elif ID_Specify=='No':
		if Supply_Type=="20A AC/DC QUINT4+ Supply" or Supply_Type=="25A AC/DC ATDI Supply" or Supply_Type=="20A AC/DC ATDI Supply – Rack Mount":
			val_2=int(Num_Cabinet) * 1
	return int(val_2)

#3K. #CXCPQ-46096
def getC300UPC_46096(Product):
	MIB = Product.Attr('MIB Configuration Required?').GetValue()
	IO_Family = Product.Attr('SerC_CG_IO_Family_Type').GetValue()
	IO_Mount = Product.Attr('SerC_IO_Mounting_Solution').GetValue()
	ID_Specify = Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
	ID_Modify = Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
	Num_Cabinet = Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
	IO_Lice = Product.Attr('C300_RG_UPC_Controlled_IO_License_Count').GetValue()
	val_3=0
	i=23
	if len(ID_Modify)>25:
		i= 24
	if len(ID_Modify)>26:
		i=25
	
	if ID_Specify=='Yes' and len(ID_Modify)> 23:
		if ID_Modify[i]=='2':
			val_3=int(Num_Cabinet) * 1
			Trace.Write("val_3 :" +str(val_3))
	elif ID_Specify=='No':
		if IO_Lice=="240 IO Control":
			val_3=int(Num_Cabinet) * 1
			Trace.Write("val_3 :" +str(val_3))
	return int(val_3)

#4K. #CXCPQ-43821
def getC300UPC_43821(Product):
	MIB = Product.Attr('MIB Configuration Required?').GetValue()
	IO_Family = Product.Attr('SerC_CG_IO_Family_Type').GetValue()
	IO_Mount = Product.Attr('SerC_IO_Mounting_Solution').GetValue()
	ID_Specify = Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
	ID_Modify = Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
	Num_Cabinet = Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
	Supply_Type = Product.Attr('C300_RG_UPC_Pwr_Supp_Type').GetValue()	#CXCPQ-45380 and #CXCPQ-43821
	Supply_Red = Product.Attr('C300_RG_UPC_Pwr_Supp_Red').GetValue()
	val_4=0
	i,j=19,20
	if len(ID_Modify)>25:
		i,j= 20,21
	if len(ID_Modify)>26:
		i,j=21,22
	if ID_Specify=='Yes' and len(ID_Modify)> 20:
		if ID_Modify[i]=='D' and ID_Modify[j]=='R':
			val_4=int(Num_Cabinet) * 1
			Trace.Write("val_4 :" +str(val_4))
	elif ID_Specify=='No':
		if Supply_Type=="20A DC/DC QUINT4+ Supply" and Supply_Red=="REDUNDANT":
			val_4=int(Num_Cabinet) * 1
	return int(val_4)

#5K. #CXCPQ-46097
def getC300UPC_46097(Product):
	MIB = Product.Attr('MIB Configuration Required?').GetValue()
	IO_Family = Product.Attr('SerC_CG_IO_Family_Type').GetValue()
	IO_Mount = Product.Attr('SerC_IO_Mounting_Solution').GetValue()
	ID_Specify = Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
	ID_Modify = Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
	Num_Cabinet = Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
	IO_Lice = Product.Attr('C300_RG_UPC_Controlled_IO_License_Count').GetValue()
	val_5=0
	i=23
	if len(ID_Modify)>25:
		i= 24
	if len(ID_Modify)>26:
		i=25
	if ID_Specify=='Yes' and len(ID_Modify)> 23:
		if ID_Modify[i]=='8':
			val_5=int(Num_Cabinet) * 1
	elif ID_Specify=='No':
		if IO_Lice=="800 IO Control":
			val_5=int(Num_Cabinet) * 1
	return int(val_5)

#6K. #CXCPQ-46087
def getC300UPC_46087(Product):
	MIB = Product.Attr('MIB Configuration Required?').GetValue()
	IO_Family = Product.Attr('SerC_CG_IO_Family_Type').GetValue()
	IO_Mount = Product.Attr('SerC_IO_Mounting_Solution').GetValue()
	ID_Specify = Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
	ID_Modify = Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
	Num_Cabinet = Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
	Uni_Count = Product.Attr('C300_RG_UPC_Universal_IO_Count').GetValue()
	UIO_Red = Product.Attr('C300_RG_UPC_UIO2_Redundancy').GetValue()
	val_6=0
	i,j=14,15
	if len(ID_Modify)>25:
		i,j= 15,16
	if len(ID_Modify)>26:
		i,j=16,17
	
	if ID_Specify=='Yes' and len(ID_Modify)> 15:
		if ID_Modify[i]=='3' and ID_Modify[j]=='R':
			val_6=int(Num_Cabinet) * 1
			Trace.Write("val_6 :" +str(val_6))
		elif ID_Modify[i]=='6' and ID_Modify[j]=='R':
			val_6=int(Num_Cabinet) * 2
			Trace.Write("val_6 :" +str(val_6))
		elif ID_Modify[i]=='9' and ID_Modify[j]=='R':
			val_6=int(Num_Cabinet) * 3
			Trace.Write("val_6 :" +str(val_6))
	elif ID_Specify=='No':
		if Uni_Count=="32" and UIO_Red=="Redundant":
			val_6=int(Num_Cabinet) * 1
		elif Uni_Count=="64" and UIO_Red=="Redundant":
			val_6=int(Num_Cabinet) * 2
		elif Uni_Count=="96" and UIO_Red=="Redundant":
			val_6=int(Num_Cabinet) * 3
			Trace.Write("val_6 :" +str(val_6))
			
	return int(val_6)

#7K. #CXCPQ-45315
def getC300UPC_45315(Product):
	MIB = Product.Attr('MIB Configuration Required?').GetValue()
	IO_Family = Product.Attr('SerC_CG_IO_Family_Type').GetValue()
	IO_Mount = Product.Attr('SerC_IO_Mounting_Solution').GetValue()
	ID_Specify = Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
	ID_Modify = Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
	Num_Cabinet = Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
	Cab_type=Product.Attr('C300_RG_UPC_Cab_Mat_Type').GetValue()
	Ambient_temp = Product.Attr('C300_RG_UPC_Ambient_Temp_Range').GetValue()
	Supply_Type = Product.Attr('C300_RG_UPC_Pwr_Supp_Type').GetValue()
	Supply_Red = Product.Attr('C300_RG_UPC_Pwr_Supp_Red').GetValue()
	FTA=Product.Attr('C300_RG_UPC_FTA').GetValue()
	AbuD_Loc = Product.Attr('C300_RG_UPC_Abu_Dhabi_Bld_Loc').GetValue()
	val_7=0
	i,j,k=19,20,24
	if len(ID_Modify)>24:
		i,j,k= 19,20,24
	if len(ID_Modify)>25:
		i,j,k= 20,21,25
	if len(ID_Modify)>26:
		i,j,k=21,22,26
	
	if ID_Specify=='Yes' and len(ID_Modify)> 24:
		if ID_Modify[1]=='S':
			if ID_Modify[2]=='B':
				if ID_Modify[12]=='X' or (ID_Modify[12]=='N' and ID_Modify[13]=='0' and ID_Modify[14]=='0') or (ID_Modify[12]=='N' and ID_Modify[13]=='0' and ID_Modify[14]=='2') or (ID_Modify[12]=='N' and ID_Modify[13]=='0' and ID_Modify[14]=='4') or (ID_Modify[12]=='N' and ID_Modify[13]=='0' and ID_Modify[14]=='6') or (ID_Modify[12]=='G' and ID_Modify[13]=='0') or (ID_Modify[12]=='G' and ID_Modify[13]=='2') or (ID_Modify[12]=='G' and ID_Modify[13]=='4') or (ID_Modify[12]=='G' and ID_Modify[13]=='6'):
					if ID_Modify[i]=='Q':
						if ID_Modify[j]=='R':
							if ID_Modify[k]=='N':
								val_7=int(Num_Cabinet) * 1
								Trace.Write("val_7 :" +str(val_7))
	elif ID_Specify=='No':
		if Cab_type=='Stainless Steel, IP66':
			if Ambient_temp=='With Fan, Max Ambient +55°C':
				if FTA=='No Treatment' or FTA=='Universal Marshalling, GI only (0-6)' or FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)':
					if Supply_Type=='20A AC/DC QUINT4+ Supply':
						if Supply_Red=='REDUNDANT':
							if AbuD_Loc=='No':
								val_7=int(Num_Cabinet) * 1
								Trace.Write("val_7 :" +str(val_7))
	return int(val_7)

#8K. #CXCPQ-45013
def getC300UPC_45013(Product):
	MIB = Product.Attr('MIB Configuration Required?').GetValue()
	IO_Family = Product.Attr('SerC_CG_IO_Family_Type').GetValue()
	IO_Mount = Product.Attr('SerC_IO_Mounting_Solution').GetValue()
	ID_Specify = Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
	ID_Modify = Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
	Num_Cabinet = Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
	CN_IOHive = Product.Attr('C300_RG_UPC_CN100_IO_HIVE').GetValue()
	CNM = Product.Attr('C300_RG_UPC_CNM').GetValue()
	CNM_ExpMod = Product.Attr('C300_RG_UPC_CNM_Exp_Module').GetValue()
	SFP = Product.Attr('C300_RG_UPC_CNM_Uplink_SFP_Type').GetValue()
	#CXCPQ-45013
	
	val_8=0
	
	if ID_Specify=='Yes' and len(ID_Modify)> 9:
		if ID_Modify[4]=='H':
			val_8=int(Num_Cabinet) * 2
		elif ID_Modify[4]=='R':
			val_8=int(Num_Cabinet) * 2
		elif ID_Modify[4]=='A' and ID_Modify[7]=='Y' and ID_Modify[8]=='Y' and ID_Modify[9]=='A':
			val_8=int(Num_Cabinet) * 2
		elif ID_Modify[4]=='B' and ID_Modify[7]=='Y' and ID_Modify[8]=='Y' and ID_Modify[9]=='A':
			val_8=int(Num_Cabinet) * 2
		elif ID_Modify[4]=='A' and ID_Modify[7]=='Y' and ID_Modify[8]=='N' and ID_Modify[9]=='A':
			val_8=int(Num_Cabinet) * 2
		elif ID_Modify[4]=='B' and ID_Modify[7]=='Y' and ID_Modify[8]=='N' and ID_Modify[9]=='A':
			val_8=int(Num_Cabinet) * 2
	elif ID_Specify=='No':
		if CN_IOHive=="Non-Redundant with SM SFP":
			val_8=int(Num_Cabinet) * 2
		elif CN_IOHive=="Redundant with SM SFP":
			val_8=int(Num_Cabinet) * 2
		elif CN_IOHive=="Non-Redundant" and CNM=="Red Pair CNM" and CNM_ExpMod=="No Expansion Module" and SFP=="Red Pair CNM with SM 10/100M SFP, 15Km":
			val_8=int(Num_Cabinet) * 2
		elif CN_IOHive=="Redundant" and CNM=="Red Pair CNM" and CNM_ExpMod=="No Expansion Module" and SFP=="Red Pair CNM with SM 10/100M SFP, 15Km":
			val_8=int(Num_Cabinet) * 2
		elif CN_IOHive=="Non-Redundant" and CNM=="Red Pair CNM" and CNM_ExpMod=="2x Expansion Modules" and SFP=="Red Pair CNM with SM 10/100M SFP, 15Km":
			val_8=int(Num_Cabinet) * 2
		elif CN_IOHive=="Redundant" and CNM=="Red Pair CNM" and CNM_ExpMod=="2x Expansion Modules" and SFP=="Red Pair CNM with SM 10/100M SFP, 15Km":
			val_8=int(Num_Cabinet) * 2
			Trace.Write("val_8 :" +str(val_8))
	return int(val_8)

#9K. #CXCPQ-45335
def getC300UPC_45335(Product):
	MIB = Product.Attr('MIB Configuration Required?').GetValue()
	IO_Family = Product.Attr('SerC_CG_IO_Family_Type').GetValue()
	IO_Mount = Product.Attr('SerC_IO_Mounting_Solution').GetValue()
	ID_Specify = Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
	ID_Modify = Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
	Num_Cabinet = Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
	#CXCPQ-45335
	Cab_type=Product.Attr('C300_RG_UPC_Cab_Mat_Type').GetValue()
	Ambient_temp = Product.Attr('C300_RG_UPC_Ambient_Temp_Range').GetValue()
	Supply_Type = Product.Attr('C300_RG_UPC_Pwr_Supp_Type').GetValue()
	Supply_Red = Product.Attr('C300_RG_UPC_Pwr_Supp_Red').GetValue()
	FTA=Product.Attr('C300_RG_UPC_FTA').GetValue()
	AbuD_Loc = Product.Attr('C300_RG_UPC_Abu_Dhabi_Bld_Loc').GetValue()
	val_9=0
	i,j,k=19,20,24
	if len(ID_Modify)>24:
		i,j,k= 19,20,24
	if len(ID_Modify)>25:
		i,j,k= 20,21,25
	if len(ID_Modify)>26:
		i,j,k=21,22,26
	
	if ID_Specify=='Yes' and len(ID_Modify)> 24:
		if ID_Modify[1]=='S':
			if ID_Modify[2]=='B':
				if ID_Modify[12]=='X' or (ID_Modify[12]=='N' and ID_Modify[13]=='0' and ID_Modify[14]=='0') or (ID_Modify[12]=='N' and ID_Modify[13]=='0' and ID_Modify[14]=='2') or (ID_Modify[12]=='N' and ID_Modify[13]=='0' and ID_Modify[14]=='4') or (ID_Modify[12]=='N' and ID_Modify[13]=='0' and ID_Modify[14]=='6') or (ID_Modify[12]=='G' and ID_Modify[13]=='0') or (ID_Modify[12]=='G' and ID_Modify[13]=='2') or (ID_Modify[12]=='G' and ID_Modify[13]=='4') or (ID_Modify[12]=='G' and ID_Modify[13]=='6'):
					if ID_Modify[i]=='R':
						if ID_Modify[j]=='R':
							if ID_Modify[k]=='Y':
								val_9=int(Num_Cabinet) * 1
								Trace.Write("val_9 :" +str(val_9))
	elif ID_Specify=='No':
		if Cab_type=='Stainless Steel, IP66':
			if Ambient_temp=='With Fan, Max Ambient +55°C':
				if FTA=='No Treatment' or FTA=='Universal Marshalling, GI only (0-6)' or FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)':
					if Supply_Type=='20A AC/DC ATDI Supply – Rack Mount':
						if Supply_Red=='REDUNDANT':
							if AbuD_Loc=='Yes':
								val_9=int(Num_Cabinet) * 1
								Trace.Write("val_9 :" +str(val_9))
	return int(val_9)

#10K. #CXCPQ-45309
def getC300UPC_45309(Product):
	MIB = Product.Attr('MIB Configuration Required?').GetValue()
	IO_Family = Product.Attr('SerC_CG_IO_Family_Type').GetValue()
	IO_Mount = Product.Attr('SerC_IO_Mounting_Solution').GetValue()
	ID_Specify = Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
	ID_Modify = Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
	Num_Cabinet = Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
	#CXCPQ-45309
	Cab_type=Product.Attr('C300_RG_UPC_Cab_Mat_Type').GetValue()
	Ambient_temp = Product.Attr('C300_RG_UPC_Ambient_Temp_Range').GetValue()
	Supply_Type = Product.Attr('C300_RG_UPC_Pwr_Supp_Type').GetValue()
	Supply_Red = Product.Attr('C300_RG_UPC_Pwr_Supp_Red').GetValue()
	FTA=Product.Attr('C300_RG_UPC_FTA').GetValue()
	AbuD_Loc = Product.Attr('C300_RG_UPC_Abu_Dhabi_Bld_Loc').GetValue()
	val_10=0
	i,j,k=19,20,24
	if len(ID_Modify)>24:
		i,j,k= 19,20,24
	if len(ID_Modify)>25:
		i,j,k= 20,21,25
	if len(ID_Modify)>26:
		i,j,k=21,22,26
		
	if ID_Specify=='Yes' and len(ID_Modify)> 24:
		if ID_Modify[1]=='S':
			if ID_Modify[2]=='A':
				if ID_Modify[12]=='X' or (ID_Modify[12]=='N' and ID_Modify[13]=='0' and ID_Modify[14]=='0') or (ID_Modify[12]=='N' and ID_Modify[13]=='0' and ID_Modify[14]=='2') or (ID_Modify[12]=='N' and ID_Modify[13]=='0' and ID_Modify[14]=='4') or (ID_Modify[12]=='N' and ID_Modify[13]=='0' and ID_Modify[14]=='6') or (ID_Modify[12]=='G' and ID_Modify[13]=='0') or (ID_Modify[12]=='G' and ID_Modify[13]=='2') or (ID_Modify[12]=='G' and ID_Modify[13]=='4') or (ID_Modify[12]=='G' and ID_Modify[13]=='6'):
					if ID_Modify[i]=='A':
						if ID_Modify[j]=='R':
							if ID_Modify[k]=='N':
								val_10=int(Num_Cabinet) * 1
								Trace.Write("val_10 :" +str(val_10))
	elif ID_Specify=='No':
		if Cab_type=='Stainless Steel, IP66':
			if Ambient_temp=='Without Fan, Max Ambient +40°C':
				if FTA=='No Treatment' or FTA=='Universal Marshalling, GI only (0-6)' or FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)':
					if Supply_Type=='25A AC/DC ATDI Supply':
						if Supply_Red=='REDUNDANT':
							if AbuD_Loc=='No':
								val_10=int(Num_Cabinet) * 1
								Trace.Write("val_10 :" +str(val_10))
	return int(val_10)
#11K. #CXCPQ-45499
def getC300UPC_45499(Product):
	MIB = Product.Attr('MIB Configuration Required?').GetValue()
	IO_Family = Product.Attr('SerC_CG_IO_Family_Type').GetValue()
	IO_Mount = Product.Attr('SerC_IO_Mounting_Solution').GetValue()
	ID_Specify = Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
	ID_Modify = Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
	Num_Cabinet = Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
	FTA = Product.Attr('C300_RG_UPC_FTA').GetValue()
	GIIS = Product.Attr('C300_RG_UPC_GIIS_Bases_Universal_Marshalling_Count').GetValue()
	Non_GIIS = Product.Attr('C300_RG_UPC_Non_GIIS_Universal_Marshalling_Count').GetValue()
	GI = Product.Attr('C300_RG_UPC_GI_Bases_Universal_Marshalling_Count').GetValue()
	Uni_Count = Product.Attr('C300_RG_UPC_Universal_IO_Count').GetValue()
	val_11=0
	if ID_Specify=='Yes' and len(ID_Modify)> 15:
		if ID_Modify[12]=='G' and ID_Modify[13]=='2' and ID_Modify[15]=='3':
			val_11=int(Num_Cabinet) * 2
		elif ID_Modify[12]=='G' and ID_Modify[13]=='4' and ID_Modify[15]=='6':
			val_11=int(Num_Cabinet) * 4
		elif ID_Modify[12]=='G' and ID_Modify[13]=='6' and ID_Modify[15]=='9':
			val_11=int(Num_Cabinet) * 6
		elif ID_Modify[12]=='N' and ID_Modify[13]=='0' and ID_Modify[14]=='2' and ID_Modify[16]=='3':
			val_11=int(Num_Cabinet) * 2
		elif ID_Modify[12]=='N' and ID_Modify[13]=='0' and ID_Modify[14]=='4' and ID_Modify[16]=='6':
			val_11=int(Num_Cabinet) * 4
		elif ID_Modify[12]=='N' and ID_Modify[13]=='0' and ID_Modify[14]=='6' and ID_Modify[16]=='9':
			val_11=int(Num_Cabinet) * 6
		elif ID_Modify[12]=='N' and ID_Modify[13]=='2' and ID_Modify[14]=='2' and ID_Modify[16]=='6':
			val_11=int(Num_Cabinet) * 2
		elif ID_Modify[12]=='N' and ID_Modify[13]=='2' and ID_Modify[14]=='4' and ID_Modify[16]=='9':
			val_11=int(Num_Cabinet) * 4
		elif ID_Modify[12]=='N' and ID_Modify[13]=='4' and ID_Modify[14]=='2' and ID_Modify[16]=='9':
			val_11=int(Num_Cabinet) * 2
	elif ID_Specify=='No':
		if FTA=="Universal Marshalling, GI only (0-6)" and GI=="2" and Uni_Count=="32":
			val_11=int(Num_Cabinet) * 2
		elif FTA=="Universal Marshalling, GI only (0-6)" and GI=="4" and Uni_Count=="64":
			val_11=int(Num_Cabinet) * 4
		elif FTA=="Universal Marshalling, GI only (0-6)" and GI=="6" and Uni_Count=="96":
			val_11=int(Num_Cabinet) * 6
		elif FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and GIIS=="0" and Non_GIIS=="2" and Uni_Count=="32":
			val_11=int(Num_Cabinet) * 2
		elif FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and GIIS=="0" and Non_GIIS=="4" and Uni_Count=="64":
			val_11=int(Num_Cabinet) * 4
		elif FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and GIIS=="0" and Non_GIIS=="6" and Uni_Count=="96":
			val_11=int(Num_Cabinet) * 6
		elif FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and GIIS=="2" and Non_GIIS=="2" and Uni_Count=="64":
			val_11=int(Num_Cabinet) * 2
		elif FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and GIIS=="2" and Non_GIIS=="4" and Uni_Count=="96":
			val_11=int(Num_Cabinet) * 4
		elif FTA=="Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)" and GIIS=="4" and Non_GIIS=="2" and Uni_Count=="96":
			val_11=int(Num_Cabinet) * 2
	return int(val_11)
#CXCPQ-46099 added by - Deepika Ghodki
def getpartposition(Product):
	Specify_id=Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
	id_modifier=Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
	cab_count=Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
	fiber_optic_ext=Product.Attr('C300_RG_UPC_Fiber_Optic_Extender').GetValue()
	var=0
	if Specify_id=='Yes' and len(id_modifier)>5:
		if id_modifier[5]=='M':
			var=int(cab_count)*2
		if id_modifier[5]=='N':
			var=int(cab_count)*4
	if Specify_id=="No":
		if fiber_optic_ext=='Multi Mode x2':
			var=int(cab_count)*2
		if fiber_optic_ext=='Multi Mode x4':
			var=int(cab_count)*4
	return var
#CXCPQ-45328
def getpart_51156387_317(Product):
	Specify_id=Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
	id_modifier=Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
	cab_count=Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
	Cab_type=Product.Attr('C300_RG_UPC_Cab_Mat_Type').GetValue()
	Ambient_Temp=Product.Attr('C300_RG_UPC_Ambient_Temp_Range').GetValue()
	Power_Supply_type=Product.Attr('C300_RG_UPC_Pwr_Supp_Type').GetValue()
	power_supply_red=Product.Attr('C300_RG_UPC_Pwr_Supp_Red').GetValue()
	abu_dhabi=Product.Attr('C300_RG_UPC_Abu_Dhabi_Bld_Loc').GetValue()
	FTA=Product.Attr('C300_RG_UPC_FTA').GetValue()
	Trace.Write("id_modifier= "+str(id_modifier))
	var1=0
	i,j,k=19,20,24
	if len(id_modifier)==26:
		i,j,k= 20,21,25
	elif len(id_modifier)==25:
		i,j,k=19,20,24
	elif len(id_modifier)==27:
		i,j,k=21,22,26
	if Specify_id=='Yes' and len(id_modifier)>24:
		if id_modifier[1]=='S' and id_modifier[2]=='B' and (id_modifier[12]=='X' or (id_modifier[12]=='G' and id_modifier[13]=='0') or (id_modifier[12]=='N' and id_modifier[13]=='0' and id_modifier[14]=='0') or (id_modifier[12]=='N' and id_modifier[13]=='0' and id_modifier[14]=='2') or (id_modifier[12]=='N' and id_modifier[13]=='0' and id_modifier[14]=='4')or (id_modifier[12]=='N' and id_modifier[13]=='0' and id_modifier[14]=='6') or (id_modifier[12]=='G' and id_modifier[13]=='2') or (id_modifier[12]=='G' and id_modifier[13]=='4') or (id_modifier[12]=='G' and id_modifier[13]=='6') ) and id_modifier[i]=='A' and id_modifier[j]=='R'and id_modifier[k]=='Y':
			var1=int(cab_count)*1
	if Specify_id=="No":
		if Cab_type=='Stainless Steel, IP66' and Ambient_Temp=='With Fan, Max Ambient +55°C' and Power_Supply_type=='25A AC/DC ATDI Supply' and power_supply_red=='REDUNDANT' and abu_dhabi=='Yes'and (FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' or FTA=='Universal Marshalling, GI only (0-6)' or FTA == 'No Treatment'):
			var1=int(cab_count)*1
	return var1
#CXCPQ-45316
def getpart_51156387_307(Product):
	Specify_id=Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
	id_modifier=Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
	cab_count=Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
	Cab_type=Product.Attr('C300_RG_UPC_Cab_Mat_Type').GetValue()
	Ambient_Temp=Product.Attr('C300_RG_UPC_Ambient_Temp_Range').GetValue()
	Power_Supply_type=Product.Attr('C300_RG_UPC_Pwr_Supp_Type').GetValue()
	power_supply_red=Product.Attr('C300_RG_UPC_Pwr_Supp_Red').GetValue()
	abu_dhabi=Product.Attr('C300_RG_UPC_Abu_Dhabi_Bld_Loc').GetValue()
	FTA=Product.Attr('C300_RG_UPC_FTA').GetValue()
	var2=0
	i,j,k=19,20,24
	if len(id_modifier)>24:
		i,j,k= 19,20,24
	if len(id_modifier)>25:
		i,j,k= 20,21,25
	if len(id_modifier)>26:
		i,j,k=21,22,26
	if Specify_id=='Yes' and len(id_modifier)>24:
		if id_modifier[1]=='S' and id_modifier[2]=='B' and (id_modifier[12]=='X' or (id_modifier[12]=='G' and id_modifier[13]=='0') or (id_modifier[12]=='N' and id_modifier[13]=='0' and id_modifier[14]=='0') or (id_modifier[12]=='N' and id_modifier[13]=='0' and id_modifier[14]=='2') or (id_modifier[12]=='N' and id_modifier[13]=='0' and id_modifier[14]=='4')or (id_modifier[12]=='N' and id_modifier[13]=='0' and id_modifier[14]=='6') or (id_modifier[12]=='G' and id_modifier[13]=='2') or (id_modifier[12]=='G' and id_modifier[13]=='4') or (id_modifier[12]=='G' and id_modifier[13]=='6') )and id_modifier[i]=='D' and id_modifier[j]=='R' and id_modifier[k]=='N' :
			var2=int(cab_count)*1
	if Specify_id=="No":
		if Cab_type=='Stainless Steel, IP66' and Ambient_Temp=='With Fan, Max Ambient +55°C' and Power_Supply_type=='20A DC/DC QUINT4+ Supply' and power_supply_red=='REDUNDANT' and abu_dhabi=='No' and (FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' or FTA=='Universal Marshalling, GI only (0-6)' or FTA == 'No Treatment'):
			var2=int(cab_count)*1
	return var2
#CXCPQ-43815
def getpart_4600135(Product):
	Specify_id=Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
	id_modifier=Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
	cab_count=Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
	FDAP=Product.Attr('C300_RG_UPC_Ext_FDAP_Comm_Supp').GetValue()
	var3=var4=0
	if Specify_id=='Yes' and len(id_modifier)>6:
		if id_modifier[6]=='S':
			var3=int(cab_count)*1
		if id_modifier[6]=='M':
			var4=int(cab_count)*1
	if Specify_id=="No":
		if FDAP=='FDAP Single-Mode':
			var3=int(cab_count)*1
		if FDAP=='FDAP Multi-Mode':
			var4=int(cab_count)*1
	return var3,var4

#CXCPQ-45336
def getpart_51156387_321(Product):
	Specify_id=Product.Attr('C300_RG_UPC_Specify_Id_Modifier').GetValue()
	id_modifier=Product.Attr('C300_RG_UPC_Id_Modifier').GetValue()
	cab_count=Product.Attr('C300_RG_UPC_Cab_Count').GetValue()
	Cab_type=Product.Attr('C300_RG_UPC_Cab_Mat_Type').GetValue()
	Ambient_Temp=Product.Attr('C300_RG_UPC_Ambient_Temp_Range').GetValue()
	Power_Supply_type=Product.Attr('C300_RG_UPC_Pwr_Supp_Type').GetValue()
	power_supply_red=Product.Attr('C300_RG_UPC_Pwr_Supp_Red').GetValue()
	abu_dhabi=Product.Attr('C300_RG_UPC_Abu_Dhabi_Bld_Loc').GetValue()
	FTA=Product.Attr('C300_RG_UPC_FTA').GetValue()
	var5=0
	i,j,k=19,20,24
	if len(id_modifier)>24:
		i,j,k= 19,20,24
	if len(id_modifier)>25:
		i,j,k= 20,21,25
	if len(id_modifier)>26:
		i,j,k=21,22,26
	if Specify_id=='Yes' and len(id_modifier)>24:
		if id_modifier[1]=='S' and id_modifier[2] =='B' and (id_modifier[12]=='X' or (id_modifier[12]=='G' and id_modifier[13]=='0') or (id_modifier[12]=='N' and id_modifier[13]=='0' and id_modifier[14]=='0') or (id_modifier[12]=='N' and id_modifier[13]=='0' and id_modifier[14]=='2') or (id_modifier[12]=='N' and id_modifier[13]=='0' and id_modifier[14]=='4')or (id_modifier[12]=='N' and id_modifier[13]=='0' and id_modifier[14]=='6') or (id_modifier[12]=='G' and id_modifier[13]=='2') or (id_modifier[12]=='G' and id_modifier[13]=='4') or (id_modifier[12]=='G' and id_modifier[13]=='6') ) and id_modifier[i] =='Q' and id_modifier[j] =='R' and id_modifier[k] =='Y':
			var5=int(cab_count)*1
	if Specify_id=="No":
		if Cab_type=='Stainless Steel, IP66' and Ambient_Temp=='With Fan, Max Ambient +55°C' and Power_Supply_type=='20A AC/DC QUINT4+ Supply' and power_supply_red=='REDUNDANT' and abu_dhabi=='Yes' and (FTA=='Universal Marshalling, GIIS (0-6)/Non-GIIS (0-6)' or FTA=='Universal Marshalling, GI only (0-6)' or FTA == 'No Treatment'):
			var5=int(cab_count)*1
	return var5