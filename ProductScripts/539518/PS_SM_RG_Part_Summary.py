#Commented some part because getting error
import System.Decimal as D
import GS_SM_ReadPart_Attrs
import GS_SM_Part_Calcs
import sm_part_add_calcs,GS_SM_identifier_position_PARTS
import GS_SMIOComponents,GS_Load_SM_RIO_Cab_Summary
import GS_SM_REMOTE_PART_SM #32148
import GS_SM_Part_Update
import GS_Power_Supply_calcs,GS_SM_CompA1_Calcs
import GS_Power_Supply_calcs1
import GS_part_add_IO_value#, GS_SM_Load_SM_RIO_cabinet_summary_Calc
import GS_SMPartsCalc, GS_SMIdentifierModifierPartsCalc
import GS_SM_CG_RG_Parts,SM_Identifier_Position_Calcs
import math as m
import GS_SM_CG_Component_Attribute,GS_SM_RG_Identifier_Modifier_Parts
# import ProductUtil as pu
import GS_SM_CG_UIO_CALC
import GS_SM_SUMRIONIS_Calc
import GS_SM_SUMUIORIS_Calcs
import GS_SM_MCAR_02_MCAREST_Calc, GS_SM_MCAR
import GS_SMPartsCalc1
import GS_SM_PART_CALCs1,GS_SM_SUMMARCHDIO_Calcs
import GS_SM_FC_MCAR_02_part
# import GS_SM_CGSystemCabinetsFront
import GS_SM_Part_Sum_CGRG,GS_SM_SUMRIORIS_Calcs
import GS_SM_TSKUNI,GS_SM_Get_Parts_FSC
import GS_SM_RG_Licenses_Calcs#,GS_SM_Comp_B_CNMPart_Calc
import GS_SM_Rio_Ethernet_Cable_Parts
import GS_SMPartsCalc2
import GS_SM_Cabinet_count_parts
import GS_SM_Identifier_Modifier_Part_Calcs,GS_SM_RG_Identifier_Modifier_STR_part
import GS_SM_CGRG_NAMUR_PARTS,GS_SM_BOM_Parts
import GS_Part_CC_USCA01_Calc
import GS_Part_CC_UGIA01_Calc,GS_SM_Identifier_POSITIONS
import GS_SM_ID_MOD
import GS_SM_ID_MOD_II
import GS_SM_ID_MOD_III
import GS_SM_RG_getexcode
import GS_SM_get_FS_CCI_HSE_20,GS_SM_Identifier1_Parts
import GS_SM_Shipping_Parts
from math import ceil
parts_dict = {}
Product.Attributes.GetByName('FC_RG_RUSIO').AssignValue('0')
Product.Attributes.GetByName('RUSIO_RG_IOTAR').AssignValue('0')
Product.Attributes.GetByName('RUSIO_RG_IOTANR').AssignValue('0')
IOComp = GS_SMIOComponents.IOComponents(Product)
SUMRION = IOComp.getSumRion()
#Trace.Write(SUMRION)

### Leo starts CXDEV-8710
def get_float(val):
	if val:
		return float(val)
	return 0.0
installed_spare=0
sum_1 = sum_2 = 0
total_qty=0
sum_tot=0
spare_percent=0
Tot_qty_FC_USCH01 = 0
cable_qty_L3 =0
spare_length=None
dig_Input=Product.GetContainerByName("SM_RG_IO_Count_Digital_Input_Cont")
dig_Output=Product.GetContainerByName('SM_RG_IO_Count_Digital_Output_Cont')
SM_RG_Cabinet_Details_Cont=Product.GetContainerByName("SM_RG_Cabinet_Details_Cont")
for spare in SM_RG_Cabinet_Details_Cont.Rows:
    installed_spare=float(spare['SM_Percent_Installed_Spare_IO'])/100 if spare['SM_Percent_Installed_Spare_IO'] else 0

SM_RG_Universal_Marshalling = Product.GetContainerByName("SM_RG_Universal_Marshalling_Cabinet_Details")
for spare in SM_RG_Universal_Marshalling.Rows:
    spare_percent=float(spare['Percentage of Spare Space'])/100 if spare['Percentage of Spare Space'] else 0
    spare_length = spare.GetColumnByName('SIC cable length for RUSIO/PUIO/ PDIO').DisplayValue

Marshalling_Option = ''
if Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows.Count > 0:
    Marshalling_Option = Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('Marshalling_Option').DisplayValue
Enclosure_Type = Product.Attr('SM_RG_Enclosure_Type').GetValue()
if Enclosure_Type == 'Cabinet' and Marshalling_Option == "Universal Marshalling":
    for ip in dig_Input.Rows:
        if ip["Red_RLY"] != "" or ip["Non_Red_RLY"] != '':
            if ip["Digital_Input_Type"] in ("SDI(1) 24Vdc UIO  (0-5000)", "SDI(1) 24Vdc DIO  (0-5000)"):
                if ip["Red_RLY"] != 0 and ip["Non_Red_RLY"] != 0 :
                    sum_1 += get_float(ip["Red_RLY"]) + get_float(ip["Non_Red_RLY"])
                    qty_ip = ceil((1 + (installed_spare)) * sum_1)
                    if qty_ip:
                        parts_dict["FC-UIRH01"] = {'Quantity': qty_ip, 'Description': 'SCA Adapter'}
            if ip["Digital_Input_Type"] == "SDI(1) 24Vdc UIO  (0-5000)":
                var1 = ip["Red_RLY"] if ip["Red_RLY"] != "" else 0
                A = ceil ((1+(spare_percent))*(ceil ((1+(installed_spare)) * get_float(var1)/16)))
                if A:
                    sum_tot+=A
                    cable_qty_L3+=A
                var2 = ip["Non_Red_RLY"] if ip["Non_Red_RLY"] != "" else 0
                B = ceil ((1+(spare_percent))*(ceil ((1+(installed_spare)) * get_float(var2)/16)))
                if B:
                    sum_tot+=B
                    cable_qty_L3+=B
            if ip["Digital_Input_Type"] == "SDI(1) 24Vdc DIO  (0-5000)":
                var3 = ip["Red_RLY"] if ip["Red_RLY"] != "" else 0
                C = ceil ((1+(spare_percent))*(ceil ((1+(installed_spare)) * get_float(var3)/16)))
                if C:
                    sum_tot+=C
                    Tot_qty_FC_USCH01+=C
                var4 = ip["Non_Red_RLY"] if ip["Non_Red_RLY"] != "" else 0
                D = ceil ((1+(spare_percent))*(ceil ((1+(installed_spare)) * get_float(var4)/16)))
                if D:
                    sum_tot+=D
                    Tot_qty_FC_USCH01+=D
    for op in dig_Output.Rows:
        if op["Red_RLY"] != "" or op["Non_Red_RLY"] != '':
            if op["Digital_Output_Type"] in ("SDO(1) 24Vdc 500mA UIO  (0-5000)", "SDO(1) 24Vdc 500mA DIO  (0-5000)"):
                if op["Red_RLY"] != 0 and op["Non_Red_RLY"] != 0:
                    sum_2 += get_float(op["Red_RLY"]) + get_float(op["Non_Red_RLY"])
                    qty_op = ceil((1 + (installed_spare)) * sum_2)
                    if qty_op:
                        parts_dict["FC-UORH01"] = {'Quantity': qty_op, 'Description': 'SCA Adapter'}
        if op["Digital_Output_Type"] =="SDO(1) 24Vdc 500mA UIO  (0-5000)":
            var5= op["Red_RLY"] if op["Red_RLY"] != "" else 0
            E = ceil ((1+(spare_percent))*(ceil ((1+(installed_spare)) * get_float(var5)/16)))
            if E:
                sum_tot+=E
                cable_qty_L3+=E
            var6= op["Non_Red_RLY"] if op["Non_Red_RLY"] != "" else 0
            F = ceil ((1+(spare_percent))*(ceil ((1+(installed_spare)) * get_float(var6)/16)))
            if F:
                sum_tot+=F
                cable_qty_L3+=F
        if op["Digital_Output_Type"] =="SDO(1) 24Vdc 500mA DIO  (0-5000)":
            var7 = op["Red_RLY"] if op["Red_RLY"] != "" else 0 
            G = ceil ((1+(spare_percent))*(ceil ((1+(installed_spare)) * get_float(var7)/16)))
            if G:
                sum_tot+=G
                Tot_qty_FC_USCH01+=G
            var8=op["Non_Red_RLY"] if op["Non_Red_RLY"] != "" else 0
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
        parts_dict["CC-UPTA01"] = {'Quantity' : PTAQuantity , 'Description': 'PTA - Pass Through Adapter'}
    #CXCPQ-33024
    AIAdapterQuantity = IOComp.getAIAdapterQuantity()
    if AIAdapterQuantity >0:
        parts_dict["FC-UAIA01"] = {'Quantity' : AIAdapterQuantity , 'Description': 'SCA ANALOG INPUT'}
    #CXCPQ-33025
    AIAdapterSinkQuantity = IOComp.getAIAdapterSinkQuantity()
    if AIAdapterSinkQuantity >0:
        parts_dict["FC-UAIS01"] = {'Quantity' : AIAdapterSinkQuantity , 'Description': 'SCA ANALOG INPUT SINK'}
elif Enclosure_Type != 'Cabinet':
    #CXCPQ-33310
    parts_dict = GS_SMIdentifierModifierPartsCalc.getFCTDIO11(Product, parts_dict)
    #CXCPQ-33321
    parts_dict = GS_SMIdentifierModifierPartsCalc.getFCTDIO51(Product, parts_dict)
    #CXCPQ-32664
    parts_dict = GS_SMIdentifierModifierPartsCalc.getFCTUIO11(Product, parts_dict)
    #CXCPQ-33991
    parts_dict = GS_SMIdentifierModifierPartsCalc.getFCMCC003(Product, parts_dict)
    #CXCPQ-103118
    parts_dict = GS_SMIdentifierModifierPartsCalc.getFCMCAR01(Product, parts_dict)
    #CXCPQ-32672
    parts_dict = GS_SMIdentifierModifierPartsCalc.getFCPDIO01(Product, parts_dict)
    #CXCPQ-33313
    parts_dict = GS_SMIdentifierModifierPartsCalc.getFCPUIO01(Product, parts_dict)
SUMRIONIS = GS_SM_SUMRIONIS_Calc.SUMRIONIS_Calc(Product)
SUMRIONIS = GS_SM_SUMRIONIS_Calc.SUMRIONIS_Calc(Product)
test = GS_SM_SUMRIORIS_Calcs.IOComponents(Product)
SUMRIORIS= test.SUMRIORIS_value()
try:
    parts_dict = GS_SM_RG_Identifier_Modifier_STR_part.get_identifier_Boot(Product,parts_dict)
except Exception,e:
    Trace.Write("Error in GS_SM_RG_Identifier_Modifier_STR_part.get_identifier_Boot(Product,parts_dict): " + str(e) )
#CXCPQ-33990
try:
    parts_dict = GS_SM_RG_Identifier_Modifier_Parts.get_identifier_UGIA01(Product,parts_dict)
except Exception,e:
    Trace.Write("Error in GS_SM_RG_Identifier_Modifier_Parts.get_identifier_UGIA01" + str(e) )

#CXCPQ-34222
try:
    parts_dict = GS_SM_Identifier_POSITIONS.get_identifier_UPTA01(Product,parts_dict)
except Exception,e:
    Trace.Write("Error in GS_SM_Identifier_POSITIONS.get_identifier_UPTA01" + str(e) )
#CXCPQ-31811
try:
    parts_dict = GS_SMPartsCalc1.get_parts1(Product,parts_dict)
except Exception,e:
    Trace.Write("Error in GS_SMPartsCalc1" + str(e) )
'''try:
    parts_dict = GS_SMPartsCalc1.rg_cabinet_access(Product,parts_dict)
except Exception,e:
    Trace.Write("Error in GS_SMPartsCalc1" + str(e) )'''
#CXCPQ-32167, 32168, 32169, 32170, 32172
try:
    parts_dict = GS_SM_Part_Sum_CGRG.get_parts(Product,parts_dict)
except Exception,e:
    Trace.Write("Error in GS_SM_Part_Sum_CGRG :" + str(e) )
#CXCPQ-34292
try:
    parts_dict = GS_SM_ID_MOD.get_MODID(Product,parts_dict)
except Exception,e:
    Trace.Write("Error in GS_SM_ID_MOD :" + str(e) )
#CXCPQ-34293
try:
    parts_dict = GS_SM_ID_MOD_II.get_MODID(Product,parts_dict)
except Exception,e:
    Trace.Write("Error in GS_SM_ID_MOD_II :" + str(e) )
#CXCPQ-34295
try:
    parts_dict = GS_SM_ID_MOD_III.get_MODID(Product,parts_dict)
except Exception,e:
    Trace.Write("Error in GS_SM_ID_MOD_III :" + str(e) )
#CXCPQ- 33364,33365,33366,33368,33369
try:
    parts_dict = GS_SM_CG_RG_Parts.cabinet_part(Product,parts_dict)
except Exception,e:
    Trace.Write("Error in GS_SM_CG_RG_Parts :" + str(e) )
#CXCPQ-34245,34240
try:
    parts_dict = GS_SM_Identifier1_Parts.identifier_Modifier1(Product,parts_dict)
    #Trace.Write("Anjani1:"+str(parts_dict))
except Exception,e:
    Trace.Write("Error in GS_SM_Identifier1_Parts :" + str(e) )
#CXCPQ-31814 to CXCPQ-31823
try:
    parts_dict = GS_SM_PART_CALCs1.Get_Parts(Product,parts_dict)
except Exception,e:
    Trace.Write("Error in GS_SM_PART_CALCs1" + str(e) )
#CXCPQ-32663
try:
    parts_dict = GS_SM_RG_Identifier_Modifier_Parts.get_identifier_Modifier(Product,parts_dict)
except Exception,e:
    Trace.Write("Error in GS_SM_RG_Identifier_Modifier_Parts" + str(e) )
try:
    attrs = GS_SM_CG_Component_Attribute.AttrStorage(Product)
except Exception,e:
    attrs = None
    Trace.Write("Error when Reading SM CG System Attributes: " + str(e) )
try:
    IOComp = GS_SMIOComponents.IOComponents(Product)
    SUMUIONPF, SUMUIORPF = IOComp.getUniversalIOCountRedNonRed()
except Exception,e:
    SUMUIORPF = 0
    SUMUIONPF = 0
    Trace.Write("Error in SUMUIORPF & SUMUIONPF Calc: " + str(e) )
#CXCPQ-31792
try:
    SUMMARCHDIO=GS_SM_SUMMARCHDIO_Calcs.getSUMMARCHDIOValue(Product)
    Trace.Write("SUMMARCHDIO:"+str(SUMMARCHDIO))
except Exception,e:
    #Product.ErrorMessages.Add("Error when Reading GS_SM_SUMMARCHDIO_Calcs : " + str(e) )
    Trace.Write("Error when Reading GS_SM_SUMMARCHDIO_Calcs : " + str(e) )
#CXCPQ-31793
try:
    SUMMARSHUIO=GS_SM_CG_UIO_CALC.get_sum_marsh_uio(attrs)
    Trace.Write(SUMMARSHUIO)
except Exception,e:
    Trace.Write("Error when Reading GS_SM_CG_UIO_CALC : " + str(e) )
try:
    parts_dict = GS_SM_TSKUNI.get_partstskuni(Product,parts_dict)
except Exception,e:
    Trace.Write("Error in GS_SM_TSKUNI: " + str(e) )
try:
    parts_dict = GS_SM_TSKUNI.get_partstspkuni(Product,parts_dict)
except Exception,e:
    Trace.Write("Error in GS_SM_TSKUNI: " + str(e) )
SUMRIOR = 0
if attrs:
    try:
        SUMRIOR = GS_SM_CG_UIO_CALC.get_sum_red_io(attrs, SUMUIORPF)
    except Exception,e:
        SUMRIOR = 0
        Trace.Write("Error in GS_SM_CG_UIO_CALC: " + str(e) )

IOComp = GS_SM_SUMUIORIS_Calcs.IOComponents(Product)
SUMUIORIS = IOComp.SUMUIORIS_value()

MCAREST = GS_SM_MCAR_02_MCAREST_Calc.MCAR_02_MCAREST_CG_RG_Calc(Product)
BCUFREST = m.ceil(MCAREST/7)
FDBCUFR = m.ceil(BCUFREST*5)

p1=m.ceil((FDBCUFR+SUMRION+SUMRIONIS)/32)
if SUMRION+SUMRIONIS==0:
    qnt=p1+2*m.ceil((SUMRIOR+SUMRIORIS)/32.0)
    if Product.Attr("SM_Universal_IOTA_Type").GetValue()=="RUSIO":
        Product.Attr('FC_RG_RUSIO').AssignValue(str(qnt))
elif SUMRION+SUMRIONIS>0:
    qnt=p1+2*m.ceil((SUMRIOR+SUMRIORIS)/32.0)
    if Product.Attr("SM_Universal_IOTA_Type").GetValue()=="RUSIO":
        Product.Attr('FC_RG_RUSIO').AssignValue(str(qnt))

IOTAR = m.ceil((SUMRIOR+SUMRIORIS)/32.0)
IOTANR =m.ceil((FDBCUFR+SUMRION+SUMRIONIS)/32)
if Product.Attr("SM_Universal_IOTA_Type").GetValue()=="RUSIO":
    Product.Attr('RUSIO_RG_IOTAR').AssignValue(str(IOTAR))
    Product.Attr('RUSIO_RG_IOTANR').AssignValue(str(IOTANR))
IOTAR = int(float(Product.Attr('RUSIO_RG_IOTAR').GetValue()))
IOTANR = int(float(Product.Attr('RUSIO_RG_IOTANR').GetValue()))
Trace.Write("iotar: "+str(IOTAR))
Trace.Write("iotanr: "+str(IOTANR))
#CXCPQ-31175
iota = Product.Attr("SM_Universal_IOTA_Type").GetValue()
if iota == "RUSIO":
    try:
        parts_dict,MCAR = GS_SM_MCAR.get_rg_mcar(Product,IOTANR,IOTAR,parts_dict)
        Trace.Write("---------------------------MCAR : "+str(MCAR))
    except Exception,e:
        #Product.ErrorMessages.Add("Error in GS_SM_MCAR: " + str(e))
        Trace.Write("Error in GS_SM_MCAR :" + str(e) + " Line Number: 226")
'''try:
	parts_dict,MCAR = get_rg_mcar(Product,IOTANR,IOTAR,parts_dict)
except Exception,e:
	Product.ErrorMessages.Add("Error in GS_SM_MCAR: " + str(e) )'''

if qnt>0:
    if Product.Attr("SM_Universal_IOTA_Type").GetValue()=="RUSIO" and Product.GetContainerByName("SM_RG_ATEX Compliance_and_Enclosure_Type_Cont").Rows[0].GetColumnByName("Enclosure_Type").DisplayValue=="Cabinet":
        parts_dict["FC-RUSIO-3224"] = {'Quantity' : qnt , 'Description': 'SM RIO module 32 ch 24Vdc'}
if IOTAR>0:
    if Product.Attr("SM_Universal_IOTA_Type").GetValue()=="RUSIO" and Product.GetContainerByName("SM_RG_ATEX Compliance_and_Enclosure_Type_Cont").Rows[0].GetColumnByName("Enclosure_Type").DisplayValue=="Cabinet":
        parts_dict["FC-IOTA-R24"] = {'Quantity' : IOTAR , 'Description': 'SM RIO redundant termination assembly'}
if IOTANR>0:
    if Product.Attr("SM_Universal_IOTA_Type").GetValue()=="RUSIO" and  Product.GetContainerByName("SM_RG_ATEX Compliance_and_Enclosure_Type_Cont").Rows[0].GetColumnByName("Enclosure_Type").DisplayValue=="Cabinet":
        parts_dict["FC-IOTA-NR24"] = {'Quantity' : IOTANR , 'Description': 'SM RIO non-redundant termination assembly'}
FC_PUIO01 = int(float(Product.Attr('FC_RG_PUIO').GetValue()))
if FC_PUIO01:
    if Product.Attr("SM_Universal_IOTA_Type").GetValue()=="PUIO" and Product.GetContainerByName("SM_RG_ATEX Compliance_and_Enclosure_Type_Cont").Rows[0].GetColumnByName("Enclosure_Type").DisplayValue=="Cabinet":
        parts_dict["FC-PUIO01"] = {'Quantity' : int(FC_PUIO01) , 'Description': 'SC SAFETY UIO IOM 24VDC, 32CH'}

FC_PDIO01 = int(float(Product.Attr('FC_RG_PDIO').GetValue()))
if FC_PDIO01:
    if Product.GetContainerByName("SM_RG_ATEX Compliance_and_Enclosure_Type_Cont").Rows[0].GetColumnByName("Enclosure_Type").DisplayValue=="Cabinet":
        parts_dict["FC-PDIO01"] = {'Quantity' : int(FC_PDIO01) , 'Description': 'SC SAFETY DIO IOM 24VDC, 32CH'}
#31139
FC_TUIO11 = int(float(Product.Attr('FC_RG_TUIO').GetValue()))  if Product.Attr('FC_RG_TUIO').GetValue()!="" else 0
if FC_TUIO11:
    if Product.Attr("SM_Universal_IOTA_Type").GetValue()=="PUIO" and Product.GetContainerByName("SM_RG_ATEX Compliance_and_Enclosure_Type_Cont").Rows[0].GetColumnByName("Enclosure_Type").DisplayValue=="Cabinet":
        parts_dict["FC-TUIO11"] = {'Quantity' : int(FC_TUIO11) , 'Description': 'SC IOTA PUIO REDUNDANT'}
#31140
FC_TDIO11 = int(float(Product.Attr('FC_RG_TDIO').GetValue()))  if Product.Attr('FC_RG_TDIO').GetValue()!="" else 0
if FC_TDIO11:
    if Product.GetContainerByName("SM_RG_ATEX Compliance_and_Enclosure_Type_Cont").Rows[0].GetColumnByName("Enclosure_Type").DisplayValue=="Cabinet":
        parts_dict["FC-TDIO11"] = {'Quantity' : int(FC_TDIO11) , 'Description': 'SC IOTA PDIO REDUNDANT'}
TCNT11 = 0 #CXCPQ-31335


'''try:
    parts_dict = GS_SMPartsCalc1.get_parts(Product,parts_dict)
except:
    Trace.Write("Error in GS_SMPartsCalc1 :" + str(e) )'''

try:
    attr = GS_SM_ReadPart_Attrs.AttrStorage(Product)
except Exception,e:
    attr = None
    #Product.ErrorMessages.Add("Error when Reading SM remote group Attributes: " + str(e) )
    Trace.Write("Error when Reading GS_SM_ReadPart_Attrs: " + str(e) )
try:
    total_rio_cabinet_summary =GS_Load_SM_RIO_Cab_Summary.getLoadSMRIOCabSummary(Product)
except Exception,e:
    total_rio_cabinet_summary = None
    #Product.ErrorMessages.Add("Error when Reading GS_SM_Load_SM_RIO_cabinet_summary_Calc: " + str(e) )
    Trace.Write("Error when Reading GS_SM_Load_SM_RIO_cabinet_summary_Calc: " + str(e) )
try:
    IOComp = GS_SMIOComponents.IOComponents(Product)
    SUMUIONPF, SUMUIORPF = IOComp.getUniversalIOCountRedNonRed()
    GPCS =D.Ceiling(SUMUIONPF/16)+D.Ceiling(SUMUIORPF/16)
    Trace.Write('GPCS : '+str(GPCS))
except Exception,e:
    Trace.Write("Error when Reading GS_SMIOComponents : " + str(e) )
try:
    atr=GS_part_add_IO_value.IOvalues(Product)
    a,b,c,d=atr.io_mon()
    TDOL = D.Ceiling((a+c)/7)+D.Ceiling((b+d)/7)
except:
    Trace.Write("Error when Reading GS_part_add_IO_value : " + str(e) )

try:
    parts_dict = sm_part_add_calcs.getCGParts(FC_PUIO01,FC_PDIO01,TDOL,GPCS, Product, parts_dict)
except Exception,e:
    Trace.Write("Error in sm_part_add_calcs: " + str(e) )

#33220
if Product.GetContainerByName("SM_RG_ATEX Compliance_and_Enclosure_Type_Cont").Rows[0].GetColumnByName("Enclosure_Type").DisplayValue=="Cabinet":
    try:
        parts_dict = sm_part_add_calcs.cabinet_part(Product,parts_dict)
    except Exception,e:
        Trace.Write("Error in sm_part_add_calcs: " + str(e) )

# Total Load Parts
try:
    parts_dict = GS_SM_Part_Calcs.get_total_parts(Product,total_rio_cabinet_summary,parts_dict)
except Exception,e:
    Trace.Write("Error in GS_SM_Part_Calcs: " + str(e) )
#CXCPQ-31853_Prabhat
try:
    parts_dict = GS_SM_Part_Calcs.get_parts1(Product,parts_dict)
except Exception,e:
    Trace.Write("Error in GS_SM_Part_Calcs.get_parts1: " + str(e) )
#CXCPQ-31854
try:
    parts_dict = GS_SM_Part_Calcs.get_parts2(Product,parts_dict)
except Exception,e:
    Trace.Write("Error in GS_SM_Part_Calcs.get_parts2: " + str(e) )
#CXCPQ-31855
try:
    parts_dict = sm_part_add_calcs.get_parts3(Product,parts_dict)
except Exception,e:
    Trace.Write("Error in sm_part_add_calcs.get_parts3: " + str(e) )
try:
    parts_dict = sm_part_add_calcs.filler_plate(Product,parts_dict)
except Exception,e:
    Trace.Write("Error in sm_part_add_calcs.filler_plate: " + str(e) )
try:
    parts_dict = sm_part_add_calcs.cabinet_part(Product,parts_dict)
except Exception,e:
    Trace.Write("Error in sm_part_add_calcs.cabinet_part: " + str(e) )
try:
    parts_dict = sm_part_add_calcs.FC_MCAR_02(FC_TUIO11,FC_TDIO11,TCNT11,Product,parts_dict)
except Exception,e:
    Trace.Write("Error in sm_part_add_calcs.get_parts3: " + str(e) )
#CXCPQ-31812
if Product.GetContainerByName("SM_RG_ATEX Compliance_and_Enclosure_Type_Cont").Rows[0].GetColumnByName("Enclosure_Type").DisplayValue=="Cabinet":
    try:
        parts_dict = GS_SM_Part_Calcs.get_FC_TDIO52(attrs,parts_dict,SUMMARCHDIO)
    except Exception,e:
        Product.ErrorMessages.Add("Error in GS_SM_Part_Calcs: " + str(e) )
#Trace.Write("blue:"+str(GS_SM_Part_Calcs.get_FC_TDIO52(parts_dict,SUMMARCHDIO)))
#CXCPQ-31793
'''if Product.GetContainerByName("SM_RG_ATEX Compliance_and_Enclosure_Type_Cont").Rows[0].GetColumnByName("Enclosure_Type").DisplayValue=="Cabinet":
    try:
        ##pass
        parts_dict = GS_SM_Part_Calcs.get_FC_TUIO52(attrs,SUMMARSHUIO,parts_dict)
        #Trace.Write("Anjani:"+str(parts_dict))
    except Exception,e:
        Product.ErrorMessages.Add("Error in GS_SM_Part_Calcs: " + str(e) )'''
#CXCPQ_33265
if Product.GetContainerByName("SM_RG_ATEX Compliance_and_Enclosure_Type_Cont").Rows[0].GetColumnByName("Enclosure_Type").DisplayValue=="Cabinet":
    try:
        ##pass
        parts_dict = GS_SM_Part_Calcs.get_partsiota(parts_dict,IOTAR,IOTANR,FC_TUIO11,FC_TDIO11)
    except Exception,e:
        Trace.Write("Error in GS_SM_Part_Calcs: " + str(e) )
#CXCPQ-32148
try:
    parts_dict = GS_SM_REMOTE_PART_SM.get_parts(Product, parts_dict)
except Exception,e:
    Trace.Write("Error in GS_SM_REMOTE_PART_SM : " + str(e) )

#CXCPQ-33504
if Product.Attr("SM_Universal_IOTA_Type").GetValue()=="RUSIO" and Product.GetContainerByName("SM_RG_ATEX Compliance_and_Enclosure_Type_Cont").Rows[0].GetColumnByName("Enclosure_Type").DisplayValue=="Cabinet":
    try:
        if Product.GetContainerByName("SM_RG_ATEX Compliance_and_Enclosure_Type_Cont").Rows[0].GetColumnByName("Enclosure_Type").DisplayValue=="Cabinet":
            parts_dict =GS_SM_FC_MCAR_02_part.get_fc_mcar_02(Product,IOTANR,IOTAR,FC_TDIO11,TCNT11,parts_dict)
    except Exception,e:
        Trace.Write("Error in GS_SM_FC_MCAR_02_part: " + str(e) )

#CXCPQ-34197
try:
    parts_dict = SM_Identifier_Position_Calcs.identifier_FC_TUIO51(Product,parts_dict)
except Exception,e:
    Trace.Write("Error in SM_Identifier_Position_Calcs : " + str(e) )

#CXCPQ-34238
try:
    parts_dict = SM_Identifier_Position_Calcs.get_identifier_SIC2005(Product,parts_dict)
except Exception,e:
    Trace.Write("Error in SM_Identifier_Position_Calcs : " + str(e) )

#CXCPQ-32662
try:
    parts_dict = GS_SM_identifier_position_PARTS.get_identifier_Positions(Product,parts_dict)
except Exception,e:
    Trace.Write("Error in GS_SM_identifier_position_PARTS" + str(e) )

#CXCPQ_33029
if Product.GetContainerByName("SM_RG_ATEX Compliance_and_Enclosure_Type_Cont").Rows[0].GetColumnByName("Enclosure_Type").DisplayValue=="Cabinet":
    try:
        parts_dict = GS_SM_CGRG_NAMUR_PARTS.get_DIDO_SL_Namur_DI(Product, parts_dict)
    except Exception,e:
        Trace.Write("Error in GS_SM_CGRG_NAMUR_PARTS : " + str(e) )
#CXCPQ_33030
if Product.GetContainerByName("SM_RG_ATEX Compliance_and_Enclosure_Type_Cont").Rows[0].GetColumnByName("Enclosure_Type").DisplayValue=="Cabinet":
    try:
        parts_dict = GS_SM_CGRG_NAMUR_PARTS.get_UIO_SL_sftyNamur_DI(Product, parts_dict)
    except Exception,e:
        Trace.Write("Error in GS_SM_CGRG_NAMUR_PARTS : " + str(e) )
#CXCPQ-33026
if Product.GetContainerByName("SM_RG_ATEX Compliance_and_Enclosure_Type_Cont").Rows[0].GetColumnByName("Enclosure_Type").DisplayValue=="Cabinet":
    try:
        parts_dict = GS_SM_BOM_Parts.get_FC_UDI501(Product,parts_dict)
    except Exception,e:
        Trace.Write("Error in GS_SM_BOM_Parts: " + str(e) )
#CXCPQ-33031
if Product.GetContainerByName("SM_RG_ATEX Compliance_and_Enclosure_Type_Cont").Rows[0].GetColumnByName("Enclosure_Type").DisplayValue=="Cabinet":
    try:
        parts_dict = GS_SM_CGRG_NAMUR_PARTS.get_UIO_SL_sftyNamur_DO(Product, parts_dict)
    except Exception,e:
        Trace.Write("Error in GS_SM_CGRG_NAMUR_PARTS: " + str(e) )
#CXCPQ-33027
if Product.GetContainerByName("SM_RG_ATEX Compliance_and_Enclosure_Type_Cont").Rows[0].GetColumnByName("Enclosure_Type").DisplayValue=="Cabinet":
    try:
        parts_dict = GS_SM_BOM_Parts.get_FC_UIR501(Product,parts_dict)
    except Exception,e:
        Trace.Write("Error in GS_SM_BOM_Parts: " + str(e) )
#CXCPQ-33028
if Product.GetContainerByName("SM_RG_ATEX Compliance_and_Enclosure_Type_Cont").Rows[0].GetColumnByName("Enclosure_Type").DisplayValue=="Cabinet":
    try:
        parts_dict = GS_SM_BOM_Parts.get_FC_UDIR01(Product,parts_dict)
    except Exception,e:
        Trace.Write("Error in GS_SM_BOM_Parts: " + str(e) )
#CXCPQ-32158
if Product.GetContainerByName("SM_RG_ATEX Compliance_and_Enclosure_Type_Cont").Rows[0].GetColumnByName("Enclosure_Type").DisplayValue=="Universal Safety Cab-1.3M":
    try:
        parts_dict = GS_SM_CGRG_NAMUR_PARTS.getidpartsbracket(Product,parts_dict)
    except Exception,e:
        Trace.Write("Error in GS_SM_CGRG_NAMUR_PARTS: " + str(e) )
#CXCPQ-32161
if Product.GetContainerByName("SM_RG_ATEX Compliance_and_Enclosure_Type_Cont").Rows[0].GetColumnByName("Enclosure_Type").DisplayValue=="Universal Safety Cab-1.3M":
    try:
        parts_dict = GS_SM_CGRG_NAMUR_PARTS.getELDqnt(Product,parts_dict)
    except Exception,e:
        Trace.Write("Error in GS_SM_CGRG_NAMUR_PARTS: " + str(e) )
#CXCPQ-34332
if Product.GetContainerByName("SM_RG_ATEX Compliance_and_Enclosure_Type_Cont").Rows[0].GetColumnByName("Enclosure_Type").DisplayValue=="Universal Safety Cab-1.3M":
    try:
        parts_dict = GS_SM_CGRG_NAMUR_PARTS.getBCTDqnt(Product,parts_dict)
    except Exception,e:
        Trace.Write("Error in GS_SM_CGRG_NAMUR_PARTS: " + str(e) )

if attr:
    try:
        parts_dict = GS_SMPartsCalc.getRGParts(Product, parts_dict)
        #CXCPQ-31795
        parts_dict = GS_SMPartsCalc.getHardwiredMarshallingParts(Product, parts_dict)
    except Exception,e:
        Trace.Write("Error in GS_SM_Part_Calcs: " + str(e) )
    Trace.Write("debugging: " + str(parts_dict))
    try:
        parts_dict = GS_SM_Part_Calcs.get_rg_parts(Product, attr, attrs, parts_dict, total_rio_cabinet_summary)
    except Exception,e:
        Trace.Write("Error in GS_SM_Part_Calcs: " + str(e) )
    Trace.Write("debugging: " + str(parts_dict))
        #CXCPQ-31159
    try:
        parts_dict = GS_Power_Supply_calcs.getPowerSupplyPart(Product, parts_dict)
    except Exception,e:
        Trace.Write("Error in GS_Power_Supply_calcs: " + str(e) )
    Trace.Write("debugging: " + str(parts_dict))

    # #CXCPQ-31191
    # Commented as the implementation is already in get_rg_parts function of GS_SM_Part_Calcs
    try:
        parts_dict = GS_Power_Supply_calcs1.getPwrSupParts(Product, parts_dict)
        Trace.Write("AAAA" +str(parts_dict))
    except Exception,e:
        Trace.Write("Error in GS_Power_Supply_calcs: " + str(e) )
    Trace.Write("debugging: " + str(parts_dict))
    #CXCPQ-34326 By Prabhat
    try:
        parts_dict = GS_Power_Supply_calcs.get_identifier_RG(Product,parts_dict)
    except Exception,e:
        Trace.Write("Error in GS_Power_Supply_calcs: " + str(e) )
    Trace.Write("debugging: " + str(parts_dict))
    #CXCPQ-31865
    try:
        parts_dict = GS_Power_Supply_calcs1.Get_Parts_Sic_length(Product,parts_dict)
    except Exception,e:
        Trace.Write("Error in GS_Power_Supply_calcs1: " + str(e) )
    Trace.Write("debugging: " + str(parts_dict))
    #Trace.Write("debugging: " + str(parts_dict))
    #GS_SM_Part_Update.execute(Product, 'SM_RG_PartSummary_Cont', parts_dict)
    #CXCPQ-31844,31846,31845
    '''try:
        parts_dict = GS_Power_Supply_calcs1.Get_Sic_length(Product,parts_dict)
    except Exception,e:
        Product.ErrorMessages.Add("Error in GS_Power_Supply_calcs1: " + str(e) )
    Trace.Write("debugging: " + str(parts_dict))'''
    
#CXCPQ-33622
try:
    parts_dict = GS_SM_Rio_Ethernet_Cable_Parts.Rio_Ethernet_Cable_Parts(Product, parts_dict)
except Exception,e:
    Trace.Write("Error in GS_SM_Rio_Ethernet_Cable_Parts: " + str(e) )

#CXCPQ-33036
try:
    parts_dict = GS_Part_CC_USCA01_Calc.Part_CC_USCA01_Calc(Product, parts_dict)
except Exception,e:
    Trace.Write("Error in GS_Part_CC_USCA01_Calc: " + str(e) )

# Commented as the logic is moved to addParts funciton in GS_SM_Part_Calcs module which is called later in this script
#CXCPQ-33046
#try:
#    parts_dict = GS_Part_FC_USCA01_Calc.Part_FC_USCA01_Calc(Product, parts_dict)
#except Exception,e:
#    Product.ErrorMessages.Add("Error in GS_Part_FC_USCA01_Calc: " + str(e) )
    
#CXCPQ-33048
try:
    parts_dict = GS_Part_CC_UGIA01_Calc.Part_CC_UGIA01_Calc(Product, parts_dict)
except Exception,e:
    Trace.Write("Error in GS_Part_CC_UGIA01_Calc: " + str(e) )

#CXCPQ-31813,31824,31839,31841
try:
    parts_dict = GS_SMPartsCalc2.get_partz(Product,parts_dict)
except Exception,e:
    Trace.Write("Error in GS_SMPartsCalc2: " + str(e) )
try:
    parts_dict = GS_SMPartsCalc1.rg_cabinet_access(Product,parts_dict)
except Exception,e:
    Trace.Write("Error in GS_SMPartsCalc1" + str(e) )
Trace.Write("debugging: " + str(parts_dict))
try:
    parts_dict = GS_SMPartsCalc1.sm_parts(Product,parts_dict)
except Exception,e:
    Trace.Write("Error in GS_SMPartsCalc1" + str(e) )
###GS_SM_Part_Update.execute(Product, 'SM_RG_PartSummary_Cont', parts_dict)
#CXCPQ-33666 to CXCPQ-33677
try:
    parts_dict = GS_SM_Identifier_Modifier_Part_Calcs.identifier_Modifier(Product,parts_dict)
except Exception,e:
    Trace.Write("Error in GS_SM_Identifier_Modifier_Part_Calcs: " + str(e) )
try:
    cabinet_count, power_supply, switches = GS_SMPartsCalc.getNumberOfRGCabinet(Product)
except Exception,e:
    cabinet_count, power_supply, switches = 0, 0, 0

if cabinet_count:
    parts_dict = GS_SM_Cabinet_count_parts.getRGParts(Product, parts_dict, cabinet_count, power_supply, switches)
#CXCPQ- 33639
A_Comp={}

try:
    if Product.GetContainerByName("SM_RG_ATEX Compliance_and_Enclosure_Type_Cont").Rows[0].GetColumnByName("Enclosure_Type").DisplayValue=="Cabinet":
        A_Comp = GS_SM_CompA1_Calcs.get_CompA1(Product)
        parts_dict=GS_SM_CompA1_Calcs.CCI_HSE(A_Comp,Product,parts_dict)
    #Trace.Write("Shivani:"+str(parts_dict))
except Exception,e:
    Trace.Write("Error in GS_SM_CompA1_Calcs" + str(e) )
#CXCPQ-33032
try:
    parts_dict = GS_SM_CGRG_NAMUR_PARTS.get_FC_UDOF01(Product,parts_dict)
except Exception,e:
    Trace.Write("Error in GS_SM_CGRG_NAMUR_PARTS: " + str(e) )
#CXCPQ-32667
try:
    parts_dict = GS_SM_get_FS_CCI_HSE_20.get_FS_CCI_HSE_20(Product,parts_dict)
except Exception,e:
    Trace.Write("Error in GS_SM_get_FS_CCI_HSE_20: " + str(e) )
#By Shivani CXCPQ-33071,33078
cab1, powerSupply1, switches1 = GS_SMPartsCalc.getNumberOfRGCabinet(Product)
try:
    parts_dict = GS_SM_Get_Parts_FSC.Get_CG_Parts_FSC(Product,parts_dict)
except Exception,e:
    Trace.Write("Error in GS_SM_Get_Parts_FSC: " + str(e) + " Line Number: 514" )
#CXCPQ-31596
try:
    parts_dict = GS_SM_CGRG_NAMUR_PARTS.get_USC(Product,parts_dict)
except Exception,e:
    Trace.Write("Error in GS_SM_CGRG_NAMUR_PARTS: " + str(e) )


#CXCPQ-33671

try:
    if Product.GetContainerByName("SM_RG_ATEX Compliance_and_Enclosure_Type_Cont").Rows[0].GetColumnByName("Enclosure_Type").DisplayValue=="Cabinet":
        a_comp=GS_SM_CompA1_Calcs.get_CompA1(Product)
        #B=GS_SM_Comp_B_CNMPart_Calc.Comp_B_CNMPart_Calc(Product)
        parts_dict=GS_SM_CompA1_Calcs.get_CompC(parts_dict,Product,a_comp)
    Trace.Write("Shivani:"+str(parts_dict))
    #Trace.Write("Shivani:"+str(parts_dict))
except Exception,e:
    Trace.Write("Error in GS_SM_CompA1_Calcs" + str(e) )

# Sprint 18
try:
    parts_dict = GS_SM_Part_Calcs.addParts(attrs, parts_dict, Tot_qty_FC_USCH01, cable_qty_L3)
except Exception, e:
    Trace.Write("Error in GS_SM_Part_Calcs addParts call: " + str(e) )

#CXCPQ-33234
try:
    parts_dict = GS_SM_RG_Licenses_Calcs.SM_RG_Licenses_Calcs(Product, parts_dict)
except Exception,e:
    pass

# #CXCPQ-31191 - First Call
try:
    parts_dict = GS_Power_Supply_calcs1.getPwrSupParts(Product, parts_dict, True)
except Exception,e:
    Trace.Write("Error in GS_Power_Supply_calcs1: " + str(e) )
Trace.Write("debugging: " + str(parts_dict))

try:
    calculated_loads = GS_SM_Part_Calcs.calculate_loads(parts_dict)
    #Product.Messages.Add("Calculated loads are " + RestClient.SerializeToJson(calculated_loads))
except Exception,e:
    Trace.Write("Error in calculate_loads" + str(e) )

#CXCPQ-32666
if Product.GetContainerByName("SM_RG_ATEX Compliance_and_Enclosure_Type_Cont").Rows[0].GetColumnByName("Enclosure_Type").DisplayValue=="Universal Safety Cab-1.3M":
    try:
        parts_dict = GS_SM_RG_getexcode.getexcode(Product,parts_dict)
    except Exception,e:
        pass

#CXCPQ-46227 - FAN Parts
EnclosureType = Product.Attr('SM_RG_Enclosure_Type').GetValue()
cabinets = 0
if EnclosureType == 'Cabinet':
    if 'FS-BCU-0036' in parts_dict.keys():
        cabinets = parts_dict['FS-BCU-0036']['Quantity']
    elif 'FS-BCU-0038' in parts_dict.keys():
        cabinets = parts_dict['FS-BCU-0038']['Quantity']
    if cabinets > 0:
        qty = cabinets*2
        parts_dict['51109516-100'] = {'Quantity' : qty, 'Description': ''}
        parts_dict['51199947-275'] = {'Quantity' : qty, 'Description': ''}

#CXCPQ-47876
try:
    parts_dict = GS_SM_Shipping_Parts.SM_Shipping_Parts_CG_RG(Product, parts_dict)
except Exception,e:
    Trace.Write("GS_SM_Shipping_Parts : " + str(e) )

#CXCPQ-118186
try:
    Enclosure_Type = Product.GetContainerByName('SM_RG_ATEX Compliance_and_Enclosure_Type_Cont').Rows[0].GetColumnByName('Enclosure_Type').DisplayValue
    if Enclosure_Type == "Universal Safety Cab-1.3M":
        Specify_Identifier = Product.GetContainerByName('SM_RG_Universal_Safety_Cabinet_1.3M_Cont').Rows[0].GetColumnByName('Specify_Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet').DisplayValue
        Identifier_Modifier = Product.GetContainerByName('SM_RG_Universal_Safety_Cabinet_1.3M_Cont').Rows[0].GetColumnByName('Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet').Value
        Safety_Cabinets_qnt = int(Product.GetContainerByName('SM_RG_Universal_Safety_Cabinet_1.3M_Cont').Rows[0].GetColumnByName('Number_of_SM_SC_1.3M_Universal_Safety_Cabinets_(0-63)').Value or 0)
        if Specify_Identifier == "Yes":
            if Identifier_Modifier[3] == "X" and Identifier_Modifier[17] == "2":
                parts_dict['50165649-001'] = {'Quantity' : 2*Safety_Cabinets_qnt, 'Description': ''}
            elif Identifier_Modifier[3] == "S" and Identifier_Modifier[17] == "4":
                parts_dict['50165649-001'] = {'Quantity' : 4*Safety_Cabinets_qnt, 'Description': ''}
        elif Specify_Identifier == "No":
            S300 = Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName('S300').DisplayValue
            CNM = Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName('Number_of_Control_Network_Module_0-100').Value
            if S300 == "No S300" and CNM == "2":
                parts_dict['50165649-001'] = {'Quantity' : 2*Safety_Cabinets_qnt, 'Description': ''}
            elif S300 == "Redundant S300" and CNM == "4":
                parts_dict['50165649-001'] = {'Quantity' : 4*Safety_Cabinets_qnt, 'Description': ''}
except Exception,e:
    Trace.Write("Error while calculating 50165649-001: " + str(e) )

GS_SM_Part_Update.execute(Product, 'SM_RG_PartSummary_Cont', parts_dict)
ScriptExecutor.Execute('PS_SM_RG_LI_Part_Summary')