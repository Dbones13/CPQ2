def getDataGatheringHours(Var_7,Var_22,Var_31,additonOfParamenters,Var_1):
	#Modified Calculation Formulla By Saqlain Malik on account of ticket CCEECOMMBR-6332
	calcVal = 0
	if Var_22 in ("YES", "Yes"):
		if additonOfParamenters > 25:
			calcVal = 32
		elif additonOfParamenters > 8 and additonOfParamenters <=25:
			calcVal = 16
		else:
			calcVal = 12
	else:
		calcVal = 0
	manhoursForDataGathering = 0
	if Var_31 in ("No","NO",""):
		manhoursForDataGathering = calcVal
	else:
		manhoursForDataGathering = Var_7 * calcVal
	manhoursForDataGathering += 8 if Var_31 in ("YES", "Yes") else 0
	manhoursForDataGathering = manhoursForDataGathering * (Var_1/2)
	return manhoursForDataGathering

def getDOcumentationHours(Product,Var_32,Var_33,additonOfParamenters):
	documentationRequired = Product.Attr('OPM_Which_documentation_is_required').GetValue()
	selectedDocumentation = documentationRequired.split(',')
	selectedDocumentation = [x.strip() for x in selectedDocumentation]
	Var_16 = "HSE and Quality Plan"
	Var_17 = "Power and Heat Calculation"
	Var_18 = "EPKS Documentation FDS/DDS/Sys"
	Var_19 = "Make or Update a drawing package"
	Var_20 = "Update existing document"
	documentationHours = 0
	if  Var_16 in selectedDocumentation:
		documentationHours = documentationHours + 8
	if Var_17 in selectedDocumentation:
		documentationHours = documentationHours + 16
	if Var_18 in selectedDocumentation:
		documentationHours = documentationHours + 40
	if Var_19 in selectedDocumentation:
		documentationHours = documentationHours + 40
	if Var_20 in selectedDocumentation:
		documentationHours = documentationHours + 20

	if Var_32 == "Yes":
		documentationHours = documentationHours + 12
	try:
		documentationHours = documentationHours + float(Var_33)
	except:
		Trace.Write("Var_33 is a String")
	migrationHours = 0
	if additonOfParamenters > 8:
		migrationHours = 22
	else:
		migrationHours = 8
	TotalDocumentationHours = documentationHours + migrationHours
	return TotalDocumentationHours

def getPreFATSAT(Var_31, Var_23, Var_4, Var_27, Var_7, Var_3, Var_8, Var_24, Var_9, Var_28, Var_29, Var_21, Var_10, Var_1, Var_2):
	preFatCal = 0
	if Var_31 in ('No',''):
		if Var_23 in ["FAT", "FAT & SAT"]:
			preFatCal = (((Var_4 + Var_27) * Var_7 * 8) + (Var_3 * Var_7 * 7) + Var_8 * 8 + Var_24 * 8 + Var_9 * 2 + Var_28 * 0.5 + Var_29 * 1)
			if Var_21 == "Yes" and Var_10 < 5:
				preFatCal += (Var_1 + Var_2) * Var_7 * 11
			elif Var_21 == "No" and Var_10 < 5:
				preFatCal += (Var_1 + Var_2) * Var_7 * 10
			elif Var_10 > 4:
				preFatCal += (Var_1 + Var_2) * Var_7 * 16
		elif Var_23 in ["HAT", "HAT & SAT"]:
			preFatCal+= 16
		else:
			preFatCal = 0
	else:
		preFatCal = 0

	if Var_23 in ["FAT", "FAT & SAT"]:
		preFatCal += (Var_1 + Var_2) * 3 + (Var_3 + Var_4 + Var_27) * 1 + 8
	elif Var_23 in ["HAT", "HAT & SAT"]:
		preFatCal += 8 + 8

	return preFatCal

def getMigration2Hours(Var_23,Var_4,Var_27,Var_7,Var_3,Var_8,Var_24,Var_9,Var_28,Var_29,Var_10,Var_1,Var_2,Var_21,Var_31):
	migration1Cal = 0
	if Var_31 in ('No',''):
		if Var_23 in ('HAT','HAT & SAT','SAT','No'):
			migration1Cal = ((Var_4 + Var_27) * Var_7 * 8) + (Var_3 * Var_7 * 7) + (Var_8 * 8) + (Var_24 * 8) + (Var_9 * 2) + (Var_28 * 0.5) + (Var_29 * 1)
			if Var_21 == "Yes" and Var_10 < 5:
				migration1Cal = migration1Cal + ((Var_1 + Var_2) * Var_7 * 11)
			elif Var_21 == "No" and Var_10 < 5:
				migration1Cal = migration1Cal + ((Var_1 + Var_2) * Var_7 * 10)
			if Var_10 > 4:
				migration1Cal = migration1Cal + ((Var_1 + Var_2) * Var_7 * 16)
		if Var_23 in ('FAT','FAT & SAT'):
			migration1Cal = 2 + ((Var_1 + Var_2) * 3) + ((Var_3 + Var_4 + Var_27) * 2) + (Var_8 * 3) + (Var_24 * 3) + (Var_9 * 0.25) + (Var_28 * 0.25) + (Var_29 * 0.25)
	else:
		migration1Cal = 0
	return migration1Cal

def getSATHours(Var_23):
	satCal = 0
	if Var_23 in ('SAT','HAT & SAT','FAT & SAT'):
		satCal = 16
	return satCal

def getMigrationL1Hours(Var_10,Var_7,Var_14,Var_11,Var_12,Var_13,Var_26,Var_25,Var_5,Var_6):
	migrationL1Cal = 0
	calc = 1 if (Var_5 =="R41x.x" and Var_6=="R530") or ( Var_5=="R43x.x" and Var_6=="R530") else Var_7
	#migrationL1Cal = (Var_10 * Var_7 * 3) + (Var_14 * 0.5) + (Var_11 * 0.5) + (Var_12 * 0.5) + (Var_13 * 0.25) + (Var_26 * 0.75)
	migrationL1Cal = (Var_10 * calc * 3) + (Var_14 * 0.5 * calc) + (Var_11 * 0.5 * calc) + (Var_12 * 0.5) + (Var_13 * 0.25) + (Var_26 * 0.75)
	if Var_5 in ('PSR400','PSR500','R10x.x','R201.x'',R210.x','R211.1','R300.1','R301.1','R301.2','R301.3','R310.2','R310.3','R311.2','R311.3'):
		migrationL1Cal = migrationL1Cal + (Var_25 * 0.15)
	return migrationL1Cal

def getPostMigrationTask(additonOfParamenters):
	postMigrationTaskHoursCal = 0
	if additonOfParamenters > 8:
		postMigrationTaskHoursCal = 32
	else:
		postMigrationTaskHoursCal = 24
	return postMigrationTaskHoursCal

def getOPMDeploymentL2 (Var_31,Var_1,Var_2,Var_3,Var_4,Var_7,Var_8,Var_9,Var_24,Var_27,Var_28,Var_29,Var_6,Var_5):
	opmL2 = 0
	opmVar =float( 1.5 if (Var_5 in ['R41x.x','R43x.x']) else 1)
	if Var_6 == "R530":
		if Var_31 not in ('No',''):
			opmL2 = (Var_1+Var_2)*4*Var_7*(opmVar)+(Var_3+Var_27+Var_4)*1.5*Var_7*(opmVar)+Var_8*3+Var_24*3+Var_9*2+Var_28*0.5+Var_29*1
	else:
		if Var_31 not in ('No',''):
			opmL2 = (Var_1+Var_2)*4*Var_7+(Var_3+Var_27+Var_4)*1.5*Var_7+Var_8*3+Var_24*3+Var_9*2+Var_28*0.5+Var_29*1
			#Trace.Write(opmL2)
	return opmL2


def getOpmMcoe(Var_1,Var_2,Var_3,Var_4,Var_7,Var_8,Var_9,Var_10,Var_21,Var_23,Var_24,Var_27,Var_28,Var_29,Var_31,Var_6,Var_5):
	opmVar = float(1.5 if (Var_5 in ['R41x.x','R43x.x']) else 1)
	if Var_6=='R530':
		if Var_31 in ('No','NO',''):
			result = 0
		else:
			if Var_23 in ["HAT", "HAT & SAT", "SAT", "NO", "FAT", "FAT & SAT"]:
				result = (((Var_4 + Var_27) * Var_7 * opmVar * 8) + (Var_3 * Var_7 * opmVar * 7) + Var_8 * 8 + Var_24 * 8 + Var_9 * 2 + Var_28 * 0.5 + Var_29 * 1)
				if Var_21 in ("YES", "Yes") and Var_10 < 5:
					result += (Var_1 + Var_2) * Var_7 * opmVar * 11
				if Var_21 in ('No','NO','') and Var_10 < 5:
					result += (Var_1 + Var_2) * Var_7 * opmVar * 10
				if Var_10 > 4:
					result += (Var_1 + Var_2) * Var_7 * opmVar * 14
			else:
				result = 0

			if Var_31 in ('No','NO',''):
				result -= 0
			else:
				result -= ((Var_1 + Var_2) * 4 * Var_7 * opmVar + (Var_3 + Var_27 + Var_4) * 1.5 * Var_7 * opmVar + Var_8 * 3 + Var_24 * 3 + Var_9 * 2 + Var_28 * 0.5 + Var_29 * 1)
	else:
		if Var_31 in ('No','NO',''):
			result = 0
		else:
			if Var_23 in ["HAT", "HAT & SAT", "SAT", "NO", "FAT", "FAT & SAT"]:
				result = (((Var_4 + Var_27) * Var_7 * 8) + (Var_3 * Var_7 * 7) + Var_8 * 8 + Var_24 * 8 + Var_9 * 2 + Var_28 * 0.5 + Var_29 * 1)
				if Var_21 in ("YES", "Yes") and Var_10 < 5:
					result += (Var_1 + Var_2) * Var_7 * 11
				if Var_21 in ('No','NO','') and Var_10 < 5:
					result += (Var_1 + Var_2) * Var_7 * 10
				if Var_10 > 4:
					result += (Var_1 + Var_2) * Var_7 * 14
			else:
				result = 0

			if Var_31 in ('No','NO',''):
				result -= 0
			else:
				result -= ((Var_1 + Var_2) * 4 * Var_7 + (Var_3 + Var_27 + Var_4) * 1.5 * Var_7 + Var_8 * 3 + Var_24 * 3 + Var_9 * 2 + Var_28 * 0.5 + Var_29 * 1)
	return result