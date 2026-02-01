import math as m
import ProductUtil as pu
import System.Decimal as D
import GS_SM_SUMUIORIS_Calcs
import GS_SM_SUMDIONIS_Calcs
import GS_SM_SUMDION_Calcs
import GS_SM_SUMDIORIS_Cal
import GS_SM_SUMDIOR_Calcs
import GS_SM_SUMUION_Cals, GS_SMIOComponents
import GS_SM_Component_Call, GS_SM_Variable_Comp_Map
import GS_SM_MCAREST_component,GS_SM_SC300
import GS_SM_SUMRIONIS_Calc, GS_SM_MCAR_02_MCAREST_Calc
Product.Attributes.GetByName('FC_PUIO').AssignValue('0')
Product.Attributes.GetByName('FC_PDIO').AssignValue('0')
Product.Attributes.GetByName('FC_TUIO').AssignValue('0')
Product.Attributes.GetByName('FC_TDIO').AssignValue('0')
iota = ''
contCommonQn = Product.GetContainerByName("SM_CG_Common_Questions_Cont")
if contCommonQn.Rows.Count > 0:
    iota = contCommonQn.Rows[0].GetColumnByName("SM_Universal_IOTA").DisplayValue

def get_thing(n):
    if n != "":
        n = int(float(n))
    else:
        n = 0
    return n

try:
    SUMRIONIS = GS_SM_SUMRIONIS_Calc.SUMRIONIS_Calc(Product)
    pu.addMessage(Product, "calculated Value of SUMRIONIS is : " + str(SUMRIONIS))
except Exception,e:
    Trace.Write("Error in GS_SM_SUMRIONIS_Calc: " + str(e))

try:
    IOComp = GS_SMIOComponents.IOComponents(Product)
    SUMUIONPF, SUMUIORPF = IOComp.getUniversalIOCountRedNonRed()
    pu.addMessage(Product, "calculated Value of SUMUIONPF is : " + str(SUMUIONPF))
    pu.addMessage(Product, "calculated Value of SUMUIORPF is : " + str(SUMUIORPF))
except Exception,e:
    SUMUIORPF = 0
    SUMUIONPF = 0
    Trace.Write("Error in SUMUIORPF & SUMUIONPF Calc: " + str(e))

try:
    attrs = GS_SM_Variable_Comp_Map.AttrStorage(Product)
    SUMUIONIS = GS_SM_Component_Call.get_SUMUIONIS(Product)
    pu.addMessage(Product, "calculated Value of SUMUIONIS is : " + str(SUMUIONIS))
    Trace.Write("SUMUIONIS:"+str(SUMUIONIS))
except Exception,e:
    SUMUIONIS = 0
    #Product.ErrorMessages.Add("Error in SUMUIONIS Calc: " + str(e))

try:
    IOComp_SUMUION = GS_SM_SUMUION_Cals.IOComponentsNRNIS(Product)
    SUMUION = IOComp_SUMUION.get_SUMUION()
    Trace.Write("SUMUION: "+str(SUMUION))
except Exception,e:
    SUMUION = 0
    Trace.Write("Error in SUMUION Calc: " + str(e))
    
if iota == "PUIO":
    try:
        IOComp_SUMUIORIS = GS_SM_SUMUIORIS_Calcs.IOComponents(Product)
        SUMUIORIS = IOComp_SUMUIORIS.SUMUIORIS_value()
        pu.addMessage(Product, "calculated Value of SUMUIORIS is : " + str(SUMUIORIS))
        Trace.Write("SUMUIORIS: "+str(SUMUIORIS))
    except Exception,e:
        SUMUIORIS = 0
        Trace.Write("Error in SUMUIORIS Calc: " + str(e))

try:
    SUMUIOR= GS_SM_Component_Call.GS_SM_SUMUIOR_Calc(Product,SUMUIORPF)
    pu.addMessage(Product, "calculated Value of SUMUIOR is : " + str(SUMUIOR))
    Trace.Write("SUMUIOR: "+str(SUMUIOR))
except Exception,e:
    SUMUIOR = 0
    Trace.Write("Error in SUMUIOR Calc: " + str(e))

try:
    SUMDIONIS = GS_SM_SUMDIONIS_Calcs.Get_SUMDIONIS(Product)
    pu.addMessage(Product, "calculated Value of SUMDIONIS is : " + str(SUMDIONIS))
    Trace.Write("SUMDIONIS: "+str(SUMDIONIS))
except Exception,e:
    SUMDIONIS = 0
    Trace.Write("Error in SUMDIONIS Calc: " + str(e))

try:
    IOComp_SUMDION = GS_SM_SUMDION_Calcs.IOComponents(Product)
    SUMDION = IOComp_SUMDION.SUMDION_value()
    pu.addMessage(Product, "calculated Value of SUMDION is : " + str(SUMDION))
    Trace.Write("SUMDION: "+str(SUMDION))
except Exception,e:
    SUMDION = 0
    Trace.Write("Error in SUMDION Calc: " + str(e))

try:
    #attrs1 = GS_SM_SUMDIORIS_Attr.AttrStorage(Product)
    SUMDIORIS = GS_SM_SUMDIORIS_Cal.Get_SUMDIORIS(Product)
    Trace.Write("SUMDIORIS: "+str(SUMDIORIS))
    pu.addMessage(Product, "calculated Value of SUMDIORIS is : " + str(SUMDIORIS))
except Exception,e:
    SUMDIORIS = 0
    Trace.Write("Error in SUMDIORIS Calc: " + str(e))

try:
    IOComp_SUMDIOR = GS_SM_SUMDIOR_Calcs.IOComponents(Product)
    SUMDIOR = IOComp_SUMDIOR.SUMDIOR_value()
    pu.addMessage(Product, "calculated Value of SUMDIOR is : " + str(SUMDIOR))
    Trace.Write("SUMDIOR: "+str(SUMDIOR))
except Exception,e:
    SUMDIOR = 0
    Trace.Write("Error in SUMDIOR Calc: " + str(e))
TCNT11 = get_thing(Product.Attr('FC_TCNT').GetValue())
pu.addMessage(Product, "calculated Value of TCNT11 is : " + str(TCNT11))
'''try:
    TCNT11=GS_SM_SC300.get_TCNT(Product, 0)[1]
    Trace.Write("TCNT11: "+str(TCNT11))
except Exception,e:
    TCNT11 = 0
    Product.ErrorMessages.Add("Error in TCNT11 Calc: " + str(e) )'''
#31081
MCAREST=0
if iota == "PUIO":
    MCAREST=GS_SM_MCAREST_component.get_MCAREST(SUMUIONIS,SUMUION,SUMUIORIS,SUMUIOR,SUMDIONIS,SUMDION,SUMDIORIS,SUMDIOR,TCNT11)
    pu.addMessage(Product, "calculated Value of MCAREST is : " + str(MCAREST))
    Trace.Write("MCAREST: "+str(MCAREST))
#31082
BCUFREST=GS_SM_MCAREST_component.get_BCUFREST(MCAREST)
pu.addMessage(Product, "calculated Value of BCUFREST is : " + str(BCUFREST))
Trace.Write("BCUFREST: "+str(BCUFREST))
#31131
FDBCUFR=GS_SM_MCAREST_component.get_FDBCUFR(BCUFREST)
pu.addMessage(Product, "calculated Value of FDBCUFR is : " + str(FDBCUFR))
Trace.Write("FDBCUFR: "+str(FDBCUFR))
#31136
FC_PDIO01=GS_SM_MCAREST_component.get_FC_PDIO01(FDBCUFR,SUMDION,SUMDIONIS,SUMDIOR,SUMDIORIS)
pu.addMessage(Product, "calculated Value of FC_PDIO01 is : " + str(FC_PDIO01))
Product.Attributes.GetByName('FC_PDIO').AssignValue(str(FC_PDIO01))
Trace.Write("FC_PDIO01: "+str(FC_PDIO01))

#31134
if iota == "PUIO":
    FC_PUIO01=GS_SM_MCAREST_component.get_FC_PUIO01(FDBCUFR,SUMUION,SUMUIONIS,SUMUIOR,SUMUIORIS)
    pu.addMessage(Product, "calculated Value of FC_PUIO01 is : " + str(FC_PUIO01))
    Product.Attributes.GetByName('FC_PUIO').AssignValue(str(FC_PUIO01))
    Trace.Write("FC_PUIO01: "+str(FC_PUIO01))

#31139
if iota == "PUIO":
    FC_TUIO11=GS_SM_MCAREST_component.get_FC_TUIO11(FDBCUFR,SUMUION,SUMUIONIS,SUMUIOR,SUMUIORIS)
    pu.addMessage(Product, "calculated Value of FC_TUIO11 is : " + str(FC_TUIO11))
    Product.Attributes.GetByName('FC_TUIO').AssignValue(str(FC_TUIO11))
    Trace.Write("FC_TUIO11: "+str(FC_TUIO11))
#31140
FC_TDIO11=GS_SM_MCAREST_component.get_FC_TDIO11(FDBCUFR,SUMDION,SUMDIONIS,SUMDIOR,SUMDIORIS)
pu.addMessage(Product, "calculated Value of FC_TDIO11 is : " + str(FC_TDIO11))
Product.Attributes.GetByName('FC_TDIO').AssignValue(str(FC_TDIO11))
Trace.Write("FC_TDIO11: "+str(FC_TDIO11))

#value display for 31172
MCAREST_2 = GS_SM_MCAR_02_MCAREST_Calc.MCAR_02_MCAREST_CG_RG_Calc(Product)
pu.addMessage(Product, "calculated Value of MCAREST_2 is : " + str(MCAREST_2))

BCUFREST_2 = m.ceil(MCAREST_2/7.0)
pu.addMessage(Product, "calculated Value of BCUFREST_2 is : " + str(BCUFREST_2))

FDBCUFR_2 = m.ceil(BCUFREST_2*5)
pu.addMessage(Product, "calculated Value of FDBCUFR_2 is : " + str(FDBCUFR_2))