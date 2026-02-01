def calc_display(parts_dict, attrs):
    #CXCPQ-21356
    quantity1 = attrs.pdc_ds
    parts_dict['PD-PDCA02'] = quantity1


    quantity2 = attrs.pds_230vac
    parts_dict['AL-PWAC01'] = quantity2

    quantity3 = attrs.pds_24vdc
    parts_dict['AL-PWDC02'] = quantity3
    return parts_dict