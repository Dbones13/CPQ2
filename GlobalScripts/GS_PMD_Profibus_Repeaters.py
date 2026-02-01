def calc_display(parts_dict, attrs):
    #CXCPQ-21364
    quantity1 = attrs.repeater
    parts_dict['6ES7972-0AA02-0XA0'] = quantity1

    #PMD_Repeater_for_Profibus_Diagnosis
    quantity2 = attrs.repeater_profib_diag
    parts_dict['6ES7972-0AB01-0XA0'] = quantity2

    return parts_dict