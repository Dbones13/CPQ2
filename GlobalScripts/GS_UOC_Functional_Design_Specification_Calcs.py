def GS_UOC_Functional_Design_Specification_Calcs(attrs):
	proT = 1 if attrs.project_type == 'Expansion' else 0
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
		pT = 2.0
	bat = 1 if pT == 2 else 0
	unP = 1 if attrs.unreleased_product == 'Yes' else 0
	mdb = 1 if attrs.marshalling_db == 'Yes' else 0
	ai = int(attrs.AI)
	ao = int(attrs.AO)
	do = int(attrs.DO)
	di = int(attrs.DI)
	proNIO  = int(attrs.profitnet_IO)
	eIPIO   = int(attrs.ethernet_IO)
	pcdi = int(attrs.peer_pcdi)
	cda = int(attrs.peer_cda)
	wio = ai + ao + do + di
	hio = float(wio + proNIO + eIPIO)
	sio = pcdi + cda
	io = hio + sio
	is_ios = 1.0 if attrs.is_ios > 0 else 0
	A = float(attrs.num_rg)
	im  = attrs.implementation_method
	bq = bsd = bmd = bcd = bmu = bru = bmr = bpr = bcscm = bco = bpfat = 0
	F = 20.5 if attrs.process_type in ['Batch - Pharma', 'BatchPharma'] else 13.0
	uio = 1 if int(attrs.uio) > 0 else 0
	iof = 1
	Numserv = int(attrs.NumServ)
	#attrs.process_type in ['Batch - Pharma', 'BatchPharma', 'Batch - Chemical','BatchChemical']
	if pT == 2:
		bsd = int(attrs.simple_complexity)
		bmd = int(attrs.medium_complexity)
		bcd = int(attrs.complex_complexity)
		bmu = int(attrs.batch_unit)
		bru = int(attrs.batch_unit_copies)
		bmr = int(attrs.product_master_recipes)
		bpr = int(attrs.product_replicated)
		bcscm = int(attrs.complex_scms)
		bco = int(attrs.complex_ops)
		bpfat = int(attrs.percentage_pre_fat)
		input_quality = attrs.input_quality
		if input_quality in ['Only verbal Description(Function Plan must be developed from scratch) 100%','OnlyverbalDescription']:
			bq = 1.0
		elif input_quality in ['Function Plan available(One revision) 40 %','FunctionPlanavailableOne']:
			bq = 0.4
		elif input_quality in ['Function Plan available(Simple correction necessary) 15 %','FunctionPlanavailableSimple']:
			bq = 0.15
	base = 0
	#based on tickets CXCPQ-117945, the formula has been updated. The previous formula has been commented out for reference
	#HW = (1.2 * (48 + (hio/200)  + (12*is_ios)/(is_ios+1) + (2 * A)/ (A + 1) + 1+ (1 + 3 * mdb)**2 + 4 * unP + 8) + 20 * proT)*0.9
	'''if io<= 400:
		base = 8
	elif io > 400 and io<=2000:
		base = 16
	elif io>2000 and io<= 5000:
		base = 32
	elif io> 5000:
		base = 64
	odd = float((do)/1.2)
	odi = float((di - (float(odd)*1.5))/1.5)
	ob = float(ai + odd + odi)
	CP = (base + 0.05 * (pT * ob) +0.02*(pcdi+cda))*0.9 '''
	if io <= 400:
		base = 60
	elif io > 400 and io <= 2000:
		base = 80
	elif io > 2000 and io <= 5000:
		base = 100
	elif io > 5000:
		base = int(attrs.mFDS)

	HW = (1 - (uio * 0.25)) * (1.2 * ((wio / 200.0) +(12 * (is_ios / (is_ios + 1))) +(2 * (A / (A + 1.0))) +(iof + (3 * mdb)) ** 2 )) * 0.66
	CP = pT * base * Numserv
	Batch = bq * ((F * bmu * 5) + (58 * bmu * bcscm) + (6.56 * bmr * 5) + (13.45 * bmr * bco))
	if im in ["Non Standard Build Estimate", "NonStandardBuildEstimate"]:
		Hrs = round(HW + CP + bat*Batch,2)
	else:
		Hrs = round(((HW*0.7) + CP) + bat*Batch,2)
	Trace.Write('Deliverable: Functional Design Specification, Calculated Hours:{}, hw:{}, cp:{}, batch:{}'.format(Hrs,HW,CP,Batch))
	return Hrs