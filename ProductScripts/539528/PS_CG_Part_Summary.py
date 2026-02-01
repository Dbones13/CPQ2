import GS_RTU_ReadAttrs
import GS_RTU_Software_Calcs
import GS_RTU_Part_Update
import GS_RTU_CG_Cabinet_Calcs
import GS_RTU_CG_Software_Calcs
import GS_RTU_CG_IO_Calcs
import GS_RTU_Replica_Config
import GS_RTU_CG_AdditionalController_Cals
import GS_RTU_CG_Get_Total_IO

attrs = GS_RTU_ReadAttrs.AttrStorage(Product)
parts_dict = {}
if attrs:
    io = GS_RTU_CG_Get_Total_IO.total_io_rtu(attrs)
    dio = GS_RTU_CG_Get_Total_IO.total_dio_rtu(attrs)
    parts_dict = GS_RTU_CG_Cabinet_Calcs.calc_cabinet_rtu_system(attrs, parts_dict, io, dio)
    parts_dict = GS_RTU_CG_Software_Calcs.calc_software_rtu_system(attrs, parts_dict)
    parts_dict = GS_RTU_CG_IO_Calcs.calc_io_details_rtu_system(attrs, parts_dict)
    parts_dict = GS_RTU_CG_AdditionalController_Cals.calc_additional_rtu_system(attrs, parts_dict)
    parts_dict = GS_RTU_Replica_Config.multiply_replica_config_cg(Product, parts_dict)
    GS_RTU_Part_Update.execute(Product, 'RTU_CG_PartSummary_Cont', parts_dict)

