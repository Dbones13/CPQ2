def calc_auxilary(attrs, parts_dict):#Added by Sumanth and Abhijeet
    #CXCPQ-20376
    if attrs.cg_or_rg == 'CG':
        qty_io_module_insert=attrs.addl_ctrlr_io_mod_label_kit
        parts_dict['514522622-503']=int(qty_io_module_insert)*1

        #CXCPQ-20379
        qty_two_pos_terminal_board_jumpers = attrs.addl_ctrlr_2_pos_term_brd_jmprs
        parts_dict['900J02-0001']=int(qty_two_pos_terminal_board_jumpers)
        #CXCPQ-20380
        qty_ten_pos_terminal_board_jumpers=attrs.addl_ctrlr_10_pos_term_brd_jmprs
        parts_dict['900J10-0001']=int(qty_ten_pos_terminal_board_jumpers)
        #CXCPQ-20381
        qty_mi_mp_250_Ohm_resistor_Kit_of_8=attrs.addl_ctrlr_mimp_250ohm_resis_kit
        parts_dict['51205995-501']=int(qty_mi_mp_250_Ohm_resistor_Kit_of_8)*1

    #CXCPQ-20378
    if attrs.comm_q_shielded_term_setup =='Yes':
        if attrs.ctrl_rack_io_rack_type =='4Rack':
            #parts_dict['900TSS-0001'] = 1*parts_dict['900R04-0200']
            parts_dict['900TSS-0001'] = 1*parts_dict['900R04-0300']
        elif attrs.ctrl_rack_io_rack_type =='8Rack':
            if attrs.ctrl_rack_pwr_sply == "Redundant":
                #parts_dict['900TSS-0001'] = 2*parts_dict['900R08R-0200']
                parts_dict['900TSS-0001'] = 2*parts_dict['900R08R-0300']
            else:
                #parts_dict['900TSS-0001'] = 2*parts_dict['900R08-0200']
                parts_dict['900TSS-0001'] = 2*parts_dict['900R08-0300']
        elif attrs.ctrl_rack_io_rack_type =='12Rack':
            if attrs.ctrl_rack_pwr_sply == "Redundant":
                #parts_dict['900TSS-0001'] = 3*parts_dict['900R12R-0200']
                parts_dict['900TSS-0001'] = 3*parts_dict['900R12R-0300']
            else:
                #parts_dict['900TSS-0001'] = 3*parts_dict['900R12-0200']
                parts_dict['900TSS-0001'] = 3*parts_dict['900R12-0300']
        elif attrs.ctrl_rack_io_rack_type == 'OptimumRack':
            try:
                #R08R = parts_dict['900R08R-0200']
                R08R = parts_dict['900R08R-0300']
            except:
                R08R = 0.00
            if '900R04-0300' in parts_dict:
                #parts_dict['900TSS-0001'] = ((1*parts_dict['900R04-0200'])+(3*parts_dict['900R12-0200']))
                parts_dict['900TSS-0001'] = ((1*parts_dict['900R04-0300'])+(3*parts_dict['900R12-0300']))
            elif '900R08R-0300' in parts_dict:
                #parts_dict['900TSS-0001'] = ((2*parts_dict['900R08R-0200'])+(3*parts_dict['900R12R-0200']))
                parts_dict['900TSS-0001'] = ((2*parts_dict['900R08R-0300'])+(3*parts_dict['900R12R-0300']))
            elif '900R08-0300' in parts_dict:
                #parts_dict['900TSS-0001'] = ((2*parts_dict['900R08-0200'])+(3*parts_dict['900R12-0200']))
                parts_dict['900TSS-0001'] = ((2*parts_dict['900R08-0300'])+(3*parts_dict['900R12-0300']))
            elif '900R12R-0300' in parts_dict:
                #parts_dict['900TSS-0001'] = ((2* R08R)+(3*parts_dict['900R12R-0200']))
                parts_dict['900TSS-0001'] = ((2* R08R)+(3*parts_dict['900R12R-0300']))
            elif '900R12-0300' in parts_dict:
                #parts_dict['900TSS-0001'] = ((3*parts_dict['900R12-0200']))
                parts_dict['900TSS-0001'] = ((3*parts_dict['900R12-0300']))

    return parts_dict