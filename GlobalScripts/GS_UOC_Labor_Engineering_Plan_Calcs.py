def GS_UOC_Labor_Engineering_Plan_Calcs(attrs):
	ai = int(attrs.AI)
	ao = int(attrs.AO)
	di = int(attrs.DI)
	do = int(attrs.DO)
	A = float(attrs.num_rg)
	base = 0
	proT = 0 if attrs.project_type == 'New' else 1
	unP = 1 if attrs.unreleased_product == 'Yes' else 0
	mdb = 1 if attrs.marshalling_db == 'Yes' else 0
	isi = 1.00 if int(attrs.is_ios) > 0 else 0.00 #'is' replaced with 'isi'
	wio = float(ai + ao + di + do)
	io = ai + ao + di + do + int(attrs.profitnet_IO) + int(attrs.ethernet_IO) + int(attrs.peer_pcdi) + int(attrs.peer_cda)
	iof = 1 #fix value given in the sheet
	#Based on tickets CXCPQ-117945 the formula has been updated. The previous formula has been commented out for reference
	'''if attrs.ges_location == 'None' or attrs.ges_location == '':
		if io <=400:
			base = 8
		elif io > 400 and io <=2000:
			base=16
		elif io > 2000 and io<=5000:
			base=40
		elif io > 5000:
			base = 40
	else:
		if io <=400:
			base = 24
		elif io > 400 and io <=2000:
			base=32
		elif io > 2000 and io<=5000:
			base=56
		elif io > 5000:
			base = 56

	HW = "{0:.2f}".format((0.1 * (1.1 * (48 + wio/ 200 + 12*isi/(isi+1) ) + 2 * A / (A+ 1) + 1 + (1 + 3 * mdb)**2 + 4 * unP+8)) + 10 *proT)'''
	if io>0 and io<=400:
		base = 12
	elif io>400 and io<=2000:
		base = 20
	elif io>2000 and io<=5000:
		base = 44
	elif io>5000:
		base = int(attrs.mEP)

	HW = "{0:.2f}".format(0.19 * (1.1 * (wio / 200 + 12 * isi / (isi + 1) + 2 * A / (A + 1) + (iof + 3 * mdb) ** 2)))
	Hrs = float(HW) + float(base)
	return Hrs