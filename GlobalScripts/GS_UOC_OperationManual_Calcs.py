def GS_UOC_OperationManual_Calcs(attrs):
	sys = int(attrs.sys)
	mar = int (attrs.marshalling_cabinets)
	isi = 1 if int(attrs.is_ios) > 0 else 0 #'is' replaced with 'isi'
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
		Hrs = 20
	elif io > 400 and io<=2000:
		Hrs = 30
	elif io>2000 and io<= 5000:
		Hrs = 40
	elif io> 5000:
		Hrs = 100

	return Hrs
