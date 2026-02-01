import math as m

def getContainer(Product,Name):
	return Product.GetContainerByName(Name)

def getRowData(Product,container,column):
	Container = getContainer(Product,container)
	for row in Container.Rows:
		return row[column]

def getAttrValue(Product,column):
	return Product.Attr(column).GetValue()

def getRowDataIndex(Product,container,column,index):
	Container = getContainer(Product,container)
	for row in Container.Rows:
		if row.RowIndex == index:
			return row[column]

def getFloat(Var):
	if Var:
		return float(Var)
	return 0

def getTotalEngHours(Product,container):
	totalFinalHours = 0
	for row in getContainer(Product,container).Rows:
		if row["Deliverable"] == "Total":
			totalFinalHours += getFloat(row["Final_Hrs"])
	return totalFinalHours

def calculateFinalHours1(row,oldCalHrs):
	if getFloat(oldCalHrs) == getFloat(row["Calculated_Hrs"]):
		return str(round(getFloat(row["Final_Hrs"])))
	else:
		return str(round(getFloat(row["Calculated_Hrs"]) * getFloat(row["Adjustment_Productivity"])))
def reCalAdj(row,oldCalHrs):
	if getFloat(oldCalHrs) != getFloat(row["Calculated_Hrs"]):
		return "1"
	else:
		return row["Adjustment_Productivity"]

def getFSCTOSMLabourHours(Product):
	
	parameters ={"FSC_to_SM_Services":{"var_7":"ATT_FSC_to_SM_In_Office_Eng_hours","var_10_t":"FSC_to_SM_Has_the_System_Audit_been_performed","var_9":"FSC_to_SM_Factory_Acceptance_Test_required","var_6":"FSC_to_SM_ACAD","var_8":"ATT_FSC_to_SM_On_Site_Eng_hours"},"FSC_to_SM_Configuration":{"var_1":"FSC_to_SM_How_many_systems_with_same_configuration_to_be_migrated_in_this_proposal","var_2_YN":"FSC_to_SM_Are_the_FSCs_in_this_configuration_connected_to_a_SafeNet_network","var_2_1":"FSC_to_SM_How_many_FSC_Systems_are_in_the_SafeNet_network","var_2_2":"FSC_to_SM_How_many_FSC_Systems_from_the_SafeNet_network_are_we_migrating_in_the_first_phase"}}
	#var_6 var_9 var_10 is pending
	for key in parameters:
		if key == "FSC_to_SM_Services":
			var_7 = getFloat(getAttrValue(Product,parameters[key]["var_7"]))
			var_6 = getAttrValue(Product,parameters[key]["var_6"])
			var_8 = getFloat(getAttrValue(Product,parameters[key]["var_8"]))
			var_9 = getAttrValue(Product,parameters[key]["var_9"])
			var_10_t = getAttrValue(Product,parameters[key]["var_10_t"])
		if key == "FSC_to_SM_Configuration":
			var_1 = 0
			var_2_1 =0
			var_2_2 = 0 #var_2_1 - var_2_2 for var_2
			for row in getContainer(Product, key).Rows:
				var_1 += getFloat(row[parameters[key]["var_1"]])
				if row[parameters[key]["var_2_YN"]] != "No":
					var_2_1 += getFloat(row[parameters[key]["var_2_1"]])
					var_2_2 += getFloat(row[parameters[key]["var_2_2"]])
			var_2 = var_2_1 - var_2_2
	
	var_10 = "No" if(var_10_t== "Yes") else "Yes"
	documentationRequired = Product.Attr('FSC_to_SM_Which_documentation_is_required').GetValue()
	selectedDocumentation = documentationRequired.split(',')
	selectedDocumentation = [x.strip() for x in selectedDocumentation]
	Var_3 = "Software Detailed Design Specification (SDDS)"
	Var_4 = "Functional Design Specification (FDS)"
	Var_5 = "Factory Acceptance Test document (FAT)"

	documentationHours = 0
	if Var_3 in selectedDocumentation:
		documentationHours = documentationHours + 12.00
	if Var_4 in selectedDocumentation:
		documentationHours = documentationHours + 12.00
	if Var_5 in selectedDocumentation:
		documentationHours = documentationHours + 12.00

	documentation = m.ceil(((documentationHours+16.00) * var_1)/8.00)*8.00
	detailHWEngHrs = m.ceil((var_1*18.00+var_7)/8.00)*8.00
	project_drawing_update = (var_1*32.00) if(var_6 == "Yes") else 0
	Application_migration_Eng = var_1 * 16.00
	Fat = var_1*8.00 if(var_9 != "No") else 0
	OnSiteHours = m.ceil((8.00+ (var_1 *8.00) + (var_2*4.00)+ var_8)/8.00)*8.00
	Sat = var_1 * 8.00
	PreMigrationAudit = (var_1 * 8.00) if(var_10 == "Yes") else 0
	OnSiteMigrationAudit = (m.ceil((var_1 * 5.00)/8.00)*8.00) if(var_10 == "Yes") else 0
	CreateMigrationAudit = (m.ceil((var_1 * 15.00)/8.00)*8.00) if(var_10 == "Yes") else 0

	return documentation, detailHWEngHrs, project_drawing_update, Application_migration_Eng, Fat, OnSiteHours, Sat, PreMigrationAudit, OnSiteMigrationAudit, CreateMigrationAudit


def getFDMLabourHours(msidcont,selectedProducts):
	fdmProd1 = None
	fdmProd2 = None
	fdmProd3 = None
	for row in msidcont.Rows:
		if row.Product.Name == 'FDM Upgrade 1':
			fdmProd1 = row.Product
		elif row.Product.Name == 'FDM Upgrade 2':
			fdmProd2 = row.Product
		elif row.Product.Name == 'FDM Upgrade 3':
			fdmProd3 = row.Product
	parameters ={"FDM_Upgrade_General_questions":{"var_UP_ADD_CONF_YN":"FDM_Upgrade_Additional_Components"}, "FDM_Upgrade_Configuration":{"var_2_YN":"FDM_Upgrade_Do_you_want_to_upgrade_this_FDM","var_3_1":"Attr_FDM_Upg1_TotalFDMClients","var_4_1":"Attr_FDMUpg1_RCIs_incExperion"}, "FDM_Upgrade_Services":{"var_5":"Attr_Experion/TPSSer","var_6":"Attr_NetworkInterf_Lic","var_7":"Attr_ExpStationsFDM","var_8":"Attr_FDMGateways","var_11":"FDM_Upgrade_Site_Acceptance_Test"}, "FDM_Upgrade_Additional_Configuration":{"var_12":"Attr_PVST_HARTESD","var_3_2":"Attr_FDMUpg_FDMClients","var_4_2":"Attr_remPCs_FDMServerviaLAN","var_14_YN":"FDM_Upgrade_Are_additional_components_required"}}
	parameters_2 ={"FDM_Upgrade_2_General_questions":{"var_UP_ADD_CONF_YN_2":"FDM_Upgrade_Additional_Components"}, "FDM_Upgrade_2_Configuration":{"var_2_YN_2":"FDM_Upgrade_Do_you_want_to_upgrade_this_FDM","var_3_1_2":"Attr_FDM_Upg1_TotalFDMClients","var_4_1_2":"Attr_FDMUpg1_RCIs_incExperion"}, "FDM_Upgrade_2_Services":{"var_5_2":"Attr_Experion/TPSSer","var_6_2":"Attr_NetworkInterf_Lic","var_7_2":"Attr_ExpStationsFDM","var_8_2":"Attr_FDMGateways","var_11_2":"FDM_Upgrade_Site_Acceptance_Test"}, "FDM_Upgrade_2_Additional_Configuration":{"var_12_2":"Attr_PVST_HARTESD","var_3_2_2":"Attr_FDMUpg_FDMClients","var_4_2_2":"Attr_remPCs_FDMServerviaLAN","var_14_YN_2":"FDM_Upgrade_Are_additional_components_required"}}
	parameters_3 ={"FDM_Upgrade_3_General_questions":{"var_UP_ADD_CONF_YN_3":"FDM_Upgrade_Additional_Components"}, "FDM_Upgrade_3_Configuration":{"var_2_YN_3":"FDM_Upgrade_Do_you_want_to_upgrade_this_FDM","var_3_1_3":"Attr_FDM_Upg1_TotalFDMClients","var_4_1_3":"Attr_FDMUpg1_RCIs_incExperion"}, "FDM_Upgrade_3_Services":{"var_5_3":"Attr_Experion/TPSSer","var_6_3":"Attr_NetworkInterf_Lic","var_7_3":"Attr_ExpStationsFDM","var_8_3":"Attr_FDMGateways","var_11_3":"FDM_Upgrade_Site_Acceptance_Test"}, "FDM_Upgrade_3_Additional_Configuration":{"var_12_3":"Attr_PVST_HARTESD","var_3_2_3":"Attr_FDMUpg_FDMClients","var_4_2_3":"Attr_remPCs_FDMServerviaLAN","var_14_YN_3":"FDM_Upgrade_Are_additional_components_required"}}
	var_2 = 0
	var_14_1 = 0
	var_8 = 0
	var_5 = 0
	var_6 = 0
	var_7 = 0
	#var_10 = 0
	var_11 = 0
	var_12 = 0
	#var_13 = 0
	var_14_2 = 0
	var_14_3 = 0
	if fdmProd1:
		var_UP_ADD_CONF_YN = getAttrValue(fdmProd1,"FDM_Upgrade_Additional_Components")
	else:
		var_UP_ADD_CONF_YN = ''
	var_2_2 = 0
	var_2_3 = 0
	var_14 = 0
	var_3_1 = 0
	var_4_1 = 0
	var_3_2 =0
	var_4_2 =0
	var_12_1 = 0
	var_5_1 = 0
	var_6_1 = 0
	var_7_1 = 0
	var_11_1 = ''
	var_8_1 = 0
	if fdmProd2:
		var_UP_ADD_CONF_YN_2 = getAttrValue(fdmProd2,"FDM_Upgrade_Additional_Components")
	else:
		var_UP_ADD_CONF_YN_2 = ''
	if fdmProd3:
		var_UP_ADD_CONF_YN_3 = getAttrValue(fdmProd3,"FDM_Upgrade_Additional_Components")
	else:
		var_UP_ADD_CONF_YN_3 = ''
	if 'FDM Upgrade 1' in selectedProducts:
		Product = fdmProd1
		for key in parameters:
			if key == "FDM_Upgrade_Configuration":
				varnew1 = getAttrValue(Product,parameters[key]["var_2_YN"])
				varnew2 = getAttrValue(Product,parameters[key]["var_3_1"])
				varnew3 = getAttrValue(Product,parameters[key]["var_4_1"])
				if varnew1 == "Yes":
					Trace.Write("var_2 insideloop"+str(var_2))
					var_2 =var_2 + 1
					var_3_1 += getFloat(varnew2)
					var_4_1 += getFloat(varnew3)
			if key == "FDM_Upgrade_Additional_Configuration":
				if var_UP_ADD_CONF_YN != "No":
					varnew4 = getAttrValue(Product,parameters[key]["var_14_YN"])
					if varnew4 == "Yes":
						var_14_1 = var_14 +1
						var_3_2 += getFloat(getAttrValue(Product,parameters[key]["var_3_2"]))
						var_4_2 += getFloat(getAttrValue(Product,parameters[key]["var_4_2"]))
						var_12_1 += getFloat(getAttrValue(Product,parameters[key]["var_12"]))
			if key == "FDM_Upgrade_Services":
				var_5_1 = getFloat(getAttrValue(Product,parameters[key]["var_5"]))
				var_6_1 = getFloat(getAttrValue(Product,parameters[key]["var_6"]))
				var_7_1 = getFloat(getAttrValue(Product,parameters[key]["var_7"]))
				var_8_1 = getFloat(getAttrValue(Product,parameters[key]["var_8"]))
				var_11_1 = getAttrValue(Product,parameters[key]["var_11"])
	var_3_1_2 = 0
	var_3_2_2 = 0
	var_4_1_2 = 0
	var_4_2_2 = 0
	var_5_1_2 = 0
	var_6_2 = 0
	var_7_2 = 0
	var_8_2 = 0
	var_5_1_2 = 0
	var_11_2 = ''
	var_2_2 = 0
	var_14_2 = 0
	var_12_2 = 0
	if 'FDM Upgrade 2' in selectedProducts:
		Product = fdmProd2
		Trace.Write("fdmupgrade2")
		for key in parameters_2:
			if key == "FDM_Upgrade_2_Configuration":
				varnew5 = getAttrValue(Product,parameters_2[key]["var_2_YN_2"])
				if varnew5 == "Yes":
					Trace.Write("var_2_2 insideloop"+str(var_2_2))
					var_2_2 =var_2_2 + 1
					var_3_1_2 += getFloat(getAttrValue(Product,parameters_2[key]["var_3_1_2"]))
					var_4_1_2 += getFloat(getAttrValue(Product,parameters_2[key]["var_4_1_2"]))
					Trace.Write("test4::"+str(var_4_1_2))
			if key == "FDM_Upgrade_2_Additional_Configuration":
				if var_UP_ADD_CONF_YN_2 != "No":
					varnew6 = getAttrValue(Product,parameters_2[key]["var_14_YN_2"])
					if varnew6 == "Yes":
						var_14_2 =var_14_2 +1
						var_3_2_2 += getFloat(getAttrValue(Product,parameters_2[key]["var_3_2_2"]))
						var_4_2_2 += getFloat(getAttrValue(Product,parameters_2[key]["var_4_2_2"]))
						var_12_2 += getFloat(getAttrValue(Product,parameters_2[key]["var_12_2"]))
			if key == "FDM_Upgrade_2_Services":
				var_5_1_2 = getFloat(getAttrValue(Product,parameters_2[key]["var_5_2"]))
				var_6_2 = getFloat(getAttrValue(Product,parameters_2[key]["var_6_2"]))
				var_7_2 = getFloat(getAttrValue(Product,parameters_2[key]["var_7_2"]))
				var_8_2 = getFloat(getAttrValue(Product,parameters_2[key]["var_8_2"]))
				var_11_2 = getAttrValue(Product,parameters_2[key]["var_11_2"])
	var_3_1_3 = 0
	var_3_2_3 = 0
	var_4_1_3 = 0
	var_4_2_3 = 0
	var_5_1_3 = 0
	var_6_3 = 0
	var_7_3 = 0
	var_8_3 = 0
	var_11_3 = ''
	var_12_3 = 0
	var_14_3 = 0 
	var_2_3 = 0
	if 'FDM Upgrade 3' in selectedProducts:
		Product = fdmProd3
		for key in parameters_3:
			if key == "FDM_Upgrade_3_Configuration":
				varnew7 = getAttrValue(Product,parameters_3[key]["var_2_YN_3"])
				if varnew7 == "Yes":
					var_2_3 =var_2_3 + 1
					var_3_1_3 += getFloat(getAttrValue(Product,parameters_3[key]["var_3_1_3"]))
					var_4_1_3 += getFloat(getAttrValue(Product,parameters_3[key]["var_4_1_3"]))
			if key == "FDM_Upgrade_3_Additional_Configuration":
				if var_UP_ADD_CONF_YN_3 != "No":
					varnew8 = getAttrValue(Product,parameters_3[key]["var_14_YN_3"])
					if varnew8 == "Yes":
						var_14_3 =var_14_3 +1
						var_3_2_3 += getFloat(getAttrValue(Product,parameters_3[key]["var_3_2_3"]))
						var_4_2_3 += getFloat(getAttrValue(Product,parameters_3[key]["var_4_2_3"]))
						var_12_3 += getFloat(getAttrValue(Product,parameters_3[key]["var_12_3"]))
			if key == "FDM_Upgrade_3_Services":
				var_5_1_3 = getFloat(getAttrValue(Product,parameters_3[key]["var_5_3"]))
				var_6_3 = getFloat(getAttrValue(Product,parameters_3[key]["var_6_3"]))
				var_7_3 = getFloat(getAttrValue(Product,parameters_3[key]["var_7_3"]))
				var_8_3 = getFloat(getAttrValue(Product,parameters_3[key]["var_8_3"]))
				var_11_3 = getAttrValue(Product,parameters_3[key]["var_11_3"])
	var_2 = var_2 + var_2_2 + var_2_3
	var_3 = var_3_1 + var_3_2 + var_3_1_2 + var_3_2_2 + var_3_1_3 + var_3_2_3
	var_4 = var_4_1 + var_4_2 + var_4_1_2 + var_4_2_2 + var_4_1_3 + var_4_2_3
	var_5 = var_5_1 + var_5_1_2 + var_5_1_3
	var_6 = var_6_1 + var_6_2 + var_6_3
	var_7 = var_7_1 + var_7_2 + var_7_3
	var_8 = var_8_1 + var_8_2 + var_8_3
	var_12=var_12_1+var_12_2+var_12_3
	var_14 = var_14_1 + var_14_2 + var_14_3
	if var_4<=5.00 and var_6<=5.00 and var_3<=3.00 and var_8==0 and var_5<=2.00 :
		var_10 = "Small"
	elif var_4>15.00 or var_6>15.00 or var_3>6.00 or var_8>4.00 or var_5>5.00 :
		var_10 = "Large"
	else :
		var_10 ="Medium"

	if var_2>0 and var_14>0:
		var_13 = "Upgr+Add"
	elif var_2>0 and var_14==0:
		var_13 = "Upgr"
	else:
		var_13 = "Add"

	Planning_and_Kom = 0
	Ordering_Software_Hardware = 0
	installation_and_config =0
	Documentation_Workpack_FAT_Checklist_SAT_Checklist =0
	interal_testing = 0 if(var_13=="Add") else 8.00
	System_backup = 0 if(var_13=="Add") else 8.00
	Commissioning= 0 
	SAT=0
	AS_Built_Documentation_and_Corrective_Actions=0
	Project_Closeout=0
	Trace.Write('Var_2:{0} , Var_3:{1} , Var_4:{2}, Var_5:{3} , Var_6:{4} , var_7:{5} , var_8:{6} , var_10:{7} , var_11:{8} , var_12:{9}'.format(var_2,var_3,var_4,var_5,var_6,var_7,var_8,var_10,var_11,var_12))
	Trace.Write('var_13:{0}, var_14:{1}'.format(var_13,var_14))
	#Planning_and_Kom
	if var_13 == "Upgr":
		Planning_and_Kom = 16.00 if(var_10 == "Large") else 8.00
	elif var_13=="Add":
		Planning_and_Kom = 4.00
	else:
		Planning_and_Kom = 20.00 if(var_10 == "Large") else 12.00
	#Ordering_Software_Hardware
	if var_13 == "Upgr":
		Ordering_Software_Hardware = 8.00 if(var_10 == "Large") else 4.00
	elif var_13 == "Add":
		Ordering_Software_Hardware = 4.00
	else:
		Ordering_Software_Hardware = 12.00 if(var_10 == "Large") else 8.00

	migration_of_fdm_servers = 0 
	migration_of_fdm_clients = 0
	migration_of_rci = 0
	Installation_and_Configuration_of_Network_Interfaces = ((var_6*20.00)/60.00) if(var_6>15.00) else ((var_6*30.00)/60.00)
	Installation_of_FDM_Maintenance_Station_View_Features = m.ceil((var_7*15.00)/60.00)
	Installation_and_Configuration_of_FDM_Gateways =0
	PSVT_Planner_config = m.ceil((var_12*2.5)/60.00)
	if var_2==0:
		migration_of_fdm_servers = 0
	elif var_2 == 3.00:
		migration_of_fdm_servers = 32.00
	else:
		migration_of_fdm_servers = 16.00 if(var_2==1) else 24.00
	if var_3<=4.00:
		migration_of_fdm_clients = var_3*3.00
	elif var_3>8.00:
		migration_of_fdm_clients = 22.00+(var_3-8.00)*2.00
	else:
		migration_of_fdm_clients = 12.00+(var_3-4.00)*2.5
	#migration_of_rci 
	if var_4<=4.00:
		migration_of_rci = var_4*3.00
	elif var_4>8.00:
		migration_of_rci = 22.00+(var_4-8.00)*2.00
	else:
		migration_of_rci = 12.00+(var_4-4.00)*2.5
	#Installation_and_Configuration_of_FDM_Gateways
	if var_8<=2.00:
		Installation_and_Configuration_of_FDM_Gateways = var_8*4.00
	elif var_8>4.00:
		Installation_and_Configuration_of_FDM_Gateways = 13.00 + (var_8-4.00)*2
	else:
		Installation_and_Configuration_of_FDM_Gateways = 8.00 + (var_8-2.00)*2.5
	installation_and_config = migration_of_fdm_servers+migration_of_fdm_clients+migration_of_rci+Installation_and_Configuration_of_Network_Interfaces+Installation_of_FDM_Maintenance_Station_View_Features+Installation_and_Configuration_of_FDM_Gateways+PSVT_Planner_config
	#Documentation_Workpack_FAT_Checklist_SAT_Checklist
	if var_13 =="Add":
		Documentation_Workpack_FAT_Checklist_SAT_Checklist=0
	elif var_10=="Large":
		Documentation_Workpack_FAT_Checklist_SAT_Checklist=40
	else: 
		if var_10 =="Small":
			Documentation_Workpack_FAT_Checklist_SAT_Checklist=24 
		else:
			Documentation_Workpack_FAT_Checklist_SAT_Checklist=32

	#Commissioning
	if var_13=="Upgr":
		Commissioning =8.00
	elif var_13=="Add":
		Commissioning =8.00
	else:
		Commissioning =12.00
	#SAT
	if var_11_1 == "Yes" or var_11_2 == "Yes" or var_11_3 == "Yes":
		if var_13=="Upgr": 
			if var_2 == 3.00:
				SAT = 16.00
			else:
				SAT = 8.00
		elif var_13=="Add":
			SAT=8.00
		else:
			if var_2==3.00:
				SAT=16.00+4.00
			else:
				SAT=8.00+4.00
	else:
		SAT=0
	#AS_Built_Documentation_and_Corrective_Actions 
	if var_13=="Upgr":
		AS_Built_Documentation_and_Corrective_Actions=4.00
	elif var_13=="Add":
		AS_Built_Documentation_and_Corrective_Actions=4.00
	else:
		AS_Built_Documentation_and_Corrective_Actions=6.00
	# Project_Closeout
	if var_13=="Upgr":
		Project_Closeout=4.00
	elif var_13=="Add":
		Project_Closeout=4.00
	else:
		Project_Closeout=6.00
	Trace.Write('Planning_and_Kom:{0} , installation_and_confi:{1} , Documentation_Workpack_FAT_Checklist_SAT_Checklist:{2} , Ordering_Software_Hardware:{3}'.format(Planning_and_Kom,installation_and_config,Documentation_Workpack_FAT_Checklist_SAT_Checklist,Ordering_Software_Hardware))
	Trace.Write('Commissioning:{0} , SAT:{1} , AS_Built_Documentation_and_Corrective_Actions:{2} , Project_Closeout:{3}'.format(Commissioning,SAT,AS_Built_Documentation_and_Corrective_Actions,Project_Closeout))
	Trace.Write('System_backup:{0} , interal_testing:{1}'.format(System_backup,interal_testing))
	return Planning_and_Kom, System_backup, Ordering_Software_Hardware, installation_and_config,Documentation_Workpack_FAT_Checklist_SAT_Checklist, interal_testing, Commissioning, SAT, AS_Built_Documentation_and_Corrective_Actions, Project_Closeout

def getXP10LabourHours(Product):
	parameters ={"XP10_Actuator_General_Information":{"var_1":"XP10_Actuator_current_actuator_model","var_2":"ATT_XP10ACTUPG"}}
	for key in parameters:
		if key == "XP10_Actuator_General_Information":
			var_1 = getAttrValue(Product,parameters[key]["var_1"])
			var_2 = getFloat(getAttrValue(Product,parameters[key]["var_2"]))

	F12=0
	if var_2<=20:
		F12 = 0.6
	elif var_2 > 20 and var_2 < 35:
		F12= 0.45
	elif var_2>35 and var_2<=45:
		F12=0.4
	elif var_2>45 and var_2<=65:
		F12=0.35
	elif var_2>65:
		F12=0.2

	F15=F12
	F16=0.1
	Site_installation = (F15+F16)*var_2
	if var_1 == "A5":
		Site_installation += 0.2*var_2
	else:
		Site_installation += 0.25*var_2
	Site_installation = (Site_installation + (0.1*var_2))/8
	Site_installation = m.ceil(Site_installation) * 8
	return Site_installation

def getLMtoELMMLabourHours(Quote,Product,msid_product):
	try:
		#var 2
		_900A01_0202 = 0
		_900B01_0301 = 0
		_900G03_0202 = 0
		_900G32_0101 = 0
		_900H01_0202 = 0
		_900H03_0202 = 0
		_900H32_0102 = 0
		_900K01_0201 = 0
		_900G04_0101 = 0
		#var 3
		_900ES1_0100 = 0
		#var 5
		_3rd_Party_cabinet = 0
		#var 6
		_900R08_0200 = 0
		_900R08R_0200 = 0
		_900R12_0200 = 0
		_900R12R_0200 = 0
		#var 8
		_51305482_102_h = 0
		_51305482_202_h = 0
		_51305482_105_h = 0
		_51305482_205_h = 0
		_51305482_110_h = 0
		_51305482_210_h = 0
		_51305482_120_h = 0
		_51305482_220_h = 0
		LMPartCont = msid_product.GetContainerByName('MSID_LM_TO_ELMM_Added_Parts_Common_Container').Rows
		
		Trace.Write("test::")
		LM3rdparty = msid_product.GetContainerByName('MSID_Third_Party_Added_Parts_Common_Container').Rows
		for row in LMPartCont:
			#var 2
			if row['PartNumber']=='900A01-0202':
				_900A01_0202 = row['Quantity']
			if row['PartNumber']=='900B01-0301':
				_900B01_0301 = row['Quantity']
			if row['PartNumber']=='900G03-0202':
				_900G03_0202 = row['Quantity']
			if row['PartNumber']=='900G32-0301':
				_900G32_0101 = row['Quantity']
			if row['PartNumber']=='900H01-0202':
				_900H01_0202 = row['Quantity']
			if row['PartNumber']=='900H03-0202':
				_900H03_0202 = row['Quantity']
			if row['PartNumber']=='900H32-0302':
				_900H32_0102 = row['Quantity']
			if row['PartNumber']=='900K01-0201':
				_900K01_0201 = row['Quantity']
			if row['PartNumber']=='900G04-0101':
				_900G04_0101 = row['Quantity']
			#var 3
			if row['PartNumber']=='900ES1-0100':
				_900ES1_0100 = row['Quantity']
			#var 6
			if row['PartNumber']=='900R08-0300':
				_900R08_0200 = row['Quantity']
			if row['PartNumber']=='900R08R-0300':
				_900R08R_0200 = row['Quantity']
			if row['PartNumber']=='900R12-0300':
				_900R12_0200 = row['Quantity']
			if row['PartNumber']=='900R12R-0300':
				_900R12R_0200 = row['Quantity']
			#var 8
			if row['PartNumber']=='51305482-102':
				_51305482_102_h = row['Quantity']
			if row['PartNumber']=='51305482-202':
				_51305482_202_h = row['Quantity']
			if row['PartNumber']=='51305482-105':
				_51305482_105_h = row['Quantity']
			if row['PartNumber']=='51305482-205':
				_51305482_205_h = row['Quantity']
			if row['PartNumber']=='51305482-110':
				_51305482_110_h = row['Quantity']
			if row['PartNumber']=='51305482-210':
				_51305482_210_h = row['Quantity']
			if row['PartNumber']=='51305482-120':
				_51305482_120_h = row['Quantity']
			if row['PartNumber']=='51305482-220':
				_51305482_220_h = row['Quantity']
		#var_5
		for row in LM3rdparty:
			if row["PartNumber"] == "3rd Party Cabinet" and row["ModuleName"] == "LMTOELMM":
				_3rd_Party_cabinet = row['Quantity']
	except:
		Trace.Write("Error in LM to ELMM Part Container ")
	var_1 = getFloat(getAttrValue(Product,"ATT_LM_QTY_OF_LMPAIR_TOBE_MIGRATED"))
	var_2 = getFloat(m.floor(getFloat(_900A01_0202)) + m.floor(getFloat(_900B01_0301)) + m.floor(getFloat(_900G03_0202)) + m.floor(getFloat(_900G32_0101)) + m.floor(getFloat(_900H01_0202)) + m.floor(getFloat(_900H03_0202)) + m.floor(getFloat(_900H32_0102)) + m.floor(getFloat(_900K01_0201)) + m.floor(getFloat(_900G04_0101)))
	var_3 = getFloat(m.floor(getFloat(_900ES1_0100)))
	var_5 = getFloat(m.floor(getFloat(_3rd_Party_cabinet)))
	var_6 = getFloat(m.floor(getFloat(_900R08_0200)) + m.floor(getFloat(_900R08R_0200)) + m.floor(getFloat(_900R12_0200)) + m.floor(getFloat(_900R12R_0200)))
	if var_1 != 0:
		var_8 = getFloat(m.floor(getFloat(_51305482_102_h))*2.00 + m.floor(getFloat(_51305482_202_h))*2.00 + m.floor(getFloat(_51305482_105_h))*5.00 + m.floor(getFloat(_51305482_205_h))*5.00 + m.floor(getFloat(_51305482_110_h))*10.00 + m.floor(getFloat(_51305482_210_h))*10.00 + m.floor(getFloat(_51305482_120_h))*20.00 + m.floor(getFloat(_51305482_220_h))*20.00)/var_1
	else:
		var_8 = 0.00
	var_4 = 0.00
	var_18 = 0.00
	var_25_check = Quote.GetCustomField('Entitlement').Content
	if var_25_check in ('K&E Pricing Flex','K&E Pricing Plus','Non-SESP MSID with new SESP Plus','Non-SESP MSID with new SESP Flex'):
		var_25 = "Yes"
	else:
		var_25 = "No"
	#var_12 - check
	parameters = {"MSID_CommonQuestions":{"var_12":"MSID_Is_FTE_based_System_already_installed_on_Site","var_14":"Yes-No Selection","var_16":"ATTR_COMQESYORN"},"LM_to_ELMM_Services":{"var_15":"AT_LM_ELMM_FELDATA_REQUIRED","var_17":"ATT_LM_ELMM_FACTORY_ACCEPTANCE","var_24":"ATT_LT_ELMM_HONEYWELL_INSTALLATION"},"LM_to_ELMM_Migration_Additional_IO_Cont":{"var_9":"LM_any_unsupported_instruction_in_the_LM_ladder_logic","var_10":"qty_3party_customized_ladder_used_in_the_LM_0_100","var_11":"qty_interposing_relays_IOM_621_2100R_2101R_2150R_6575_0_100","var_22_23":"qty_IO_points_to_be_rewired_0_5000"},"LM_to_ELMM_ControlEdge_PLC_Remote_IO_Cont":{"var_7":"total_remote_serial_IO_racks_0_16"},"LM_to_ELMM_ControlEdge_PLC_Cont":{"var_20":"LM_do_you_have_additional_space_in_the_cabinet_room_to_mount_the_CE_System","var_19":"LM_do_you_need_Redundant_PS_for_IO_Racks"}}
	for key in parameters:
		if key == "MSID_CommonQuestions":
			var_12 = getAttrValue(msid_product,parameters[key]["var_12"])
			var_14 = getAttrValue(msid_product,parameters[key]["var_14"])
			var_16 = getAttrValue(msid_product,parameters[key]["var_16"])
			Trace.Write("var_16::"+str(var_16))
		if key == "LM_to_ELMM_Services":
			var_15 = getAttrValue(Product,parameters[key]["var_15"])
			var_17 = getAttrValue(Product,parameters[key]["var_17"])
			var_24 = getAttrValue(Product,parameters[key]["var_24"])
		if key == "LM_to_ELMM_Migration_Additional_IO_Cont":
			var_9 = 0
			var_10 = 0
			var_11 = 0
			var_22 = 0
			var_23 = 0
			for row in getContainer(Product, key).Rows:
				var_10 += getFloat(row[parameters[key]["var_10"]])
				var_11 += getFloat(row[parameters[key]["var_11"]])
				if row[parameters[key]["var_9"]] in ("Yes","Unknown"): 
					var_9 += 1.00
				if getRowDataIndex(Product,"LM_to_ELMM_ControlEdge_PLC_Cont","LM_do_the_customer_wants_to_retain_the_wiring",row.RowIndex) == "Yes":
					var_23 += getFloat(row[parameters[key]["var_22_23"]])
				else:
					var_22 += getFloat(row[parameters[key]["var_22_23"]])
		if key == "LM_to_ELMM_ControlEdge_PLC_Remote_IO_Cont":
			var_7 = 0
			for row in getContainer(Product, key).Rows:
				var_7 += getFloat(row[parameters[key]["var_7"]])
		if key == "LM_to_ELMM_ControlEdge_PLC_Cont":
			var_20 = 0.00
			var_19 = "No"
			for row in getContainer(Product, key).Rows:
				if row[parameters[key]["var_20"]] == "Yes":
					var_20 += 0.00
				else:
					var_20 += 1.00

				if row[parameters[key]["var_19"]] == "Yes":
					var_19 = "Yes"

	var_21 = 0.00
	for row in getContainer(Product, "LM_to_ELMM_ControlEdge_PLC_Local_IO_Cont").Rows:
		if getRowDataIndex(Product,"LM_to_ELMM_ControlEdge_PLC_Cont","LM_do_you_have_additional_space_in_the_cabinet_room_to_mount_the_CE_System",row.RowIndex) == "Yes":
			continue
		var_21 += getFloat(row["qty_621_0022_AR_VR_Isolated_AI_IOM_0_72"])
		var_21 += getFloat(row["qty_621_0010_AR_VR_AO_IOM_0_72"])
		var_21 += getFloat(row["qty_621_1100R_115_VAC_VDC_DI_IOM_0_72"])
		var_21 += getFloat(row["qty_621_1101R_115_VAC_VDC_Isolated_DI_IOM_0_72"])
		var_21 += getFloat(row["qty_621_1180R_115_VAC_VDC_Isolated_DI_IOM_0_72"])
		var_21 += getFloat(row["qty_621_1500R_24_VAC_VDC_DI_IOM_0_72"])
		var_21 += getFloat(row["qty_621_3552R_3560R_24_VAC_VDC_Sink_DI_IOM_0_72"])
		var_21 += getFloat(row["qty_621_3580_24_VDC_DI_IOM_0_72"])
		var_21 += getFloat(row["qty_621_4500R_24_VDC_Source_DI_IOM_0_72"])
		var_21 += getFloat(row["qty_621_1160R_1250R_115VAC_240VAC_DI_IOM_0_72"])
		var_21 += getFloat(row["qty_621_0007R_Reed_Relay_Output_IOM_0_72"])
		var_21 += getFloat(row["qty_621_2150R_115VAC_DO_IOM_0_72"])
		var_21 += getFloat(row["qty_621_6550R_6551R_24_VDC_DO_IOM_0_72"])
		var_21 += getFloat(row["qty_621_6575_24_VDC_DO_IOM_0_72"])
		var_21 += getFloat(row["qty_621_2200R_230_VAC_DO_IOM_0_72"])
		var_21 += getFloat(row["qty_621_2100R_2101R_2102R_115_VAC_DO_IOM_0_72"])
		var_21 += getFloat(row["qty_621_6500R_12_24_VDC_Source_DO_IOM_0_72"])
		var_21 += getFloat(row["qty_621_6503R_12_24_VDC_Source_Self_Protected_DO_IOM_0_72"])
		var_21 += getFloat(row["qty_ASCII_IOM_0_6"])
		var_21 += getFloat(row["qty_621_0020R_UAIM_621_0025R_RTDM_IOM_0_72"])
		var_21 += getFloat(row["qty_621_0024R_0307R_Pulse_Input_Module_High_Speed_Counter_IOM_0_6"])
	for row in getContainer(Product, "LM_to_ELMM_ControlEdge_PLC_Remote_IO_Cont").Rows:
		if getRowDataIndex(Product,"LM_to_ELMM_ControlEdge_PLC_Cont","LM_do_you_have_additional_space_in_the_cabinet_room_to_mount_the_CE_System",row.RowIndex) == "Yes":
			continue
		var_21 += getFloat(row["total_qty_621_0022_AR_0022_VR_Isolated_AI_IOM_0_72"])
		var_21 += getFloat(row["total_qty_621_0010_AR_0010_VR_AO_IOM_0_72"])
		var_21 += getFloat(row["total_qty_621_1100R_115_Vac_Vdc_DI_IOM_0_72"])
		var_21 += getFloat(row["total_qty_621_1101R_115_Vac_Vdc_Isolated_DI_IOM_0_72"])
		var_21 += getFloat(row["total_qty_621_1180R_115_Vac_Vdc_Isolated_DI_IOM_0_72"])
		var_21 += getFloat(row["total_qty_621_1500R_24_Vac_Vdc_DI_IOM_0_72"])
		var_21 += getFloat(row["total_qty_621_3552R_3560R_24_Vdc_Sink_DI_IOM_0_72"])
		var_21 += getFloat(row["total_qty_621_3580_24Vdc_DI_IOM_0_72"])
		var_21 += getFloat(row["total_qty_621_4500R_24_Vdc_Source_DI_IOM_0_72"])
		var_21 += getFloat(row["total_qty_621_1160R_1250R_115Vac_240_Vac_DI_IOM_0_72"])
		var_21 += getFloat(row["total_qty_621_0007R_Reed_Relay_Output_IOM_0_72"])
		var_21 += getFloat(row["total_qty_621_2150R_115_Vac_DO_IOM_0_72"])
		var_21 += getFloat(row["total_qty_621_6550R_6551R_24_Vdc_DO_IOM_0_72"])
		var_21 += getFloat(row["total_qty_621_6575_24_Vdc_DO_IOM_0_72"])
		var_21 += getFloat(row["total_qty_621_2200R_230_Vac_DO_IOM_0_72"])
		var_21 += getFloat(row["total_qty_621_2100R_2101R_2102R_115_Vac_DO_IOM_0_72"])
		var_21 += getFloat(row["total_qty_621_6500R_12_24_Vdc_Source_DO_IOM_0_72"])
		var_21 += getFloat(row["total_qty_621_6503R_12_24_Vdc_Source_Self-Protected_DO_IOM_0_72"])
		var_21 += getFloat(row["total_qty_ASCII_IOM_0_6"])
		var_21 += getFloat(row["total_qty_621_0020R_UAIM_0025R_RTDM_IOM_0_72"])
		var_21 += getFloat(row["total_qty_621_0024R_0307R_Pulse_Input_Module_High_Speed_Counter_IOM_0_6"])

	#calculation
	plan_kom = 24.00 if var_25 == "No" else 20.00
	plan_eaps = plan_kom*0.95
	plan_esss = plan_kom*0.05
	feldatagathering = 40.00 if var_15 == "Yes" else 0.00
	migrationdds = 70.00
	migrationdds_esss = 0.00
	migrationdds_eaps = 0.00
	sw_hworder = 8.00
	inhouse = 0.00
	inhouse_esss = 0.00
	inhouse_eaps = 0.00
	prefat = 0.00
	fat = 0.00
	siteinstallation_est = 0.00
	siteinstallation_eaps = (1.50*var_1) + (var_2 + var_6 + var_18)*0.10
	sat = 20.00

	if var_1 > 1:
		migrationdds += (var_1 - 1.00)
	if var_16 == "Yes":
		migrationdds += 80.00
	migrationdds_esss = migrationdds*0.10
	migrationdds_eaps = migrationdds*0.90

	inhouse = (18.10*var_1) + (var_9 + var_10)*4.00 + (var_3*10.00)
	inhouse_esss = inhouse*0.10
	inhouse_eaps = inhouse*0.90

	if var_17 == "Yes":
		prefat += 28.00
		if var_1 > 1:
			prefat += (var_1 - 1.00)

	if var_17 == "Yes":
		fat += 16.00
		if var_1 > 1:
			fat += 4.00*(var_1 - 1.00)

	if var_1 > 1:
		sat += (16.00 + 1.50*(var_1 - 1.00))

	if var_14 == "Yes":
		siteinstallation_eaps += 1.00
	if var_25 == "No":
		if var_12 == "No":
			siteinstallation_eaps += 24.00
		else:
			siteinstallation_eaps += 48.00
	if var_1 > 5:
		siteinstallation_eaps += 80.00
	else:
		siteinstallation_eaps += 40.00

	if var_24 == "Yes":
		siteinstallation_est = (var_1*2.00) + (var_5*7.50) + (2.00 + (var_8/30.00) + (var_8/20.00))*var_7
		if (var_8/30.00) < 30.00:
			siteinstallation_est += (1.50*var_7)
		else:
			siteinstallation_est += ((var_8/30.00)*var_7)
		siteinstallation_est += (0.10*var_11 + 2.00 + 4.00*var_20)
		if var_20 > 0.00:
			siteinstallation_est += (0.10*var_21)
			if var_19 == "Yes":
				siteinstallation_est += (0.60*var_6)
			else:
				siteinstallation_est += (0.50*var_6)
		siteinstallation_est += (1.25*var_22 + 0.50*var_23)

	return plan_esss, plan_eaps, feldatagathering, migrationdds_esss, migrationdds_eaps, sw_hworder, inhouse_esss, inhouse_eaps, prefat, fat, siteinstallation_eaps, siteinstallation_est, sat

# def getXP10LabourHours(Product):
#     parameters ={"XP10_Actuator_General_Information":{"var_1":"XP10_Actuator_Select_current_actuator_model","var_2":"XP10_Actuator_Number_of_actuators_to_be_upgraded"}}
#     for key in parameters:
#         if key == "XP10_Actuator_General_Information":
#             var_1 = getRowData(Product,key,parameters[key]["var_1"])
#             var_2 = getFloat(getRowData(Product,key,parameters[key]["var_2"]))

#     F12=0
#     if var_2<=20:
#         F12 = 0.6
#     elif var_2 > 20 and var_2 < 35:
#         F12= 0.45
#     elif var_2>35 and var_2<=45:
#         F12=0.4
#     elif var_2>45 and var_2<=65:
#         F12=0.35
#     elif var_2>65:
#         F12=0.2

#     F15=F12
#     F16=0.1
#     Site_installation = (F15+F16)*var_2
#     if var_1 == "A5":
#         Site_installation += 0.2*var_2
#     else:
#         Site_installation += 0.25*var_2
#     Site_installation = (Site_installation + (0.1*var_2))/8
#     Site_installation = m.ceil(Site_installation) * 8
#     return Site_installation

def getFSCtoSMIOAuditLabourHours(Product):
	var_1 = 0
	var_8 = 0
	var_9 = ''
	#Cont1 = Product.GetContainerByName('FSC_to_SM_IO_Migration_General_Information')
	Cont2 = Product.GetContainerByName('FSC_to_SM_IO_Series_1_&_2_FSC_IO_configurations')
	Cont3 = Product.GetContainerByName('FSC_to_SM_IO_Services')
	#row = Cont1.Rows[0]
	var_1 = int(getAttrValue(Product,'ATT_FSCtoSMIOMigrationTotalFSC')) if getAttrValue(Product,'ATT_FSCtoSMIOMigrationTotalFSC') != '' else 0
	#service = Cont3.Rows[0]
	var_9 = getAttrValue(Product,'FSC_to_SM_IO_Has_the_FSC_IO_Audit_been_performed')
	for rack in Cont2.Rows:
		if rack['FSC_to_SM_IO_IO_Module_IO_Rack_Type'] == 'RED':
			red = 0 if rack['FSC_to_SM_IO_Number_of_IO_Racks'] == '' else int(rack['FSC_to_SM_IO_Number_of_IO_Racks'])
			Trace.Write(red)
		if rack['NON_RED_FSC_to_SM_IO_IO_Module_IO_Rack_Type'] == 'NON-RED':
			nonred = int(rack['NON_RED_FSC_to_SM_IO_Number_of_IO_Racks']) if rack['NON_RED_FSC_to_SM_IO_Number_of_IO_Racks'] != '' else 0
			Trace.Write(nonred)
		sum1 = red+nonred
		if sum1 > 6:
			var_8 = var_8 + 1

	if not(var_9 == 'Yes'):
		Safety_Audit = var_8*24+(var_1-var_8)*16
	else:
		Safety_Audit = 0
	return Safety_Audit