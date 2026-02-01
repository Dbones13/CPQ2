import System.Decimal as d

def calc_racks(attrs, parts_dict, IO_mods):
    ## IO Mod = UIO + DI24V + DI110_240 + UAI + DO24V + DO110_24V + PIFI + AIM + AOM + DIC + DORelay + VirtualIO (CXCPQ-20369)
    ### Beg Module Mappings ###
    #UIO: '900U01-0100'
    #UAI: '900A01-0202'
    #DI24V: '900G32-0101'
    #DO24V: '900H32-0102'
    #DI110_240: '900G03-0202', '900G04-0101'
    #DO110_24V: '900H03-0202'
    #DORelay: '900H01-0202'
    #AOM: '900B01-0301', '900B08-0202'
    #AIM: '900A16-0103',
    #PIFI: '900K01-0201'
    #DIC: '900G01-0202'
    #PhysicalIO = UIO + DI24V + DI110_240 + UAI + DO24V + DO110_24V + PIFI + AIM + AOM + DIC + AO8ME + AO8MI
    #VirtualIO = PhysicalIO * SpareSlotRate
    ### End Module Mappings ###

    # BFJ - Added condition, due that UOC does not use 900K01-0201
    if attrs.plc_or_uoc == 'PLC':
        io_slot_spare = attrs.plc_comm_q_io_slot_spare
        io_spare = attrs.plc_comm_q_io_spare
        #IO_mods['Total'] = parts_dict['900U01-0100'] + parts_dict['900A01-0202'] + parts_dict['900G32-0101'] + parts_dict['900H32-0102'] + parts_dict['900G03-0202'] + parts_dict['900G04-0101'] + parts_dict['900H03-0202'] + parts_dict['900H01-0202'] + parts_dict['900B01-0301'] + parts_dict['900B08-0202'] + parts_dict['900A16-0103'] + parts_dict['900K01-0201'] + parts_dict['900G01-0202']

    elif attrs.plc_or_uoc == 'UOC':
        io_slot_spare = attrs.UOC_comm_q_io_slot_spare
        io_spare = attrs.UOC_comm_q_io_spare
        #IO_mods['Total'] = parts_dict['900U01-0100'] + parts_dict['900A01-0202'] + parts_dict['900G32-0101'] + parts_dict['900H32-0102'] + parts_dict['900G03-0202'] + parts_dict['900G04-0101'] + parts_dict['900H03-0202'] + parts_dict['900H01-0202'] + parts_dict['900B01-0301'] + parts_dict['900B08-0202'] + parts_dict['900A16-0103'] + parts_dict['900G01-0202']

    n_total_IO_mods = d.Ceiling(IO_mods['Total'] * (1 + io_slot_spare))
    Trace.Write("n_total_IO_mods: {0}".format(n_total_IO_mods))

    # number of modules used for constraints outlined in CXCPQ-20370
    # calculation of n_ao8_ext and n_ao8_int should be handled in calc modules
    n_ao8_ext = d.Ceiling((attrs.other_io_ao8_extrnl / 8) * (1 + io_spare))
    n_ao8_int = d.Ceiling((attrs.other_io_ao8_intrnl / 8) * (1 + io_spare))
    n_ao4 = d(parts_dict['900B01-0301'])
    n_generic = d(n_total_IO_mods - n_ao8_ext - n_ao8_int - n_ao4)
    Trace.Write("n_ao8_ext: {0}, n_ao8_int: {1}".format(n_ao8_ext, n_ao8_int))

    # CXCPQ-20374
    qty = 0
    n_12_slot_nr = n_12_slot_r = n_8_slot_nr = n_8_slot_r = n_4_slot = 0
    if attrs.ctrl_rack_io_rack_type == "OptimumRack":
        base_qty = d.Floor(n_total_IO_mods / 12)    
        remainder = n_total_IO_mods % 12
        constraint_qty = d.Ceiling(max((d.Ceiling(n_ao8_int/5) + d.Ceiling(n_ao8_ext/10)), n_ao4/10))
        Trace.Write("Base Qty: {0}, Constraint Qty: {1}, Remainder: {2}".format(base_qty, constraint_qty, remainder))
        
        if constraint_qty < base_qty + 1: #this is the normal optimum rack calculation
            if attrs.ctrl_rack_pwr_sply == "Redundant":
                if (remainder > 8):
                    #parts_dict['900R12R-0200'] = n_12_slot_r = base_qty + 1
                    parts_dict['900R12R-0300'] = n_12_slot_r = base_qty + 1
                elif 1 <= remainder <= 8:
                    #parts_dict['900R12R-0200'] = n_12_slot_r = base_qty
                    parts_dict['900R12R-0300'] = n_12_slot_r = base_qty
                    #parts_dict['900R08R-0200'] = n_8_slot_r = 1
                    parts_dict['900R08R-0300'] = n_8_slot_r = 1
                elif remainder == 0:
                    #parts_dict['900R12R-0200'] = n_12_slot_r = base_qty
                    parts_dict['900R12R-0300'] = n_12_slot_r = base_qty
            elif attrs.ctrl_rack_pwr_sply == "NonRedundant":
                if (5 <= remainder <= 8):
                    #parts_dict['900R12-0200'] = n_12_slot_nr = base_qty
                    parts_dict['900R12-0300'] = n_12_slot_nr = base_qty
                    #parts_dict['900R08-0200'] = n_8_slot_nr = 1
                    parts_dict['900R08-0300'] = n_8_slot_nr = 1
                elif (1 <= remainder <= 4):
                    #parts_dict['900R12-0200'] = n_12_slot_nr = base_qty
                    parts_dict['900R12-0300'] = n_12_slot_nr = base_qty
                    #parts_dict['900R04-0200'] = n_4_slot = 1
                    parts_dict['900R04-0300'] = n_4_slot = 1
                elif (remainder > 8):
                   #parts_dict['900R12-0200'] = n_12_slot_nr = base_qty + 1 
                    parts_dict['900R12-0300'] = n_12_slot_nr = base_qty + 1 
                elif remainder == 0:
                    #parts_dict['900R12-0200'] = n_12_slot_nr = base_qty
                    parts_dict['900R12-0300'] = n_12_slot_nr = base_qty

        elif constraint_qty >= base_qty + 1: #this calculates the number of slots garnered from 100% 8-slot racks. Then, calculates the difference between that number and the total number of IO modules, and uses that to determine the number of needed 12-slot racks.
            slot_diff_total = slot_diff = d.Ceiling((n_total_IO_mods - constraint_qty * 8) / 4) #upgrade from 8 to 12 slot rack is a +4
            Trace.Write("slot_diff_total: {0}".format(slot_diff_total))
            if n_ao4>0:
                slot_diff_ao4 = d.Ceiling((n_ao4 - constraint_qty * 8) / 2) #upgrade from 8 to 12 slot rack is only a +2, because a04 maxes out at 10/rack
                slot_diff = max(slot_diff, slot_diff_ao4)
                Trace.Write("slot_diff_ao4: {0}".format(slot_diff_ao4))
            if n_ao8_ext>0:
                slot_diff_ao8 = d.Ceiling((n_ao8_ext - (constraint_qty - d.Ceiling(n_ao8_int/5)) * 8) / 2) #upgrade from 8 to 12 slot rack is only a +2, because a04 maxes out at 10/rack. We also subtract out the AO8 internal modules, since they can't share a rack.
                slot_diff = max(slot_diff, slot_diff_ao8)
                Trace.Write("slot_diff_ao8: {0}".format(slot_diff_ao8))
            Trace.Write("slot_diff: {0}".format(slot_diff))
            if slot_diff > 0:
                if attrs.ctrl_rack_pwr_sply == "Redundant":
                    #parts_dict['900R12R-0200'] = n_12_slot_r = slot_diff
                    parts_dict['900R12R-0300'] = n_12_slot_r = slot_diff
                    #parts_dict['900R08R-0200'] = n_8_slot_r = constraint_qty - slot_diff
                    parts_dict['900R08R-0300'] = n_8_slot_r = constraint_qty - slot_diff
                elif attrs.ctrl_rack_pwr_sply == "NonRedundant":
                    #parts_dict['900R12-0200'] = n_12_slot_nr = slot_diff
                    parts_dict['900R12-0300'] = n_12_slot_nr = slot_diff
                    #parts_dict['900R08-0200'] = n_8_slot_nr = constraint_qty - slot_diff
                    parts_dict['900R08-0300'] = n_8_slot_nr = constraint_qty - slot_diff
            if slot_diff <= 0: #Sometimes we need to downgrade to a 4-slot instead of upgrading to a 12-slot
                if attrs.ctrl_rack_pwr_sply == "Redundant": #There is no 4-slot redundant rack, so downgrading isn't possible
                    #parts_dict['900R12R-0200'] = 0
                    parts_dict['900R12R-0300'] = 0
                    #parts_dict['900R08R-0200'] = n_8_slot_r = constraint_qty
                    parts_dict['900R08R-0300'] = n_8_slot_r = constraint_qty
                    parts_dict['900R04R-0200'] = 0
                elif attrs.ctrl_rack_pwr_sply == "NonRedundant":
                    downgrade = 0
                    if slot_diff <= -1 and constraint_qty != d.Ceiling(n_ao8_int/5): #This is for AO4 and AO8 External modules. It determines when we could downgrade one of them to a 4-slot rack
                        downgrade = 1
                        if constraint_qty > 1 and (constraint_qty - d.Ceiling(n_ao8_ext/10))*5 - n_ao8_int > 0 and (constraint_qty - d.Ceiling(n_ao8_ext/10))*8 - n_ao8_int + 4 >= n_generic + n_ao4: #This is for AO8 Internal 
                            downgrade = 2
                    Trace.Write("Downgrade: {0}".format(downgrade))
                    #parts_dict['900R12-0200'] = 0
                    parts_dict['900R12-0300'] = 0
                    #parts_dict['900R08-0200'] = n_8_slot_nr = constraint_qty - downgrade
                    parts_dict['900R08-0300'] = n_8_slot_nr = constraint_qty - downgrade
                    #parts_dict['900R04-0200'] = n_4_slot = downgrade
                    parts_dict['900R04-0300'] = n_4_slot = downgrade
                    
    # CXCPQ-20373
    # qty calculation based on constraints outlined in CXCPQ-20370
    elif attrs.ctrl_rack_io_rack_type == "12Rack":
        qty = d.Ceiling(max((n_total_IO_mods / 12), (d.Ceiling(n_ao8_int / 5) + d.Ceiling(n_ao8_ext / 10)), (n_ao4 / 10)))
        if attrs.ctrl_rack_pwr_sply == "Redundant":
            #parts_dict['900R12R-0200'] = n_12_slot_r = qty
            parts_dict['900R12R-0300'] = n_12_slot_r = qty
        elif attrs.ctrl_rack_pwr_sply == "NonRedundant":
            #parts_dict['900R12-0200'] = n_12_slot_nr = qty
            parts_dict['900R12-0300'] = n_12_slot_nr = qty
    # CXCPQ-20372
    elif attrs.ctrl_rack_io_rack_type == "8Rack":
        qty = d.Ceiling(max((n_total_IO_mods / 8), (d.Ceiling(n_ao8_int / 5) + d.Ceiling(n_ao8_ext / 10)), (n_ao4 / 10)))
        if attrs.ctrl_rack_pwr_sply == "Redundant":
            #parts_dict['900R08R-0200'] = n_8_slot_r = qty
            parts_dict['900R08R-0300'] = n_8_slot_r = qty
        elif attrs.ctrl_rack_pwr_sply == "NonRedundant":
            #parts_dict['900R08-0200'] = n_8_slot_nr = qty
            parts_dict['900R08-0300'] = n_8_slot_nr = qty
    # CXCPQ-20371
    elif attrs.ctrl_rack_io_rack_type == "4Rack":
        qty = d.Ceiling(max(n_total_IO_mods / 4, d.Ceiling(n_ao8_int / 4) + d.Ceiling(n_ao8_ext / 4)    ))
        #parts_dict['900R04-0200'] = n_4_slot = qty
        parts_dict['900R04-0300'] = n_4_slot = qty

    # for CXCPQ-20338 - passing this to racks calc | Added by Ashok
    io_racks = {}
    io_racks["Redundant"] = n_8_slot_r + n_12_slot_r
    io_racks["NonRedundant"] = n_12_slot_nr + n_8_slot_nr + n_4_slot
    io_racks["Total"]  = float(n_12_slot_nr + n_12_slot_r + n_8_slot_nr + n_8_slot_r + n_4_slot)
    #===============================================================


    if (attrs.comm_q_io_fill_mod == "Yes"):
        #n_filler = float(((n_12_slot_nr * 12) + (n_12_slot_r * 12) + (n_8_slot_nr * 8) + (n_8_slot_r * 8) + (n_4_slot * 4)) - n_total_IO_mods)
        n_filler = float(((n_12_slot_nr * 12) + (n_12_slot_r * 12) + (n_8_slot_nr * 8) + (n_8_slot_r * 8) + (n_4_slot * 4)) - IO_mods['Total'])
        parts_dict["900TNF-0200"] = n_filler

    return parts_dict,io_racks