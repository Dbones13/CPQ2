import System.Decimal as D
#import sys
import GS_SM_ReadPart_Attrs,GS_SM_Part_attributes
import GS_SM_Part_Calcs,GS_SM_CG_RG_Parts,GS_Load_SM_RIO_Cab_Summary
import GS_SM_Part_Update
import GS_SMPartsCalc,GS_SM_CompA1_Calcs
import sm_part_add_calcs
import GS_Power_Supply_calcs
import GS_Power_Supply_calcs1
import GS_SMIOComponents, GS_SM_CG_Part_Summary
import GS_part_add_IO_value, GS_SM_Load_SM_RIO_cabinet_summary_Calc
import math as m
import GS_SM_CG_Component_Attribute
import ProductUtil as pu
import GS_SM_CG_UIO_CALC
import GS_SM_SUMRIONIS_Calc,GS_SM_SUMRIORIS_Calcs
import GS_SM_SUMUIORIS_Calcs
import GS_SM_MCAR_02_MCAREST_Calc
import GS_SMPartsCalc1,GS_SM_MCAR,GS_SM_SUMMARCHDIO_Calcs
import GS_SM_PART_CALCs1
import GS_SM_SC300
import GS_SM_FC_MCAR_02_part
import GS_SM_CGSystemCabinetsFront
import GS_SM_Part_Sum_CGRG
import GS_SM_TSKUNI,GS_SM_Get_Parts_FSC
import GS_SM_Licenses_Calcs
import GS_SM_Rio_Ethernet_Cable_Parts
import GS_SM_Cabinet_count_parts,GS_SM_Comp_B_CNMPart_Calc
import GS_SMPartsCalc2
import GS_SM_CGRG_NAMUR_PARTS
import GS_SM_BOM_Parts
import GS_Part_CC_USCA01_Calc
import GS_Part_CC_UGIA01_Calc
import GS_SM_ID_MOD
import GS_SM_Shipping_Parts
#import GS_SM_Part_total_calcs
from math import ceil

Product.Attributes.GetByName('FC_RUSIO').AssignValue('0')
Product.Attributes.GetByName('Rusio_IotaR').AssignValue('0')
Product.Attributes.GetByName('Rusio_IotaNR').AssignValue('0')
Product.Attributes.GetByName('FC_TCNT').AssignValue('0')

parts_dict = {}
IOComp = GS_SMIOComponents.IOComponents(Product)
SUMRION = IOComp.getSumRion()
#Trace.Write(SUMRION)

Marshalling_Option = ''
contCabLeft = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Left')
### Leo starts CXDEV-8710
def get_float(val):
	if val:
		return float(val)
	return 0.0
dig_Input=Product.GetContainerByName("SM_IO_Count_Digital_Input_Cont")
dig_Output=Product.GetContainerByName('SM_IO_Count_Digital_Output_Cont')
installed_spare=Product.Attr("SM_CG_Percent_Installed_Spare").GetValue()
if installed_spare:
    installed_spare=float(installed_spare)/100
else:
    installed_spare=0
sum_1 = sum_2 = 0
total_qty=0
sum_tot=0
Tot_qty_FC_USCH01 = 0
spare_percent=0
cable_qty_L3 =0
spare_length=None

SM_CG_Universal_Marshalling = Product.GetContainerByName("SM_CG_Universal_Marshalling_Cabinet_Details")
for spare in SM_CG_Universal_Marshalling.Rows:
    spare_percent=float(spare['Percentage of Spare Space'])/100 if spare['Percentage of Spare Space'] else 0
    spare_length = spare.GetColumnByName('SIC cable length for RUSIO/PUIO/ PDIO').DisplayValue
    #if spare_percent:
        #spare_percent=float(spare_percent)/100
Part_Numbers=["FC-UIRH01","FC-UORH01"]
Sm_cont = Product.GetContainerByName('SM_CG_PartSummary_Cont')


if contCabLeft.Rows.Count > 0:
    Marshalling_Option = contCabLeft.Rows[0].GetColumnByName('Marshalling_Option').DisplayValue
if Marshalling_Option == "Universal Marshalling":
    for ip in dig_Input.Rows:
        if ip["Red (RLY)"] != "" or ip["Non Red (RLY)"] != '':
            if ip["Digital Input Type"] in ("SDI(1) 24Vdc UIO (0-5000)", "SDI(1) 24Vdc DIO (0-5000)"):
                if ip["Red (RLY)"] != 0 and ip["Non Red (RLY)"] != 0 :
                    sum_1 += get_float(ip["Red (RLY)"]) + get_float(ip["Non Red (RLY)"])
                    qty_ip = ceil((1 + (installed_spare)) * sum_1)
                    if qty_ip:
                        parts_dict["FC-UIRH01"] = {'Quantity': qty_ip, 'Description': 'SCA Adapter'}
            if ip["Digital Input Type"] == "SDI(1) 24Vdc UIO (0-5000)":
                var1 = ip["Red (RLY)"] if ip["Red (RLY)"] != "" else 0
                A = ceil ((1+(spare_percent))*(ceil ((1+(installed_spare)) * get_float(var1)/16)))
                if A:
                    sum_tot+=A
                    cable_qty_L3+=A
                var2 = ip["Non Red (RLY)"] if ip["Non Red (RLY)"] != "" else 0
                B = ceil ((1+(spare_percent))*(ceil ((1+(installed_spare)) * get_float(var2)/16)))
                if B:
                    sum_tot+=B
                    cable_qty_L3+=B
            if ip["Digital Input Type"] == "SDI(1) 24Vdc DIO (0-5000)":
                var3 = ip["Red (RLY)"] if ip["Red (RLY)"] != "" else 0
                C = ceil ((1+(spare_percent))*(ceil ((1+(installed_spare)) * get_float(var3)/16)))
                if C:
                    sum_tot+=C
                    Tot_qty_FC_USCH01+=C
                var4 = ip["Non Red (RLY)"] if ip["Non Red (RLY)"] != "" else 0
                D = ceil ((1+(spare_percent))*(ceil ((1+(installed_spare)) * get_float(var4)/16)))
                if D:
                    sum_tot+=D
                    Tot_qty_FC_USCH01+=D
    for op in dig_Output.Rows:
        if op["Red (RLY)"] != "" or op["Non Red (RLY)"] != '':
            if op["Digital Output Type"] in ("SDO(1) 24Vdc 500mA UIO (0-5000)", "SDO(1) 24Vdc 500mA DIO (0-5000)"):
                if op["Red (RLY)"] != 0 and op["Non Red (RLY)"] != 0:
                    sum_2 += get_float(op["Red (RLY)"]) + get_float(op["Non Red (RLY)"])
                    qty_op = ceil((1 + (installed_spare)) * sum_2)
                    if qty_op:
                        parts_dict["FC-UORH01"] = {'Quantity': qty_op, 'Description': 'SCA Adapter'}
        if op["Digital Output Type"] =="SDO(1) 24Vdc 500mA UIO (0-5000)":
            var5= op["Red (RLY)"] if op["Red (RLY)"] != "" else 0
            E = ceil ((1+(spare_percent))*(ceil ((1+(installed_spare)) * get_float(var5)/16)))
            if E:
                sum_tot+=E
                cable_qty_L3+=E
            var6= op["Non Red (RLY)"] if op["Non Red (RLY)"] != "" else 0
            F = ceil ((1+(spare_percent))*(ceil ((1+(installed_spare)) * get_float(var6)/16)))
            if F:
                sum_tot+=F
                cable_qty_L3+=F
        if op["Digital Output Type"] =="SDO(1) 24Vdc 500mA DIO (0-5000)":
            var7 = op["Red (RLY)"] if op["Red (RLY)"] != "" else 0 
            G = ceil ((1+(spare_percent))*(ceil ((1+(installed_spare)) * get_float(var7)/16)))
            if G:
                sum_tot+=G
                Tot_qty_FC_USCH01+=G
            var8=op["Non Red (RLY)"] if op["Non Red (RLY)"] != "" else 0
            H = ceil ((1+(spare_percent))*(ceil ((1+(installed_spare)) * get_float(var8)/16)))
            Trace.Write("--H = "+str(H))
            if H:
                sum_tot+=H
                Tot_qty_FC_USCH01+=H
    total_qty=int(sum_tot)
    parts_dict["FC-USCH01"] = {'Quantity': total_qty, 'Description': 'SCA Adapter'}
    ##########leo ends CXDEV-8710 ##########
    #CXCPQ-33022
    PTAQuantity = IOComp.getPTAQuantity()
    if PTAQuantity >0:
        parts_dict["CC-UPTA01"] = {'Quantity': PTAQuantity , 'Description': 'PTA - Pass Through Adapter'}
    #CXCPQ-33024
    AIAdapterQuantity = IOComp.getAIAdapterQuantity()
    if AIAdapterQuantity >0:
        parts_dict["FC-UAIA01"] = {'Quantity': AIAdapterQuantity , 'Description': 'SCA ANALOG INPUT'}
    #CXCPQ-33025
    AIAdapterSinkQuantity = IOComp.getAIAdapterSinkQuantity()
    if AIAdapterSinkQuantity >0:
        parts_dict["FC-UAIS01"] = {'Quantity': AIAdapterSinkQuantity , 'Description': 'SCA ANALOG INPUT SINK'}

SUMRIONIS = GS_SM_SUMRIONIS_Calc.SUMRIONIS_Calc(Product)
try:
    test = GS_SM_SUMRIORIS_Calcs.IOComponents(Product)
    SUMRIORIS= test.SUMRIORIS_value()
except Exception,e:
    SUMRIORIS=0
    Trace.Write("Error in GS_SM_SUMRIORIS_Calcs" + str(e))
#CXCPQ-31811
try:
    parts_dict = GS_SMPartsCalc1.get_parts(Product,parts_dict)
except Exception,e:
    Trace.Write("Error in GS_SMPartsCalc1" + str(e))# + " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))
#CXCPQ-33364,33365,33366,33368,33369
try:
    parts_dict = GS_SM_CG_RG_Parts.cabinet_part(Product,parts_dict)
except Exception,e:
    Trace.Write("Error in GS_SM_CG_RG_Parts" + str(e) )#+ " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))

#CXCPQ-32167,32168,32169,32170,32172
try:
    Qty_parts = GS_SM_Part_Sum_CGRG.get_parts(Product,parts_dict)
    Trace.Write("Value :"+str(Qty_parts))
except Exception,e:
    Trace.Write("Error GS_SM_Part_Sum_CGRG" + str(e))# + " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))
#CXCPQ-34292
try:
    Qty_parts = GS_SM_ID_MOD.get_MODID(Product,parts_dict)
    Trace.Write("Value :"+str(Qty_parts))
except Exception,e:
    Trace.Write("Error GS_SM_ID_MOD :" + str(e))# + " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))

try:
    attrs = GS_SM_CG_Component_Attribute.AttrStorage(Product)
except Exception,e:
    attrs = None
    Trace.Write("Error when Reading SM CG System Attributes: " + str(e) )#+ " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))
try:
    #SUMMARCHDIO=GS_SM_SUMMARCHDIO_Calcs.getSUMMARCHDIOValue(attrs)
    SUMMARSHUIO=GS_SM_CG_UIO_CALC.get_sum_marsh_uio(attrs)
    Trace.Write(SUMMARSHUIO)
except Exception,e:
    SUMMARSHUIO = 0
    Trace.Write("Error when Reading GS_SM_CG_UIO_CALC : " + str(e))# + " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))
#CXCPQ-31792
try:
    SUMMARCHDIO=GS_SM_SUMMARCHDIO_Calcs.getSUMMARCHDIOValue(Product)
    Trace.Write("SUMMARCHDIO:"+str(SUMMARCHDIO))
except Exception,e:
    #Trace.Write("Error when Reading GS_SM_SUMMARCHDIO_Calcs : " + str(e))# + " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))
    Trace.Write("Error when Reading GS_SM_SUMMARCHDIO_Calcs : " + str(e))# + " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))
#CXCPQ-31848,31851
try:
    parts_dict = GS_SM_TSKUNI.get_partstskuni(Product,parts_dict)
except Exception,e:
    Trace.Write("Error in GS_SM_TSKUNI: " + str(e))# + " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))
try:
    parts_dict = GS_SM_TSKUNI.get_partstspkuni(Product,parts_dict)
except Exception,e:
    Trace.Write("Error in GS_SM_TSKUNI: " + str(e) )#+ " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))
try:
    IOComp = GS_SMIOComponents.IOComponents(Product)
    SUMUIONPF, SUMUIORPF = IOComp.getUniversalIOCountRedNonRed()
except Exception,e:
    SUMUIORPF = 0
    SUMUIONPF = 0
    Trace.Write("Error in SUMUIORPF & SUMUIONPF Calc: " + str(e))# + " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))
SUMRIOR = 0
if attrs:
    try:
        SUMRIOR = GS_SM_CG_UIO_CALC.get_sum_red_io(attrs, SUMUIORPF)
    except Exception,e:
        SUMRIOR = 0
        Trace.Write("Error in GS_SM_CG_UIO_CALC: " + str(e))# + " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))

IOComp = GS_SM_SUMUIORIS_Calcs.IOComponents(Product)
try:
    SUMUIORIS = IOComp.SUMUIORIS_value()
except Exception,e:
    SUMUIORIS=0
    Trace.Write("Error in GS_SM_CG_UIO_CALC: " + str(e))

MCAREST = GS_SM_MCAR_02_MCAREST_Calc.MCAR_02_MCAREST_CG_RG_Calc(Product)
BCUFREST = m.ceil(MCAREST/7)
FDBCUFR = m.ceil(BCUFREST*5)
coqu=Product.GetContainerByName("SM_CG_Common_Questions_Cont")
p1=m.ceil((FDBCUFR+SUMRION+SUMRIONIS)/32.0)
if SUMRION+SUMRIONIS==0:
    qnt=p1+2*m.ceil((SUMRIOR+SUMRIORIS)/32.0)
    if coqu.Rows.Count > 0:
        if Product.GetContainerByName("SM_CG_Common_Questions_Cont").Rows[0].GetColumnByName("SM_Universal_IOTA").DisplayValue == "RUSIO":
            Product.Attr('FC_RUSIO').AssignValue(str(qnt))
elif SUMRION+SUMRIONIS>0:
    qnt=p1+2*m.ceil((SUMRIOR+SUMRIORIS)/32.0)
    if coqu.Rows.Count > 0:
        if Product.GetContainerByName("SM_CG_Common_Questions_Cont").Rows[0].GetColumnByName("SM_Universal_IOTA").DisplayValue == "RUSIO":
            Product.Attr('FC_RUSIO').AssignValue(str(qnt))

IOTAR = m.ceil((SUMRIOR+SUMRIORIS)/32.0)
IOTANR =m.ceil((FDBCUFR+SUMRION+SUMRIONIS)/32.0)
if coqu.Rows.Count > 0:
    if Product.GetContainerByName("SM_CG_Common_Questions_Cont").Rows[0].GetColumnByName("SM_Universal_IOTA").DisplayValue == "RUSIO":
        Product.Attr('Rusio_IotaR').AssignValue(str(IOTAR))
        Product.Attr('Rusio_IotaNR').AssignValue(str(IOTANR))
IOTAR=int(float(Product.Attr('Rusio_IotaR').GetValue()))
IOTANR=int(float(Product.Attr('Rusio_IotaNR').GetValue()))
#Trace.Write("iotar: "+str(IOTAR))
#Trace.Write("iotanr: "+str(IOTANR))
#CXCPQ-31175
iota=""
if coqu.Rows.Count > 0:
    iota = Product.GetContainerByName("SM_CG_Common_Questions_Cont").Rows[0].GetColumnByName("SM_Universal_IOTA").DisplayValue
if iota == "RUSIO":
    try:
        parts_dict,MCAR = GS_SM_MCAR.get_mcar(Product,IOTANR,IOTAR,parts_dict)
        Trace.Write("---------------------------MCAR : "+str(MCAR))
    except Exception,e:
        #Trace.Write("Error in GS_SM_MCAR: " + str(e))
        Trace.Write("Error when Reading GS_SM_MCAR: " + str(e))# + " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))
try:
    total_rio_cabinet_summary = GS_Load_SM_RIO_Cab_Summary.getLoadSMRIOCabSummary(Product)
    Trace.Write(total_rio_cabinet_summary)
except Exception,e:
    total_rio_cabinet_summary = None
    Trace.Write("Error when Reading SM remote group Attributes: " + str(e))# + " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))

try:
    attr = GS_SM_ReadPart_Attrs.AttrStorage(Product)
    Trace.Write("Nimish : "+str(attr))
except Exception,e:
    attr = None
    Trace.Write("Error when Reading GS_SM_ReadPart_Attrs: " + str(e))# + " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))

try:
    IOComp = GS_SMIOComponents.IOComponents(Product)
    SUMUIONPF, SUMUIORPF = IOComp.getUniversalIOCountRedNonRed()
    GPCS =D.Ceiling(SUMUIONPF/16.0)+D.Ceiling(SUMUIORPF/16.0)
    Trace.Write('GPCS : '+str(GPCS))
except Exception,e:
    Trace.Write("Error when Reading GS_SMIOComponents : " + str(e) )#+ " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))


if qnt>0:
    if Product.GetContainerByName("SM_CG_Common_Questions_Cont").Rows[0].GetColumnByName("SM_Universal_IOTA").DisplayValue=="RUSIO":
        parts_dict["FC-RUSIO-3224"] = {'Quantity' : qnt , 'Description': 'SM RIO module 32 ch 24Vdc'}
if IOTAR>0:
    if Product.GetContainerByName("SM_CG_Common_Questions_Cont").Rows[0].GetColumnByName("SM_Universal_IOTA").DisplayValue=="RUSIO":
        parts_dict["FC-IOTA-R24"] = {'Quantity' : IOTAR , 'Description': 'SM RIO redundant termination assembly'}
    
if IOTANR>0:
    if Product.GetContainerByName("SM_CG_Common_Questions_Cont").Rows[0].GetColumnByName("SM_Universal_IOTA").DisplayValue=="RUSIO":
        parts_dict["FC-IOTA-NR24"] = {'Quantity' : IOTANR , 'Description': 'SM RIO non-redundant termination assembly'}
#CXCPQ-31134
FC_PUIO01 =Product.Attr('FC_PUIO').GetValue()
if coqu.Rows.Count > 0:
    if Product.GetContainerByName("SM_CG_Common_Questions_Cont").Rows[0].GetColumnByName("SM_Universal_IOTA").DisplayValue=="PUIO":
        if FC_PUIO01:
            parts_dict["FC-PUIO01"] = {'Quantity' : int(FC_PUIO01) , 'Description': 'SC SAFETY UIO IOM 24VDC, 32CH'}
    
#CXCPQ-31136
FC_PDIO01 = Product.Attr('FC_PDIO').GetValue()
if FC_PDIO01:
    parts_dict["FC-PDIO01"] = {'Quantity' : int(FC_PDIO01) , 'Description': 'SC SAFETY DIO IOM 24VDC, 32CH'}
    
#CXCPQ- 31139
FC_TUIO11 = int(float(Product.Attr('FC_TUIO').GetValue())) if Product.Attr('FC_TUIO').GetValue() != '' else 0
if FC_TUIO11:
    if Product.GetContainerByName("SM_CG_Common_Questions_Cont").Rows[0].GetColumnByName("SM_Universal_IOTA").DisplayValue=="PUIO":
        parts_dict["FC-TUIO11"] = {'Quantity' : int(FC_TUIO11) , 'Description': 'SC IOTA PUIO REDUNDANT'}
#CXCPQ-31140
FC_TDIO11 = int(float(Product.Attr('FC_TDIO').GetValue())) if Product.Attr('FC_TDIO').GetValue() != '' else 0
if FC_TDIO11:
    parts_dict["FC-TDIO11"] = {'Quantity' : int(FC_TDIO11) , 'Description': 'SC IOTA PDIO REDUNDANT'}
#TCNT11 = 0 # CXCPQ-31335 need to add value(LAHU)
try:
    atr=GS_part_add_IO_value.IOvalues(Product)
    a,b,c,d=atr.io_mon()
    TDOL = D.Ceiling((a+c)/7)+D.Ceiling((b+d)/7)
except:
    Trace.Write("Error when Reading GS_part_add_IO_value : " + str(e))# + " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))
try:
    parts_dict = sm_part_add_calcs.getCGParts(FC_PUIO01,FC_PDIO01,TDOL,GPCS, Product, parts_dict)
except Exception,e:
    Trace.Write("Error in sm_part_add_calcs: " + str(e))# + " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))
#CXCPQ-31335
try:
    parts_dict, TCNT11 = GS_SM_SC300.get_TCNT(Product, parts_dict)
    Product.Attr('FC_TCNT').AssignValue(str(TCNT11))
    Trace.Write("Part_FC_TCNT: "+str(TCNT11))
except Exception,e:
    Trace.Write("Error in GS_SM_SC300: " + str(e))# + " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))
#CXCPQ-31516
try:
    TCNT111,TCNT12=GS_SM_SC300.get_TCNT(Product,parts_dict)
    parts_dict = GS_SM_Part_Calcs.get_TCNT11(parts_dict,TCNT12)
except Exception,e:
    Trace.Write("Error in GS_SM_Part_attributes: " + str(e))# + " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))
try:
    parts_dict = GS_SM_Part_Calcs.get_parts(Product,total_rio_cabinet_summary, parts_dict)
except Exception,e:
    Trace.Write("Error in GS_SM_Part_Calcs: " + str(e))# + " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))

try:
    parts_dict = GS_SM_Part_Calcs.get_parts1(Product,parts_dict)
except Exception,e:
    Trace.Write("Error in GS_SM_Part_Calcs: " + str(e))# + " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))
#CXCPQ-31854
try:
    parts_dict = GS_SM_Part_Calcs.get_parts2(Product,parts_dict)
except Exception,e:
    Trace.Write("Error in GS_SM_Part_Calcs: " + str(e))# + " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))
#CXCPQ-31812
try:
    parts_dict = GS_SM_Part_Calcs.get_FC_TDIO52(attrs,parts_dict,SUMMARCHDIO)
except Exception,e:
    Trace.Write("Error in GS_SM_Part_Calcs: " + str(e))# + " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))
#Trace.Write("blue:"+str(GS_SM_Part_Calcs.get_FC_TDIO52(parts_dict,SUMMARCHDIO)))
#CXCPQ-31793
try:
    ##pass
    parts_dict = GS_SM_Part_Calcs.get_FC_TUIO52(attrs,SUMMARSHUIO,parts_dict)
except Exception,e:
    Trace.Write("Error in GS_SM_Part_Calcs: " + str(e))# + " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))
#CXCPQ-33265
try:
    parts_dict = GS_SM_Part_Calcs.get_partsiota(parts_dict,IOTAR,IOTANR,FC_TUIO11,FC_TDIO11)
except Exception,e:
    Trace.Write("Error in GS_SM_Part_Calcs: " + str(e))# + " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))

#CXCPQ-31855
try:
    parts_dict = sm_part_add_calcs.get_parts3(Product,parts_dict)
except Exception,e:
    Trace.Write("Error in sm_part_add_calcs.get_parts3: " + str(e))# + " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))
try:
    parts_dict = sm_part_add_calcs.filler_plate(Product,parts_dict)
except Exception,e:
    Trace.Write("Error in sm_part_add_calcs.filler_plate: " + str(e))# + " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))
try:
    parts_dict = sm_part_add_calcs.cabinet_part(Product,parts_dict)
except Exception,e:
    Trace.Write("Error in sm_part_add_calcs.cabinet_part: " + str(e))# + " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))
try:
    parts_dict = sm_part_add_calcs.FC_MCAR_02(FC_TUIO11,FC_TDIO11,TCNT11,Product,parts_dict)
except Exception,e:
    Trace.Write("Error in sm_part_add_calcs.get_parts3: " + str(e))# + " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))

#CXCPQ-31814 to CXCPQ-31823
try:
    parts_dict =GS_SM_PART_CALCs1.Get_Parts(Product,parts_dict)
except Exception,e:
    Trace.Write("Error in GS_SM_PART_CALCs: " + str(e))# + " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))

#CXCPQ-33504
if coqu.Rows.Count > 0:
    if Product.GetContainerByName("SM_CG_Common_Questions_Cont").Rows[0].GetColumnByName("SM_Universal_IOTA").DisplayValue=="RUSIO":
        try:
            parts_dict =GS_SM_FC_MCAR_02_part.get_fc_mcar_02(Product,IOTANR,IOTAR,FC_TDIO11,TCNT11,parts_dict)
        except Exception,e:
            Trace.Write("Error in GS_SM_FC_MCAR_02_part: " + str(e))# + " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))
#CXCPQ-33234
try:
    parts_dict =GS_SM_Licenses_Calcs.SM_Licenses_Calcs(Product,parts_dict,TCNT11)
except Exception,e:
    Trace.Write("Error in GS_SM_Licenses_Calcs: " + str(e))# + " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))
#CXCPQ-33029
try:
    parts_dict = GS_SM_CGRG_NAMUR_PARTS.get_DIDO_SL_Namur_DI(Product, parts_dict)
except Exception,e:
    Trace.Write("Error in GS_SM_CGRG_NAMUR_PARTS : " + str(e))# + " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))
#CXCPQ-33030
try:
    parts_dict = GS_SM_CGRG_NAMUR_PARTS.get_UIO_SL_sftyNamur_DI(Product, parts_dict)
except Exception,e:
    Trace.Write("Error in GS_SM_CGRG_NAMUR_PARTS : " + str(e) )#+ " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))
#CXCPQ-33031
try:
    parts_dict = GS_SM_CGRG_NAMUR_PARTS.get_UIO_SL_sftyNamur_DO(Product, parts_dict)
except Exception,e:
    Trace.Write("Error in GS_SM_CGRG_NAMUR_PARTS : " + str(e))# + " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))




if attr:
    try:
        ##pass
        parts_dict = GS_SM_Part_Calcs.get_cg_parts(Product, attr, attrs, parts_dict, total_rio_cabinet_summary)
    except Exception,e:
        Trace.Write("Error in GS_SM_Part_Calcs: " + str(e))# + " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))

    #Mocha parts
    parts_dict = GS_SMPartsCalc.getCGParts(Product, parts_dict)
    #CXCPQ-31795
    parts_dict = GS_SMPartsCalc.getHardwiredMarshallingParts(Product, parts_dict)

    #CXCPQ-31159
    try:
        parts_dict = GS_Power_Supply_calcs.getPowerSupplyPart(Product, parts_dict)
    except Exception,e:
        Trace.Write("Error in GS_Power_Supply_calcs: " + str(e))# + " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))
    #Trace.Write("debugging: " + str(parts_dict))

    # #CXCPQ-31191 - First Call
    try:
        parts_dict = GS_Power_Supply_calcs1.getPwrSupParts(Product, parts_dict)
    except Exception,e:
        Trace.Write("Error in GS_Power_Supply_calcs1: " + str(e))# + " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))
    Trace.Write("debugging: " + str(parts_dict))
    #CXCPQ-31865
    try:
        parts_dict = GS_Power_Supply_calcs1.Get_Parts_Sic_length(Product,parts_dict)
    except Exception,e:
        Trace.Write("Error in GS_Power_Supply_calcs1: " + str(e))# + " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))
    #CXCPQ-31844,31845,31846
    '''try:
        parts_dict = GS_Power_Supply_calcs1.Get_Sic_length(Product,parts_dict)
    except Exception,e:
        Trace.Write("Error in GS_Power_Supply_calcs1: " + str(e) + " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))'''
    
    #CXCPQ-33622
    try:
        parts_dict = GS_SM_Rio_Ethernet_Cable_Parts.Rio_Ethernet_Cable_Parts(Product, parts_dict)
    except Exception,e:
        Trace.Write("Error in GS_SM_Rio_Ethernet_Cable_Parts: " + str(e))# + " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))
    
    #CXCPQ-33036
    try:
        parts_dict = GS_Part_CC_USCA01_Calc.Part_CC_USCA01_Calc(Product, parts_dict)
    except Exception,e:
        Trace.Write("Error in GS_Part_CC_USCA01_Calc: " + str(e))# + " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))
    
    # commented as the logic moved to add part function in GS_SM_Part_Calcs module which is called later in this script
    '''#CXCPQ-33046
    try:
        parts_dict = GS_Part_FC_USCA01_Calc.Part_FC_USCA01_Calc(Product, parts_dict)
    except Exception,e:
        Trace.Write("Error in GS_Part_FC_USCA01_Calc: " + str(e))# + " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))'''
        
    ##CXCPQ-33048
    try:
        parts_dict = GS_Part_CC_UGIA01_Calc.Part_CC_UGIA01_Calc(Product, parts_dict)
    except Exception,e:
        Trace.Write("Error in GS_Part_CC_UGIA01_Calc: " + str(e))# + " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))
        
    #Trace.Write("debugging: " + str(parts_dict))
    #GS_SM_Part_Update.execute(Product, 'SM_CG_PartSummary_Cont', parts_dict)
#CXCPQ-31813,31824,31839,31841
try:
    parts_dict = GS_SMPartsCalc2.get_partz(Product,parts_dict)
except Exception,e:
    Trace.Write("Error in GS_SMPartsCalc2: " + str(e))# + " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))

try:
    parts_dict = GS_SMPartsCalc1.cg_cabinet_access(Product,parts_dict)
except Exception,e:
    Trace.Write("Error in GS_SMPartsCalc1" + str(e))# + " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))
Trace.Write("debugging: " + str(parts_dict))
##GS_SM_Part_Update.execute(Product, 'SM_CG_PartSummary_Cont', parts_dict)

try:
    cabinet_count, power_supply, switches = GS_SMPartsCalc.getNumberOfCGCabinet(Product)
except Exception,e:
    cabinet_count, power_supply, switches = 0, 0, 0

if cabinet_count:
    parts_dict = GS_SM_Cabinet_count_parts.getCGParts(Product, parts_dict, cabinet_count, power_supply, switches)


#CXCPQ- 33639
A_Comp={}
try:
    A_Comp= GS_SM_CompA1_Calcs.get_CompA1(Product)
    parts_dict=GS_SM_CompA1_Calcs.CCI_HSE(A_Comp,Product,parts_dict)
    #Trace.Write("Shivani:"+str(parts_dict))
except Exception,e:
    Trace.Write("Error in GS_SM_CompA1_Calcs" + str(e) )#+ " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))
#CXCPQ-33032
try:
    parts_dict = GS_SM_CGRG_NAMUR_PARTS.get_FC_UDOF01(Product,parts_dict)
except Exception,e:
    Trace.Write("Error in GS_SM_CGRG_NAMUR_PARTS: " + str(e))# + " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))
    
#CXCPQ-33026
try:
    parts_dict = GS_SM_BOM_Parts.get_FC_UDI501(Product,parts_dict)
except Exception,e:
    Trace.Write("Error in GS_SM_BOM_Parts: " + str(e))# + " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))
#CXCPQ-33027
try:
    parts_dict = GS_SM_BOM_Parts.get_FC_UIR501(Product,parts_dict)
except Exception,e:
    Trace.Write("Error in GS_SM_BOM_Parts: " + str(e) )#+ " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))
#CXCPQ-33028
try:
    parts_dict = GS_SM_BOM_Parts.get_FC_UDIR01(Product,parts_dict)
except Exception,e:
    Trace.Write("Error in GS_SM_BOM_Parts: " + str(e))# + " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))

    
#CXCPQ-33078,33071
cab, powerSupply, switches = GS_SMPartsCalc.getNumberOfCGCabinet(Product)
try:
    parts_dict = GS_SM_Get_Parts_FSC.Get_CG_Parts_FSC(Product,parts_dict)
except Exception,e:
    Trace.Write("Error in GS_SM_Get_Parts_FSC: " + str(e))# + " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))

#CXCPQ-33671
try:
    a_comp=GS_SM_CompA1_Calcs.get_CompA1(Product)
    #B=GS_SM_Comp_B_CNMPart_Calc.Comp_B_CNMPart_Calc(Product)
    parts_dict=GS_SM_CompA1_Calcs.get_CompC(parts_dict,Product,a_comp)
    #Trace.Write("Shivani:"+str(parts_dict))
except Exception,e:
    Trace.Write("Error in GS_SM_CompA1_Calcs" + str(e))# + " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))
# Sprint 16 parts script - Nimish
try:
    parts_dict = GS_SM_CG_Part_Summary.get_parts(Product, parts_dict)
except Exception,e:
    Trace.Write("Error in GS_SM_CG_Part_Summary: " + str(e))# + " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))

Trace.Write("debugging: " + str(parts_dict))

# Sprint 18
try:
    parts_dict = GS_SM_Part_Calcs.addParts(attrs, parts_dict, Tot_qty_FC_USCH01,cable_qty_L3)
except Exception, e:
    #Trace.Write("Error in GS_SM_Part_Calcs addParts call: " + str(e))# + " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))
    Trace.Write("Error in GS_SM_Part_Calcs addParts call: " + str(e) )#+ " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))

# #CXCPQ-31191 - First Call
try:
    parts_dict = GS_Power_Supply_calcs1.getPwrSupParts(Product, parts_dict, True)
except Exception,e:
    Trace.Write("Error in GS_Power_Supply_calcs1: " + str(e))# + " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))

try:
    calculated_loads = GS_SM_Part_Calcs.calculate_loads(parts_dict)
    #Product.Messages.Add("Calculated loads are " + RestClient.SerializeToJson(calculated_loads))
except Exception,e:
    Trace.Write("Error in calculate_loads" + str(e) )#+ " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))

#CXCPQ-46227 - FAN Parts
cabinets = 0
if 'FS-BCU-0036' in parts_dict.keys():
    cabinets = parts_dict['FS-BCU-0036']['Quantity']
elif 'FS-BCU-0038' in parts_dict.keys():
    cabinets = parts_dict['FS-BCU-0038']['Quantity']
if cabinets > 0:
    qty = cabinets*2
    parts_dict['51109516-100'] = {'Quantity' : qty, 'Description': ''}
    parts_dict['51199947-275'] = {'Quantity' : qty, 'Description': ''}

#CXCPQ-47876 and CXCPQ-47877
try:
    parts_dict = GS_SM_Shipping_Parts.SM_Shipping_Parts_CG_RG(Product, parts_dict)
    parts_dict = GS_SM_Shipping_Parts.SM_Shipping_Parts_CG(Product, parts_dict)
except Exception,e:
    Trace.Write("GS_SM_Shipping_Parts : " + str(e))# + " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))

Trace.Write("parts_dict===+===="+str(parts_dict))
def sint(ip):
	if ip:
		ip = int(ip)
	else:
		return 0
	return ip

def check_cont(col_dict):
	cols=[]
	for cont,cols in col_dict.items():
		if Product.GetContainerByName(cont):
			for data in Product.GetContainerByName(cont).Rows:
				for colums in cols:
					if sint(data[colums])>0:
						return True
	return False

valid_cols=['Red (IS)','Non Red (IS)','Red (NIS)','Non Red (NIS)']
valid_col = ['Red (IS)','Non Red (IS)','Red (NIS)','Non Red (NIS)','Red (RLY)','Non Red (RLY)']
NMR_Cont = ['Red_SIL2_RLY','Non_Red_SIL2_RLY','Red_SIL3_RLY','Non_Red_SIL3_RLY','Red_NMR','Non_Red_NMR','Red_NMR_Safety','Non_Red_NMR_Safety']
col_dict={'SM_IO_Count_Analog_Output_Cont':valid_cols,'SM_IO_Count_Analog_Input_Cont':valid_cols,'SM_IO_Count_Digital_Output_Cont':valid_col,'SM_IO_Count_Digital_Input_Cont':valid_col,'SM_CG_DI_RLY_NMR_Cont':NMR_Cont,'SM_CG_DO_RLY_NMR_Cont':NMR_Cont}

Trace.Write('-->'+str(check_cont(col_dict)))
if not check_cont(col_dict):
	for data in parts_dict.values():
		if data['Quantity'] in (0,0.0):
			data['Quantity']=0
			#data['Quantity']=0
GS_SM_Part_Update.execute(Product, 'SM_CG_PartSummary_Cont', parts_dict)
ScriptExecutor.Execute("PS_SM_CG_LI_Part_Summary")