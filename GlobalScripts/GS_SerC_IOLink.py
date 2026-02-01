#CXCPQ-53578
import math,GS_Get_Set_AtvQty
import System.Decimal as sd
def SerC_IOLink(Product,PCNT_A1):
	B=C=D=E=F=G=H=H1=0
	temp_b=temp_c=temp_d=0
	qty = {}
	A1 = int(float(PCNT_A1)) if PCNT_A1 != '' else 0
	prod_cab = {'Series-C Control Group':'SerC_CG_Cabinet_Access','Series-C Remote Group':'SerC_RG_Cabinet_Access'}
	Cabinet_parts = ['CC-CBDS01','51454314-300','51454314-600','CC-CBDD01','51454314-100','51454314-200','51454314-400','51454314-500']
	MCAR_parts = ['CC-MCAR01','CC-MCAR30','CC-MCARW1','MU-TMCN01']
	IOTA_parts = ['CC-TAIN11','CC-TAIN01','CC-TAIX61','CC-TAIX51','CC-TAIL51','CC-TAON01','CC-TAOX51','CC-TAOX61','CC-TAON11','CC-TUIO41','CC-TUIO31','CC-TUIO11','CC-TUIO01','CC-TAID11','CC-TAOX11','CC-TAID01','CC-TAIM01','CC-TAOX01','CC-TDIL11','CC-TDI120','CC-TDI230','CC-TDOB11','CC-TDOR11','CC-TDOR01','CC-TPIX11','CC-TDIL01','CC-TDI110','CC-TDI151','CC-TDI220','CC-TDOB01','CC-GAIX11','CC-GAOX11','CC-GDIL11','CC-GAIX21','CC-GAOX21','CC-GDIL21','CC-GDIL01','CC-GDOL11','CC-TAIX01','CC-TAIX11']
	prod_part = {'Series-C Control Group':'Series_C_CG_Part_Summary_Cont','Series-C Remote Group':'Series_C_RG_Part_Summary_Cont'}
	CA = GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','CADS')
	if Product.Attr(prod_cab[Product.Name]).GetValue() == "Single Access":
		CA = GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','CASS')
	Trace.Write("CA:"+str(CA))
	if Product.Name in prod_part:
		for row in Product.GetContainerByName(prod_part[Product.Name]).Rows:
			if row["PartNumber"] in Cabinet_parts and A1:
				temp_b+=int(row["Part_Qty"] if row["Part_Qty"] != '' else 0)
			if row["PartNumber"] in MCAR_parts:
				#Trace.Write(row["PartNumber"])
				temp_c+=int(row["Part_Qty"]) if row["Part_Qty"] != '' else 0
				#Trace.Write(row["Part_Qty"])
			if row["PartNumber"] in IOTA_parts:
				#Trace.Write(row["PartNumber"])
				temp_d+=int(row["Part_Qty"]) if row["Part_Qty"] != '' else 0
				#Trace.Write(row["Part_Qty"])
		temp_b+=int(CA)
		Trace.Write("temp_b:"+str(temp_b))
		if temp_b and A1:
			B = sd.Ceiling(float(temp_b)/float(A1))
			Trace.Write("B value is: {}".format(B))
		if temp_c and A1:
			C = sd.Ceiling(float(temp_c)/float(A1))
		if temp_d and A1:
			D = sd.Ceiling(float(temp_d)/float(A1))
			E = math.ceil(D/40.0)
		if int(E) == 1:
			F=C
		elif int(E) == 2:
			G=math.ceil(C/2.0)
			F=math.ceil(C/2.0)
		if D>0 and D<=40:
			if F:
				H = math.ceil(D/F)
		elif D>40 and D<=80:
			if G:
				H1 = math.ceil((D-40)/G)
			if F:
				H = math.ceil(40/F)
		qty = {'H':int(H),'H1':int(H1),'F':int(F),'G':int(G),'D':int(D)}
	return qty
#Trace.Write(SerC_IOLink(Product))
#CXCPQ-45942
def SerC_Header(Product):
	cab_qty=D_qty=0
	prod_part = {'Series-C Control Group':'Series_C_CG_Part_Summary_Cont','Series-C Remote Group':'Series_C_RG_Part_Summary_Cont'}
	prod_cab = {'Series-C Control Group':'SerC_CG_Cabinet_Access','Series-C Remote Group':'SerC_RG_Cabinet_Access'}
	single_part = ['CC-CBDS01','51454314-300','51454314-600']
	dual_part = ['CC-CBDD01','51454314-100','51454314-200','51454314-400','51454314-500']
	D_part = ['51109524-200','51109524-600','51109524-500','51109524-700','51109524-100']
	CA = GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','CADS')
	if Product.Attr(prod_cab[Product.Name]).GetValue() == "Single Access":
		CA = GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','CASS')
	if Product.Name in prod_part:
		for row in Product.GetContainerByName(prod_part[Product.Name]).Rows:
			if Product.Attr(prod_cab[Product.Name]).GetValue() == 'Single Access':
				if row["PartNumber"] in single_part:
					cab_qty +=math.ceil(int(row["Part_Qty"]))
			elif Product.Attr(prod_cab[Product.Name]).GetValue() == 'Dual Access':
				if row["PartNumber"] in dual_part:
					cab_qty +=2*math.ceil(int(row["Part_Qty"]))
			if row["PartNumber"] in D_part:
				D_qty +=math.ceil(int(row["Part_Qty"]))
		if Product.Attr(prod_cab[Product.Name]).GetValue() == 'Single Access':
			cab_qty += CA
		elif Product.Attr(prod_cab[Product.Name]).GetValue() == 'Dual Access':
			cab_qty += 2*CA
	return int(cab_qty), int(D_qty)
## Mark 2
#CXCPQ-46126
#import math
def SMC_IOLink(Product,PCNT_A1):
	AttrName = 'Series_C_CG_Part_Summary'
	if Product.Name == 'Series-C Remote Group':
		AttrName = 'Series_C_RG_Part_Summary'
	B=C=D=E=F=G=H=H1=0
	temp_c=temp_d=0
	qty = {}
	A1 = int(float(PCNT_A1)) if PCNT_A1 != '' else 0
	Cabinet_parts = ['CC-CBDS01','CC-CBDD01']
	MCAR_parts = ['51454909-100']
	IOTA_parts = ['DC-TAIX61','DC-TAIX51','DC-TAOX61','DC-TAOX51','DC-TDIL61','DC-TDIL51','DC-TDOD61','DC-TDOD51','DC-TUIO41','DC-TUIO31','DC-TAID11','DC-TAID01','DC-TAOX11','DC-TAOX01','DC-TDIL11','DC-TDIL01','DC-TDOB11','DC-TDOR11','DC-TPIX11','DC-TDI110','DC-TDI220','DC-TDOB01','DC-TDOR01','DC-TAIL51','DC-TAIX11','DC-TAIX01']
	if A1:
		for part in Cabinet_parts:
			temp_b = GS_Get_Set_AtvQty.getAtvQty(Product, AttrName, part)
			B+=math.ceil(temp_b/A1)
	for part in MCAR_parts:
		temp_c += int(GS_Get_Set_AtvQty.getAtvQty(Product, AttrName, part))
	for part in IOTA_parts:
		temp_d += int(GS_Get_Set_AtvQty.getAtvQty(Product, AttrName, part))

	if temp_c and A1:
		C = sd.Ceiling(float(temp_c)/float(A1))
		Log.Info("C:"+str(C))
	if temp_d and A1:
		D = sd.Ceiling(float(temp_d)/float(A1))
		E = math.ceil(D/40.0)
		Log.Info("D:"+str(D))
		Log.Info("E:"+str(E))
	if int(E) == 1:
		F=C
		Log.Info("F:"+str(F))
	elif int(E) == 2:
		G=math.ceil(C/2.0)
		F=math.ceil(C/2.0)
		Log.Info("G:"+str(G))
	if D>0 and D<=40:
		if F:
			H = math.ceil(D/F)
			Log.Info("H:"+str(H))
	elif D>40 and D<=80:
		if G:
			H1 = math.ceil((D-40)/G)
		if F:
			H = math.ceil(40/F)
	qty = {'H':int(H),'H1':int(H1),'F':int(F),'G':int(G),'D':int(D)}
	return qty
#Trace.Write(str(SMC_IOLink(Product)))
#CXCPQ-46127
def SMC_extension(Product):
	ext_qty=0
	prod_part = {'Series-C Control Group':'Series_C_CG_Part_Summary_Cont','Series-C Remote Group':'Series_C_RG_Part_Summary_Cont'}
	D_part = ['51109524-200','51109524-600','51109524-500','51109524-700']
	if Product.Name in prod_part:
		for row in Product.GetContainerByName(prod_part[Product.Name]).Rows:
			if row["PartNumber"] in D_part:
				ext_qty +=math.ceil(int(row["Part_Qty"])) if row["Part_Qty"] != '' else 0
	return int(ext_qty)
#Trace.Write(str(SMC_extension(Product)))
### Turbomachinery
#CXCPQ-46122
def Turbo_IOLink(Product,PCNT_A1):
	B=C=D=E=F=G=H=H1=0
	temp_c=temp_d=0
	qty = {}
	A1 = int(float(PCNT_A1)) if PCNT_A1 != '' else 0
	Cabinet_parts = ['CC-CBDS01','CC-CBDD01']
	MCAR_parts = ['CC-MCAR01','CC-MCARW1','MU-TMCN01','CC-MCC003']
	IOTA_parts = ['CC-TSV211','CC-TSP411','CC-TUIO41','CC-TUIO31','CC-TUIO11','CC-TUIO01','CC-TAID11','CC-TAOX11','CC-TAID01','CC-TAIM01','CC-TAOX01','CC-TDIL11','CC-TDI120','CC-TDI230','CC-TDOB11','CC-TDOR11','CC-TDOR01','xCC-TPIX11','CC-TDIL01','CC-TDI110','CC-TDI151','CC-TDI220','CC-TDOB01','CC-GAIX11','CC-GAOX11','CC-GDIL11','CC-GAIX21','CC-GAOX21','CC-GDIL21','CC-GDIL01','CC-GDOL11']
	prod_part = {'Series-C Control Group':'Series_C_CG_Part_Summary_Cont','Series-C Remote Group':'Series_C_RG_Part_Summary_Cont'}
	if Product.Name in prod_part:
		for row in Product.GetContainerByName(prod_part[Product.Name]).Rows:
			if row["PartNumber"] in Cabinet_parts and A1:
				B+=math.ceil(int(row["Part_Qty"] if row["Part_Qty"] != '' else 0)/A1)
			if row["PartNumber"] in MCAR_parts:
				#Trace.Write(row["PartNumber"])
				temp_c+=int(row["Part_Qty"]) if row["Part_Qty"] != '' else 0
				#Trace.Write(row["Part_Qty"])
			if row["PartNumber"] in IOTA_parts:
				#Trace.Write(row["PartNumber"])
				temp_d+=int(row["Part_Qty"]) if row["Part_Qty"] != '' else 0
				#Trace.Write(row["Part_Qty"])
		if temp_c and A1:
			C = sd.Ceiling(float(temp_c)/float(A1))
		if temp_d and A1:
			D = sd.Ceiling(float(temp_d)/float(A1))
			E = math.ceil(D/6.0)
		if int(E) == 1:
			F=C
		elif int(E) == 2:
			G=math.ceil(C/2.0)
			F=math.ceil(C/2.0)
		if D>0 and D<=6:
			if F:
				H = math.ceil(D/F)
		elif D>6 and D<=12:
			if G:
				H1 = math.ceil((D-6)/G)
			if F:
				H = math.ceil(6/F)
		qty = {'H':int(H),'H1':int(H1),'F':int(F),'G':int(G),'D':int(D)}
	return qty
#Trace.Write(str(Turbo_IOLink(Product)))
#CXCPQ-46124
def Turbo_Header(Product):
	cab_qty=D_qty=0
	prod_part = {'Series-C Control Group':'Series_C_CG_Part_Summary_Cont','Series-C Remote Group':'Series_C_RG_Part_Summary_Cont'}
	prod_cab = {'Series-C Control Group':'SerC_CG_Cabinet_Access','Series-C Remote Group':'SerC_RG_Cabinet_Access'}
	single_part = ['CC-CBDS01']
	dual_part = ['CC-CBDD01']
	D_part = ['51109524-200','51109524-600','51109524-500','51109524-700','51109524-100']
	if Product.Name in prod_part:
		for row in Product.GetContainerByName(prod_part[Product.Name]).Rows:
			if Product.Attr(prod_cab[Product.Name]).GetValue() == 'Single Access':
				if row["PartNumber"] in single_part:
					cab_qty +=math.ceil(int(row["Part_Qty"]))
			elif Product.Attr(prod_cab[Product.Name]).GetValue() == 'Dual Access':
				if row["PartNumber"] in dual_part:
					cab_qty +=2*math.ceil(int(row["Part_Qty"]))
			if row["PartNumber"] in D_part:
				D_qty +=math.ceil(int(row["Part_Qty"]))
	return int(cab_qty), int(D_qty)
#Trace.Write(str(Turbo_Header(Product)))
## IOHIVE -- CN100
#CXCPQ-55123 -- CXCPQ-52363
def IOHIVE_drop(Product):
	B=C=D=E=F=H=0
	temp_b=temp_c=temp_d=0
	qty = {}
	prod_cab = {'Series-C Control Group':'SerC_CG_Cabinet_Access','Series-C Remote Group':'SerC_RG_Cabinet_Access'}
	Cabinet_parts = ['CC-CBDS01','51454314-300','51454314-600','CC-CBDD01','51454314-100','51454314-200','51454314-400','51454314-500']
	MCAR_parts = ['CC-MCAR01','CC-MCAR30','CC-MCARW1','MU-TMCN01']
	IOTA_parts = ['CC-TAIN11','CC-TAIN01','CC-TAIX61','CC-TAIX51','CC-TAIL51','CC-TAON01','CC-TAOX51','CC-TAOX61','CC-TAON11','CC-TUIO41','CC-TUIO31','CC-TUIO11','CC-TUIO01','CC-TAID11','CC-TAOX11','CC-TAID01','CC-TAIM01','CC-TAOX01','CC-TDIL11','CC-TDI120','CC-TDI230','CC-TDOB11','CC-TDOR11','CC-TDOR01','CC-TPIX11','CC-TDIL01','CC-TDI110','CC-TDI151','CC-TDI220','CC-TDOB01','CC-GAIX11','CC-GAOX11','CC-GDIL11','CC-GAIX21','CC-GAOX21','CC-GDIL21','CC-GDIL01','CC-GDOL11','CC-TAIX01','CC-TAIX11']
	prod_part = {'Series-C Control Group':'Series_C_CG_Part_Summary_Cont','Series-C Remote Group':'Series_C_RG_Part_Summary_Cont'}
	prod_part1 = {'Series-C Control Group':'Series_C_CG_Part_Summary','Series-C Remote Group':'Series_C_RG_Part_Summary'}
	A1 = GS_Get_Set_AtvQty.getAtvQty(Product, prod_part1[Product.Name], 'CC-TION11')
	CA = GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','CADS')
	if Product.Attr(prod_cab[Product.Name]).GetValue() == "Single Access":
		CA = GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','CASS')
	if Product.Name in prod_part:
		for row in Product.GetContainerByName(prod_part[Product.Name]).Rows:
			if row["PartNumber"] in Cabinet_parts and A1:
				temp_b+=int(row["Part_Qty"] if row["Part_Qty"] != '' else 0)
			if row["PartNumber"] in MCAR_parts:
				#Trace.Write(row["PartNumber"])
				temp_c+=int(row["Part_Qty"]) if row["Part_Qty"] != '' else 0
				#Trace.Write(row["Part_Qty"])
			if row["PartNumber"] in IOTA_parts:
				#Trace.Write(row["PartNumber"])
				temp_d+=int(row["Part_Qty"]) if row["Part_Qty"] != '' else 0
				#Trace.Write(row["Part_Qty"])
		temp_b+=int(CA)
		if temp_b and A1:
			B = sd.Ceiling(float(temp_b)/float(A1))
		if temp_c and A1:
			C = sd.Ceiling(float(temp_c)/float(A1))
		if temp_d and A1:
			D = sd.Ceiling(float(temp_d)/float(A1))
			E = math.ceil(D/40.0)
		if int(E) == 1:
			F=C
		if D>0 and D<=40:
			if F:
				H = math.ceil(D/F)
		qty = {'H':int(H),'F':int(F),'D':int(D)}
	return qty
#Trace.Write(str(IOHIVE_drop(Product)))
#CXCPQ-55119 -- CXCPQ-52362
def IO_Header(Product):
	cab_qty=D_qty=0
	prod_part = {'Series-C Control Group':'Series_C_CG_Part_Summary_Cont','Series-C Remote Group':'Series_C_RG_Part_Summary_Cont'}
	prod_cab = {'Series-C Control Group':'SerC_CG_Cabinet_Access','Series-C Remote Group':'SerC_RG_Cabinet_Access'}
	prod_part1 = {'Series-C Control Group':'Series_C_CG_Part_Summary','Series-C Remote Group':'Series_C_RG_Part_Summary'}
	single_part = ['CC-CBDS01','51454314-300','51454314-600']
	dual_part = ['CC-CBDD01','51454314-100','51454314-200','51454314-400','51454314-500']
	D_part = ['51109524-200','51109524-600','51109524-500','51109524-700','51109524-100']
	IION01 = GS_Get_Set_AtvQty.getAtvQty(Product, prod_part1[Product.Name], 'CC-IION01')
	CA = GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','CADS')
	if Product.Attr(prod_cab[Product.Name]).GetValue() == "Single Access":
		CA = GS_Get_Set_AtvQty.getAtvQty(Product,'SerC_IO_Params','CASS')
	if Product.Name in prod_part:
		for row in Product.GetContainerByName(prod_part[Product.Name]).Rows:
			if Product.Attr(prod_cab[Product.Name]).GetValue() == 'Single Access':
				if row["PartNumber"] in single_part:
					cab_qty +=math.ceil(int(row["Part_Qty"]))
			elif Product.Attr(prod_cab[Product.Name]).GetValue() == 'Dual Access':
				if row["PartNumber"] in dual_part:
					cab_qty +=2*math.ceil(int(row["Part_Qty"]))
			#if row["PartNumber"] in D_part:
				#D_qty +=math.ceil(int(row["Part_Qty"]))
		if Product.Attr(prod_cab[Product.Name]).GetValue() == 'Single Access':
			cab_qty += CA
		elif Product.Attr(prod_cab[Product.Name]).GetValue() == 'Dual Access':
			cab_qty += 2*CA
		for part in D_part:
			D_qty += int(GS_Get_Set_AtvQty.getAtvQty(Product, prod_part1[Product.Name], part))
	return int(cab_qty),int(IION01),int(D_qty)
#Trace.Write(str(IO_Header(Product)))
#CXCPQ-55609
def PMIO_FTA(Product):
	A=0
	IOM_Parts = ['MC-PAIH03','MC-PHAI01','MC-PAIL02','MC-PLAM02','MC-PRHM01','MC-PSTX03','MC-PAOY22','MC-PHAO01','MC-PDIX02','MC-PDIY22','MC-PDIS12','MC-PDOX02','MC-PDOY22']
	rg_cont = Product.GetContainerByName('Series_C_Remote_Groups_Cont')
	if Product.Name == 'Series-C Control Group':
		for row in Product.GetContainerByName('Series_C_CG_Part_Summary_Cont').Rows:
			if row["PartNumber"] in IOM_Parts:
				A+=int(row["Part_Qty"] if row["Part_Qty"] != '' else 0)
		'''for rgs in rg_cont.Rows:
			rg = rgs.Product
			for row in rg.GetContainerByName('Series_C_RG_Part_Summary_Cont').Rows:
				if row["PartNumber"] in IOM_Parts:
					A+=int(row["Part_Qty"] if row["Part_Qty"] != '' else 0)'''
	#Trace.Write("A value is {}".format(A))
	return int(A)
#Trace.Write(PMIO_FTA(Product))
def PMIO_RG_FTA(Product):
	A=0
	IOM_Parts = ['MC-PAIH03','MC-PHAI01','MC-PAIL02','MC-PLAM02','MC-PRHM01','MC-PSTX03','MC-PAOY22','MC-PHAO01','MC-PDIX02','MC-PDIY22','MC-PDIS12','MC-PDOX02','MC-PDOY22']
	if Product.Name == 'Series-C Remote Group':
		for row in Product.GetContainerByName('Series_C_RG_Part_Summary_Cont').Rows:
			if row["PartNumber"] in IOM_Parts:
				A+=int(row["Part_Qty"] if row["Part_Qty"] != '' else 0)
	return int(A)
#Trace.Write(PMIO_RG_FTA(Product))