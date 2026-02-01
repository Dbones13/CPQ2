import GS_SM_Power_Attrs
import GS_SM_PowerLoad_C

try:
    attrs = GS_SM_Power_Attrs.AttrStorage(Product)
except Exception,e:
    attrs = None
    #Product.ErrorMessages.Add("Error when Reading GS_SM_Power_Attrs: " + str(e) + " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))
    Trace.Write("Error when Reading GS_SM_Power_Attrs" + str(e))

if attrs:
    try:
        component_c = GS_SM_PowerLoad_C.get_component_c(attrs)
    except Exception,e:
        #Product.ErrorMessages.Add("Error in GS_SM_PowerLoad_C: " + str(e) + " Line Number: " + str(sys.exc_traceback.tb_next.tb_lineno))
        Trace.Write("Error in GS_SM_PowerLoad_C " + str(e))