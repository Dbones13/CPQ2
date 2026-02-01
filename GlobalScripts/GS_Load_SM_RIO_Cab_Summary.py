from GS_SM_PowerLoad_IOTA_A_Calc import PowerLoad_IOTA_A_Calc
from GS_SM_Power_Calc import get_power_component_b
from GS_SM_PowerLoad_C import get_component_c
import GS_SM_Power_Attrs

def getLoadSMRIOCabSummary(Product):
    try:
        power_attrs = GS_SM_Power_Attrs.AttrStorage(Product)
    except Exception,e:
        power_attrs = None
        Product.ErrorMessages.Add("Error when Reading SM CG Power Attributes: " + str(e))
        Trace.Write("Error when Reading SM CG Power Attributes: " + str(e))
    
    try:
        component_A = float(PowerLoad_IOTA_A_Calc(Product))
    except Exception,e:
        component_A = 0
        Product.ErrorMessages.Add("Error in GS_SM_PowerLoad_IOTA_A_Calc: " + str(e))
    try:
        component_B = float(get_power_component_b(power_attrs))
    except Exception,e:
        component_B = 0
        Product.ErrorMessages.Add("Error in GS_SM_Power_Calc: " + str(e))
    try:
        component_C = float(get_component_c(power_attrs))
    except Exception,e:
        component_C = 0
        Product.ErrorMessages.Add("Error in GS_SM_PowerLoad_C: " + str(e))

    component_D = 0

    Load_SM_RIO_calc =  (component_A+ component_B+ component_C+component_D)/1000

    return Load_SM_RIO_calc