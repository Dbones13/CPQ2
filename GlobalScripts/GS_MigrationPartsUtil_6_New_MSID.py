import math
def getContainer(prod, conName):
	return prod.GetContainerByName(conName)
def getFloat(Var):
	if Var:
		return float(Var)
	return 0

def updateAttributeDictWithCustomFSCtoSM(product, migrationAttrDict):
	con = getContainer(product, "FSC_to_SM_Configuration")
	for row in con.Rows:
		l = migrationAttrDict.get("FSC_to_SM_Serial_communication_System_gtr_2",list())
		l.append('True' if getFloat(row["FSC_to_SM_Serial_communication_System"]) > 2 else 'False')
		migrationAttrDict["FSC_to_SM_Serial_communication_System_gtr_2"] = l

def updateAttributeDictWithCustomFSSMcom(product, migrationAttrDict):
	con = getContainer(product, "FSC_to_SM_Configuration")
	for row in con.Rows:
		l = migrationAttrDict.get("FSC_to_SM_Serial_communication_System_gtr_0",list())
		l.append('True' if getFloat(row["FSC_to_SM_Serial_communication_System"]) > 0 else 'False')
		migrationAttrDict["FSC_to_SM_Serial_communication_System_gtr_0"] = l

def updateAttrDictWithCustomFSCtoSMParts(product, attrValDict, Quote):
	product = product
	con1 = getContainer(product, 'FSC_to_SM_Configuration')
	sespType = Quote.GetCustomField("Entitlement").Content if Quote and Quote.GetCustomField("Entitlement").Content else "No"
	if con1.Rows.Count >0:
		FC_DCOM_485 = 0.00
		#SDW_550EC = 0.00
		SDW_50194005_001 = 0.00
		FS_CCI_UNI_04 = 0.00
		FS_CCI_HSE_02 = 0.00
		MTL24571 = 0.00
		FS_CCI_UNI_04_data = 0.00
		FS_CCI_HSE_02_data = 0.00
		FC_DCOM_485_data = 0.0
		SDW_550EC_data = 0.0
		MTL24571_data = 0.0
		FS_SMSNUPL801 = 0.0
		diff = 0.0
		FS_SMSNUPL801_01S = 0.0
		FS_SMSNE810_01 = 0.0
		for row in con1.Rows:
			fscComSystem = getFloat(row['FSC_to_SM_Serial_communication_System'])
			fscDCS = (row['FSC_to_SM_SM_communication_to_DCS'])
			migratedSystemCount = getFloat(row['FSC_to_SM_How_many_systems_with_same_configuration_to_be_migrated_in_this_proposal'])
			fscSysSafeNet = getFloat(row['FSC_to_SM_How_many_FSC_Systems_are_in_the_SafeNet_network'])
			fcsConfigConn = (row['FSC_to_SM_Are_the_FSCs_in_this_configuration_connected_to_a_SafeNet_network'])
			fcsSysSafeNetMig = getFloat(row['FSC_to_SM_How_many_FSC_Systems_from_the_SafeNet_network_are_we_migrating_in_the_first_phase'])
			Trace.Write("fscSysSafeNet:{0},fcsConfigConn:{1}".format(fscSysSafeNet,fcsConfigConn ))
			if fscComSystem == 0.00:
				FC_DCOM_485_data  =  1.00
			elif fscComSystem > 0.00:
				if fscDCS == 'Serial Modbus-RTU' or fscDCS == '' :
					FC_DCOM_485_data = 2.00 + fscComSystem
				else:
					FC_DCOM_485_data = fscComSystem
				FS_CCI_UNI_04_data = ((2.00 * FC_DCOM_485_data) - 2.00)

			if fscDCS == 'Modbus-TCP/IP' or fscDCS == 'EUCN' :
				SDW_550EC_data = 3.00
			else:
				SDW_550EC_data = 1.00
			if fscDCS == 'FTE-SCADA':
				MTL24571_data = 2.00
			else:
				MTL24571_data = 0.00
			if fcsConfigConn == 'Yes' or fcsConfigConn == '':
				diff = fscSysSafeNet - fcsSysSafeNetMig
				if diff > 0.0 and sespType == 'No':
					FS_SMSNUPL801 += diff
					FS_SMSNE810_01 = 1
					attrValDict['FS_SMSNUPL801'] = round(FS_SMSNUPL801)
					#attrValDict['FS_SMSNE810_01'] = 1
				elif diff > 0.0 and (sespType == 'Yes' or sespType == 'K&E Pricing Plus' or sespType == 'K&E Pricing Flex' or sespType == 'Non-SESP MSID with new SESP Plus' or sespType == 'Non-SESP MSID with new SESP Flex'):
					FS_SMSNUPL801_01S += diff
					FS_SMSNE810_01 = 1
					attrValDict['FS_SMSNUPL801_01S'] = round(FS_SMSNUPL801_01S)
					#attrValDict['FS_SMSNE810_01'] = 1
				Trace.Write("FS_SMSNUPL801:{0}".format(diff))
			FS_CCI_HSE_02_data =round(float((SDW_550EC_data + MTL24571_data)/2.00))

			FC_DCOM_485 += float(FC_DCOM_485_data * migratedSystemCount)
			#SDW_550EC += float(SDW_550EC_data * migratedSystemCount)
			SDW_50194005_001 += float(SDW_550EC_data * migratedSystemCount)
			MTL24571 += float(MTL24571_data * migratedSystemCount)
			FS_CCI_UNI_04 += float(FS_CCI_UNI_04_data * migratedSystemCount)
			FS_CCI_HSE_02 += float(FS_CCI_HSE_02_data * migratedSystemCount)

		Trace.Write("FS_SMSNUPL8012:{0}".format(diff))
		attrValDict['FS_CCI_HSE_02'] = round(FS_CCI_HSE_02)
		attrValDict['FC_DCOM_485'] = round(FC_DCOM_485)
		#attrValDict['SDW_550EC'] = round(SDW_550EC)
		attrValDict['SDW_50194005_001'] = round(SDW_50194005_001)
		attrValDict['MTL24571'] = round(MTL24571)
		attrValDict['FS_CCI_UNI_04'] = round(FS_CCI_UNI_04)
		#attrValDict['FS_SMSNUPL801'] = round(FS_SMSNUPL801)
		#attrValDict['FS_SMSNUPL801_01S'] = round(FS_SMSNUPL801)
		attrValDict['FS_SMSNE810_01'] = round(FS_SMSNE810_01)
def updteAttrDict3PartyPLCUOC(product):
	attrValDict = dict()
	con1 = getContainer(product, 'MSID_Third_Party_PLC_Added_Parts_Common_Container')
	for row in con1.Rows:
		Log.Info(row['Quantity'])
		attrValDict[row['PartNumber'] ] = round(float(row['Quantity']))
	return attrValDict
def updAttrDictGS(product, index, partdict):
	try:
		genericsystemrow = product.GetContainerByName('MSID_Product_Container_Generic_hidden').Rows.Item[index].Product
		con1 = getContainer(genericsystemrow, 'Generic_System_Mig_Uploaded_Parts_Cont')
		if con1 != None:
			for row in con1.Rows:
				if row['Message'] =='Valid' and int(float(row['Final Quantity'])) > 0:
					cu = partdict.get(row['PartNumber'], 0)
					partdict[row['PartNumber'] ] = int(float(row['Final Quantity']) + cu)
		return partdict
	except:
		return partdict
def getGenericSystemCont(product, container_name,index):
	try:
		genericsystemrow = product.GetContainerByName('MSID_Product_Container_Generic_hidden').Rows.Item[index].Product
		return getContainer(genericsystemrow, container_name)
	except:
		return None
def getChildContainerMap():
	partContainers = [
		"MSID_OPM_Added_Parts_Common_Container",
		"MSID_LCN_Added_Parts_Common_Container",
		"MSID_NON_SESP_Added_Parts_Common_Container",
		"MSID_EBR_Added_Parts_Common_Container",
		"MSID_ELCN_Added_Parts_Common_Container",
		"MSID_Orion_Console_Added_Parts_Common_Container",
		"MSID_EHPM_C300PM_Added_Parts_Common_Container",
		"MSID_PM_Added_Parts_Common_Container",
		"MSID_TPS_EXP_Added_Parts_Common_Container",
		"MSID_TCMI_Added_Parts_Common_Container",
		"MSID_Spare_Parts_Added_Parts_Common_Container",
		"MSID_EHPM_HART_IO_Added_Parts_Common_Container",
		"MSID_CB_EC_Added_Parts_Common_Container",
		"MSID_C200_Migration_Added_Parts_Common_Container",
		"MSID_xPM_C300_Added_Parts_Common_Container",
		"MSID_FDM_Upgrade_1_Added_Parts_Common_Container",
		"MSID_FDM_Upgrade_2_Added_Parts_Common_Container",
		"MSID_FDM_Upgrade_3_Added_Parts_Common_Container",
		"MSID_FSC_to_SM_Added_Parts_Common_Container",
		"MSID_LM_TO_ELMM_Added_Parts_Common_Container",
		"MSID_XP10_Actuator_Added_Parts_Common_Container",
		"MSID_Graphics_Added_Parts_Common_Container",
		"MSID_FSCtoSM_IO_Added_Parts_Common_Container",
		"MSID_CD_Actuator_Added_Parts_Common_Container",
		"MSID_CWS_RAE_Upgrade_Added_Parts_Common_Container",
		"MSID_Third_Party_PLC_Added_Parts_Common_Container",
		"MSID_Virtualization_Added_Parts_Common_Container",
		"MSID_QCS_Added_Parts_Common_Container",
		"MSID_TPA_Added_Parts_Common_Container",
		# Extended Logic(container name) for ELEPIU Module -- Dipak Shekokar : CXCPQ-60173
		"MSID_ELEPIU_Added_Parts_Common_Container",
		"MSID_GS1_Added_Parts_Common_Container",
		"MSID_GS2_Added_Parts_Common_Container",
		"MSID_GS3_Added_Parts_Common_Container",
		"MSID_GS4_Added_Parts_Common_Container",
		"MSID_GS5_Added_Parts_Common_Container"
	]
	contProductMap = {
		"MSID_OPM_Added_Parts_Common_Container": "OPM",
		"MSID_LCN_Added_Parts_Common_Container": "LCN One Time Upgrade",
		"MSID_NON_SESP_Added_Parts_Common_Container": "Non-SESP Exp Upgrade",
		"MSID_EBR_Added_Parts_Common_Container": "EBR",
		"MSID_ELCN_Added_Parts_Common_Container": "ELCN",
		"MSID_Orion_Console_Added_Parts_Common_Container":"Orion Console",
		"MSID_EHPM_C300PM_Added_Parts_Common_Container":"EHPM/EHPMX/ C300PM",
		"MSID_PM_Added_Parts_Common_Container": "Project Management",
		"MSID_TPS_EXP_Added_Parts_Common_Container": "TPS to Experion",
		"MSID_TCMI_Added_Parts_Common_Container":"TCMI",
		"MSID_LM_TO_ELMM_Added_Parts_Common_Container" : "LM to ELMM ControlEdge PLC",
		"MSID_Spare_Parts_Added_Parts_Common_Container": "Spare Parts",
		"MSID_EHPM_HART_IO_Added_Parts_Common_Container": "EHPM HART IO",
		"MSID_CB_EC_Added_Parts_Common_Container": "CB-EC Upgrade to C300-UHIO",
		"MSID_C200_Migration_Added_Parts_Common_Container": "C200 Migration",
		"MSID_xPM_C300_Added_Parts_Common_Container": "xPM to C300 Migration",
		"MSID_FDM_Upgrade_1_Added_Parts_Common_Container": "FDM Upgrade 1",
		"MSID_FDM_Upgrade_2_Added_Parts_Common_Container": "FDM Upgrade 2",
		"MSID_FDM_Upgrade_3_Added_Parts_Common_Container": "FDM Upgrade 3",
		"MSID_FSC_to_SM_Added_Parts_Common_Container" : "FSC to SM",
		"MSID_XP10_Actuator_Added_Parts_Common_Container": "XP10 Actuator Upgrade",
		"MSID_Graphics_Added_Parts_Common_Container": "Graphics Migration",
		"MSID_FSCtoSM_IO_Added_Parts_Common_Container": "FSC to SM IO Migration",
		"MSID_CD_Actuator_Added_Parts_Common_Container": "CD Actuator I-F Upgrade",
		"MSID_CWS_RAE_Upgrade_Added_Parts_Common_Container": "CWS RAE Upgrade",
		"MSID_Third_Party_PLC_Added_Parts_Common_Container": "3rd Party PLC to ControlEdge PLC/UOC",
		"MSID_Virtualization_Added_Parts_Common_Container": "Virtualization System Migration",
		"MSID_QCS_Added_Parts_Common_Container": "QCS RAE Upgrade",
		"MSID_TPA_Added_Parts_Common_Container": "TPA/PMD Migration",
		# Extended Logic(container name) for ELEPIU Module -- Dipak Shekokar : CXCPQ-60173
		"MSID_ELEPIU_Added_Parts_Common_Container": "ELEPIU ControlEdge RTU Migration Engineering",
		"MSID_GS1_Added_Parts_Common_Container": "Generic System Migration",
		"MSID_GS2_Added_Parts_Common_Container": "Generic System Migration",
		"MSID_GS3_Added_Parts_Common_Container": "Generic System Migration",
		"MSID_GS4_Added_Parts_Common_Container": "Generic System Migration",
		"MSID_GS5_Added_Parts_Common_Container": "Generic System Migration"
	}
	return partContainers, contProductMap
def GetPartAndModulesDict():
	partNumbersToBeAdded = {
		"OPM": dict(),
		"LCN": dict(),
		"NONSESP": dict(),
		"EBR": dict(),
		"ELCN": dict(),
		"Orion_Console": dict(),
		"EHPM/EHPMX/ C300PM": dict(),
		"PM": dict(),
		"TPS_EXP": dict(),
		"TCMI": dict(),
		"LMTOELMM": dict(),
		"Spare Parts": dict(),
		"EHPMHART": dict(),
		"C200 Migration": dict(),
		"CBEC": dict(),
		"XPM C300": dict(),
		"FDM_Upgrade": dict(),
		"FDM_Upgrade_2": dict(),
		"FDM_Upgrade_3": dict(),
		"FSC_to_SM": dict(),
		"FSC_to_SM_audit": dict(),
		"THIRD_PARTY" : dict(),
		"XP10_Actuator": dict(),
		"Graphics_Migration": dict(),
		"CWS_RAE_Upgrade": dict(),
		"FSCtoSM_IO": dict(),
		"FSCtoSM_IO_AUDIT": dict(),
		"CD_Actuator_IF_Upgrade": dict(),
		"Virtualization_System_Migration": dict(),
		"QCS_RAE_Upgrade": dict(),
		"GS_Migration_1":dict(),
		"GS_Migration_2":dict(),
		"GS_Migration_3":dict(),
		"GS_Migration_4":dict(),
		"GS_Migration_5":dict(),
		"TPA/PMD_Migration": dict(),
		"ELEPIU_ControlEdge_RTU_Migration_Engineering": dict(),
		"3rd_Party_PLC_to_ControlEdge_PLC/UOC" : dict()
	}
	modules = {
		"OPM": dict(),
		"LCN": dict(),
		"NONSESP": dict(),
		"EBR": dict(),
		"ELCN": dict(),
		"Orion_Console": dict(),
		"EHPM/EHPMX/ C300PM": dict(),
		"PM": dict(),
		"TPS_EXP": dict(),
		"TCMI": dict(),
		"LMTOELMM": dict(),
		"Spare Parts": dict(),
		"EHPMHART": dict(),
		"C200 Migration": dict(),
		"CBEC": dict(),
		"XPM C300": dict(),
		"FDM_Upgrade": dict(),
		"FDM_Upgrade_2": dict(),
		"FDM_Upgrade_3": dict(),
		"FSC_to_SM": dict(),
		"FSC_to_SM_audit": dict(),
		"THIRD_PARTY" : dict(),
		"XP10_Actuator": dict(),
		"CWS_RAE_Upgrade": dict(),
		"Graphics_Migration": dict(),
		"FSCtoSM_IO": dict(),
		"FSCtoSM_IO_AUDIT": dict(),
		"CD_Actuator_IF_Upgrade": dict(),
		"Virtualization_System_Migration": dict(),
		"QCS_RAE_Upgrade": dict(),
		"GS_Migration_1":dict(),
		"GS_Migration_2":dict(),
		"GS_Migration_3":dict(),
		"GS_Migration_4":dict(),
		"GS_Migration_5":dict(),
		"TPA/PMD_Migration": dict(),
		"ELEPIU_ControlEdge_RTU_Migration_Engineering": dict(),
		"3rd_Party_PLC_to_ControlEdge_PLC/UOC" : dict()
	}
	return partNumbersToBeAdded,modules

def updateAttrWithTpsExpValues(product, attrValDict):
	#added by Saqlain Malik on account of CCEECOMMBR-5949
	tps_server = 0
	EP_PKS511_ESD = 0
	EP_PKS520_ESD = 0

	est_cont = getContainer(product,'TPS_EX_Station_Conversion_EST')
	for row in est_cont.Rows:
		if row["TPS_EX_Station_Conversion_Type"] == "US_AM to ES-T":
			if getFloat(row["TPS_EX_Quantity"]) > 0:
				tps_server += 1

	acet_cont = getContainer(product,'TPS_EX_Conversion_ACET_EAPP')
	for row in acet_cont.Rows:
		if row["TPS_EX_Conversion_ACET_EAPP_Type"] == "APP to ACE-T":
			if getFloat(row["TPS_EX_Conversion_ACET_EAPP_Qty"]) > 0:
				tps_server += 1

	con1 = getContainer(product,"MSID_CommonQuestions")
	for row in con1.Rows:
		fut_rel = row["MSID_Future_Experion_Release"]
		break

	if tps_server > 0:
		if fut_rel == "R520":
			EP_PKS520_ESD += 1
		else:
			EP_PKS511_ESD += 1
	attrValDict['EP_PKS520_ESD'] = EP_PKS520_ESD
	attrValDict['EP_PKS511_ESD'] = EP_PKS511_ESD