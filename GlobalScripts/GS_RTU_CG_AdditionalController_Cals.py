def calc_additional_rtu_system(attrs, parts_dict):
    # CXCPQ-21373
    if int(attrs.add_ctrl)>0:
        qty = attrs.add_ctrl
        if attrs.controller_redundancy == "Redundant":
            parts_dict["SC-UCNN11"] = {'Quantity' : qty, 'Description': 'Control Edge RTU Redundant Controller'}
        elif attrs.controller_redundancy == "Non Redundant":
            parts_dict["SC-UCMX02"] = {'Quantity' : qty, 'Description': 'Control Edge RTU Non-Redundant Controller'}


    return parts_dict