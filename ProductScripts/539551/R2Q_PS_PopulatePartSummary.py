isR2Qquote = True if Quote.GetCustomField("isR2QRequest").Content else False
if isR2Qquote:
	import math
	from ProductUtil import getContainer
	from GS_MigrationPartsUtil_New_MSID import (updateAttributeWithCustomC200MigrationValues,updateAttrWithCustomCBECValues,updateAttrWithCustomTpsValues)
	from GS_Msid_Populatepartcontainer import checkPartQtyToBeAdded #
	from GS_MigrationPartsUtil_2_New_MSID import updateAttrDictWithCustomC200toC300
	from GS_MigrationPartsUtil_3_New_MSID import updateAttrDictWithCustomxPMC300
	from GS_MigrationPartsUtil_4_New_MSID import updateAttributeWithLMtoELMMValues, populateSparePartCabinetSummary
	from GS_MigrationPartsUtil_5_New_MSID import updateAttrDictWithXP10Actuator,updateAttrDictWithCWSRAE,updateAttrDictWithQCSRAE
	from GS_MigrationPartsUtil_7_New_MSID import FSCtoSM_IOparts, updateAttrDictWithTPA
	from GS_MigrationPartsUtil_8_New_MSID import updateAttrDictWithCustomXpm
	from GS_MigrationPartsUtil_6_New_MSID import GetPartAndModulesDict 
	from GS_PartSummaryHelper import productAttrMatchingNames, getProductLaborDeliverablesContainer, popthirdPartSummary
	from GS_PartSummaryHelper_1 import updateAttrDictWithCustomFDMUpgrade, updateAttrDictWithCustomFDMUpgrade2, updateAttrDictWithCustomFDMUpgrade3
	from GS_PartSummaryHelper_2 import updateAttributeWithCustomELCNValues,GetPartNumberDict
	from GS_Add_NP_Parts import  getNonPricingParts

	def log_dict(d):
		return RestClient.SerializeToJson(d)

	def getFloat(var):
		if var:
			return float(var)
		return 0

	def getValue(row,col):
		if col.IsProductAttribute and col.ReferencingAttribute and col.ReferencingAttribute.SelectedValue:
			val = col.ReferencingAttribute.SelectedValue.Display
			if not val:
				val = col.DisplayValue
				if not val:
					val = row[col.Name] if row[col.Name] else ''
			return val
		if col.DisplayType == 'DropDown':
			val = col.DisplayValue
			if not val:
				val = row[col.Name] if row[col.Name] else ''
			return val
		if col.DisplayType == 'TextBox':
			return col.Value
		if col.DisplayType == "Label":
			return col.Value
		return ""

	def updateAttributeDict(product, attributeValueDict, containerNames):
		for containerName in containerNames:
			container = getContainer(product, containerName)
			for row in container.Rows:
				for col in row.Columns:
					attributeValueDict[col.Name] = getValue(row,col)
				if containerName != "OPM_Node_Configuration":
					break

	def updateAttributeDictWithMultiplier(product, attributeValueDict, containerNames):
		for containerName in containerNames:
			total = 0
			container = getContainer(product, containerName)
			for row in container.Rows:
				for col in row.Columns:
					try:
						total += float(getValue(row,col))
					except:
						pass
			if total > 0:
				attributeValueDict[containerName+"_Multiplier"] = 1
			else:
				attributeValueDict[containerName+"_Multiplier"] = 0

	def updateAttributeDictMultiRow(product, attributeValueDict, containerNames):
		for containerName in containerNames:
			container = getContainer(product, containerName)
			for row in container.Rows:
				for col in row.Columns:
					l = attributeValueDict.get(col.Name,list())
					l.append(getValue(row,col))
					attributeValueDict[col.Name] = l

	def updateContainerDetails(product, containerNames, attributeValueDict):
		for containerName in containerNames:
			container = getContainer(product, containerName)
			row = container.Rows[0]
			for col in row.Columns:
				attributeValueDict[col.Name] = getValue(row,col)

	def getELCNTotalSum(attributeValueDict, keys , prefix):
		total = 0
		for key in keys:
			total += getFloat(attributeValueDict[prefix + "_" + key])
		return total

	def updateAttributeDictWithCustomOrion(product, migrationAttrDict):
		con = getContainer(product, "Orion_Station_Configuration")
		for row in con.Rows:
			l = migrationAttrDict.get("Orion_Left_Aux_Sum_0",list())
			l.append(str(getFloat(row["Orion_Number_of_Left_Auxiliary_Equipment_Unit"]) + getFloat(row["Orion_Number_of_Left_Extended_Auxiliary_Equipment_Unit"]) == 0).upper())
			migrationAttrDict["Orion_Left_Aux_Sum_0"] = l
			l = migrationAttrDict.get("Orion_Right_Aux_Sum_0",list())
			l.append(str(getFloat(row["Orion_Number_of_Right_Auxiliary_Equipment_Unit"]) + getFloat(row["Orion_Number_of_Right_Extended_Auxiliary_Equipment_Unit"]) == 0).upper())
			migrationAttrDict["Orion_Right_Aux_Sum_0"] = l
			l = migrationAttrDict.get("Orion_2_3_Position_Sum_1",list())
			l.append(str(getFloat(row["Orion_Number_of_2_Position_Base_Unit"]) + getFloat(row["Orion_Number_of_3_Position_Base_Unit"]) == 1).upper())
			migrationAttrDict["Orion_2_3_Position_Sum_1"] = l
			l = migrationAttrDict.get("Orion_2_Position_multiplier",list())
			l.append(1 if getFloat(row["Orion_Number_of_2_Position_Base_Unit"]) > 0 else 0)
			migrationAttrDict["Orion_2_Position_multiplier"] = l
			l = migrationAttrDict.get("Orion_3_Position_multiplier",list())
			l.append(1 if getFloat(row["Orion_Number_of_3_Position_Base_Unit"]) > 0 else 0)
			migrationAttrDict["Orion_3_Position_multiplier"] = l

	def updateAttributeWithCustomEHPMHARTIOValues(product, attributeValueDict):
		container = product.GetContainerByName("EHPM_HART_IO_Configuration_Cont")
		for row in container.Rows:
			if row.RowIndex == 0:
				customKey = 'With_License'
			elif row.RowIndex == 2:
				customKey = 'Without_License'
			else:
				continue
			for col in row.Columns:
				try:
					attributeValueDict[customKey+"_"+col.Name] = float(getValue(row,col))
				except:
					attributeValueDict[customKey+"_"+col.Name] = 0
					pass

	def updateAttributeWithC200MigrationSESP(product, attributeValueDict):
		sespType = Quote.GetCustomField("Entitlement").Content if Quote and Quote.GetCustomField("Entitlement").Content else "No"
		C200sMigrating = getFloat(getContainer(product, 'C200_Migration_General_Qns_Cont').Rows[0]['C200_How_many_C200s_are_we_migrating'])

		if sespType in ("No","Support Flex", "Value Support Flex"):
			EPUPUOC1Points = C200sMigrating
			attributeValueDict["EPUPUOC1Points"] = EPUPUOC1Points
		else:
			pass

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
					elif diff > 0.0 and (sespType == 'Yes' or sespType == 'K&E Pricing Plus' or sespType == 'K&E Pricing Flex' or sespType == 'Non-SESP MSID with new SESP Plus' or sespType == 'Non-SESP MSID with new SESP Flex'):
						FS_SMSNUPL801_01S += diff
						FS_SMSNE810_01 = 1
						attrValDict['FS_SMSNUPL801_01S'] = round(FS_SMSNUPL801_01S)
				FS_CCI_HSE_02_data =round(float((SDW_550EC_data + MTL24571_data)/2.00))
				FC_DCOM_485 += float(FC_DCOM_485_data * migratedSystemCount)
				#SDW_550EC += float(SDW_550EC_data * migratedSystemCount)
				SDW_50194005_001 += float(SDW_550EC_data * migratedSystemCount)
				MTL24571 += float(MTL24571_data * migratedSystemCount)
				FS_CCI_UNI_04 += float(FS_CCI_UNI_04_data * migratedSystemCount)
				FS_CCI_HSE_02 += float(FS_CCI_HSE_02_data * migratedSystemCount)

			attrValDict['FS_CCI_HSE_02'] = round(FS_CCI_HSE_02)
			attrValDict['FC_DCOM_485'] = round(FC_DCOM_485)
			#attrValDict['SDW_550EC'] = round(SDW_550EC)
			attrValDict['SDW_50194005_001'] = round(SDW_50194005_001)
			attrValDict['MTL24571'] = round(MTL24571)
			attrValDict['FS_CCI_UNI_04'] = round(FS_CCI_UNI_04)
			attrValDict['FS_SMSNE810_01'] = round(FS_SMSNE810_01)

	def migrationAttrDict(product,childproduct):
		migrationAttrDict = dict()
		Trace.Write('prodname = '+str(product.Name))
		updateStandAloneAttributesDict(product, childproduct, migrationAttrDict)
		if childproduct.Name == 'OPM':
			containersNames = ["OPM_Basic_Information","OPM_Node_Configuration"]
		elif childproduct.Name == 'LCN One Time Upgrade':
			containersNames = ["LCN_Design_Inputs_for_TPN_OTU_Upgrade"]
		elif childproduct.Name == 'Non-SESP Exp Upgrade':
			containersNames = ["NONSESP_Design_Inputs_for_Experion_Upgrade_License","NONSESP_Design_Inputs_for_eServer_Upgrade_License"]
		elif childproduct.Name == 'EBR':
			containersNames = ["EBR_Basic_Information","EBR_Upgrade"]
		#elif product.Name == 'LM to ELMM ControlEdge PLC':
			#containersNames = ["LM_to_ELMM_ControlEdge_PLC_Migration_Gen_Cont"]
		elif childproduct.Name == 'C200 Migration':
			containersNames = ["C200_Migration_General_Qns_Cont"]
		elif childproduct.Name == 'C300 V2 to V5 Migration':
			containersNames = ["C300_V2_to_V5_Migration_Inputs_Cont"]
		elif childproduct.Name == 'EHPM/EHPMX/ C300PM':
			containersNames = ["xPM_Migration_General_Qns_Cont"]
		elif childproduct.Name == 'EHPM HART IO':
			containersNames = ["EHPM_HART_IO_General_Qns_Cont"]
		elif childproduct.Name == 'CB-EC Upgrade to C300-UHIO':
			containersNames = ["CB_EC_migration_to_C300_UHIO_Configuration_Cont"]
		elif childproduct.Name == 'TCMI':
			containersNames = ["TCMI_General_Information","TCMI_Hardware_and_Licenses"]
		else:
			containersNames = []
		updateAttributeDict(childproduct, migrationAttrDict, containersNames)
		if childproduct.Name == 'LCN One Time Upgrade':
			contNames = ["LCN_Design_Inputs_for_TPN_OTU_Upgrade"]
		elif childproduct.Name == 'Non-SESP Exp Upgrade':
			contNames = ["NONSESP_Design_Inputs_for_Experion_Upgrade_License","NONSESP_Design_Inputs_for_eServer_Upgrade_License"]
		else:
			contNames = []
		updateAttributeDictWithMultiplier(childproduct, migrationAttrDict, contNames)
		if childproduct.Name == 'Orion Console':
			containers = ["Orion_Station_Configuration"]
		elif childproduct.Name == 'EHPM/EHPMX/ C300PM':
			containers = ["xPM_Migration_Config_Cont","ENB_Migration_Config_Cont"]
		elif childproduct.Name == 'TPS to Experion':
			containers = ["TPS_EX_Additional_Stations","TPS_EX_Additional_Servers","TPS_EX_Station_Conversion_EST","TPS_EX_Conversion_ACET_EAPP"]
		elif childproduct.Name == 'C200 Migration':
			containers = ["C200_Migration_Config_Cont"]
		elif childproduct.Name == 'FSC to SM':
			containers = ["FSC_to_SM_Configuration"]
		elif childproduct.Name == 'LM to ELMM ControlEdge PLC':
			containers = ["LM_to_ELMM_ControlEdge_PLC_Cont","LM_to_ELMM_ControlEdge_PLC_Local_IO_Cont","LM_to_ELMM_ControlEdge_PLC_Remote_IO_Cont"]
		else:
			containers = []
		updateAttributeDictMultiRow(childproduct, migrationAttrDict, containers)
		#updateAttributeDictMultiRow(product, migrationAttrDict, containers)
		if childproduct.Name == 'FSC to SM':
			updateAttributeDictWithCustomFSCtoSM(childproduct, migrationAttrDict)
			updateAttributeDictWithCustomFSSMcom(childproduct, migrationAttrDict)
			updateAttrDictWithCustomFSCtoSMParts(childproduct, migrationAttrDict, Quote)
		elif childproduct.Name == 'FDM Upgrade 1':
			updateAttrDictWithCustomFDMUpgrade(childproduct, migrationAttrDict)
		elif childproduct.Name == 'FDM Upgrade 2':
			updateAttrDictWithCustomFDMUpgrade2(childproduct, migrationAttrDict)
		elif childproduct.Name == 'FDM Upgrade 3':
			updateAttrDictWithCustomFDMUpgrade3(childproduct, migrationAttrDict)
		elif childproduct.Name == 'Orion Console':
			updateAttributeDictWithCustomOrion(childproduct, migrationAttrDict)
		elif childproduct.Name == 'EHPM/EHPMX/ C300PM':
			updateAttrDictWithCustomXpm(childproduct, migrationAttrDict, Quote, product.Attr('SESP_TYPE').GetValue())
		elif childproduct.Name == 'TPS to Experion':
			updateAttrWithCustomTpsValues(childproduct, migrationAttrDict)
		elif childproduct.Name == 'ELCN':
			updateAttributeWithCustomELCNValues(childproduct, migrationAttrDict)
		elif childproduct.Name == 'EHPM HART IO':
			updateAttributeWithCustomEHPMHARTIOValues(childproduct, migrationAttrDict)
		elif childproduct.Name == 'FSC to SM IO Migration':
			FSCtoSM_IOparts(childproduct, migrationAttrDict, product)
		elif childproduct.Name == 'C200 Migration':
			updateAttributeWithC200MigrationSESP(childproduct, migrationAttrDict)
		elif childproduct.Name == 'CB-EC Upgrade to C300-UHIO':
			updateAttrWithCustomCBECValues(childproduct, migrationAttrDict)
		elif childproduct.Name == 'LM to ELMM ControlEdge PLC':
			updateAttributeWithLMtoELMMValues(childproduct, migrationAttrDict)
			#updateAttributeWithLMtoELMMValues(product, migrationAttrDict)
		elif childproduct.Name == 'xPM to C300 Migration':
			updateAttrDictWithCustomxPMC300(childproduct, migrationAttrDict, Quote, product)
		elif childproduct.Name == 'XP10 Actuator Upgrade':
			updateAttrDictWithXP10Actuator(childproduct, migrationAttrDict)
		if product.Attr("MIgration_Scope_Choices").GetValue() not in ["LABOR"]:
			if childproduct.Name == 'CWS RAE Upgrade':
				updateAttrDictWithCWSRAE(childproduct, migrationAttrDict)
			elif childproduct.Name == 'QCS RAE Upgrade':
				updateAttrDictWithQCSRAE(childproduct, migrationAttrDict)
			elif childproduct.Name == 'TPA/PMD Migration':
				updateAttrDictWithTPA(childproduct, migrationAttrDict,Quote)
		if childproduct.Name == 'C200 Migration':
			tempdata = {"C300_var_2": 0, "C300_var_11":  0, "C200_UOC_var_9": 0}
			childproduct.Attr('Temporary Data').AssignValue(str(tempdata))
			TypeofUOC = childproduct.Attr('C200_Select_Migration_Scenario').GetValue()
			if TypeofUOC =='C200 to ControlEdge UOC':
				updateAttributeWithCustomC200MigrationValues(childproduct, migrationAttrDict)
			else:
				updateAttrDictWithCustomC200toC300(childproduct, migrationAttrDict, Quote)
		return migrationAttrDict

	def updateProductDict(dictToUpdate, row, qty):
		if row.IsThirdParty:
			productDict = dictToUpdate["THIRD_PARTY"]
			partQty = productDict.get(row.Child_Part + row.Product_Name, [row.Child_Part, row.Product_Name, 0])
			partQty[2] = partQty[2] + qty
			productDict[row.Child_Part + row.Product_Name] = partQty
		else:
			productDict = dictToUpdate[row.Product_Name]
			partQty = productDict.get(row.Child_Part, 0)
			productDict[row.Child_Part] = partQty + qty

	def getQuestionMapping(product_key):
		query = "select * from MIGRATION_MODULE_QUE_MAP where product_key = '{}'".format(product_key)
		res = SqlHelper.GetList(query)

		resDict = dict()
		for r in res:
			rDict = resDict.get(r.Module_Key,dict())
			rDict[r.Module_Question] = r.Migration_Question
			resDict[r.Module_Key] = rDict
		return resDict

	def migrationValue(name, que, attrValues, defaults):
		migrationQuestion = que.get(name)
		if migrationQuestion is not None:
			return attrValues.get(migrationQuestion,'').lower() if str(type(attrValues.get(migrationQuestion,''))) != "<type 'list'>" else ""
		defaultAns = defaults.get(name)
		if defaultAns is not None:
			return defaultAns.lower()

	def canBeadded(row, attrValues, queDict, defaults):
		if row.Attribute_Name and migrationValue(row.Attribute_Name, queDict, attrValues, defaults) != row.Attribute_Value_Code.lower():
			return False
		if row.Dependency_Attribute_Name and migrationValue(row.Dependency_Attribute_Name, queDict, attrValues, defaults) != row.Dependency_Attribute_Value_Code.lower():
			return False
		if row.Dependency_Attribute_Name_2 and migrationValue(row.Dependency_Attribute_Name_2, queDict, attrValues, defaults) != row.Dependency_Attribute_Value_Code_2.lower():
			return False
		return True

	def getPricingPartsForModel(res, attrValues, queDict, partNumbersToBeAdded, qty, prod, defaults):
		partsAdded = set()
		for row in res:
			if canBeadded(row, attrValues, queDict, defaults):
				productDict = partNumbersToBeAdded[prod]
				partQty = productDict.get(row.Child_Products, 0)
				productDict[row.Child_Products] = partQty + (qty * int(row.Quantity))
				if partQty + (qty * int(row.Quantity)) > 0:
					partsAdded.add(row.Child_Products)
		return partsAdded

	def getDefaultAnswer():
		query = "select * from KE_QUE_DEFAULT"
		res = SqlHelper.GetList(query)
		d = dict()
		for r in res:
			d[r.Attribute_Name] = r.Default
		return d

	def getPricingParts(modules, attributeValueDict, partNumbersToBeAdded, partsList):
		query = "select Child_Products, Quantity, Attribute_Name, Attribute_Value_Code, Dependency_Attribute_Name, Dependency_Attribute_Value_Code, Dependency_Attribute_Name_2, Dependency_Attribute_Value_Code_2 from KE_Package_Part_Qty_Mapping where Package_Model_Number = '{0}' and Pricing = 'Yes' union select Child_Products, Quantity, Attribute_Name, Attribute_Value_Code, '','','','' from SERVER_CABINET_PART_QTY_MAPPING where Package_Model_Number = '{0}' and Pricing = 'Yes'"
		defaults = getDefaultAnswer()

		for product, packages in modules.items():
			queDict = getQuestionMapping(product)
			for module, qty in packages.items():
				res = SqlHelper.GetList(query.format(module))
				partsList = partsList.union(getPricingPartsForModel(res, attributeValueDict, queDict.get(module,queDict.get("",dict())), partNumbersToBeAdded, qty, product, defaults))
		return partsList

	def qtyBasedOnExpRelease(remoteUserEntered):
		qty= "0"
		if remoteUserEntered >= 6 and remoteUserEntered <= 10:
			qty = "1"
		elif remoteUserEntered >= 11 and remoteUserEntered <= 15:
			qty = "2"
		return qty

	def getPartDetailDict(partsList):
		resDict = dict()
		query = "select PRODUCT_CATALOG_CODE, PRODUCT_NAME, PLSG, PLSGDesc from products p join HPS_PRODUCTS_MASTER hpm ON p.PRODUCT_CATALOG_CODE = hpm.PartNumber where PRODUCT_CATALOG_CODE in ('{0}') UNION select PRODUCT_CATALOG_CODE, PRODUCT_NAME, PLSG, PLSGDesc from Migration_Third_Party_Products where PRODUCT_CATALOG_CODE in ('{0}')"
		query = query.format("','".join(partsList))
		res = SqlHelper.GetList(query)
		for r in res:
			resDict[r.PRODUCT_CATALOG_CODE] = [r.PRODUCT_NAME, r.PLSG, r.PLSGDesc]
		return resDict

	def getPartsToBeAdded(attributeValueDict,mappingPart):
		partNumbersToBeAdded, modules = GetPartAndModulesDict()
		partsList = set()
		query = "select * from MIGRATION_PART_MAPPING (NOLOCK) WHERE Product_Name='{}'".format(mappingPart)
		res = SqlHelper.GetList(query)
		for r in res:
			qty = checkPartQtyToBeAdded(r, attributeValueDict)
			if qty and r.Module_Name:
				updateProductDict(modules, r, qty)
				partsList.add(r.Child_Part)
			if qty:
				updateProductDict(partNumbersToBeAdded, r, qty)
				attributeValueDict[r.Child_Part] = attributeValueDict.get(r.Child_Part[0],0) + qty
				partsList.add(r.Child_Part)
		partsList = getPricingParts(modules, attributeValueDict, partNumbersToBeAdded, partsList)
		return partNumbersToBeAdded, partsList

	def getUserInputMap(prodName, container, userInputMap):
		for row in container.Rows:
			if prodName == "THIRD_PARTY":
				continue
			else:
				data = {'adjQty' : row['Adj Quantity'],'comment' : row['Comments']}
				if prodName not in userInputMap:
					userInputMap[prodName] = {}
				userInputMap[prodName][row['PartNumber']] = data
		return userInputMap

	def getProductAttrMappingName(productName, attrName):
		names = productAttrMatchingNames()
		if productName in names and attrName in names[productName]:
			return names[productName][attrName]
		else:
			return attrName

	def updateStandAloneAttributesDict(product,childproduct, attributeValueDict):
		for attr in childproduct.Attributes:
			if attr.DisplayType not in ['Container', 'DisplayOnlyText', 'CheckBox']:
				mappingName = getProductAttrMappingName(childproduct.Name, attr.Name)
				attributeValueDict[mappingName] = attr.GetValue()
		commonQuestions = ['MSID_Current_Experion_Release', 'MSID_Future_Experion_Release', 'MSID_Current_TPN_Release', 'MSID_Future_TPN_Release']
		for attrName in commonQuestions:
			if product.Attr(attrName).Allowed:
				attributeValueDict[attrName] = product.Attr(attrName).GetValue()
	userInputMap = {}
	ShipcrateParts=["CF-CTD001","CF-CTD002","CF-CTWA00","CF-CTWA01","CF-CTW000","CF-CTW001"]
	TPS_Sub_parts=["TP-ZSDRB1","TP-ZSDRC1","TP-ZSDRD1","TP-ZSDRE1","TP-ZSDRL1","TP-ZSHRD1","TP-ZSDRJ1","TP-ZSDRK1","TP-ZSDRP1","TP-ZSDRQ1","TP-ZSHRA1",
				"TP-ZSHRB1","TP-ZSDTB2","TP-ZSDTB3","TP-ZSDRR1","TP-ZWDTA1","TP-ZWDRA1","TP-ZWDTD1","TP-ZWHTB1","TP-ZWDRD1","TP-ZWDTF1","TP-ZSDRF1",
				"TP-ZSDRG1"]
	Total_TPSSubparts_qty=0
	MZ_PCSR02_qty=0
	c200_sumqty = 0
	ebr_sumQty = 0
	opm_sumQty = 0
	c200_BOM = ['CC-C8DS01', 'CC-C8SS01', 'CC-CBDD01', 'CC-CBDS01']
	ebr_BOM = ('MZ-PCST01','MZ-PCST02', 'MZ-PCST82', 'MZ-PCSR01','MZ-PCSR02', 'MZ-PCSR82', 'MZ-PCSV84', 'MZ-PCSV65', 'MZ-NWSTR6', 'MZ-NWSTR6')
	opm_BOM = ('TP-ZESVR4', 'TP-ZESVL6', 'TP-ZESVT5', 'TP-ZESVT6', 'TP-ZDSRB2', 'TP-ZDSRA2', 'TP-ZDSRA3', 'TP-ZSHRF1', 'TP-ZSDTG2', 'TP-ZSDTG3', 'TP-ZSDRN1', 'TP-ZSHRE1', 'TP-ZSDTE2', 'TP-ZSDTE3', 'TP-ZSDRM1', 'TP-ZSHRC1', 'TP-ZSDTD2', 'TP-ZSDTD3', 'TP-ZSDRH1', 'TP-ZESCH4', 'TP-ZESCD3', 'TP-ZESCR7')

	migration_new_cont = Product.GetContainerByName('CONT_Migration_MSID_Selection')
	for MigrationNew in migration_new_cont.Rows:
		containerNameMapping = {
		"OPM": getContainer(MigrationNew.Product, "MSID_OPM_Added_Parts_Common_Container"),
		"LCN": getContainer(MigrationNew.Product, "MSID_LCN_Added_Parts_Common_Container"),
		"NONSESP": getContainer(MigrationNew.Product, "MSID_NON_SESP_Added_Parts_Common_Container"),
		"EBR": getContainer(MigrationNew.Product, "MSID_EBR_Added_Parts_Common_Container"),
		"ELCN": getContainer(MigrationNew.Product, "MSID_ELCN_Added_Parts_Common_Container"),
		"PM": getContainer(MigrationNew.Product, "MSID_PM_Added_Parts_Common_Container"),
		"Orion_Console": getContainer(MigrationNew.Product, "MSID_Orion_Console_Added_Parts_Common_Container"),
		"EHPM/EHPMX/ C300PM": getContainer(MigrationNew.Product, "MSID_EHPM_C300PM_Added_Parts_Common_Container"),
		"TPS_EXP": getContainer(MigrationNew.Product, "MSID_TPS_EXP_Added_Parts_Common_Container"),
		"TCMI": getContainer(MigrationNew.Product, "MSID_TCMI_Added_Parts_Common_Container"),
		"LMTOELMM": getContainer(MigrationNew.Product, "MSID_LM_TO_ELMM_Added_Parts_Common_Container"),
		"Spare Parts": getContainer(MigrationNew.Product, "MSID_Spare_Parts_Added_Parts_Common_Container"),
		"EHPMHART": getContainer(MigrationNew.Product, "MSID_EHPM_HART_IO_Added_Parts_Common_Container"),
		"C200 Migration": getContainer(MigrationNew.Product, "MSID_C200_Migration_Added_Parts_Common_Container"),
		"CBEC": getContainer(MigrationNew.Product, "MSID_CB_EC_Added_Parts_Common_Container"),
		"XPM C300": getContainer(MigrationNew.Product, "MSID_xPM_C300_Added_Parts_Common_Container"),
		"FDM_Upgrade": getContainer(MigrationNew.Product, "MSID_FDM_Upgrade_1_Added_Parts_Common_Container"),
		"FDM_Upgrade_2": getContainer(MigrationNew.Product, "MSID_FDM_Upgrade_2_Added_Parts_Common_Container"),
		"FDM_Upgrade_3": getContainer(MigrationNew.Product, "MSID_FDM_Upgrade_3_Added_Parts_Common_Container"),
		"FSC_to_SM": getContainer(MigrationNew.Product, "MSID_FSC_to_SM_Added_Parts_Common_Container"),
		"FSC_to_SM_audit": getContainer(MigrationNew.Product, "MSID_FSC_to_SM_audit_Added_Parts_Common_Container"),
		"THIRD_PARTY" : getContainer(MigrationNew.Product, "MSID_Third_Party_Added_Parts_Common_Container"),
		"XP10_Actuator": getContainer(MigrationNew.Product, "MSID_XP10_Actuator_Added_Parts_Common_Container"),
		"CWS_RAE_Upgrade": getContainer(MigrationNew.Product, "MSID_CWS_RAE_Upgrade_Added_Parts_Common_Container"),
		"Graphics_Migration": getContainer(MigrationNew.Product, "MSID_Graphics_Added_Parts_Common_Container"),
		"FSCtoSM_IO": getContainer(MigrationNew.Product, "MSID_FSCtoSM_IO_Added_Parts_Common_Container"),
		"FSCtoSM_IO_AUDIT": getContainer(MigrationNew.Product, "MSID_FSCtoSM_IO_audit_Added_Parts_Common_Container"),
		"CD_Actuator_IF_Upgrade": getContainer(MigrationNew.Product, "MSID_CD_Actuator_Added_Parts_Common_Container"),
		"3rd_Party_PLC_to_ControlEdge_PLC/UOC": getContainer(MigrationNew.Product, "MSID_Third_Party_PLC_Added_Parts_Common_Container"),
		"Virtualization_System_Migration": getContainer(MigrationNew.Product, "MSID_Virtualization_Added_Parts_Common_Container"),
		"QCS_RAE_Upgrade": getContainer(MigrationNew.Product, "MSID_QCS_Added_Parts_Common_Container"),
		"GS_Migration_1": getContainer(MigrationNew.Product, "MSID_GS1_Added_Parts_Common_Container"),
		"GS_Migration_2": getContainer(MigrationNew.Product, "MSID_GS2_Added_Parts_Common_Container"),
		"GS_Migration_3": getContainer(MigrationNew.Product, "MSID_GS3_Added_Parts_Common_Container"),
		"GS_Migration_4": getContainer(MigrationNew.Product, "MSID_GS4_Added_Parts_Common_Container"),
		"GS_Migration_5": getContainer(MigrationNew.Product, "MSID_GS5_Added_Parts_Common_Container"),
		"TPA/PMD_Migration": getContainer(MigrationNew.Product, "MSID_TPA_Added_Parts_Common_Container"),
		# Extended Logic for Labor Part summary ELEPIU Module -- Dipak Shekokar : CXCPQ-60173
		"ELEPIU_ControlEdge_RTU_Migration_Engineering": getContainer(MigrationNew.Product, "MSID_ELEPIU_Added_Parts_Common_Container")
	}
		for prodName, container in containerNameMapping.items():
			userInputMap = getUserInputMap(prodName, container, userInputMap)
			#if prodName != 'Virtualization_System_Migration':
			if container.Rows.Count:
				container.Clear()

	
		selectedProducts = MigrationNew.Product.GetContainerByName('CONT_MSID_SUBPRD')
		scope = MigrationNew.Product.Attr('MIgration_Scope_Choices').GetValue()
		sesp_type=MigrationNew.Product.Attr('SESP_TYPE').GetValue()
		MigrationNew.Product.Attr('KE_SESP').AssignValue(sesp_type)
		partMapping_forSel={
			'OPM':'OPM',
			'LCN One Time Upgrade':'LCN',
			'Non-SESP Exp Upgrade':'NONSESP',
			'EBR':'EBR',
			'ELCN':'ELCN',
			'TPS to Experion':'TPS_EXP',
			'Orion Console':'Orion_Console',
			'TCMI':'TCMI',
			'EHPM HART IO':'EHPMHART',
			'C200 Migration':'C200 Migration',
			'C300 V2 to V5 Migration':'C300 V2 to V5 Migration',
			'CB-EC Upgrade to C300-UHIO':'CBEC',
			'xPM to C300 Migration':'XPM C300',
			'FDM Upgrade 1':'FDM_Upgrade',
			'LM to ELMM ControlEdge PLC':'LMTOELMM',
			'FSC to SM':'FSC_to_SM',
			'XP10 Actuator Upgrade':'XP10_Actuator',
			'EHPM/EHPMX/ C300PM':'EHPM/EHPMX/ C300PM',
			'CWS RAE Upgrade':'CWS_RAE_Upgrade',
			'QCS RAE Upgrade':'QCS_RAE_Upgrade',
			'FSC to SM IO Migration':'FSCtoSM_IO',
			'TPA/PMD Migration':'TPA/PMD_Migration',
			'FDM Upgrade 3':'FDM_Upgrade_3',
			'FDM Upgrade 2':'FDM_Upgrade_2',
			'Virtualization System Migration':'Virtualization_System_Migration',
			'Virtualization System':'Virtualization_System_Migration',
			'Generic System Migration':'GS_Migration_1',
			'Generic System Migration':'GS_Migration_2',
			'Generic System Migration':'GS_Migration_3',
			'Generic System Migration':'GS_Migration_4',
			'Generic System Migration':'GS_Migration_5',
			'3rd Party PLC to ControlEdge PLC/UOC':'3rd_Party_PLC_to_ControlEdge_PLC/UOC',
			'CD Actuator I-F Upgrade':'CD_Actuator_IF_Upgrade',
			'ELEPIU ControlEdge RTU Migration Engineering':'ELEPIU_ControlEdge_RTU_Migration_Engineering',
			'Graphics Migration':'Graphics_Migration',
			'Project Management':'PM',
			'Spare Parts':'Spare Parts',
			'Trace Software':'Trace_Software'
			
		}
		partnumbercont = MigrationNew.Product.GetContainerByName("Non Pricing Parts")
		if partnumbercont:
			partnumbercont.Rows.Clear()
		for selectedRow in selectedProducts.Rows:
			mappingPart = partMapping_forSel[selectedRow.Product.Name] if selectedRow.Product.Name in partMapping_forSel else selectedRow.Product.Name
			attributeValueDict = migrationAttrDict(MigrationNew.Product, selectedRow.Product)
			attributeValueDict['SESP_TYPE']=sesp_type
			migration_scenario = attributeValueDict.get('C200_Select_the_Migration_Scenario', '')
			if selectedRow.Product.Name == 'C200 Migration':
				if migration_scenario == 'C200 to C300':
					keys_to_remove =['C200_How_many_co_located_C200_groups_exists','C200_Type_of_UOC','C200_Type_of_downlink_communication_UOC','C200_Series_A_IO_in_Controller_Rack_Non','C200_Number_of_Serial_Interface_points','C200_Number_of_Serial_Interface_IOMs','C200_Number_of_1756_DI_IOMs','C200_Number_of_CNI_segments','C200_Data_Gathering_Required','C200_Documentation_Required','C200_Factory_Acceptance_Test_Required']
					for key in keys_to_remove:
						if key in attributeValueDict:
							del attributeValueDict[key]
			partNumbersToBeAdded, partsList = getPartsToBeAdded(attributeValueDict, mappingPart)
			if partnumbercont:
				getNonPricingParts(partsList,mappingPart,partnumbercont, attributeValueDict)
			if selectedRow.Product.Name == '3rd Party PLC to ControlEdge PLC/UOC' and scope != 'LABOR':
				popthirdPartSummary(selectedRow.Product, partNumbersToBeAdded, partsList, MigrationNew.Product)
			if scope != "HW/SW":
				getProductLaborDeliverablesContainer(selectedRow.Product.Name, partNumbersToBeAdded, partsList, MigrationNew.Product)
			if selectedRow.Product.Name == 'Spare Parts':
				sparePartsCabinetDict = populateSparePartCabinetSummary(selectedRow.Product, partsList)
				partNumbersToBeAdded["Spare Parts"] = sparePartsCabinetDict
			partsList.add("EP-S08CAL")
			partsList.add("EP-S04CAL")
			partDetailsDict = getPartDetailDict(partsList)
			c200_migration_parts_del = ['CF-SP0000','CF-PP0000','CF-CT4A00','CF-CT4A01','CF-CT4000','CF-CT4001']
			if selectedRow.Product.Name == 'C200 Migration':
				c200_migration_parts = partNumbersToBeAdded.get('C200 Migration', {})
				if migration_scenario == 'C200 to ControlEdge UOC':
					parts_to_delete = [key for key in c200_migration_parts if key in c200_migration_parts_del]    
					for key in parts_to_delete:
						del c200_migration_parts[key]
				else:
					BomQty = (c200_migration_parts[child] for child in c200_BOM if child in c200_migration_parts)
					c200_sumqty = list(BomQty)
			for product, parts in partNumbersToBeAdded.items():
				container = containerNameMapping[product]
				if product == "THIRD_PARTY":
					for part, data in parts.items():
						if data[2] > 0.00 and data[2] != '':
							row = None
							for existingRow in container.Rows:
								if existingRow['PartNumber'] == data[0]:
									row = existingRow
							if not row:
								row = container.AddNewRow(False)
							row['PartNumber'] = data[0]
							row['Quantity'] = str(data[2])
							adjQty = 0
							row['Adj Quantity'] = str(adjQty)
							row['Final Quantity'] = str(getFloat(data[2]) + adjQty)
							row['ModuleName'] = data[1]
							if partDetailsDict.get(data[0]):
								row['PartDescription'] = partDetailsDict[data[0]][0]
								row['PLSG'] = partDetailsDict[data[0]][1]
								row['plsgDescription'] = partDetailsDict[data[0]][2]
					continue
				else:
					ebr_sumQty = sum(int(qty) for part, qty in parts.items() if selectedRow.Product.Name == "EBR" and str(part) in ebr_BOM)
					opm_sumQty =  sum(int(qty) for part, qty in parts.items() if selectedRow.Product.Name == "OPM" and str(part) in opm_BOM)
					TPS_sumQty =  sum(int(qty) for part, qty in parts.items() if selectedRow.Product.Name == "TPS to Experion" and str(part) in TPS_Sub_parts)
					for part, qty in parts.items():
						if part in ('CF-SP0000','CF-PP0000','CF-CT4A00','CF-CT4A01','CF-CT4000','CF-CT4001') and selectedRow.Product.Name == "C200 Migration" and migration_scenario == 'C200 to C300':
							qty = c200_sumqty[0] if len(c200_sumqty)>0 else 1
						if qty > 0.00 and qty != '' and part not in ShipcrateParts:
							row = None
							for existingRow in container.Rows:
								if existingRow['PartNumber'] == part:
									row = existingRow
							if not row:
								row = container.AddNewRow(False)
							row['PartNumber'] = part
							row['Quantity'] = str(qty)
							adjQty = 0
							comment = ''
							if userInputMap.get(product) and userInputMap.get(product).get(part):
								adjQty = getFloat(userInputMap.get(product).get(part)['adjQty'])
								comment = userInputMap.get(product).get(part)['comment']
							row['Adj Quantity'] = str(adjQty)
							row['Final Quantity'] = str(getFloat(qty) + adjQty)
							row['Comments'] = comment
							if partDetailsDict.get(part):
								row['PartDescription'] = partDetailsDict[part][0]
								row['PLSG'] = partDetailsDict[part][1]
								row['plsgDescription'] = partDetailsDict[part][2]
							if selectedRow.Product.Name == "ELCN" and (part=="MZ-PCSR02" or "MZ-PCSR02" in partDetailsDict):
								MZ_PCSR02_qty=qty
						elif part in ShipcrateParts:
							if (selectedRow.Product.Name == "ELCN" and qty > 0.00 and qty != '' and MZ_PCSR02_qty>0) or (selectedRow.Product.Name == "TPS to Experion" and qty > 0.00 and qty != '' and TPS_sumQty>0) or (selectedRow.Product.Name == 'EBR' and (qty > 0.00 and qty != '') and ebr_sumQty>0)  or (selectedRow.Product.Name == 'LM to ELMM ControlEdge PLC' and qty > 0.00 and qty != '') or (selectedRow.Product.Name == "OPM" and qty > 0.00 and qty != '' and opm_sumQty>0) or (selectedRow.Product.Name =='Virtualization System Migration' and qty > 0.00 and qty != '')or (selectedRow.Product.Name =='Virtualization System' and qty > 0.00 and qty != '') or (selectedRow.Product.Name == "FDM Upgrade 1" and qty > 0.00 and qty != '') or (selectedRow.Product.Name == "FDM Upgrade 2" and qty > 0.00 and qty != '') or (selectedRow.Product.Name == "FDM Upgrade 3" and qty > 0.00 and qty != ''):
								if selectedRow.Product.Name == "OPM":
									qty = opm_sumQty
								elif selectedRow.Product.Name == "TPS to Experion":
									qty = TPS_sumQty
								else:
									qty=qty
								row = None
								for existingRow in container.Rows:
									if existingRow['PartNumber'] == part:
										row = existingRow
								if not row:
									row = container.AddNewRow(False)
								row['PartNumber'] = part
								row['Quantity'] = str(qty)
								adjQty = 0
								comment = ''
								if userInputMap.get(product) and userInputMap.get(product).get(part):
									adjQty = getFloat(userInputMap.get(product).get(part)['adjQty'])
									comment = userInputMap.get(product).get(part)['comment']
								row['Adj Quantity'] = str(adjQty)
								row['Final Quantity'] = str(getFloat(qty) + adjQty)
								row['Comments'] = comment
								if partDetailsDict.get(part):
									row['PartDescription'] = partDetailsDict[part][0]
									row['PLSG'] = partDetailsDict[part][1]
									row['plsgDescription'] = partDetailsDict[part][2]
			if selectedRow.Product.Name == 'OPM':
				TargetExpRelease = attributeValueDict.get("MSID_Future_Experion_Release", '')
				remoteUserEntered  = int(attributeValueDict["OPM_No_of_RESS_Remote_Users"] or '0') if "OPM_No_of_RESS_Remote_Users" in attributeValueDict else 0
				container = containerNameMapping["OPM"]

				Qty =  qtyBasedOnExpRelease(remoteUserEntered)
				if TargetExpRelease in ('R501','R510','R511','R520','R530'):
					if Qty != "0":
						row = container.AddNewRow(False)
						row['PartNumber'] = "EP-S04CAL"
						row['Quantity']  = Qty
						adjQty = 0
						comment = ''
						if userInputMap.get("OPM") and userInputMap.get("OPM").get("EP-S04CAL"):
							adjQty = getFloat(userInputMap.get("OPM").get("EP-S04CAL")['adjQty'])
							comment = userInputMap.get("OPM").get("EP-S04CAL")['comment']
						row['Adj Quantity'] = str(adjQty)
						row['Final Quantity'] = str(getFloat(qty) + adjQty)
						row['Comments'] = comment
						if partDetailsDict.get("EP-S04CAL"):
							row['PartDescription'] = partDetailsDict["EP-S04CAL"][0]
							row['PLSG'] = partDetailsDict["EP-S04CAL"][1]
							row['plsgDescription'] = partDetailsDict["EP-S04CAL"][2]

				elif TargetExpRelease in ('R432'):
					if Qty != "0":
						row = container.AddNewRow(False)
						row['PartNumber'] = "EP-S08CAL"
						row['Quantity']  = Qty
						adjQty = 0
						comment = ''
						if userInputMap.get("OPM") and userInputMap.get("OPM").get("EP-S08CAL"):
							adjQty = getFloat(userInputMap.get("OPM").get("EP-S08CAL")['adjQty'])
							comment = userInputMap.get("OPM").get("EP-S08CAL")['comment']
						row['Adj Quantity'] = str(adjQty)
						row['Final Quantity'] = str(getFloat(qty) + adjQty)
						row['Comments'] = comment
						if partDetailsDict.get("EP-S08CAL"):
							row['PartDescription'] = partDetailsDict["EP-S08CAL"][0]
							row['PLSG'] = partDetailsDict["EP-S08CAL"][1]
							row['plsgDescription'] = partDetailsDict["EP-S08CAL"][2]
							
			if selectedRow.Product.Name == 'Virtualization System Migration' and selectedRow.Product.GetContainerByName("Virtualization_partsummary_cont"):
				for Prd_Trace in selectedRow.Product.GetContainerByName("Virtualization_partsummary_cont").Rows:
					MSID_Trace = MigrationNew.Product.GetContainerByName("MSID_Virtualization_Added_Parts_Common_Container").AddNewRow(False)
					MSID_Trace ['PartNumber'] = Prd_Trace['partnumber']
					MSID_Trace ['Quantity'] = Prd_Trace['CE_Part_Qty']
					MSID_Trace ['PartDescription'] = Prd_Trace['CE_Part_Description']
					#MSID_Trace ['PLSG'] = Prd_Trace['PLSG']
					#MSID_Trace ['plsgDescription'] = Prd_Trace['plsgDescription']
					MSID_Trace ['Adj Quantity'] = Prd_Trace['CE_Adj_Quantity']
					MSID_Trace ['Final Quantity'] = Prd_Trace['CE_Final_Quantity']
					MSID_Trace ['Comments'] = Prd_Trace['CE_Comments']
		