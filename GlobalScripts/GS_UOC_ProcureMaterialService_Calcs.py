def GS_UOC_ProcureMaterialService_Calcs(attrs):
	isi = 1 if int(attrs.is_ios)> 0 else 0
	A = int(attrs.num_rg)
	unP = 1 if attrs.unreleased_product=='Yes'else 0
	sys = float(attrs.sys)
	mar = float(attrs.marshalling_cabinets)
	uio = 1 if int(attrs.uio) > 0 else 0
	iof = 1 #fixed value

	#Based on tickets CXCPQ-117945, the formula has been updated. The previous formula has been commented out for reference 
	'''BOMHrs = ( isi + 0.1 * (sys + mar ) + 2 * (sys + mar ) / (sys + mar + 1) + 2 * A  + 2 * (1+1))
	IPRHrs = ( 0.5 * sys  + 2 * sys  / (sys  + 1) + 0.5 * A + 2 * (1+1)+4 * unP)
	OPRHrs =  isi *4 + mar +  5 * mar / (mar + 1)  + 2 * A

	Hrs = BOMHrs + IPRHrs + OPRHrs
	return round(Hrs,2)'''

	# calculations
	BOMHrs = (1-uio*0.15)*1.9*(isi+0.1*(mar+sys)+2*(mar+sys)/(mar+sys+1)+2*A+2*iof)
	IPRHrs = (1-uio*0.05)*(0.5*sys+2*sys/(sys+1)+0.5*A+2*iof)*1.05
	OPRHrs = (isi*4+mar+5*mar/(mar+1)+2*A)*0.8
	im  = attrs.implementation_method
	Hrs = BOMHrs + IPRHrs + OPRHrs
	if im in ["Non Standard Build Estimate", "NonStandardBuildEstimate"]:
		Hrs = BOMHrs * 0.95 + IPRHrs + OPRHrs
	return round(Hrs,2)