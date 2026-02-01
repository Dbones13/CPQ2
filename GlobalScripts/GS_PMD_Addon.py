def calc_display(parts_dict, attrs):
    #CXCPQ-24570
    quantity1 = round(attrs.des_mod)
    parts_dict['PD-DMNL01'] = quantity1
    quantity2 = round(attrs.des_mod_mr)
    parts_dict['PD-DMNL02'] = quantity2
    return parts_dict