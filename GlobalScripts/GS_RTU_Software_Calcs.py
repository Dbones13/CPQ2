def calc_software_rtu_system(attrs, parts_dict):
    RTU_Release = {
            '172': ['SP-EMD172',{'Quantity' : '1', 'Description': 'CONTROLEDGE Builder R172, Media Kit'}],
            '171': ['SP-EMD171',{'Quantity' : '1', 'Description': 'CONTROLEDGE Builder R171, Media Kit'}],
            '174': ['SP-EMD174',{'Quantity' : '1', 'Description': 'CONTROLEDGE Builder R174, Media Kit'}],
            '180': ['SP-EMD180',{'Quantity' : '1', 'Description': 'CONTROLEDGE Builder R180, Media Kit'}],
            '181': ['SP-EMD181',{'Quantity' : '1', 'Description': 'CONTROLEDGE Builder R181, Media Kit'}],
            '182': ['SP-EMD182',{'Quantity' : '1', 'Description': 'CONTROLEDGE Builder R182, Media Kit'}]
            }
    if attrs.base_media_delivery == 'PD':
        if RTU_Release.get(attrs.ce_rtu_release):
            parts_dict[RTU_Release.get(attrs.ce_rtu_release)[0]] = RTU_Release.get(attrs.ce_rtu_release)[1]
    elif attrs.base_media_delivery == 'ED':
        if RTU_Release.get(attrs.ce_rtu_release):
            parts_dict[str(RTU_Release.get(attrs.ce_rtu_release)[0])+'-ESD'] = RTU_Release.get(attrs.ce_rtu_release)[1]
    if attrs.gas_liquid_cals == 'Yes':
        parts_dict['SP-MCALC1'] = {'Quantity' : '1', 'Description': 'Gas Liquid Calculation Library'}
    if int(attrs.builder_client_License):
        parts_dict['SP-EBLDR1'] = {'Quantity' : attrs.builder_client_License, 'Description': 'ControlEdge Builder Client License'}
    if int(attrs.rtu_engineering_stations):
        parts_dict['MZ-PCWS77'] = {'Quantity' :attrs.rtu_engineering_stations, 'Description': 'Desk Mount Engineering Station'}
        parts_dict['TP-FPW231'] = {'Quantity' :attrs.rtu_engineering_stations, 'Description': '23 Inch Display monitor'}
    return parts_dict