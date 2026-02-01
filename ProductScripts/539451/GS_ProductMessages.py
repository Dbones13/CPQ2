if Product.ParseString("<*CTX( Product.RootProduct.SystemId )*>") == 'Migration2_cpq':
	def getContainer(containerName):
		return Product.GetContainerByName(containerName)
	def getFloat(Var):
		if Var:
			return float(Var)
		return 0

	def getAttributeValue(Name):
		return Product.Attr(Name).GetValue()

	def setAttrValue(Name,value):
		Product.Attr(Name).AssignValue(value)

	def getContainerColSum(containerName , rowId):
		container = getContainer(containerName)
		sum = 0
		for row in container.Rows:
			if row.RowIndex == rowId:
				for col in row.Columns:
					try:
						sum += float(row[col.Name])
					except:
						pass
		return sum > 0

	incomplete1 = []
	incomplete = []
	isR2qQuote = True if Quote.GetCustomField('isR2QRequest').Content == 'Yes' else False
	try:
		scope = Product.Attr('Scope').SelectedValue.Display
	except:
		scope = Product.Attributes.GetByName('Scope').GetValue()
	if Product.Name =="OPM":
		if getContainer("OPM_Basic_Information"):
			opmBasic = getContainer("OPM_Basic_Information")
			if opmBasic.Rows.Count>0:
				row = opmBasic.Rows[0]
				hwReplaceNeeded = row["OPM_Servers_and_Stations_HW_replace_needed"] == 'Yes' and Product.Attr('MIgration_Scope_Choices').GetValue() != "LABOR"
			else:
				hwReplaceNeeded = ''
		if not getContainerColSum("OPM_Node_Configuration" , 0):
			incomplete.append("OPM_Node_Configuration")
		if hwReplaceNeeded:
			if not getContainerColSum("OPM_Node_Configuration" , 2):
				incomplete.append("OPMNode_Configuration_HW")

	if Product.Name =="Non-SESP Exp Upgrade":
		if not getContainerColSum("NONSESP_Design_Inputs_for_Experion_Upgrade_License" , 0):
			incomplete.append("NONSESP_Design_Inputs_for_Experion_Upgrade_License")
	if Product.Name =="LCN One Time Upgrade":
		if not getContainerColSum("LCN_Design_Inputs_for_TPN_OTU_Upgrade" , 0):
			incomplete.append("LCN_Design_Inputs_for_TPN_OTU_Upgrade")

	if Product.Name =='ELCN':
		elcnUpgradeNewElcnNodesCon =  getContainer('ELCN_Upgrade_New_ELCN_Nodes')
		totalQtyOfNetworkGateway = 0
		rowAssetDB = 2
		rowIndex = 0
		if elcnUpgradeNewElcnNodesCon.Rows.Count>0:
			for row in elcnUpgradeNewElcnNodesCon.Rows:
				if rowIndex != rowAssetDB:
					for column in row.Columns:
						if row[column.Name] != '':
							totalQtyOfNetworkGateway += int(row[column.Name])
				rowIndex += 1
		if totalQtyOfNetworkGateway == 0:
			incomplete.append("ELCN_Nodes")

	if Product.Name =='EHPM/EHPMX/ C300PM':
		xPMMigrationGeneralQnsCont =  getContainer('xPM_Migration_General_Qns_Cont')
		xPMMigrationConfigCont =  getContainer('xPM_Migration_Config_Cont')
		ENBMigrationConfigCont = getContainer('ENB_Migration_Config_Cont')
		xPMMigrationScenarioCont = getAttributeValue("xPM_Select_the_migration_scenario")
		tpnRelease = ''
		epksRelease = ''
		xPMMigrations = 0
		NIMMigrations = int(getAttributeValue("xPM_NIMsconf"))
		if xPMMigrationGeneralQnsCont.Rows.Count>0:
			row1 = xPMMigrationGeneralQnsCont.Rows[0]
			xPMMigrations = int(row1['xPM_How_many_xPMs_configurations_are_we_migrating']) if  row1['xPM_How_many_xPMs_configurations_are_we_migrating'].strip()!='' else 0
			tpnRelease = row1["xPM_TPN_SW_Release_at_time_of_xPM_migration"]
			epksRelease = row1["xPM_EPKS_SW_Release_at_time_of_xPM_migration"]
		if tpnRelease == '-':
			incomplete.append("xpm_select_tpn")
		if epksRelease == '-':
			incomplete.append("xpm_select_epks")
		if (xPMMigrations + NIMMigrations) <= 0:
			incomplete.append("How_many_xPMs")
		else:
			noOfConfigInValid = False
			totalNoOfIncludedSi = False
			peertopeer = False
			if xPMMigrations > 0:
				for row in xPMMigrationConfigCont.Rows:
					noOfConfigs = int(row['xPM_Number_of_xPMs_in_this_config']) if  row['xPM_Number_of_xPMs_in_this_config'].strip() != '' else 0
					if row['xPM_Number_of_xPM_Points_including_SI'].strip() in ('',"0",0):
						totalNoOfIncludedSi = True
					if noOfConfigs <= 0:
						noOfConfigInValid = True
					else:
						if getFloat(row["xPM_EHPMX_need_Experion_peer_to_peer_connectivity"]) > noOfConfigs or getFloat(row["xPM_Controller_need_Experion_peer_to_peer_connectivity"])> noOfConfigs or getFloat(row["xPM_How_many_EHPMs_will_require_Exp_conn"] )> noOfConfigs:
							peertopeer = True

				if noOfConfigInValid:
					incomplete.append("No_of_xPMs")
				if totalNoOfIncludedSi and xPMMigrationScenarioCont == "xPM to C300PM" and scope != "LABOR":
					incomplete.append("No_of_included_si")
				if peertopeer:
					incomplete.append("EHPM_peertopeer")
			if NIMMigrations > 0:
				isInvalid = False
				fteCount = int(getAttributeValue("ATT_QFTENK"))
				if fteCount <= 0 and scope != "LABOR":
					incomplete.append("xPM_fte_input")
				for row in ENBMigrationConfigCont.Rows:
					noOfConfigs = int(row['xPM_Number_of_NIMs_in_this_config']) if  row['xPM_Number_of_NIMs_in_this_config'].strip() != '' else 0
					if noOfConfigs <= 0:
						isInvalid = True
						break
				if isInvalid:
					incomplete.append("No_of_NIMs")

	if Product.Name=='EHPM HART IO':
		EHPMHARTIOGeneralQnsCont =  getContainer('EHPM_HART_IO_General_Qns_Cont')
		if getContainer('EHPM_HART_IO_Configuration_Cont').Rows<0 and EHPMHARTIOGeneralQnsCont:
			EHPMHARTIOConfigCont = getContainer('EHPM_HART_IO_Configuration_Cont')
			row1 = EHPMHARTIOGeneralQnsCont.Rows[0]
			numberofins = 0
			sumOfIoConfig = 0

			for row in EHPMHARTIOConfigCont.Rows:
				for column in row.Columns:
					if row[column.Name] not in ('',"0"):
						sumOfIoConfig = int(row[column.Name])

			cxrRelease = row1["Current_Experion_Release"]
			tpnRelease = row1["Current_TPN_Release"]
		if cxrRelease == '-':
			incomplete.append("Current_Experion_Release")
		if tpnRelease == '-':
			incomplete.append("Current_TPN_Release")
		if getAttributeValue('scope') in ["LABOR", "HW/SW/LABOR"]:
			numberofins = int(Product.Attr('EHPM_HART_IO_WBI').GetValue())
			if numberofins <= 0:
				incomplete.append("Number_of_EHPM_where_HART_IO_will_be_installed")
		if sumOfIoConfig <= 0:
			incomplete.append("Number_of_Non_Redundant_HART_HLAI")
	if Product.Name=='CB-EC Upgrade to C300-UHIO':
		CBECConfigCont = getContainer('CB_EC_migration_to_C300_UHIO_Configuration_Cont')
		if CBECConfigCont.Rows.Count > 0:
			row1=CBECConfigCont.Rows[0]
			CB = row1["CB_EC_How_many_CBs_are_being_migrated"] or 0
			EC = row1["CB_EC_How_many_ECs_are_being_migrated"] or 0
			sumOfCBAndEC=int(CB)+int(EC)
			if(sumOfCBAndEC) < 2:
				incomplete.append("Sum_of_CB_And_EC")
	if Product.Name=="CB-EC Upgrade":
		CBECConfigCont = getContainer('CB_EC_Services_1_Cont')
		row = CBECConfigCont.Rows[0]
		if (row["CB_EC_Total_Number_of_Analog_Input_points_HGAIN"] == '' or row["CB_EC_Total_Number_of_Analog_Input_points_HGAIN"] == "0") and (row["CB_EC_Total_Number_of_Analog_Output_points_HGAOT"] == '' or row["CB_EC_Total_Number_of_Analog_Output_points_HGAOT"] == "0") and (row["CB_EC_Total_Number_of_Regulatory_points_HGREG"] == '' or row["CB_EC_Total_Number_of_Regulatory_points_HGREG"] == "0") and (row["CB_EC_Total_Number_of_Digital_Input_points_HGDIN"] == '' or row["CB_EC_Total_Number_of_Digital_Input_points_HGDIN"] == "0") and (row["CB_EC_Total_Number_of_Digital_Output_points_HGDOT"] == '' or row["CB_EC_Total_Number_of_Digital_Output_points_HGDOT"] == "0") and (row["CB_EC_Total_Number_of_Digital_Composite_points_HGDCP"] == '' or row["CB_EC_Total_Number_of_Digital_Composite_points_HGDCP"] == "0") and (row["CB_EC_Total_Number_of_Cascade_Loop"] == '' or row["CB_EC_Total_Number_of_Cascade_Loop"] == "0") and (row["CB_EC_Total_Number_of_Complex_Loop"] == '' or row["CB_EC_Total_Number_of_Complex_Loop"] == "0") and (row["CB_EC_Total_Number_of_Aux_function"] == '' or row["CB_EC_Total_Number_of_Aux_function"] == "0") and row["CB_EC_Do_you_know_the_number_of AI_AO_Regulatory_points_DI_DO_and_Digital_Composite_points"] =="Yes":
			incomplete.append("CBEC_Services")

	if Product.Name=='xPM to C300 Migration':
		xpmC300Config = getContainer('xPM_C300_Migration_Configuration_Cont')
		rowConfig = xpmC300Config.Rows
		noOfMigrations = getAttributeValue("ATT_NUMXPMC300")
		test = getAttributeValue("ATT_NUMAMPTS")
		if scope != 'HWSW':
			AM_ACE = getAttributeValue("ATT_NUMAMTOACE")
		else:
			AM_ACE = 0
		if scope != 'HWSW':
			AMPoints = getAttributeValue("ATT_NUMAMPTS")
		else:
			AMPoints = 0
		if noOfMigrations == '0' or noOfMigrations == '':
			incomplete.append("xPMs_to_be_Migrated")
		if scope != 'HWSW' and AM_ACE > 0 and AMPoints <= 0:
			incomplete.append("AM_ACE_Points")
		for row in rowConfig:
			SerialInterfacePoints = getFloat(row['xPM_C300_Number_of_Serial_Interface_points_for_Scada_conversion'])
			devices_xpmSI = getFloat(row['xPM_C300_Number_of_devices_connected_to_xPM_SI_for_PCDI_conversion'])
			if scope != 'HWSW':
				SerialInterfaceModules = 0 if row['xPM_C300_Number_of_Serial_Interface_modules'] == "" else int(row['xPM_C300_Number_of_Serial_Interface_modules'])
			else:
				SerialInterfaceModules = 0
			if scope != 'HWSW':
				SI_AB_Modbus = 0 if row['xPM_C300_Number_of_SI_Modbus_and_Allen_Bradley_Rockwell_Array_points_for_PCDI_conversion'] == "" else int(row['xPM_C300_Number_of_SI_Modbus_and_Allen_Bradley_Rockwell_Array_points_for_PCDI_conversion'])
			else:
				SI_AB_Modbus = 0
			if scope != 'LABOR':
				xpmIOMs = 0 if row['xPM_C300_Number_of_xPM_IOMs'] == "" else int(row['xPM_C300_Number_of_xPM_IOMs'])
			else:
				xpmIOMs = 0
			totalPoints1 = getFloat(row['xPM_C300_Number_of_xPM_Analog_Input_points']) + getFloat(row['xPM_C300_Number_of_xPM_Analog_Output_points']) + getFloat(row['xPM_C300_Number_of_xPM_Digital_Input_points']) + getFloat(row['xPM_C300_Number_of_xPM_Digital_output_points'])
			totalPoints2 = SerialInterfacePoints + SI_AB_Modbus
			totalPoints3 = SerialInterfacePoints + devices_xpmSI + SI_AB_Modbus
			if ((row['xPM_C300_Number_of_xPM_Analog_Input_points'] == '0' or row['xPM_C300_Number_of_xPM_Analog_Input_points'] == '') and (row['xPM_C300_Number_of_xPM_Analog_Output_points'] == '0' or row['xPM_C300_Number_of_xPM_Analog_Output_points'] == '') and (row['xPM_C300_Number_of_xPM_Digital_Input_points'] == '0' or row['xPM_C300_Number_of_xPM_Digital_Input_points'] == '') and (row['xPM_C300_Number_of_xPM_Digital_output_points'] == '0' or row['xPM_C300_Number_of_xPM_Digital_output_points'] == '')) or totalPoints1 == 0:
				incomplete.append("2ndValidation")
			if totalPoints1 + totalPoints2 > 45000:
				incomplete.append("3rdValidation")
			if xpmIOMs <= 0 and scope != 'LABOR':
				incomplete.append("xpm_IOMs")
			if SerialInterfaceModules > 0 and totalPoints3 <= 0 and scope != 'HWSW':
				incomplete.append("5thValidation")
	if Product.Name=='LM to ELMM ControlEdge PLC':
		lmToELMM3Party = getContainer('LM_to_ELMM_3rd_Party_Items')
		row = lmToELMM3Party.Rows
		for col in lmToELMM3Party.Properties:
			col_name = col.Name.split('|')[0]
			if row.Count > 0:
				if (float(row[0][col_name] if row[0][col_name] != '' else 0 ) > 0  and (float(row[1][col_name] if row[1][col_name] != '' else 0) == 0 or row[2][col_name] == '')) or (float(row[1][col_name] if row[1][col_name] != '' else 0 ) > 0  and (float(row[0][col_name] if row[0][col_name] != '' else 0) == 1 or row[2][col_name] == '')):
					incomplete.append("LMThirdPatryWriteIn")
		qtyLMPair = 0
		#lmToELMMGenCont = getContainer('LM_to_ELMM_ControlEdge_PLC_Migration_Gen_Cont')
		#for r in lmToELMMGenCont.Rows:
			#if r['LM_Qty_Of_LM_Pair_To_Be_Migrated'] == '' or (r['LM_Qty_Of_LM_Pair_To_Be_Migrated']).ToString() == "0":
				#incomplete.append("QtyOfLMPair")
			#else:
				#qtyLMPair = 1
		if getAttributeValue('ATT_LM_QTY_OF_LMPAIR_TOBE_MIGRATED')== '' or getAttributeValue('ATT_LM_QTY_OF_LMPAIR_TOBE_MIGRATED')== '0':
			incomplete.append("QtyOfLMPair")
		else:
			qtyLMPair = 1
		if int(getAttributeValue('ATT_LM_ADDITIONALSWITCHES') if getAttributeValue('ATT_LM_ADDITIONALSWITCHES') != "" else 0) >0 and (getAttributeValue('ATT_LM_ELMM_ADDITIONAL_SWITCH') == "None" or getAttributeValue('ATT_LM_ELMM_ADDITIONAL_SWITCH') == ""):
			incomplete.append("AdditionalSwitchValidation")
		lmToELMMAdditionalIOCont = getContainer('LM_to_ELMM_Migration_Additional_IO_Cont')
		for r in lmToELMMAdditionalIOCont.Rows:
			if (r['qty_IO_points_to_be_rewired_0_5000'] == '' or str(r['qty_IO_points_to_be_rewired_0_5000']) == "0") and scope != 'HW/SW':
				incomplete.append("QtyOfIORewired")
		con2 = getContainer("LM_to_ELMM_ControlEdge_PLC_Cont")
		lmLocalIO = getContainer("LM_to_ELMM_ControlEdge_PLC_Local_IO_Cont")
		lmRemoteIO = getContainer("LM_to_ELMM_ControlEdge_PLC_Remote_IO_Cont")
		for row in con2.Rows:
			if qtyLMPair == 0:
				break
			if row['LM_are_the_IO_Racks_remotely_located'] == 'Yes - Only Remote' and row.RowIndex <= lmRemoteIO.Rows.Count -1:
				row_remote = sum(
									int(column.Value) if column.Value != '' else 0
									for column in lmRemoteIO.Rows[row.RowIndex].Columns
									if column.Name != 'total_remote_serial_IO_racks_0_16' and column.Name != 'no_of_PLC_Remote_IO_group_0_16'
								)
				row_plc_remote_io =sum(
										int(column.Value) if column.Value != '' else 0
										for column in lmRemoteIO.Rows[row.RowIndex].Columns
										if column.Name == 'no_of_PLC_Remote_IO_group_0_16'
										)
				row_total_remote_serial_io = sum(
												int(column.Value) if column.Value != '' else 0
												for column in lmRemoteIO.Rows[row.RowIndex].Columns
												if column.Name == 'total_remote_serial_IO_racks_0_16'
											)
				if row_remote == 0:
					incomplete.append("QtyOfRemoteIO")
				if row_plc_remote_io == 0 or row_total_remote_serial_io == 0:
					incomplete.append("RemoteIO_Qty_Validation2")
			if row['LM_are_the_IO_Racks_remotely_located'] in ['No', ''] and row.RowIndex <= lmLocalIO.Rows.Count -1:
				row_local = getContainerColSum("LM_to_ELMM_ControlEdge_PLC_Local_IO_Cont", row.RowIndex)
				if row_local == 0:
					incomplete.append("QtyOfLocalIO")
			if row['LM_are_the_IO_Racks_remotely_located'] == 'Yes - Local and Remote' and row.RowIndex <= lmLocalIO.Rows.Count -1:
				row_local = getContainerColSum("LM_to_ELMM_ControlEdge_PLC_Local_IO_Cont", row.RowIndex)
				if row_local == 0:
					incomplete.append("QtyOfLocalIO")
				row_remote = getContainerColSum("LM_to_ELMM_ControlEdge_PLC_Remote_IO_Cont", row.RowIndex)
				row_plc_remote_io = sum(
										int(column.Value) if column.Value != '' else 0
										for column in lmRemoteIO.Rows[row.RowIndex].Columns
										if column.Name == 'no_of_PLC_Remote_IO_group_0_16'
									)
				row_total_remote_serial_io = sum(
												int(column.Value) if column.Value != '' else 0
												for column in lmRemoteIO.Rows[row.RowIndex].Columns
												if column.Name == 'total_remote_serial_IO_racks_0_16'
											)
				if row_remote == 0:
					incomplete.append("QtyOfRemoteIO")
				if row_plc_remote_io == 0 or row_total_remote_serial_io == 0:
					incomplete.append("RemoteIO_Qty_Validation2")
	if Product.Name=='FDM Upgrade 1':
		check = getAttributeValue("FDM_Upgrade_Additional_Components")
		if str(getAttributeValue("FDM_Upgrade_Do_you_want_to_upgrade_this_FDM")) == "Yes" and getAttributeValue("Attr_FDM_Upg1ServerDevicePoints") in ['0', None, ''] and getAttributeValue("Attr_FDMUpg1_AuditTrailDev") in ['0', None, ''] and getAttributeValue("Attr_FDMUpg1_RCIs_incExperion") in ['0', None, ''] and getAttributeValue("Attr_FDMUpg1_RCIs_excExperion") in ['0', None, ''] and getAttributeValue("Attr_FDM_Upg1_TotalFDMClients") in ['0', None, '']:
			incomplete.append("FDMflag")

		if check == "Yes" and getAttributeValue("FDM_Upgrade_Are_additional_components_required") == "Yes" and getAttributeValue("Attr_FDM_Upg_devmanaged") in ['0', None, ''] and getAttributeValue("Attr_FDM_Upg_AuditTrailDev") in ['0', None, ''] and getAttributeValue("Attr_FDMUpg_FDMClients") in ['0', None, ''] and getAttributeValue("Attr_Experion/TPS_Servers_FDMInt") in ['0', None, ''] and getAttributeValue("Attr_ServerNetInterfaceLic") in ['0', None, '']:
			incomplete.append("FDMaddflag")

	if Product.Name=='FSC to SM':
		flag1 = 0
		flag2 = 0
		check = getAttributeValue("ATT_FSC_to_SM_Number_of_configurations")
		if int(check) > 0:
			fscConfig = getContainer("FSC_to_SM_Configuration")
			for row in fscConfig.Rows:
				if row["FSC_to_SM_How_many_systems_with_same_configuration_to_be_migrated_in_this_proposal"] in ("0",None,""):
					flag1 = 1
				if getFloat(row["FSC_to_SM_How_many_FSC_Systems_from_the_SafeNet_network_are_we_migrating_in_the_first_phase"]) > getFloat(row["FSC_to_SM_How_many_FSC_Systems_are_in_the_SafeNet_network"]):
					flag2 = 1
		if flag1 == 1:
			incomplete.append("sameconfigFSC")
		if flag2 == 1:
			incomplete.append("safenetFSC")

		fsc3rdparty = getContainer("FSC_to_SM_3rd_Party_Items")
		if fsc3rdparty.Rows.Count > 0:
			price = getFloat(fsc3rdparty.Rows[0]["FSC_to_SM_3rd_Party_Hardware_per_Audit_Report"])
			cost = getFloat(fsc3rdparty.Rows[2]["FSC_to_SM_3rd_Party_Hardware_per_Audit_Report"])
			description = fsc3rdparty.Rows[3]["FSC_to_SM_3rd_Party_Hardware_per_Audit_Report"]
			if (price > 0 and (cost == 0 or description == "")) or (cost > 0 and (price == 0 or description == "")):
				incomplete.append("thirdpartyFSC")

	if Product.Name=='FSC to SM IO Migration':

		if Product.Attr('Scope').GetValue() != "HW/SW":
			qcf_proposalType = Quote.GetCustomField('EGAP_Proposal_Type').Content
			if Quote.GetCustomField('EGAP_Proposal_Type').Content:
				qcf_proposalType = Quote.GetCustomField('EGAP_Proposal_Type').Content
				if qcf_proposalType == "Firm":
					auditRow = getAttributeValue("FSC_to_SM_IO_Has_the_FSC_IO_Audit_been_performed")
					if auditRow in ("","No"):
						incomplete.append("flagAuditFSCio")

		flagQtyFSCio = 0
		flagSumFSCio = 0
		flagIORacks = 0
		flagAnalogDigital = 0
		scope_labor = 0
		
		flagFscRed = 0
		flagFscNonRed = 0
		flagFscRange1 = 0
		flagFscRange2 = 0
		flagFscRange3 = 0

		check = getFloat(getAttributeValue("ATT_FSCtoSMIOMigrationTotalFSC"))

		if Product.Attr('Scope').GetValue() != "LABOR":
			val = getContainer("FSC_to_SM_IO_Migration_General_Information2").Rows.Count
			if val>0:
				fsc_to_sm_migration_gen_info2 = getContainer("FSC_to_SM_IO_Migration_General_Information2")
				row = fsc_to_sm_migration_gen_info2.Rows[0]
				row1 = fsc_to_sm_migration_gen_info2.Rows[1]
				row2 = fsc_to_sm_migration_gen_info2.Rows[2]
				price = getFloat(row["FSC_to_SM_IO_Migration_3rd_Party_Hardware_per_Audit_Report"])
				cost = getFloat(row1["FSC_to_SM_IO_Migration_3rd_Party_Hardware_per_Audit_Report"])
				description = len(row2["FSC_to_SM_IO_Migration_3rd_Party_Hardware_per_Audit_Report"])
				if price != 0 or cost != 0 or description != 0:
					if price == 0 or cost == 0 or description == 0:
						incomplete.append("fsc_to_sm_3rd_party_price")
				check1 =  getAttributeValue("FSC_to_SM_IO_Migration_Where_will_IO_be_installed")
				if check1 != 'New SM Cabinet':
					scope_labor = 1

		if int(check) > 0:
			for row in getContainer("FSC_to_SM_IO_Series_1_&_2_FSC_IO_configurations").Rows:
				if getFloat(row["FSC_to_SM_IO_Quantity_of_Cabinets_containing_IO_Rack"]) == 0:
					flagQtyFSCio += 1
				#else:
					#if getFloat(row["FSC_to_SM_IO_Number_of_IO_Racks"]) == 0:
						#flagFscRed += 1
					#if getFloat(row["NON_RED_FSC_to_SM_IO_Number_of_IO_Racks"]) == 0:
						#flagFscNonRed += 1
				if (getFloat(row["FSC_to_SM_IO_Number_of_IO_Racks"]) + getFloat(row["NON_RED_FSC_to_SM_IO_Number_of_IO_Racks"])) > 34:
					flagSumFSCio += 1
				if (getFloat(row["FSC_to_SM_IO_Number_of_IO_Racks"]) + getFloat(row["NON_RED_FSC_to_SM_IO_Number_of_IO_Racks"])) > 8 and (getFloat(row["FSC_to_SM_IO_Number_of_IO_Racks"]) + getFloat(row["NON_RED_FSC_to_SM_IO_Number_of_IO_Racks"])) <= 17 and getFloat(row["FSC_to_SM_IO_Quantity_of_Cabinets_containing_IO_Rack"]) < 2:
					flagFscRange1 += 1
				if (getFloat(row["FSC_to_SM_IO_Number_of_IO_Racks"]) + getFloat(row["NON_RED_FSC_to_SM_IO_Number_of_IO_Racks"])) > 17 and (getFloat(row["FSC_to_SM_IO_Number_of_IO_Racks"]) + getFloat(row["NON_RED_FSC_to_SM_IO_Number_of_IO_Racks"])) <= 25 and getFloat(row["FSC_to_SM_IO_Quantity_of_Cabinets_containing_IO_Rack"]) < 3:
					flagFscRange2 += 1
				if (getFloat(row["FSC_to_SM_IO_Number_of_IO_Racks"]) + getFloat(row["NON_RED_FSC_to_SM_IO_Number_of_IO_Racks"])) > 25 and (getFloat(row["FSC_to_SM_IO_Number_of_IO_Racks"]) + getFloat(row["NON_RED_FSC_to_SM_IO_Number_of_IO_Racks"])) <= 34 and getFloat(row["FSC_to_SM_IO_Quantity_of_Cabinets_containing_IO_Rack"]) < 4:
					flagFscRange3 += 1
				if scope_labor == 1:
					if (getFloat(row["FSC_to_SM_IO_Number_of_IO_Racks"]) + getFloat(row["NON_RED_FSC_to_SM_IO_Number_of_IO_Racks"])) == 0:
						flagIORacks += 1

				sum = 0
				for col in row.Columns:
					if col.Name not in ("FSC_to_SM_IO_Quantity_of_Cabinets_containing_IO_Rack","FSC_to_SM_IO_IO_Module_IO_Rack_Type","FSC_to_SM_IO_Number_of_IO_Racks","FSC_to_SM_IO_Series_1_FSC_IO","FSC_to_SM_IO_Series_2_FSC_IO","NON_RED_FSC_to_SM_IO_IO_Module_IO_Rack_Type","NON_RED_FSC_to_SM_IO_Number_of_IO_Racks","NON_RED_FSC_to_SM_IO_Series_1_FSC_IO","NON_RED_FSC_to_SM_IO_Series_2_FSC_IO"):
						if getFloat(row[col.Name]) > 0:
							sum += 1
							break
				if sum == 0:
					flagAnalogDigital += 1

		if flagQtyFSCio > 0:
			incomplete.append("flagQtyFSCio")
		if flagSumFSCio > 0:
			incomplete.append("flagSumFSCio")
		if flagIORacks > 0:
			incomplete.append("flagFSCIORacks")
		if flagAnalogDigital > 0:
			incomplete.append("flagFSCioAnalogDigital")
		#if flagFscRed > 0:
			#incomplete.append("flagFscRed")
		#if flagFscNonRed > 0:
			#incomplete.append("flagFscNonRed")
		if flagFscRange1 > 0:
			incomplete.append("flagFscRange1")
		if flagFscRange2 > 0:
			incomplete.append("flagFscRange2")
		if flagFscRange3 > 0:
			incomplete.append("flagFscRange3")
	
	if Product.Name =='Graphics Migration':
		GraphicsMenuCont = getContainer('Graphics_Migration_Displays_Shapes_Faceplates')
		if GraphicsMenuCont.Rows.Count > 0:
			row=GraphicsMenuCont.Rows[0]
			sumofShapes = getFloat(row["Number_of_Simple_Custom_Shapes"]) + getFloat(row["Number_of_Medium_Custom_Shapes"]) + getFloat(row["Number_of_Complex_Custom_Shapes"]) + getFloat(row["Number_of_Very_Complex_Custom_Shapes"]) + getFloat(row["Number_of_Repeats_Custom_Shapes"])
			sumOfFaceplates = getFloat(row["Number_of_Simple_Custom_Faceplates"]) + getFloat(row["Number_of_Medium_Custom_Faceplates"]) + getFloat(row["Number_of_Complex_Custom_Faceplates"]) + getFloat(row["Number_of_Very_Complex_Custom_Faceplates"]) + getFloat(row["Number_of_Repeats_Custom_Faceplates"])
			if not isR2qQuote:
				if (sumofShapes) <= 0:
					incomplete.append("Sum_of_Shapes")
				if (sumOfFaceplates) <= 0:
					incomplete.append("Sum_of_Faceplates")
				if (getFloat(row["Total_Number_of_Displays"])) in [0,0.0,'']:
					incomplete.append("Sum_of_Displays")
			if isR2qQuote and (getFloat(row["Total_Number_of_Displays"])) in [0,0.0,'']:
				incomplete.append("Sum_of_Displays")

			'''if isR2qQuote and (getFloat(row["Number_of_Repeats_Custom_Shapes"]) in [0,0.0,'']):
					incomplete.append("Sum_of_Shapes")
					incomplete.append("Sum_of_Faceplates")'''

		if getContainer("Graphics_Migration_Additional_Questions"):
			graphicAddCon = getContainer("Graphics_Migration_Additional_Questions")
			rowAddCon = graphicAddCon.Rows[0]
			if rowAddCon["Graphics_Migration_New_Safeview_Configuration"] not in ("None"):
				if getFloat(rowAddCon["Graphics_Migration_Number_of_station_licenses"]) == 0:
					incomplete.append("graphicAdditionalCon")
		else:
			if Product.Attr('Graphics_Migration_New_Safeview_Configuration').GetValue() not in ("None"):
				if getFloat(Product.Attr('ATT_GMNUMSL').GetValue()) in [0,0.0,'']:
					incomplete.append("graphicAdditionalCon")

	if Product.Name=='CD Actuator I-F Upgrade':
		Actuator_zone = getAttributeValue("ATT_CD_ACTUATOR_NOZONES")
		if Actuator_zone == '0':
			incomplete.append("Actuator_zone_incomplete_msg")
		elif int(Actuator_zone) < 10 and int(Actuator_zone) > 256:
			incomplete.append("Actuator_zone_incomplete_msg")
		if Product.Attr('Scope').GetValue() != "LABOR":
			cd_act_gen_info_cont = getContainer("CD_Actuator_pricing_factory_cost")
			if cd_act_gen_info_cont.Rows.Count > 0:
				row = cd_act_gen_info_cont.Rows[0]
				row1 = cd_act_gen_info_cont.Rows[1]
				row2 = cd_act_gen_info_cont.Rows[2]
				price = getFloat(row["CD_Actuator_Special_Special_or_iLon_upgrade_pricing"])
				cost = getFloat(row1["CD_Actuator_Special_Special_or_iLon_upgrade_pricing"])
				description = len(row2["CD_Actuator_Special_Special_or_iLon_upgrade_pricing"])
				if price != 0 or cost != 0 or description != 0:
					if price == 0 or cost == 0 or description == 0:
						incomplete.append("cd_actuator_pricing_factory_cost")
	if Product.Name=='TCMI':
		TCMIcon = getContainer("TCMI_Hardware_and_Licenses") 
		for row in TCMIcon.Rows:
			sum1 = getFloat(row["TCMI_Number_of_systems_Upgrading_TCMI_for_TPN_Only"]) + getFloat(row["TCMI_Number_of_systems_Upgrading_TCMI_for_Hybrid_TPN-EPKS"])
			sum2 = getFloat(row["TCMI_Number_of_Front_and_Rear_Access_Upgrade_TCMI"]) + getFloat(row["TCMI_Number_of_Front_Access_Upgrade_TCMI"])
			sum3 = getFloat(row["TCMI_Number_of_NEW_systems_TCMI_for_TPN_Only"]) + getFloat(row["TCMI_Number_of_NEW_systems_TCMI_for_Hybrid_TPN-EPKS"])
			sum4 = getFloat(row["TCMI_Number_of_Front_and_Rear_Access_New_TCMI"]) + getFloat(row["TCMI_Number_of_Front_Access_New_TCMI"])
			break

		if sum1 != sum2:
			incomplete.append("TCMI_Upgrade")
		if sum3 != sum4:
			incomplete.append("TCMI_New")
	if Product.Name == 'FSC to SM IO Migration' :
		check = getFloat(getAttributeValue("ATT_FSCtoSMIOMigrationTotalFSC"))
		flagFscRed = flagFscNonRed = 0
		if check > 0:
			for row in getContainer("FSC_to_SM_IO_Series_1_&_2_FSC_IO_configurations").Rows:
				if getFloat(row["FSC_to_SM_IO_Quantity_of_Cabinets_containing_IO_Rack"]) > 0:
					NonRed = getFloat(row["NON_RED_FSC_to_SM_IO_DI_24VDC"]) + getFloat(row["NON_RED_FSC_to_SM_IO_DI_60VDC"]) + getFloat(row["NON_RED_FSC_to_SM_IO_DI_48VDC"]) + getFloat(row["NON_RED_FSC_to_SM_IO_AI_4_20mA"]) + getFloat(row["NON_RED_FSC_to_SM_IO_DI_IS_(Eex(i))"]) + getFloat(row["NON_RED_FSC_to_SM_IO_DI_IS_(Eex(ii))"]) + getFloat(row["NON_RED_FSC_to_SM_IO_DI_24VDC_10104/1/1"]) + getFloat(row["NON_RED_FSC_to_SM_IO_DO 24VDC_10201/1/1"]) + getFloat(row["NON_RED_FSC_to_SM_IO_FDO_DS_24VDC_10203/1/1"]) + getFloat(row["NON_RED_FSC_to_SM_IO_FDO_DS_24VDC_10203/1/2"]) + getFloat(row["NON_RED_FSC_to_SM_IO_AO_4-20mA_10205/1/1"]) + getFloat(row["NON_RED_FSC_to_SM_IO_DO_24VDC_10206/1/1"]) + getFloat(row["NON_RED_FSC_to_SM_IO_DO_IS_10207/1/1"]) + getFloat(row["NON_RED_FSC_to_SM_IO_RO_10208/1/1"]) + getFloat(row["NON_RED_FSC_to_SM_IO_DO_24VDC_10209/1/1"]) + getFloat(row["NON_RED_FSC_to_SM_IO_DO_24VDC_10212/1/1"]) + getFloat(row["NON_RED_FSC_to_SM_IO_DO_110VDC_10213/1/1"]) + getFloat(row["NON_RED_FSC_to_SM_IO_SDO_60VDC_10213/1/2"]) + getFloat(row["NON_RED_FSC_to_SM_IO_SD_ 48VDC_10213/1/3"]) + getFloat(row["NON_RED_FSC_to_SM_IO_SDOL 220VDC_10214/1/2"]) + getFloat(row["NON_RED_FSC_to_SM_IO_SDO_24VDC_10215/1/1"]) + getFloat(row["NON_RED_FSC_to_SM_IO_SDOL_24VDC_10216/1/1"]) + getFloat(row["NON_RED_FSC_to_SM_IO_SDI_24VDC"]) + getFloat(row["NON_RED_FSC_to_SM_IO_SDI_60VDC_10101/2/2"]) + getFloat(row["NON_RED_FSC_to_SM_IO_SDI_48VDC_10101/2/3"]) + getFloat(row["NON_RED_FSC_to_SM_IO_SAI_10102/2/1"]) + getFloat(row["NON_RED_FSC_to_SM_IO_DI_24VDC_10104/2/1"]) + getFloat(row["NON_RED_FSC_to_SM_IO_AI_10105/2/1"]) + getFloat(row["NON_RED_FSC_to_SM_IO_SDIL_10106/2/1"]) + getFloat(row["NON_RED_FSC_to_SM_IO_SDO_24VDC_10201/2/1"]) + getFloat(row["NON_RED_FSC_to_SM_IO_SAO_10205/2/1"]) + getFloat(row["NON_RED_FSC_to_SM_IO_DO_24VDC_10206/2/1"]) + getFloat(row["NON_RED_FSC_to_SM_IO_RO_10208/2/1"]) + getFloat(row["NON_RED_FSC_to_SM_IO_DO_24VDC_10209/2/1"]) + getFloat(row["NON_RED_FSC_to_SM_IO_SDO_110VDC_10213/2/1"]) + getFloat(row["NON_RED_FSC_to_SM_IO_SDO_60VDC_10213/2/2"]) + getFloat(row["NON_RED_FSC_to_SM_IO_SDO_48VDC_10213/2/3"]) + getFloat(row["NON_RED_FSC_to_SM_IO_SDOL_220VDC_10214/2/2"]) + getFloat(row["NON_RED_FSC_to_SM_IO_SDO_24VDC_10215/2/1"]) + getFloat(row["NON_RED_FSC_to_SM_IO_SDOL_24VDC_10216/2/1"])
					Red = getFloat(row["FSC_to_SM_IO_DI_24VDC"]) + getFloat(row["FSC_to_SM_IO_DI_60VDC"]) + getFloat(row["FSC_to_SM_IO_DI_48VDC"]) + getFloat(row["FSC_to_SM_IO_AI_4_20mA"]) + getFloat(row["FSC_to_SM_IO_DI_IS_(Eex(i))"]) + getFloat(row["FSC_to_SM_IO_DI_IS_(Eex(ii))"]) + getFloat(row["FSC_to_SM_IO_DI_24VDC_10104/1/1"]) + getFloat(row["FSC_to_SM_IO_DO 24VDC_10201/1/1"]) + getFloat(row["FSC_to_SM_IO_FDO_DS_24VDC_10203/1/1"]) + getFloat(row["FSC_to_SM_IO_FDO_DS_24VDC_10203/1/2"]) + getFloat(row["FSC_to_SM_IO_AO_4-20mA_10205/1/1"]) + getFloat(row["FSC_to_SM_IO_DO_24VDC_10206/1/1"]) + getFloat(row["FSC_to_SM_IO_DO_IS_10207/1/1"]) + getFloat(row["FSC_to_SM_IO_RO_10208/1/1"]) + getFloat(row["FSC_to_SM_IO_DO_24VDC_10209/1/1"]) + getFloat(row["FSC_to_SM_IO_DO_24VDC_10212/1/1"]) + getFloat(row["FSC_to_SM_IO_DO_110VDC_10213/1/1"]) + getFloat(row["FSC_to_SM_IO_SDO_60VDC_10213/1/2"]) + getFloat(row["FSC_to_SM_IO_SD_ 48VDC_10213/1/3"]) + getFloat(row["FSC_to_SM_IO_SDOL 220VDC_10214/1/2"]) + getFloat(row["FSC_to_SM_IO_SDO_24VDC_10215/1/1"]) + getFloat(row["FSC_to_SM_IO_SDOL_24VDC_10216/1/1"]) + getFloat(row["FSC_to_SM_IO_SDI_24VDC"]) + getFloat(row["FSC_to_SM_IO_SDI_60VDC_10101/2/2"]) + getFloat(row["FSC_to_SM_IO_SDI_48VDC_10101/2/3"]) + getFloat(row["FSC_to_SM_IO_SAI_10102/2/1"]) + getFloat(row["FSC_to_SM_IO_DI_24VDC_10104/2/1"]) + getFloat(row["FSC_to_SM_IO_AI_10105/2/1"]) + getFloat(row["FSC_to_SM_IO_SDIL_10106/2/1"]) + getFloat(row["FSC_to_SM_IO_SDO_24VDC_10201/2/1"]) + getFloat(row["FSC_to_SM_IO_SAO_10205/2/1"]) + getFloat(row["FSC_to_SM_IO_DO_24VDC_10206/2/1"]) + getFloat(row["FSC_to_SM_IO_RO_10208/2/1"]) + getFloat(row["FSC_to_SM_IO_DO_24VDC_10209/2/1"]) + getFloat(row["FSC_to_SM_IO_SDO_110VDC_10213/2/1"]) + getFloat(row["FSC_to_SM_IO_SDO_60VDC_10213/2/2"]) + getFloat(row["FSC_to_SM_IO_SDO_48VDC_10213/2/3"]) + getFloat(row["FSC_to_SM_IO_SDOL_220VDC_10214/2/2"]) + getFloat(row["FSC_to_SM_IO_SDO_24VDC_10215/2/1"]) + getFloat(row["FSC_to_SM_IO_SDOL_24VDC_10216/2/1"]) + getFloat(row["FSC_to_SM_IO_SDOL_48VDC_10216/2/3"])
					if getFloat(row["FSC_to_SM_IO_Number_of_IO_Racks"]) == 0 and Red>0:
						flagFscRed += 1
					if getFloat(row["NON_RED_FSC_to_SM_IO_Number_of_IO_Racks"]) == 0 and NonRed>0:
						flagFscNonRed += 1

		if flagFscRed > 0:
			incomplete1.append("flagFscRed")
		if flagFscNonRed > 0:
			incomplete1.append("flagFscNonRed")


	if Product.Name == 'FDM Upgrade 2':
		check = getAttributeValue("FDM_Upgrade_Additional_Components")
		if str(getAttributeValue("FDM_Upgrade_Do_you_want_to_upgrade_this_FDM")) == "Yes" and getAttributeValue("Attr_FDM_Upg1ServerDevicePoints") in ['0', None, ''] and getAttributeValue("Attr_FDMUpg1_AuditTrailDev") in ['0', None, ''] and getAttributeValue("Attr_FDMUpg1_RCIs_incExperion") in ['0', None, ''] and getAttributeValue("Attr_FDMUpg1_RCIs_excExperion") in ['0', None, ''] and getAttributeValue("Attr_FDM_Upg1_TotalFDMClients") in ['0', None, '']:
			incomplete1.append("FDMflag2")

		if check == "Yes" and getAttributeValue("FDM_Upgrade_Are_additional_components_required") == "Yes" and getAttributeValue("Attr_FDM_Upg_devmanaged") in ['0', None, ''] and getAttributeValue("Attr_FDM_Upg_AuditTrailDev") in ['0', None, ''] and getAttributeValue("Attr_FDMUpg_FDMClients") in ['0', None, ''] and getAttributeValue("Attr_Experion/TPS_Servers_FDMInt") in ['0', None, ''] and getAttributeValue("Attr_ServerNetInterfaceLic") in ['0', None, '']:
			incomplete1.append("FDMaddflag2")

	if Product.Name == 'FDM Upgrade 3':
		#check = getAttributeValue("FDM_Upgrade_Additional_Components")
		if str(getAttributeValue("FDM_Upgrade_Do_you_want_to_upgrade_this_FDM")) == "Yes" and getAttributeValue("Attr_FDM_Upg1ServerDevicePoints") in ['0', None, ''] and getAttributeValue("Attr_FDMUpg1_AuditTrailDev") in ['0', None, ''] and getAttributeValue("Attr_FDMUpg1_RCIs_incExperion") in ['0', None, ''] and getAttributeValue("Attr_FDMUpg1_RCIs_excExperion") in ['0', None, ''] and getAttributeValue("Attr_FDM_Upg1_TotalFDMClients") in ['0', None, '']:
			incomplete1.append("FDMflag3")

		#if check == "Yes" and getAttributeValue("FDM_Upgrade_Are_additional_components_required") == "Yes" and getAttributeValue("Attr_FDM_Upg_devmanaged") in ['0', None, ''] and getAttributeValue("Attr_FDM_Upg_AuditTrailDev") in ['0', None, ''] and getAttributeValue("Attr_FDMUpg_FDMClients") in ['0', None, ''] and getAttributeValue("Attr_Experion/TPS_Servers_FDMInt") in ['0', None, ''] and getAttributeValue("Attr_ServerNetInterfaceLic") in ['0', None, '']:

	
	if Product.Attributes.GetByName('Incomplete'):
		Product.Attr('Incomplete').AssignValue(",".join(incomplete))
	if Product.Attributes.GetByName('Incomplete1'):
		
		Product.Attr('Incomplete1').AssignValue(",".join(incomplete1))