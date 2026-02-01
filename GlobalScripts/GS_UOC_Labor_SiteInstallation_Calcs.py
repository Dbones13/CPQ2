def GS_UOC_Labor_SiteInstallation_Calcs(attrs):
	mar = int (attrs.marshalling_cabinets)
	A = int(attrs.num_rg)
	sys = int (attrs.sys)

	#Hrs = round (6 +( 6 * (mar + sys)) + (4 *A))

	#Hrs = 0.76*(6*(mar+sys)+4*A)

	return 0.76*(6*(mar+sys)+4*A)
