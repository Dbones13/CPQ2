def calc_power_supplies(attrs, parts_dict, io_racks):

    #CXCPQ-20338 Added by Ashok
    try:
        #cpm_racks = parts_dict['900RR0-0200']
        cpm_racks = parts_dict['900RR0-0300']
    except:
        cpm_racks = 0.0
    try:
        one_slot = parts_dict['900R01-0300']
    except:
        one_slot = 0.0
    if attrs.ctrl_rack_pwr_sply == "Redundant":

        if attrs.ctrl_rack_pwr_input == "AC" and attrs.ctrl_operating_temp == '0 to 60 DegC or Marine application':
            parts_dict["900P01-0501"] = (2 * io_racks["Redundant"]) + (2 * cpm_racks)
        elif attrs.ctrl_rack_pwr_input == "AC" and attrs.ctrl_operating_temp == 'Extended -40 to 70 DegC':
            #parts_dict["900P01-0301"] = (2 * io_racks["Redundant"]) + (2 * cpm_racks)
            parts_dict["900P01-0701"] = (2 * io_racks["Redundant"]) + (2 * cpm_racks)

        elif attrs.ctrl_rack_pwr_input == "DC":
            #parts_dict["900P24-0301"] = (2 * io_racks["Redundant"]) + (2 * cpm_racks)
            parts_dict["900P24-0501"] = (2 * io_racks["Redundant"]) + (2 * cpm_racks)

    elif attrs.ctrl_rack_pwr_sply == "NonRedundant":

        if attrs.ctrl_rack_pwr_input == "AC" and attrs.ctrl_operating_temp == '0 to 60 DegC or Marine application':
            #parts_dict["900P01-0301"] = (1 * io_racks["NonRedundant"]) + (2 * cpm_racks) + (one_slot)
            parts_dict["900P01-0501"] = (1 * io_racks["NonRedundant"]) + (2 * cpm_racks) + (one_slot)
        elif attrs.ctrl_rack_pwr_input == "AC" and attrs.ctrl_operating_temp == 'Extended -40 to 70 DegC':
            parts_dict["900P01-0701"] = (1 * io_racks["NonRedundant"]) + (2 * cpm_racks) + (one_slot)

        elif attrs.ctrl_rack_pwr_input == "DC":
            #parts_dict["900P24-0301"] = (1 * io_racks["NonRedundant"]) + (2 * cpm_racks) + (one_slot)
            parts_dict["900P24-0501"] = (1 * io_racks["NonRedundant"]) + (2 * cpm_racks) + (one_slot)

    #CXCPQ-20341 Added by Sumanth

    parts_dict['900PSM-0200'] = 0 #Fixed by Paul
    if '900RNF-0200' not in parts_dict:
        parts_dict['900RNF-0200'] = 0
    Trace.Write("initial RNF: {}".format(parts_dict['900RNF-0200']))
    if attrs.ctrl_rack_pwr_sply == "Redundant":
        if attrs.ctrl_rack_pwr_status_mod_red_sply == 'Yes' and attrs.ctrl_rack_io_rack_type == '8Rack':
            #parts_dict['900PSM-0200'] += parts_dict['900R08R-0200']
            parts_dict['900PSM-0200'] += parts_dict['900R08R-0300']
        elif attrs.ctrl_rack_pwr_status_mod_red_sply == 'No' and attrs.ctrl_rack_io_rack_type == '8Rack':
            #parts_dict['900RNF-0200'] += parts_dict['900R08R-0200']
            parts_dict['900RNF-0200'] += parts_dict['900R08R-0300']
        elif attrs.ctrl_rack_pwr_status_mod_red_sply == 'Yes' and attrs.ctrl_rack_io_rack_type == '12Rack':
            #parts_dict['900PSM-0200'] += parts_dict['900R12R-0200']
            parts_dict['900PSM-0200'] += parts_dict['900R12R-0300']
        elif attrs.ctrl_rack_pwr_status_mod_red_sply == 'No' and attrs.ctrl_rack_io_rack_type == '12Rack':
            #parts_dict['900RNF-0200'] += parts_dict['900R12R-0200']
            parts_dict['900RNF-0200'] += parts_dict['900R12R-0300']
        elif attrs.ctrl_rack_pwr_status_mod_red_sply == 'Yes' and attrs.ctrl_rack_io_rack_type == 'OptimumRack':
            if '900R08R-0300' in parts_dict:
                #parts_dict['900PSM-0200'] += parts_dict['900R08R-0200']
                parts_dict['900PSM-0200'] += parts_dict['900R08R-0300']
            if '900R12R-0300' in parts_dict:
                parts_dict['900PSM-0200'] += parts_dict['900R12R-0300']
                #parts_dict['900PSM-0200'] += parts_dict['900R12R-0200']
        elif attrs.ctrl_rack_pwr_status_mod_red_sply == 'No' and attrs.ctrl_rack_io_rack_type == 'OptimumRack':
            if '900R08R-0300' in parts_dict:
                #parts_dict['900RNF-0200'] += parts_dict['900R08R-0200']
                parts_dict['900RNF-0200'] += parts_dict['900R08R-0300']
            if '900R12R-0300' in parts_dict:
                #parts_dict['900RNF-0200'] += parts_dict['900R12R-0200']
                parts_dict['900RNF-0200'] += parts_dict['900R12R-0300']
    '''elif attrs.ctrl_rack_pwr_sply == "NonRedundant":
        if attrs.ctrl_rack_io_rack_type == '4Rack':
            #parts_dict['900RNF-0200'] += parts_dict['900R04-0200']
            parts_dict['900RNF-0200'] += parts_dict['900R04-0300']
            
        elif attrs.ctrl_rack_io_rack_type == '8Rack':
            #parts_dict['900RNF-0200'] += parts_dict['900R08-0200']
            parts_dict['900RNF-0200'] += parts_dict['900R08-0300']
        elif attrs.ctrl_rack_io_rack_type == '12Rack':
            #parts_dict['900RNF-0200'] += parts_dict['900R12-0200']
            parts_dict['900RNF-0200'] += parts_dict['900R12-0300']
        elif attrs.ctrl_rack_io_rack_type == 'OptimumRack':
            if '900R04-0300' in parts_dict:
                #parts_dict['900RNF-0200'] += parts_dict['900R04-0200']
                parts_dict['900RNF-0200'] += parts_dict['900R04-0300']
            if '900R08-0300' in parts_dict: 
                #parts_dict['900RNF-0200'] += parts_dict['900R08-0200']
                parts_dict['900RNF-0200'] += parts_dict['900R08-0300']
            elif '900R12-0300' in parts_dict:
                #parts_dict['900RNF-0200'] += parts_dict['900R12-0200']
                parts_dict['900RNF-0200'] += parts_dict['900R12-0300']'''

    return parts_dict