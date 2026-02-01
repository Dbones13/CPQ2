import System.Decimal as d

def calc_processor_modules(attrs, parts_dict, io_racks, IO_mods, Product):
    #Section to roll-up info from Remote Groups
    rg_io_mods = rg_analog_channels = rg_digital_channels = rg_ao_modules = rg_pfq_modules = rg_modbus_slaves = rg_modbus_masters = rg_opc_servers =rg_opc_clients = rg_cda_controllers = rg_io_racks = rg_comm_modules = point_sub_total = io_sub_total = num_pfqc = num_exp_ioracks_reduncontrl = NumofIO = cpm_3 = cpm_2 = 0.0

    if attrs.cg_or_rg == 'CG' and attrs.plc_or_uoc == 'PLC':
        remote_groups = Product.GetContainerByName('PLC_RemoteGroup_Cont').Rows
        for remote in remote_groups:
            rg_io_mods += float(remote.Product.Attr('PLC_RG_IO_Modules').GetValue())
            rg_analog_channels += float(remote.Product.Attr('PLC_RG_Analog_Channels').GetValue())
            rg_digital_channels += float(remote.Product.Attr('PLC_RG_Digital_Channels').GetValue())
            rg_ao_modules += float(remote.Product.Attr('PLC_RG_AO_Modules').GetValue())
            rg_pfq_modules += float(remote.Product.Attr('PLC_RG_PFQ_Modules').GetValue())
            rg_modbus_slaves += float(remote.Product.Attr('PLC_Modbus_Slaves').GetValue())
            rg_modbus_masters += float(remote.Product.Attr('PLC_Modbus_Master').GetValue())
            rg_opc_servers += float(remote.Product.Attr('PLC_OPC_Servers').GetValue())
            rg_opc_clients += float(remote.Product.Attr('PLC_OPC_Clients').GetValue())
            rg_cda_controllers += float(remote.Product.Attr('PLC_CDA_Controllers').GetValue())
            rg_io_racks += float(remote.Product.Attr('PLC_RG_IO_Racks').GetValue())
            rg_comm_modules += float(remote.Product.Attr('PLC_RG_Communications_Modules').GetValue())

    elif attrs.cg_or_rg == 'CG' and attrs.plc_or_uoc == 'UOC':
        remote_groups = Product.GetContainerByName('UOC_RemoteGroup_Cont').Rows
        for remote in remote_groups:
            try:
                rg_io_mods += float(remote.Product.Attr('UOC_RG_IO_Modules').GetValue())
                rg_analog_channels += float(remote.Product.Attr('UOC_RG_Analog_Channels').GetValue())
                rg_digital_channels += float(remote.Product.Attr('UOC_RG_Digital_Channels').GetValue())
                rg_ao_modules += float(remote.Product.Attr('UOC_RG_AO_Modules').GetValue())
                rg_io_racks += float(remote.Product.Attr('UOC_RG_IO_Racks').GetValue())
            except:
                pass

    #Calculating CPMs - Shared for both UOC & PLC
    num_iom = d.Ceiling((IO_mods['Total'] + rg_io_mods)/144)
                                       
    num_ac = d.Ceiling((parts_dict['900A01-0202'] + parts_dict['900A16-0103'] + parts_dict['900B01-0301'] + parts_dict['900B08-0202'] + rg_analog_channels)/2304)
                                     
    #num_dc = d.Ceiling((parts_dict['900G03-0202'] + parts_dict['900G32-0101'] + parts_dict['900G01-0202'] + parts_dict['900G04-0101'] + parts_dict['900H03-0202'] + parts_dict['900H32-0102'] + parts_dict['900H01-0202'] + rg_digital_channels)/4608)
    num_dc = d.Ceiling((parts_dict['900G03-0202'] + parts_dict['900G32-0301'] + parts_dict['900G01-0202'] + parts_dict['900G04-0101'] + parts_dict['900H03-0202'] + parts_dict['900H32-0302'] + parts_dict['900H01-0202'] + rg_digital_channels)/4608)
                                     
    num_ao = d.Ceiling((parts_dict['900B01-0301'] + parts_dict['900B08-0202'] + rg_ao_modules)/120)
                                     

    if attrs.plc_or_uoc == 'UOC': #For UOC no need below SKUs
        parts_dict['900ES1-0100'] = num_modbus_mc = num_modbus_sc = num_opc_sc = num_opc_cc = num_cda_cc = num_cim = IndiIOModUOC = UniIOModUOC = NumofIO = 0.00
        UniIOModUOC = attrs.nr_uio_ai_pts + attrs.nr_uio_ai_hart_pts + attrs.nr_uio_ao_100_250 + attrs.nr_uio_ao_250_499 + attrs.nr_uio_ao_500 + attrs.nr_uio_ao_hart_100_250 + attrs.nr_uio_ao_hart_250_499 + attrs.nr_uio_ao_hart_500 + attrs.nr_uio_di_pts + attrs.nr_uio_do_10_250 + attrs.nr_uio_do_250_500
        IndiIOModUOC = attrs.other_io_univ_ai8 + attrs.other_io_univ_ai8_tcrtdmvohm + attrs.other_io_ai16 + attrs.other_io_ao4 + attrs.other_io_ao8_intrnl + attrs.other_io_ao8_extrnl + attrs.other_io_di32 + attrs.other_io_di16_120240vac + attrs.other_io_di_cntct_type16 + attrs.other_io_di_16_125vdc + attrs.other_io_do32 + attrs.other_io_do8 + attrs.other_io_do_relay8 + attrs.other_io_pulseinput_freq4
        NumofIO = UniIOModUOC + IndiIOModUOC

    
    elif attrs.plc_or_uoc == 'PLC':
        num_modbus_mc = d.Ceiling((attrs.comm_intf_modbus_mstr + rg_modbus_masters)/32)
        num_modbus_sc = d.Ceiling((attrs.comm_intf_modbus_slvs + rg_modbus_slaves)/128)
        num_opc_sc = d.Ceiling((attrs.comm_intf_opc_srvrs + rg_opc_servers)/10)
        num_opc_cc = d.Ceiling((attrs.comm_intf_opc_clnts + rg_opc_clients)/10)
        num_cda_cc = d.Ceiling((attrs.comm_intf_cda_ctrlrs + rg_cda_controllers)/20)
        num_cim = d.Ceiling((parts_dict['900ES1-0100'] + rg_comm_modules)/6)

    if attrs.ctrl_rack_ctrl_type == 'Redundant':
        if attrs.plc_or_uoc == 'PLC':
            num_pfqc = d.Ceiling((parts_dict['900K01-0201'] + rg_pfq_modules)/48)
            num_exp_ioracks_reduncontrl = d.Ceiling((io_racks["Total"] + rg_io_racks)/12)
        if attrs.plc_or_uoc == 'UOC':
            num_exp_ioracks_reduncontrl = d.Ceiling((io_racks["Total"] + rg_io_racks) / 12)
            cpm_3 = d.Ceiling((parts_dict['900B01-0301'] + rg_ao_modules) / 12)
                                                                                
    elif attrs.ctrl_rack_ctrl_type == 'NonRedundant':
        if attrs.plc_or_uoc == 'PLC':
            num_pfqc = d.Ceiling((parts_dict['900K01-0201'] + rg_pfq_modules)/44)
            num_exp_ioracks_reduncontrl = d.Ceiling((io_racks["Total"] + rg_io_racks)/11)
        if attrs.plc_or_uoc == 'UOC':
            num_exp_ioracks_reduncontrl = d.Ceiling((io_racks["Total"] + rg_io_racks) / 13)
            cpm_3 = d.Ceiling((parts_dict['900B01-0301'] + rg_ao_modules) / 13)
                                                                                
    
    io_sub_total = max(num_iom,num_ac,num_dc,num_ao,num_pfqc,num_exp_ioracks_reduncontrl) #Comm Interfaces modules purposely excluded here
    point_sub_total = max(num_modbus_mc,num_modbus_sc,num_opc_sc,num_opc_cc,num_cda_cc)
    cpm_2 = d.Ceiling((NumofIO) / 2048 )
                                   
                                                 
                                   
                                   
    finalQty = max(io_sub_total, point_sub_total, num_cim)
    finalQty1 = max(io_sub_total,cpm_2,cpm_3)
    Trace.Write("io_sub_total: {0}, point_sub_total {1}, num_cim: {2}".format(io_sub_total, point_sub_total, num_cim))

    parts_dict['900CP1-0200'] = 0.00
    parts_dict['900CP1-0300'] = 0.00                                
    parts_dict['900CP2-0100'] = 0.00
    if attrs.ctrl_rack_ctrl_type == 'Redundant':
        #parts_dict['900CP1-0200'] += finalQty * 2
        #--start--CXCPQ-22214 Added by Ashok=-----
        if attrs.plc_or_uoc == 'PLC':
            if attrs.ctrl_operating_temp == '0 to 60 DegC or Marine application':
                parts_dict['900CP1-0200'] += finalQty * 2
                parts_dict["900RR0-0300"] = d.Ceiling(parts_dict['900CP1-0200'] / 2)
                parts_dict["900RNF-0200"] = d.Ceiling(parts_dict['900CP1-0200'] / 2)
           #parts_dict["900RR0-0200"] = d.Ceiling(parts_dict['900CP1-0200'] / 2)
           #parts_dict["900RNF-0200"] = d.Ceiling(parts_dict['900CP1-0200'] / 2)
            elif attrs.ctrl_operating_temp == 'Extended -40 to 70 DegC':
                parts_dict['900CP2-0100'] += finalQty * 2
                parts_dict["900RR0-0300"] = d.Ceiling(parts_dict['900CP2-0100'] / 2)
                parts_dict["900RNF-0200"] = d.Ceiling(parts_dict['900CP2-0100'] / 2)
            #parts_dict["900RR0-0300"] = d.Ceiling(parts_dict['900CP2-0100'] / 2)
            #parts_dict["900RNF-0200"] = d.Ceiling(parts_dict['900CP2-0100'] / 2)
        #--end------------------------
        if attrs.plc_or_uoc == 'UOC':
            #parts_dict['900CP1-0200'] += finalQty1 * 2
            if attrs.ctrl_operating_temp == '0 to 60 DegC or Marine application':
                                                     
                parts_dict['900CP1-0200'] += finalQty1 * 2
            elif attrs.ctrl_operating_temp == 'Extended -40 to 70 DegC':
                parts_dict['900CP1-0300'] += finalQty1 * 2
            #parts_dict['900CP2-0100'] += finalQty1 * 2
    elif attrs.ctrl_rack_ctrl_type == 'NonRedundant':
        if attrs.plc_or_uoc == 'PLC':
            #parts_dict['900CP1-0200'] += finalQty
            if attrs.ctrl_operating_temp == '0 to 60 DegC or Marine application':
                parts_dict['900CP1-0200'] += finalQty
            elif attrs.ctrl_operating_temp == 'Extended -40 to 70 DegC':
                parts_dict['900CP2-0100'] += finalQty
            #parts_dict['900CP2-0100'] += finalQty
        if attrs.plc_or_uoc == 'UOC':
            #parts_dict['900CP1-0200'] += finalQty1
             if attrs.ctrl_operating_temp == '0 to 60 DegC or Marine application':
                                                        
                parts_dict['900CP1-0200'] += finalQty1
             elif attrs.ctrl_operating_temp == 'Extended -40 to 70 DegC':
                parts_dict['900CP1-0300'] += finalQty1
            #parts_dict['900CP2-0100'] += finalQty1
    #Trace.Write(" parts_dict['900CP1-0200']:{0}".format( parts_dict['900CP2-0100']))
    #Adding IO racks to accomodate points that don't have IO modules. Also handles the scenario where Comm Interface Modules add more CPMs than racks available.
    extra_needed = 0
    if attrs.ctrl_rack_ctrl_type == 'NonRedundant' and attrs.cg_or_rg == 'CG':
        if num_cim == finalQty:
            extra_needed = num_cim - io_racks["Total"]
        else:
            extra_needed = point_sub_total - max(io_sub_total, num_cim)
        Trace.Write("extra_needed: {0}".format(extra_needed))
        #BFJ - The following line is changed, in case of a negative number - resulting in 1 less rack, resulting in 1 less EPM
        if extra_needed > 0:
            io_racks["Total"] += extra_needed
            if attrs.ctrl_rack_pwr_sply == 'NonRedundant':
                io_racks["NonRedundant"] += extra_needed
                if attrs.ctrl_rack_io_rack_type == 'OptimumRack' or attrs.ctrl_rack_io_rack_type == '4Rack':
                    rack_type = '04'
                elif attrs.ctrl_rack_io_rack_type == '8Rack':
                    rack_type = '08'
                elif attrs.ctrl_rack_io_rack_type == '12Rack':
                    rack_type = '12'   
            elif attrs.ctrl_rack_pwr_sply == 'Redundant':
                io_racks["Redundant"] += extra_needed
                if attrs.ctrl_rack_io_rack_type == 'OptimumRack' or attrs.ctrl_rack_io_rack_type == '8Rack': #4Rack is an impossible configuration here
                    rack_type = '08R'
                elif attrs.ctrl_rack_io_rack_type == '12Rack':
                    rack_type = '12R'
        
            rack_part_num = "900R{0}-0200".format(rack_type)
            try:
                parts_dict[rack_part_num] += extra_needed
            except:
                parts_dict[rack_part_num] = extra_needed

    #CX-CPQ20407
    parts_dict['900SP1-0200'] = 0.0
    parts_dict['900SP1-0300'] = 0.0
    if attrs.ctrl_rack_ctrl_type == "Redundant" :
        if attrs.ctrl_operating_temp == '0 to 60 DegC or Marine application':
            #parts_dict['900SP1-0200'] = io_racks["Total"] + rg_io_racks
            parts_dict['900SP1-0200'] = io_racks["Total"] + rg_io_racks
        elif attrs.ctrl_operating_temp == 'Extended -40 to 70 DegC':
            parts_dict['900SP1-0300'] = io_racks["Total"] + rg_io_racks
    elif attrs.ctrl_rack_ctrl_type == "NonRedundant":
        if attrs.ctrl_operating_temp == '0 to 60 DegC or Marine application':
            parts_dict['900SP1-0200'] = io_racks["Total"] + rg_io_racks - parts_dict['900CP1-0200']
            #parts_dict['900SP1-0300'] = io_racks["Total"] + rg_io_racks - parts_dict['900CP2-0100']
        elif attrs.ctrl_operating_temp == 'Extended -40 to 70 DegC':
            if attrs.plc_or_uoc == 'UOC':
                parts_dict['900SP1-0300'] = io_racks["Total"] + rg_io_racks - parts_dict['900CP1-0300']
            elif attrs.plc_or_uoc == 'PLC':
                parts_dict['900SP1-0300'] = io_racks["Total"] + rg_io_racks - parts_dict['900CP2-0100']   
    #CXCPQ-20375]
    try:
        #EPM = parts_dict['900SP1-0200']
        EPM = parts_dict['900SP1-0300']
    except:
        EPM = 0
        #parts_dict["51307946-001"] = EPM + parts_dict['900CP1-0200']
        if attrs.plc_or_uoc == 'UOC':
            parts_dict["51307946-001"] = EPM + parts_dict['900CP1-0300']
        elif attrs.plc_or_uoc == 'PLC':
            parts_dict["51307946-001"] = EPM + parts_dict['900CP2-0100']

    qty = 0
    n_12_slot = n_12_slot_r = n_8_slot = n_8_slot_r = n_4_slot = 0
    if attrs.plc_or_uoc == 'UOC':
        #Added by Abhijeet Shinde CCEECOMMBR-5446
        if (parts_dict['900CP1-0300'] != 0) :
            if (attrs.ctrl_rack_ctrl_type == 'Redundant'):
                #parts_dict['TC-SWCS90'] = (d.Ceiling(parts_dict['900CP1-0200']/2))
                parts_dict['TC-SWCS90'] = (d.Ceiling(parts_dict['900CP1-0300']/2))
            if (attrs.ctrl_rack_ctrl_type == 'NonRedundant'):
                #parts_dict['TC-SWCS90'] = parts_dict['900CP1-0200']
                parts_dict['TC-SWCS90'] = parts_dict['900CP1-0300']
        elif (parts_dict['900CP1-0200'] != 0) :
            if (attrs.ctrl_rack_ctrl_type == 'Redundant'):
                #parts_dict['TC-SWCS90'] = (d.Ceiling(parts_dict['900CP1-0200']/2))
                parts_dict['TC-SWCS90'] = (d.Ceiling(parts_dict['900CP1-0200']/2))
            if (attrs.ctrl_rack_ctrl_type == 'NonRedundant'):
                #parts_dict['TC-SWCS90'] = parts_dict['900CP1-0200']
                parts_dict['TC-SWCS90'] = parts_dict['900CP1-0200']
    #CXCPQ-21304 Added by Abhijeet
        if (attrs.ctrl_rack_ctrl_type == 'Redundant') and (attrs.ctrl_rack_phys_sep == 'Yes'):
#            if (attrs.ctrl_rack_phys_sep == 'Yes'):
            #parts_dict['900R01-0300'] =  parts_dict['900CP1-0200']
            if attrs.ctrl_operating_temp == '0 to 60 DegC or Marine application':
                parts_dict['900R01-0300'] =  parts_dict['900CP1-0200']
                parts_dict['900E01-0100'] =  parts_dict['900CP1-0200']
            elif attrs.ctrl_operating_temp == 'Extended -40 to 70 DegC':
                parts_dict['900R01-0300'] =  parts_dict['900CP1-0300']
                #parts_dict['900E01-0100'] =  parts_dict['900CP1-0200']
                parts_dict['900E01-0100'] =  parts_dict['900CP1-0300']
        elif (attrs.ctrl_rack_ctrl_type == 'Redundant') and (attrs.ctrl_rack_phys_sep != 'Yes'):
            #parts_dict['900RR0-0200'] = d.Ceiling(parts_dict['900CP1-0200'] / 2)
            if attrs.ctrl_operating_temp == '0 to 60 DegC or Marine application':
                parts_dict['900RR0-0300'] = d.Ceiling(parts_dict['900CP1-0200'] / 2)
                #parts_dict['900RNF-0200'] = d.Ceiling(parts_dict['900CP1-0200'] / 2)
                parts_dict['900RNF-0200'] = d.Ceiling(parts_dict['900CP1-0200'] / 2)
            elif attrs.ctrl_operating_temp == 'Extended -40 to 70 DegC':
                parts_dict['900RR0-0300'] = d.Ceiling(parts_dict['900CP1-0300'] / 2)
                #parts_dict['900RNF-0200'] = d.Ceiling(parts_dict['900CP1-0200'] / 2)
                parts_dict['900RNF-0200'] = d.Ceiling(parts_dict['900CP1-0300'] / 2)
            if attrs.comm_q_io_fill_mod == "Yes":
                #parts_dict['900RNF-0200'] = (d.Ceiling(parts_dict['900CP1-0200']/2))
                if attrs.ctrl_operating_temp == '0 to 60 DegC or Marine application':
                    parts_dict['900RNF-0200'] = (d.Ceiling(parts_dict['900CP1-0200']/2))
                elif attrs.ctrl_operating_temp == 'Extended -40 to 70 DegC':
                    parts_dict['900RNF-0200'] = (d.Ceiling(parts_dict['900CP1-0300']/2))
        if attrs.ctrl_rack_phys_sep == 'No' and attrs.ctrl_rack_ctrl_type == 'NonRedundant' and IO_mods['Total'] == 0 and attrs.cg_or_rg == 'CG':
            if attrs.ctrl_rack_io_rack_type == "4Rack":
                if attrs.ctrl_rack_pwr_sply == "NonRedundant":
                    if attrs.ctrl_operating_temp == '0 to 60 DegC or Marine application':
                        qty = parts_dict['900CP1-0200']
                        parts_dict['900R04-0300'] = n_4_slot = qty
                    if attrs.ctrl_operating_temp == 'Extended -40 to 70 DegC':
                        qty = parts_dict['900CP1-0300']
                        parts_dict['900R04-0300'] = n_4_slot = qty
            if attrs.ctrl_rack_io_rack_type == "8Rack":
                if attrs.ctrl_rack_pwr_sply == "Redundant":
                    if attrs.ctrl_operating_temp == '0 to 60 DegC or Marine application':
                        qty = parts_dict['900CP1-0200']
                        parts_dict['900R08R-0300'] = n_8_slot_r = qty
                    if attrs.ctrl_operating_temp == 'Extended -40 to 70 DegC':
                        qty = parts_dict['900CP1-0300']
                        parts_dict['900R08R-0300'] = n_8_slot_r = qty
                elif attrs.ctrl_rack_pwr_sply == "NonRedundant":
                    if attrs.ctrl_operating_temp == '0 to 60 DegC or Marine application':
                        qty = parts_dict['900CP1-0200']
                        parts_dict['900R08-0300'] = n_8_slot = qty
                    if attrs.ctrl_operating_temp == 'Extended -40 to 70 DegC':
                        qty = parts_dict['900CP1-0300']
                        parts_dict['900R08-0300'] = n_8_slot = qty
            if attrs.ctrl_rack_io_rack_type == "12Rack":
                if attrs.ctrl_rack_pwr_sply == "Redundant":
                    if attrs.ctrl_operating_temp == '0 to 60 DegC or Marine application':
                        qty = parts_dict['900CP1-0200']
                        parts_dict['900R12R-0300'] = n_12_slot_r = qty
                    if attrs.ctrl_operating_temp == 'Extended -40 to 70 DegC':
                        qty = parts_dict['900CP1-0300']
                        parts_dict['900R12R-0300'] = n_12_slot_r = qty
                elif attrs.ctrl_rack_pwr_sply == "NonRedundant":
                    if attrs.ctrl_operating_temp == '0 to 60 DegC or Marine application':
                        qty = parts_dict['900CP1-0200']
                        parts_dict['900R12-0300'] = n_12_slot = qty
                    if attrs.ctrl_operating_temp == 'Extended -40 to 70 DegC':
                        qty = parts_dict['900CP1-0300']
                        parts_dict['900R12-0300'] = n_12_slot = qty
            if attrs.ctrl_rack_io_rack_type == "OptimumRack":
                if attrs.ctrl_rack_pwr_sply == "Redundant":
                    if attrs.ctrl_operating_temp == '0 to 60 DegC or Marine application':
                        qty = parts_dict['900CP1-0200']
                        parts_dict['900R08R-0300'] = n_8_slot_r = qty
                    if attrs.ctrl_operating_temp == 'Extended -40 to 70 DegC':
                        qty = parts_dict['900CP1-0300']
                        parts_dict['900R08R-0300'] = n_8_slot_r = qty
                elif attrs.ctrl_rack_pwr_sply == "NonRedundant":
                    if attrs.ctrl_operating_temp == '0 to 60 DegC or Marine application':
                        qty = parts_dict['900CP1-0200']
                        parts_dict['900R04-0300'] = n_4_slot = qty
                    if attrs.ctrl_operating_temp == 'Extended -40 to 70 DegC':
                        qty = parts_dict['900CP1-0300']
                        parts_dict['900R04-0300'] = n_4_slot = qty
    io_racks["Redundant"] += n_8_slot_r + n_12_slot_r
    io_racks["NonRedundant"] += n_12_slot + n_8_slot + n_4_slot
    io_racks["Total"] += float(n_12_slot + n_12_slot_r + n_8_slot + n_8_slot_r + n_4_slot)
    return parts_dict, io_racks