import GS_RTU_ReadAttrs
import GS_RTU_Software_Calcs
import GS_RTU_Part_Update
import GS_RTU_CG_Cabinet_Calcs
import GS_RTU_CG_Software_Calcs
import GS_RTU_CG_IO_Calcs
import GS_RTU_Replica_Config
import GS_RTU_CG_AdditionalController_Cals
try:
    attrs = GS_RTU_ReadAttrs.AttrStorage(Product)
except Exception,e:
    attrs = None
    Product.Messages.Add("Error when Reading RTU System Attributes: " + str(e))
    Trace.Write("Error when Reading RTU System Attributes: " + str(e))
    Log.Error("Error when Reading RTU System Attributes: " + str(e))

parts_dict = {}

if attrs:
    try:
        parts_dict = GS_RTU_CG_Cabinet_Calcs.calc_cabinet_rtu_system(attrs, parts_dict)
    except Exception,e:
        Product.Messages.Add("Error in GS_RTU_CG_Cabinet_Calc: " + str(e))
    try:
        parts_dict = GS_RTU_CG_Software_Calcs.calc_software_rtu_system(attrs, parts_dict)
    except Exception,e:
        Product.Messages.Add("Error in GS_RTU_Software_Calcs: " + str(e))
    try:
        parts_dict = GS_RTU_CG_IO_Calcs.calc_io_details_rtu_system(attrs, parts_dict)
    except Exception,e:
        Product.Messages.Add("Error in GS_RTU_CG_IO_Calcs: " + str(e))
    try:
        parts_dict = GS_RTU_CG_AdditionalController_Cals.calc_additional_rtu_system(attrs, parts_dict)
    except Exception,e:
        Product.Messages.Add("Error in GS_RTU_CG_AdditionalController_Cals: " + str(e))
    
    '''try:
        parts_dict = GS_RTU_Software_Calcs.calc_software_rtu_system(attrs, parts_dict)
    except Exception,e:
        Product.Messages.Add("Error in GS_RTU_Software_Calcs: " + str(e))'''
    
    try:
        parts_dict = GS_RTU_Replica_Config.multiply_replica_config_cg(Product, parts_dict)
    except Exception,e:
        Product.Messages.Add("Error in GS_RTU_Replica_Config: " + str(e))
    Trace.Write("debugging: " + str(parts_dict))
    GS_RTU_Part_Update.execute(Product, 'RTU_CG_PartSummary_Cont', parts_dict)