country = Quote.GetCustomField('Account Address Country').Content
isR2Qquote = True if Quote.GetCustomField("isR2QRequest").Content else False
def getContainer(Name):
	return Product.GetContainerByName(Name)
##EBR Product
if Product.Name == 'EBR':
	ebrBasicInfo = Product.GetContainerByName('EBR_Basic_Information')
	attributeebr = Product.Attr('EBR_If_hardware_desired_select_host_type')
	for Row in ebrBasicInfo.Rows:
		if Row['EBR_Future_EBR_Release'] == 'R520':
			attributeebr = Product.Attr('EBR_If_hardware_desired_select_host_type')
			for value in attributeebr.Values:
				if value.Display in ('DELL T150 STD TPM','DELL T550 STD TPM','DELL T550 STD No TPM','DELL R250XE STD TPM','DELL R450 STD TPM','Dell R740XL', 'HP DL360 G10','DELL R450 STD No TPM','HP DL320 G11','Dell PE T160','Dell PE T360','Dell PE R260','Dell PE R360'):
					value.Allowed = True
			break
	for values in attributeebr.Values:
		if country != 'china':
			if values.Display in ('DELL T550 STD No TPM','DELL R450 STD No TPM'):
				values.Allowed = False
#ELCN
if Product.Name == 'ELCN':
	elcnUpgradeNewElcnNodesCon =  Product.GetContainerByName('ELCN_Upgrade_New_ELCN_Nodes')
	totalQtyOfNetworkGateway = 0
	rowAssetDB = 2
	rowIndex = 0
	for row in elcnUpgradeNewElcnNodesCon.Rows:
		if rowIndex != rowAssetDB:
			for column in row.Columns:
				if row[column.Name] != '' and column.Name == "ELCN_Qty_of_Network_Gateways":
					totalQtyOfNetworkGateway += int(row[column.Name])
		rowIndex += 1
	if totalQtyOfNetworkGateway < 2:
		attributelcn = Product.Attr('ELCN_Select_Switch_configuration_required')
		for value in attributelcn.Values:
			if value.Display == 'Responsible - Alternate configuration':
				value.Allowed = False
	else:
		attributelcn = Product.Attr('ELCN_Select_Switch_configuration_required')
		for value in attributelcn.Values:
			if value.Display == 'Responsible - Alternate configuration':
				value.Allowed = True
#FDM Upgrade 1
if Product.Name == 'FDM Upgrade 1' or Product.Name == 'FDM Upgrade 2' or Product.Name == 'FDM Upgrade 3':
	attr =  Product.Attr('FDM_Upgrade_Select_desired_FDM_release')
	attr1 =  Product.Attr('FDM_Upgrade_What_is_the_current_release').GetValue()
	'''if attr1 in ("FDM R440 or Lower",""):
		for value in attr.Values:
			if value.Display == "FDM R520":
				value.Allowed = False
			if value.Display in ("FDM R501","FDM R511"):
				value.Allowed = True'''
	if attr1 in ("FDM R450","FDM R500","FDM R501","FDM R511",""):
		for value in attr.Values:
			if value.Display in ("FDM R520","FDM R521","FDM R530","FDM R540"):
				value.Allowed = True
	if attr1 in ("FDM R520"):
		for value in attr.Values:
			if value.Display in ("FDM R521","FDM R530","FDM R540"):
				value.Allowed = True
			if value.Display == "FDM R520":
				value.Allowed = False
	if attr1 in ("FDM R521"):
		for value in attr.Values:
			if value.Display in ("FDM R520","FDM R521"):
				value.Allowed = False
			if value.Display in ("FDM R530","FDM R540"):
				value.Allowed = True
	if attr1 in ("FDM R530"):
		for value in attr.Values:
			if value.Display in ("FDM R520","FDM R521","FDM R530"):
				value.Allowed = False
			if value.Display in ("FDM R540"):
				value.Allowed = True

#EHPM/EHPMX/ C300PM
if Product.Name == 'EHPM/EHPMX/ C300PM':
	eNBMigrationConfigCont = Product.GetContainerByName('ENB_Migration_Config_Cont')
	xPMMigrationGeneralQnsCont = Product.GetContainerByName('xPM_Migration_General_Qns_Cont')
	xPMMigratonScenarioCont = Product.Attr('xPM_Select_the_migration_scenario').GetValue()
	listOfEHPMOptions = ['UPG PM/APM TO 7-SLOT EHPM Non RED With IOL','UPG PM/APM TO 15-SLOT EHPM Non RED With IOL','UPG PM/APM TO 7-SLOT EHPM RED With IOL','UPG PM/APM TO 15-SLOT EHPM RED With IOL','UPG HPM TO EHPM Non RED With IOL','UPG HPM TO EHPM RED With IOL','UPG HPM TO EHPM Non RED Without IOL','UPG HPM TO EHPM RED Without IOL']
	listOfC300PMOptions = ['Non-redundant PM/APM to C300PM in 7-slot chassis', 'Non-redundant PM/APM to C300PM in 15-slot chassis', 'Redundant PM/APM to C300PM in 7-slot chassis', 'Redundant PM/APM to C300PM in15-slot chassis', 'Non-redundant HPM to C300PM', 'Redundant HPM to C300PM', 'Non-redundant EHPM to C300PM', 'Redundant EHPM to C300PM','Non-redundant EHPMX to C300PM','Redundant EHPMX to C300PM']
	listOfEHPMXOptions = ["Non-redundant PM/APM to EHPMX in 7-slot chassis", "Non-redundant PM/APM to EHPMX in 15-slot chassis", "Redundant PM/APM to EHPMX in 7-slot chassis", "Redundant PM/APM to EHPMX in15-slot chassis", "Non-redundant HPM to EHPMX", "Redundant HPM to EHPMX", "Non-redundant EHPM to EHPMX", "Redundant EHPM to EHPMX"]
	C300list = ['Redundant HPM to C300PM','Redundant EHPM to C300PM','Redundant EHPMX to C300PM']
	EHPMXlist = ['Redundant HPM to EHPMX', 'Redundant EHPM to EHPMX']
	xPMMigrationConfigCont = Product.GetContainerByName('xPM_Migration_Config_Cont')
	if xPMMigrationGeneralQnsCont.Rows.Count > 0:
		row = xPMMigrationGeneralQnsCont.Rows[0]
		if row["xPM_On_Process_Red_HPMs_or_Off_Process_Migration"] == "HPM to EHPM On Process" or row["xPM_On_Process_Red_HPMs_EHPMs_only"] == "HPM/EHPM to C300PM On Process":
			for rowENB in eNBMigrationConfigCont.Rows:
				attribute = rowENB.GetColumnByName("xPM_What_is_the_NIM_migration_scenario").ReferencingAttribute
				for value in attribute.Values:
					if value.Display == 'Non Redundant NIM to ENB':
						value.Allowed = False
		else:
			for rowENB in eNBMigrationConfigCont.Rows:
				attribute = rowENB.GetColumnByName("xPM_What_is_the_NIM_migration_scenario").ReferencingAttribute
				for value in attribute.Values:
					if value.Display == 'Non Redundant NIM to ENB':
						value.Allowed = True
		if row['xPM_On_Process_Red_HPMs_EHPMs_only'] == 'HPM/EHPM/EHPMX to C300PM On Process':
			for row in xPMMigrationConfigCont.Rows:
				attribute = row.GetColumnByName("xPM_Migration_Scenario").ReferencingAttribute
				z =sum([listOfEHPMOptions,listOfC300PMOptions,listOfEHPMXOptions],[])
				for value in attribute.Values:
					if value.Display in C300list:
						value.Allowed = True
					elif value.Display in z:
						value.Allowed = False 
		elif row['xPM_On_Process_Red_HPMs_EHPMs_for_EHPMX_mig'] == 'HPM/EHPM to EHPMX On Process':
			for row in xPMMigrationConfigCont.Rows:
				attribute = row.GetColumnByName("xPM_Migration_Scenario").ReferencingAttribute
				z =sum([listOfEHPMOptions,listOfC300PMOptions,listOfEHPMXOptions],[])
				for value in attribute.Values:
					if value.Display in EHPMXlist:
						value.Allowed = True
					elif value.Display in z:
						value.Allowed = False
		if xPMMigratonScenarioCont == 'xPM to C300PM':
			for row in xPMMigrationConfigCont.Rows:
				attribute = row.GetColumnByName("xPM_Migration_Scenario").ReferencingAttribute
				z =sum([listOfEHPMOptions,listOfEHPMXOptions],[])
				for value in attribute.Values:
					if value.Display in listOfC300PMOptions:
						value.Allowed = True
					elif value.Display in z:
						value.Allowed = False
				if row['xPM_Migration_Scenario'] not in listOfC300PMOptions or not row['xPM_Migration_Scenario']:
					for col in row.Columns:
						if col.Name == 'xPM_Migration_Scenario':
							col.SetAttributeValue("Non-redundant PM/APM to C300PM in 7-slot chassis")
							row['xPM_Migration_Scenario'] = "Non-redundant PM/APM to C300PM in 7-slot chassis"
							break
		elif xPMMigratonScenarioCont == 'xPM to EHPM':
			for row in xPMMigrationConfigCont.Rows:
				attribute = row.GetColumnByName("xPM_Migration_Scenario").ReferencingAttribute
				z =sum([listOfC300PMOptions,listOfEHPMXOptions],[])
				for value in attribute.Values:
					if value.Display in listOfEHPMOptions:
						value.Allowed = True
					elif value.Display in z:
						value.Allowed = False
				if row['xPM_Migration_Scenario'] not in listOfEHPMOptions or not row['xPM_Migration_Scenario']:
					for col in row.Columns:
						if col.Name == 'xPM_Migration_Scenario':
							col.SetAttributeValue("UPG PM/APM TO 7-SLOT EHPM Non RED With IOL")
							row['xPM_Migration_Scenario'] = "UPG PM/APM TO 7-SLOT EHPM Non RED With IOL"
							break
		elif xPMMigratonScenarioCont == 'xPM to EHPMX':
			for row in xPMMigrationConfigCont.Rows:
				attribute = row.GetColumnByName("xPM_Migration_Scenario").ReferencingAttribute
				z =sum([listOfC300PMOptions,listOfEHPMOptions],[])
				for value in attribute.Values:
					if value.Display in listOfEHPMXOptions:
						value.Allowed = True
					elif value.Display in z:
						value.Allowed = False
				if row['xPM_Migration_Scenario'] not in listOfEHPMXOptions or not row['xPM_Migration_Scenario']:
					for col in row.Columns:
						if col.Name == 'xPM_Migration_Scenario':
							col.SetAttributeValue("Non-redundant PM/APM to EHPMX in 7-slot chassis")
							row['xPM_Migration_Scenario'] = "Non-redundant PM/APM to EHPMX in 7-slot chassis"
							break

#LM to ELMM ControlEdge PLC
if Product.Name == 'LM to ELMM ControlEdge PLC':
	for row in Product.GetContainerByName('LM_to_ELMM_ControlEdge_PLC_Cont').Rows:
		attribute = row.GetColumnByName("LM_select_IO_network_topology").ReferencingAttribute
		if row["LM_are_the_IO_Racks_remotely_located"] in [""]:
			row["LM_are_the_IO_Racks_remotely_located"] = "No"
		if row["LM_are_the_IO_Racks_remotely_located"] in ["Yes - Local and Remote", "Yes - Only Remote"]:
			for value in attribute.Values:
				value.Allowed = False if value.Display == "Ring" else True
				row.Product.Attr("LM_select_IO_network_topology").SelectDisplayValue("Star")
			switch_attribute = row.GetColumnByName("LM_select_type_of_Switch_for_the_IO_network").ReferencingAttribute
			for val in switch_attribute.Values:
				val.Allowed = False if val.Display == "NA" else True
				if(row["LM_select_type_of_Switch_for_the_IO_network"] not in ("Single Mode Redundant","Single Mode Non-Redundant", "Multimode Non-Redundant")):
					row.Product.Attr("LM_select_type_of_Switch_for_the_IO_network").SelectDisplayValue("Multimode Redundant")
					row.ApplyProductChanges()
		else:
			for value in attribute.Values:
				value.Allowed = True
		attribute = row.GetColumnByName("LM_select_type_of_Switch_for_the_IO_network").ReferencingAttribute
		if row["LM_select_IO_network_topology"] in ["Ring"]:
			for value in attribute.Values:
				value.Allowed = True if value.Display == "NA" else False
				row.Product.Attr("LM_select_type_of_Switch_for_the_IO_network").SelectDisplayValue("NA")
		else:
			for value in attribute.Values:
				if(row["LM_select_type_of_Switch_for_the_IO_network"] not in ("Single Mode Redundant","Single Mode Non-Redundant", "Multimode Non-Redundant")):
					row.Product.Attr("LM_select_type_of_Switch_for_the_IO_network").SelectDisplayValue("")
					if not isR2Qquote:
						value.Allowed = False if value.Display == "NA" else True
						row.Product.Attr("LM_select_type_of_Switch_for_the_IO_network").SelectDisplayValue("Multimode Redundant")
					
		row.ApplyProductChanges()

#xPM to C300 Migration 
if Product.Name == 'xPM to C300 Migration':
	attr1 = Product.Attr('Power System Type')
	attr = Product.Attr('Power System Vendor').GetValue()
	if attr == 'Meanwell' or attr == 'Phoenix Contact':
		for value in attr1.Values:
			if value.Display in ('Redundant with BBU 20A','Redundant 40A','Non Redundant 40A'):
				value.Allowed = False
			if value.Display in ('Redundant 20A','Non Redundant 20A'):
				value.Allowed = True
	if attr == 'TDI':
		for value in attr1.Values:
			if value.Display in ('Redundant with BBU 20A','Redundant 40A','Non Redundant 40A','Redundant 20A','Non Redundant 20A'):
				value.Allowed = True
	attr2 = Product.Attr('ATT_XPMC300PST')
	attr3 = Product.Attr('ATT_XPMC300PSV').GetValue()
	if attr3 == 'Meanwell' or attr3 == 'Phoenix Contact':
		for value in attr2.Values:
			if value.Display in ('Redundant with BBU 20A','Redundant 40A','Non Redundant 40A'):
				value.Allowed = False
			if value.Display in ('Redundant 20A','Non Redundant 20A'):
				value.Allowed = True
	if attr3 == 'TDI':
		for value in attr2.Values:
			if value.Display in ('Redundant with BBU 20A','Redundant 40A','Non Redundant 40A','Redundant 20A','Non Redundant 20A'):
				value.Allowed = True

#C200 Migration
if Product.Name == 'C200 Migration':
	C200MigrationGeneralQnsCon = Product.GetContainerByName('C200_Migration_General_Qns_Cont')
	C200MigrationConfigCont = Product.GetContainerByName('C200_Migration_Config_Cont')
	C200MigrationScenario = Product.Attr('C200_Select_Migration_Scenario').GetValue()
	scope = Product.Attr('Scope').GetValue()
	if not isR2Qquote:
		if C200MigrationScenario == 'C200 to C300':
			for rowENB in C200MigrationGeneralQnsCon.Rows:
				attribute = rowENB.GetColumnByName("C200_Connection _to_Experion_Server").ReferencingAttribute
				for value in attribute.Values:
					if value.Display == 'Dual Ethernet':
						value.Allowed = False
				break
		elif C200MigrationScenario == 'C200 to ControlEdge UOC':
			for rowENB in C200MigrationGeneralQnsCon.Rows:
				attribute = rowENB.GetColumnByName("C200_Connection _to_Experion_Server").ReferencingAttribute
				for value in attribute.Values:
					x = value
					if value.Display == 'Dual Ethernet':
						value.Allowed = True
				break
			
		if C200MigrationScenario == 'C200 to C300':
			for rowENB in C200MigrationConfigCont.Rows:
				attribute = rowENB.GetColumnByName("C200_peer_to_peer_communication").ReferencingAttribute
				for value in attribute.Values:
					if value.Display in ('Allen Bradley PLC L2 connected','Allen Bradley PLC over ControlNet','C200 across cluster over ControlNet','C200 within same cluster'):
						value.Allowed = False
					if value.Display in ('C200','Allen Bradley PLC'):
						value.Allowed = True
		elif C200MigrationScenario == 'C200 to ControlEdge UOC':
			for rowENB in C200MigrationConfigCont.Rows:
				attribute = rowENB.GetColumnByName("C200_peer_to_peer_communication").ReferencingAttribute
				for value in attribute.Values:
					if value.Display in ('Allen Bradley PLC L2 connected','Allen Bradley PLC over ControlNet','C200 across cluster over ControlNet','C200 within same cluster'):
						value.Allowed = True
					if value.Display in ('C200','Allen Bradley PLC'):
						value.Allowed = False
		
	else:
		
		if C200MigrationScenario == 'C200 to C300':
			for rowENB in C200MigrationGeneralQnsCon.Rows:
				attribute = rowENB.GetColumnByName("C200_Connection _to_Experion_Server").ReferencingAttribute
				for value in attribute.Values:
					if value.Display == 'Dual Ethernet':
							
						value.Allowed = True
				break
			for rowENB in C200MigrationConfigCont.Rows:
				attribute = rowENB.GetColumnByName("C200_peer_to_peer_communication").ReferencingAttribute
				for value in attribute.Values:
					if value.Display in ('Allen Bradley PLC L2 connected','Allen Bradley PLC over ControlNet','C200 across cluster over ControlNet','C200 within same cluster'):
						value.Allowed = False
					if value.Display in ('C200','Allen Bradley PLC'):
						value.Allowed = True
				rowENB.Calculate()
		elif C200MigrationScenario == 'C200 to ControlEdge UOC':
			for rowENB in C200MigrationGeneralQnsCon.Rows:
				attribute = rowENB.GetColumnByName("C200_Connection _to_Experion_Server").ReferencingAttribute
				for value in attribute.Values:
					x = value
					if value.Display == 'Dual Ethernet':
							
						value.Allowed = True
				
			for rowENB in C200MigrationConfigCont.Rows:
				attribute = rowENB.GetColumnByName("C200_peer_to_peer_communication").ReferencingAttribute
				for value in attribute.Values:
					if value.Display in ('Allen Bradley PLC L2 connected','Allen Bradley PLC over ControlNet','C200 across cluster over ControlNet','C200 within same cluster'):
						value.Allowed = False
					if value.Display in ('C200','Allen Bradley PLC'):
						value.Allowed = True
				rowENB.Calculate()
	if C200MigrationScenario == 'C200 to C300':
		for rowENB in C200MigrationConfigCont.Rows:
			attribute = rowENB.GetColumnByName("C200_Existing_PM_or_Non_Standard_Cabinet_Used").ReferencingAttribute
			if(rowENB["C200_Cabinet_type_customer_plans"] not in ("New Front & Rear Access Series C Cabinet","New Front Access Only Series C Cabinet")):
				for value in attribute.Values:
					value.Allowed = False if value.Display == "NA" else True
				if rowENB.Product.Attr("C200_Existing_PM_or_Non_Standard_Cabinet_Used").GetValue() not in ("New Front Access Only Series C Cabinet"):
					rowENB.Product.Attr("C200_Existing_PM_or_Non_Standard_Cabinet_Used").SelectDisplayValue("New Front & Rear Access Series C Cabinet")
					rowENB.ApplyProductChanges()
			elif(rowENB["C200_Cabinet_type_customer_plans"] in ("New Front & Rear Access Series C Cabinet","New Front Access Only Series C Cabinet")):
				for value in attribute.Values:
					value.Allowed = True if value.Display == "NA" else False
				rowENB.Product.Attr("C200_Existing_PM_or_Non_Standard_Cabinet_Used").SelectDisplayValue("NA")
				rowENB.ApplyProductChanges()
			rowENB.Calculate()
	if C200MigrationScenario == 'C200 to C300' and scope != 'HW/SW':
		attribute = Product.Attr('C200_Documentation_Required')
		for value in attribute.Values:
			if value.Display in ('DDS','DDS & Network Drawing'):
				value.Allowed = False
			if value.Display in ('Yes'):
				value.Allowed =True
	elif C200MigrationScenario == 'C200 to ControlEdge UOC' and scope != 'HW/SW':
		attribute1 = Product.Attr('C200_Documentation_Required')
		for value in attribute1.Values:
			if value.Display in ('DDS','DDS & Network Drawing'):
				value.Allowed = True
			if value.Display in ('Yes'):
				value.Allowed =False
	attr2 = Product.Attr('Power System Type')
	attr = Product.Attr('Power System Vendor').GetValue()
	if attr == 'Meanwell' or attr == 'Phoenix Contact':
		for value in attr2.Values:
			if value.Display in ('Redundant with BBU 20A','Redundant 40A','Non Redundant 40A'):
				value.Allowed = False
			if value.Display in ('Redundant 20A','Non Redundant 20A'):
				value.Allowed = True
	if attr == 'TDI':
		for value in attr2.Values:
			if value.Display in ('Redundant with BBU 20A','Redundant 40A','Non Redundant 40A','Redundant 20A','Non Redundant 20A'):
				value.Allowed = True
	attr1 = Product.Attr('ATT_C200C300PST')
	attr3 = Product.Attr('ATT_C200C300PSV').GetValue()
	if attr3 == 'Meanwell' or attr3 == 'Phoenix Contact':
		for value in attr1.Values:
			if value.Display in ('Redundant with BBU 20A','Redundant 40A','Non Redundant 40A'):
				value.Allowed = False
			if value.Display in ('Redundant 20A','Non Redundant 20A'):
				value.Allowed = True
	if attr3 == 'TDI':
		for value in attr1.Values:
			if value.Display in ('Redundant with BBU 20A','Redundant 40A','Non Redundant 40A','Redundant 20A','Non Redundant 20A'):
				value.Allowed = True

#TPS to Experion
if Product.Name == 'TPS to Experion':
	con = Product.GetContainerByName('TPS_EX_Additional_Stations')
	cont = Product.Attr('TPS_EX_Additional_Server_Stations_Required').GetValue()
	if(cont == "Yes"):
		for row in con.Rows:
			if(row["TPS_EX_Additional_Stations_Type"] in ("Flex Station - Cabinet","Console Station - Cabinet","Console Extended Station - Cabinet","ES-T Station - Cabinet")):
				attribute = row.GetColumnByName("TPS_EX_Additional_Stations_Cabinat_Hardware").ReferencingAttribute
				for value in attribute.Values:
					value.Allowed = False if value.Display in ("HP Z4 G4") else True


			elif(row["TPS_EX_Additional_Stations_Type"] in ("Console Station - Orion","Console Extended Station - Orion","Flex Station - Orion","ES-T Station - Orion")):
				attribute = row.GetColumnByName("TPS_EX_Additional_Stations_Cabinat_Hardware").ReferencingAttribute
				for value in attribute.Values:
					value.Allowed = False if value.Display in ("Dell R7920XL RAID") else True

			elif(row["TPS_EX_Additional_Stations_Type"] == "ES-T Station - Desk"):
				attribute = row.GetColumnByName("TPS_EX_Additional_Stations_Desk_Hardware").ReferencingAttribute
				for value in attribute.Values:
					value.Allowed = False if value.Display in ("Dell OptiPlex XE3") else True
			elif(row["TPS_EX_Additional_Stations_Type"] in ("Flex Station - Cabinet","Console Station - Cabinet","Console Extended Station - Cabinet","ES-T Station - Cabinet")):
				attribute = row.GetColumnByName("TPS_EX_Additional_Stations_RPS_Mounting_Furniture").ReferencingAttribute
				if (row["TPS_EX_Additional_Stations_RPS_Type"] in ("P&F BTC12 – Dual Video Thin Client","P&F BTC14 – Quad Video Thin Client","WYSE 5070 - Thin Client for 5+ displays")):
					for value in attribute.Values:
						value.Allowed = False if value.Display not in ("NA") else True
				else:
					for value in attribute.Values:
						value.Allowed = True if value.Display not in ("NA") else False
			else:
				attribute = row.GetColumnByName("TPS_EX_Additional_Stations_RPS_Type").ReferencingAttribute
				for value in attribute.Values:
					value.Allowed = False if value.Display in ("WYSE 5070 - Thin Client","WYSE 5070 - Universal Thin Client") else True
	con1 = Product.GetContainerByName('TPS_EX_Additional_Servers')
	ExRel = Product.Attr('MSID_Future_Experion_Release').GetValue()
	if ExRel in ('R501','R511','R510'):
		for row in con1.Rows:
			attribute_1 = row.GetColumnByName("TPS_EX_Additional_Server_Hardware").ReferencingAttribute
			for value in attribute_1.Values:
				if value.Display in ('Dell T340 Standard RAID','Dell T340 Performance','Dell R240XL','Dell R340XL','DELL T250XE STD TPM','DELL T150 STD TPM','DELL R250XE STD TPM'):
					value.Allowed = False
				if value.Display in ('DELL T550 STD TPM','DELL T550 STD No TPM','DELL T450 STD TPM','DELL T450 STD No TPM','Dell R740XL','Dell XR11'):
					value.Allowed = True
	elif ExRel == 'R520':
		for row in con1.Rows:
			attribute_1 = row.GetColumnByName("TPS_EX_Additional_Server_Hardware").ReferencingAttribute
			for value in attribute_1.Values:
				if value.Display in ('Dell T340 Standard RAID','Dell T340 Performance','Dell R240XL','Dell R340XL'):
					value.Allowed = False
				if value.Display in ('HP DL 320 G11','DELL T150 STD TPM','DELL T550 STD TPM','DELL T550 STD No TPM','DELL T250XE STD TPM','DELL T450 STD TPM','DELL T450 STD No TPM','Dell R740XL','Dell XR11','DELL R250XE STD TPM'):
					value.Allowed = True
	for Row1 in con1.Rows:
		attributeebr = Row1.GetColumnByName('TPS_EX_Additional_Server_Hardware').ReferencingAttribute
		for values in attributeebr.Values:
			if country != 'china':
				if values.Display in ('DELL T550 STD No TPM','DELL R450 STD No TPM'):
					values.Allowed = False
	if(cont == "Yes"):
		for row in con1.Rows:
			attribute_1 = row.GetColumnByName("TPS_EX_Addtional_Server_Additional_Hard_Drive").ReferencingAttribute
			attribute_2 = row.GetColumnByName("TPS_EX_Additional_Server_Additional_Memory").ReferencingAttribute
			if (row["TPS_EX_Additional_Server_Hardware"] in ("DELL T150 STD TPM","DELL T550 STD TPM","DELL T550 STD No TPM","DELL T250XE STD TPM","DELL T450 STD TPM","DELL T450 STD No TPM")):
				for value_1 in attribute_1.Values:
					value_1.Allowed = False if value_1.Display not in ("NA") else True
				for value_2 in attribute_2.Values:
					value_2.Allowed = False if value_2.Display not in ("NA") else True
				row.Product.Attr("TPS_EX_Additional_Server_Additional_Memory").SelectDisplayValue("NA")
				row.Product.Attr("TPS_EX_Additional_Hard_Drives").SelectDisplayValue("NA")
				row.ApplyProductChanges()
			else:
				for value_1 in attribute_1.Values:
					value_1.Allowed = True if value_1.Display not in ("NA") else False
				for value_2 in attribute_2.Values:
					value_2.Allowed = True if value_2.Display not in ("NA") else False
				if row['TPS_EX_Additional_Server_Additional_Memory'] == 'NA':
					row.Product.Attr("TPS_EX_Additional_Server_Additional_Memory").SelectDisplayValue("None")
				if row['TPS_EX_Addtional_Server_Additional_Hard_Drive'] == 'NA':
					row.Product.Attr("TPS_EX_Additional_Hard_Drives").SelectDisplayValue("No")
				row.ApplyProductChanges()
	con2 = getContainer('TPS_EX_Conversion_ACET_EAPP')
	for row in con2.Rows:
		attribute = row.GetColumnByName("TPS_EX_Conversion_ACET_EAPP_Server_Hardware").ReferencingAttribute
		for value in attribute.Values:
			if (not isR2Qquote and ((row["TPS_EX_Conversion_ACET_EAPP_Type"] == "APP to ACE-T" and value.Display in ("HP DL 320 G11", "DELL R740XL")) or (row["TPS_EX_Conversion_ACET_EAPP_Type"] == "APP to EAPP" and value.Display in ("HP DL 320 G11", "DELL T550 STD TPM", "DELL T550 STD No TPM", "DELL R740XL") and country in ('china', 'China')) or (row["TPS_EX_Conversion_ACET_EAPP_Type"] == "APP to EAPP" and value.Display in ("HP DL 320 G11", "DELL T550 STD TPM", "DELL R740XL") and country not in ('china', 'China')))) or (isR2Qquote and ((row["TPS_EX_Conversion_ACET_EAPP_Type"] == "APP to ACE-T" and value.Display == "HP DL 320 G11") or (row["TPS_EX_Conversion_ACET_EAPP_Type"] == "APP to EAPP" and value.Display in ("HP DL 320 G11", "DELL T550 STD TPM")))) :
				value.Allowed = True
			else:
				value.Allowed = False
	estCon = getContainer('TPS_EX_Station_Conversion_EST')
	acetCon = getContainer('TPS_EX_Conversion_ACET_EAPP')
	addSerCon = getContainer('TPS_EX_Additional_Servers')
	for row in estCon.Rows:
		EX_FMF = row.GetColumnByName("TPS_EX_Future_Mounting_Furniture").ReferencingAttribute
		EX_RES = row.GetColumnByName("TPS_EX_RPS_Type").ReferencingAttribute
		con_type = row['TPS_EX_Station_Conversion_Type']
		attr1 = row.GetColumnByName("TPS_EX_Hardware").ReferencingAttribute
		for value in attr1.Values :
			if ExRel not in('R520','R530'):
				if value.Display in ('HP Z4 G4 MLK','HP Z4 G5','Dell T5860XL','Dell R7960XL'):
					value.Allowed = False
				else:
					value.Allowed = True
			elif ExRel == 'R530':
				if con_type == 'UGUS to ES-T':
					if value.Display in ('Dell T5860XL','HP Z4 G5'):
						value.Allowed = True
					else:
						value.Allowed = False
				else:
					if value.Display in ('Dell T5860XL','HP Z4 G5','Dell R7960XL'):
						value.Allowed = True
					else:
						value.Allowed = False
			
			else:
				if value.Display in ('HP Z4 G4 MLK','DELL R7920XL RAID','DELL T5820XL'):
					value.Allowed = True
				else:
					value.Allowed = False
			if isR2Qquote :
				value.Allowed = True if value.Display in ('Dell T5860XL','HP Z4 G5','Dell R7960XL') else False
			row.ApplyProductChanges()
		row.ApplyProductChanges()

	hardwareValues=['Dell Optiplex XE4','Dell R7960XL','HP Z4 G5','Dell T5860XL']
	for row in con.Rows:
		flag = True if ExRel == 'R530'and cont == "Yes" else False
		if(row["TPS_EX_Additional_Stations_Type"] in ("Flex Station - Cabinet","Console Station - Cabinet","Console Extended Station - Cabinet","ES-T Station - Cabinet","Console Station - Orion","Console Extended Station - Orion","Flex Station - Orion","ES-T Station - Orion")):
			attr1 = row.GetColumnByName("TPS_EX_Additional_Stations_Cabinat_Hardware").ReferencingAttribute
			for value in attr1.Values:
				value.Allowed = True if value.Display in hardwareValues and flag else True if value.Display not in hardwareValues and flag==False else False
		elif(row["TPS_EX_Additional_Stations_Type"] in ("Console Station - Desk","Console Extended Station - Desk","Flex Station - Desk","ES-T Station - Desk")):
			attr2 = row.GetColumnByName("TPS_EX_Additional_Stations_Desk_Hardware").ReferencingAttribute
			for value in attr2.Values:
				value.Allowed = True if value.Display in hardwareValues and flag else True if value.Display not in hardwareValues and flag==False else False
	row.ApplyProductChanges()
	containerList=[acetCon,addSerCon]
	containerAttrMap={
		"TPS_EX_Conversion_ACET_EAPP":"TPS_EX_Conversion_ACET_EAPP_Server_Hardware",
		"TPS_EX_Additional_Servers":"TPS_EX_Additional_Server_Hardware"
	}
	flag=True
	for container in containerList:
		columName=containerAttrMap[container.Name]
		flag=False if( columName=="TPS_EX_Additional_Server_Hardware" and cont!="Yes") else True
		for row in container.Rows:
			attr1 = row.GetColumnByName(columName).ReferencingAttribute
			if ExRel in ('R520','R530','R511','R510') and flag:
				for value in attr1.Values:
					if ExRel in ('R510','R511') and value.Display in('HP DL 320 G11'):
						value.Allowed=False
					
		row.ApplyProductChanges()
	refattr= Product.Attr('TPS_EX_ESVT_Server_Hardware')
	flag=False if (refattr and cont!="Yes") else True
	if ExRel in ('R520','R530','R511','R510') and flag:
		for val in refattr.Values:
			if ExRel in ('R510','R511') and val.Display in('HP DL 320 G11'):
				val.Allowed=False
	Bunattr= Product.Attr('TPS_EX_Bundle_Conversion_ESVT_Server_Hardware')
	flag=False if (Bunattr and cont!="Yes") else True
	if ExRel in ('R520','R530','R511','R510') and flag:
		for val1 in Bunattr.Values:
			if ExRel in ('R510','R511') and val1.Display in('HP DL 320 G11','HP DL360 G11'):
				val1.Allowed=False
	bundleCon= Product.Attr('TPS_EX_Bundle_Conversion_EST_Station_Hardware')
	if ExRel not in('R520','R530'):
		for value in bundleCon.Values:
			if value.Display in ('HP Z4 G4 MLK','HP Z4 G5','Dell T5860XL','Dell R7960XL'):
				value.Allowed = False
			else:
				value.Allowed = True
	elif ExRel =='R530':
		for value in bundleCon.Values:
			if value.Display in ('Dell T5860XL','HP Z4 G5','Dell R7960XL'):
				value.Allowed = True
			else:
				value.Allowed = False
	else:
		for value in bundleCon.Values:
			if value.Display == 'HP Z4 G4 MLK':
				value.Allowed = True
			else:
				value.Allowed = False
	if isR2Qquote:
		Bunattr= Product.Attr('TPS_EX_Bundle_Conversion_ESVT_Server_Hardware')
		for val1 in Bunattr.Values:
			if val1.Display in('HP DL360 G11'):
				val1.Allowed=True
			else:
				val1.Allowed=False
		bundleCon= Product.Attr('TPS_EX_Bundle_Conversion_EST_Station_Hardware')
		for value in bundleCon.Values:
			if value.Display in ('HP Z4 G5','Dell T5860XL','Dell R7960XL'):
				value.Allowed = True
			else:
				value.Allowed = False
		BunFurnattr= Product.Attr('TPS_EX_Bundle_Conversion_EST_Station_Mounting_Furn')
		for value in BunFurnattr.Values:
			if value.Display in ('Desktop','Classic Black Direct Mounting','Classic Beige Direct Mounting','Classic Black Slide Mounting','Classic Beige Slide Mounting','Z Console','EZ Console','Icon Console'):
				value.Allowed = True
			else:
				value.Allowed = False
#OPM/TPS to Experion
if Product.Name in('OPM','TPS to Experion'):
	curr_rel=Product.Attr('MSID_Current_Experion_Release').GetValue()
	fut_attr = Product.Attr('MSID_Future_Experion_Release')
	if curr_rel == 'R511.x':
		for value in fut_attr.Values:
			if value.Display in ('R510','R511'):
				value.Allowed = False
			else:
				value.Allowed = True
	elif curr_rel == 'R520.x':
		for value in fut_attr.Values:
			if value.Display in ('R510','R511','R520'):
				value.Allowed = False
			else:
				value.Allowed = True
	elif curr_rel == 'R510.x':
		for value in fut_attr.Values:
			if value.Display in ('R510'):
				value.Allowed = False
			else:
				value.Allowed = True
	else:
		for value in fut_attr.Values:
			value.Allowed = True
#3rd Party PLC to ControlEdge PLC/UOC
if isR2Qquote and Product.Name == '3rd Party PLC to ControlEdge PLC/UOC':
		container = Product.GetContainerByName('LSS_Configuration_for_Rockwell_transpose')
		for data in container.Rows:
			data.Product.DisallowAttrValues('LSS_PLC_Network_Topology', *['Redundant Star-PRP','Ring-HSR','Ring-DLR via ETAPs','Ring-DLR Direct Connection'])