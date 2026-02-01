def GS_UOC_Factory_Acceptance_Test_Calcs(attrs):
	fat = float(attrs.perc_fat)
	bmu = int(attrs.batch_unit)
	bru = int(attrs.batch_unit_copies)
	F = 9.412 if attrs.process_type in ['Batch - Pharma', 'BatchPharma'] else 6.052
	scm = 15
	bcscm = int(attrs.complex_scms)
	bmr = int(attrs.product_master_recipes)
	bpr = int(attrs.product_replicated)
	bco = int(attrs.complex_ops)
	#BFAT = (fat/100) * ((bmu + bru) * (F * 5 + 26.212 * bcscm + 6.4) + (bmr + bpr) * (4.66 * 5 + 11.55 * bco + 8.9))
	BFAT = (fat/100) * ((bmu + bru) * (F * 5 + 26.212 * bcscm + 6.4)+(bmr + bpr)*(4.66 * 5 + 11.55 * bco + 8.9))
	sys = attrs.sys
	mar = int(attrs.marshalling_cabinets)
	is_ios = 1 if attrs.is_ios > 0 else 0
	uio = 1 if int(attrs.uio) > 0 else 0
	ai = int(attrs.AI)
	ao = int(attrs.AO)
	do = int(attrs.DO)
	di = int(attrs.DI)
	proNIO  = int(attrs.profitnet_IO)
	eIPIO   = int(attrs.ethernet_IO)
	pcdi = int(attrs.peer_pcdi)
	cda = int(attrs.peer_cda)
	Tpty = int(attrs.Thirdparty_Serial_Scada)
	if attrs.peer_to_peer_io == '':
		ptp = 0
	else:
		ptp = int(attrs.peer_to_peer_io)
	wio = ai + ao + do + di
	hio = wio + proNIO + eIPIO
	sio = pcdi + cda + ptp + Tpty
	io = hio + sio
	if io<= 400:
		base = 16
	elif io > 400 and io<=2000:
		base = 32
	elif io>2000 and io<= 5000:
		base = 64
	elif io> 5000:
		base = int(attrs.mFAT)
	ctr = attrs.ctr
	nty = int(attrs.new_typicals)
	pT = 0
	if attrs.process_type == 'Continuous':
		pT = 1
	elif attrs.process_type in ['Continuous + Interlock', 'ContinuousInterlock']:
		pT = 1.2
	elif attrs.process_type in ['Continuous + Sequence', 'ContinuousSequence']:
		pT = 1.5
	elif attrs.process_type in ['Continuous + Interlock + Sequence', 'ContinuousInterlockSequence']:
		pT = 1.8
	elif attrs.process_type in ['Batch - Pharma', 'BatchPharma', 'Batch - Chemical','BatchChemical']:
		pT = 2
	bat = 1 if pT == 2 else 0
	HW_FAT = (1 - uio * 0.1) * 0.1 *(sys * 40 * 0.5 + mar * (40 + is_ios * 10))
	SW_FAT = 0.97 * (base + 0.66 * ctr + ( 4 * nty + 0.029 * io * fat / 100) * pT + scm * 0.11)
	Hrs = HW_FAT + SW_FAT * 0.97 + bat * BFAT
	im  = attrs.implementation_method
	if im in ["Non Standard Build Estimate", "NonStandardBuildEstimate"]:
		Hrs = HW_FAT + SW_FAT + bat * BFAT
	return round(Hrs,2)