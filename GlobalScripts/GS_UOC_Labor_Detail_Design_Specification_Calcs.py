def GS_UOC_Labor_Detail_Design_Specification_Calcs(attrs):
	Base= 0
	ges_location = attrs.ges_location
	im  = attrs.implementation_method
	Ctr = int(attrs.ctr)
	QpT  = attrs.process_type
	ai = int(attrs.AI)
	ao = int(attrs.AO)
	di = int(attrs.DI)
	do = int(attrs.DO)
	nty = int(attrs.new_typicals)
	A = int(attrs.num_rg)
	proT = 0 if attrs.project_type == 'New' else 1
	unP = 1 if attrs.unreleased_product == 'Yes' else 0
	mdb = 1 if attrs.marshalling_db == 'Yes' else 0
	isi = 1 if int(attrs.is_ios) > 0 else 0 #'is' replaced with 'isi'
	wio = ai + ao + di + do
	io = ai + ao + di + do + int(attrs.profitnet_IO) + int(attrs.ethernet_IO) + int(attrs.peer_pcdi) + int(attrs.peer_cda)
	bat = 1 if (attrs.process_type in ['Batch - Pharma', 'BatchPharma', 'Batch - Chemical','BatchChemical']) else 0
	sNode =  int(attrs.scada_node_type)
	ty = int(attrs.ttl_typicals)

	if QpT == 'ContinuousInterlockSequence':
		pT = 1.8
	elif QpT == 'ContinuousSequence':
		pT = 1.5
	elif QpT == 'ContinuousInterlock':
		pT = 1.2


	pT = 2 if ( QpT == 'BatchPharma' or QpT == 'BatchChemical'  ) else 1


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
	else:
		pT = 1
	'''
	if im in ('StandardBuildEstimate','Standard Build Estimate'):
		if io<= 400:
			Base = 8
		elif io> 400 and io<=2000:
			Base=16
		elif io>2000 and io<= 5000:
			Base = 32
		elif io> 5000:
			Base = 64

	if im == 'NonStandardBuildEstimate':
		if io <= 400:
			Base = 16
		elif io> 400 and io<=2000:
			Base = 32
		elif io>2000 and io<= 5000:
			Base = 64
		elif io>5000:
			Base = 128

	if ges_location == 'None' or attrs.ges_location == '':
		Hrs = (Base + (8 * Ctr) + (16 * pT * nty ) ) * 0.9 + ( 120 * bat )

	else:
		Hrs = ((Base + (10 * Ctr) + (20 * pT * nty) ) * 0.9 + (120 * bat ) )'''

	#Updated Calculation as part of the ticket CXCPQ-117945
	if io > 0 and io <= 400:
		Base = 60
	elif io > 400 and io <= 2000:
		Base = 80
	elif io > 2000 and io <= 5000:
		Base = 100
	elif io > 5000:
		Base = int(attrs.mDDS)

	Hrs = (Base + 10 * Ctr + 10 * sNode + (20 * nty + 5 * (ty - nty)) * pT + 120 * bat)

	return Hrs