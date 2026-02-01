def calc_display(parts_dict, attrs):
    #CXCPQ-21348
    quantity1 = attrs.dual_cc
    parts_dict['AL-PMCA01'] = quantity1

    quantity2 = attrs.single_cc_600
    parts_dict['AL-PMCA02'] = quantity2

    quantity3 = attrs.single_cc_400
    parts_dict['AL-PMCA03'] = quantity3

    quantity4 = attrs.furn_pie
    parts_dict['AL-IFCS41'] = quantity4

    quantity5 = attrs.wiremaking_ccb
    parts_dict['AL-WMCB01'] = quantity5

    quantity6 = attrs.wiremaking_half
    parts_dict['AL-WMIF01'] = quantity6

    #CXCPQ-21346
    quantity7 = attrs.er_ccct
    parts_dict['AL-ERCC01'] = quantity7

    quantity8 = attrs.er_ccct_r
    parts_dict['AL-ERCC02'] = quantity8


    return parts_dict