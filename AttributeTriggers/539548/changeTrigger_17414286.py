# Define helper functions
def getContainer(Name):
	return Product.GetContainerByName(Name)

def getAttrValue(Name):
	return Product.Attr(Name).GetValue()

def handle_graphics_migration(row, selectedprd):
	# Handle "GAP Analysis" deliverable
	if row["Deliverable"] == "GAP Analysis":
		gapanalysis = selectedprd.Attr('Graphics_Migration_For_GAP_Analysis_project_com').GetValue()
		if gapanalysis == 'Limitations to use GES':
			row["FO_Eng_Percentage_Split"] = "70"
			row["GES_Eng_Percentage_Split"] = "30"
		elif gapanalysis == "No limitation to use GES":
			row["FO_Eng_Percentage_Split"] = "30"
			row["GES_Eng_Percentage_Split"] = "70"
	
	# Handle "FAT Support" deliverable
	elif row["Deliverable"] == "FAT Support":
		fatvalue = selectedprd.Attr('Graphics_Migration_FAT_required?').GetValue()
		if fatvalue == 'Yes via VEP/Remote GES':
			row["FO_Eng_Percentage_Split"] = "50"
			row["GES_Eng_Percentage_Split"] = "50"
		else:
			row["FO_Eng_Percentage_Split"] = "100"
			row["GES_Eng_Percentage_Split"] = "0"

def updategeseng(row,container):
	if row["Deliverable_Type"] in ("Offsite", "Off-Site"):
		Trace.Write("Check1" + "," + str(container))
		if container  == 'MSID_Labor_Project_Management' :
			row["GES_Eng"] = "SVC_GES_P215B_{}".format(TagParserProduct.ParseString('<*ValueCode(MSID_GES_Location)*>'))
		elif container in ( "MSID_Labor_CWS_RAE_Upgrade_con","MSID_Labor_QCS_RAE_Upgrade_con"):
			row["GES_Eng"] = "SVC_GES_P350B_CN" if row["Deliverable"] in ('MD CD Configuration', 'In-house Engineering MD-CD') else "SVC_GES_P350B_{}".format(location)
				
		elif container != "MSID_Labor_Graphics_Migration_con" and container != "3rd_Party_PLC_UOC_Labor" and container != "MSID_Labor_Project_Management" :
			row["GES_Eng"] = "SVC_GES_P350B_{}".format(location)
		elif container == "3rd_Party_PLC_UOC_Labor":
			row["GES_Eng"] = "SVC_GES_PLCB_{}".format(location)
		else:
			row["GES_Eng"] = "SVC_GES_P335B_{}".format(location)
	
	if row["Deliverable_Type"] in ("Onsite", "On-Site"):
		if container != "MSID_Labor_Graphics_Migration_con" and container != "3rd_Party_PLC_UOC_Labor":
			row["GES_Eng"] = "SVC_GES_P350F_{}".format(location)
		elif container == "3rd_Party_PLC_UOC_Labor":
			row["GES_Eng"] = "SVC_GES_PLCB_{}".format(location)
		else:
			row["GES_Eng"] = "SVC_GES_P335F_{}".format(location)



# Define a dictionary to map each product to specific containers
product_to_containers = {
	"EBR": "MSID_Labor_EBR_Con",
	"ELCN": "MSID_Labor_ELCN_Con",
	"Orion Console": "MSID_Labor_Orion_Console_Con", 
	"EHPM/EHPMX/ C300PM": "MSID_Labor_EHPM_C300PM_Con", 
	"TPS to Experion": "MSID_Labor_TPS_TO_EXPERION_Con", 
	"TCMI": "MSID_Labor_TCMI_Con", 
	"C200 Migration": "MSID_Labor_C200_Migration_Con",
	"CB-EC Upgrade to C300-UHIO": "MSID_Labor_CB-EC_Upgrade_to_C300-UHIO_con", 
	"FSC to SM": "MSID_Labor_FSC_to_SM_con", 
	"FSC to SM Audit": "MSID_Labor_FSC_to_SM_audit_Con", 
	"xPM to C300 Migration": "MSID_Labor_xPM_to_C300_Migration_Con", 
	"LM to ELMM ControlEdge PLC": "MSID_Labor_LM_to_ELMM_Con",
	"EHPM HART IO": "MSID_Labor_EHPM_HART_IO_Con",
	"XP10 Actuator Upgrade": "MSID_Labor_XP10_Actuator_Upgrade_con", 
	"Graphics Migration": "MSID_Labor_Graphics_Migration_con",
	"CD Actuator I-F Upgrade": "MSID_Labor_CD_Actuator_con",
	"FSC to SM IO Migration": "MSID_Labor_FSCtoSM_IO_con",
	"FSC to SM IO Audit": "MSID_Labor_FSC_to_SM_IO_Audit_Con", 
	"3rd Party PLC to ControlEdge PLC/UOC": "3rd_Party_PLC_UOC_Labor",
	"OPM": "MSID_Labor_OPM_Engineering", 
	"LCN One Time Upgrade": "MSID_Labor_LCN_One_Time_Upgrade_Engineering",
	"CWS RAE Upgrade": "MSID_Labor_CWS_RAE_Upgrade_con", 
	"Virtualization System Migration": "MSID_Labor_Virtualization_con",
	"Generic System 1": "MSID_Labor_Generic_System1_Cont",
	"Generic System 2": "MSID_Labor_Generic_System2_Cont",
	"Generic System 3": "MSID_Labor_Generic_System3_Cont",
	"Generic System 4": "MSID_Labor_Generic_System4_Cont",
	"Generic System 5": "MSID_Labor_Generic_System5_Cont",
	"QCS RAE Upgrade": "MSID_Labor_QCS_RAE_Upgrade_con",
	"TPA/PMD Migration": "MSID_Labor_TPA_con", 
	"ELEPIU ControlEdge RTU Migration Engineering": "MSID_Labor_ELEPIU_con",
	"FDM Upgrade":"MSID_Labor_FDM_Upgrade_Con",
	"Project Management":"MSID_Labor_Project_Management"
}

container_dict = { 
				  'MSID_Labor_OPM_Engineering' : {'OPM Documentation' : [20,80],'Documentation' :[20,80],'Migration DDS':[20,80],'Inhouse Engineering': [0,100]},
				  'MSID_Labor_Orion_Console_Con': {'OPM Documentation' : [20,80],'Documentation' :[20,80],'Migration DDS':[20,80],'Inhouse Engineering': [0,100]},
				  'MSID_Labor_EHPM_C300PM_Con': {'OPM Documentation' : [20,80],'Documentation' :[20,80],'Migration DDS':[20,80],'Inhouse Engineering': [0,100]},
				  'MSID_Labor_TCMI_Con': {'OPM Documentation' : [20,80],'Documentation' :[20,80],'Migration DDS':[20,80],'Inhouse Engineering': [0,100]},
				  'MSID_Labor_EHPM_HART_IO_Con': {'OPM Documentation' : [20,80],'Documentation' :[20,80],'Migration DDS':[20,80],'Inhouse Engineering': [0,100]},
				  'MSID_Labor_TPS_TO_EXPERION_Con': {'Migration Documentation' : [10,90],'FAT Procedure' :[10,90]},
				  'MSID_Labor_xPM_to_C300_Migration_Con': {'Migration DDS' : [10,90],'In-house engineering' :[0,100],'FAT Procedure':[0,100],'Pre FAT':[0,100],'FAT':[50,50]},
				  'MSID_Labor_CD_Actuator_con':{'In-house engineering':[0,100]},
				  'MSID_Labor_Graphics_Migration_con': {'Customer Input Study' : [25,75],'Display Generation' :[25,75],'Shapes':[20,80],'Safeview Configuration':[30,70],'Testing System Setup':[30,70],'Query Generation & Clarification': [0,100],'Migration FDS':[70,30],'FAT & SAT Documentation':[40,60],'Migration DDS':[30,70],'Faceplates':[16.67,83.33]},
				  'MSID_Labor_CWS_RAE_Upgrade_con': {'MD CD Configuration' : [0,100],'Server/Station Build' :[0,100]},
				  'MSID_Labor_QCS_RAE_Upgrade_con': {'In-house Engineering MD-CD' : [0,100],'Server/Station Build' :[0,100],'In-house Engineering' :[0,100],'System Specials':[0,100]},
				  '3rd_Party_PLC_UOC_Labor': {'Migration DDS' : [50,50],'Inhouse Engineering' :[10,90],'FAT Procedure' :[0,100],'Pre-FAT':[50,50],'FAT':[60,40]},
				  'MSID_Labor_Virtualization_con':{'Documentation' : [30,70]},
				  'MSID_Labor_TPA_con':{'HMI Engineering':[20,80],'Factory Acceptance Test':[30,70]}
				 }

# Get the selected products from a specific container
def getSelectedProducts():
	selected_products = []
	selectedprd =''
	selected_container = getContainer('CONT_MSID_SUBPRD')
	for row in selected_container.Rows:
		if row.Product.Name == 'Graphics Migration':
			selectedprd = row.Product
		if row["Selected_Products"] in product_to_containers and row["Selected_Products"] != 'Generic System Migration' and row["Selected_Products"] not in ('FDM Upgrade') :
			selected_products.append(row["Selected_Products"])
		elif row["Selected_Products"]  == 'Generic System Migration':
			selected_products.append(row["Product Name"])
		elif row["Selected_Products"]  in  ('FDM Upgrade 1', 'FDM Upgrade 2', 'FDM Upgrade 3'):
			selected_products.append('FDM Upgrade')
	return selected_products,selectedprd

# Function to update specific containers based on the selected products
def updateContainersByProductSelection(selected_products, location, check_value,selectedprd):
	for product in selected_products:
		container = product_to_containers.get(product, [])
		containername = getContainer(container)
		if containername:
			for row in containername.Rows:
				if check_value == "None" and location == '':
					if row["Deliverable"] not in ('Total', 'Off-Site', 'On-Site'):
						row["GES_Eng_Percentage_Split"] = "0"
						row["FO_Eng_Percentage_Split"] = "100"

				if location != '':
					updategeseng(row,container)

						
					if check_value != "Country":
						
					

						if container_dict.get(container) and container_dict[container].get(row["Deliverable"]):
							row["FO_Eng_Percentage_Split"] =str(container_dict[container][row["Deliverable"]][0])
							row["GES_Eng_Percentage_Split"] = str(container_dict[container][row["Deliverable"]][1])


						if container == 'MSID_Labor_Graphics_Migration_con':
							handle_graphics_migration(row, selectedprd)
							
# Main execution based on location
if getAttrValue("MSID_GES_Location") != 'None':
	location = TagParserProduct.ParseString('<*ValueCode(MSID_GES_Location)*>')
	check_value = Product.Attr('MSID_GES_check').GetValue()
	selected_products,selectedprd = getSelectedProducts()
	updateContainersByProductSelection(selected_products, location, check_value,selectedprd)
	Product.Attr('MSID_GES_check').AssignValue('Country')
else:
	Product.Attr('MSID_GES_check').AssignValue('None')
	check_value = Product.Attr('MSID_GES_check').GetValue()
	selected_products,selectedprd = getSelectedProducts()
	updateContainersByProductSelection(selected_products, '', check_value,selectedprd)

# Execute script after updating containers
ScriptExecutor.Execute('PS_PopulatePartNumberContainer', {"Product": Product})
