def calc_display(parts_dict, attrs):
    #CXCPQ-21368
    quantity3 = attrs.anybus_x

	#CXCPQ-21366
    quantity1 = attrs.dp_coupler
    parts_dict['6ES7158-0AD01-0XA0'] = quantity1

    quantity2 = attrs.ab7646f_anybus
    parts_dict['AB7646-F'] = quantity2
    return parts_dict