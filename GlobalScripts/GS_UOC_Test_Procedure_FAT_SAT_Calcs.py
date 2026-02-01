def GS_UOC_Test_Procedure_FAT_SAT_Calcs(attrs):
	im = str(attrs.implementation_method)
	isi = 1 if int(attrs.is_ios) > 0 else 0 #'is' replaced with 'isi'
	sys = float(attrs.sys)
	mar = float(attrs.marshalling_cabinets)
	uio = 1 if int(attrs.uio) > 0 else 0

	hw_FAT_Proc_Hrs = (1-uio*0.1)*4.75*(0.007*(sys*40*0.5+mar*(40+isi*10)))

	hw_SAT_Proc_Hrs = (1-uio*0.1)*2*(0.007*(sys*40*0.5+mar*(40+isi*10)))

	if im == "NonStandardBuildEstimate":
		HW_Hrs = hw_FAT_Proc_Hrs + hw_SAT_Proc_Hrs
	else:
		HW_Hrs = hw_FAT_Proc_Hrs * 0.6 + hw_SAT_Proc_Hrs * 0.6

	pt_dict = {'Continuous' : 1, 'ContinuousInterlockSequence' : 1.8, 'ContinuousSequence' : 1.5, 'ContinuousInterlock' : 1.2, 'BatchPharma' : 2, 'BatchChemical': 2}

	process_type = attrs.process_type

	try:
		pT= pt_dict[process_type]
	except KeyError:
		pT = 1

	ty = int(attrs.ttl_typicals)
	cl = int(attrs.complex_loop_labour)

	ctr_FAT_Proc_Hrs = 16 + 2*pT*(ty+cl)

	ctr_SAT_Proc_Hrs = 12 + 1.5*pT*(ty+cl)

	Hrs = HW_Hrs + ctr_FAT_Proc_Hrs + ctr_SAT_Proc_Hrs

	return Hrs
