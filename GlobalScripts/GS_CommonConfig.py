###############################################################################################
# Class CL_CommonSettings:
# Class to store general Common properties
###############################################################################################
class CL_CommonSettings:
    getQuoteType = {
        'Project' : "Projects",
        'Change Order' : "Projects",
        'Spot Service' : "Parts and Spot",
        'Parts/Hardware/K&E' : "Parts and Spot",
        'Products' : "Parts and Spot",
        'Software Only' : "Parts and Spot",
        'Automation College' : "Parts and Spot",
        'Run Rate' : "Parts and Spot",
        'Contract New' : 'Contract New',
        'Contract Renewal' : 'Contract Renewal'
    }
    setdefaultvalue ={'QI_Expedite_Fees':0,'UnitMpaPrice':0,'msid_QInumber':'','MSID':'','EGAP_Contigency_Costs_USD':0}
    listprice_cal_WISS = {'ListPrice_WISSP':0,'WISSP_FLAG':0,'RollupValue':0}
    setBeforeQuoteItems = dict()
    setBeforeEffectivedate = dict()
    cyberProductfromtable = []
    TotalLaborqty={"Qty":'0'}

    getLaborContainer = {
        "ControlEdge PLC System": {
            "checkAll": 'CE PLC Engineering Labor Container',
            'checkAll_1': 'CE PLC Additional Custom Deliverables'
        },
        "PMD System": {
            "checkAll": "PMD Engineering Labor Container"
        },
        "ControlEdge UOC System": {
            "checkAll": 'CE UOC Engineering Labor Container',
            'checkAll_1': 'CE UOC Additional Custom Deliverables'
        },
        "ControlEdge CN900 System": {
            "checkAll": 'CE CN900 Engineering Labor Container',
            'checkAll_1': 'CE CN900 Additional Custom Deliverables'
        },
        "ControlEdge RTU System": {
            "checkAll": 'CE RTU Engineering Labor Container',
            'checkAll_1': 'CE RTU Additional Custom Deliverables'
        },
        "Write-in Products": {
            "checkAll": 'WriteInProduct'
        },
        "Solution Enhancement Support Program": {
            'checkAll': 'SC_Models_Scope',
            'checkAll_1': ['SC_Select_MSID_Cont', 'SC_Select_MSID_Cont_Hidden'],
            'checkAll_2': 'SC_SESP_MultiSites',
            'checkAll_3': {
                'New': 'SC_Invalid_Models',
                'Renewal': 'SC_Invalid_Models_Renewal'
            },
            'checkAll': {
                'New': 'SC_Models_Scope',
                'Renewal': 'SC_Models_Scope_Renewal'
            },
            'CalculateAndTrigger':'ScriptExecutor.Execute("GS_MSIDs_OTU_SESP")'
        },
        "Honeywell Digital Prime": {
            'checkAll': 'SC_MSID_Container',
            'checkAll_2': 'SC_SESP_MultiSites',
            'CalculateAndTrigger':'HDP_msid_count(laborRows, Product)'
        },
        "Experion Extended Support - RQUP ONLY": {
            'checkAll': 'SC_MSID_Container',
            'checkAll_1': 'SC_Experion_Models_Scope',
            'checkAll_2': 'SC_SESP_MultiSites',
            'CalculateAndTrigger':'ScriptExecutor.Execute("GS_Update_Model_Msid_SelectAll")'
        },
        "Parts Management": {
            'checkAll': 'SC_P1P2_Parts_Details',
            'checkAll_1': 'SC_P1P2_Invalid_Parts'
        },
        "MES Performix": {
            'checkAll': 'SC_MES_Models_Scope',
            'checkAll_1': 'SC_MES_Invalid_Models'
        },
        "Local Support Standby": {
            'checkAll': 'SC_Local_Support_Standby_validModel',
            'checkAll_1': {
                'Renewal': 'SC_ValidModels_HR_RWL'
            }
        },
        "Workforce Excellence Program": {
            'checkAll': 'SC_WEP_Models_Scope_HIF',
            'checkAll_1': 'SC_WEP_Invalid_Models_HIF',
            'checkAll_2': 'SC_WEP_Models_Scope_IFS',
            'checkAll_3': 'SC_WEP_Invalid_Models_IFS',
            'checkAll_4': 'SC_WEP_Models_Scope_Halo',
            'checkAll_5': 'SC_WEP_Invalid_Models_Halo',
            'checkAll_6': 'SC_WEP_Models_Scope_Training',
            'checkAll_7': 'SC_WEP_Invalid_Models_Training',
            'checkAll_8': 'SC_WEP_Models_Scope_TNA',
            'checkAll_9': 'SC_WEP_Invalid_Models_TNA',
            'checkAll_10': 'SC_WEP_Configurable_Models_Training'
        },
        "BGP inc Matrikon": {
            'checkAll': 'SC_BGP_Models_Scope_Cont',
            'checkAll_1': 'SC_BGP_Invalid_Cont'
        },
        "Cyber": {
            'checkAll': 'SC_Cyber_Models_Scope_Cont',
            'checkAll_1': 'SC_Cyber_Invalid_Cont'
        },
        "Generic Module": {
            'checkAll': 'SC_GN_AT_Models_Scope_Cont',
            'checkAll_1': 'SC_GN_AT_Invalid_Cont'
        },
        "Third Party Services": {
            'checkAll': 'SC_TPS_Models_Scope',
            'checkAll_1': 'SC_TPS_Invalid_Models'
        },
        "Experion HS System": {
            'checkAll': 'Experion HS Engineering Labor Container',
            'checkAll_1': 'Experion HS Additional Custom Deliverables'
        },
        "ControlEdge PCD System": {
            'checkAll': 'PCD Engineering Labor Container',
            'checkAll_1': 'PCD Additional Custom Deliverables'
        },
        "Generic System": {
            'checkAll': 'Generic Engineering Labor Container',
            'checkAll_1': 'Generic Additional Custom Deliverables'
        },
        "Experion LX Generic": {
            'checkAll': 'Generic Engineering Labor Container',
            'checkAll_1': 'Generic Additional Custom Deliverables'
        },
        "MasterLogic-200 Generic": {
            'checkAll': 'Generic Engineering Labor Container',
            'checkAll_1': 'Generic Additional Custom Deliverables'
        },
        "MasterLogic-50 Generic": {
            'checkAll': 'Generic Engineering Labor Container',
            'checkAll_1': 'Generic Additional Custom Deliverables'
        },
        "MasterLogic-50 Generic": {
            'checkAll': 'Generic Engineering Labor Container',
            'checkAll_1': 'Generic Additional Custom Deliverables'
        },
        "PlantCruise System": {
            'checkAll': 'PlantCruise Engineering Labor Container',
            'checkAll_1': 'PlantCruise Additional Custom Deliverables'
        },
        "HC900 System": {
            'checkAll': 'HC900 Engineering Labor Container',
            'checkAll_1': 'HC900 Additional Custom Deliverables'
        },
        "Terminal Manager": {
            'checkAll': 'Terminal Engineering Labor Container',
            'checkAll_1': 'Terminal Additional Custom Deliverables'
        },
        "Variable Frequency Drive System": {
            'checkAll': 'VFD Engineering Labor Container',
            'checkAll_1': 'VFD Additional Custom Deliverables'
        },
        "Measurement IQ System": {
            'checkAll': 'MIQ Engineering Labor Container',
            'checkAll_1': 'MIQ Additional Custom Deliverables'
        },
        "Field Device Manager": {
            'checkAll': 'FDM Engineering Labor Container',
            'checkAll_1': 'FDM Additional Custom Deliverables'
        },
        "Safety Manager ESD": {
            'checkAll': 'SM Safety System - ESD/FGS/BMS/HIPPS Container',
            'checkAll_1': 'SM_Additional_Custom_Deliverables_Labor_Container',
            'checkAll_2': 'SM_SSE_Engineering_Labor_Container'
        },
        "Safety Manager FGS": {
            'checkAll': 'SM Safety System - ESD/FGS/BMS/HIPPS Container',
            'checkAll_1': 'SM_Additional_Custom_Deliverables_Labor_Container',
            'checkAll_2': 'SM_SSE_Engineering_Labor_Container'
        },
        "Safety Manager BMS": {
            'checkAll': 'SM Safety System - ESD/FGS/BMS/HIPPS Container',
            'checkAll_1': 'SM_Additional_Custom_Deliverables_Labor_Container',
            'checkAll_2': 'SM_SSE_Engineering_Labor_Container'
        },
        "Safety Manager HIPPS": {
            'checkAll': 'SM Safety System - ESD/FGS/BMS/HIPPS Container',
            'checkAll_1': 'SM_Additional_Custom_Deliverables_Labor_Container',
            'checkAll_2': 'SM_SSE_Engineering_Labor_Container'
        },
        "Experion Enterprise System": {
            'checkAll': 'Hardware Engineering Labour Container',
            'checkAll_1': 'System_Network_Engineering_Labor_Container',
            'checkAll_2': 'System_Interface_Engineering_Labor_Container',
            'checkAll_3': 'HMI_Engineering_Labor_Container',
            'checkAll_4': 'Additional_CustomDev_Labour_Container',
            'checkAll_5': 'EBR_Engineering_Labor_Container'
        },
        "New / Expansion Project": {
            'checkAll': 'Labor_Container',
            'checkAll_1': 'PLE_Labor_Container',
            'checkAll_2': 'Project_management_Labor_Container',
            'checkAll_3': 'PM_Additional_Custom_Deliverables_Labor_Container',
            'checkAll_4': 'Staging_and_Integration_Expense_Cont'
        },
        "3rd Party Devices/Systems Interface (SCADA)": {
            'checkAll': 'SCADA_Engineering_Labor_Container',
            'checkAll_1': 'SCADA_Additional_Custom_Deliverables_Container'
        },
        "Experion MX System": {
            'checkAll': 'Experion_mx_Labor_Container',
            'checkAll_1': 'Experion_mx_labor_Additional_Cust_Deliverables_con'
        },
        "MXProLine System": {
            'checkAll': 'MXPro_Labor_Container',
            'checkAll_1': 'MXPro_Labor_Additional_Cust_Deliverables_con'
        },
        "C300 System": {
            'checkAll': 'C300_Engineering_Labor_Container',
            'checkAll_1': 'C300_Additional_Custom_Deliverables_Container'
        },
        "Digital Video Manager": {
            'checkAll': 'DVM_Engineering_Labor_Container',
            'checkAll_1': 'DVM_Additional_Labour_Container'
        },
        "Virtualization System": {
            'checkAll': 'Virtualization_Labor_Deliverable',
            'checkAll_1': 'Virtualization_Additional_Custom_Deliverables'
        },
        "eServer System": {
            'checkAll': 'eServer_Labor_Container',
            'checkAll_1': 'eServer_Labor_Additional_Cust_Deliverables_con'
        },
        "ARO, RESS & ERG System": {
            'checkAll': 'ARO_RESS_Engineering_Labor_Container',
            'checkAll_1': 'ARO_RESS_Additional_Labour_Container'
        },
        "Fire and Gas Consultancy Service": {
            'checkAll': 'FGC_Engineering_Labor_Container',
            'checkAll_1': 'FGC_Additional_Labour_Container'
        },
        "Public Address General Alarm System": {
            'checkAll': 'PAGA_Labor_Container',
            'checkAll_1': 'PAGA_Additional_Labour_Container'
        },
        "One Wireless System": {
            'checkAll': 'OWS_Engineering_Labor_Container',
            'checkAll_1': 'OWS_Additional_Labour_Container'
        },
        "Tank Gauging Engineering": {
            'checkAll': 'TGE_Engineering_Labor_Container',
            'checkAll_1': 'TGE_Additional_Labour_Container'
        },
        "MS Analyser System Engineering": {
            'checkAll': 'MS_ASE_Engineering_Labor_Container',
            'checkAll_1': 'MS_ASE_Additional_Labour_Container'
        },
        "Process Safety Workbench Engineering": {
            'checkAll': 'PSW_Labor_Container',
            'checkAll_1': 'PSW_Additional_Labor_Container'
        },
        "Metering Skid Engineering": {
            'checkAll': 'MSE_Engineering_Labor_Container',
            'checkAll_1': 'MSE_Additional_Labor_Container'
        },
        "Fire Detection & Alarm Engineering": {
            'checkAll': 'FDA_Engineering_Labor_Container',
            'checkAll_1': 'FDA_Additional_Labor_Container'
        },
        "PRMS Skid Engineering": {
            'checkAll': 'PRMS_Engineering_Labor_Container',
            'checkAll_1': 'PRMS_Additional_Labor_Container'
        },
        "Gas MeterSuite Engineering - C300 Functions": {
            'checkAll': 'Gas_MeterSuite_Engineering_Labor_Container',
            'checkAll_1': 'Gas_MeterSuite_Additional_Labor_Container'
        },
        "Liquid MeterSuite Engineering - C300 Functions": {
            'checkAll': 'LMS_Labor_Container',
            'checkAll_1': 'LMS_Additional_Labor_Container'
        },
        "MeterSuite Engineering - MSC Functions": {
            'checkAll': 'MSC_Engineering_Labor_Container',
            'checkAll_1': 'MSC_Additional_Labour_Container'
        },
        "Industrial Security (Access Control)": {
            'checkAll': 'IS_Labor_Container',
            'checkAll_1': 'IS_Additional_Labor_Container'
        },
        "Simulation System": {
            'checkAll_1': 'Simulation_Labor_Additional_Cust_Deliverables_con'
        },
        "Electrical Substation Data Collector": {
            'checkAll_1': 'ESDC_Labor_Additional_Cust_Deliverables_con'
        },
        "Third Party": {
            'checkAll_1': 'HWOS_Model Scope_3party',
            'checkAll_2': 'HWOS_Invalid_Model Scope_3party'
        },
        "Hardware Refresh": {
            'checkAll': {
                'New': 'HWOS_Model Scope_3party'
            },
            'checkAll_1': {
                'Renewal': 'SC_ValidModels_HR_RWL'
            },
            'checkAll_2': {
                'Renewal': 'SC_InvalidModels_HR_RWL'
            }
        },
        "Hardware Warranty": {
            'checkAll': {
                'New': 'HWOS_Model Scope_3party'
            },
            'checkAll_1': {
                'Renewal': 'SC_ValidModels_HR_RWL'
            },
            'checkAll_2': {
                'Renewal': 'SC_InvalidModels_HR_RWL'
            }
        },
        "Enabled Services": {
            'checkAll_1': ['SC_Select_MSID_Cont', 'SC_Select_MSID_Cont_Hidden'],
            'checkAll_2':'SC_SESP_MultiSites'
        },
        "Training": {
            'checkAll_1': 'HWOS_Model Scope_3party_Training',
            'checkAll_2':'HWOS_Invalid_Model Scope_3party_Training'
        },
        "Cyber": [ 'AR_SMX_Activities', 'AR_Assessment_Activities', 'AR_MSS_Activities', 'AR_CAC_Activities', 'AR_PCNH_Activities','Generic_System_Activities'],
        "Cyber": {
            'checkAll': 'AR_SMX_Activities',
            'checkAll_1': 'AR_Assessment_Activities',
            'checkAll_2': 'AR_CAC_Activities',
            'checkAll_3': 'AR_MSS_Activities',
            'checkAll_4': 'AR_PCNH_Activities',
            'checkAll_5': 'Cyber_Labor_Project_Management',
            'checkAll_6': 'Generic_System_Activities'
        },
        "Winest Labor Import": {
            "checkAll": 'Winest Labor Container',
            "checkAll_1": 'Winest Additional Labor Container'
        }
        # Add other product mappings here...
    }
    getCyberPartSummaryContainer = { 'SMX':'AR_Cyber_PartsSummary',
                        'MSS':'AR_MSS_PartsSummary',
                        'PCN Hardening':'AR_PCNH_PartsSummary',
                        'Assessments':'AR_Assessments_PartsSummary',
                        'Cyber App Control':'AR_CAC_PartsSummary',
						'Cyber Generic System':'Generic_System_PartsSummary'
                        }
    getCyberLaborAttr = {  'SMX':{'container':'AR_SMX_Activities','country':'SMX_Execution_Country','year':'SMX_Execution_Year','salesOrg':'Sales_Org_SMX','productivity':'SMX_PRODUCTIVITY'},
                        'MSS':{'container':'AR_MSS_Activities','country':'MSS_Execution_Country','year':'MSS_Execution_Year','salesOrg':'Sales_Org_MSS','productivity':'MSS_PRODUCTIVITY'},
                        'PCN Hardening':{'container':'AR_PCNH_Activities','country':'PCNH_Execution_Country','year':'PCNH_Execution_Year','salesOrg':'Sales_Org_PCN','productivity':'PCN_PRODUCTIVITY'},
                        'Assessments':{'container':'AR_Assessment_Activities','country':'Assessments_Execution_Country','year':'Assessments_Execution_Year','salesOrg':'Sales_Org_Assessments','productivity':'ASSESSMENT_PRODUCTIVITY'},
                        'Cyber App Control':{'container':'AR_CAC_Activities','country':'CAC_Execution_Country','year':'CAC_Execution_Year','salesOrg':'Sales_Org_CAC','productivity':'CAC_PRODUCTIVITY'},
                        'Cyber Generic System':{'container':'Generic_System_Activities','country':'GENERIC_SYSTEM_Execution_Country','year':'GENERIC_SYSTEM_Execution_Year','salesOrg':'Sales_Org_Generic','productivity':'GENERIC_SYSTEM_PRODUCTIVITY'}

                        }
    cyberActivities = {'AR_SMX_Activities':'SMX','AR_CAC_Activities':'Cyber App Control','AR_MSS_Activities':'MSS','AR_Assessment_Activities':'Assessments','AR_PCNH_Activities':'PCN','Generic_System_Activities':'Cyber Generic System'}
    
    RQUP_Dict={'Modules':'','PreRealseParts':''}
    
    product_name    = ['PMD System','Field Device Manager','ControlEdge RTU System','ControlEdge PLC System','Experion HS System','Virtualization System','3rd Party Devices/Systems Interface (SCADA)','eServer System','ARO, RESS & ERG System','Digital Video Manager','Electrical Substation Data Collector','Simulation System','MXProLine System','QCS-SE System','ControlEdge UOC System','ControlEdge CN900 System','Experion Enterprise System','New / Expansion Project','Generic System','C300 System','Experion MX System','ControlEdge PCD System','Experion HS System','PlantCruise System','HC900 System',"Variable Frequency Drive System","Measurement IQ System","Safety Manager ESD","Safety Manager FGS","Safety Manager BMS","Safety Manager HIPPS","Terminal Manager","MasterLogic-50 Generic","MasterLogic-200 Generic","Experion LX Generic","One Wireless System","Fire and Gas Consultancy Service","Tank Gauging Engineering","Public Address General Alarm System","PRMS Skid Engineering","Metering Skid Engineering","Process Safety Workbench Engineering", "Fire Detection & Alarm Engineering","MS Analyser System Engineering","Gas MeterSuite Engineering - C300 Functions","Liquid MeterSuite Engineering - C300 Functions","Industrial Security (Access Control)","MeterSuite Engineering - MSC Functions","Winest Labor Import"]
    
    conNames = {
            "PMD System":["PMD Engineering Labor Container","PMD Labor Additional Custom Deliverable"],
            "Field Device Manager":["FDM Engineering Labor Container","FDM Additional Custom Deliverables"],
            "ControlEdge RTU System":["CE RTU Engineering Labor Container","CE RTU Additional Custom Deliverables"],
            "ControlEdge PLC System":["CE PLC Engineering Labor Container","CE PLC Additional Custom Deliverables"],
            "ControlEdge UOC System":["CE UOC Engineering Labor Container","CE UOC Additional Custom Deliverables"],
            "ControlEdge CN900 System":["CE CN900 Engineering Labor Container","CE CN900 Additional Custom Deliverables"],
            "Experion HS System":["Experion HS Engineering Labor Container","Experion HS Additional Custom Deliverables"],
            "Virtualization System":["Virtualization_Labor_Deliverable","Virtualization_Additional_Custom_Deliverables"],
            "3rd Party Devices/Systems Interface (SCADA)":["SCADA_Engineering_Labor_Container","SCADA_Additional_Custom_Deliverables_Container"],
            "eServer System":["eServer_Labor_Container","eServer_Labor_Additional_Cust_Deliverables_con"],
            "ARO, RESS & ERG System":["ARO_RESS_Engineering_Labor_Container","ARO_RESS_Additional_Labour_Container"],
            "Digital Video Manager":["DVM_Engineering_Labor_Container","DVM_Additional_Labour_Container"],
            "Electrical Substation Data Collector":["ESDC_Labor_Additional_Cust_Deliverables_con"],
            "Simulation System":["Simulation_Labor_Additional_Cust_Deliverables_con"],
            "MXProLine System":["MXPro_Labor_Container","MXPro_Labor_Additional_Cust_Deliverables_con"],"QCS-SE System":["QCS_SE_Labor_Container","MXPro_Labor_Additional_Cust_Deliverables_con"],
            "Experion Enterprise System":["Hardware Engineering Labour Container","System_Network_Engineering_Labor_Container","System_Interface_Engineering_Labor_Container","HMI_Engineering_Labor_Container","EBR_Engineering_Labor_Container","Additional_CustomDev_Labour_Container"],
            "C300 System":["C300_Engineering_Labor_Container","C300_Additional_Custom_Deliverables_Container"],
            "Experion MX System":["Experion_mx_Labor_Container","Experion_mx_labor_Additional_Cust_Deliverables_con"],
            "ControlEdge PCD System":["PCD Engineering Labor Container","PCD Additional Custom Deliverables"],
            "Experion HS System":["Experion HS Engineering Labor Container","Experion HS Additional Custom Deliverables"],
            "PlantCruise System":["PlantCruise Engineering Labor Container","PlantCruise Additional Custom Deliverables"],
            "HC900 System":["HC900 Engineering Labor Container","HC900 Additional Custom Deliverables"],
            "Variable Frequency Drive System":["VFD Engineering Labor Container","VFD Additional Custom Deliverables"],
            "Measurement IQ System":["MIQ Engineering Labor Container","MIQ Additional Custom Deliverables"],
            "Safety Manager ESD":["SM_SSE_Engineering_Labor_Container","SM_Additional_Custom_Deliverables_Labor_Container","SM Safety System - ESD/FGS/BMS/HIPPS Container"],
            "Safety Manager FGS":["SM_SSE_Engineering_Labor_Container","SM_Additional_Custom_Deliverables_Labor_Container","SM Safety System - ESD/FGS/BMS/HIPPS Container"],
            "Safety Manager BMS":["SM_SSE_Engineering_Labor_Container","SM_Additional_Custom_Deliverables_Labor_Container","SM Safety System - ESD/FGS/BMS/HIPPS Container"],
            "Safety Manager HIPPS":["SM_SSE_Engineering_Labor_Container","SM_Additional_Custom_Deliverables_Labor_Container","SM Safety System - ESD/FGS/BMS/HIPPS Container"],
            "Terminal Manager":["Terminal Engineering Labor Container","Terminal Additional Custom Deliverables"],
            "MasterLogic-50 Generic":["Generic Engineering Labor Container","Generic Additional Custom Deliverables"],
            "MasterLogic-200 Generic":["Generic Engineering Labor Container","Generic Additional Custom Deliverables"],
            "Experion LX Generic":["Generic Engineering Labor Container","Generic Additional Custom Deliverables"],
            "Public Address General Alarm System":["PAGA_Labor_Container","PAGA_Additional_Labour_Container"],
            "PRMS Skid Engineering":["PRMS_Engineering_Labor_Container","PRMS_Additional_Labor_Container"],
            "One Wireless System":["OWS_Engineering_Labor_Container","OWS_Additional_Labour_Container"],
            "Fire and Gas Consultancy Service":["FGC_Engineering_Labor_Container","FGC_Additional_Labour_Container"],
            "Tank Gauging Engineering":["TGE_Engineering_Labor_Container","TGE_Additional_Labour_Container"],
            "MS Analyser System Engineering":["MS_ASE_Engineering_Labor_Container","MS_ASE_Additional_Labour_Container"],
            "Metering Skid Engineering":["MSE_Engineering_Labor_Container","MSE_Additional_Labor_Container"],
            "Process Safety Workbench Engineering":["PSW_Labor_Container","PSW_Additional_Labor_Container"],
            "Fire Detection & Alarm Engineering":['FDA_Engineering_Labor_Container', 'FDA_Additional_Labor_Container'],
            "Liquid MeterSuite Engineering - C300 Functions":['LMS_Labor_Container','LMS_Additional_Labor_Container'],
            "Gas MeterSuite Engineering - C300 Functions":['Gas_MeterSuite_Engineering_Labor_Container', 'Gas_MeterSuite_Additional_Labor_Container'],
            "MeterSuite Engineering - MSC Functions":['MSC_Engineering_Labor_Container','MSC_Additional_Labour_Container'],
            "Industrial Security (Access Control)":['IS_Labor_Container','IS_Additional_Labor_Container'],
            "New / Expansion Project":["Labor_Container","PLE_Labor_Container","PM_Additional_Custom_Deliverables_Labor_Container","Project_management_Labor_Container"],
            "Generic System":["Generic Engineering Labor Container","Generic Additional Custom Deliverables"],
			"OPM":["MSID_Labor_OPM_Engineering"],
			"LCN One Time Upgrade":["MSID_Labor_LCN_One_Time_Upgrade_Engineering"],
			#"Non-SESP Exp Upgrade":["MSID_Labor_EBR_Con"], -
			"EBR":["MSID_Labor_EBR_Con"],
			"ELCN":["MSID_Labor_ELCN_Con"],
			"Orion Console":["MSID_Labor_Orion_Console_Con"],
			"EHPM/EHPMX/ C300PM":["MSID_Labor_EHPM_C300PM_Con"],
			"Project Management":["MSID_Labor_Project_Management"],
			"TPS to Experion":["MSID_Labor_TPS_TO_EXPERION_Con"],
			"TCMI":["MSID_Labor_TCMI_Con"],
			"LM to ELMM ControlEdge PLC":["MSID_Labor_LM_to_ELMM_Con"],
			#"Spare Parts":["MSID_Spare_Parts_Added_Parts_Common_Container"],
			"EHPM HART IO":["MSID_Labor_EHPM_HART_IO_Con"],
			"CB-EC Upgrade to C300-UHIO":["MSID_Labor_CB-EC_Upgrade_to_C300-UHIO_con"],
			"C200 Migration":["MSID_Labor_C200_Migration_Con"],
			"xPM to C300 Migration":["MSID_Labor_xPM_to_C300_Migration_Con"],
			"FDM Upgrade 1":["MSID_Labor_FDM_Upgrade_Con"],
			"FDM Upgrade 2":["MSID_Labor_FDM_Upgrade_Con"],
			"FDM Upgrade 3":["MSID_Labor_FDM_Upgrade_Con"],
			"FSC to SM":["MSID_Labor_FSC_to_SM_con","MSID_Labor_FSC_to_SM_audit_Con"],
			"XP10 Actuator Upgrade":["MSID_Labor_XP10_Actuator_Upgrade_con"],
			"Graphics Migration":["MSID_Labor_Graphics_Migration_con"],
			"FSC to SM IO Migration":["MSID_Labor_FSCtoSM_IO_con"],
			"CD Actuator I-F Upgrade":["MSID_Labor_CD_Actuator_con"],
			"CWS RAE Upgrade":["MSID_Labor_CWS_RAE_Upgrade_con"],
			"3rd Party PLC to ControlEdge PLC/UOC":["3rd_Party_PLC_UOC_Labor"],
			"Virtualization System Migration":["MSID_Labor_Virtualization_con"],
			"QCS RAE Upgrade":["MSID_Labor_QCS_RAE_Upgrade_con"],
			"TPA/PMD Migration":["MSID_Labor_TPA_con"],
			"ELEPIU ControlEdge RTU Migration Engineering":["MSID_Labor_ELEPIU_con"],
			"Generic System Migration":["MSID_Labor_Generic_System1_Cont", "MSID_Labor_Generic_System2_Cont", "MSID_Labor_Generic_System3_Cont", "MSID_Labor_Generic_System4_Cont", "MSID_Labor_Generic_System5_Cont"],
            "Trace Software":["Trace_Software_Labor_con", "Trace_Additional_Custom_Deliverables", "Trace_Project_Management_Labor_con"],
			"Winest Labor Import":["Winest Labor Container", "Winest Additional Labor Container"]
				}