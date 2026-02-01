def GS_UOC_Hardware_DetailDesign_Spec_Calcs(attrs):
	isi = 1 if int(attrs.is_ios)> 0 else 0
	im  = attrs.implementation_method
	A = int(attrs.num_rg)
	sys = float(attrs.sys)
	mar = float(attrs.marshalling_cabinets)
	CRHrs =2*((sys+mar)*0.5)*0.9
	uio = 1 if int(attrs.uio) > 0 else 0

	if im == "Non Standard Build Estimate":
		CCHrs =(1-(uio *0.15))*1.1 * ((sys * 8) + (mar *(8+(isi * 2)))) * 0.9
		Hrs = round(((CCHrs * 0.7) + CRHrs),2)
	else:
		CCHrs =(1-(uio *0.15))*1.1 * ((sys * 8) + (mar *(8+(isi * 2)))) * 0.9 * 0.7
		Hrs = round((CCHrs + CRHrs),2)
	return Hrs