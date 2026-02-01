import GS_SM_Power_Attrs
import GS_SM_PowerLoad_C
try:
    attrs = GS_SM_Power_Attrs.AttrStorage(Product)
except Exception,e:
    attrs = None
    Product.ErrorMessages.Add("Error when Reading GS_SM_Power_Attrs: " + str(e))
    Trace.Write("Error when Reading GS_SM_Power_Attrs " + str(e))

    if attrs:
        try:
            component_C = GS_SM_PowerLoad_C.get_component_c(attrs)
        except Exception,e:
            Product.ErrorMessages.Add("Error in GS_SM_PowerLoad_C: " + str(e))