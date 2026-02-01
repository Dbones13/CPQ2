def GS_UOC_Control_Application_Configuration_Calcs(attrs):
	ai = int(attrs.AI)
	ao = int(attrs.AO)
	do = int(attrs.DO)
	di = int(attrs.DI)
	proNIO  = int(attrs.profitnet_IO)
	eIPIO   = int(attrs.ethernet_IO)
	pcdi = int(attrs.peer_pcdi)
	cda = int(attrs.peer_cda)
	sNode = int(attrs.scada_node_type)
	ptp = int(attrs.peer_to_peer_io)
	Tpty = int(attrs.Thirdparty_Serial_Scada)
	wio = ai + ao + do + di
	hio = wio + proNIO + eIPIO
	sio = pcdi + cda + ptp + Tpty
	io = hio + sio + sNode
	if io <= 400:
		base = 24
	elif io > 400 and io <= 2000:
		base = 32
	elif io >2000 and io <= 5000:
		base = 40
	elif io > 5000:
		base = int(attrs.mConf)
	#Refer to CCEECOMMBR-5535
	#Sbase = 0
	#if sio > 0 and sio <= 400:
	#    Sbase = 8
	#elif sio > 400 and sio<=2000:
	#    Sbase = 16
	#elif sio > 2000 and sio <= 5000:
	#    Sbase = 24
	#elif sio > 5000:
	#    Sbase = 48
	ctr = attrs.ctr
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
	odd = float( do /1.2)
	odi = float((di - (odd*1.5))/1.5)
	'''constant value'''
	scm = 15
	CLC_Hrs = (base + 5 * ctr + pT * (0.15 * (wio + sio) + 0.65 * (ai - ao) + 0.65 * (ao) + 0.25 * (do / 1.2) + (1 + 0.1 * bat) * scm))
	#Refer to CCEECOMMBR-5535
	#SIC_Hrs = (Sbase + 0.05 * cda + 0.15 * pcdi) * 1.1
	#Trace.Write("SIC_Hrs:{0}".format(SIC_Hrs))
	#GES = attrs.ges_location.strip()
	#if GES == 'None' or GES == '':
	#    SIC_Hrs = Sbase + 0.05 * cda + 0.15 * pcdi
	#Trace.Write("SIC_Hrs:{0},CLC_Hrs:{1}".format(SIC_Hrs,CLC_Hrs))
	#Hrs = CLC_Hrs + SIC_Hrs
	Hrs = CLC_Hrs
	Trace.Write("base:{0},ctr:{1},pT:{2},ai:{3},ao:{4},di:{5},do:{6},odd:{7},odi:{8},bat:{9},Hrs:{10}".format(base,ctr,pT,ai,ao,di,do,odd,odi,bat,Hrs))
	return round(Hrs, 2)