#Script is getting executed by the rule
import math as m
import System.Decimal as Dec
import GS_SerC_CG_RG_Amps
import GS_PS_Exp_Ent_BOM
import GS_C300_AMP_A_Calcs
import GS_C300_Calc_Module
import GS_Get_Set_AtvQty
import GS_SerC_CG_RG_Turbo_amps
import GS_C300_MCAR_calcs
ampA=GS_C300_AMP_A_Calcs.AMP_A(Product)
Product.ExecuteRulesOnce = True
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PWRN01",0)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PWRB01",0)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PWRN01",0)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","51306305-300",0)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","51199406-200",0)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-C8DS01",0)

imo=Product.Attributes.GetByName("SerC_CG_IO_Mounting_Solution").GetValue()
PST=Product.Attributes.GetByName("SerC_CG_Power_System_Type").GetValue()
PSV=Product.Attributes.GetByName("SerC_CG_Power_System_Vendor").GetValue()
iofam=Product.Attributes.GetByName("SerC_CG_IO_Family_Type").GetValue()
lenth=Product.Attributes.GetByName('SerC_CG_TID_Power_Supply_Cable_Length').GetValue()
cabside=Product.Attributes.GetByName('SerC_CG_Cabinet_Access').GetValue()

mounting_solution =Product.Attr('Dummy_CG_IO_Mounting_Solution').GetValue()
cabinet_access = Product.Attr('SerC_CG_Cabinet_Access').GetValue()
cabinet_type = Product.Attr('SerC_CG_Cabinet_Type_03').GetValue()
integrate_marshall = Product.Attr('SerC_CG_Integrated_Marshalling_Cabinet').GetValue()
cab_door_default = Product.Attr('SerC_CG_Cabinet_Doors_Default').GetValue()
cab_keylock_default = Product.Attr('SerC_CG_Cabinet_Door_Keylock _Default').GetValue()
cab_hinge = Product.Attr('SerC_CG_Cabinet_Hinge_Type').GetValue()
cab_color = Product.Attr('SerC_CG_Cabinet_Color_Default').GetValue()
io_flag = False
cont_col_mapping = {'C300_C IO MS': 'Labor_IS', 'C300_CG_Universal_IO_cont_1':'Labor_IS', 'C300_CG_Universal_IO_cont_2':'Labor_IS', 'SerC_CG_Enhanced_Function_IO_Cont':'Labor_IS','SerC_CG_Enhanced_Function_IO_Cont2':'Labor_IS'}
for cont in cont_col_mapping:
	io_cont = Product.GetContainerByName(cont)
	for cont_row in io_cont.Rows:
		#Trace.Write("Val = "+cont_row.GetColumnByName(cont_col_mapping[cont]).Value)
		if int(cont_row.GetColumnByName(cont_col_mapping[cont]).Value) > 0:
			io_flag = True
			break
	if io_flag:
		break


if iofam == "Series C":
	Product.Messages.Add("Total Amp(Series C) = {}".format(ampA))
Product.Attributes.GetByName('Low_amps').AssignValue("")
A=0
B=Product.Attributes.GetByName("SerC_CG_Amps_Value").GetValue()
if B=="":
	B=0
else:
	B=int(B)
B=B-ampA
A=m.ceil(ampA/20.0)
A1=m.ceil(ampA/40.0)

q=0
A3=0
q2= ampA % 40

if ampA % 40 > 20:
	q=1
else:
	q=0

if q2 > 0 and q2 <= 20:
	A3=1
else:
	A3=0
Trace.Write("amp"+str(ampA))
A2= int(ampA) // 40 + q

#CXCPQ-39269
CC_PWRN01add=0
if PST=="Non Redundant 20A" and PSV=="TDI" and imo=="Cabinet" and iofam=="Series C":
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PWRN01",A)
	CC_PWRN01add=A
else:
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PWRN01",0)
	CC_PWRN01add=0

CC_PWRR01add=0
if PST=="Redundant 20A" and PSV=="TDI" and imo=="Cabinet" and iofam=="Series C":
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PWRR01",A)
	CC_PWRR01add=A
else:
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PWRR01",0)
	CC_PWRR01add=0

CC_PWRB01add=0
if PST=="Redundant with BBU 20A" and PSV=="TDI" and imo=="Cabinet" and iofam=="Series C":
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PWRB01",A)
	CC_PWRB01add=A
else:
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PWRB01",0)
	CC_PWRB01add=0


CC_PWR401add=0
if PST=="Redundant 40A" and PSV=="TDI" and imo=="Cabinet" and iofam=="Series C":
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PWR401",A1)
	CC_PWR401add=A1
else:
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PWR401",0)
	CC_PWR401add=0

CC_PWN401add=0
if PST=="Non Redundant 40A" and PSV=="TDI" and imo=="Cabinet" and iofam=="Series C":
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PWN401",A1)
	CC_PWN401add=A1
else:
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PWN401",0)
	CC_PWN401add=0


if PST=="Locally Supplied Power" and B < 0:
	Product.Attributes.GetByName('Low_amps').AssignValue("Power supply is not enough to generate needed Amps")


if PST=="Minimum Required Redundant" and PSV=="TDI" and imo=="Cabinet" and iofam=="Series C":
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PWR401",A2)
	CC_PWR401add=A2
elif CC_PWR401add==0:
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PWR401",0)

if PST=="Minimum Required Redundant" and PSV=="TDI" and imo=="Cabinet" and iofam=="Series C":
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PWRR01",A3)
	CC_PWRR01add=A3
elif CC_PWRR01add==0:
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PWRR01",0)

if PST=="Minimum Required Non Redundant" and PSV=="TDI" and imo=="Cabinet" and iofam=="Series C":
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PWN401",A2)
	CC_PWN401add=A2
elif CC_PWN401add==0:
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PWN401",0)

if PST=="Minimum Required Non Redundant" and PSV=="TDI" and imo=="Cabinet" and iofam=="Series C":
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PWRN01",A3)
	CC_PWRN01add=A3
elif CC_PWRN01add==0:
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PWRN01",0)

#CXCPQ-39363
AA=m.ceil(ampA/20.0)
CU_PWMN20add=0
if (PST=="Non Redundant 20A" or PST=="Minimum Required Non Redundant") and PSV=="Meanwell" and imo=="Cabinet" and iofam=="Series C":
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","CU-PWMN20",AA)
	CU_PWMN20add=AA
else:
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","CU-PWMN20",0)
	CU_PWMN20add=0

CU_PWMR20add=0
if (PST=="Redundant 20A" or PST=="Minimum Required Redundant")  and PSV=="Meanwell" and imo=="Cabinet" and iofam=="Series C":
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","CU-PWMR20",AA)
	CU_PWMR20add=AA
else:
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","CU-PWMR20",0)
	CU_PWMR20add=0

#CXCPQ-39366
CU_PWPN20add=0
if (PST=="Non Redundant 20A" or PST=="Minimum Required Non Redundant") and PSV=="Phoenix Contact" and imo=="Cabinet" and iofam=="Series C":
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","CU-PWPN21",AA)
	CU_PWPN20add=AA
else:
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","CU-PWPN21",0)
	CU_PWPN20add=0

CU_PWPR20add=0
if (PST=="Redundant 20A" or PST=="Minimum Required Redundant") and PSV=="Phoenix Contact" and imo=="Cabinet" and iofam=="Series C":
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","CU-PWPR21",AA)
	CU_PWPR20add=AA
else:
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","CU-PWPR21",0)
	CU_PWPR20add=0

fpart = CC_PWRN01add + CC_PWRR01add + CC_PWRB01add + CC_PWR401add + CC_PWN401add + CU_PWMN20add + CU_PWMR20add + CU_PWPN20add + CU_PWPR20add
C4=GS_C300_MCAR_calcs.cab_c(Product)[20]
if fpart > 0:
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","51306305-300",fpart)
else:
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","51306305-300",0)

if iofam == "Series C" and io_flag>0 and mounting_solution == "Cabinet" and cabinet_access == "Dual Access" and cabinet_type == "Normal Cabinet" and integrate_marshall == "No" and cab_door_default == "Standard" and cab_keylock_default == "Standard" and cab_hinge == "130 Degree" and cab_color == "Gray-RAL 7035" and (fpart >0 or C4 >0):
	sum_of_parts = Dec.Ceiling((fpart)/2.0) if fpart>0 else 0.00
	c4_value = Dec.Ceiling((C4)/2.0) if C4>0 else 0.00
	C8DS01=max(sum_of_parts, c4_value)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-C8DS01",C8DS01)

amps=GS_SerC_CG_RG_Amps.gettotalamps(Product)
Product.Attributes.GetByName('Amp_message').AssignValue("Amp, A for SCM: "+str(amps))
if iofam == "Series-C Mark II":
	Product.Messages.Add("Amp, A for SCM: "+ str(amps))

rq= m.ceil(amps/20.0)
#CXCPQ-46080,CXCPQ-46081,CXCPQ-46082
if PSV == "TDI" and iofam == "Series-C Mark II":
	if PST=="Redundant 20A" and (rq+A+A3)>0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PWRR01",rq+CC_PWRR01add)
	elif CC_PWRR01add==0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PWRR01",0)
	if PST=="Redundant with BBU 20A" and (rq+A)>0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PWRB01",rq+CC_PWRB01add)
	elif CC_PWRB01add==0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PWRB01",0)
else:
	if CC_PWRR01add==0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PWRR01",0)
	if CC_PWRB01add==0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PWRB01",0)

if PSV == "Meanwell" and iofam == "Series-C Mark II":
	if PST=="Redundant 20A" and (rq+AA)>0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","CU-PWMR20",rq+CU_PWMR20add)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","CU-PWMR20",0)
else:
	if CU_PWMR20add==0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","CU-PWMR20",0)

if PSV == "Phoenix Contact" and iofam == "Series-C Mark II":
	if PST=="Redundant 20A" and (rq+AA)>0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","DU-PWPR21",rq+CU_PWPR20add)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","DU-PWPR21",0)
else:
	if CU_PWPR20add==0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","DU-PWPR21",0)
# Calculate cabinet parts mark II
GS_C300_Calc_Module.populateCabinetParts(Product)
GS_SerC_CG_RG_Amps.generic_type_markII(Product)
#cabinet bay qty
B, D, E, F = GS_C300_Calc_Module.getBayQuantities(Product)
if iofam == "Series-C Mark II":
	Product.Messages.Add("Bay Qty B = {}, D = {}, E = {}, F = {}".format(B, D, E, F))
#CXCPQ-39286
qnty=0
p1=GS_Get_Set_AtvQty.getAtvQty(Product, 'Series_C_CG_Part_Summary','CC-CBDS01')
p2=GS_Get_Set_AtvQty.getAtvQty(Product, 'Series_C_CG_Part_Summary','CC-CBDD01')
p3=GS_Get_Set_AtvQty.getAtvQty(Product, 'Series_C_CG_Part_Summary','51454314-300')
p4=GS_Get_Set_AtvQty.getAtvQty(Product, 'Series_C_CG_Part_Summary','51454314-100')
p5=GS_Get_Set_AtvQty.getAtvQty(Product, 'Series_C_CG_Part_Summary','51454314-200')
p6=GS_Get_Set_AtvQty.getAtvQty(Product, 'Series_C_CG_Part_Summary','CC-CASS11')
p7=GS_Get_Set_AtvQty.getAtvQty(Product, 'Series_C_CG_Part_Summary','CC-CADS11')
p8=GS_Get_Set_AtvQty.getAtvQty(Product, 'Series_C_CG_Part_Summary','51454314-600')
p9=GS_Get_Set_AtvQty.getAtvQty(Product, 'Series_C_CG_Part_Summary','51454314-400')
p10=GS_Get_Set_AtvQty.getAtvQty(Product,'Series_C_CG_Part_Summary','51454314-500')

valuelist=[p1,p2,p3,p4,p5,p6,p7,p8,p9,p10]

for i in valuelist:
	Trace.Write(i)
	if int(i)>0:
		qnty=int(i)

if qnty>0:
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","51199406-200",qnty)
else:
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","51199406-200",0)

#CXCPQ-48865
#B,D,E,F=GS_C300_calc_module.getBayQuantities(Product)
z1=GS_Get_Set_AtvQty.getAtvQty(Product,'Series_C_CG_Part_Summary','51454909-100')
z2=GS_Get_Set_AtvQty.getAtvQty(Product,'Series_C_CG_Part_Summary','51307186-275')
z3= (D*4) + (E*8) + (B*8)

if imo=="Cabinet" and iofam=="Series-C Mark II":
	if PSV=="TDI":
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","51203160-100",z3)
	else:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","51203160-100",0)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","51307186-275",2*m.ceil(z1/6.0))
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","50135106-100",m.ceil(2*m.ceil(z1/6.0)/2.0))
else:
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","51307186-275",0)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","50135106-100",0)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","51203160-100",0)

#CXCPQ-39274
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","51202324-110",0)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","51202324-310",0)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","51202324-410",0)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","51202324-210",0)

x1=GS_Get_Set_AtvQty.getAtvQty(Product,'Series_C_CG_Part_Summary','CC-CBDS01')
x2=GS_Get_Set_AtvQty.getAtvQty(Product,'Series_C_CG_Part_Summary','CC-CBDD01')
x3=GS_Get_Set_AtvQty.getAtvQty(Product,'Series_C_CG_Part_Summary','51454314-300')
x4=GS_Get_Set_AtvQty.getAtvQty(Product,'Series_C_CG_Part_Summary','51454314-100')
x5=GS_Get_Set_AtvQty.getAtvQty(Product,'Series_C_CG_Part_Summary','51454314-200')
x6=GS_Get_Set_AtvQty.getAtvQty(Product,'Series_C_CG_Part_Summary','CC-CASS11')
x7=GS_Get_Set_AtvQty.getAtvQty(Product,'Series_C_CG_Part_Summary','CC-CADS11')
x8=GS_Get_Set_AtvQty.getAtvQty(Product,'Series_C_CG_Part_Summary','51454314-600')
x9=GS_Get_Set_AtvQty.getAtvQty(Product,'Series_C_CG_Part_Summary','51454314-400')
x10=GS_Get_Set_AtvQty.getAtvQty(Product,'Series_C_CG_Part_Summary','51454314-500')
x11=GS_Get_Set_AtvQty.getAtvQty(Product,'Series_C_CG_Part_Summary','51307186-275')

slist=[x1,x2,x3,x4,x5,x6,x7,x8,x9,x10]
xx=0
for i in slist:
	if i>0:
		xx=i
Trace.Write(xx)

si=0

#CXCPQ-50786
x12=GS_Get_Set_AtvQty.getAtvQty(Product,'Series_C_CG_Part_Summary','CC-CBDS01')
x13=GS_Get_Set_AtvQty.getAtvQty(Product,'Series_C_CG_Part_Summary','CC-CBDD01')

if iofam=="Turbomachinery":
	if cabside=="Single Access":
		si=1
		xx=x12
	elif cabside=="Dual Access":
		si=2
		xx=x13

if cabside=="Single Access" and imo=="Cabinet" and PSV=="TDI" and iofam=="Series C":
	si=1
elif cabside=="Dual Access" and imo=="Cabinet" and PSV=="TDI" and iofam=="Series C":
	si=2
elif imo=="Cabinet" and PSV=="TDI" and iofam=="Series-C Mark II":
	si=x11
	xx=1

if iofam != "Series-C Mark II":
	lenth = Product.Attributes.GetByName('SerC_CG_Power_Supply_Cable_Length').GetValue()

if lenth=="10 In":
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","51202324-110",si* int(xx))
elif lenth=="48 In":
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","51202324-310",si* int(xx))
elif lenth=="82 In":
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","51202324-410",si* int(xx))
elif lenth=="20 In":
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","51202324-210",si* int(xx))

#CXCPQ-48863
jc=0
y1=GS_Get_Set_AtvQty.getAtvQty(Product,'Series_C_CG_Part_Summary','CC-PWRR01')
y2=GS_Get_Set_AtvQty.getAtvQty(Product,'Series_C_CG_Part_Summary','CC-PWRB01')
y3=GS_Get_Set_AtvQty.getAtvQty(Product,'Series_C_CG_Part_Summary','CU-PWMR20')
y4=GS_Get_Set_AtvQty.getAtvQty(Product,'Series_C_CG_Part_Summary','DU-PWPR21')
list2=[y1,y2,y3,y4]

for j in list2:
	if j>0:
		jc=j
if iofam=="Series-C Mark II":
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","51306305-300",jc+fpart)

#CXCPQ-50762
TAmp=GS_SerC_CG_RG_Turbo_amps.Get_turbo_amps(Product)
Product.Attributes.GetByName('Amps_turbo').AssignValue("Amp,for turbo: "+str(TAmp))
if iofam == "Turbomachinery":
	Product.Messages.Add("TAmp,for Turbo = {}".format(TAmp))

#CXCPQ-50771 CXCPQ-51409
jj=0
if x12!=0:
	jj=x12
if x13!=0:
	jj=x13
qa=0
if iofam=="Turbomachinery":
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","51199406-200",jj)
	if PST =="Redundant 20A":
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PWRR01",m.ceil(TAmp/20.0))
		qa=m.ceil(TAmp/20.0)
	elif PST=="Redundant with BBU 20A":
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PWRB01",m.ceil(TAmp/20.0))
		qa=m.ceil(TAmp/20.0)
	elif PST=="Non Redundant 20A":
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","CC-PWRN01",m.ceil(TAmp/20.0))
		qa=m.ceil(TAmp/20.0)
	#CXCPQ-51412
	if qa>0:
		GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Series_C_CG_Part_Summary","51306305-300",qa)
Product.ApplyRules()
Product.ExecuteRulesOnce = False