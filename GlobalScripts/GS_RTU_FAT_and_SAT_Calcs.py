def GS_RTU_FAT_and_SAT_Calcs(param):
	tns = int(param.rtu)
	if tns < 48:
		cal_hrs = 48
	elif tns >= 48 and tns < 168:
		cal_hrs = 80
	else:
		cal_hrs = 80
	return cal_hrs