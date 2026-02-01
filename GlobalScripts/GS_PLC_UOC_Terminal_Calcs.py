import System.Decimal as d

def calc_terminals(attrs, parts_dict, IO_mods): #Added by Ashok

    rts_sku_qty = tek_sku_qty = tbk_sku_qty = tck_sku_qty = ter_sku_qty = tbr_sku_qty = 0
    L2_sku_qty = C34_sku_qty = H2_sku_qty = 0

    #CXCPQ-21312, 21314
    if attrs.plc_or_uoc == 'UOC':#and attrs.cg_or_rg == 'CG':

        if parts_dict['900U01-0100']:

            #Non Redundant UIO
            channel_ai_2 = attrs.nr_uio_ai_pts + attrs.nr_uio_ai_hart_pts
            channel_ao_100_2 = attrs.nr_uio_ao_100_250 + attrs.nr_uio_ao_hart_100_250
            channel_ao_250_2 = attrs.nr_uio_ao_250_499 + attrs.nr_uio_ao_hart_250_499
            channel_ao_500_2 = attrs.nr_uio_ao_500 + attrs.nr_uio_ao_hart_500
            channel_di_2 = attrs.nr_uio_di_pts
            channel_do_250_2 = attrs.nr_uio_do_10_250
            channel_do_500_2 = attrs.nr_uio_do_250_500
            total_nr_uio = channel_ai_2 + channel_ao_100_2 + channel_ao_250_2 + channel_ao_500_2 + channel_di_2 + channel_do_250_2 + channel_do_500_2
            if IO_mods['Non-Redundant'] and total_nr_uio > 0:
                final_non_redundant = IO_mods['Non-Redundant'] - IO_mods['ISO-UIO-Total']
                if attrs.ctrl_rack_field_wire_other == "TerminalBlockEuro":
                    tek_sku_qty += final_non_redundant
                elif attrs.ctrl_rack_field_wire_other == "TerminalBlockBarrier":
                    tbk_sku_qty += final_non_redundant
                elif attrs.ctrl_rack_field_wire_other == "RemoteTerminalBlock":
                    rts_sku_qty += final_non_redundant #RTP
                    if attrs.cg_or_rg == 'CG':
                        if attrs.ctrl_rack_rem_term_pan_cab_type == 'HighVoltage':
                            H2_sku_qty += final_non_redundant
                        elif attrs.ctrl_rack_rem_term_pan_cab_type == "LowVoltage":
                            L2_sku_qty += final_non_redundant
                    else:
                        H2_sku_qty += final_non_redundant

            #CXCPQ-21314
            #Redundant UIO
            #if IO_mods['Redundant']:
            #    if attrs.ctrl_rack_field_wire_other == "RemoteTerminalBlock":
            #        parts_dict["900RTI-0100"] = IO_mods['Redundant']

            #        if attrs.ctrl_rack_rem_term_pan_cab_type == 'HighVoltage':
            #            H2_sku_qty += IO_mods['Redundant']
            #        elif attrs.ctrl_rack_rem_term_pan_cab_type == "LowVoltage":
            #            L2_sku_qty += IO_mods['Redundant']


    Trace.Write("900A01-0202"+ str(parts_dict["900A01-0202"]))
    Trace.Write("900G01-0202"+ str(parts_dict["900G01-0202"]))
    Trace.Write("900B08-0202"+ str(parts_dict["900B08-0202"]))
    #CXCPQ-20358 #Added by Ashok
    if parts_dict["900A01-0202"]:

        #900A01-0202 Question 3
        if attrs.ctrl_rack_field_wire_other == "TerminalBlockEuro":
            tek_sku_qty += parts_dict["900A01-0202"]
        elif attrs.ctrl_rack_field_wire_other == "TerminalBlockBarrier":
            tbk_sku_qty += parts_dict["900A01-0202"]
        elif attrs.ctrl_rack_field_wire_other == "RemoteTerminalBlock":
            parts_dict["900RTA-L001"] = parts_dict["900A01-0202"] #RTP Defect: CXCPQ-22842

            L2_sku_qty += parts_dict["900A01-0202"]

    #CXCPQ-20359 #Added by Ashok
    if parts_dict["900G32-0301"]:#part number cahnged to 900G32-0301 from 900G32-0101

        #900G32-0101 Question 1
        if attrs.ctrl_rack_field_wire_didoaoai == "TerminalBlockEuro":
            #tck_sku_qty += parts_dict["900G32-0101"]
            tck_sku_qty += parts_dict["900G32-0301"]
        elif attrs.ctrl_rack_field_wire_didoaoai == "RemoteTerminalBlock":
            #rts_sku_qty += 2 * parts_dict["900G32-0101"] #RTP defect: CXCPQ-22836
            rts_sku_qty += 2 * parts_dict["900G32-0301"] #RTP defect: CXCPQ-22836

            #C34_sku_qty += parts_dict["900G32-0101"]
            C34_sku_qty += parts_dict["900G32-0301"]

    #CXCPQ-20360 #Added by Ashok
    if parts_dict["900G03-0202"]:

        #900G03-0202 Question 3
        if attrs.ctrl_rack_field_wire_other == "TerminalBlockEuro":
            ter_sku_qty += parts_dict["900G03-0202"]
        elif attrs.ctrl_rack_field_wire_other == "TerminalBlockBarrier":
            tbr_sku_qty += parts_dict["900G03-0202"]
        elif attrs.ctrl_rack_field_wire_other == "RemoteTerminalBlock":
            rts_sku_qty += parts_dict["900G03-0202"] #RTP Defect: CXCPQ-22867

            H2_sku_qty += parts_dict["900G03-0202"]

    #CXCPQ-20361 #Added by Ashok
    if parts_dict["900H32-0302"]: #part number replaced by 900H32-0302

        #900H32-0102 Question 1
        if attrs.ctrl_rack_field_wire_didoaoai == "TerminalBlockEuro":
            #tck_sku_qty +=  parts_dict["900H32-0102"]
            tck_sku_qty +=  parts_dict["900H32-0302"]
        elif attrs.ctrl_rack_field_wire_didoaoai == "RemoteTerminalBlock":
            #rts_sku_qty += 2 * parts_dict["900H32-0102"] #RTP Defect: CXCPQ-22841
            rts_sku_qty += 2 * parts_dict["900H32-0302"] #RTP Defect: CXCPQ-22841

            #C34_sku_qty += parts_dict["900H32-0102"]
            C34_sku_qty += parts_dict["900H32-0302"]

    #CXCPQ-20362 #Added by Ashok
    if parts_dict["900H03-0202"]:

        #900H03-0202 Question 3
        if attrs.ctrl_rack_field_wire_other == "TerminalBlockEuro":
            ter_sku_qty += parts_dict["900H03-0202"]
        elif attrs.ctrl_rack_field_wire_other == "TerminalBlockBarrier":
            tbr_sku_qty += parts_dict["900H03-0202"]
        elif attrs.ctrl_rack_field_wire_other == "RemoteTerminalBlock":
            rts_sku_qty += parts_dict["900H03-0202"] #RTP Defect: CXCPQ-22867

            H2_sku_qty += parts_dict["900H03-0202"]

    #CXCPQ-20363 #Added by Ashok
    if parts_dict["900H01-0202"]:

        #900H01-0202 Question 3
        if attrs.ctrl_rack_field_wire_other == "TerminalBlockEuro":
            ter_sku_qty += parts_dict["900H01-0202"]
        elif attrs.ctrl_rack_field_wire_other == "TerminalBlockBarrier":
            tbr_sku_qty += parts_dict["900H01-0202"]
        elif attrs.ctrl_rack_field_wire_other == "RemoteTerminalBlock":
            parts_dict["900RTR-H001"] = parts_dict["900H01-0202"] #RTP Defect: CXCPQ-22838

            H2_sku_qty += parts_dict["900H01-0202"]

    #CXCPQ-20364 #Added by Ashok
    if parts_dict["900A16-0103"]:

        #900A16-0103 Question 1
        if attrs.ctrl_rack_field_wire_didoaoai == "TerminalBlockEuro":
            tck_sku_qty += parts_dict["900A16-0103"]
        elif attrs.ctrl_rack_field_wire_didoaoai == "RemoteTerminalBlock":
            rts_sku_qty += 2 * parts_dict["900A16-0103"] #RTP Defect: CXCPQ-22836

            C34_sku_qty += parts_dict["900A16-0103"]

    #CXCPQ-20365 #Added by Ashok
    if parts_dict["900B01-0301"]:

        #900B01-0301 Question 3
        if attrs.ctrl_rack_field_wire_other == "TerminalBlockEuro":
            tek_sku_qty += parts_dict["900B01-0301"]
        elif attrs.ctrl_rack_field_wire_other == "TerminalBlockBarrier":
            tbk_sku_qty += parts_dict["900B01-0301"]
        elif attrs.ctrl_rack_field_wire_other == "RemoteTerminalBlock":
            rts_sku_qty += parts_dict["900B01-0301"] #RTP Defect: CXCPQ-22837

            L2_sku_qty += parts_dict["900B01-0301"]

    #CXCPQ-20366 #Added by Ashok
    if parts_dict["900B08-0202"]:

        #900B08-0202 Question 1
        if attrs.ctrl_rack_field_wire_didoaoai == "TerminalBlockEuro":
            tck_sku_qty += parts_dict["900B08-0202"]
        elif attrs.ctrl_rack_field_wire_didoaoai == "RemoteTerminalBlock":
            rts_sku_qty += 2 * parts_dict["900B08-0202"] #RTP Defect: CXCPQ-22836

            if attrs.ctrl_rack_remote_term_cbl_len == "1M":
                parts_dict["900RTC-BA10"] = parts_dict["900B08-0202"]
            elif attrs.ctrl_rack_remote_term_cbl_len == "2.5M":
                parts_dict["900RTC-BA25"] = parts_dict["900B08-0202"]
            elif attrs.ctrl_rack_remote_term_cbl_len == "5M":
                parts_dict["900RTC-BA50"] = parts_dict["900B08-0202"]

    #CXCPQ-20367 #Added by Ashok
    if parts_dict["900G01-0202"]:

        #900G01-0202 Question 3
        if attrs.ctrl_rack_field_wire_other == "TerminalBlockEuro":
            tek_sku_qty += parts_dict["900G01-0202"]
        elif attrs.ctrl_rack_field_wire_other == "TerminalBlockBarrier":
            tbk_sku_qty += parts_dict["900G01-0202"]
        elif attrs.ctrl_rack_field_wire_other == "RemoteTerminalBlock":
            rts_sku_qty += parts_dict["900G01-0202"] #RTP By CXCPQ-22835

            L2_sku_qty += parts_dict["900G01-0202"]

    #CXCPQ-20368 #Added by Ashok
    if parts_dict["900G04-0101"]:

        #900G04-0101 Question 3
        if attrs.ctrl_rack_field_wire_other == "TerminalBlockEuro":
            tck_sku_qty += parts_dict["900G04-0101"]


    #CXCPQ-20418 Added by Ashok
    if attrs.plc_or_uoc == 'PLC':
        if parts_dict['900U01-0100']:

            nr_qty = r_qty = 0
            #Non Redundant UIO
            if IO_mods['Non-Redundant']:
                if attrs.ctrl_rack_field_wire_other == "TerminalBlockEuro":
                    tek_sku_qty += IO_mods['Non-Redundant']
                elif attrs.ctrl_rack_field_wire_other == "TerminalBlockBarrier":
                    tbk_sku_qty += IO_mods['Non-Redundant']
                elif attrs.ctrl_rack_field_wire_other == "RemoteTerminalBlock":
                    rts_sku_qty += IO_mods['Non-Redundant'] #RTP

                    nr_qty = IO_mods['Non-Redundant']

            #CXCPQ-20419 Added by Ashok
            #Redundant UIO
            if IO_mods['Redundant']:
                if attrs.ctrl_rack_field_wire_other == "RemoteTerminalBlock":
                    parts_dict["900RTI-0100"] = IO_mods['Redundant'] #RTP - no rounding is needed because these modules will always come in pairs (redundant).

                    r_qty = IO_mods['Redundant']

            if attrs.ctrl_rack_field_wire_other == "RemoteTerminalBlock":
                H2_sku_qty += nr_qty + r_qty

        #CXCPQ-20420 #Added by Ashok
        #900K01-0201
        if parts_dict["900K01-0201"]:

            if attrs.ctrl_rack_field_wire_PIFII == "TerminalBlockEuro":
                tek_sku_qty += parts_dict["900K01-0201"]
            elif attrs.ctrl_rack_field_wire_PIFII == "TerminalBlockBarrier":
                tbk_sku_qty += parts_dict["900K01-0201"]

    if rts_sku_qty != 0:
        parts_dict["900RTS-0001"] = rts_sku_qty

    if tek_sku_qty != 0:
        parts_dict["900TEK-0200"] = tek_sku_qty

    if tbk_sku_qty != 0:
        parts_dict["900TBK-0200"] = tbk_sku_qty

    if ter_sku_qty != 0:
        parts_dict["900TER-0200"] = ter_sku_qty

    if tbr_sku_qty != 0:
        parts_dict["900TBR-0200"] = tbr_sku_qty

    if tck_sku_qty != 0:
        parts_dict["900TCK-0200"] = tck_sku_qty

    #RTP Cables 
    #L210_sku_qty
    if L2_sku_qty != 0 and attrs.ctrl_rack_field_wire_other == "RemoteTerminalBlock":

        if attrs.ctrl_rack_remote_term_cbl_len == "1M":
            parts_dict["900RTC-L210"] = L2_sku_qty
        elif attrs.ctrl_rack_remote_term_cbl_len == "2.5M":
            parts_dict["900RTC-L225"] = L2_sku_qty
        elif attrs.ctrl_rack_remote_term_cbl_len == "5M":
            parts_dict["900RTC-L250"] = L2_sku_qty

    if C34_sku_qty != 0 and attrs.ctrl_rack_field_wire_didoaoai == "RemoteTerminalBlock":

        if attrs.ctrl_rack_remote_term_cbl_len == "1M":
            parts_dict["900RTC-3410"] = C34_sku_qty
        elif attrs.ctrl_rack_remote_term_cbl_len == "2.5M":
            parts_dict["900RTC-3425"] = C34_sku_qty
        elif attrs.ctrl_rack_remote_term_cbl_len == "5M":
            parts_dict["900RTC-3450"] = C34_sku_qty

    if H2_sku_qty != 0 and attrs.ctrl_rack_field_wire_other == "RemoteTerminalBlock":

        if attrs.ctrl_rack_remote_term_cbl_len == "1M":
            parts_dict["900RTC-H210"] = H2_sku_qty
        elif attrs.ctrl_rack_remote_term_cbl_len == "2.5M":
            parts_dict["900RTC-H225"] = H2_sku_qty
        elif attrs.ctrl_rack_remote_term_cbl_len == "5M":
            parts_dict["900RTC-H250"] = H2_sku_qty


    return parts_dict