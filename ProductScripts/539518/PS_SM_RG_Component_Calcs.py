import GS_SM_CG_Component_Attribute
import GS_SM_CG_UIO_CALC
import GS_SM_SUMDION_Calcs
import GS_SM_SUMDIOR_Calcs

try:
    attrs = GS_SM_CG_Component_Attribute.AttrStorage(Product)
except Exception,e:
    attrs = None
    Trace.Write("Error when Reading SM CG System Attributes: " + str(e) + " Line Number: 12" )

if attrs:
    try:
        SUMUIONIS = GS_SM_CG_UIO_CALC.get_sum_non_red_is_io(attrs)
    except Exception,e:
        Trace.Write("Error in GS_SM_CG_UIO_CALC: " + str(e) + " Line Number: 19")

    try:
        #TODO: Update the logic to calculate the SUMUIORPF
        SUMUIORPF = 0
    except Exception,e:
        SUMUIORPF = 0
        Trace.Write("Error in GS_SM_CG_UIO_CALC: " + str(e) + " Line Number: 27")

    try:
        SUMRIOR = GS_SM_CG_UIO_CALC.get_sum_red_io(attrs, SUMUIORPF)
    except Exception,e:
        Trace.Write("Error in GS_SM_CG_UIO_CALC: " + str(e) + " Line Number: 33")

    try:
        SUMUIOR_Check = GS_SM_CG_UIO_CALC.get_SM_SC_RIO(attrs, SUMUIORPF)
    except Exception,e:
        Trace.Write("Error in GS_SM_CG_UIO_CALC: " + str(e) + " Line Number: 36")
    try:
        IOComp_SUMDION = GS_SM_SUMDION_Calcs.IOComponents(Product)
        SUMDION = IOComp_SUMDION.SUMDION_value()
    except Exception,e:
        SUMDION = 0
        Trace.Write("Error in SUMDION Calc: " + str(e) + " Line Number: 42")
    try:
        IOComp_SUMDIOR = GS_SM_SUMDIOR_Calcs.IOComponents(Product)
        SUMDIOR = IOComp_SUMDIOR.SUMDIOR_value()
        #pu.addMessage(Product, "calculated Value of SUMDIOR is : " + str(SUMDIOR))
    except Exception,e:
        SUMDIOR = 0
        Trace.Write("Error in SUMDIOR Calc: " + str(e) + " Line Number: 49")

    try:
        SUMDIONIS = GS_SM_CG_UIO_CALC.get_sum_non_red_is_dio(attrs)
    except Exception,e:
        Trace.Write("Error in GS_SM_CG_UIO_CALC: " + str(e) + " Line Number: 58")

    try:
        SUMRIORIS = GS_SM_CG_UIO_CALC.get_sum_red_is_io(attrs) # Same calculation as 30835
    except Exception,e:
        Trace.Write("Error in GS_SM_CG_UIO_CALC: " + str(e) + " Line Number: 64")

try:
    power_attrs = GS_SM_Power_Attrs.AttrStorage(Product)
except Exception,e:
    power_attrs = None
    Trace.Write("Error when Reading SM CG Power Attributes: " + str(e) + " Line Number: 70")

if power_attrs:
    try:
        component_b = GS_SM_Power_Calc.get_power_component_b(power_attrs)
        pu.addMessage(Product, "Calculated value of component B is : " + str(component_b))
    except Exception,e:
        Trace.Write("Error in GS_SM_Power_Calc - Component B calculations: " + str(e) + " Line Number: 78")