def populateType(con):
	typeNameDict = {
		"TPS_EX_Additional_Servers" : "TPS_EX_Additional_Server_Type",
		"TPS_EX_Additional_Stations" : "TPS_EX_Additional_Stations_Type",
		"TPS_EX_Station_Conversion_EST" : "TPS_EX_Station_Conversion_Type",
		"TPS_EX_Conversion_ACET_EAPP" : "TPS_EX_Conversion_ACET_EAPP_Type"
	}
	typeDict = {
		"TPS_EX_Additional_Servers": [
			"Experion Server (ESV) - Desk",
			"Experion Server (ESV) - Cabinet"
		],
		"TPS_EX_Additional_Stations": [
			"Flex Station - Desk",
			"Flex Station - Cabinet",
			"Flex Station - Orion",
			"Console Station - Desk",
			"Console Station - Cabinet",
			"Console Station - Orion",
			"Console Extended Station - Desk",
			"Console Extended Station - Cabinet",
			"Console Extended Station - Orion",
			"ES-T Station - Desk",
			"ES-T Station - Cabinet",
			"ES-T Station - Orion"
		],
		"TPS_EX_Station_Conversion_EST":[
			"US_AM to ES-T",
			"GUS to ES-T",
			"UGUS to ES-T"
		],
		"TPS_EX_Conversion_ACET_EAPP":[
			"APP to ACE-T",
			"APP to EAPP"
		]
	}
	l = typeDict[con.Name]
	for row in con.Rows:
		row[typeNameDict[con.Name]] = l[row.RowIndex]

def populateTPSContainerRows():
	containerDict = {
		"TPS_EX_Additional_Servers": 2,
		"TPS_EX_Additional_Stations": 12,
		"TPS_EX_Bundle_Conversion_Server_Stations": 1,
		"TPS_EX_Conversion_ESVT_Server": 2,
		"TPS_EX_General_Questions": 1,
		"TPS_EX_Monitors": 1,
		"TPS_EX_Service" : 1,
		"TPS_EX_Station_Conversion_EST": 3,
		"TPS_EX_Server_Cabinet_Config" : 1,
		"TPS_EX_Conversion_ACET_EAPP" : 2
	}

	for containerName, rows in containerDict.items():
		container = Product.GetContainerByName(containerName)
		if container is not None:
			if container.Rows.Count == 0:
				row = container.AddNewRow(False)
				for i in range(rows - 1):
					container.CopyRow(row.RowIndex)
			if containerName in ('TPS_EX_Station_Conversion_EST',"TPS_EX_Conversion_ACET_EAPP",'TPS_EX_Additional_Servers','TPS_EX_Additional_Stations'):
				populateType(container)
			#container.Calculate()

def populateOrionWriteInContainerRows():
	containerName = "Orion_General_Information_Container"
	container = Product.GetContainerByName(containerName)
	writeIns = ["Third Party labor for Unboxing / Installation / etc","Orion Console Freight"]
	writeInProducts = ["Write-In Third Party Labor","Write-In Freight"]
	if container is not None:
		if container.Rows.Count != 0:
			return
	for writeIn,WriteInProduct in zip(writeIns,writeInProducts):
		if container is not None:
			newRow = container.AddNewRow(False)
			newRow["WriteIn"] = writeIn
			newRow["WriteInProduct"] = WriteInProduct
			container.Calculate()

	writeIns = ["Cables and adapters per 2 base unit w/55in","Cables and adapters per 2 base unit w/23in","Cables and adapters per 3 base unit w/55in","Cables and adapters per 3 base unit w/23in"]
	containerName = "Orion_General_Information"
	container = Product.GetContainerByName(containerName)
	if container is not None:
		if container.Rows.Count != 0:
			return
		for writeIn in writeIns:
			newRow = container.AddNewRow(False)
			newRow["WriteIn"] = writeIn
		container.Calculate()

containerAttributeDict = dict()

containerAttributeDict = {
	"OPM": ["OPM_Basic_Information", "OPM_Node_Configuration", "OPM_Migration_platforms", "OPM_FTE_Switches_migration_info", "OPM_Services"],
	"EBR": ["EBR_Basic_Information", "EBR_Upgrade", "EBR_New_Additional_EBR", "EBR_Hardware_to_Host_EBR_Physical_Node_Only", "EBR_Services"],
	"Non-SESP Exp Upgrade": ["NONSESP_Design_Inputs_for_Experion_Upgrade_License", "NONSESP_Design_Inputs_for_eServer_Upgrade_License"],
	"LCN One Time Upgrade": ["LCN_Design_Inputs_for_TPN_OTU_Upgrade"],
	"ELCN": ["ELCN_Basic_Information", "ELCN_Upgrade_New_ELCN_Nodes", "ELCN_Network_Gateway_Upgrade", "ELCN_Services", "ELCN_Server_Cabinet_Configuration"],
	"xPM to C300 Migration": ["xPM_Config_Asset_DB_Cont", "xPM_Migration_General_Qns_Cont", "xPM_Migration_Scenario_Cont", "xPM_C300_General_Qns_Cont", "xPM_C300_Series_C_Cabinet_Configuration_FAOnly", "xPM_C300_Series_C_Cabinet_Configuration", "xPM_C300_config_Asset_DB", "xPM_C300_Services_Cont"],
	"Orion Console": ["Orion_General_Information_Container2", "Orion_Services"],
	"TCMI": ["TCMI_General_Information", "TCMI_Hardware_and_Licenses", "TCMI_Services"],
	"C200 Migration": ["C200_Migration_General_Qns_Cont", "C200_Migration_Scenario_Cont", "C200_Services_1_Cont", "C200_Services_2_Cont", "C200_C300_Series_C_Cabinet_Config_Cont", "C200_C300_Series_C_Cabinet_Config_Cont_FAOnly", "C200_Third_Party_Items_Cont"],
	"EHPM HART IO": ["EHPM_HART_IO_General_Qns_Cont", "EHPM_HART_IO_Configuration_Cont", "EHPM_HART_IO_Services_Cont", "EHPM_HART_IO_Services_Cont_1"],
	"CB-EC Upgrade to C300-UHIO": ["CB_EC_migration_to_C300_UHIO_Configuration_Cont", "CB_EC_Services_1_Cont", "CB_EC_Services_2_Cont", "CB_EC_Third_party_items_Cont"],
	"FSC to SM": ["FSC_to_SM_3rd_Party_Items", "FSC_to_SM_General_Information", "FSC_to_SM_Services", "FSC_to_SM_IO_Services2", "FSC_to_SM_IO_Services", "FSC_to_SM_IO_New_SM_Cabinet_Configuration", "FSC_to_SM_IO_Migration_General_Information2", "FSC_to_SM_IO_Migration_General_Information"],"FSC to SM IO Migration": ["FSC_to_SM_IO_Migration_General_Information2"],
	"FDM Upgrade": ["FDM_Upgrade_General_questions", "FDM_Upgrade_2_General_questions", "FDM_Upgrade_3_General_questions", "FDM_Upgrade_Services", "FDM_Upgrade_2_Services", "FDM_Upgrade_3_Services", "FDM_Upgrade_Configuration", "FDM_Upgrade_2_Configuration", "FDM_Upgrade_3_Configuration", "FDM_Upgrade_Hardware_to_host_FDM_Server", "FDM_Upgrade_2_Hardware_to_host_FDM_Server", "FDM_Upgrade_3_Hardware_to_host_FDM_Server", "FDM_Upgrade_Additional_Configuration", "FDM_Upgrade_2_Additional_Configuration", "FDM_Upgrade_3_Additional_Configuration"],
	"LM to ELMM": ["LM_to_ELMM_ControlEdge_PLC_Migration_Gen_Cont", "LM_to_ELMM_3rd_Party_Items", "LM_to_ELMM_Services"],
	"TPS to Experion": ["TPS_to_EX_3rd_Party_Items"],
	"XP10 Actuator": ["XP10_Actuator_General_Information"],
	"Graphics Migration": [ "Graphics_Migration_Displays_Shapes_Faceplates"],
	"CD Actuator Upgrade": ["CD_Actuator_IF_Upgrade_Services_Cont", "CD_Actuator_IF_Upgrade_General_Info_Cont", "CD_Actuator_pricing_factory_cost"],
	"EHPM/EHPMX/ C300PM" : ["ENB_Config_Asset_DB_Cont","ENB_Migration_General_Qns_Cont","xPM_Config_Asset_DB_Cont","xPM_Migration_General_Qns_Cont"],
	"LM to ELMM ControlEdge PLC" : ["LM_to_ELMM_ControlEdge_PLC_Migration_Gen_Cont","LM_to_ELMM_3rd_Party_Items"],
	"TCMI" : ["TCMI_GENERAL_INFORMATION","TCMI_Hardware_and_Licenses"],
    "CD Actuator I-F Upgrade" :["CD_Actuator_pricing_factory_cost"],
    "3rd Party PLC to ControlEdge PLC/UOC" :["LSS_Third_party_items"]
}



for name in containerAttributeDict[Product.Name]:
	container = Product.GetContainerByName(name)
	if container is not None:
		if container.Rows.Count == 0:
			row = container.AddNewRow(False)
			'''if name not in ['ELCN_Server_Cabinet_Configuration','CB_EC_Third_party_items_Cont','LM_to_ELMM_ControlEdge_PLC_Migration_Gen_Cont','LM_to_ELMM_Services','Graphics_Migration_Migration_Scenario','Graphics_Migration_Training_Testing_Documentation','Graphics_Migration_Additional_Questions','FDM_Upgrade_Configuration','FDM_Upgrade_2_Configuration','FDM_Upgrade_3_Configuration','FDM_Upgrade_Hardware_to_host_FDM_Server','FDM_Upgrade_2_Hardware_to_host_FDM_Server','FDM_Upgrade_3_Hardware_to_host_FDM_Server','FDM_Upgrade_Additional_Configuration','FDM_Upgrade_2_Additional_Configuration','FDM_Upgrade_3_Additional_Configuration']:
				container.CopyRow(row.RowIndex)
			if name not in ['ENB_Config_Asset_DB_Cont', 'ELCN_Server_Cabinet_Configuration', 'CB_EC_Third_party_items_Cont','LM_to_ELMM_ControlEdge_PLC_Migration_Gen_Cont','LM_to_ELMM_Services','TPS_to_EX_3rd_Party_Items','Graphics_Migration_Migration_Scenario','Graphics_Migration_Training_Testing_Documentation','Graphics_Migration_Additional_Questions',"Graphics_Migration_Displays_Shapes_Faceplates",'FDM_Upgrade_Configuration','FDM_Upgrade_2_Configuration','FDM_Upgrade_3_Configuration','FDM_Upgrade_Hardware_to_host_FDM_Server','FDM_Upgrade_2_Hardware_to_host_FDM_Server','FDM_Upgrade_3_Hardware_to_host_FDM_Server','FDM_Upgrade_Additional_Configuration','FDM_Upgrade_2_Additional_Configuration','FDM_Upgrade_3_Additional_Configuration']:
				container.CopyRow(row.RowIndex)'''
			if name == 'TPS_to_EX_3rd_Party_Items':
				container.CopyRow(row.RowIndex)
			if name in ['FSC_to_SM_IO_Migration_General_Information2','LM_to_ELMM_3rd_Party_Items','EHPM_HART_IO_Configuration_Cont','CD_Actuator_pricing_factory_cost']:
				container.CopyRow(row.RowIndex)
				container.CopyRow(row.RowIndex)
			elif name in ['xPM_C300_config_Asset_DB','FSC_to_SM_3rd_Party_Items']:
				container.CopyRow(row.RowIndex)
				container.CopyRow(row.RowIndex)
				container.CopyRow(row.RowIndex)
			elif name in ['LCN_Design_Inputs_for_TPN_OTU_Upgrade','NONSESP_Design_Inputs_for_Experion_Upgrade_License','NONSESP_Design_Inputs_for_eServer_Upgrade_License','ELCN_Basic_Information','EHPM_HART_IO_General_Qns_Cont','EBR_Basic_Information','EBR_Upgrade','C200_Migration_General_Qns_Cont','xPM_Migration_General_Qns_Cont','Graphics_Migration_Displays_Shapes_Faceplates','TCMI_General_Information','TCMI_Hardware_and_Licenses','CB_EC_migration_to_C300_UHIO_Configuration_Cont']:
				container.CopyRow(row.RowIndex)
			elif name in ['xPM_Config_Asset_DB_Cont','ELCN_Upgrade_New_ELCN_Nodes']:
				i = 5
				while i > 0:
					container.CopyRow(row.RowIndex)
					i -= 1
			elif name == 'CB_EC_Third_party_items_Cont':
				row["CB_EC_Name"] = "3rd Party Hardware"
#        container.Calculate()
if Product.Name == 'ELCN':
    Product.DisallowAttr('ELCN_Select_Switch_configuration_required')
Session["traceOnload"] = 'True'
populateOrionWriteInContainerRows()
if Product.Name == "TPS to Experion":
    populateTPSContainerRows()