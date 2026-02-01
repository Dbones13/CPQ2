import GS_PLC_UOC_IO_Calcs
import GS_PLC_UOC_Racks_Calcs
import GS_PLC_UOC_Processor_Calcs
import GS_PLC_UOC_PSU_Calcs
import GS_PLC_UOC_Terminal_Calcs
import GS_PLC_UOC_Auxilary_Calcs
import GS_PLC_UOC_Cabinet_Calcs
import GS_UOC_ReadAttrs
import GS_PLC_UOC_PartUpdate
isR2Qquote = True if Quote.GetCustomField("isR2QRequest").Content else False
Checkproduct = Product.ParseString('<*CTX(Product.RootProduct.PartNumber)*>')
try:
    attrs = GS_UOC_ReadAttrs.AttrStorage(Product)
    if (isR2Qquote and  Checkproduct != "Migration") and (not attrs.ctrl_rack_pwr_sply):
        attrs.ctrl_rack_pwr_sply = 'NonRedundant'
except Exception,e:
    attrs = None
    Product.Messages.Add("Error when Reading UOC RG Attributes: " + str(e))
    Trace.Write("Error when Reading UOC RG Attributes: " + str(e))
    #Log.Error("Error when Reading UOC RG Attributes: " + str(e))
parts_dict = {}

if attrs:
    try:
        parts_dict,IO_mods = GS_PLC_UOC_IO_Calcs.calc_io_modules(attrs, parts_dict)
    except Exception,e:
        Product.ErrorMessages.Add("Error in GS_PLC_UOC_IO_Calcs: " + str(e))

    try:
        parts_dict,io_racks = GS_PLC_UOC_Racks_Calcs.calc_racks(attrs, parts_dict, IO_mods)
    except Exception,e:
        Product.ErrorMessages.Add("Error in GS_PLC_UOC_Racks_Calcs: " + str(e))

    try:
        parts_dict = GS_PLC_UOC_Cabinet_Calcs.calc_cabinets(attrs, parts_dict, io_racks)
    except Exception,e:
        Product.ErrorMessages.Add("Error in GS_PLC_UOC_Cabinet_Calcs: " + str(e))

    try:
        parts_dict = GS_PLC_UOC_PSU_Calcs.calc_power_supplies(attrs, parts_dict, io_racks)
    except Exception,e:
        Product.ErrorMessages.Add("Error in GS_PLC_UOC_PSU_Calcs: " + str(e))

    try:
        parts_dict = GS_PLC_UOC_Terminal_Calcs.calc_terminals(attrs, parts_dict, IO_mods)
    except Exception,e:
        Product.ErrorMessages.Add("Error in GS_PLC_UOC_Terminal_Calcs: " + str(e))

    try:
        parts_dict = GS_PLC_UOC_Auxilary_Calcs.calc_auxilary(attrs, parts_dict)
    except Exception,e:
        Product.ErrorMessages.Add("Error in GS_PLC_UOC_Auxilary_Calcs: " + str(e))

    Trace.Write("Parts Dict: {0}".format(parts_dict))
    #Set the product attributes to enable roll-up calculations
    Product.Attr('UOC_RG_IO_Modules').AssignValue(str(IO_mods['Total']))
    Product.Attr('UOC_RG_Analog_Channels').AssignValue(str(parts_dict['900A01-0202'] + parts_dict['900A16-0103'] + parts_dict['900B01-0301'] + parts_dict['900B08-0202']))
    #Product.Attr('UOC_RG_Digital_Channels').AssignValue(str(parts_dict['900G03-0202'] + parts_dict['900G32-0101'] + parts_dict['900G01-0202'] + parts_dict['900G04-0101'] + parts_dict['900H03-0202'] + parts_dict['900H32-0102'] + parts_dict['900H01-0202']))
    Product.Attr('UOC_RG_Digital_Channels').AssignValue(str(parts_dict['900G03-0202'] + parts_dict['900G32-0301'] + parts_dict['900G01-0202'] + parts_dict['900G04-0101'] + parts_dict['900H03-0202'] + parts_dict['900H32-0302'] + parts_dict['900H01-0202']))
    Product.Attr('UOC_RG_AO_Modules').AssignValue(str(parts_dict['900B01-0301'] + parts_dict['900B08-0202']))
    Product.Attr('UOC_RG_IO_Racks').AssignValue(str(io_racks["Total"]))
    if Product.Attr('MIgration_Scope_Choices').GetValue() == 'LABOR':
        parts_dict = {}

    GS_PLC_UOC_PartUpdate.execute(Product, 'UOC_RG_PartSummary_Cont', parts_dict,attrs)