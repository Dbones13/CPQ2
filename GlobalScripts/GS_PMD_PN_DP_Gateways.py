def calc_display(parts_dict, attrs):
    #CXCPQ-21368
    quantity = attrs.anybus_x
    parts_dict['AB7646-F'] = quantity

    return parts_dict