def quantity_display(parts_dict, attrs):
    quantity1 = attrs.tpctb + attrs.tpctb_2
    parts_dict['AL-CCCW01'] = quantity1
    quantity2 = attrs.wmpcp + attrs.wmpcp_2
    parts_dict['AL-WMCC01'] = quantity2
    return parts_dict