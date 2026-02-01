def calc_display(parts_dict, attrs):
    #CXCPQ-21370
    quantity1 = attrs.olm_g11_glass_fo_cable
    parts_dict['6GK1503-2CB00'] = quantity1

    quantity2 = attrs.olm_g12_glass_fo_cable
    parts_dict['6GK1503-3CB00'] = quantity2

    quantity3 = attrs.olm_p11_plastic_fo_cable
    parts_dict['6GK1503-2CA01'] = quantity3

    quantity4 = attrs.olm_p12_plastic_fo_cable
    parts_dict['6GK1503-3CA01'] = quantity4
    return parts_dict