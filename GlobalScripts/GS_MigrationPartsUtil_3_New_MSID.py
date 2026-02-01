import math
def getContainer(prod, conName):
	return prod.GetContainerByName(conName)
def getFloat(Var):
	if Var:
		return float(Var)
	return 0

def updateAttrDictWithCustomxPMC300(product, attrValDict, Quote, parentProduct=None):
	con1 = getContainer(product, 'xPM_C300_Migration_Configuration_Cont')
	con2 = getContainer(product, 'xPM_C300_General_Qns_Cont')
	con3 = getContainer(product, 'xPM_C300_Series_ C_Cabinet_Configuration')
	con4 = getContainer(product, 'xPM_C300_Series_C_Cabinet_Configuration_FAOnly')
	if con2:
		FTEswitch = con2.Rows[0]['xPM_C300_FTE_switch']
		averagecablelength = con2.Rows[0]['xPM_C300_Average_Cable_Length']
		isRedundancy = con2.Rows[0]['xPM_C300_General_redundancy']
	else:
		FTEswitch = product.Attr('xPM_C300_FTE_switch').GetValue()
		averagecablelength = product.Attr('xPM_C300_Average_Cable_Length').GetValue()
		isRedundancy = product.Attr('xPM_C300_General_redundancy').GetValue()
	#Front & Rear Cabinet Declarition
	if con3:
		FRCabDoors = con3.Rows[0]['xPM_C300_Cabinet_Doors']
		FRCabHinType = con3.Rows[0]['xPM_C300_Cabinet_Hinge_Type']
		FRCabKeyLock = con3.Rows[0]['xPM_C300_Cabinet_Keylock_Type']
		FRCabColor = con3.Rows[0]['xPM_C300_Cabinet_Color']
		FRFanVolt = con3.Rows[0]['xPM_C300_Fan_Voltage']

		#Front & Rear Cabinet Power System Vendor and Type
		FRPowerVendor = con3.Rows[0]['xPM_C300_Power_System_Vendor']
		FRPowerType = con3.Rows[0]['xPM_C300_Power_System_Type']
	else:
		FRCabDoors = product.Attr('xPM_C300_Cabinet_Doors').GetValue()
		FRCabHinType = product.Attr('xPM_C300_Cabinet_Hinge_Type').GetValue()
		FRCabKeyLock = product.Attr('xPM_C300_Cabinet_Keylock_Type').GetValue()
		FRCabColor = product.Attr('xPM_C300_Cabinet_Color').GetValue()
		FRFanVolt = product.Attr('C200_C300_Fan_Voltage').GetValue()

		#Front & Rear Cabinet Power System Vendor and Type
		FRPowerVendor = product.Attr('Power System Vendor').GetValue()
		FRPowerType = product.Attr('Power System Type').GetValue()

	#Front Only Cabinet Declarition
	if con4:
		FCabDoors = con4.Rows[0]['xPM_C300_Cabinet_Doors_FAOnly']
		FCabHinType = con4.Rows[0]['xPM_C300_Cabinet_Hinge_Type_FAOnly']
		FCabKeyLock = con4.Rows[0]['xPM_C300_Cabinet_Keylock_Type_FAOnly']
		FCabColor = con4.Rows[0]['xPM_C300_Cabinet_Color_FAOnly']
		FFanVolt = con4.Rows[0]['xPM_C300_Fan_Voltage_FAOnly']

		#Front Only Power System Vendor and Type
		FCPowerVendor = con4.Rows[0]['xPM_C300_Power_System_Vendor']
		FCPowerType = con4.Rows[0]['xPM_C300_Power_System_Type']
	else:
		FCabDoors = product.Attr('C200_C300_Cabinet_Doors_FAO').GetValue()
		FCabHinType = product.Attr('ATT_xPMC300HNGTYP').GetValue()
		FCabKeyLock = product.Attr('ATT_xPMC300KEYTYP').GetValue()
		FCabColor = product.Attr('ATT_xPMC300CABCLR').GetValue()
		FFanVolt = product.Attr('ATT_C200C300FANV').GetValue()

		#Front Only Power System Vendor and Type
		FCPowerVendor = product.Attr('ATT_XPMC300PSV').GetValue()
		FCPowerType = product.Attr('ATT_XPMC300PST').GetValue()

	# SESP Type
	accountName = Quote.GetCustomField("Account Name").Content if Quote and Quote.GetCustomField("Account Name").Content else " "
	if parentProduct:
		getMSID = parentProduct.Attr('Migration_MSID_Choices').GetValue()
	else:
		getMSID = product.Attr('Migration_MSID_Choices').GetValue()
	sespType=''
	sespCurr = SqlHelper.GetFirst("Select * from MSID where SFDCIdentifier IS NOT NULL and MSID = '{}' and Account_Name='{}'" .format(getMSID,accountName))
	if sespCurr is not None:
		if sespCurr.Service_Product is not None:
			sespType= sespCurr.Service_Product
	#Scope
	if parentProduct:
		scope = parentProduct.Attr('MIgration_Scope_Choices').GetValue()
	else:
		scope = product.Attr('MIgration_Scope_Choices').GetValue()

	#UHIO
	CC_ZHR042 = 0
	CC_ZHR041 = 0
	CC_ZHMT10 = 0
	TC_CSUG50 = 0
	TS_CSUG50 = 0
	X51305980_136 = 0
	X51305980_236 = 0
	X51454475_100 = 0
	X51202329_722 = 0
	X51202329_302 = 0 #Available under UHIO and in New C300
	#UHIO+New c300 Controller
	NE_FWMB01 = 0
	NE_FWMB12 = 0
	MC_ZLLAI2 = 0
	MC_ZLLMF2 = 0
	MC_ZRHMF1 = 0
	MC_ZAIHF3 = 0
	MC_PAIH03 = 0
	MC_ZSTXF3 = 0
	MC_ZPSUG2 = 0
	MC_ZPSR04 = 0
	#New C300
	CC_SCMB05 = 0
	CC_PCNT05 = 0
	CC_TCNT01 = 0
	CC_PCNT02 = 0
	TC_SWCS30 = 0
	CC_TCF901 = 0
	CC_PCF901 = 0
	CC_TPIX11 = 0
	CC_PPIX01 = 0
	B51305980_184 = 0
	B51305980_284 = 0
	B51305980_836 = 0
	B51202329_102 = 0
	B51202329_302 = 0#Available in UHIO and C300
	B51202329_312 = 0
	B51202329_412 = 0
	B51202329_616 = 0
	CC_SCMB02 = 0
	MC_IOLX02 = 0
	B8937_HN = 0
	B8939_HN = 0
	CC_KFPGR5 = 0
	CC_MCAR01 = 0
	X51202335_300 = 0
	CC_C8DS01 = 0
	CC_C8SS01 = 0
	CC_CBDD01 = 0
	CC_CBDS01 = 0
	X51199947_175 = 0
	X51199947_275 = 0
	X51199406_200 = 0
	CC_PWRB01 = 0

	#Per Upgrade
	EP_DPR10K = 0
	EP_DPR05K = 0
	EP_DPR02K = 0
	EP_DPR01K = 0
	EP_DPR100 = 0

	EP_DSC10K = 0
	EP_DSC05K = 0
	EP_DSC02K = 0
	EP_DSC01K = 0
	EP_DSC100 = 0

	TC_PCDX50 = 0
	TC_PCDX10 = 0
	TC_PCDX05 = 0
	TC_PCDX01 = 0
	SI_3300I2 = 0
	SI_920LN4 = 0
	SI_930LN4 = 0
	SI_920LN8 = 0
	B51305786_502 = 0
	B51199562_200 = 0

	B51305482_102 = 0
	B51305482_202 = 0
	B51305482_105 = 0
	B51305482_205 = 0
	B51305482_110 = 0
	B51305482_210 = 0
	B51305482_120 = 0
	B51305482_220 = 0

	#Power System
	CU_PWMR20 = 0
	CU_PWMN20 = 0
	CU_PWPR21 = 0
	CU_PWPN21 = 0
	CC_PWRR01 = 0
	CC_PWRN01 = 0
	CC_PWRB01_1 = 0
	CC_PWR401 = 0
	CC_PWN401 = 0

	#Per Upgrade Declarition
	#NumberofXpmpoints = 0
	TotalNumberofXpmpoints = 0
	totalSerialInterfacePointsScada = 0
	totalDevicestoxPMSIforPCDI = 0

	#Cabinet Deduction Declarition
	noOfLocatSep_C8DS01 = 0
	noOfLocatSep_CBDD01 = 0
	CQcon = getContainer(product, 'MSID_CommonQuestions')
	if CQcon:
		for row in CQcon.Rows:
			epks_rel = row["MSID_Future_Experion_Release"]
			break
	else:
		epks_rel = product.Attr("MSID_Future_Experion_Release").GetValue()

	for row in con1.Rows:
		typeofXpm = row['xPM_C300_Type_of_xPM']
		spaceinthexpmcabinet = row['xPM_C300_space_in_the_existing_xPM_cabinet']
		numberofpulseinputIOMs = getFloat(row['xPM_C300_Number_of_Pulse_Input_IOMs'])
		controllerRedundancy = row['xPM_C300_Controller_Redundancy']
		numberofPMIOMs = getFloat(row['xPM_C300_Number_of_xPM_IOMs'])
		cabinettypeneeded = row['xPM_C300_Cabinet_type_if_new_cabinet_needed']
		#serialinterface = getFloat(row['xPM_C300_Number_of_Serial_Interface_modules']) 
		serialinterface = getFloat(row['xPM_C300_Number_of_Serial_Interface_Modbus_IOMs'])
		locateSeparate = row['xPM_C300_located_separated_from_remote_location']
		AnalogInputpoints = getFloat(row['xPM_C300_Number_of_xPM_Analog_Input_points'])
		AnalogOutputpoints = getFloat(row['xPM_C300_Number_of_xPM_Analog_Output_points'])
		DigitalInputPoints = getFloat(row['xPM_C300_Number_of_xPM_Digital_Input_points'])
		DigitalOutputPoints = getFloat(row['xPM_C300_Number_of_xPM_Digital_output_points'])
		SerialInterfacePointsScada = getFloat(row['xPM_C300_Number_of_Serial_Interface_points_for_Scada_conversion'])
		devicestoxPMSIforPCDI = getFloat(row['xPM_C300_Number_of_devices_connected_to_xPM_SI_for_PCDI_conversion'])
		ModbusFirewall = row['xPM_C300_Required_Modbus_Firewall']
		numberofLLAI6_0 = getFloat(row['xPM_C300_Number_of_LLAI_with_FW_Rev_less_than_6.0'])
		numberofLLMUX4_1 = getFloat(row['xPM_C300_Number_of_LLMUX_with_FW_Rev_less_than_4.1'])
		numberofRHMUX6_0 = getFloat(row['xPM_C300_Number_of_RHMUX_with_FW_Rev_less_than_6.0'])
		numberofHLAI3_4 = getFloat(row['xPM_C300_Number_of_HLAI_with_FW_Rev_bet_3.4_and_6.0'])
		numberofHLAI3_3 = getFloat(row['xPM_C300_Number_of_HLAI_with_FW_Rev_GEQ_3.3'])
		numberofSTIMV6_0 = getFloat(row['xPM_C300_Number_of_STI_MV_with_FW_Rev_less_than_6.0'])
		powersupplyupgrade = row['xPM_C300_Power_Supply_Upgrade_Needed']
		powersystemupgrade = row['xPM_C300_Power_System_Upgrade_Needed']
		ModbusAllenBradley = getFloat(row['xPM_C300_Number_of_SI_Modbus_and_Allen_Bradley_Rockwell_Array_points_for_PCDI_conversion'])
		#UHIO Kit
		if(spaceinthexpmcabinet == 'Yes' or  spaceinthexpmcabinet == '') and (numberofpulseinputIOMs == 0):
			if epks_rel in ["R520","R530"]:
				CC_ZHR042 += 1
			else:
				CC_ZHR041 += 1
			CC_ZHMT10 += 1
			if sespType in ("No","SESP Support Flex", ""):
				TC_CSUG50 += 1
			elif sespType in ("SESP Value Plus","SESP Value Plus Connected","SESP Value Remote Plus", "SESP Software Flex"):
				TS_CSUG50 += 1

			X51305980_136 += 1 * 2
			X51305980_236 += 1 * 2
			X51454475_100 += 1
			X51202329_722 += 1
			X51202329_302 += 1

		#New C300 Controller
		else:
			currentCC_TCNT01 = 0.0
			currentCC_SCMB02 = 0.0
			currentCC_TCF901 = 0.0
			currentMountQty  = 0.0
			currentCC_MCAR01 = 0.0
			currentCabSides  = 0.0
			if (controllerRedundancy == 'Redundant' or controllerRedundancy == '') and scope != "LABOR":
				currentCC_TCNT01 = float(2)
				CC_TCNT01 += currentCC_TCNT01
				B51305980_836 += 1
				TC_SWCS30 += currentCC_TCNT01/2
			elif(controllerRedundancy == 'Non Redundant'):
				currentCC_TCNT01 = float(1)
				CC_TCNT01 += currentCC_TCNT01
				TC_SWCS30 += currentCC_TCNT01
			if epks_rel in ["R520","R530"]:
				CC_PCNT05 += currentCC_TCNT01
			else:
				CC_PCNT02 += currentCC_TCNT01
			currentCC_TCF901= math.ceil(currentCC_TCNT01/ 2) * 2
			if epks_rel not in ["R520","R530"]:
				CC_TCF901 += currentCC_TCF901
				CC_PCF901 += currentCC_TCF901
			CC_TPIX11 += numberofpulseinputIOMs
			CC_PPIX01 += numberofpulseinputIOMs * 2
			B51305980_184 += currentCC_TCNT01
			B51305980_284 += currentCC_TCNT01

			if(numberofPMIOMs > 0):
				B51202329_102 += 1
				B51202329_302 += 1
			if(numberofpulseinputIOMs > 0):
				B51202329_312 += 1
				B51202329_616 += 1
			currentB51202329_412 = math.floor(numberofpulseinputIOMs/3)
			B51202329_412 += currentB51202329_412

			MC_IOLX02 += 1
			B8937_HN += 2
			B8939_HN += 2
			CC_KFPGR5 += 1
			#Mounting Unit Calculation
			currentCC_SCMB02 = math.ceil(currentCC_TCNT01/4)
			if currentCC_TCNT01 > 0:
				currentMountQty = 8 + 3*currentCC_TCNT01 + currentCC_SCMB02 + 2*currentCC_TCF901 + 2*2 + 2*2 + 4*numberofpulseinputIOMs
 				#Cabinet Sides Calculation
 				currentCC_MCAR01 = math.ceil(currentMountQty/12.0)
 				currentCabSides = math.ceil(currentCC_MCAR01/6.0)

			#Cabinet Calculation - Front and Rear Access
			if cabinettypeneeded == 'Front & Rear Access' and scope != "LABOR":
				if(FRCabDoors == 'Standard' or FRCabDoors == '') and (FRCabHinType == '130 Degrees' or FRCabHinType == '') and (FRCabKeyLock == 'Standard' or FRCabKeyLock == '') and (FRCabColor == 'Gray-RAL7035' or FRCabColor == ''):
					current_C8DS01 = math.ceil(currentCabSides/2.0)
					CC_C8DS01 += current_C8DS01
					#Cabinet Deduction Preparation
					if(current_C8DS01 > 0 and (locateSeparate=='No' or locateSeparate =='') and currentCabSides == 1):
						noOfLocatSep_C8DS01 += 1
				else:
					current_CBDD01 = math.ceil(currentCabSides/2.0)
					CC_CBDD01 += current_CBDD01
					#Cabinet Deduction Preparation
					if(current_CBDD01>0 and (locateSeparate=='No' or locateSeparate =='') and currentCabSides==1):
						noOfLocatSep_CBDD01 += 1

				#Fan calculation
				if (FRFanVolt =='115VAC' or FRFanVolt ==''):
					X51199947_175 += currentCabSides
				else:
					X51199947_275 += currentCabSides

				#Power Supply Calculation
				if (FRPowerVendor == 'Meanwell' or FRPowerVendor == '') and (FRPowerType == 'Redundant 20A' or FRPowerType == ''):
					CU_PWMR20 = 1
				elif (FRPowerVendor == 'Meanwell' or FRPowerVendor == '') and (FRPowerType == 'Non Redundant 20A'):
					CU_PWMN20 = 1
				elif (FRPowerVendor == 'Phoenix Contact' and FRPowerType == 'Redundant 20A'):
					CU_PWPR21 = 1
				elif (FRPowerVendor == 'Phoenix Contact' and FRPowerType == 'Non Redundant 20A'):
					CU_PWPN21 = 1
				elif (FRPowerVendor == 'TDI' and FRPowerType == 'Redundant 20A'):
					CC_PWRR01 = 1
				elif (FRPowerVendor == 'TDI' and FRPowerType == 'Non Redundant 20A'):
					CC_PWRN01 = 1
				elif (FRPowerVendor == 'TDI' and FRPowerType == 'Redundant with BBU 20A'):
					CC_PWRB01_1 = 1
				elif (FRPowerVendor == 'TDI' and FRPowerType == 'Redundant 40A'):
					CC_PWR401 = 1
				elif (FRPowerVendor == 'TDI' and FRPowerType == 'Non Redundant 40A'):
					CC_PWN401 = 1
			#Cabinet Calculation - Front only Access
			elif (cabinettypeneeded == 'Front Access Only' or cabinettypeneeded == '') and scope != "LABOR":
				if(FCabDoors == 'Standard' or FCabDoors == '') and (FCabHinType == '130 Degrees' or FCabHinType == '') and (FCabKeyLock == 'Standard' or FCabKeyLock == '') and (FCabColor == 'Gray-RAL7035' or FCabColor == ''):
					CC_C8SS01 += currentCabSides
				else:
					CC_CBDS01 += currentCabSides
				#Fan calculation
				if (FFanVolt =='115VAC' or FFanVolt ==''):
					X51199947_175 += currentCabSides
				else:
					X51199947_275 += currentCabSides

				#Power Supply Calculation
				if (FCPowerVendor == 'Meanwell' or FCPowerVendor == '') and (FCPowerType == 'Redundant 20A' or FCPowerType == ''):
					CU_PWMR20 = 1
				elif (FCPowerVendor == 'Meanwell' or FCPowerVendor == '') and (FCPowerType == 'Non Redundant 20A'):
					CU_PWMN20 = 1
				elif (FCPowerVendor == 'Phoenix Contact' and FCPowerType == 'Redundant 20A'):
					CU_PWPR21 = 1
				elif (FCPowerVendor == 'Phoenix Contact' and FCPowerType == 'Non Redundant 20A'):
					CU_PWPN21 = 1
				elif (FCPowerVendor == 'TDI' and FCPowerType == 'Redundant 20A'):
					CC_PWRR01 = 1
				elif (FCPowerVendor == 'TDI' and FCPowerType == 'Non Redundant 20A'):
					CC_PWRN01 = 1
				elif (FCPowerVendor == 'TDI' and FCPowerType == 'Redundant with BBU 20A'):
					CC_PWRB01_1 = 1
				elif (FCPowerVendor == 'TDI' and FCPowerType == 'Redundant 40A'):
					CC_PWR401 = 1
				elif (FCPowerVendor == 'TDI' and FCPowerType == 'Non Redundant 40A'):
					CC_PWN401 = 1
			if epks_rel in ["R520","R530"]:
				CC_SCMB05 += currentCC_SCMB02
			else:
				CC_SCMB02 += currentCC_SCMB02
			CC_MCAR01 += currentCC_MCAR01
			X51202335_300 += math.floor(currentCC_MCAR01/3) 
			X51199406_200 += currentCabSides
			#CC_PWRB01 += currentCabSides #refer to CCEECOMMBR-6205 ticket

		#Common models for UHIO Kit and New C300 Controller
		if(ModbusFirewall == 'Read-Write' or ModbusFirewall == '') and scope != "LABOR":
			NE_FWMB01 += 1 * serialinterface
		elif(ModbusFirewall == 'Read-Only'):
			NE_FWMB12 += 1 * serialinterface

		MC_ZLLAI2 += numberofLLAI6_0
		MC_ZLLMF2 += numberofLLMUX4_1
		MC_ZRHMF1 += numberofRHMUX6_0
		MC_ZAIHF3 += numberofHLAI3_4
		MC_PAIH03 += numberofHLAI3_3
		MC_ZSTXF3 += numberofSTIMV6_0

		if(powersupplyupgrade == 'Yes'):#or powersupplyupgrade == ''
			MC_ZPSUG2 += 1
		if(powersystemupgrade == 'Yes'):#or powersystemupgrade == ''
			MC_ZPSR04 += 1

		#Preparation for Total Number of xPM Points(including SI) Calculation
		#NumberofXpmpoints = (AnalogInputpoints + AnalogOutputpoints + DigitalInputPoints + DigitalOutputPoints + SerialInterfacePointsScada)
		NumberofXpmpoints = (AnalogInputpoints + AnalogOutputpoints + DigitalInputPoints + DigitalOutputPoints + ModbusAllenBradley)
		totalSerialInterfacePointsScada += SerialInterfacePointsScada
		totalDevicestoxPMSIforPCDI += devicestoxPMSIforPCDI
		if sespType in ("No","SESP Support Flex", ""):
			TotalNumberofXpmpoints += NumberofXpmpoints
		elif sespType in ("SESP Value Plus","SESP Value Plus Connected","SESP Value Remote Plus", "SESP Software Flex"):
			if scope != "LABOR":
				if typeofXpm !="HPM":
					XpmPoints = NumberofXpmpoints - 1000 if NumberofXpmpoints >1000 else 0
				else:
					XpmPoints = NumberofXpmpoints - 2200 if NumberofXpmpoints >2200 else 0

			TotalNumberofXpmpoints += XpmPoints

	#Cabinet Deduction Calculation
	pairOfLocateSepStd = math.floor(float(noOfLocatSep_C8DS01)/2)
	pairOfLocateSepNonStd = math.floor(float(noOfLocatSep_CBDD01)/2)
	CC_C8DS01 -= pairOfLocateSepStd
	CC_CBDD01 -= pairOfLocateSepNonStd

	#Per Upgrade Calculation
	if 9900<TotalNumberofXpmpoints<= 10000:
		EP_DPR10K = 1
	else:
		EP_DPR10K = math.floor(TotalNumberofXpmpoints/10000)
		if 4900 < TotalNumberofXpmpoints<=5000 or 4900 < (TotalNumberofXpmpoints -EP_DPR10K*10000)<=5000:
			EP_DPR05K =1
		else:
			EP_DPR05K = math.floor((TotalNumberofXpmpoints -EP_DPR10K*10000)/5000)
			if 3900 < TotalNumberofXpmpoints<=4000 or 3900 < (TotalNumberofXpmpoints-EP_DPR10K*10000-EP_DPR05K*5000)<=4000:
				EP_DPR02K =2
			elif 1900 < TotalNumberofXpmpoints<=2000 or 1900 < (TotalNumberofXpmpoints-EP_DPR10K*10000-EP_DPR05K*5000)<=2000:
				EP_DPR02K =1
			else:
				EP_DPR02K += math.floor((TotalNumberofXpmpoints-EP_DPR10K*10000-EP_DPR05K*5000)/2000)
				if 900 < TotalNumberofXpmpoints<=1000 or 900 < (TotalNumberofXpmpoints-EP_DPR10K*10000-EP_DPR05K*5000-EP_DPR02K*2000)<=1000 :
					EP_DPR01K =1
				else:
					EP_DPR01K = math.floor((TotalNumberofXpmpoints-EP_DPR10K*10000-EP_DPR05K*5000-EP_DPR02K*2000)/1000)
					EP_DPR100 = math.ceil((TotalNumberofXpmpoints-EP_DPR10K*10000-EP_DPR05K*5000-EP_DPR02K*2000-EP_DPR01K*1000)/100)

	EP_DSC10K = math.floor(totalSerialInterfacePointsScada/10000)
	EP_DSC05K = math.floor((totalSerialInterfacePointsScada - EP_DSC10K*10000)/5000)
	EP_DSC02K = math.floor((totalSerialInterfacePointsScada - EP_DSC05K*5000 - EP_DSC10K*10000)/2000)
	EP_DSC01K = math.floor((totalSerialInterfacePointsScada - EP_DSC02K*2000 - EP_DSC05K*5000 - EP_DSC10K*10000)/1000)
	EP_DSC100 = math.ceil((totalSerialInterfacePointsScada - EP_DSC01K*1000 - EP_DSC02K*2000 - EP_DSC05K*5000 - EP_DSC10K*10000)/100)

	TC_PCDX50 = math.floor(totalDevicestoxPMSIforPCDI/50)
	TC_PCDX10 = math.floor((totalDevicestoxPMSIforPCDI - TC_PCDX50*50)/10)
	TC_PCDX05 = math.floor((totalDevicestoxPMSIforPCDI - TC_PCDX50*50 - TC_PCDX10*10)/5)
	TC_PCDX01 = math.floor((totalDevicestoxPMSIforPCDI - TC_PCDX50*50 - TC_PCDX10*10 - TC_PCDX05*5))

	if(FTEswitch == 'EightPortCISCOSwitch'):
		SI_3300I2 = math.ceil(((NE_FWMB01+NE_FWMB12) / 8 + CC_ZHR041 / 8 + CC_TCF901 / 16))* 2
		B51305786_502 = SI_3300I2/2
	elif(FTEswitch == 'EightPortCISCOSplitSwitch'):
		SI_3300I2 = math.ceil(((NE_FWMB01+NE_FWMB12) / 8 + CC_ZHR041 / 6 + CC_TCF901 / 12))* 2
		B51305786_502 = SI_3300I2 / 2 * 3
	elif(FTEswitch == 'TwentyFourSTPPortCISCOSwitch'):
		SI_920LN4 = math.ceil(((NE_FWMB01+NE_FWMB12) /24 + CC_ZHR041 / 12 + CC_TCF901 / 24))* 2
		B51305786_502 = SI_920LN4/2
	elif(FTEswitch == 'TwentyFourSTPPortCISCOSplitSwitch'):
		SI_920LN4 = math.ceil(((NE_FWMB01+NE_FWMB12) /24 + CC_ZHR041 / 11 + CC_TCF901 / 22))* 2
		B51305786_502 = SI_920LN4/2*3
	elif(FTEswitch == 'TwentyFourSTPPortCISCOGBSwitch'):
		SI_930LN4 = math.ceil(((NE_FWMB01+NE_FWMB12) /24 +CC_ZHR041 / 12 + CC_TCF901 / 24))* 2
		B51305786_502 = SI_930LN4 / 2
	elif(FTEswitch == 'TwentyFourSTPPortCISCOGBSplitSwitch'):  
		SI_930LN4 = math.ceil(((NE_FWMB01+NE_FWMB12) /24 + CC_ZHR041 / 11 + CC_TCF901 / 22))* 2
		B51305786_502 = SI_930LN4 / 2*3
	elif(FTEswitch == 'FortyEightSTPPortCISCOSwitch'):
		SI_920LN8 = math.ceil(((NE_FWMB01+NE_FWMB12) /48 +CC_ZHR041 / 24 + CC_TCF901 / 48))* 2
		B51305786_502 = SI_920LN8 / 2
	elif(FTEswitch == 'FortyEightSTPPortCISCOSplitSwitch'):
		SI_920LN8 = math.ceil(((NE_FWMB01+NE_FWMB12) /48 + CC_ZHR041 / 23 + CC_TCF901 / 46))* 2
		B51305786_502 = SI_920LN8 / 2*3
	elif(FTEswitch == 'FortyEightSTPPortCISCONonRoutableGBSwitch'):
		SI_920LN8 = math.ceil(((NE_FWMB01+NE_FWMB12) /48 + CC_ZHR041 / 24 + CC_TCF901 / 48))* 2
		B51305786_502 = SI_920LN8 / 2
	if(FTEswitch == 'FortyEightSTPPortCISCONonRoutableGBSplitSwitch'):
		SI_920LN8 =  math.ceil(((NE_FWMB01+NE_FWMB12) /48 + CC_ZHR041 / 23 + CC_TCF901 / 46))* 2
		B51305786_502 = SI_920LN8 / 2*3

	B51199562_200 = SI_3300I2 + SI_920LN4 + SI_930LN4 + SI_920LN8

	if(averagecablelength == '2m'):
		B51305482_102 = NE_FWMB01+NE_FWMB12 + CC_ZHR041 + (CC_TCF901 / 2)
		B51305482_202 = CC_ZHR041 + (CC_TCF901 / 2)
	elif(averagecablelength == '5m'):
		B51305482_105 = NE_FWMB01+NE_FWMB12 + CC_ZHR041 + (CC_TCF901 / 2)
		B51305482_205 = CC_ZHR041 + (CC_TCF901 / 2)
	elif((averagecablelength == '10m' or averagecablelength == '') and scope != "LABOR"):
		B51305482_110 = NE_FWMB01+NE_FWMB12 + CC_ZHR041 + (CC_TCF901 / 2)
		B51305482_210 = CC_ZHR041 + (CC_TCF901 / 2) 
	elif(averagecablelength == '20m'):
		B51305482_120 = NE_FWMB01+NE_FWMB12 + CC_ZHR041 + (CC_TCF901 / 2)
		B51305482_220 = CC_ZHR041 + (CC_TCF901 / 2)
	#UHIO
	attrValDict["CC_ZHR042"] = CC_ZHR042
	attrValDict["CC-ZHR041"] = CC_ZHR041
	attrValDict["CC-ZHMT10"] = CC_ZHMT10
	attrValDict["TC-SWCS30"] = TC_SWCS30
	attrValDict["TC-CSUG50"] = TC_CSUG50
	attrValDict["TS-CSUG50"] = TS_CSUG50
	attrValDict["51305980-136"] = X51305980_136
	attrValDict["51305980-236"] = X51305980_236
	attrValDict["51454475-100"] = X51454475_100
	attrValDict["51202329-722"] = X51202329_722
	#attrValDict["51202329-302"] = X51202329_302
	#New C300
	attrValDict["CC_SCMB05"] = CC_SCMB05
	attrValDict["CC_PCNT05"] = CC_PCNT05
	attrValDict["CC-TCNT01"] = CC_TCNT01
	attrValDict["CC-PCNT02"] = CC_PCNT02
	attrValDict["TC-SWCS30"] = TC_SWCS30
	attrValDict["CC-TCF901"] = CC_TCF901
	attrValDict["CC-PCF901"] = CC_PCF901
	attrValDict["CC-TPIX11"] = CC_TPIX11
	attrValDict["CC-PPIX01"] = CC_PPIX01
	attrValDict["51305980-184"] = B51305980_184
	attrValDict["51305980-284"] = B51305980_284
	attrValDict["51305980-836"] = B51305980_836
	attrValDict["51202329-102"] = B51202329_102
	attrValDict["51202329-302"] = B51202329_302 + X51202329_302# Same part under UHIO and C300, need to add together
	attrValDict["51202329-312"] = B51202329_312
	attrValDict["51202329-412"] = B51202329_412
	attrValDict["51202329-616"] = B51202329_616
	attrValDict["CC-SCMB02"] = CC_SCMB02
	attrValDict["MC-IOLX02"] = MC_IOLX02
	attrValDict["8937-HN"] = B8937_HN
	attrValDict["8939-HN"] = B8939_HN
	attrValDict["CC-KFPGR5"] = CC_KFPGR5
	attrValDict["CC-MCAR01"] = CC_MCAR01
	attrValDict["51202335-300"] = X51202335_300
	attrValDict["CC-C8DS01"] = CC_C8DS01
	attrValDict["CC-C8SS01"] = CC_C8SS01
	attrValDict["CC-CBDD01"] = CC_CBDD01
	attrValDict["CC-CBDS01"] = CC_CBDS01
	Crate_BOM_XPMC300=CC_C8DS01+CC_C8SS01+CC_CBDD01+CC_CBDS01
	attrValDict["Crate_BOM_XPMC300"] = Crate_BOM_XPMC300
	attrValDict["51199947-175"] = X51199947_175
	attrValDict["51199947-275"] = X51199947_275
	attrValDict["51199406-200"] = X51199406_200
	#attrValDict["CC-PWRB01"] = CC_PWRB01
	#UHIO+New c300 Controller
	attrValDict["NE-FWMB01"] = NE_FWMB01
	attrValDict["NE-FWMB12"] = NE_FWMB12
	attrValDict["MC-ZLLAI2"] = MC_ZLLAI2
	attrValDict["MC-ZLLMF2"] = MC_ZLLMF2
	attrValDict["MC-ZRHMF1"] = MC_ZRHMF1
	attrValDict["MC-ZAIHF3"] = MC_ZAIHF3
	attrValDict["MC-PAIH03"] = MC_PAIH03
	attrValDict["MC-ZSTXF3"] = MC_ZSTXF3
	attrValDict["MC-ZPSUG2"] = MC_ZPSUG2
	attrValDict["MC-ZPSR04"] = MC_ZPSR04
	#Per Upgrade
	attrValDict["EP-DPR10K"] = EP_DPR10K
	attrValDict["EP-DPR05K"] = EP_DPR05K
	attrValDict["EP-DPR02K"] = EP_DPR02K
	attrValDict["EP-DPR01K"] = EP_DPR01K
	attrValDict["EP-DPR100"] = EP_DPR100
	if isRedundancy == "Redundant":
		attrValDict["EP-RPR100"] = EP_DPR100
		attrValDict["EP-RPR01K"] = EP_DPR01K
		attrValDict["EP-RPR02K"] = EP_DPR02K
		attrValDict["EP-RPR05K"] = EP_DPR05K
		attrValDict["EP-RPR10K"] = EP_DPR10K

	attrValDict["EP-DSC10K"] = EP_DSC10K
	attrValDict["EP-DSC05K"] = EP_DSC05K
	attrValDict["EP-DSC02K"] = EP_DSC02K
	attrValDict["EP-DSC01K"] = EP_DSC01K
	attrValDict["EP-DSC100"] = EP_DSC100
	attrValDict["EP-RSC100"] = EP_DSC100
	attrValDict["EP-RSC01K"] = EP_DSC01K
	attrValDict["EP-RSC02K"] = EP_DSC02K
	attrValDict["EP-RSC05K"] = EP_DSC05K
	attrValDict["EP-RSC10K"] = EP_DSC10K

	attrValDict["TC-PCDX50"] = TC_PCDX50
	attrValDict["TC-PCDX10"] = TC_PCDX10
	attrValDict["TC-PCDX05"] = TC_PCDX05
	attrValDict["TC-PCDX01"] = TC_PCDX01

	attrValDict["SI-3300I2"] = SI_3300I2
	attrValDict["SI-920LN4"] = SI_920LN4
	attrValDict["SI-930LN4"] = SI_930LN4
	attrValDict["SI-920LN8"] = SI_920LN8
	attrValDict["51305786-502"] = B51305786_502
	attrValDict["51199562-200"] = B51199562_200

	attrValDict["51305482-102"] = B51305482_102
	attrValDict["51305482-202"] = B51305482_202
	attrValDict["51305482-105"] = B51305482_105
	attrValDict["51305482-205"] = B51305482_205
	attrValDict["51305482-110"] = B51305482_110
	attrValDict["51305482-210"] = B51305482_210
	attrValDict["51305482-120"] = B51305482_120
	attrValDict["51305482-220"] = B51305482_220

	attrValDict["CU-PWMR20"] = CU_PWMR20
	attrValDict["CU-PWMN20"] = CU_PWMN20
	attrValDict["CU-PWPR21"] = CU_PWPR21
	attrValDict["CU-PWPN21"] = CU_PWPN21
	attrValDict["CC-PWRR01"] = CC_PWRR01
	attrValDict["CC-PWRN01"] = CC_PWRN01
	attrValDict["CC_PWRB01"] = CC_PWRB01_1
	attrValDict["CC-PWR401"] = CC_PWR401
	attrValDict["CC-PWN401"] = CC_PWN401


def populateWriteInsCWSRAEUpgrade(product,Quote):
	writeInData = dict()
	msid= product.Attr('MSID').GetValue()
	sysNumber= product.Attr('System Number').GetValue()
	area = msid +" - "+ sysNumber
	virtconfig = product.Attr('CWS_Mig_Virtualization_Configuration').GetValue()
	if virtconfig:
		list90 =2128
		cost90 =1033
		list91 =2479
		cost91 = 1204
		quoteCurrency = Quote.SelectedMarket.CurrencyCode
		factor = 1.00
		if quoteCurrency != "USD":
			query = SqlHelper.GetFirst("select Exchange_Rate from Currency_ExchangeRate_Mapping where From_Currency = 'USD' and To_Currency = '{}'".format(quoteCurrency))
			if query is not None:
				factor = getFloat(query.Exchange_Rate)

			list90 *= factor
			cost90 *= factor
			list91 *= factor
			cost91 *= factor

		if virtconfig == "ESXi Virtualization with Management host and four VMs and four thin clients":
			writeInData["Q1000-90 Write-In Integration Center"] = [list90,cost90,"Q1000-90:ESXi SW Load and network configuration","2",area]
			writeInData["Q1000-91 Write-In Integration Center"] = [list91,cost91,'Q1000-91:Virtual Machine Load. "Qty one per Virtual Machine"',"4",area]

		elif virtconfig == "Virtualization on a Server with One VM and 2 Thin Clients":
			writeInData["Q1000-90 Write-In Integration Center"] = [list90,cost90,"Q1000-90:ESXi SW Load and network configuration","1",area]
			writeInData["Q1000-91 Write-In Integration Center"] = [list91,cost91,'Q1000-91:Virtual Machine Load. "Qty one per Virtual Machine"',"1",area]

		elif virtconfig == "Workstation Virtualization":
			writeInData["Q1000-91 Write-In Integration Center"] = [list91,cost91,'Q1000-91:Virtual Machine Load. "Qty one per Virtual Machine"',"1",area]

		'''productContainer = product.GetContainerByName("MSID_Product_Container")
		productRow = productContainer.Rows.GetByColumnName("Product Name", "CWS RAE Upgrade")
		prod = productRow.Product'''
		con = product.GetContainerByName("WriteInProduct")
		if con.Rows.Count > 0:
			con.Clear()
		Trace.Write("writeInData++++ "+str(writeInData))
		for wi, wiData in writeInData.items():
			row = con.AddNewRow()
			row.Product.Attr("Selected_WriteIn").AssignValue("Write-In Integration Center")
			row.Product.Attr("Price").AssignValue(str(wiData[0]))
			row.Product.Attr("Cost").AssignValue(str(wiData[1]))
			row.Product.Attr("Area").AssignValue(wiData[4])
			row.Product.Attr("ItemQuantity").AssignValue(wiData[3])
			row.Product.Attr("Extended Description").AssignValue(wiData[2])
			row.Product.ApplyRules()
			row.ApplyProductChanges()
			row.Calculate()
	else:
		'''productContainer = product.GetContainerByName("MSID_Product_Container")
		productRow = productContainer.Rows.GetByColumnName("Product Name", "CWS RAE Upgrade")
		prod = productRow.Product'''
		con = product.GetContainerByName("WriteInProduct")
		if con.Rows.Count > 0:
			con.Clear()
	con.Calculate()