import GS_PLC_UOC_IO_Calcs
import GS_PLC_UOC_Racks_Calcs
import GS_PLC_UOC_Processor_Calcs
import GS_PLC_UOC_PSU_Calcs
import GS_PLC_UOC_Software_Calcs
import GS_PLC_UOC_Terminal_Calcs
import GS_PLC_UOC_Auxilary_Calcs
import GS_PLC_UOC_Network_Calcs
import GS_PLC_UOC_Cabinet_Calcs
import GS_UOC_ReadAttrs
import GS_PLC_UOC_PartUpdate

try:
    attrs = GS_UOC_ReadAttrs.AttrStorage(Product)
except Exception,e:
    attrs = None
    Product.Messages.Add("Error when Reading UOC CG Attributes: " + str(e))
parts_dict = {}

if attrs:
    try:
        parts_dict,IO_mods = GS_PLC_UOC_IO_Calcs.calc_io_modules(attrs, parts_dict)
    except Exception,e:
        Product.Messages.Add("Error in GS_PLC_UOC_IO_Calcs: " + str(e))

    try:
        parts_dict,io_racks = GS_PLC_UOC_Racks_Calcs.calc_racks(attrs, parts_dict, IO_mods)
    except Exception,e:
        Product.Messages.Add("Error in GS_PLC_UOC_Racks_Calcs: " + str(e))

    try:
        parts_dict,io_racks = GS_PLC_UOC_Processor_Calcs.calc_processor_modules(attrs, parts_dict, io_racks, IO_mods,Product)
    except Exception,e:
        Product.Messages.Add("Error in GS_PLC_UOC_Processor_Calcs: " + str(e))

    try:
        parts_dict = GS_PLC_UOC_Cabinet_Calcs.calc_cabinets(attrs, parts_dict, io_racks)
    except Exception,e:
        Product.Messages.Add("Error in GS_PLC_UOC_Cabinet_Calcs: " + str(e))

    try:
        parts_dict = GS_PLC_UOC_PSU_Calcs.calc_power_supplies(attrs, parts_dict, io_racks)
    except Exception,e:
        Product.Messages.Add("Error in GS_PLC_UOC_PSU_Calcs: " + str(e))

    try:
        parts_dict = GS_PLC_UOC_Terminal_Calcs.calc_terminals(attrs, parts_dict, IO_mods)
    except Exception,e:
        Product.Messages.Add("Error in GS_PLC_UOC_Terminal_Calcs: " + str(e))

    try:
        parts_dict = GS_PLC_UOC_Auxilary_Calcs.calc_auxilary(attrs, parts_dict)
    except Exception,e:
        Product.Messages.Add("Error in GS_PLC_UOC_Auxilary_Calcs: " + str(e))

    try:
        parts_dict = GS_PLC_UOC_Network_Calcs.calc_network(attrs, parts_dict, io_racks)
    except Exception,e:
        Product.Messages.Add("Error in GS_PLC_UOC_Network_Calcs: " + str(e))

    #parts_dict['900CP1-0200'] += attrs.addl_ctrlr_addl_ctrlr
    parts_dict['900CP1-0300'] += attrs.addl_ctrlr_addl_ctrlr
    if Product.Attr('MIgration_Scope_Choices').GetValue() == 'LABOR':
        parts_dict = dict()

    Trace.Write("Parts Dict: {0}".format(parts_dict))
    GS_PLC_UOC_PartUpdate.execute(Product, 'UOC_CG_PartSummary_Cont', parts_dict,attrs)