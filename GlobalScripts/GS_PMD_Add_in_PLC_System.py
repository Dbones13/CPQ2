import System.Decimal as d

def pmd_plc_system(parts_dict, attrs):

    # Racks & Cabinets
    quantity = d.Ceiling(attrs.pmd_plc_rack_8)
    parts_dict['900R08-0200'] = quantity
    quantity = d.Ceiling(attrs.pmd_plc_rack_12)
    parts_dict['900R12-0200'] = quantity
    quantity = attrs.pmd_plc_cab
    parts_dict['PD-C9SS01'] = quantity
    
    # Power Supplies
    parts_dict['900P01-0301'] = d.Ceiling(attrs.pmd_plc_rack_8 + attrs.pmd_plc_rack_12)
    
    #EPM with PROFINET Software
    parts_dict['PD-PNSEPM1'] = d.Ceiling(attrs.pmd_plc_rack_8 + attrs.pmd_plc_rack_12)
    
    #PLC I/O Cards
    quantity = attrs.pmd_plc_univ_io
    pmd_plc_univ_io_quant = d.Ceiling(quantity*(1+attrs.pmd_io_space_2/100)/16.0)
    parts_dict['900U01-0100'] = pmd_plc_univ_io_quant
    
    quantity = attrs.pmd_plc_univ_ai
    pmd_plc_univ_ai_quant = d.Ceiling(quantity*(1+attrs.pmd_io_space_2/100)/8.0)
    parts_dict['900A01-0202'] = pmd_plc_univ_ai_quant
    
    quantity = attrs.pmd_plc_di_16
    pmd_plc_di_16_quant = d.Ceiling(quantity*(1+attrs.pmd_io_space_2/100)/16.0)
    parts_dict['900G03-0202'] = pmd_plc_di_16_quant
    
    quantity = attrs.pmd_plc_di_32
    pmd_plc_di_32_quant = d.Ceiling(quantity*(1+attrs.pmd_io_space_2/100)/32.0)
    parts_dict['900G32-0101'] = pmd_plc_di_32_quant
    
    quantity = attrs.pmd_plc_do_8
    pmd_plc_do_8_quant = d.Ceiling(quantity*(1+attrs.pmd_io_space_2/100)/8.0)
    parts_dict['900H03-0202'] = pmd_plc_do_8_quant
    
    quantity = attrs.pmd_plc_do_32
    pmd_plc_do_32_quant = d.Ceiling(quantity*(1+attrs.pmd_io_space_2/100)/32.0)
    parts_dict['900H32-0102'] = pmd_plc_do_32_quant
    
    
    # Blank Covers
    parts_dict['900TNF-0200'] = max((attrs.pmd_plc_rack_8 * 8) + (attrs.pmd_plc_rack_12 * 12) - (pmd_plc_univ_io_quant + pmd_plc_univ_ai_quant + pmd_plc_di_16_quant + pmd_plc_di_32_quant + pmd_plc_do_8_quant + pmd_plc_do_32_quant), 0)


    return parts_dict