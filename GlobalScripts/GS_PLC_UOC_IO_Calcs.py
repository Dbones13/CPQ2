import System.Decimal as d

def calc_io_modules(attrs, parts_dict):
	IO_mods = {}
   
	if attrs.plc_or_uoc == 'PLC':
		SF = attrs.plc_comm_q_io_spare
	else:
		SF = attrs.UOC_comm_q_io_spare

	#BFJ - JIRA CXCPQ-20344 - Calculate number of Universal Analog Input, RTD, TC, V, 8 Ch Modules
	io_uai_8 = d.Ceiling(((attrs.other_io_univ_ai8 + attrs.other_io_univ_ai8_tcrtdmvohm)*(1+SF))/8)
	parts_dict['900A01-0202'] = io_uai_8

	#BFJ - JIRA CXCPQ-20346 - Calculate number of Analog Input (16) I/O Modules
	ai_16 = d.Ceiling((attrs.other_io_ai16*(1+SF)) / 16)
	parts_dict['900A16-0103'] = ai_16

	#BFJ - JIRA CXCPQ-20347 - Calculate number of Analog Output (4) I/O Modules
	ao_0_20mA_4 = d.Ceiling((attrs.other_io_ao4*(1+SF))/4)
	parts_dict['900B01-0301'] = ao_0_20mA_4

	#BFJ - JIRA CXCPQ-20351 - Calculate number of Digital Input (32) 24VDC I/O Modules
	di_24vdc_32 = d.Ceiling((attrs.other_io_di32*(1+SF))/32)
	#parts_dict['900G32-0101'] = di_24vdc_32
	parts_dict['900G32-0301'] = di_24vdc_32

	#BFJ - JIRA CXCPQ-20353 - Calculate number of Digital Output (32) 24VDC I/O Modules
	do_24vdc_32 = d.Ceiling((attrs.other_io_do32*(1+SF))/32)
	#parts_dict['900H32-0102'] = do_24vdc_32
	parts_dict['900H32-0302'] = do_24vdc_32

	#BFJ - JIRA CXCPQ-20348 - Calculate number of Analog Output (8) I/O Modules (Internal) 
	ao_8_int = d.Ceiling((attrs.other_io_ao8_intrnl*(1+SF))/8)
	parts_dict['900B08-0202'] = ao_8_int

	#BFJ - JIRA CXCPQ-20348 - Calculate number of Analog Output (8) I/O Modules (External) 
	ao_8_ext = d.Ceiling((attrs.other_io_ao8_extrnl*(1+SF))/8)
	#  Add the value to the existing value in the same dictionary entry
	parts_dict['900B08-0202'] += ao_8_ext

	#BFJ - JIRA CXCPQ-20352 - Calculate number of Digital Output (8) 120/240 VAC Modules
	do_ac_8 = d.Ceiling((attrs.other_io_do8*(1+SF))/8)
	parts_dict['900H03-0202'] = do_ac_8

	#BFJ - JIRA CXCPQ-20349 - Calculate number of Digital Input (16) 120/240 VAC Modules
	di_ac_16 = d.Ceiling((attrs.other_io_di16_120240vac*(1+SF))/16)
	parts_dict['900G03-0202'] = di_ac_16

	#BFJ - JIRA CXCPQ-20350 - Calculate number of Digital Input Contact Type (16) Modules
	di_contact_16 = d.Ceiling((attrs.other_io_di_cntct_type16*(1+SF))/16)
	parts_dict['900G01-0202'] = di_contact_16

	#BFJ - JIRA CXCPQ-20354 - Calculate number of Digital Output Relay (8) Modules
	do_contact_8 = d.Ceiling((attrs.other_io_do_relay8*(1+SF))/8)
	parts_dict['900H01-0202'] = do_contact_8

	#BFJ - JIRA CXCPQ-20356 - Redundant UIO Modules - Calculate correct number of UIO modules
		#Channels are created from container values
	channel_ai_1 = attrs.r_uio_ai_pts + attrs.r_uio_ai_hart_pts
	channel_ao_100_1 = attrs.r_uio_ao_100_250 + attrs.r_uio_ao_hart_100_250
	channel_ao_250_1 = attrs.r_uio_ao_250_499 + attrs.r_uio_ao_hart_250_499
	channel_ao_500_1 = attrs.r_uio_ao_500 + attrs.r_uio_ao_hart_500
	channel_di_1 = attrs.r_uio_di_pts
	channel_do_250_1 = attrs.r_uio_do_10_250
	channel_do_500_1 = attrs.r_uio_do_250_500
		# Calculate Thermal Outputs of each type of IO Module
	TDI_1 = d.Ceiling(channel_di_1 * (1+SF)) * 0.01
	TD250_1 = d.Ceiling(channel_do_250_1 * (1+SF)) * 0.25
	TD500_1 = d.Ceiling(channel_do_500_1 * (1+SF)) * 0.5
	TAI_1 = d.Ceiling(channel_ai_1 * (1+SF)) * 0.0125
	TA100_1 = d.Ceiling(channel_ao_100_1 * (1+SF)) * 0.7
	TA250_1 = d.Ceiling(channel_ao_250_1 * (1+SF)) * 0.525
	TA500_1 = d.Ceiling(channel_ao_500_1 * (1+SF)) * 0.525
		# Create 2 scenarios
	uio_scenario_1_1 = 2 * d.Ceiling((TDI_1+TD250_1+TD500_1+TAI_1+TA100_1+TA250_1+TA500_1) / 4.2)
	uio_scenario_2_1 = 2 * d.Ceiling((channel_ai_1 + channel_ao_100_1 + channel_ao_250_1 + channel_ao_500_1 + channel_di_1 + channel_do_250_1 + channel_do_500_1) * (1+SF) / 14)
		# Take the greater value of the 2 scenarios
	uio_subtotal_1 = max(uio_scenario_1_1, uio_scenario_2_1)
	IO_mods['Redundant'] = uio_subtotal_1

	#BFJ - JIRA CXCPQ-20355 - Non-Redundant UIO Modules - Calculate correct number of UIO modules
		#Channels are created from variable values
	channel_ai_2 = attrs.nr_uio_ai_pts + attrs.nr_uio_ai_hart_pts
	channel_ao_100_2 = attrs.nr_uio_ao_100_250 + attrs.nr_uio_ao_hart_100_250
	channel_ao_250_2 = attrs.nr_uio_ao_250_499 + attrs.nr_uio_ao_hart_250_499
	channel_ao_500_2 = attrs.nr_uio_ao_500 + attrs.nr_uio_ao_hart_500
	channel_di_2 = attrs.nr_uio_di_pts
	channel_do_250_2 = attrs.nr_uio_do_10_250
	channel_do_500_2 = attrs.nr_uio_do_250_500
		# Calculate Thermal Outputs of each type of IO Module
	TDI_2 = d.Ceiling(channel_di_2 * (1+SF)) * 0.01
	TD250_2 = d.Ceiling(channel_do_250_2 * (1+SF)) * 0.25
	TD500_2 = d.Ceiling(channel_do_500_2 * (1+SF)) * 0.5
	TAI_2 = d.Ceiling(channel_ai_2 * (1+SF)) * 0.0125
	TA100_2 = d.Ceiling(channel_ao_100_2 * (1+SF)) * 0.7
	TA250_2 = d.Ceiling(channel_ao_250_2 * (1+SF)) * 0.525
	TA500_2 = d.Ceiling(channel_ao_500_2 * (1+SF)) * 0.33333
		# Create 2 scenarios
	uio_scenario_1_2 = d.Ceiling((TDI_2+TD250_2+TD500_2+TAI_2+TA100_2+TA250_2+TA500_2) / 4.2)
	uio_scenario_2_2 = d.Ceiling((channel_ai_2 + channel_ao_100_2 + channel_ao_250_2 + channel_ao_500_2 + channel_di_2 + channel_do_250_2 + channel_do_500_2) * (1+SF) / 16)
		# Take the greater value of the 2 scenarios
	uio_subtotal_2 = max(uio_scenario_1_2, uio_scenario_2_2)
	

	# Isolated Universal Non Redundant IO Points
	iso_uio_subtotal = 0
	if attrs.plc_or_uoc == 'UOC':
		isolated_ai = attrs.pf_io_ai_points + attrs.pf_io_ai_hart
		isolated_ao_100 = 0
		isolated_ao_250 = attrs.pf_io_ao_points + attrs.pf_io_ao_hart
		isolated_ao_500 = 0
		isolated_di = attrs.pf_io_di_cont
		isolated_do_250 = attrs.pf_io_do_points
		isolated_do_500 = 0

		# Calculate Thermal Outputs of each type of Isolated Universal Non Redundant IO Points
		TDI_3 = d.Ceiling(isolated_di * (1+SF)) * 0.01
		TD250_3 = d.Ceiling(isolated_do_250 * (1+SF)) * 0.25
		TD500_3 = d.Ceiling(isolated_do_500 * (1+SF)) * 0.5
		TAI_3 = d.Ceiling(isolated_ai * (1+SF)) * 0.0125
		TA100_3 = d.Ceiling(isolated_ao_100 * (1+SF)) * 0.7
		TA250_3 = d.Ceiling(isolated_ao_250 * (1+SF)) * 0.525
		TA500_3 = d.Ceiling(isolated_ao_500 * (1+SF)) * 0.33333
		
		# Create 2 scenarios
		iso_uio_scenario_1 = d.Ceiling((TDI_3+TD250_3+TD500_3+TAI_3+TA100_3+TA250_3+TA500_3) / 4.2)
		iso_uio_scenario_2 = d.Ceiling((isolated_ai + isolated_ao_100 + isolated_ao_250 + isolated_ao_500 + isolated_di + isolated_do_250 + isolated_do_500) * (1+SF) / 16)
		# Take the greater value of the 2 scenarios
		iso_uio_subtotal = max(iso_uio_scenario_1, iso_uio_scenario_2)
	# Add both Redundant and Non-Redundant UIO Qty's together for number of UIO Modules + Isolated Universal Non Redundant IO
	parts_dict['900U01-0100'] = uio_subtotal_1 + uio_subtotal_2 + iso_uio_subtotal

	IO_mods['Non-Redundant'] = uio_subtotal_2 + iso_uio_subtotal
	IO_mods['ISO-UIO-Total'] = iso_uio_subtotal

	#BFJ - JIRA CXCPQ-20408 - Calculate proper constraints put on Pulse/Frequency/ Quadrature (4 Channel) (Model number: 900K01-0201) so that system functions correctly.
	if attrs.plc_or_uoc =='PLC':
		PFQ = attrs.other_io_quad_inp
		# If number of PI/PO/FI channels are greater than Quad Channels, then add additional modules
		if (attrs.other_io_pulse_inp_freq_inp4 + attrs.other_io_pulse_outp4) > (attrs.other_io_quad_inp * 2):
			PFQ += d.Ceiling((attrs.other_io_pulse_inp_freq_inp4 + attrs.other_io_pulse_outp4)*(1+SF) / 4)
		parts_dict['900K01-0201'] = PFQ

		#BFJ - JIRA CXCPQ-20409 - Calculate number of Communication Interface Module RS485/RS232 IO Modules
		comm_interface_2_port_RS485_RS232 =  d.Ceiling(attrs.other_io_comm_intf_mod_485232) #CXCPQ-25308 - Paul - Removed spare factor 
		parts_dict['900ES1-0100'] = comm_interface_2_port_RS485_RS232

#CXCPQ-81811 - Kaousalya Adala
	if attrs.plc_or_uoc =='UOC':
		qty=0
		if attrs.exp_pks_software_release in ["R530","R520"]:
			if (attrs.other_io_pulseinput_freq4)>0:
				qty += d.Ceiling((attrs.other_io_pulseinput_freq4)*(1+SF) / 4)
				Trace.Write("Shiva")
				Trace.Write(qty)
			parts_dict['900K01-0201'] = qty
		elif attrs.exp_pks_software_release=="R511":
			parts_dict['900K01-0201'] = 0
			Trace.Write("Kumar")
	Trace.Write(parts_dict['900K01-0201'])        
	#BFJ - JIRA CXCPQ-21616 - Calculate number of Digital Input (16) 120/240 VAC (125VDC) IO Modules
	di_16_125vdc =  d.Ceiling((attrs.other_io_di_16_125vdc*(1+SF))/16)
	parts_dict['900G04-0101'] = di_16_125vdc
   
	if attrs.plc_or_uoc == 'PLC':
		IO_mods['Total'] = float(io_uai_8 + ai_16 + ao_0_20mA_4 + di_24vdc_32 + do_24vdc_32 + ao_8_int + ao_8_ext + do_ac_8 + di_ac_16 + di_contact_16 + do_contact_8 + uio_subtotal_1 + uio_subtotal_2 + PFQ + parts_dict['900K01-0201'] + comm_interface_2_port_RS485_RS232 + di_16_125vdc)
	elif attrs.plc_or_uoc == 'UOC':
		IO_mods['Total'] = float(io_uai_8 + ai_16 + ao_0_20mA_4 + di_24vdc_32 + do_24vdc_32 + ao_8_int + ao_8_ext + do_ac_8 + di_ac_16 + di_contact_16 + do_contact_8 + uio_subtotal_1 + uio_subtotal_2 + parts_dict['900K01-0201'] + di_16_125vdc + iso_uio_subtotal)
#    if attrs.plc_or_uoc == 'UOC':
#        #CXCPQ-21310 Added by Abhijeet
#        qty_cal = int((attrs.pf_io_ai_hart) + (attrs.pf_io_ao_hart) + (attrs.pf_io_di_cont) + (attrs.pf_io_di_namur) + (attrs.pf_io_do_max_load))
#        parts_dict['FC-GPCS-RIO16-PF'] = int(d.Ceiling(qty_cal/16))
#        parts_dict['HiC2441 ']=qty_cal
#        if attrs.pf_io_cab_len == "1M":
#            a="CAB-GEN-XX-S37F18-MX-01010".replace("XX","01")
#            parts_dict[a]=int(d.Ceiling(qty_cal/16))
#        elif attrs.pf_io_cab_len == "2M":
#            a="CAB-GEN-XX-S37F18-MX-01010".replace("XX","02")
#            parts_dict[a]=int(d.Ceiling(qty_cal/16))
#        elif attrs.pf_io_cab_len == "3M":
#            a="CAB-GEN-XX-S37F18-MX-01010".replace("XX","03")
#            parts_dict[a]=int(d.Ceiling(qty_cal/16))
#        elif attrs.pf_io_cab_len == "5M":
#            a="CAB-GEN-XX-S37F18-MX-01010".replace("XX","05")
#            parts_dict[a]=int(d.Ceiling(qty_cal/16))
#        elif attrs.pf_io_cab_len == "10M":
#            a="CAB-GEN-XX-S37F18-MX-01010".replace("XX","10")
#            parts_dict[a]=int(d.Ceiling(qty_cal/16))
#        elif attrs.pf_io_cab_len == "15M":
#            a="CAB-GEN-XX-S37F18-MX-01010".replace("XX","15")
#            parts_dict[a]=int(d.Ceiling(qty_cal/16))
#        elif attrs.pf_io_cab_len == "20M":
#            a="CAB-GEN-XX-S37F18-MX-01010".replace("XX","20")
#            parts_dict[a]=int(d.Ceiling(qty_cal/16))
#        elif attrs.pf_io_cab_len == "25M":
#            a="CAB-GEN-XX-S37F18-MX-01010".replace("XX","25")
#            parts_dict[a]=int(d.Ceiling(qty_cal/16))
#        elif attrs.pf_io_cab_len == "30M":
#            a="CAB-GEN-XX-S37F18-MX-01010".replace("XX","30")
#            parts_dict[a]=int(d.Ceiling(qty_cal/16))


	return parts_dict, IO_mods