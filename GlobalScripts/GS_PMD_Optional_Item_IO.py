def calc_display(parts_dict, attrs):
    #CXCPQ-21347
    quantity1 = attrs.ioc
    parts_dict['AL-OCIP01'] = quantity1

    quantity2 = attrs.ioc_aldix
    parts_dict['AL-OCIP02'] = quantity2
    return parts_dict