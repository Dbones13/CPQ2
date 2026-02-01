def GS_UOC_Hardware_Engineering_Calcs(attrs):
	ai = int(attrs.AI)
	ao = int(attrs.AO)
	do = int(attrs.DO)
	di = int(attrs.DI)
	sys = attrs.sys
	mar = int(attrs.marshalling_cabinets)
	wio = ai + ao + do + di
	mdb = 1 if attrs.marshalling_db == 'Yes' else 0
	A = int(attrs.num_rg)
	ld = 1 if attrs.loop_drawings == 'Yes' else 0
	uio = 1 if int(attrs.uio) > 0 else 0
	iof = 1 #fixed value
	isi = 1 if int(attrs.is_ios)> 0 else 0

	# Updated formulas based on CXCPQ-117945
	CS_Hrs = (1-uio*0.15)*1.6*(wio/300.0+0.1*mar*mdb+0.5*sys+0.5*A)
	CD_Hrs = (1-uio*0.2)*0.7*((0.16*wio+10*iof)*mdb+0.16*wio*0.06*isi)*1.05
	LD_Hrs = (1-uio*0.35)*0.38*ld*((0.16*wio+10*iof)*mdb+0.16*wio*0.06*isi)*1.05


	im  = attrs.implementation_method
	Hrs = CS_Hrs * 0.9 + CD_Hrs + LD_Hrs
	if im in ["Non Standard Build Estimate", "NonStandardBuildEstimate"]:
		Hrs = CS_Hrs + CD_Hrs + LD_Hrs
	return round(Hrs,2)