import System.Decimal as d

def calc_display(parts_dict, attrs):
    #CXCPQ-21345
    #quantity = attrs.analog_oc
    #parts_dict['AL-AOCU01'] = quantity

    #quantity2 = attrs.analog_ic
    #parts_dict['AL-AICU01'] = quantity2

    #quantity3 = attrs.binary_oc
    #parts_dict['AL-DOBL01'] = quantity3

    #quantity4 = attrs.power_boc_115v
    #parts_dict['AL-DOPL01'] = quantity4

    #quantity5 = attrs.power_boc_230v
    #parts_dict['AL-DOPH01'] = quantity5

    #quantity6 = attrs.binary_ic_16ch
    #parts_dict['AL-DISL01'] = quantity6

    #quantity7 = attrs.binary_ic_24ch
    #parts_dict['AL-DIML01'] = quantity7

    #quantity8 = attrs.power_bic_115v
    #parts_dict['AL-DIPL01'] = quantity8

    #quantity9 = attrs.power_bic_230v
    #parts_dict['AL-DIPH01'] = quantity9
    
    #CXCPQ-21345 new_changes_with_calculation
    quantity = attrs.analog_oc
    parts_dict['AL-AOCU01'] = d.Ceiling(quantity*(1+(attrs.io_space_req/100.0))/10.0)

    quantity2 = attrs.analog_ic
    parts_dict['AL-AICU01'] = d.Ceiling(quantity2*(1+(attrs.io_space_req/100.0))/10.0)

    quantity3 = attrs.binary_oc
    parts_dict['AL-DOBL01'] = d.Ceiling(quantity3*(1+(attrs.io_space_req/100.0))/16.0)

    quantity4 = attrs.power_boc_115v
    parts_dict['AL-DOPL01'] = d.Ceiling(quantity4*(1+(attrs.io_space_req/100.0))/8.0)

    quantity5 = attrs.power_boc_230v
    parts_dict['AL-DOPH01'] = d.Ceiling(quantity5*(1+(attrs.io_space_req/100.0))/8.0)

    quantity6 = attrs.binary_ic_16ch
    parts_dict['AL-DISL01'] = d.Ceiling(quantity6*(1+(attrs.io_space_req/100.0))/16.0)

    quantity7 = attrs.binary_ic_24ch
    parts_dict['AL-DIML01'] = d.Ceiling(quantity7*(1+(attrs.io_space_req/100.0))/24.0)

    quantity8 = attrs.power_bic_115v
    parts_dict['AL-DIPL01'] = d.Ceiling(quantity8*(1+(attrs.io_space_req/100.0))/16.0)

    quantity9 = attrs.power_bic_230v
    parts_dict['AL-DIPH01'] = d.Ceiling(quantity9*(1+(attrs.io_space_req/100.0))/16.0)

    return parts_dict