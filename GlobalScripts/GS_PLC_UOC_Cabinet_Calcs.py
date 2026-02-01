import System.Decimal as d

def calc_cabinets(attrs, parts_dict, io_racks): #Added by Ashok

    #CXCPQ-20386 Added by Ashok
    #total_racks_in_cabinet = d.Ceiling(io_racks["Total"] * (1 + attrs.cabinet_spare_space))
    one_slot = 0.0
    if '900R01-0300' in parts_dict:
        try:
            one_slot = parts_dict['900R01-0300']
        except:
            one_slot = 0.0
    if '900RR0-0300' in parts_dict:
        try:
            one_slot = parts_dict['900RR0-0300']
        except:
            one_slot = 0.0
    total_racks_in_cabinet = d.Ceiling((io_racks["Total"] + one_slot) * (1 + attrs.cabinet_spare_space))

    #CXCPQ-20387 Added by Ashok
    cabinet_count = 0
    #Trace.Write("abhi:{0}".format(attrs.plc_comm_q_io_slot_spare))
    if attrs.comm_q_cabinet_required == 'Yes':
        if attrs.cabinet_type == "Dual":
            if attrs.cabinet_integ_marshalling == "No":
                cabinet_count = d.Ceiling(total_racks_in_cabinet / 10)
            elif attrs.cabinet_integ_marshalling == "Yes":
                cabinet_count = d.Ceiling(total_racks_in_cabinet / 5)
    
        elif attrs.cabinet_type == "One":
            if attrs.cabinet_integ_marshalling == "No":
                cabinet_count = d.Ceiling(total_racks_in_cabinet / 5)
            elif attrs.cabinet_integ_marshalling == "Yes":
                cabinet_count = d.Ceiling(total_racks_in_cabinet / 2)
    
        #CXCPQ-20389
        if attrs.cabinet_type == "Dual":
            parts_dict["51196958-400"] = 1 * cabinet_count
            parts_dict["CF-MSD000"] = 1 * cabinet_count
            parts_dict["51198959-200"] = 1 * cabinet_count
            parts_dict["51121311-100"] = 1 * cabinet_count
            parts_dict["CC-CBDD01"] = 1 * cabinet_count
            parts_dict["51199948-100"] = 1 * cabinet_count
            parts_dict["MU-C8DSS1"] = 2 * cabinet_count
    
            #CXCPQ-20390
            if attrs.cabinet_door_type == "Standard":
                parts_dict["51197150-100"] = 1 * cabinet_count
                parts_dict["MU-C8DRS1"] = 2 * cabinet_count
            elif attrs.cabinet_door_type == "Double":
                parts_dict["MU-C8DRD1"] = 2 * cabinet_count
    
            #CXCPQ-20391
            if attrs.cabinet_base_size == "100mm":
                parts_dict["MU-C8DBA1"] = 1 * cabinet_count
                parts_dict["CF-SP0000"] = 1 * cabinet_count
            elif attrs.cabinet_base_size == "200mm":
                parts_dict["MU-C8DBA2"] = 1 * cabinet_count
                parts_dict["CF-SP0001"] = 1 * cabinet_count
    
            #CXCPQ-20392
            if attrs.cabinet_door_keylock == "Standard":
                parts_dict["51197165-100"] = 2 * cabinet_count
            elif attrs.cabinet_door_keylock == "Pushbutton":
                parts_dict["51197165-200"] = 2 * cabinet_count
    
            #CXCPQ-20393
            if attrs.cabinet_pwr_entry == "None":
                parts_dict["51306305-300"] = 1 * cabinet_count
            elif attrs.cabinet_pwr_entry == "Double Pole":
                parts_dict["51403902-100"] = 1 * cabinet_count
        
            #CXCPQ-20395
            if attrs.cabinet_light == "Yes":
                parts_dict["MU-CULF01"] = 2 * cabinet_count

        #CXCPQ-20397
        elif attrs.cabinet_type == "One":
            parts_dict["51196958-400"] = 1 * cabinet_count
            parts_dict["CF-MSD000"] = 1 * cabinet_count
            parts_dict["51198959-200"] = 1 * cabinet_count
            parts_dict["51121311-200"] = 1 * cabinet_count
            parts_dict["CC-CBDS01"] = 1 * cabinet_count
            parts_dict["MU-C8SSS1"] = 2 * cabinet_count
    
            #CXCPQ-20398
            if attrs.cabinet_door_type == "Standard":
                parts_dict["51197150-500"] = 1 * cabinet_count
                parts_dict["MU-C8DRS1"] = 1 * cabinet_count
            elif attrs.cabinet_door_type == "Double":
                parts_dict["MU-C8DRD1"] = 1 * cabinet_count
    
            #CXCPQ-20399
            if attrs.cabinet_base_size == "100mm":
                parts_dict["MU-C8SBA1"] = 1 * cabinet_count
                parts_dict["CF-SP0000"] = 1 * cabinet_count
            elif attrs.cabinet_base_size == "200mm":
                parts_dict["MU-C8SBA2"] = 1 * cabinet_count
                parts_dict["CF-SP0001"] = 1 * cabinet_count
    
            #CXCPQ-20400
            if attrs.cabinet_door_keylock == "Standard":
                parts_dict["51197165-100"] = 1 * cabinet_count
            elif attrs.cabinet_door_keylock == "Pushbutton":
                parts_dict["51197165-200"] = 1 * cabinet_count
    
            #CXCPQ-20401
            if attrs.cabinet_pwr_entry == "None":
                parts_dict["51306305-300"] = 1 * cabinet_count
            elif attrs.cabinet_pwr_entry == "Double Pole":
                parts_dict["51403902-100"] = 1 * cabinet_count
    
            #CXCPQ-20403
            if attrs.cabinet_light == "Yes":
                parts_dict["MU-CULF01"] = 1 * cabinet_count
    
        #CXCPQ-20394, CXCPQ-20396, CXCPQ-20402, CXCPQ-20403
        if attrs.cabinet_type == "One" and attrs.cabinet_integ_marshalling == "Yes":
            assign_qty = d.Ceiling(total_racks_in_cabinet / 2)
        else:
            full_cabinet = d.Floor(total_racks_in_cabinet / 10)
            partial_cabinet = total_racks_in_cabinet % 10
            assign_qty = full_cabinet * 2
            
            if partial_cabinet in range(1,6):
                assign_qty = assign_qty + 1
            elif partial_cabinet > 5:
                assign_qty = assign_qty + 2
            
    
        if attrs.cabinet_tstat == "Yes":
            parts_dict["MU-C8TRM1"] = assign_qty
        if attrs.ce_proj_site_volt == '120V':
            parts_dict["51199947-175"] = assign_qty
        elif attrs.ce_proj_site_volt == '240V':
            parts_dict["51199947-275"] = assign_qty
    #Trace.Write("Parts:{0}".format(parts_dict))
    return parts_dict