import GS_Migration_Container_Attributes_Mapper

def getContainer(product, name):
	return product.GetContainerByName(name)
def getRowData(Product,container,column):
	Container = getContainer(Product,container)
	for row in Container.Rows:
		return row[column]

def updateAttributeDict(container, msidAttributeDict, isContainer, parentProduct=None, product=None, replacedContainerName=None):
	if isContainer:
		if container.Name == "ELCN_Upgrade_New_ELCN_Nodes":
			suffixList = [
				"_Upgrade_Physical",
				"_Upgrade_Virtual",
				"",
				"_New_Physical",
				"_New_Virtual",
			]
			for row in filter(lambda r: r.RowIndex != 2 and  r.RowIndex < 5, container.Rows):
				for col in row.Columns:
					val = getValue(col,row)
					msidAttributeDict[col.Name + suffixList[row.RowIndex]] = val if val else 0
			return
		for row in container.Rows:
			for col in row.Columns:
				"""if str(container.Name) in('Orion_Services','MSID_CommonQuestions','xPM_Services_Cont') and col.Name == 'MSID_Will_Honeywell_perform_equipment_installation':
					pdt=Product.Attr("MSID_Selected_Products").GetValue()
					if "EHPM/EHPMX/ C300PM" in pdt and str(col.DisplayValue) in ('Yes','No') and str(container.Name) in('xPM_Services_Cont'):
						msidAttributeDict[col.Name] = getValue(col,row)
					elif "Orion Console" in pdt and str(col.DisplayValue) in ('Yes','No') and str(container.Name) in('Orion_Services'):
						msidAttributeDict[col.Name] = getValue(col,row)
				else:"""
				msidAttributeDict[col.Name] = getValue(col,row)
			break
		if container.Name == "OPM_Node_Configuration":
			for row in container.Rows:
				if row.RowIndex == 2:
					for col in row.Columns:
						msidAttributeDict[col.Name + "_HW_Replace"] = getValue(col,row)
					break
	elif not isContainer and product:
		for attrName, colName in container.items():
			if replacedContainerName in ('MSID_CommonQuestions'):
				productReferring = parentProduct
			else:
				productReferring = product
			attrValue = productReferring.Attr(attrName).GetValue()
			if replacedContainerName in('Orion_Services','MSID_CommonQuestions','xPM_Services_Cont') and colName == 'MSID_Will_Honeywell_perform_equipment_installation':
				pdt=parentProduct.Attr("MSID_Selected_Products").GetValue()
				if "EHPM/EHPMX/ C300PM" in pdt and attrValue in ('Yes','No') and replacedContainerName in('xPM_Services_Cont'):
					msidAttributeDict[colName] = attrValue
				elif "Orion Console" in pdt and attrValue in ('Yes','No') and replacedContainerName in('Orion_Services'):
					msidAttributeDict[colName] = attrValue
			else:
				msidAttributeDict[colName] = attrValue
		
	if msidAttributeDict.get("OPM_Is_this_is_a_Remote_Migration_Service_RMS") is not None and msidAttributeDict.get("OPM_Is_this_is_a_Remote_Migration_Service_RMS") == '':
		msidAttributeDict["OPM_Is_this_is_a_Remote_Migration_Service_RMS"] = "No"


def updateMultilineAttributeDict(container, msidAttributeDict, isContainer, product=None):
	if isContainer:
		for row in container.Rows:
			for col in row.Columns:
				shouldDelete = msidAttributeDict.get(col.Name+"_delete",True)
				val = getValue(col,row)
				if val not in ('','0',"None","No",0,None,"Yes - Local and Remote","Yes - Only Remote"):
					shouldDelete = False
				msidAttributeDict[col.Name+"_delete"] = shouldDelete
				l = msidAttributeDict.get(col.Name,list())
				l.append(getValue(col,row))
				msidAttributeDict[col.Name] = l
	elif not isContainer and product:
		contMapperDict = multiLineMappingDict.get(container)
		if contMapperDict:
			for attrName, colName in contMapperDict.items():
				shouldDelete = msidAttributeDict.get(colName+"_delete",True)
				val = product.Attr(attrName).GetValue()
				if val not in ('','0',"None","No",0,None,"Yes - Local and Remote","Yes - Only Remote"):
					shouldDelete = False
				msidAttributeDict[colName+"_delete"] = shouldDelete
				l = msidAttributeDict.get(colName,list())
				l.append(val)
				msidAttributeDict[colName] = l



def updateMultilineAttributeDict_fsc(container, msidAttributeDict):
	for row in container.Rows:
		for col in row.Columns:
			shouldDelete_fsc = msidAttributeDict.get(col.Name+"_delete",1)
			val = getValue(col,row)
			if val not in ('','0'):
				shouldDelete_fsc = 0
			msidAttributeDict[col.Name+"_delete"] = shouldDelete_fsc
			l = msidAttributeDict.get(col.Name,list())
			l.append(getValue(col,row))
			msidAttributeDict[col.Name] = l

def populateQuoteTableIAA(guid, attr, attr_value, table, msid_esids=''):
	row = table.AddNewRow()
	row["MSID_GUID"] = guid
	row["Attribute"] = attr
	row['Item_Number'] = msid_esids
	row["Attribute_Value"] = ",".join(attr_value) if str(type(attr_value)) == "<type 'list'>" else str(attr_value)

def populateQuoteTable(guid, dataDict, table):

	for key, value in dataDict.items():
		row = table.AddNewRow()
		row["MSID_GUID"] = guid
		row["Attribute"] = key
		row["Attribute_Value"] = ",".join(value) if str(type(value)) == "<type 'list'>" else value


def getValue(col,row):
	if col.DisplayType == "DropDown":
		if col.DisplayValue != '':
			return col.DisplayValue
		return row[col.Name]
	if col.DisplayType == "TextBox":
		if col.DataType == "Number" and col.Value == "":
			return "0"
		return col.Value
	return ""


def populateMsidAttributes(product, parentProduct):
	msidAttributeDict = dict()

	attributeContianers = [
		"Orion_Services",
		"MSID_CommonQuestions",
		"LCN_Design_Inputs_for_TPN_OTU_Upgrade",
		"NONSESP_Design_Inputs_for_Experion_Upgrade_License",
		"NONSESP_Design_Inputs_for_eServer_Upgrade_License",
		"OPM_Basic_Information",
		"OPM_Node_Configuration",
		"OPM_Migration_platforms",
		"OPM_FTE_Switches_migration_info",
		"OPM_Services",
		"EBR_Basic_Information",
		"EBR_Upgrade",
		"EBR_New_Additional_EBR",
		"EBR_Hardware_to_Host_EBR_Physical_Node_Only",
		"EBR_Services",
		"ELCN_Basic_Information",
		"ELCN_Network_Gateway_Upgrade",
		"ELCN_Server_Cabinet_Configuration",
		"ELCN_Services",
		"ELCN_Upgrade_New_ELCN_Nodes",
		"xPM_Migration_Scenario_Cont",
		"xPM_Services_Cont",
		"xPM_Migration_General_Qns_Cont",
		"xPM_Network_Upgrade_Cont",
		"ENB_Migration_General_Qns_Cont",
		"TPS_EX_Conversion_ESVT_Server",
		"TPS_EX_Bundle_Conversion_Server_Stations",
		"TPS_EX_General_Questions",
		"TPS_EX_Service",
		"Orion_General_Information_Container2",
		"TCMI_Hardware_and_Licenses",
		"TCMI_Services",
		"TCMI_General_Information",
		"EHPM_HART_IO_General_Qns_Cont",
		"EHPM_HART_IO_Services_Cont",
		"C200_Migration_General_Qns_Cont",
		"C200_Migration_Scenario_Cont",
		"C200_Services_1_Cont",
		"C200_Services_2_Cont",
		"xPM_Migration_General_Qns_Cont",
		"CB_EC_migration_to_C300_UHIO_Configuration_Cont",
		"CB_EC_Services_1_Cont",
		"CB_EC_Services_2_Cont",
		"xPM_C300_Services_Cont",
		"xPM_C300_General_Qns_Cont",
		"FSC_to_SM_Services",
		"FSC_to_SM_General_Information",
		"xPM_C300_General_Qns_Cont",
		"FDM_Upgrade_General_questions",
		"FDM_Upgrade_Services",
		"FDM_Upgrade_2_General_questions",
		"FDM_Upgrade_2_Services",
		"FDM_Upgrade_3_General_questions",
		"FDM_Upgrade_3_Services",
		"LM_to_ELMM_ControlEdge_PLC_Migration_Gen_Cont",
		"LM_to_ELMM_Services",
		"FSC_to_SM_IO_Migration_General_Information",
		"Graphics_Migration_Migration_Scenario",
		"Graphics_Migration_Training_Testing_Documentation",
		"Graphics_Migration_Additional_Questions",
		"XP10_Actuator_General_Information",
		"FSC_to_SM_IO_Migration_General_Information",
		"FSC_to_SM_IO_New_SM_Cabinet_Configuration",
		"FSC_to_SM_IO_Services",
		"CD_Actuator_IF_Upgrade_General_Info_Cont",
		"CD_Actuator_IF_Upgrade_Services_Cont"
	]
	multilineContainer = [
		"ENB_Migration_Config_Cont",
		"xPM_Migration_Config_Cont",
		"TPS_EX_Station_Conversion_EST",
		"TPS_EX_Additional_Servers",
		"TPS_EX_Additional_Stations",
		"TPS_EX_Conversion_ACET_EAPP",
		"Orion_Station_Configuration",
		"EHPM_HART_IO_Configuration_Cont",
		"C200_Migration_Config_Cont",
		"FSC_to_SM_Configuration",
		"FDM_Upgrade_Configuration",
		"FDM_Upgrade_Additional_Configuration",
		"FDM_Upgrade_2_Configuration",
		"FDM_Upgrade_2_Additional_Configuration",
		"FDM_Upgrade_3_Configuration",
		"FDM_Upgrade_3_Additional_Configuration",
		"LM_to_ELMM_Migration_Additional_IO_Cont",
		"LM_to_ELMM_ControlEdge_PLC_Cont",
		"LM_to_ELMM_ControlEdge_PLC_Remote_IO_Cont",
		"LM_to_ELMM_ControlEdge_PLC_Local_IO_Cont",
		"FDM_Upgrade_Hardware_to_host_FDM_Server",
		"FDM_Upgrade_2_Hardware_to_host_FDM_Server",
		"FDM_Upgrade_3_Hardware_to_host_FDM_Server",
		"xPM_C300_Migration_Configuration_Cont",
		"Graphics_Migration_Displays_Shapes_Faceplates",
	]
	
	singleLineMappingDict = GS_Migration_Container_Attributes_Mapper.getSingleLineMapperDict()
	multiLineMappingDict = GS_Migration_Container_Attributes_Mapper.getMultiLineMapperDict()

	for containerName in attributeContianers:
		container = getContainer(product, containerName)
		replacedContainerDict = {}
		productMapperDetails = singleLineMappingDict.get(product.Name)
		
		if productMapperDetails:
			replacedContainerDict = productMapperDetails.get(containerName)
		if container and not replacedContainerDict:
			updateAttributeDict(container, msidAttributeDict, True)
		elif replacedContainerDict:
			updateAttributeDict(replacedContainerDict, msidAttributeDict, False, parentProduct, product, containerName)
		
	for containerName in multilineContainer:
		container = getContainer(product, containerName)
		replacedContainerDict = {}
		productMapperDetails = multiLineMappingDict.get(product.Name)
		if productMapperDetails:
			replacedContainerDict = productMapperDetails.get(containerName)
		if container and not replacedContainerDict:
			updateMultilineAttributeDict(container, msidAttributeDict, True)
		elif replacedContainerDict:
			updateMultilineAttributeDict(replacedContainerDict, msidAttributeDict, False, parentProduct, product, containerName)

	multilineContainer_fsc = ["FSC_to_SM_IO_Series_1_&_2_FSC_IO_configurations"]
	for containerName in multilineContainer_fsc:
		container = getContainer(product, containerName)
		if container:
			updateMultilineAttributeDict_fsc(container, msidAttributeDict)

	msidAttributeDict["MSID_Selected_Products"] = parentProduct.Attr(
			"MSID_Selected_Products"
	).GetValue()
	msidAttributeDict["Migration_MSID_System_Number"] = parentProduct.Attr(
		"Migration_MSID_System_Number"
	).GetValue()
	msidAttributeDict["Migration_MSID_Choices"] = parentProduct.Attr(
		"Migration_MSID_Choices"
	).GetValue()
	msidAttributeDict["MIgration_Scope_Choices"] = parentProduct.Attr(
		"MIgration_Scope_Choices"
	).GetValue()
	msidAttributeDict["MSID_Is_Site_Acceptance_Test_Required"] = parentProduct.Attr(
			"MSID_Is_Site_Acceptance_Test_Required"
		).GetValue()
	msidAttributeDict["MSID_Current_Experion_Release"] = parentProduct.Attr("MSID_Current_Experion_Release").GetValue()
	msidAttributeDict["MSID_Future_Experion_Release"] = parentProduct.Attr("MSID_Future_Experion_Release").GetValue()
	if product.Name == 'OPM':
		msidAttributeDict["OPM_Which_documentation_is_required"] = product.Attr(
			"OPM_Which_documentation_is_required"
		).GetValue()
		opm= getRowData(product,'OPM_Basic_Information','OPM_Is_this_is_a_Remote_Migration_Service_RMS')
		if opm=="Yes":
			msidAttributeDict["OPM_Is_this_is_a_Remote_Migration_Service_RMS"] = "Yes"
		else:
			msidAttributeDict["OPM_Is_this_is_a_Remote_Migration_Service_RMS"] = "No"
	elif product.Name == 'LCN One Time Upgrade':
		msidAttributeDict["MSID_Current_TPN_Release"] = parentProduct.Attr(
			"MSID_Current_TPN_Release"
		).GetValue()
		msidAttributeDict["MSID_Future_TPN_Release"] = parentProduct.Attr(
			"MSID_Future_TPN_Release"
		).GetValue()
	elif product.Name == 'Virtualization System Migration':
		if Quote.GetCustomField("isR2QRequest").Content == 'Yes':
			VirtWL = product.GetContainerByName('Virtualization_System_WorkLoad_Cont').Rows
			for WorkLoad in VirtWL:
				msidAttributeDict["Vir_Workload_"+str(WorkLoad['Work_Load_Type'])]=WorkLoad['Work_Load_Type']
	elif product.Name == 'FDM Upgrade 1':
		msidAttributeDict["FDM_Upgrade_Is_HW_required_for_this_FDM_1"] = product.Attr("FDM_Upgrade_Is_HW_required_for_this_FDM").GetValue()
		msidAttributeDict["FDM_Upgrade_Select_desired_FDM_release_1"] = product.Attr("FDM_Upgrade_Select_desired_FDM_release").GetValue()
		msidAttributeDict["FDM_Upgrade_Site_Acceptance_Test_1"] = product.Attr("FDM_Upgrade_Site_Acceptance_Test").GetValue()
	elif product.Name == 'FDM Upgrade 2':
		msidAttributeDict["FDM_Upgrade_Is_HW_required_for_this_FDM_2"] = product.Attr("FDM_Upgrade_Is_HW_required_for_this_FDM").GetValue()
		msidAttributeDict["FDM_Upgrade_Select_desired_FDM_release_2"] = product.Attr("FDM_Upgrade_Select_desired_FDM_release").GetValue()
		msidAttributeDict["FDM_Upgrade_Site_Acceptance_Test_2"] = product.Attr("FDM_Upgrade_Site_Acceptance_Test").GetValue()
	elif product.Name == 'FDM Upgrade 3':
		msidAttributeDict["FDM_Upgrade_Is_HW_required_for_this_FDM_3"] = product.Attr("FDM_Upgrade_Is_HW_required_for_this_FDM").GetValue()
		msidAttributeDict["FDM_Upgrade_Select_desired_FDM_release_3"] = product.Attr("FDM_Upgrade_Select_desired_FDM_release").GetValue()
		msidAttributeDict["FDM_Upgrade_Site_Acceptance_Test_3"] = product.Attr("FDM_Upgrade_Site_Acceptance_Test").GetValue()
	elif product.Name == 'EHPM/EHPMX/ C300PM':
		msidAttributeDict["MSID_Selected_Products"] = 'EHPM/EHPMX/ C300PM'
		msidAttributeDict["xPM_Is_FTE_Network_Infrastructure_Existing"] =  getRowData(product,'xPM_Migration_General_Qns_Cont','xPM_Is_FTE_Network_Infrastructure_Existing')
		msidAttributeDict["xPM_On_Process_Red_HPMs_EHPMs_for_EHPMX_mig"] =  getRowData(product,'xPM_Migration_General_Qns_Cont','xPM_On_Process_Red_HPMs_EHPMs_for_EHPMX_mig')
		msidAttributeDict["xPM_TPN_SW_Release_at_time_of_xPM_migration"] =  getRowData(product,'xPM_Migration_General_Qns_Cont','xPM_TPN_SW_Release_at_time_of_xPM_migration')
		msidAttributeDict["xPM_EPKS_SW_Release_at_time_of_xPM_migration"] = getRowData(product,'xPM_Migration_General_Qns_Cont','xPM_EPKS_SW_Release_at_time_of_xPM_migration')
		msidAttributeDict["xPM_Which_documentation_is_required"] = product.Attr(
			"xPM_Which_documentation_is_required"
		).GetValue()
		msidAttributeDict["xPM_Select_the_migration_scenario"] = product.Attr(
			"xPM_Select_the_migration_scenario"
		).GetValue()
		msidAttributeDict["xPM_Number_of_NIMs_configurations_to_be_migrated"] = product.Attr("xPM_NIMsconf").GetValue()
		msidAttributeDict["xPM_How_many_xPMs_configurations_are_we_migrating"] = getRowData(product,'xPM_Migration_General_Qns_Cont','xPM_How_many_xPMs_configurations_are_we_migrating')
		msidAttributeDict["MSID_Will_Honeywell_perform_equipment_installation"] = product.Attr("MSID_Will_Honeywell_perform_equipment_installation").GetValue()
		msidAttributeDict["xPM_Factory_Acceptance_Test_Required"] = product.Attr("xPM_Factory_Acceptance_Test_Required").GetValue()
		msidAttributeDict["MSID_FEL_Data_Gathering_Required"] = product.Attr("MSID_FEL_Data_Gathering_Required").GetValue()
	elif product.Name == 'TPS to Experion':
		msidAttributeDict["TPS_EX_Which_Documentation_Required"] = product.Attr(
			"TPS_EX_Which_Documentation_Required"
		).GetValue()
		msidAttributeDict["MSID_FEL_Data_Gathering_Required"] = product.Attr("MSID_FEL_Data_Gathering_Required").GetValue()
		msidAttributeDict["MSID_Acceptance_Test_Required"] = parentProduct.Attr("MSID_Acceptance_Test_Required").GetValue()
		msidAttributeDict["TPS_EX_Service_Acceptance_Test_Required"] = parentProduct.Attr("MSID_Acceptance_Test_Required").GetValue()
		msidAttributeDict["MSID_Is_Switch_Configuration_in_Honeywell_Scope"] = parentProduct.Attr("MSID_Is_Switch_Configuration_in_Honeywell_Scope").GetValue()
		msidAttributeDict["TPS_EX_Need_Domain_Controller_Added"] = product.Attr("TPS_EX_Need_Domain_Controller_Added").GetValue()
	elif product.Name == 'Orion Console':
		msidAttributeDict["Orion_Which_documentation_is_required"] = product.Attr("Orion_Which_documentation_is_required").GetValue()
		msidAttributeDict["OrionConstruction_Work_Package_doc_require"] = parentProduct.Attr("Yes-No Selection").GetValue()
	elif product.Name == 'CB-EC Upgrade to C300-UHIO':
		msidAttributeDict["MSID_Acceptance_Test_Required"] = parentProduct.Attr(
			"MSID_Acceptance_Test_Required"
		).GetValue()
	elif product.Name == 'EHPM HART IO':
		msidAttributeDict["EHPM_HART_IO_Which_documentation_is_required?"] = product.Attr(
			"EHPM_HART_IO_Which_documentation_is_required?"
		).GetValue()
		msidAttributeDict["EHPM_HART_IO_Costruction_Work_Package_documentation_required"] = parentProduct.Attr(
			"EHPM_HART_IO_Construction_Work_Package_doc_require"
		).GetValue()
	elif product.Name == 'xPM to C300 Migration':
		msidAttributeDict["xPM_C300_Which_Documentation_Required"] = product.Attr(
			"xPM_C300_Which_Documentation_Required"
		).GetValue()
		msidAttributeDict["MSID_Is_Switch_Configuration_in_Honeywell_Scope"] = parentProduct.Attr("MSID_Is_Switch_Configuration_in_Honeywell_Scope").GetValue()
		msidAttributeDict["ATT_NUMAMTOACE"] = product.Attr("ATT_NUMAMTOACE").GetValue()
		msidAttributeDict["ATT_NUMAMPTS"] = product.Attr("ATT_NUMAMPTS").GetValue()
	elif product.Name == 'LM to ELMM ControlEdge PLC':
		msidAttributeDict["LM_to_ELMM_Local_Remote_Flag"] = product.Attr(
			"LM_to_ELMM_Local_Remote_Flag"
		).GetValue()
		msidAttributeDict["MSID_Is_FTE_based_System_already_installed_on_Site"] = parentProduct.Attr(
			"MSID_Is_FTE_based_System_already_installed_on_Site"
		).GetValue()
		msidAttributeDict["LM_ELMM_Does_the_customer_want_Honeywell_to_configure_the_switches"] = parentProduct.Attr(
			"ATTR_COMQESYORN"
		).GetValue()
		msidAttributeDict["LM_ELMM_Construction_work_package_document_prepared_by_Honeywell"] = parentProduct.Attr("Yes-No Selection").GetValue()
	elif product.Name == 'ELCN':
		msidAttributeDict["MSID_FEL_Data_Gathering_Required"] = product.Attr(
			"MSID_FEL_Data_Gathering_Required"
		).GetValue()
	elif product.Name == 'C200 Migration':
		msidAttributeDict["MSID_Is_Switch_Configuration_in_Honeywell_Scope"] = parentProduct.Attr(
			"MSID_Is_Switch_Configuration_in_Honeywell_Scope"
		).GetValue()
	elif product.Name == 'Graphics Migration':
		msidAttributeDict["Graphics_Migration_Type_of_Existing_Displays"] = product.Attr(
			"Graphics_Migration_Type_of_Existing_Displays"
		).GetValue()
		msidAttributeDict["Graphics_Migration_For_existing_US_GUS_DSP_what_percentage_of_Standard_Builds_will_be_used?"] = product.Attr(
			"ATT_GMPERUSD"
		).GetValue()
		msidAttributeDict["Graphics_Migration_Is_Standard_Builds_used_for_EXP_to_EXP?"] = product.Attr(
			"Migration_Configuration_Is_Standard_Builds_used"
		).GetValue()
		msidAttributeDict["Graphics_Migration_FAT_required?"] = product.Attr(
			"Graphics_Migration_FAT_required?"
		).GetValue()
		msidAttributeDict["Graphics_Migration_Does_the_customer_require_SAT?"] = product.Attr(
			"Graphics_Migration_Does_the_customer_require_SAT?"
		).GetValue()
		msidAttributeDict["Graphics_Migration_Gap_Analysis_done?"] = product.Attr(
			"Graphics_Migration_Gap_Analysis_done?"
		).GetValue()
		msidAttributeDict["Graphics_Migration_DDS_Required?"] = product.Attr(
			"Graphics_Migration_DDS_Required?"
		).GetValue()
		msidAttributeDict["Graphics_Migration_FDS_Required?"] = product.Attr(
			"Graphics_Migration_FDS_Required?"
		).GetValue()
	elif product.Name == 'CWS RAE Upgrade':
		msidAttributeDict["CWS_Mig_For_MD_CD_work_are_we_doing_installation"] = product.Attr(
			"CWS_Mig_For_MD_CD_work_are_we_doing_installation"
		).GetValue()
		msidAttributeDict["CWS_Mig_HSE_and_Quality_Plan"] = product.Attr(
			"CWS_Mig_HSE_and_Quality_Plan"
		).GetValue()
		msidAttributeDict["CWS_Mig_Update_existing_documents"] = product.Attr(
			"CWS_Mig_Update_existing_documents"
		).GetValue()
		msidAttributeDict["CWS_Mig_Site_Acceptance_Test_Required"] = product.Attr(
			"CWS_Mig_Site_Acceptance_Test_Required"
		).GetValue()
		msidAttributeDict["CWS_Mig_Machine_Cross_Direction_controls_upgraded_peripheral_hardware_licensing"] = product.Attr(
			"CWS_Mig_Machine_Cross_Direction_controls_upgraded_peripheral_hardware_licensing"
		).GetValue()
		msidAttributeDict["CWS_Mig_Cross_Direction_controls_upgraded_peripheral_hardware_licensing"] = product.Attr(
			"CWS_Mig_Cross_Direction_controls_upgraded_peripheral_hardware_licensing"
		).GetValue()		
	elif product.Name == '3rd Party PLC to ControlEdge PLC/UOC':
		msidAttributeDict["LSS_PLC_Number_of_ControlEdge_PLC_Groups_required"] = product.Attr("LSS_PLC_Number_of_ControlEdge_PLC_Groups_required").GetValue()
		msidAttributeDict["LSS_PLC_Number_of_ControlEdge_UOC_vUOC_confi_req"] = product.Attr("LSS_PLC_Number_of_ControlEdge_UOC_vUOC_confi_req").GetValue()
		msidAttributeDict["LSS_PLC_Number_of_ControlEdge_PLC_UOC_vUOC_confi"] = product.Attr("LSS_PLC_Number_of_ControlEdge_PLC_UOC_vUOC_confi").GetValue()
		msidAttributeDict["LSS_PLC_How_many_existing_Cabinets_will_be_used"] = product.Attr("LSS_PLC_How_many_existing_Cabinets_will_be_used").GetValue()
		msidAttributeDict["LSS_Does_the_customer_want_Honeywell"] = product.Attr("LSS_Does_the_customer_want_Honeywell").GetValue()
		msidAttributeDict["LSS_Will_Honeywell_perform_equipment_installation"] = product.Attr("LSS_Will_Honeywell_perform_equipment_installation").GetValue()
		msidAttributeDict["LSS_Documentation_required?"] = product.Attr("LSS_Documentation_required?").GetValue()
		msidAttributeDict["LSS_PLC_EPKS_Software_Release"] = product.Attr("LSS_PLC_EPKS_Software_Release").GetValue()
		msidAttributeDict["LSS_PLC_Base_Media_Delivery"] = product.Attr("LSS_PLC_Base_Media_Delivery").GetValue()
		msidAttributeDict["LSS_Hardware_Drawings_Required?"] = product.Attr("LSS_Hardware_Drawings_Required?").GetValue()
		msidAttributeDict["LSS_PLC_Server_Redundancy"] = product.Attr("LSS_PLC_Server_Redundancy").GetValue()
		msidAttributeDict["LSS_PLC_Total_Number_of_new_SCADA_point_License"] = product.Attr("LSS_PLC_Total_Number_of_new_SCADA_point_License").GetValue()
		msidAttributeDict["LSS_PLC_Total_Number_of_new_PCDI_License"] = product.Attr("LSS_PLC_Total_Number_of_new_PCDI_License").GetValue()
		msidAttributeDict["MSID_Is_FTE_based_System_already_installed_on_Site"] = parentProduct.Attr("MSID_Is_FTE_based_System_already_installed_on_Site").GetValue()
		msidAttributeDict["LSS_Will_Honeywell_perform_equipment_installation"] = product.Attr("LSS_Will_Honeywell_perform_equipment_installation").GetValue()
		msidAttributeDict["LSS_Does_the_customer_want_Honeywell"] = product.Attr("LSS_Does_the_customer_want_Honeywell").GetValue()
		msidAttributeDict["LSS_FEL/Data_gathering_required?"] = product.Attr("LSS_FEL/Data_gathering_required?").GetValue()
	elif product.Name == 'QCS RAE Upgrade':
		msidAttributeDict["QCS_Mig_system_contain_Serial_Communication_links"] = product.Attr("QCS_Mig_system_contain_Serial_Communication_links").GetValue()
		msidAttributeDict["QCS_Mig_switches_be_included_for_Measurement"] = product.Attr("QCS_Mig_switches_be_included_for_Measurement").GetValue()
		msidAttributeDict["QCS_Mig_Manual_translation_of_databases_required_DRG_file"] = product.Attr("QCS_Mig_Manual_translation_of_databases_required_DRG_file").GetValue()
		msidAttributeDict["QCS_Mig_Customization_to_be_migrated"] = product.Attr("QCS_Mig_Customization_to_be_migrated").GetValue()
		msidAttributeDict["QCS_Mig_HSE_and_Quality_Plan"] = product.Attr("QCS_Mig_HSE_and_Quality_Plan").GetValue()
		msidAttributeDict["QCS_Mig_Update_existing_documents"] = product.Attr("QCS_Mig_Update_existing_documents").GetValue()
		msidAttributeDict["QCS_Mig_Site_Acceptance_Test_Req"] = product.Attr("QCS_Mig_Site_Acceptance_Test_Req").GetValue()
	elif product.Name == 'FSC to SM':
		msidAttributeDict["FSC_to_SM_Which_documentation_is_required"] = product.Attr("FSC_to_SM_Which_documentation_is_required").GetValue()
	"""msidAttributeDict["FSC_to_SM_IO_Is_the_series_2_FTA_and_SIC_cable_reu"] = product.Attr(
		"FSC_to_SM_IO_Is_the_series_2_FTA_and_SIC_cable_reu"
	).GetValue()"""

	return msidAttributeDict
def DeleteQuoteTableItem(table):
	item_delete = []
	for row in table.Rows:
		if str(row['MIgration_GUID'])  == "": # exception for IAA -Project
			item_delete.append(row.Id)
	c=sorted(item_delete, reverse=True)
	for r in c:
		table.DeleteRow(r)
	table.Save()

msidAttributeDict = dict()
singleLineMappingDict = GS_Migration_Container_Attributes_Mapper.getSingleLineMapperDict()
multiLineMappingDict = GS_Migration_Container_Attributes_Mapper.getMultiLineMapperDict()
table = Quote.QuoteTables["Migration_Document_Data"]
#table.Rows.Clear()
"""parentItemGUID = ''
for i in arg.QuoteItemCollection:
	parentItemGUID = i.ParentItemGuid"""
DeleteQuoteTableItem(table)

migrlvlCont = Product.GetContainerByName("CONT_Migration_MSID_Selection")
for msidlvlcont in migrlvlCont.Rows:
	msidcont = msidlvlcont.Product.GetContainerByName("CONT_MSID_SUBPRD")
	for msidRow in msidcont.Rows:
		msidAttributeDict = populateMsidAttributes(msidRow.Product, msidlvlcont.Product)
		x = RestClient.SerializeToJson (msidAttributeDict)
		Trace.Write(RestClient.SerializeToJson (msidAttributeDict))
		populateQuoteTable(msidlvlcont.UniqueIdentifier, msidAttributeDict, table)

		if msidRow['Selected_Products'] == 'Integrated Automation Assessment':
			contIAA1 = getContainer(msidRow.Product, "IAA Inputs_Cont")
			for row in contIAA1.Rows:
				guid = msidRow.UniqueIdentifier
				msid_esid = row["IAA_List_individual_MSIDs/ESIDs"]
				attr = row["IAA_Assessment_Type"]
				attr_value = row["IAA_Quantity"]
				populateQuoteTableIAA(guid, attr, attr_value, table, msid_esid)

			contIAA2 = getContainer(msidRow.Product, "IAA Inputs_Cont_2")
			for row in contIAA2.Rows:
				guid = msidRow.UniqueIdentifier
				attr = row["Name"]
				attr_value = row["Quantity"]
				populateQuoteTableIAA(guid, attr, attr_value, table)

			contIAAprice = getContainer(msidRow.Product, "IAA Pricing")
			for row in contIAAprice.Rows:
				guid = msidRow.UniqueIdentifier
				attr = row["Name"]
				attr_value = row["Price"]
				populateQuoteTableIAA(guid, attr, attr_value, table)

table.Save()