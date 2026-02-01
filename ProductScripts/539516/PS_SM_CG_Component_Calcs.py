import ProductUtil as pu
import GS_SM_CG_Component_Attribute
import GS_SM_Power_Attrs
import GS_SM_CG_UIO_CALC
import GS_SM_Power_Calc
import GS_SMIOComponents

try:
    attrs = GS_SM_CG_Component_Attribute.AttrStorage(Product)
except Exception,e:
    attrs = None
    #Product.ErrorMessages.Add("Error when Reading SM CG System Attributes: " + str(e) + " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))
    Trace.Write("Error when Reading SM CG System Attributes: " + str(e) + " Line Number: 14")

try:
    power_attrs = GS_SM_Power_Attrs.AttrStorage(Product)
except Exception,e:
    power_attrs = None
    #Product.ErrorMessages.Add("Error when Reading SM CG Power Attributes: " + str(e) + " Line Number: 20")
    Trace.Write("Error when Reading SM CG Power Attributes: " + str(e) + " Line Number: 21")

try:
    IOComp = GS_SMIOComponents.IOComponents(Product)
    SUMUIONPF, SUMUIORPF = IOComp.getUniversalIOCountRedNonRed()
    pu.addMessage(Product, "calculated Value of SUMUIORPF is : " + str(SUMUIORPF))
    pu.addMessage(Product, "calculated Value of SUMUIONPF is : " + str(SUMUIONPF))
except Exception,e:
    SUMUIORPF = 0
    SUMUIONPF = 0
    Trace.Write("Error in SUMUIORPF & SUMUIONPF Calc: " + str(e) + " Line Number: 31")
if attrs:
    try:
        SUMUIONIS = GS_SM_CG_UIO_CALC.get_sum_non_red_is_io(attrs)
    except Exception,e:
        Trace.Write("Error in GS_SM_CG_UIO_CALC: " + str(e) + " Line Number: 36")

    try:
        SUMRIOR = GS_SM_CG_UIO_CALC.get_sum_red_io(attrs, SUMUIORPF)
        pu.addMessage(Product, "calculated Value of SUMRIOR is : " + str(SUMRIOR))
    except Exception,e:
        Trace.Write("Error in GS_SM_CG_UIO_CALC: " + str(e) + " Line Number: 42")

if power_attrs:
    try:
        component_b = GS_SM_Power_Calc.get_power_component_b(power_attrs)
        pu.addMessage(Product, "Calculated value of component B is : " + str(component_b))
    except Exception,e:
        Trace.Write("Error in GS_SM_Power_Calc - Component B calculations: " + str(e) + " Line Number: 49")
    # Please replace the particular compenents with there respective calculations - Krishna
    component_a = 0 # CXCPQ-31144
    component_c = 0 # CXCPQ-31146
    component_d = 0 # CXCPQ-31155

    components = {'A': component_a, 'B': component_b, 'C': component_c, 'D': component_d}
    """try:
        total_rio_cabinet_summary = GS_SM_Total_RIO_Cabinet_Summary.get_total_rio_cabinet_summary(components)
    except Exception,e:
        Trace.Write("Error in GS_SM_Total_RIO_Cabinet_Summary Total RIO calculations: " + str(e) + " Line Number: 59")"""