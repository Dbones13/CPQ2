def calc_display(parts_dict,attrs):
    #Added by Siddharth CXCPQ-25458
    if attrs.prc_sol == 1:
        parts_dict['TC-SWCS90'] = 1
    return parts_dict