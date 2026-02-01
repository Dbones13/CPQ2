def calc_cc_cabinets(parts_dict, attrs):
    
    #CXCPQ-21350, CXCPQ-25531 (TDH)
    parts_dict['PD-CCCS01'] = attrs.ssccc + attrs.ssccc_2
    parts_dict['PD-CCCD01'] = attrs.dsccc + attrs.dsccc_2
    parts_dict['AL-CCAS01'] = attrs.sscc_1200 + attrs.sscc_1200_2
    parts_dict['AL-CCAD01'] = attrs.dscc_1200 + attrs.dscc_1200_2
    parts_dict['PD-CCCS02'] = attrs.sscc_482 + attrs.sscc_482_2
    parts_dict['PD-CCCD02'] = attrs.dscc_482 + attrs.dscc_482_2
    parts_dict['AL-FCCA41'] = attrs.sscc_d400 + attrs.sscc_d400_2

    #CXCPQ-21352
    # Moved to GS_PMD_Cross_Connection_Cabling_Terminal
    #parts_dict['AL-CCCW01'] = attrs.tpctb
    #parts_dict['AL-WMCC01'] = attrs.wmpcp
    
    return parts_dict