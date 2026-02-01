def GS_UOC_Labor_SystemIntegration_Internal_Calcs(attrs):
	sys = int(attrs.sys)
	mar = int(attrs.marshalling_cabinets)
	isi= 1 if int(attrs.is_ios) > 0  else  0    #'is'replacedwith'isi'
	A = int(attrs.num_rg)
	uio = 1 if int(attrs.uio) > 0 else 0
	IntegrationHrs = 0.82*(6*(mar+sys)+2*A)
	IntTestHrs = (1-uio*0.1)*0.12*(sys*40*0.5+mar*(40+isi*10))
	Hrs = IntegrationHrs + IntTestHrs

	return Hrs