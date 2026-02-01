import System.Decimal as d

def calc_network(attrs, parts_dict, io_racks, Product=None):


# PLC SECTION
        #CXCPQ-20421 Added by Sumanth and Abhijeet
        #qty_fiber_optic_converter_single_G3 = attrs.addl_ctrlr_fib_opt_conv_single_g3
        #parts_dict['50135395-004']=int(qty_fiber_optic_converter_single_G3)*1
        # TDH - CXCPQ-20422
    if attrs.ctrl_rack_ether_swtch_splyr == 'Honeywell': 
        if attrs.plc_or_uoc =='PLC':
            if attrs.addl_ctrlr_fib_opt_conv_multi_g3 != "" and int(attrs.addl_ctrlr_fib_opt_conv_multi_g3) != 0:
                parts_dict['50135395-003'] = int(attrs.addl_ctrlr_fib_opt_conv_multi_g3)

            #CXCPQ-20384 Added by Ashok
            if attrs.ctrl_rack_ether_swtch_type == 'MultiMode':
                if attrs.ctrl_rack_g3_opt_ether_swtch == 'No' and int(attrs.addl_ctrlr_fib_opt_conv_multi) > 0:
                    parts_dict['50135395-001'] = 1 * int(attrs.addl_ctrlr_fib_opt_conv_multi)
            #CXCPQ-20385 Added by Ashok
            if attrs.ctrl_rack_ether_swtch_type == 'SingleMode' and int(attrs.addl_ctrlr_fib_opt_conv_single) > 0:
                parts_dict['50135395-002'] = 1 *int(attrs.addl_ctrlr_fib_opt_conv_single) 

            #BFJ - CXCPQ-20383 & CXCPQ-20410
            #  Formula to determine rack quantity for formulations
            rg_io_racks = 0
            if attrs.cg_or_rg == 'CG':
                remote_groups = Product.GetContainerByName('PLC_RemoteGroup_Cont').Rows
                for remote in remote_groups:
                    rg_io_racks += float(remote.Product.Attr('PLC_RG_IO_Racks').GetValue())
            full_racks = d.Floor((float(io_racks["Total"]) + rg_io_racks) / 12)
            partial_rack = (io_racks["Total"] + rg_io_racks) % 12
            Trace.Write("Racks: {0} {1} {2}".format(io_racks["Total"],full_racks,partial_rack))

        #BFJ - CXCPQ-20383
        #Determine how many non-G3 ethernet switches, of which types, are needed 
        if attrs.plc_or_uoc == 'PLC':
            if attrs.ctrl_rack_g3_opt_ether_swtch == 'No':
                if attrs.ctrl_rack_ctrl_type == 'NonRedundant':
                    if attrs.ctrl_rack_network_topo == 'RedundantStar':
                        if attrs.ctrl_rack_ether_swtch_type == 'MultiMode':
                            if (2 <= partial_rack <= 5):
                                parts_dict['50008930-001'] = 2
                            elif (6 <= partial_rack <= 12):
                                full_racks = full_racks + 1
                            parts_dict['50008930-002'] = full_racks * 2
                        elif attrs.ctrl_rack_ether_swtch_type == 'SingleMode':
                            if (2 <= partial_rack <= 5):
                               parts_dict['50008930-004'] = 2
                            elif (6 <= partial_rack <= 12):
                                full_racks = full_racks + 1
                            parts_dict['50008930-003'] = full_racks * 2
                    elif attrs.ctrl_rack_network_topo == 'NonRedundantStar':
                        if attrs.ctrl_rack_ether_swtch_type == 'MultiMode':
                            if (2 <= partial_rack <= 5):
                                parts_dict['50008930-001'] = 1
                            elif (6 <= partial_rack <= 12):
                                full_racks = full_racks + 1
                            parts_dict['50008930-002'] = full_racks
                        elif attrs.ctrl_rack_ether_swtch_type == 'SingleMode':
                            if (2 <= partial_rack <= 5):
                                parts_dict['50008930-004'] = 1
                            elif (6 <= partial_rack <= 12):
                                full_racks = full_racks + 1
                            parts_dict['50008930-003'] = full_racks
                elif attrs.ctrl_rack_ctrl_type == 'Redundant':
                    if attrs.ctrl_rack_network_topo == 'RedundantStar':
                        if attrs.ctrl_rack_ether_swtch_type == 'MultiMode':
                            if (1 <= partial_rack <= 4):
                                parts_dict['50008930-001'] = 2
                            elif (5 <= partial_rack <= 12):
                               full_racks = full_racks + 1
                            parts_dict['50008930-002'] = full_racks * 2
                        elif attrs.ctrl_rack_ether_swtch_type == 'SingleMode':
                            if (1 <= partial_rack <= 4):
                                parts_dict['50008930-004'] = 2
                            elif (5 <= partial_rack <= 12):
                                full_racks = full_racks + 1
                            parts_dict['50008930-003'] = full_racks * 2
                    elif attrs.ctrl_rack_network_topo == 'NonRedundantStar':
                        if attrs.ctrl_rack_ether_swtch_type == 'MultiMode':
                            if (1 <= partial_rack <= 4):
                                parts_dict['50008930-001'] = 1
                            elif (5 <= partial_rack <= 12):
                                full_racks = full_racks + 1
                            parts_dict['50008930-002'] = full_racks
                        elif attrs.ctrl_rack_ether_swtch_type == 'SingleMode':
                            if (1 <= partial_rack <= 4):
                                parts_dict['50008930-004'] = 1
                            elif (5 <= partial_rack <= 12):
                                full_racks = full_racks + 1
                            parts_dict['50008930-003'] = full_racks
                #BFJ - CXCPQ-20410 - Determine how many G3 ethernet switches are needed, if applicable
                elif attrs.ctrl_rack_g3_opt_ether_swtch == 'Yes':
                    if (1 <= partial_rack <= 11):
                        full_racks = full_racks + 1
                    parts_dict['50008930-008'] = full_racks
                    #parts_dict['50135395-003'] += full_racks #CXCPQ-23592 removed because of ticket number 23592
    
# UOC SECTION     
        if attrs.plc_or_uoc =='UOC':
            #CXCPQ-20384 Added by Ashok
            if attrs.ctrl_rack_ether_swtch_type == 'MultiMode':
                if int(attrs.addl_ctrlr_fib_opt_conv_multi) > 0:
                    parts_dict['50135395-001'] = 1 * int(attrs.addl_ctrlr_fib_opt_conv_multi)
            #CXCPQ-20385 Added by Ashok
            if attrs.ctrl_rack_ether_swtch_type == 'SingleMode' and int(attrs.addl_ctrlr_fib_opt_conv_single) > 0:
                parts_dict['50135395-002'] = 1 *int(attrs.addl_ctrlr_fib_opt_conv_single) 

            #BFJ - CXCPQ-20383 & CXCPQ-20410
            #  Formula to determine rack quantity for formulations
            rg_io_racks = 0
            #if attrs.cg_or_rg == 'CG':
                #remote_groups = Product.GetContainerByName('UOC_RemoteGroup_Cont').Rows
                #for remote in remote_groups:
                    #rg_io_racks += float(remote.Product.Attr('UOC_RG_IO_Racks').GetValue())
            full_racks = d.Floor((float(io_racks["Total"]) + rg_io_racks) / 12)
            partial_rack = (io_racks["Total"] + rg_io_racks) % 12
            Trace.Write("Racks: {0} {1} {2}".format(io_racks["Total"],full_racks,partial_rack))

        #BFJ - CXCPQ-20383
        #Determine how many non-G3 ethernet switches, of which types, are needed 
        if attrs.plc_or_uoc == 'UOC':
            if attrs.ctrl_rack_ctrl_type == 'NonRedundant':
                if attrs.ctrl_rack_network_topo == 'RedundantStar' or attrs.ctrl_rack_network_topo == 'RedundantStarPRP':
                    if attrs.ctrl_rack_ether_swtch_type == 'MultiMode':
                        if (2 <= partial_rack <= 5):
                            parts_dict['50008930-001'] = 2
                        elif (6 <= partial_rack <= 12):
                            full_racks = full_racks + 1
                        parts_dict['50008930-002'] = full_racks * 2
                    elif attrs.ctrl_rack_ether_swtch_type == 'SingleMode':
                        if (2 <= partial_rack <= 5):
                           parts_dict['50008930-004'] = 2
                        elif (6 <= partial_rack <= 12):
                            full_racks = full_racks + 1
                        parts_dict['50008930-003'] = full_racks * 2
                elif attrs.ctrl_rack_network_topo == 'NonRedundantStar':
                    if attrs.ctrl_rack_ether_swtch_type == 'MultiMode':
                        if (2 <= partial_rack <= 5):
                            parts_dict['50008930-001'] = 1
                        elif (6 <= partial_rack <= 12):
                            full_racks = full_racks + 1
                        parts_dict['50008930-002'] = full_racks
                    elif attrs.ctrl_rack_ether_swtch_type == 'SingleMode':
                        if (2 <= partial_rack <= 5):
                            parts_dict['50008930-004'] = 1
                        elif (6 <= partial_rack <= 12):
                            full_racks = full_racks + 1
                        parts_dict['50008930-003'] = full_racks
            elif attrs.ctrl_rack_ctrl_type == 'Redundant':
                if attrs.ctrl_rack_network_topo == 'RedundantStarPRP' or attrs.ctrl_rack_network_topo == 'RedundantStar':
                    if attrs.ctrl_rack_ether_swtch_type == 'MultiMode':
                        if (1 <= partial_rack <= 4):
                            parts_dict['50008930-001'] = 2
                        elif (5 <= partial_rack <= 12):
                            full_racks = full_racks + 1
                        parts_dict['50008930-002'] = full_racks * 2
                    elif attrs.ctrl_rack_ether_swtch_type == 'SingleMode':
                        if (1 <= partial_rack <= 4):
                            parts_dict['50008930-004'] = 2
                        elif (5 <= partial_rack <= 12):
                            full_racks = full_racks + 1
                        parts_dict['50008930-003'] = full_racks * 2
                elif attrs.ctrl_rack_network_topo == 'NonRedundantStar':
                    if attrs.ctrl_rack_ether_swtch_type == 'MultiMode':
                        if (1 <= partial_rack <= 4):
                            parts_dict['50008930-001'] = 1
                        elif (5 <= partial_rack <= 12):
                            full_racks = full_racks + 1
                        parts_dict['50008930-002'] = full_racks
                    elif attrs.ctrl_rack_ether_swtch_type == 'SingleMode':
                        if (1 <= partial_rack <= 4):
                            parts_dict['50008930-004'] = 1
                        elif (5 <= partial_rack <= 12):
                            full_racks = full_racks + 1
                        parts_dict['50008930-003'] = full_racks

    else:
        parts_dict['50008930-001'] = 0

    return parts_dict