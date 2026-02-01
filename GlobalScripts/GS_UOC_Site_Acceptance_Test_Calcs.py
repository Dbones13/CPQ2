def GS_UOC_Site_Acceptance_Test_Calcs(attrs):
	sys = attrs.sys
	mar = int(attrs.marshalling_cabinets)
	is_ios = 1 if attrs.is_ios > 0 else 0
	HW_SAT = 0.17 * 0.3 * (sys * 40 * 0.5 + mar *(40 +is_ios *10))
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
	if io <= 400:
		SW_SAT = 40
	elif io > 400 and io <= 2000:
		SW_SAT = 60
	elif io > 2000 and io <= 5000:
		SW_SAT = 120
	elif io > 5000:
		SW_SAT = int(attrs.mSAT)
	Hrs = HW_SAT + SW_SAT
	return Hrs
