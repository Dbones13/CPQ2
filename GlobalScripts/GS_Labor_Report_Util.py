from GS_Winest_Labor_Price_Cost import service_material_map2
Lob_Labor_Map = {'7031-7000':'PAS FO Engineering', '7030-7000':'PAS FO Project Management', '7197-7000':'PAS GES Eng & PM',
'7072-7263':'LSS FO Engineering','7680-7B34':'LSS FO Engineering','7070-7253':'LSS FO Engineering','7678-7B32':'LSS FO Engineering',
'7679-7B33':'LSS FO Engineering','7071-7258':'LSS FO Engineering', '7068-7243':'LSS FO Project Management',
'7757-7000':'LSS GES Eng & PM', '7126-7000':'HCI FO Engineering', '7125-7000':'HCI FO Project Management', '7758-7000':'HCI GES Eng & PM',
'7708-7000':'PMC FO Engineering', '7711-7000':'PMC FO Engineering', 'H60D-H60O':'PMC FO Engineering', '7709-7000':'PMC FO Project Management', '7712-7000':'PMC FO Project Management',
'7710-7000':'PMC GES Eng & PM','7713-7000':'PMC GES Eng & PM',
'G451-Y857':'CYB FO Eng & PM','G451-Y858':'CYB FO Eng & PM','G451-Y859':'CYB FO Eng & PM','G451-Y859':'CYB FO Eng & PM','7681-7B35':'CYB FO Eng & PM','7073-7272':'CYB FO Eng & PM','7073-7732':'CYB FO Eng & PM','7681-7B36':'CYB FO Eng & PM','7681-7B37':'CYB FO Eng & PM','7073-7733':'CYB FO Eng & PM', '7150-7000':'HCI FO Engineering','7069-7252':'LSS FO Engineering','7228-7000':'HCI FO Engineering','7157-7000':'HCI FO Engineering','7156-7000':'HCI FO Engineering','7151-7000':'HCI FO Engineering','7152-7000':'HCI FO Engineering','7124-7000':'HCI FO Engineering','7226-7000':'HCI FO Engineering','7153-7000':'HCI FO Engineering','7162-7000':'HCI FO Engineering','7158-7000':'HCI FO Engineering','7154-7000':'HCI FO Engineering','7160-7000':'HCI FO Engineering','7225-7000':'HCI FO Engineering','7161-7000':'HCI FO Engineering','7155-7000':'HCI FO Engineering','7229-7000':'HCI FO Engineering','7159-7000':'HCI FO Engineering'}

Master_Prod_Cont_map = {'New / Expansion Project' : ['Project_management_Labor_Container', 'Labor_Container', 'PLE_Labor_Container', 'PM_Additional_Custom_Deliverables_Labor_Container'],
'Experion Enterprise System' : ['Hardware Engineering Labour Container', 'System_Network_Engineering_Labor_Container', 'System_Interface_Engineering_Labor_Container', 'HMI_Engineering_Labor_Container', 'EBR_Engineering_Labor_Container', 'Additional_CustomDev_Labour_Container'],
'C300 System':['C300_Engineering_Labor_Container', 'C300_Additional_Custom_Deliverables_Container'],'PlantCruise System':['PlantCruise Engineering Labor Container', 'PlantCruise Additional Custom Deliverables'],'HC900 System':['HC900 Engineering Labor Container', 'HC900 Additional Custom Deliverables'],'ControlEdge PCD System':['PCD Engineering Labor Container', 'PCD Additional Custom Deliverables'],'Experion HS System':['Experion HS Engineering Labor Container', 'Experion HS Additional Custom Deliverables'],'Terminal Manager':['Terminal Engineering Labor Container', 'Terminal Additional Custom Deliverables'],'Generic System':['Generic Engineering Labor Container', 'Generic Additional Custom Deliverables'],'Experion LX Generic':['Generic Engineering Labor Container', 'Generic Additional Custom Deliverables'],'MasterLogic-50 Generic':['Generic Engineering Labor Container', 'Generic Additional Custom Deliverables'],'MasterLogic-200 Generic':['Generic Engineering Labor Container', 'Generic Additional Custom Deliverables'],'Variable Frequency Drive System':['VFD Engineering Labor Container', 'VFD Additional Custom Deliverables'],'Measurement IQ System':['MIQ Engineering Labor Container', 'MIQ Additional Custom Deliverables'],
'Safety Manager ESD':['SM_SSE_Engineering_Labor_Container','SM Safety System - ESD/FGS/BMS/HIPPS Container','SM_Additional_Custom_Deliverables_Labor_Container'],
'Safety Manager FGS':['SM_SSE_Engineering_Labor_Container','SM Safety System - ESD/FGS/BMS/HIPPS Container','SM_Additional_Custom_Deliverables_Labor_Container'],
'Safety Manager BMS':['SM_SSE_Engineering_Labor_Container','SM Safety System - ESD/FGS/BMS/HIPPS Container','SM_Additional_Custom_Deliverables_Labor_Container'],
'Safety Manager HIPPS':['SM_SSE_Engineering_Labor_Container','SM Safety System - ESD/FGS/BMS/HIPPS Container','SM_Additional_Custom_Deliverables_Labor_Container'],
'ControlEdge PLC System':['CE PLC Engineering Labor Container', 'CE PLC Additional Custom Deliverables'],
'ControlEdge UOC System':['CE UOC Engineering Labor Container', 'CE UOC Additional Custom Deliverables'],
'ControlEdge CN900 System':['CE CN900 Engineering Labor Container', 'CE CN900 Additional Custom Deliverables'],
'ControlEdge RTU System':['CE RTU Engineering Labor Container', 'CE RTU Additional Custom Deliverables'],
'Digital Video Manager':['DVM_Engineering_Labor_Container', 'DVM_Additional_Labour_Container'],
'ARO, RESS & ERG System':['ARO_RESS_Engineering_Labor_Container', 'ARO_RESS_Additional_Labour_Container'],
'3rd Party Devices/Systems Interface (SCADA)':['SCADA_Engineering_Labor_Container','SCADA_Additional_Custom_Deliverables_Container'],
'Experion MX System':['Experion_mx_Labor_Container','Experion_mx_labor_Additional_Cust_Deliverables_con'],
'MXProLine System':['MXPro_Labor_Container','MXPro_Labor_Additional_Cust_Deliverables_con'],
'eServer System':['eServer_Labor_Container','eServer_Labor_Additional_Cust_Deliverables_con'],
'Electrical Substation Data Collector':['ESDC_Labor_Additional_Cust_Deliverables_con'],
'Simulation System':['Simulation_Labor_Additional_Cust_Deliverables_con'],
'Virtualization System':['Virtualization_Labor_Deliverable','Virtualization_Additional_Custom_Deliverables'],'Field Device Manager':['FDM Engineering Labor Container','FDM Additional Custom Deliverables'],'PMD System':['PMD Engineering Labor Container','PMD Labor Additional Custom Deliverable'],'Fire and Gas Consultancy Service':['FGC_Engineering_Labor_Container','FGC_Additional_Labour_Container'],'Process Safety Workbench Engineering':['PSW_Labor_Container','PSW_Additional_Labor_Container'],'Fire Detection & Alarm Engineering':['FDA_Engineering_Labor_Container','FDA_Additional_Labor_Container'],'Industrial Security (Access Control)':['IS_Labor_Container','IS_Additional_Labor_Container']}
Master_Cont_col_map = {'Labor_Container' : ['Deliverable', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split','FO Eng 1','FO Eng 1 % Split','FO Eng 2','FO Eng 2 % Split','Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],
'PM_Additional_Custom_Deliverables_Labor_Container' : ['Deliverable Name', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split', 'FO Eng', 'FO Eng % Split', 'FO Eng 2','FO Eng 2 % Split', 'Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],
'PLE_Labor_Container' : ['Deliverable', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split','FO Eng 1','FO Eng 1 % Split','FO Eng 2','FO Eng 2 % Split','Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],
'Project_management_Labor_Container' : ['Deliverable', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split','FO Eng 1','FO Eng 1 % Split','FO Eng 2','FO Eng 2 % Split','Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],
'Hardware Engineering Labour Container' : ['Deliverable', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split','FO Eng 1','FO Eng 1 % Split','FO Eng 2','FO Eng 2 % Split','Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],
'System_Network_Engineering_Labor_Container' : ['Deliverable', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split','FO Eng 1','FO Eng 1 % Split','FO Eng 2','FO Eng 2 % Split','Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],
'System_Interface_Engineering_Labor_Container' : ['Deliverable', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split','FO Eng 1','FO Eng 1 % Split','FO Eng 2','FO Eng 2 % Split','Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],
'HMI_Engineering_Labor_Container' : ['Deliverable', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split','FO Eng 1','FO Eng 1 % Split','FO Eng 2','FO Eng 2 % Split','Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],
'EBR_Engineering_Labor_Container' : ['Deliverable', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split','FO Eng 1','FO Eng 1 % Split','FO Eng 2','FO Eng 2 % Split','Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],
'Additional_CustomDev_Labour_Container' : ['Deliverable Name', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split', 'FO Eng', 'FO Eng % Split', 'FO Eng 2','FO Eng 2 % Split', 'Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],
'C300_Engineering_Labor_Container' : ['Deliverable', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split','FO Eng 1','FO Eng 1 % Split','FO Eng 2','FO Eng 2 % Split','Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],
'C300_Additional_Custom_Deliverables_Container' : ['Deliverable Name', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split', 'FO Eng', 'FO Eng % Split', 'FO Eng 2','FO Eng 2 % Split', 'Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],
'PlantCruise Engineering Labor Container' : ['Deliverable', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split','FO Eng 1','FO Eng 1 % Split','FO Eng 2','FO Eng 2 % Split','Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],
'PlantCruise Additional Custom Deliverables' : ['Deliverable Name', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split', 'FO Eng', 'FO Eng % Split', 'FO Eng 2','FO Eng 2 % Split', 'Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],
'HC900 Engineering Labor Container' : ['Deliverable', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split','FO Eng 1','FO Eng 1 % Split','FO Eng 2','FO Eng 2 % Split','Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],
'HC900 Additional Custom Deliverables' : ['Deliverable Name', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split', 'FO Eng', 'FO Eng % Split', 'FO Eng 2','FO Eng 2 % Split', 'Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],
'PCD Engineering Labor Container' : ['Deliverable', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split','FO Eng 1','FO Eng 1 % Split','FO Eng 2','FO Eng 2 % Split','Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],
'PCD Additional Custom Deliverables' : ['Deliverable Name', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split', 'FO Eng', 'FO Eng % Split', 'FO Eng 2','FO Eng 2 % Split', 'Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],
'Experion HS Engineering Labor Container' : ['Deliverable', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split','FO Eng 1','FO Eng 1 % Split','FO Eng 2','FO Eng 2 % Split','Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],
'Experion HS Additional Custom Deliverables' : ['Deliverable Name', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split', 'FO Eng', 'FO Eng % Split', 'FO Eng 2','FO Eng 2 % Split', 'Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],
'Terminal Engineering Labor Container' : ['Deliverable', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split','FO Eng 1','FO Eng 1 % Split','FO Eng 2','FO Eng 2 % Split','Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],
'Terminal Additional Custom Deliverables' : ['Deliverable Name', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split', 'FO Eng', 'FO Eng % Split', 'FO Eng 2','FO Eng 2 % Split', 'Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],
'Generic Engineering Labor Container' : ['Deliverable', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split','FO Eng 1','FO Eng 1 % Split','FO Eng 2','FO Eng 2 % Split','Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],
'Generic Additional Custom Deliverables' : ['Deliverable Name', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split', 'FO Eng', 'FO Eng % Split', 'FO Eng 2','FO Eng 2 % Split', 'Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],
'VFD Engineering Labor Container' : ['Deliverable', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split','FO Eng 1','FO Eng 1 % Split','FO Eng 2','FO Eng 2 % Split','Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],
'VFD Additional Custom Deliverables' : ['Deliverable Name', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split', 'FO Eng', 'FO Eng % Split', 'FO Eng 2','FO Eng 2 % Split', 'Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],
'MIQ Engineering Labor Container' : ['Deliverable', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split','FO Eng','FO Eng % Split','FO Eng 2','FO Eng 2 % Split','Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],
'MIQ Additional Custom Deliverables' : ['Deliverable Name', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split', 'FO Eng', 'FO Eng % Split', 'FO Eng 2','FO Eng 2 % Split', 'Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],
'SM_SSE_Engineering_Labor_Container' : ['Deliverable', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split','FO Eng 1','FO Eng 1 % Split','FO Eng 2','FO Eng 2 % Split','Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],
'SM_Additional_Custom_Deliverables_Labor_Container' : ['Deliverable Name', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split', 'FO Eng', 'FO Eng % Split', 'FO Eng 2','FO Eng 2 % Split', 'Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],
'SM Safety System - ESD/FGS/BMS/HIPPS Container' : ['Deliverable', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split','FO Eng 1','FO Eng 1 % Split','FO Eng 2','FO Eng 2 % Split','Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],'DVM_Additional_Labour_Container':['Deliverable Name', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split','FO Eng','FO Eng % Split','FO Eng 2','FO Eng 2 % Split','Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],
'DVM_Engineering_Labor_Container':['Deliverable', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split','FO Eng 1','FO Eng 1 % Split','FO Eng 2','FO Eng 2 % Split','Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],
'ARO_RESS_Additional_Labour_Container':['Deliverable Name', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split','FO Eng','FO Eng % Split','FO Eng 2','FO Eng 2 % Split','Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],
'ARO_RESS_Engineering_Labor_Container':['Deliverable', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split','FO Eng 1','FO Eng 1 % Split','FO Eng 2','FO Eng 2 % Split','Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],
'CE PLC Additional Custom Deliverables':['Deliverable Name', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split','FO Eng','FO Eng % Split','FO Eng 2','FO Eng 2 % Split','Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],
'CE PLC Engineering Labor Container':['Deliverable', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split','FO Eng 1','FO Eng 1 % Split','FO Eng 2','FO Eng 2 % Split','Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],
'CE UOC Additional Custom Deliverables':['Deliverable Name', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split','FO Eng','FO Eng % Split','FO Eng 2','FO Eng 2 % Split','Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],
'CE UOC Engineering Labor Container':['Deliverable', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split','FO Eng 1','FO Eng 1 % Split','FO Eng 2','FO Eng 2 % Split','Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],
'CE CN900 Additional Custom Deliverables':['Deliverable Name', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split','FO Eng','FO Eng % Split','FO Eng 2','FO Eng 2 % Split','Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],
'CE CN900 Engineering Labor Container':['Deliverable', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split','FO Eng 1','FO Eng 1 % Split','FO Eng 2','FO Eng 2 % Split','Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],
'CE RTU Additional Custom Deliverables':['Deliverable Name', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split','FO Eng','FO Eng % Split','FO Eng 2','FO Eng 2 % Split','Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],
'CE RTU Engineering Labor Container':['Deliverable', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split','FO Eng 1','FO Eng 1 % Split','FO Eng 2','FO Eng 2 % Split','Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],
'SCADA_Engineering_Labor_Container':['Deliverable', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split','FO Eng 1','FO Eng 1 % Split','FO Eng 2','FO Eng 2 % Split','Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],
'SCADA_Additional_Custom_Deliverables_Container':['Deliverable Name', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split','FO Eng','FO Eng % Split','FO Eng 2','FO Eng 2 % Split','Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],
'Experion_mx_Labor_Container':['Deliverable', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split','FO Eng 1','FO Eng 1 % Split','FO Eng 2','FO Eng 2 % Split','Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],
'Experion_mx_labor_Additional_Cust_Deliverables_con':['Deliverable Name', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split','FO Eng','FO Eng % Split','FO Eng 2','FO Eng 2 % Split','Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],
'MXPro_Labor_Container':['Deliverable', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split','FO Eng 1','FO Eng 1 % Split','FO Eng 2','FO Eng 2 % Split','Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],
'MXPro_Labor_Additional_Cust_Deliverables_con':['Deliverable Name', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split','FO Eng','FO Eng % Split','FO Eng 2','FO Eng 2 % Split','Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],
'eServer_Labor_Container':['Deliverable', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split','FO Eng 1','FO Eng 1 % Split','FO Eng 2','FO Eng 2 % Split','Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],
'eServer_Labor_Additional_Cust_Deliverables_con':['Deliverable Name', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split','FO Eng','FO Eng % Split','FO Eng 2','FO Eng 2 % Split','Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],
'Virtualization_Labor_Deliverable':['Deliverable', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split','FO Eng 1','FO Eng 1 % Split','FO Eng 2','FO Eng 2 % Split','Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],
'Virtualization_Additional_Custom_Deliverables':['Deliverable Name', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split','FO Eng','FO Eng % Split','FO Eng 2','FO Eng 2 % Split','Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],
'ESDC_Labor_Additional_Cust_Deliverables_con':['Deliverable Name', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split','FO Eng','FO Eng % Split','FO Eng 2','FO Eng 2 % Split','Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],
'Simulation_Labor_Additional_Cust_Deliverables_con':['Deliverable Name', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split','FO Eng','FO Eng % Split','FO Eng 2','FO Eng 2 % Split','Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],'FDM Additional Custom Deliverables':['Deliverable Name', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split','FO Eng','FO Eng % Split','FO Eng 2','FO Eng 2 % Split','Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],
'FDM Engineering Labor Container':['Deliverable', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split','FO Eng 1','FO Eng 1 % Split','FO Eng 2','FO Eng 2 % Split','Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],
'PMD Engineering Labor Container':['Deliverable', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split','FO Eng 1','FO Eng 1 % Split','FO Eng 2','FO Eng 2 % Split','Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],
'PMD Labor Additional Custom Deliverable':['Deliverable Name', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split','FO Eng','FO Eng % Split','FO Eng 2','FO Eng 2 % Split','Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],
'FGC_Engineering_Labor_Container':['Deliverable', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split','FO Eng 1','FO Eng 1 % Split','FO Eng 2','FO Eng 2 % Split','Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],
'FGC_Additional_Labour_Container':['Deliverable Name', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split','FO Eng','FO Eng % Split','FO Eng 2','FO Eng 2 % Split','Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],
'PSW_Labor_Container':['Deliverable', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split','FO Eng 1','FO Eng 1 % Split','FO Eng 2','FO Eng 2 % Split','Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],
'PSW_Additional_Labor_Container':['Deliverable Name', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split','FO Eng','FO Eng % Split','FO Eng 2','FO Eng 2 % Split','Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],'FDA_Engineering_Labor_Container':['Deliverable', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split','FO Eng 1','FO Eng 1 % Split','FO Eng 2','FO Eng 2 % Split','Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'], 'FDA_Additional_Labor_Container':['Deliverable Name', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split','FO Eng','FO Eng % Split','FO Eng 2','FO Eng 2 % Split','Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'],'IS_Labor_Container':['Deliverable', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split','FO Eng 1','FO Eng 1 % Split','FO Eng 2','FO Eng 2 % Split','Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice'], 'IS_Additional_Labor_Container':['Deliverable Name', 'Calculated Hrs', 'Productivity', 'Final Hrs', 'GES Eng', 'GES Eng % Split','FO Eng','FO Eng % Split','FO Eng 2','FO Eng 2 % Split','Execution Country', 'Execution Year', 'FO_Regional_Cost', 'GES_Regional_Cost','FO_WTW_Cost','GES_WTW_Cost','FO_ListPrice','GES_ListPrice']
}
Master_Cont_Labor_map = {'Project_management_Labor_Container' : 'Project Management', 'Labor_Container' : 'Project Controls & Administration',
'PLE_Labor_Container' : 'Project Lead Engineering', 'PM_Additional_Custom_Deliverables_Labor_Container' : 'Additional Custom Deliverables',
'Hardware Engineering Labour Container' : 'Hardware Engineering', 'System_Network_Engineering_Labor_Container':'System Network Engineering (Level 1 & 2)',
'System_Interface_Engineering_Labor_Container':'System Interface Engineering', 'HMI_Engineering_Labor_Container':'HMI Engineering',
'EBR_Engineering_Labor_Container':'Experion Backup Restore Engineering', 'Additional_CustomDev_Labour_Container':'Additional Custom Deliverables',
'C300_Engineering_Labor_Container':'C300 Engineering', 'C300_Additional_Custom_Deliverables_Container':'C300 Additional Custom Deliverables','PlantCruise Engineering Labor Container':'PlantCruise Engineering', 'PlantCruise Additional Custom Deliverables':'PlantCruise Additional Custom Deliverables','HC900 Engineering Labor Container':'HC900 Engineering', 'HC900 Additional Custom Deliverables':'HC900 Additional Custom Deliverables','PCD Engineering Labor Container':'PCD Engineering', 'PCD Additional Custom Deliverables':'PCD Additional Custom Deliverables','Experion HS Engineering Labor Container':'Experion HS Engineering', 'Experion HS Additional Custom Deliverables':'Experion HS Additional Custom Deliverables','Terminal Engineering Labor Container':'Terminal Engineering', 'Terminal Additional Custom Deliverables':'Terminal Additional Custom Deliverables','Generic Engineering Labor Container':'Generic Engineering', 'Generic Additional Custom Deliverables':'Generic Additional Custom Deliverables','VFD Engineering Labor Container':'VFD Engineering', 'VFD Additional Custom Deliverables':'VFD Additional Custom Deliverables','MIQ Engineering Labor Container':'MIQ Engineering', 'MIQ Additional Custom Deliverables':'MIQ Additional Custom Deliverables',
'SM_SSE_Engineering_Labor_Container':'Safety System Base', 'SM_Additional_Custom_Deliverables_Labor_Container':'SMSC Additional Custom Deliverables',
'SM Safety System - ESD/FGS/BMS/HIPPS Container':'SM Safety System','DVM_Additional_Labour_Container':'DVM Additional Custom Deliverables','DVM_Engineering_Labor_Container':'DVM Engineering',
'ARO_RESS_Additional_Labour_Container':'ARO RESS Additional Custom Deliverables','ARO_RESS_Engineering_Labor_Container':'ARO RESS Engineering','CE PLC Additional Custom Deliverables':'PLC Additional Custom Deliverables','CE PLC Engineering Labor Container':'PLC Engineering',
'CE UOC Additional Custom Deliverables':'UOC Additional Custom Deliverables','CE UOC Engineering Labor Container':'UOC Engineering','CE CN900 Additional Custom Deliverables':'CN900 Additional Custom Deliverables','CE CN900 Engineering Labor Container':'CN900 Engineering','CE RTU Additional Custom Deliverables':'RTU Additional Custom Deliverables','CE RTU Engineering Labor Container':'RTU Engineering',
'SCADA_Engineering_Labor_Container':'Scada Engineering', 'SCADA_Additional_Custom_Deliverables_Container':'Additional Custom Deliverables',
'Experion_mx_Labor_Container':'Experion MX Engineering', 'Experion_mx_labor_Additional_Cust_Deliverables_con':'Additional Custom Deliverables',
'MXPro_Labor_Container':'MXProLine Engineering', 'MXPro_Labor_Additional_Cust_Deliverables_con':'Additional Custom Deliverables',
'eServer_Labor_Container':'eServer Engineering', 'eServer_Labor_Additional_Cust_Deliverables_con':'Additional Custom Deliverables',
'Virtualization_Labor_Deliverable':'Virtualization Engineering', 'Virtualization_Additional_Custom_Deliverables':'Additional Custom Deliverables',
'ESDC_Labor_Additional_Cust_Deliverables_con':'Additional Custom Deliverables',
'Simulation_Labor_Additional_Cust_Deliverables_con':'Additional Custom Deliverables','FDM Engineering Labor Container':'FDM Engineering Labor Container','FDM Additional Custom Deliverables':'FDM Additional Custom Deliverables',
'PMD Engineering Labor Container':'PMD Engineering', 'PMD Labor Additional Custom Deliverable':'Additional Custom Deliverables','FGC_Engineering_Labor_Container':'FGC Engineering','FGC_Additional_Labour_Container':'Additional Custom Deliverables','PSW_Labor_Container':'PSW Engineering','PSW_Additional_Labor_Container':'Additional Custom Deliverables','FDA_Engineering_Labor_Container':'Fire Detection & Alarm Engineering','FDA_Additional_Labor_Container':'Fire Detection & Alarm Engineering','IS_Labor_Container':'Industrial Security (Access Control)','IS_Additional_Labor_Container':'Industrial Security (Access Control)','Winest Labor Container':'Winest Labor','Winest Additional Labor Container':'Winest Labor','MSID_Labor_OPM_Engineering':'OPM Engineering','MSID_Labor_LCN_One_Time_Upgrade_Engineering':'LCN One Time Upgrade Engineering',
'MSID_Labor_EBR_Con':'EBR Engineering' ,'MSID_Labor_ELCN_Con':'ELCN Engineering','MSID_Labor_Virtualization_con':'Virtualization System Migration Engineering',
'MSID_Labor_Graphics_Migration_con':'Graphics Migration Engineering' ,'MSID_Labor_EHPM_HART_IO_Con':'EHPM HART IO Engineering','MSID_Labor_EHPM_C300PM_Con':'EHPM/EHPMX/ C300PM Engineering',
'MSID_Labor_Orion_Console_Con':'Orion Console Engineering', 'MSID_Labor_TPS_TO_EXPERION_Con':'TPS to Experion Engineering','MSID_Labor_TCMI_Con':'TCMI Engineering',
'MSID_Labor_C200_Migration_Con':'C200 Migration Engineering', 'MSID_Labor_CB-EC_Upgrade_to_C300-UHIO_con':'CB-EC Upgrade to C300-UHIO Engineering',
'MSID_Labor_FSC_to_SM_con':'FSC to SM Engineering','MSID_Labor_FSC_to_SM_audit_Con':'FSC to SM Engineering', 'MSID_Labor_FSCtoSM_IO_con':'FSC to SM Engineering',
'MSID_Labor_FSC_to_SM_IO_Audit_Con':'FSC to SM Engineering','MSID_Labor_xPM_to_C300_Migration_Con':'xPM to C300 Migration Engineering', 'MSID_Labor_FDM_Upgrade_Con':'FDM Upgrade Engineering',
'MSID_Labor_LM_to_ELMM_Con':'LM to ELMM ControlEdge PLC Engineering','MSID_Labor_XP10_Actuator_Upgrade_con':'XP10 Actuator Upgrade Engineering' ,
'3rd_Party_PLC_UOC_Labor':'3rd Party PLC to ControlEdge PLC/UOC Engineering','MSID_Labor_CWS_RAE_Upgrade_con':'CWS RAE Upgrade Engineering',
'MSID_Labor_QCS_RAE_Upgrade_con':'QCS RAE Upgrade Engineering', 'MSID_Labor_CD_Actuator_con':'CD Actuator I-F Upgrade Engineering','MSID_Labor_TPA_con':'TPA/PMD Migration Engineering',
'MSID_Labor_Generic_System1_Cont':'Generic System Migration Engineering', 'MSID_Labor_Generic_System2_Cont':'Generic System Migration Engineering',
'MSID_Labor_Generic_System3_Cont':'Generic System Migration Engineering', 
'MSID_Labor_Generic_System4_Cont':'Generic System Migration Engineering','MSID_Labor_Generic_System5_Cont':'Generic System Migration Engineering', 
'MSID_Labor_ELEPIU_con':'ELEPIU ControlEdge RTU Migration Engineering','MSID_Labor_Project_Management':'Migration Project Management',
'MSID_Additional_Custom_Deliverables':'Migration Additional Custom Deliverables','Generic_System_Activities':'Cyber Generic System Engineering','AR_SMX_Activities':'SMX Engineering',
'AR_Assessment_Activities':'Assessments Engineering','AR_PCNH_Activities':'PCN Hardening Engineering','AR_MSS_Activities':'MSS Engineering','AR_CAC_Activities':'Cyber App Control Engineering',
'Cyber_Labor_Project_Management':'Cyber Project Management','AR_Cyber_AdditionalCustomDeliverable':'Cyber Additional Custom Deliverables','HCI_PHD_EngineeringLabour':' Engineering','HCI_PHD_ProjectManagement2':' Project Lead Engineering','HCI_PHD_ProjectManagement':' Project Management','HCI_PHD_AdditionalDeliverables':'Additional Custom Deliverables','AR_HCI_LABOR_CONTAINER':'Labor Deliverables'}
def to_float(val):
    return float(val) if val not in ('', None) else 0
def safe_get(lst, idx, default=0): 
    return to_float(lst[idx]) if idx < len(lst) else default

def get_LOB_Labor(lob):
    if lob in Lob_Labor_Map:
        return Lob_Labor_Map[lob]
    else:
        return ''

def get_plsg(fo_lbr):
    plsg = ''
    plsg = SqlHelper.GetFirst("select PLSG from HPS_LABOR_PLSG_MAPPING where Part_Name = '{0}'".format(fo_lbr))
    if plsg != None:
        return plsg.PLSG
    else:
        Fo_Part=service_material_map2.get(fo_lbr)
        plsg = SqlHelper.GetFirst("select PLSG from HPS_PRODUCTS_MASTER where PartNumber = '{0}'".format(Fo_Part))
        if plsg != None:
            return plsg.PLSG
        else:
        	return ''
    
def Store_Lbr_Dtls_in_QT(Quote, Cont_Labor_map, labor_deliverables):
    QT_Table = Quote.QuoteTables["Labor_Deliverables"]
    QT_Table.Rows.Clear()
    for x in labor_deliverables:
        newRow = QT_Table.AddNewRow()
        newRow['ProductName'] = x[0]
        newRow['PartNumber'] = x[1]
        newRow['Labor_Container'] = Cont_Labor_map[x[2]]
        Trace.Write("Processing Labor Container: " + Cont_Labor_map[x[2]])
        newRow['Deliverable'] = x[3]
        Trace.Write('deliverable-->' + (newRow['Deliverable']))
        if x[4] == '' or x[4] == None:
            newRow['Calculated_Hrs'] = 0
        else:
            newRow['Calculated_Hrs'] = x[4]   
        newRow['Productivity'] = x[5]
        if x[6] == '':
            newRow['Final_Hrs'] = 0
        else:
            newRow['Final_Hrs'] = x[6]
        newRow['GES_Eng'] = x[7]
        if x[8] == '' or x[8] == None:
            newRow['GES_Eng_Split'] = 0
        else:
            newRow['GES_Eng_Split'] = x[8]
        newRow['FO_Eng_1'] = x[9]
        #Log.Info(x[0] + " " + x[1] + " " + Cont_Labor_map[x[2]] + " " + str(x[10]))
        if x[10] == '' or x[10] == None:
            newRow['FO_Eng_1_Split'] = 0
        else:
            newRow['FO_Eng_1_Split'] = float(x[10])
        newRow['FO_Eng_2'] = x[11]
        if x[12] == '' or x[12] == None:
            newRow['FO_Eng_2_Split'] = 0
        else:
            newRow['FO_Eng_2_Split'] = float(x[12])
        newRow['Execution_Country'] = x[13]
        newRow['Execution_Year'] = x[14]
        newRow['FO_Cost'] = x[15]
        newRow['GES_Cost'] = x[16]
        newRow['PLSG'] = x[17]
        newRow['System_Group_name'] = x[18]
        newRow['FO_Labor'] = x[19]
        newRow['GES_Labor'] = x[20]
        newRow['Sales_org_Country'] = x[21]
        newRow['LOB_Labor'] = x[22]
        newRow['GES_LOB_Labor'] = x[23]
        newRow['GES_PLSG'] = x[24]
        newRow['FO_WTW_Cost'] = safe_get(x,25)
        newRow['GES_WTW_Cost'] = safe_get(x,26)
        newRow['FO_ListPrice'] = safe_get(x,27)
        newRow['GES_ListPrice'] = safe_get(x,28)
    QT_Table.Save()