def calc_field_pow_supp(parts_dict, attrs):
    #CXCPQ-21333
    quantity = attrs.red_24vdc_pwr_supp
    parts_dict['PD-FPCB03'] = quantity
    
    #CXCPQ-21358
    parts_dict['AL-FPCB01'] = attrs.fps_10a + attrs.fps_10a_2
    parts_dict['AL-FPCB02'] = attrs.fps_20a + attrs.fps_20a_2
    
    return parts_dict