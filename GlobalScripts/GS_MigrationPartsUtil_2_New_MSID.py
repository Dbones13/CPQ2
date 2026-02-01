import math
def getContainer(prod, conName):
	return prod.GetContainerByName(conName)
def getFloat(Var):
	if Var:
		return float(Var)
	return 0

def updateAttrDictWithCustomC200toC300(product, attrValDict, Quote):
	con1 = getContainer(product, 'C200_Migration_General_Qns_Cont')
	con2 = getContainer(product, 'C200_Migration_Config_Cont')
	con3 = getContainer(product, 'C200_C300_Series_C_Cabinet_Config_Cont')
	con4 = getContainer(product, 'C200_C300_Series_C_Cabinet_Config_Cont_FAOnly')
	
	providingFTECables = con1.Rows[0]['C200_Is_Honeywell_Providing_FTE_cables'] #empty
	existingC200Server = con1.Rows[0]['C200_Connection _to_Experion_Server'] #FTE
	AvgCableLength = con1.Rows[0]['C200_Average_Cable_Length'] #empty
	FTEswitch = con1.Rows[0]['C200_FTE_Switch_to_connect_required_exp_servers'] #empty
	additionalSwitches = getFloat(con1.Rows[0]['C200_Number_of_additional_switches']) #0

	if con3:
		cabinetdoors = con3.Rows[0]['C200_C300_Cabinet_Doors'] #standard
		cabinethingetype = con3.Rows[0]['C200_C300_Cabinet_Hinge_Type'] #empty
		cabinetkeylock = con3.Rows[0]['C200_C300_Cabinet_Keylock_Type'] #empty
		cabinetcolor = con3.Rows[0]['C200_C300_Cabinet_Color'] #empty
		FanVoltage = con3.Rows[0]['C200_C300_Fan_Voltage'] #empty
		powerSystemVendor = con3.Rows[0]['C200_C300_Power_System_Vendor']#Meanwell
		powerSystemType = con3.Rows[0]['C200_C300_Power_System_Type']#Redundant 20A
	else:
		cabinetdoors = product.Attr('C200_C300_Cabinet_Doors').GetValue() #standard
		cabinethingetype = product.Attr('C200_C300_Cabinet_Hinge_Type').GetValue() #empty
		cabinetkeylock = product.Attr('C200_C300_Cabinet_Keylock_Type').GetValue() #empty
		cabinetcolor = product.Attr('C200_C300_Cabinet_Color').GetValue() #empty
		FanVoltage = product.Attr('C200_C300_Fan_Voltage').GetValue() #empty
		powerSystemVendor = product.Attr('Power System Vendor').GetValue() #Meanwell
		powerSystemType = product.Attr('Power System Type').GetValue() #Redundant 20A

	if con4:
		cabinetdoorsFAOnly = con4.Rows[0]['C200_C300_Cabinet_Doors_FAOnly'] #standard
		cabinethingetypeFAOnly = con4.Rows[0]['C200_C300_Cabinet_Hinge_Type_FAOnly'] #empty
		cabinetkeylockFAOnly = con4.Rows[0]['C200_C300_Cabinet_Keylock_Type_FAOnly'] #empty
		cabinetcolorFAOnly = con4.Rows[0]['C200_C300_Cabinet_Color_FAOnly'] #empty
		FanVoltageFAOnly = con4.Rows[0]['C200_C300_Fan_Voltage_FAOnly'] #empty
		powerSystemFAVendor = con4.Rows[0]['C200_C300_Power_System_Vendor']#Meanwell
		powerSystemFAType = con4.Rows[0]['C200_C300_Power_System_Type']#Redundant 20A
	else:
		cabinetdoorsFAOnly = product.Attr('C200_C300_Cabinet_Doors_FAO').GetValue() #standard
		cabinethingetypeFAOnly = product.Attr('ATT_C200C300CABHTYP').GetValue() #empty
		cabinetkeylockFAOnly = product.Attr('ATT_C200C300CABKEYTYP').GetValue() #empty
		cabinetcolorFAOnly = product.Attr('ATT_C200C300CABCLR').GetValue() #empty
		FanVoltageFAOnly = product.Attr('ATT_C200C300FANVOLT').GetValue() #empty
		powerSystemFAVendor = product.Attr('ATT_C200C300PSV').GetValue() #Meanwell
		powerSystemFAType = product.Attr('ATT_C200C300PST').GetValue() #Redundant 20A

	#sespType = Quote.GetCustomField("Entitlement").Content if Quote and Quote.GetCustomField("Entitlement").Content else "No"
	sespType = "No" if Quote and Quote.GetCustomField("Entitlement").Content in ('','None','Non-SESP MSID with new SESP Flex','Support Flex') else "Yes"

	test = 0
	X_TKFTEB01 = 0
	#UHOKit Parts
	X_CCZHR042 = 0
	X_CCZHR041 = 0
	X_CCZHMT10 = 0
	X_CCZHER01 = 0
	X_TCEPLX01 = 0
	X_TCCSUG50 = 0
	X_TSCSUG50 = 0
	X_51305980136 = 0
	X_51305980236 = 0
	X_51454475100 = 0
	X_51202329722 = 0
	X_51202329732 = 0
	X_51202341112 = 0
	#X_SIM = 0

	#newC300Parts
	Y_CCPCNT05 = 0
	Y_CCTCNT01 = 0
	Y_CCPCNT02 = 0
	Y_TCSWCS30 = 0
	Y_CCTCF901 = 0
	Y_CCPCF901 = 0
	Y_CCTFB412 = 0
	Y_CCTFB402 = 0
	Y_CCPFB401 = 0
	Y_CCTFB811 = 0
	Y_CCPFB801 = 0
	Y_51202329102 = 0 #Common
	Y_51202329302 = 0 #Common
	Y_51202329312 = 0
	Y_51305980184 = 0
	Y_51305980284 = 0
	Y_51305980836 = 0

	Y_CCSCMB05 = 0
	Y_CCSCMB02 = 0
	Y_NEFWMB01 = 0 #Common
	Y_NEFWMB12 = 0 #Common
	Y_8937HN = 0
	Y_8939HN = 0
	Y_CCKFPGR5 = 0
	Y_CCKFPVR5 = 0
	Y_51305482102 = 0 #Common
	Y_51305482202 = 0 #Common
	Y_51305482105 = 0 #Common
	Y_51305482205 = 0 #Common
	Y_51305482110 = 0 #Common
	Y_51305482210 = 0 #Common
	Y_51305482120 = 0 #Common
	Y_51305482220 = 0 #Common
	Y_TKFXX102 = 0 #Common
	Y_TKFPCXX2 = 0 #Common
	Y_TCXXXXX2 = 0 #Common
	'''CHANGES DONE BY RP: CXCPQ-91893'''
	Y_CCTEIM01 = 0
	Y_CCPEIM01 = 0

	#Cabinet Related
	Y_CC_MCAR01 = 0
	Y_51202335300 = 0
	Y_CCC8DS01 = 0
	Y_CCC8SS01 = 0
	Y_CCCBDD01 = 0
	Y_CCCBDS01 = 0
	Y_51199947175 = 0
	Y_51199947275 = 0
	Y_51199406200 = 0
	#Y_CCPWRB01 = 0
	#per upgrade
	Z_SI3300I2 = 0
	Z_SI920LN4 = 0
	Z_SI930LN4 = 0
	Z_SI920LN8 = 0
	Z_51305786_502 = 0
	Z_51199562_200 = 0

	#Cabinet Deduction Declarition
	noOfLocatSep_C8DS01 = 0
	noOfLocatSep_CBDD01 = 0

	#Other Declarition
	half_CCTCF901 = 0
	totaLSerialInterfaceModbusIOMs = 0
	currentMountQty = 0
	current8937HN = 0
	current8939HN = 0
	
	#new questions
	Y_CU_PWMR20 = 0
	Y_CU_PWMN20 = 0
	Y_CU_PWPR21 = 0
	Y_CU_PWPN21 = 0
	Y_CC_PWRR01 = 0
	Y_CC_PWRN01 = 0
	Y_CC_PWRB01 = 0
	Y_CC_PWR401 = 0
	Y_CC_PWN401 = 0

	try:
		tempdata=eval(eval("product.Attr('Temporary Data').GetValue()"))
	except:
		tempdata = None
	currentCC_TCNT01 = 0
	CQcon = getContainer(product, 'MSID_CommonQuestions')
	if CQcon:
		for row in CQcon.Rows:
			Trace.Write(row["MSID_Future_Experion_Release"])
			epks_rel = row["MSID_Future_Experion_Release"]
			break
	else:
		epks_rel = product.Attr("MSID_Future_Experion_Release").GetValue()

	for row in con2.Rows:
		FIM2IOMs_Redundant = getFloat(row['C200_Number_of_Redundant_FIM2_IOMs_to_FIM4_conversion'])
		FIM2IOMs_NonRedundant = getFloat(row['C200_Number_of_Non-Redundant_FIM2_IOMs'])
		PMIOMs = getFloat(row['C200_Number_of_PM_IOMs'])
		noOf1765DIDOAIAO = getFloat(row['C200_Number_of_1756_IOMs'])
		PulseInputIOMs = getFloat(row['C200_C300_Number_of_Pulse_Input_IOMs'])
		ProfibusIOMs = getFloat(row['C200_Number_of_Profibus_IOMs'])
		DeviceNetIOMs = getFloat(row['C200_Number_of_DeviceNet_IOMs'])
		C200PeerToPeer = row['C200_peer_to_peer_communication']#empty
		controllerRedundancy = row['C200_Controller_Redundancy']#empty
		SeriesAIORacks = getFloat(row['C200_C300_Number_of_Series_A_IO_Racks'])
		AllenBradleyIOMs = getFloat(row['C200_Number_of_Serial_Interface_Allen_Bradley_IOMs'])
		FIM2Points = FIM2IOMs_Redundant + FIM2IOMs_NonRedundant
		TotalIOs = math.ceil(noOf1765DIDOAIAO + PulseInputIOMs + ProfibusIOMs + DeviceNetIOMs)
		IOUnits = UHOCondition = math.ceil(PMIOMs + noOf1765DIDOAIAO * 1 + PulseInputIOMs * 1.5 + ProfibusIOMs * 4.5 + DeviceNetIOMs * 4 + FIM2Points * 4)

		"""TK-FTEB01 Calculation"""
		if (IOUnits == 0) and (existingC200Server != 'FTE') and (C200PeerToPeer == 'Allen Bradley PLC'):
			X_TKFTEB01 += 1
		if (existingC200Server == 'FTE') and (controllerRedundancy == 'Non Redundant') and (C200PeerToPeer == 'Allen Bradley PLC'):
			X_TKFTEB01 += SeriesAIORacks - 1 + AllenBradleyIOMs + 1
		if (existingC200Server == 'FTE') and (controllerRedundancy == 'Redundant' or controllerRedundancy == '') and (C200PeerToPeer == 'Allen Bradley PLC'):
			X_TKFTEB01 += SeriesAIORacks - 2 + AllenBradleyIOMs + 1
		if (existingC200Server != 'FTE') and (controllerRedundancy == 'Non Redundant') and (C200PeerToPeer == 'Allen Bradley PLC'):
			X_TKFTEB01 += SeriesAIORacks + AllenBradleyIOMs + 1
		if (existingC200Server != 'FTE') and (controllerRedundancy == 'Redundant' or controllerRedundancy == '') and (C200PeerToPeer == 'Allen Bradley PLC'):
			X_TKFTEB01 += SeriesAIORacks + AllenBradleyIOMs + 1

	#Assign TK-FTEB01 qty to dictionary
	attrValDict['TK-FTEB01'] = XX_TKFTEB01 = float(X_TKFTEB01)

	for row in con2.Rows:
		locateSeparate = row['C200_located_separated_from_0thers_remote_location']
		FIM2IOMs_Redundant = getFloat(row['C200_Number_of_Redundant_FIM2_IOMs_to_FIM4_conversion'])
		FIM2IOMs_NonRedundant = getFloat(row['C200_Number_of_Non-Redundant_FIM2_IOMs'])
		PMIOMs = getFloat(row['C200_Number_of_PM_IOMs'])
		noOf1765DIDOAIAO = getFloat(row['C200_Number_of_1756_IOMs'])
		PulseInputIOMs = getFloat(row['C200_C300_Number_of_Pulse_Input_IOMs'])
		ProfibusIOMs = getFloat(row['C200_Number_of_Profibus_IOMs'])
		DeviceNetIOMs = getFloat(row['C200_Number_of_DeviceNet_IOMs'])
		cabinetTypeCustomerPlans = row['C200_Cabinet_type_customer_plans']#empty
		ExistingPMorNonStandard = row['C200_Existing_PM_or_Non_Standard_Cabinet_Used']#empty
		ModbusFirewall = row['C200_Required_Modbus_Firewall']#empty
		SerialInterfaceModbusIOMs = getFloat(row['C200_Number_of_Serial_Interface_Modbus_IOMs'])
		C200PeerToPeer = row['C200_peer_to_peer_communication']#empty
		controllerRedundancy = row['C200_Controller_Redundancy']#empty
		SeriesAIORacks = getFloat(row['C200_C300_Number_of_Series_A_IO_Racks'])
		AllenBradleyIOMs = getFloat(row['C200_Number_of_Serial_Interface_Allen_Bradley_IOMs'])
		FIM2IOMtoFIM8IOM = getFloat(row['C200_Number_of_Redundant_FIM2_IOMs_to_FIM8_conversion'])
		FIM2Points = FIM2IOMs_Redundant + FIM2IOMs_NonRedundant + FIM2IOMtoFIM8IOM
		TotalIOs = math.ceil(noOf1765DIDOAIAO + PulseInputIOMs + ProfibusIOMs + DeviceNetIOMs)
		IOUnits = UHOCondition = math.ceil(PMIOMs + noOf1765DIDOAIAO * 1 + PulseInputIOMs * 1.5 + ProfibusIOMs * 4.5 + DeviceNetIOMs * 4 + FIM2Points * 4)

		"""Buying UHO Kit"""
		scope = product.Attr("MIgration_Scope_Choices").GetValue() #added for CXCPQ-109620 and below line added scope condition
		if (FIM2Points == 0) and (UHOCondition <= 64) and (cabinetTypeCustomerPlans != 'New Front Access Only Series C Cabinet' and cabinetTypeCustomerPlans != 'New Front & Rear Access Series C Cabinet'):
			if (epks_rel in ["R520","R530"] and (noOf1765DIDOAIAO > 0 or SeriesAIORacks > 0)) and scope != "LABOR":
				X_CCZHER01 += 1
				X_TCEPLX01 += 1
				X_51305980136 = X_TCEPLX01 * 2
				X_51305980236 = X_TCEPLX01 * 2
				X_51454475100 = X_TCEPLX01
			elif (epks_rel in ["R520","R530"] and noOf1765DIDOAIAO == 0 and SeriesAIORacks == 0) and scope != "LABOR":
				X_CCZHR042 += 1
				X_CCZHMT10 = X_CCZHR042
				X_51305980136 = X_CCZHR042 * 2
				X_51305980236 = X_CCZHR042 * 2
				X_51454475100 = X_CCZHR042
			elif scope != "LABOR":
				X_CCZHR041 += 1
				X_CCZHMT10 = X_CCZHR041
				X_51305980136 = X_CCZHR041 * 2
				X_51305980236 = X_CCZHR041 * 2
				X_51454475100 = X_CCZHR041
			if scope != "LABOR":	
				#X_SIM += SerialInterfaceModbusIOMs ##
				X_51202329722 += 1 if (PMIOMs > 0) else 0
				X_51202329732 += 1 if (PMIOMs > 40) else 0
				X_51202341112 += 1 if (PMIOMs > 40) else 0
				#Calculation for 51305482-102 to 220 ( same parts for new C300)
				#totalUHIOSerialInterfaceModbusIOMs += SerialInterfaceModbusIOMs

		else:
			flag = 0
			if(controllerRedundancy == 'Redundant' or controllerRedundancy == ''):
				currentCC_TCNT01 = 2.0 * math.ceil(IOUnits/64.0)
				Y_TCSWCS30 += currentCC_TCNT01/2.0
				Y_51305980836 += 1
				flag = currentCC_TCNT01/2.0
			else:
				currentCC_TCNT01 = 1.0 * math.ceil(IOUnits/64.0)
				Y_TCSWCS30 += currentCC_TCNT01
				flag = currentCC_TCNT01

			Y_CCTCNT01 += currentCC_TCNT01									 
			if currentCC_TCNT01 > 0 and tempdata:
				tempdata["C300_var_2"] += flag
				product.Attr('Temporary Data').AssignValue(str(tempdata))								 
			if PMIOMs > 0 and tempdata:
				tempdata["C300_var_11"] += flag
				product.Attr('Temporary Data').AssignValue(str(tempdata))

			#Y_CCPCNT02 += currentCC_TCNT01
			if epks_rel in ["R520","R530"]:
				Y_CCPCNT05 += currentCC_TCNT01
			else:
				Y_CCPCNT02 += currentCC_TCNT01

			Y_CCTFB412 += FIM2IOMs_Redundant
			Y_CCTFB402 += FIM2IOMs_NonRedundant

			currentCC_TCF901 = math.ceil(currentCC_TCNT01 / 2.0) * 2.0 + math.ceil(FIM2IOMs_Redundant/ 4.0) * 2.0 + math.ceil(FIM2IOMs_NonRedundant / 8.0) * 2.0

			Y_CCTCF901 += currentCC_TCF901
			Y_CCPCF901 += currentCC_TCF901
			Y_CCPFB401 += (FIM2IOMs_Redundant*2.0 + FIM2IOMs_NonRedundant)
			
			Y_CCTFB811 += FIM2IOMtoFIM8IOM
			Y_CCPFB801 += (FIM2IOMtoFIM8IOM *2.0)

			Y_51202329102 += 1 if (PMIOMs > 0) else 0
			Y_51305980184 += (currentCC_TCNT01 + FIM2IOMs_NonRedundant + FIM2IOMs_Redundant * 2)
			Y_51305980284 += (currentCC_TCNT01 + FIM2IOMs_NonRedundant + FIM2IOMs_Redundant * 2)

			if (PMIOMs > 0 and PMIOMs <= 40):
				current8937HN = current8939HN = 2
				Y_8937HN += 2
				Y_8939HN += 2
			elif(PMIOMs > 40):
				current8937HN = current8939HN = 4
				Y_8937HN += 4
				Y_8939HN += 4 
			Y_CCKFPGR5 += 1 if (PMIOMs > 0) else 0
			Y_CCKFPVR5 += 1 if (PMIOMs > 40) else 0

			#Preparation for total calculation for 51305482-102 to 220
			#totalC300SerialInterfaceModbusIOMs += SerialInterfaceModbusIOMs
			half_CCTCF901 += math.ceil(currentCC_TCF901/2.0)

			#Memory Calculation
			currentCC_SCMB02 = math.ceil(currentCC_TCNT01/4.0)
			#Mounting Unit Calculation
			if currentCC_TCNT01 > 0:
				currentMountQty = 3.0 * currentCC_TCNT01 + currentCC_SCMB02 + 2.0 * currentCC_TCF901 + 2.0 * current8937HN + 2.0 * current8939HN + FIM2IOMs_NonRedundant * 2.0 + FIM2IOMs_Redundant * 4.0 + FIM2IOMtoFIM8IOM * 4.0            
			#Cabinet Sides Calculation   
			currentCC_MCAR01 = math.ceil(currentMountQty/12.0)
			currentCabSides = math.ceil(currentCC_MCAR01/6.0)

			#Cabinet Calculation - Front and Rear Access
			if (cabinetTypeCustomerPlans == 'New Front & Rear Access Series C Cabinet' or ExistingPMorNonStandard == 'New Front & Rear Access Series C Cabinet' or ExistingPMorNonStandard == ''):
				if(cabinetdoors == 'Standard' or cabinetdoors == '') and (cabinethingetype == '130 Degrees' or cabinethingetype == '') and (cabinetkeylock == 'Standard' or cabinetkeylock == '') and (cabinetcolor == 'Gray-RAL7035' or cabinetcolor == ''):
					current_C8DS01 = math.ceil(currentCabSides/2.0)
					Y_CCC8DS01 += current_C8DS01
					#Cabinet Deduction Preparation
					if(current_C8DS01 > 0 and (locateSeparate=='No' or locateSeparate =='') and currentCabSides == 1):
						noOfLocatSep_C8DS01 += 1
				else:
					current_CBDD01 = math.ceil(currentCabSides/2.0)
					Y_CCCBDD01 += current_CBDD01
					#Cabinet Deduction Preparation
					if(current_CBDD01 > 0 and (locateSeparate=='No' or locateSeparate =='') and currentCabSides==1):
						noOfLocatSep_CBDD01 += 1

				#Fan calculation
				if (FanVoltage =='115VAC' or FanVoltage ==''):
					Y_51199947175 += currentCabSides
				else:
					Y_51199947275 += currentCabSides
				#Power System
				if (powerSystemVendor == 'Meanwell' or powerSystemVendor == '') and (powerSystemType == 'Redundant 20A' or powerSystemType == ''):
					Y_CU_PWMR20 = 1
				elif (powerSystemVendor == 'Meanwell' or powerSystemVendor == '') and powerSystemType == 'Non Redundant 20A':
					Y_CU_PWMN20 = 1
				elif powerSystemVendor == 'Phoenix Contact' and (powerSystemType == 'Redundant 20A' or powerSystemType == ''):
					Y_CU_PWPR21 = 1
				elif powerSystemVendor == 'Phoenix Contact' and powerSystemType == 'Non Redundant 20A':
					Y_CU_PWPN21 = 1
				elif powerSystemVendor == 'TDI' and (powerSystemType == 'Redundant 20A' or powerSystemType == ''):
					Y_CC_PWRR01 = 1
				elif powerSystemVendor == 'TDI' and powerSystemType == 'Non Redundant 20A':
					Y_CC_PWRN01 = 1
				elif powerSystemVendor == 'TDI' and powerSystemType == 'Redundant with BBU 20A':
					Y_CC_PWRB01 = 1
				elif powerSystemVendor == 'TDI' and powerSystemType == 'Redundant 40A':
					Y_CC_PWR401 = 1
				elif powerSystemVendor == 'TDI' and powerSystemType == 'Non Redundant 40A':
					Y_CC_PWN401 = 1
				

			#Cabinet Calculation - Front only Access
			elif (cabinetTypeCustomerPlans == 'New Front Access Only Series C Cabinet' or ExistingPMorNonStandard == 'New Front Access Only Series C Cabinet'):
				if(cabinetdoorsFAOnly  == 'Standard' or cabinetdoorsFAOnly  == '') and (cabinethingetypeFAOnly == '130 Degrees' or cabinethingetypeFAOnly == '') and (cabinetkeylockFAOnly == 'Standard' or cabinetkeylockFAOnly == '') and (cabinetcolorFAOnly == 'Gray-RAL7035' or cabinetcolorFAOnly == ''):
					Y_CCC8SS01 += currentCabSides
				else:
					Y_CCCBDS01 += currentCabSides
				#Fan calculation
				if (FanVoltageFAOnly =='115VAC' or FanVoltageFAOnly ==''):
					Y_51199947175 += currentCabSides
				else:
					Y_51199947275 += currentCabSides

				#Power System
				if (powerSystemFAVendor == 'Meanwell' or powerSystemFAVendor == '') and (powerSystemFAType == 'Redundant 20A' or powerSystemFAType == ''):
					Y_CU_PWMR20 = 1
				elif (powerSystemFAVendor == 'Meanwell' or powerSystemFAVendor == '') and powerSystemFAType == 'Non Redundant 20A':
					Y_CU_PWMN20 = 1
				elif powerSystemFAVendor == 'Phoenix Contact' and (powerSystemFAType == 'Redundant 20A' or powerSystemFAType == ''):
					Y_CU_PWPR21 = 1
				elif powerSystemFAVendor == 'Phoenix Contact' and powerSystemFAType == 'Non Redundant 20A':
					Y_CU_PWPN21 = 1
				elif powerSystemFAVendor == 'TDI' and (powerSystemFAType == 'Redundant 20A' or powerSystemFAType == ''):
					Y_CC_PWRR01 = 1
				elif powerSystemFAVendor == 'TDI' and powerSystemFAType == 'Non Redundant 20A':
					Y_CC_PWRN01 = 1
				elif powerSystemFAVendor == 'TDI' and powerSystemFAType == 'Redundant with BBU 20A':
					Y_CC_PWRB01 = 1
				elif powerSystemFAVendor == 'TDI' and powerSystemFAType == 'Redundant 40A':
					Y_CC_PWR401 = 1
				elif powerSystemFAVendor == 'TDI' and powerSystemFAType == 'Non Redundant 40A':
					Y_CC_PWN401 = 1
			#Y_CCSCMB02 += currentCC_SCMB02
			if epks_rel in ["R520","R530"]:
				Y_CCSCMB05 += currentCC_SCMB02
			else:
				Y_CCSCMB02 += currentCC_SCMB02
			'''CHANGES DONE BY RP: CXCPQ-91893'''
			if epks_rel in ["R520","R530"] and noOf1765DIDOAIAO > 0 and SeriesAIORacks > 0:
				Y_CCTEIM01 += 2
				Y_CCPEIM01 += 2
				X_TCEPLX01 += 1

			Y_CC_MCAR01 += currentCC_MCAR01
			Y_51202335300 += math.floor(currentCC_MCAR01/3.0)
			Y_51199406200 += currentCabSides
			#Y_CCPWRB01 += currentCabSides

		#Common Part for UHIO and C300
		Y_TKFXX102 += 1 if (C200PeerToPeer == 'Allen Bradley PLC') and (TotalIOs > 0) else 0
		Y_TKFPCXX2 += 1 if (C200PeerToPeer == 'Allen Bradley PLC') and (TotalIOs > 0) else 0
		Y_TCXXXXX2 += 3 if (C200PeerToPeer == 'Allen Bradley PLC') else 0
		Y_NEFWMB01 += SerialInterfaceModbusIOMs if (ModbusFirewall == 'Read-Write' or ModbusFirewall == '') else 0
		Y_NEFWMB12 += SerialInterfaceModbusIOMs if (ModbusFirewall == 'Read-Only') else 0  
		Y_51202329302 += 1 if (PMIOMs > 0) else 0
		Y_51202329312 += 1 if (PMIOMs > 40) else 0
		
		#Preparation for total calculation for 51305482-102 to 220
		totaLSerialInterfaceModbusIOMs += SerialInterfaceModbusIOMs

	X_TCCSUG50 = X_CCZHER01+X_CCZHR042+X_CCZHR041 if sespType == 'No' else 0
	X_TSCSUG50 = X_CCZHER01+X_CCZHR042+X_CCZHR041 if sespType == 'Yes' else 0

	#Calculation for final calculation for 51305482-102 to 220
	Y_51305482102 = X_TKFTEB01 + totaLSerialInterfaceModbusIOMs + half_CCTCF901 if (AvgCableLength == '2m') else 0
	Y_51305482202 = X_TKFTEB01 + half_CCTCF901 if (AvgCableLength == '2m') else 0
	Y_51305482105 = X_TKFTEB01 + totaLSerialInterfaceModbusIOMs+ half_CCTCF901 if (AvgCableLength == '5m') else 0
	Y_51305482205 = X_TKFTEB01 + half_CCTCF901 if (AvgCableLength == '5m') else 0
	Y_51305482110 = X_TKFTEB01 + totaLSerialInterfaceModbusIOMs + half_CCTCF901 if (AvgCableLength == '10m' or AvgCableLength == '') else 0
	Y_51305482210 = X_TKFTEB01 + half_CCTCF901 if (AvgCableLength == '10m' or AvgCableLength == '') else 0
	Y_51305482120 = X_TKFTEB01 + totaLSerialInterfaceModbusIOMs + half_CCTCF901 if (AvgCableLength == '20m') else 0
	Y_51305482220 = X_TKFTEB01 + half_CCTCF901 if (AvgCableLength == '20m') else 0
	
	#Cabinet Deduction Calculation
	pairOfLocateSepStd = math.floor(float(noOfLocatSep_C8DS01)/2)
	pairOfLocateSepNonStd = math.floor(float(noOfLocatSep_CBDD01)/2)
	Y_CCC8DS01 -= pairOfLocateSepStd
	Y_CCCBDD01 -= pairOfLocateSepNonStd   

	Trace.Write('C200 to C300 Test')
	#UHIO
	attrValDict['X_CCZHR042'] = X_CCZHR042
	attrValDict['X_CCZHR041'] = X_CCZHR041
	attrValDict['X_CCZHMT10'] = X_CCZHMT10
	attrValDict['X_CCZHER01'] = X_CCZHER01
	attrValDict['X_TCEPLX01'] = X_TCEPLX01
	attrValDict['X_TCCSUG50'] = X_TCCSUG50
	attrValDict['X_TSCSUG50'] = X_TSCSUG50
	attrValDict['X_51305980136'] = X_51305980136
	attrValDict['X_51305980236'] = X_51305980236
	attrValDict['X_51454475100'] = X_51454475100
	attrValDict['X_51202329722'] = X_51202329722
	attrValDict['X_51202329732'] = X_51202329732
	attrValDict['X_51202341112'] = X_51202341112

	#C300
	attrValDict['Y_CCSCMB05'] = Y_CCSCMB05
	attrValDict['Y_CCPCNT05'] = Y_CCPCNT05
	attrValDict['Y_CCTCNT01'] = Y_CCTCNT01
	attrValDict['Y_CCPCNT02'] = Y_CCPCNT02
	attrValDict['Y_TCSWCS30'] = Y_TCSWCS30
	attrValDict['Y_CCTCF901'] = Y_CCTCF901
	attrValDict['Y_CCPCF901'] = Y_CCPCF901
	attrValDict['Y_CCTFB412'] = Y_CCTFB412
	attrValDict['Y_CCTFB402'] = Y_CCTFB402
	attrValDict['Y_CCPFB401'] = Y_CCPFB401
	attrValDict['Y_CCTFB811'] = Y_CCTFB811
	attrValDict['Y_CCPFB801'] = Y_CCPFB801
	attrValDict['Y_51202329102'] = Y_51202329102
	attrValDict['Y_51202329302'] = Y_51202329302
	attrValDict['Y_51202329312'] = Y_51202329312
	attrValDict['Y_51305980184'] = Y_51305980184
	attrValDict['Y_51305980284'] = Y_51305980284
	attrValDict['Y_51305980836'] = Y_51305980836
	attrValDict['Y_CCSCMB02'] = Y_CCSCMB02
	attrValDict['Y_NEFWMB01'] = Y_NEFWMB01
	attrValDict['Y_NEFWMB12'] = Y_NEFWMB12
	attrValDict['Y_8937HN'] = Y_8937HN
	attrValDict['Y_8939HN'] = Y_8939HN
	attrValDict['Y_CCKFPGR5'] = Y_CCKFPGR5
	attrValDict['Y_CCKFPVR5'] = Y_CCKFPVR5
	attrValDict['Y_51305482102'] = Y_51305482102
	attrValDict['Y_51305482202'] = Y_51305482202
	attrValDict['Y_51305482105'] = Y_51305482105
	attrValDict['Y_51305482205'] = Y_51305482205
	attrValDict['Y_51305482110'] = Y_51305482110
	attrValDict['Y_51305482210'] = Y_51305482210
	attrValDict['Y_51305482120'] = Y_51305482120
	attrValDict['Y_51305482220'] = Y_51305482220
	attrValDict['Y_TKFXX102'] = Y_TKFXX102
	attrValDict['Y_TKFPCXX2'] = Y_TKFPCXX2
	attrValDict['Y_TCXXXXX2'] = Y_TCXXXXX2
	attrValDict['Y_CC_MCAR01'] = Y_CC_MCAR01
	attrValDict['Y_51202335300'] = Y_51202335300
	attrValDict['Y_CCC8DS01'] = Y_CCC8DS01
	attrValDict['Y_CCC8SS01'] = Y_CCC8SS01
	attrValDict['Y_CCCBDD01'] = Y_CCCBDD01
	attrValDict['Y_CCCBDS01'] = Y_CCCBDS01
	attrValDict['Y_51199947175'] = Y_51199947175
	attrValDict['Y_51199947275'] = Y_51199947275
	attrValDict['Y_51199406200'] = Y_51199406200
	#attrValDict['Y_CCPWRB01'] = Y_CCPWRB01
	'''Changes done by RP: CXCPQ-91893'''
	attrValDict['Y_CCPEIM01'] = Y_CCPEIM01
	attrValDict['Y_CCTEIM01'] = Y_CCTEIM01
	
	#powersystem
	attrValDict['Y_CU_PWMR20'] = Y_CU_PWMR20
	attrValDict['Y_CU_PWMN20'] = Y_CU_PWMN20
	attrValDict['Y_CU_PWPR21'] = Y_CU_PWPR21
	attrValDict['Y_CU_PWPN21'] = Y_CU_PWPN21
	attrValDict['Y_CC_PWRR01'] = Y_CC_PWRR01
	attrValDict['Y_CC_PWRN01'] = Y_CC_PWRN01
	attrValDict['Y_CC_PWRB01'] = Y_CC_PWRB01
	attrValDict['Y_CC_PWR401'] = Y_CC_PWR401
	attrValDict['Y_CC_PWN401'] = Y_CC_PWN401

	"""if (FIM2Points == 0) and (UHOCondition <= 64) and ((X_TKFTEB01 <= 7 and (controllerRedundancy == 'Redundant' or controllerRedundancy == '')) or (X_TKFTEB01 <= 6 and (controllerRedundancy == 'Non Redundant'))) and (cabinetTypeCustomerPlans != 'New Front Access Only Series C Cabinet' or cabinetTypeCustomerPlans != 'New Front & Rear Access Series C Cabinet'):
		Trace.Write('Yes' )
	else:
		Trace.Write('No')"""
	if(FTEswitch == 'EightPortCISCOSwitch'):
		Z_SI3300I2 = math.ceil(((Y_NEFWMB01+Y_NEFWMB12) / 8 + X_CCZHR041 / 8 + Y_CCTCF901 / 16) * 2)
		Z_51305786_502 = math.ceil(Z_SI3300I2/2)
	elif(FTEswitch == 'EightPortCISCOSplitSwitch'):
		Z_SI3300I2 = math.ceil(((Y_NEFWMB01+Y_NEFWMB12) / 8 + X_CCZHR041 / 6 + Y_CCTCF901 / 12) * 2)
		Z_51305786_502 = math.ceil(Z_SI3300I2 / 2 * 3)
	elif(FTEswitch == 'TwentyFourSTPPortCISCOSwitch'):
		Z_SI920LN4 = math.ceil(((Y_NEFWMB01+Y_NEFWMB12) /24 + X_CCZHR041 / 12 + Y_CCTCF901 / 24) * 2)
		Z_51305786_502 = math.ceil(Z_SI920LN4/2)
	elif(FTEswitch == 'TwentyFourSTPPortCISCOSplitSwitch'):
		Z_SI920LN4 = math.ceil(((Y_NEFWMB01+Y_NEFWMB12) /24 + X_CCZHR041 / 11 + Y_CCTCF901 / 22) * 2)
		Z_51305786_502 = math.ceil(Z_SI920LN4/2*3)
	elif(FTEswitch == 'TwentyFourSTPPortCISCOGBSwitch'):
		Z_SI930LN4 = math.ceil(((Y_NEFWMB01+Y_NEFWMB12) /24 +X_CCZHR041 / 12 + Y_CCTCF901 / 24) * 2)
		Z_51305786_502 = math.ceil(Z_SI930LN4 / 2)
	elif(FTEswitch == 'TwentyFourSTPPortCISCOGBSplitSwitch'):  
		Z_SI930LN4 = math.ceil(((Y_NEFWMB01+Y_NEFWMB12) /24 + X_CCZHR041 / 11 + Y_CCTCF901 / 22) * 2)
		Z_51305786_502 = math.ceil(Z_SI930LN4 / 2*3)
	elif(FTEswitch == 'FortyEightSTPPortCISCOSwitch'):
		Z_SI920LN8 = math.ceil(((Y_NEFWMB01+Y_NEFWMB12) /48 +X_CCZHR041 / 24 + Y_CCTCF901 / 48) * 2)
		Z_51305786_502 = math.ceil(Z_SI920LN8 / 2)
	elif(FTEswitch == 'FortyEightSTPPortCISCOSplitSwitch'):
		Z_SI920LN8 = math.ceil(((Y_NEFWMB01+Y_NEFWMB12) /48 + X_CCZHR041 / 23 + Y_CCTCF901 / 46) * 2)
		Z_51305786_502 = math.ceil(Z_SI920LN8 / 2*3)
	elif(FTEswitch == 'FortyEightSTPPortCISCONonRoutableGBSwitch'):
		Z_SI920LN8 = math.ceil(((Y_NEFWMB01+Y_NEFWMB12) /48 + X_CCZHR041 / 24 + Y_CCTCF901 / 48) * 2)
		Z_51305786_502 = math.ceil(Z_SI920LN8 / 2)
	elif(FTEswitch == 'FortyEightSTPPortCISCONonRoutableGBSplitSwitch'):
		Z_SI920LN8 =  math.ceil(((Y_NEFWMB01+Y_NEFWMB12) /48 + X_CCZHR041 / 23 + Y_CCTCF901 / 46) * 2)
		Z_51305786_502 = math.ceil(Z_SI920LN8 / 2*3)

	Z_51199562_200 = Z_SI3300I2 + Z_SI920LN4 + Z_SI930LN4 + Z_SI920LN8

	attrValDict['Z_SI3300I2'] = Z_SI3300I2
	attrValDict['Z_SI920LN4'] = Z_SI920LN4
	attrValDict['Z_SI930LN4'] = Z_SI930LN4
	attrValDict['Z_SI920LN8'] = Z_SI920LN8
	attrValDict['Z_51199562_200'] = Z_51199562_200
	attrValDict['Z_51305786_502'] = Z_51305786_502
	
def populateWriteInsTPS(product):
	writeInData = dict()
	msid= product.Attr('MSID').GetValue()
	sysNumber= product.Attr('System Number').GetValue()
	area = str(msid) +" - "+ str(sysNumber)
	con = getContainer(product, "TPS_to_EX_3rd_Party_Items")

	i=1
	price = 0
	cost = 0
	extendedDesc  = 0
	for row in con.Rows:
		if(i == 1):
			price = str(row["Thin_Client_cables_and_adapters"] if row["Thin_Client_cables_and_adapters"] !='' else 0)
		elif(i == 2):
			cost = str(row["Thin_Client_cables_and_adapters"] if row["Thin_Client_cables_and_adapters"] !='' else 0)
		i+=1
		
		extendedDesc = "Thin Client cables and adapters"

	writeInData["Write-in Third Party Hardware Misc"] = [price,cost,extendedDesc,area]
	if (float(price) > 0  and float(cost) > 0):
		'''productContainer = product.GetContainerByName("MSID_Product_Container")
		productRow = productContainer.Rows.GetByColumnName("Product Name", "TPS to Experion")
		prod = productRow.Product'''
		con = product.GetContainerByName("WriteInProduct")
		if con.Rows.Count == 1:
			con.DeleteRow(0)
		for wi, wiData in writeInData.items():
				if con.Rows.Count == 0:
					row = con.AddNewRow()
				row.Product.Attr("Selected_WriteIn").AssignValue(wi)
				row.Product.Attr("Price").AssignValue(wiData[0])
				row.Product.Attr("Cost").AssignValue(wiData[1])
				row.Product.Attr("QI_Area").AssignValue(wiData[3])
				row.Product.Attr("ItemQuantity").AssignValue("1")
				row.Product.Attr("Extended Description").AssignValue(wiData[2])
				row.Product.ApplyRules()
				row.ApplyProductChanges()
				row.Calculate()
	elif(float(price) == 0  or float(cost) == 0):
		'''productContainer = product.GetContainerByName("MSID_Product_Container")
		productRow = productContainer.Rows.GetByColumnName("Product Name", "TPS to Experion")
		prod = productRow.Product'''
		con = product.GetContainerByName("WriteInProduct")
		con.DeleteRow(0)
	con.Calculate()

def populateWriteInsOPM(msidProduct):
	i = 0
	j= 0
	curr_exp_rel = ['R430.x','R431.x','R432.x','R500.x','R501.x','R510.x','R511.x','R41x.x','R43x.x']
	writeInData = dict()
	msid= msidProduct.Attr('MSID').GetValue()
	sysNumber= msidProduct.Attr('System Number').GetValue()
	area = str(msid) +" - "+ str(sysNumber)
	Trace.Write("--area---"+str(area))
	#con1 = getContainer(product, "MSID_CommonQuestions")
	#Trace.Write("--cont1---"+str(con1))
	#for row in con1.Rows:
	if msidProduct.Attr("MSID_Current_Experion_Release").GetValue() in curr_exp_rel:
		Trace.Write("--"+str(msidProduct.Attr("MSID_Current_Experion_Release").GetValue()))
		i = 1    
		Trace.Write("-i-"+str(i))
	
	con2 = getContainer(msidProduct, "OPM_Basic_Information")
	for row in con2.Rows:
		if (row["OPM_Is_this_is_a_Remote_Migration_Service_RMS"] == "No" and row["OPM_If_AMT_Will_Not_Be_Used"] != "Yes") or (row["OPM_Is_this_is_a_Remote_Migration_Service_RMS"] =="" and row["OPM_If_AMT_Will_Not_Be_Used"] != "Yes"):
			j = 1
		break
	scope = msidProduct.Attr("MIgration_Scope_Choices").GetValue()
	price = '0'
	cost = '0'
	extendedDesc  = 'Additional fee – not using AMT'
	writeInData["Write-in Site Support Labor"] = [price,cost,extendedDesc,area]
	Trace.Write("Write ---"+str(writeInData["Write-in Site Support Labor"]))
	#productContainer = product.GetContainerByName("MSID_Product_Container")
	#productRow = productContainer.Rows.GetByColumnName("Product Name", "OPM")
	prod = msidProduct
	con = prod.GetContainerByName("WriteInProduct")
	if i == 1 and j == 1 and scope != "HW/SW":
		Trace.Write("inside@")
		if con.Rows.Count == 1:
			con.DeleteRow(0)
		for wi, wiData in writeInData.items():
			if con.Rows.Count == 0:
				Trace.Write("-Writein cont")
				row = con.AddNewRow()
				row.Product.Attr("Selected_WriteIn").AssignValue(wi)
				row.Product.Attr("Price").AssignValue(wiData[0])
				row.Product.Attr("Cost").AssignValue(wiData[1])
				#row.Product.Attr("Area").AssignValue(wiData[3])
				row.Product.Attr("ItemQuantity").AssignValue("1")
				row.Product.Attr("Extended Description").AssignValue(wiData[2])
				row.Product.ApplyRules()
				row.ApplyProductChanges()
				row.Calculate()
	elif (i != 1 or j !=1 or scope == "HW/SW"):
		#productContainer = product.GetContainerByName("MSID_Product_Container")
		#productRow = productContainer.Rows.GetByColumnName("Product Name", "OPM")
		prod = msidProduct
		con = prod.GetContainerByName("WriteInProduct")
		con.DeleteRow(0)
	con.Calculate()
	
def populateWriteInsCDActuatorIFUpgrade(product):
	writeInData = dict()
	msid= product.Attr('MSID').GetValue()
	sysNumber= product.Attr('System Number').GetValue()
	area = str(msid) +" - "+ str(sysNumber)
	con = getContainer(product, "CD_Actuator_pricing_factory_cost")
	i=1
	price = 0
	cost = 0
	extendedDesc  = 0
	for row in con.Rows:
		if(i == 1):
			price = str(row["CD_Actuator_Special_Special_or_iLon_upgrade_pricing"] if row["CD_Actuator_Special_Special_or_iLon_upgrade_pricing"] !='' else 0)
		elif(i == 2):
			cost = str(row["CD_Actuator_Special_Special_or_iLon_upgrade_pricing"] if row["CD_Actuator_Special_Special_or_iLon_upgrade_pricing"] !='' else 0)
		elif(i == 3):
			extendedDesc = str(row["CD_Actuator_Special_Special_or_iLon_upgrade_pricing"])
		i+=1

	writeInData["Write-in Third Party Hardware Misc"] = [price,cost,extendedDesc,area]
	Trace.Write("CD AC writeIn {} :".format(writeInData))
	if (float(price) > 0  and float(cost) > 0):
		'''productContainer = product.GetContainerByName("MSID_Product_Container")
		productRow = productContainer.Rows.GetByColumnName("Product Name", "CD Actuator I-F Upgrade")
		prod = productRow.Product'''
		con = product.GetContainerByName("WriteInProduct")
		if con.Rows.Count == 1:
			con.DeleteRow(0)
		for wi, wiData in writeInData.items():
			if con.Rows.Count == 0:
				row = con.AddNewRow()
				row.Product.Attr("Selected_WriteIn").AssignValue(wi)
				row.Product.Attr("Price").AssignValue(wiData[0])
				row.Product.Attr("Cost").AssignValue(wiData[1])
				row.Product.Attr("QI_Area").AssignValue(wiData[3])
				row.Product.Attr("ItemQuantity").AssignValue("1")
				row.Product.Attr("Extended Description").AssignValue(wiData[2])
				row.Product.ApplyRules()
				row.ApplyProductChanges()
				row.Calculate()
	elif(float(price) == 0  or float(cost) == 0):
		'''productContainer = product.GetContainerByName("MSID_Product_Container")
		productRow = productContainer.Rows.GetByColumnName("Product Name", "CD Actuator I-F Upgrade")
		prod = productRow.Product'''
		con = product.GetContainerByName("WriteInProduct")
		con.DeleteRow(0)
	con.Calculate()