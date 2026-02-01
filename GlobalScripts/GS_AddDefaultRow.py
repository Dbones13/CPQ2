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
        if container.Rows.Count == 0:
            row = container.AddNewRow(False)
            for i in range(rows - 1):
                container.CopyRow(row.RowIndex)
        if containerName in ('TPS_EX_Additional_Servers','TPS_EX_Additional_Stations','TPS_EX_Station_Conversion_EST',"TPS_EX_Conversion_ACET_EAPP"):
            populateType(container)
        container.Calculate()

def populateOrionWriteInContainerRows():
    containerName = "Orion_General_Information_Container"
    container = Product.GetContainerByName(containerName)
    writeIns = ["Third Party labor for Unboxing / Installation / etc","Orion Console Freight"]
    writeInProducts = ["Write-In Third Party Labor","Write-In Freight"]
    if container.Rows.Count != 0:
        return
    for writeIn,WriteInProduct in zip(writeIns,writeInProducts):
        newRow = container.AddNewRow(False)
        newRow["WriteIn"] = writeIn
        newRow["WriteInProduct"] = WriteInProduct
    container.Calculate()

    writeIns = ["Cables and adapters per 2 base unit w/55in","Cables and adapters per 2 base unit w/23in","Cables and adapters per 3 base unit w/55in","Cables and adapters per 3 base unit w/23in"]
    containerName = "Orion_General_Information"
    container = Product.GetContainerByName(containerName)
    if container.Rows.Count != 0:
        return
    for writeIn in writeIns:
        newRow = container.AddNewRow(False)
        newRow["WriteIn"] = writeIn
    container.Calculate()

containerAttributeDict = dict()

containerAttributeDict['OPM'] = ["OPM_Basic_Information","OPM_Node_Configuration"]

containerAttributeDict['MSID'] = [
    "MSID_CommonQuestions",
    "NONSESP_Design_Inputs_for_Experion_Upgrade_License",
    "NONSESP_Design_Inputs_for_eServer_Upgrade_License",
    "LCN_Design_Inputs_for_TPN_OTU_Upgrade",
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
    "ELCN_Upgrade_New_ELCN_Nodes",
    "ELCN_Network_Gateway_Upgrade",
    "ELCN_Services",
    "ELCN_Server_Cabinet_Configuration",
    "xPM_Services_Cont",
    "xPM_Network_Upgrade_Cont",
    "ENB_Config_Asset_DB_Cont",
    "ENB_Migration_General_Qns_Cont",
    "xPM_Config_Asset_DB_Cont",
    "xPM_Migration_General_Qns_Cont",
    "xPM_Migration_Scenario_Cont",
    "Orion_Services",
    "Orion_General_Information_Container2",
    "TCMI_General_Information",
    "TCMI_Hardware_and_Licenses",
    "TCMI_Services",
    "C200_Migration_Scenario_Cont",
    "C200_Migration_General_Qns_Cont",
    "C200_Services_1_Cont",
    "C200_Services_2_Cont",
    "C200_C300_Series_C_Cabinet_Config_Cont",
    "C200_C300_Series_C_Cabinet_Config_Cont_FAOnly",
    "EHPM_HART_IO_General_Qns_Cont",
    "EHPM_HART_IO_Configuration_Cont",
    "EHPM_HART_IO_Services_Cont",
    "CB_EC_migration_to_C300_UHIO_Configuration_Cont",
    "CB_EC_Services_1_Cont",
    "CB_EC_Services_2_Cont",
    "CB_EC_Third_party_items_Cont",
    "FSC_to_SM_3rd_Party_Items",
    "FSC_to_SM_General_Information",
    "FSC_to_SM_Services",
    "FSC_to_SM_IO_Services2",
    "FSC_to_SM_IO_Services",
    "FSC_to_SM_IO_New_SM_Cabinet_Configuration",
    "FSC_to_SM_IO_Migration_General_Information2",
    "FSC_to_SM_IO_Migration_General_Information",
    "xPM_C300_General_Qns_Cont",
    "xPM_C300_Series_C_Cabinet_Configuration_FAOnly",
    "xPM_C300_Series_ C_Cabinet_Configuration",
    "xPM_C300_config_Asset_DB",
    "xPM_C300_Services_Cont",
    "EHPM_HART_IO_Services_Cont_1",
    "FDM_Upgrade_General_questions",
    "FDM_Upgrade_Services",
    "LM_to_ELMM_ControlEdge_PLC_Migration_Gen_Cont",
    "LM_to_ELMM_3rd_Party_Items",
    "LM_to_ELMM_Services",
    "TPS_to_EX_3rd_Party_Items",
    "FDM_Upgrade_Configuration",
    "FDM_Upgrade_Hardware_to_host_FDM_Server",
    "XP10_Actuator_General_Information",
    "Graphics_Migration_Migration_Scenario",
    "Graphics_Migration_Training_Testing_Documentation",
    "Graphics_Migration_Additional_Questions",
    "Graphics_Migration_Displays_Shapes_Faceplates",
    "CD_Actuator_IF_Upgrade_Services_Cont",
    "CD_Actuator_IF_Upgrade_General_Info_Cont",
    "CD_Actuator_pricing_factory_cost"
]


for name in containerAttributeDict[Product.Name]:
    container = Product.GetContainerByName(name)
    if container.Rows.Count == 0:
        row = container.AddNewRow(False)
        if name not in ['ELCN_Server_Cabinet_Configuration','CB_EC_Third_party_items_Cont','LM_to_ELMM_ControlEdge_PLC_Migration_Gen_Cont','LM_to_ELMM_Services','Graphics_Migration_Migration_Scenario','Graphics_Migration_Training_Testing_Documentation','Graphics_Migration_Additional_Questions']:
            container.CopyRow(row.RowIndex)
        if name not in ['ENB_Config_Asset_DB_Cont', 'ELCN_Server_Cabinet_Configuration', 'CB_EC_Third_party_items_Cont','LM_to_ELMM_ControlEdge_PLC_Migration_Gen_Cont','LM_to_ELMM_Services','TPS_to_EX_3rd_Party_Items','Graphics_Migration_Migration_Scenario','Graphics_Migration_Training_Testing_Documentation','Graphics_Migration_Additional_Questions',"Graphics_Migration_Displays_Shapes_Faceplates"]:
            container.CopyRow(row.RowIndex)
        if name == 'ELCN_Upgrade_New_ELCN_Nodes':
            container.CopyRow(row.RowIndex)
            container.CopyRow(row.RowIndex)
        if name == 'FSC_to_SM_3rd_Party_Items':
            container.CopyRow(row.RowIndex)
            container.CopyRow(row.RowIndex)
        if name == 'FSC_to_SM_IO_Migration_General_Information2':
            container.CopyRow(row.RowIndex)
            container.CopyRow(row.RowIndex)
        '''if name == 'C200_Third_Party_Items_Cont':
            container.CopyRow(row.RowIndex)'''
        if name == 'xPM_C300_config_Asset_DB':
            container.CopyRow(row.RowIndex)
            container.CopyRow(row.RowIndex)
            container.CopyRow(row.RowIndex)
        if  name == 'xPM_Config_Asset_DB_Cont':
            i = 5
            while i > 0:
                container.CopyRow(row.RowIndex)
                i -= 1
#        container.Calculate()
populateOrionWriteInContainerRows()
populateTPSContainerRows()