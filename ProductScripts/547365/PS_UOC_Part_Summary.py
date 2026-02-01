import GS_PLC_UOC_Software_Calcs
import GS_PLC_UOC_PartUpdate
import GS_UOC_ReadAttrs

try:
    attrs = GS_UOC_ReadAttrs.AttrStorage(Product)
except Exception,e:
    attrs = None
    Product.ErrorMessages.Add("Error when Reading UOC System Attributes: " + str(e))
parts_dict = {}

if attrs:
    # Paul - commented this out because all the software calcs are PLC-specific. When can add this back in when we get the UOC-specific ones in.
    try:
        parts_dict = GS_PLC_UOC_Software_Calcs.calc_software_uoc_system(attrs,parts_dict)
    except Exception,e:
        Product.ErrorMessages.Add("Error in GS_PLC_UOC_Software_Calcs: " + str(e))

    GS_PLC_UOC_PartUpdate.execute(Product, 'UOC_PartSummary_Cont', parts_dict)