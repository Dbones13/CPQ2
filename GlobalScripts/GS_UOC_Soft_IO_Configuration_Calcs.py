def GS_UOC_Soft_IO_Configuration_Calcs(attrs):
	if attrs.scada_node_type == '':
		sNode = 0
	else:
		sNode = int(attrs.scada_node_type)
	#Trace.Write(str(type(sNode)))
	pcdi = int(attrs.peer_pcdi)
	cda = int(attrs.peer_cda)
	Tpty = int(attrs.Thirdparty_Serial_Scada)
	if attrs.peer_to_peer_io == '':
		ptp = 0
	else:
		ptp = int(attrs.peer_to_peer_io)
	#ptp = int(attrs.peer_to_peer_io)
	sio = pcdi + cda + ptp + Tpty
	Sbase = 0
	if sio > 0 and sio <= 400:
		Sbase = 8
	elif sio > 400 and sio<=2000:
		Sbase = 16
	elif sio > 2000 and sio <= 5000:
		Sbase = 24
	elif sio > 5000:
		Sbase = int(attrs.mSIOConf)
	SIC_Hrs = 1.1 * (Sbase + 5 * sNode + 0.1 * Tpty + 0.05*cda + 0.15*(pcdi + ptp))
	Hrs = SIC_Hrs
	#Trace.Write("Sbase:{0},sNode:{1},pcdi:{2},cda:{3},ptp:{4}".format(Sbase,sNode,pcdi,cda,ptp))
	return round(Hrs, 2)
