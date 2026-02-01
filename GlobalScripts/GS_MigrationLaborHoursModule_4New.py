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
def calculateEMPEfforts(Product,Con):
    EMP_Hrs=0
    RMP_Effort = Product.Attr('Regional_Migration_Principal_Efforts_Required').GetValue()
    if RMP_Effort=="Yes":
        for row in Con.Rows:
            if row["Deliverable"] not in ["Off-Site","On-Site","Total","Regional Migration Principal Efforts"]:
                EMP_Hrs+=int(getFloat(row["Final_Hrs"]))
    for row in Con.Rows:
        if row["Deliverable"] == "Regional Migration Principal Efforts":
            oldCalHrs = row["Calculated_Hrs"]
            row["Calculated_Hrs"] = str(float(EMP_Hrs*8)/100) if EMP_Hrs else '0'
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            Trace.Write(str(Con)+"EMP_Hrs-"+str(EMP_Hrs)+"- row['Calculated_Hrs']-"+str(row['Calculated_Hrs']))
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
def getGraphicsMigrationLabourHours(Product,msid_product):
	Trace.Write("test::")
	parameters ={"Graphics_Migration_Migration_Scenario":{"var_51":"ATT_GMPERUSD","var_1":"Graphics_Migration_Select_Vertical_Market","var_34":"Graphics_Migration_Have_specific_native_or_GUS","var_33":"Graphics_Migration_Require_an_HMI_interface_for_AM","var_32":"Migration_Graphics_Willing_to_accept_alternative","var_31":"Migration_Graphics_Have_array_point_that_requires","var_16":"Migration_Graphics_Using_device_control_digital","var_17":"Migration_Graphics_Have_multiple_DI_or_DO","var_18":"Graphics_Migration_Require_multi_tag_shapes","var_19":"Graphics_Migration_Have_process_module_point","var_20":"Migration_Configuration_Is_Standard_Builds_used","var_21":"Graphics_Migration_Is_the_system_connected_to","var_26":"Graphics_Migration_Type_of_Existing_Displays"},"Graphics_Migration_Displays_Shapes_Faceplates":{"var_35":"Experion_shapes_multiplier","var_2":"Total_Number_of_Displays","var_3":"Number_of_Simple_Displays","var_4":"Number_of_Medium_Displays","var_5":"Number_of_Complex_Displays","var_6":"Number_of_Very_Complex_Displays","var_7":"Number_of_Repeats_Displays","var_8":"Total_Number_of_Custom_Shapes","var_9":"Number_of_Simple_Custom_Shapes","var_10":"Number_of_Medium_Custom_Shapes","var_11":"Number_of_Complex_Custom_Shapes","var_12":"Number_of_Very_Complex_Custom_Shapes","var_13":"Number_of_Repeats_Custom_Shapes","var_14":"Total_Number_of_Custom_Faceplates","var_15":"Number_of_Custom_Context_Menus","var_37":"Number_of_Simple_Custom_Faceplates","var_38":"Number_of_Medium_Custom_Faceplates","var_39":"Number_of_Complex_Custom_Faceplates","var_40":"Number_of_Very_Complex_Custom_Faceplates","var_41":"Number_of_Repeats_Custom_Faceplates"},"Graphics_Migration_Training_Testing_Documentation":{"var_50":"Graphics_Migration_DDS_Required?","var_49":"Graphics_Migration_FDS_Required?","var_22":"Graphics_Migration_FAT_required?","var_23":"Graphics_Migration_Does_the_customer_require_SAT?","var_24":"Graphics_Migration_Does_require_Operator_Training?","var_25":"ATT_GMTRNSESREQ"},"Graphics_Migration_Additional_Questions":{"var_36":"Graphics_Migration_For_GAP_Analysis_project_com","var_27":"Graphics_Migration_Gap_Analysis_done?","var_42":"Graphics_Migration_DCA_IRA_done?","var_43":"Graphics_Migration_New_Safeview_Configuration","var_44":"Graphics_Migration_Alarm_groups_configured?","var_45":"ATT_GMNUMSL","var_29":"ATT_GMADGAPAN","var_48":"ATT_GMOBJSI"}}
	for key in parameters:
		if key == "Graphics_Migration_Migration_Scenario":
			Trace.Write("test11::")
			var_51 = getFloat(getAttrValue(Product,parameters[key]["var_51"]))
			Trace.Write("test12::")
			var_1 = getAttrValue(Product,parameters[key]["var_1"])
			var_34 = getAttrValue(Product,parameters[key]["var_34"])
			var_31 = getAttrValue(Product,parameters[key]["var_31"])
			var_32 = getAttrValue(Product,parameters[key]["var_32"])
			var_33 = getAttrValue(Product,parameters[key]["var_33"])
			var_16 = getAttrValue(Product,parameters[key]["var_16"])
			var_17 = getAttrValue(Product,parameters[key]["var_17"])
			var_18 = getAttrValue(Product,parameters[key]["var_18"])
			var_19 = getAttrValue(Product,parameters[key]["var_19"])
			var_20 = getAttrValue(Product,parameters[key]["var_20"])
			var_21 = getAttrValue(Product,parameters[key]["var_21"])
			var_26 = getAttrValue(Product,parameters[key]["var_26"])
			
		if key == "Graphics_Migration_Displays_Shapes_Faceplates":
			Trace.Write("test2::")
			var_35 = getFloat(getRowData(Product,key,parameters[key]["var_35"]))
			Trace.Write("test3::")
			var_2 = getFloat(getRowData(Product,key,parameters[key]["var_2"]))#2-15 35
			var_3 = getFloat(getRowData(Product,key,parameters[key]["var_3"]))
			var_4 = getFloat(getRowData(Product,key,parameters[key]["var_4"]))
			var_5 = getFloat(getRowData(Product,key,parameters[key]["var_5"]))
			var_6 = getFloat(getRowData(Product,key,parameters[key]["var_6"]))
			var_7 = getFloat(getRowData(Product,key,parameters[key]["var_7"]))
			var_8 = getFloat(getRowData(Product,key,parameters[key]["var_8"]))
			var_9 = getFloat(getRowData(Product,key,parameters[key]["var_9"]))
			var_10 = getFloat(getRowData(Product,key,parameters[key]["var_10"]))
			var_11 = getFloat(getRowData(Product,key,parameters[key]["var_11"]))
			var_12 = getFloat(getRowData(Product,key,parameters[key]["var_12"]))
			var_13 = getFloat(getRowData(Product,key,parameters[key]["var_13"]))
			var_14 = getFloat(getRowData(Product,key,parameters[key]["var_14"]))
			var_15 = getFloat(getRowData(Product,key,parameters[key]["var_15"]))
			var_37 = getFloat(getRowData(Product,key,parameters[key]["var_37"]))
			var_38 = getFloat(getRowData(Product,key,parameters[key]["var_38"]))
			var_39 = getFloat(getRowData(Product,key,parameters[key]["var_39"]))
			var_40 = getFloat(getRowData(Product,key,parameters[key]["var_40"]))
			var_41 = getFloat(getRowData(Product,key,parameters[key]["var_41"]))

		if key == "Graphics_Migration_Training_Testing_Documentation":
			Trace.Write("test13::")
			var_49 = getAttrValue(Product,parameters[key]["var_49"])
			var_50 = getAttrValue(Product,parameters[key]["var_50"])
			var_22 = getAttrValue(Product,parameters[key]["var_22"])
			var_23 = getAttrValue(Product,parameters[key]["var_23"])
			var_24 = getAttrValue(Product,parameters[key]["var_24"])
			var_25 = getFloat(getAttrValue(Product,parameters[key]["var_25"]))
		
		if key == "Graphics_Migration_Additional_Questions":
			Trace.Write("test123::")
			var_45 = getFloat(getAttrValue(Product,parameters[key]["var_45"]))
			Trace.Write("var_45::"+str(var_45))
			var_36 = getAttrValue(Product,parameters[key]["var_36"])
			var_27 = getAttrValue(Product,parameters[key]["var_27"])
			var_42 = getAttrValue(Product,parameters[key]["var_42"])
			var_43 = getAttrValue(Product,parameters[key]["var_43"])
			var_44 = getAttrValue(Product,parameters[key]["var_44"])
			var_29 = getFloat(getAttrValue(Product,parameters[key]["var_29"]))
			var_48 = getFloat(getAttrValue(Product,parameters[key]["var_48"]))

	Ges_Location=msid_product.Attr('MSID_GES_Location').GetValue()
	if var_26 == "Existing US Graphics":
		var_28 = 1.00
	elif var_26 == "Existing GUS Graphics":
		var_28 = 0.9
	elif var_26 == "Existing Experion .DSP Graphics":
		var_28 = 0.9
	elif var_26 == "Existing Experion HMI Web Graphics Release 200-310":
		var_28 = 0.3
	elif var_26 == "Existing Experion HMI Web Graphics Release 311-400":
		var_28 = 0.2
	elif var_26 == "Existing Experion HMI Web Graphics Release 400-510":
		var_28 = 0.1
	else:
		var_28 = 0
	#=IF(var_2<50,"small", IF(AND(var_2>49,var_2<201),"medium", "large"))
	if var_2<50:
		var_30 = "small"
	elif var_2>49 and var_2<201:
		var_30 = "medium"
	else:
		var_30 = "large"
	#IF(var_43="Single",012,0)+IF(var _43="Dual",013,0)+IF(var 43="Triple",014,0)+IF(var_43="Quad",015,0)+IF(var_43="Combination",016,0)
	var_46=0
	var_46+= 0.5 if(var_43=="Single") else 0
	var_46+= 1.00 if(var_43=="Dual") else 0
	var_46+= 2.00 if(var_43=="Triple") else 0
	var_46+= 2.00 if(var_43=="Quad") else 0
	var_46+= 2.5 if(var_43=="Combination") else 0
	#var_28 30 46 47 48
	#=IF(OR(var_19="Yes",var_33="Yes"),4,IF(var_21="Yes",3,IF(OR(var_26=1,var_26=2,var_26=3),2,1)))
	var_47=0
	if var_19 == "Yes" or var_33 == "Yes":
		var_47 = 4.00
	else:
		if var_21 == "Yes":
			var_47 = 3.00
		elif var_26 == "Existing US Graphics" or var_26 == "Existing GUS Graphics" or var_26 == "Existing Experion .DSP Graphics":
			var_47 = 2.00
		else:
			var_47 = 1.00
	#var_48 = var_2*7.00
	#ROUNDUP((var_2*(55/202)*var_28),0)
	customer_input_Study = m.ceil((var_2 *55/202)*var_28)
	#ROUNDUP((var_2*56)/202,0)
	Query_Generation_Clarification = m.ceil((var_2*56)/202)
	#=ROUNDUP((var_3*8.03+var_4*11.28+var_5*13+var_6*15+var_7*2.57)*var_28,0)+var_29+var_48*0.05
	Display_Generation = m.ceil(((var_3*8.03)+(var_4*11.28)+(var_5*13.00)+(var_6*15.00)+(var_7*2.57))*var_28)
	Display_Generation = Display_Generation + (var_29 + (var_48 *0.05))
	#EAPS=(IF(var_43="None",0,(var_46*4+6+var_45*0.8+IF(var_44="Yes",12,0))))*30%

	#GES=(IF(var_43="None",0,(var_46*4+6+var_45*0.8+IF(var_44="Yes",12,0))))*70%
	# Safeview_Configuration=0
	if var_43=="None":
		Safeview_Configuration = 0.00
	else:
		Safeview_Configuration = var_46*4.00+6.00+var_45*0.8
		if var_44 == "Yes":
			Safeview_Configuration += 12.00
		else:
			Safeview_Configuration +=0.00

	#EAPS==(8*var_47)*30%
	
	Testing_system= 8*var_47
	#=IF(var_23 ="Yes", ROUNDUP(IF(var_30="small",10,IF(var_30="medium",20, 48)),0),0)
	SAT_Support =0
	if var_23 == "Yes":
		if var_30 == "small":
			SAT_Support = 10.00
		elif var_30=="medium":
			SAT_Support = 20.00
		else:
			SAT_Support =48.00
		m.ceil(SAT_Support)
	else:
		SAT_Support=0.00
	#=IF(var_24 ="Yes", ROUNDUP((var_25*8*VLOOKUP(var_30,'Display Advisor'!N3:X6,11,FALSE)+16),0),0)
	Operator_Training = 0
	if var_30 == "small":
		Oper_Train_proj_clos_val = 0.5
	elif var_30 == "medium":
		Oper_Train_proj_clos_val = 1.00
	elif var_30 == "large":
		Oper_Train_proj_clos_val = 2.00
	else:
		Oper_Train_proj_clos_val = 0.00
	if var_24 == "Yes":
		Operator_Training = m.ceil((var_25*8.00*Oper_Train_proj_clos_val)+16.00)
	else:
		Operator_Training = 0.00
	#=8*VLOOKUP(var_30,'Display Advisor'!N3:X6,10,FALSE)
	Project_Close_Out = 8 * Oper_Train_proj_clos_val

	#Shape and Faceplate
	#Shape_and_faceplate_EAPS = m.ceil((((var_9*2.00)+(var_10*6.00)+ (var_11*10.00)+ (var_12*16.00)+(var_13*0.5)+(var_15*8.00))*0.2+((0.7+0.4)*((var_37*3.00)+(var_38*8.00)+(var_39*12.00)+(var_40*18)+(var_41*1.00))*0.2))*var_28)
	#Shape_and_faceplate_GES = m.ceil((((var_9*2.00)+(var_10*6.00)+ (var_11*10.00)+ (var_12*16.00)+(var_13*0.5)+(var_15*8.00))*0.8+((0.7+0.4)*((var_37*3.00)+(var_38*8.00)+(var_39*12.00)+(var_40*18)+(var_41*1.00))))*var_28)
	#Shape_and_faceplate = Shape_and_faceplate_EAPS + Shape_and_faceplate_GES
	Shapes = m.ceil(((var_9*2+var_10*6+var_11*10+var_12*16+var_13*0.5+var_15*8)*var_28))
	#FDS
	fds = 0
	if var_49=="Yes":
		if var_30=="small":
			fds = 16.00 * 1.00
		elif var_30=="medium":
			fds = 16.00 * 2.00
		else:
			fds = 16.00 * 5.00
		fds = (fds + (4.00*var_46))
	else:
		fds = 0.00
	Migration_FDS = fds

	FAT_Support = 0
	if var_22=="Yes via VEP/Remote GES":
		if var_30=="small":
			FAT_Support = (var_2/1.25) + 4.00
		elif var_30 =="medium":
			FAT_Support = (var_2/1.25) + 8.00
		else:
			FAT_Support = (var_2/1.25) + 16.00
		FAT_Support = FAT_Support
	elif var_22 =="Yes no VEP/Remote GES":
		if var_30=="small":
			FAT_Support = (var_2/1.25) + 4.00
		elif var_30 =="medium":
			FAT_Support = (var_2/1.25) + 8.00
		else:
			FAT_Support = (var_2/1.25) + 16.00
		FAT_Support = FAT_Support
	else:
		FAT_Support = 0.00
	FAT_Support = m.ceil(FAT_Support)

#GAP Analysis
	GAP_Analysis_EAPS = 0
	GAP_Analysis_GES = 0
	if var_26 == "Existing US Graphics" or var_26 == "Existing GUS Graphics" or var_26 == "Existing Experion .DSP Graphics":
		if var_36 == "Limitations to use GES":
			if var_27 == "Yes < 2 years for another migration":
				GAP_Analysis_EAPS = ((var_9*0.15) + (var_10*0.3) + (var_11*0.4)) * var_28 * 0.1
			elif var_27 == "No":
				if var_42 == "Yes < 2 years for another migration":
					GAP_Analysis_EAPS = (((var_9*0.15)+ (var_10*0.3) +(var_11 * 0.4))* var_28) * 0.9
				elif var_42 =="No":
					GAP_Analysis_EAPS = ((var_9*0.15)+(var_10*0.3)+(var_11*0.4))*var_28
				else:
					GAP_Analysis_EAPS = (((var_9*0.15)+(var_10*0.3)+(var_11*0.4))*var_28)*0.8
			GAP_Analysis_EAPS = (m.ceil(GAP_Analysis_EAPS))
		elif var_27=="Yes < 2 years for another migration":
			GAP_Analysis_EAPS = (m.ceil(((var_9*0.15)+(var_10*0.3)+(var_11*0.4))*var_28*0.1))
		else:
			if var_27 =="No":
				if var_42=="Yes < 2 years for another migration":
					GAP_Analysis_EAPS = (((var_9*0.15)+(var_10*0.3)+(var_11*0.4))*var_28)*0.9
				else:
					if var_42 =="No":
						GAP_Analysis_EAPS = (((var_9*0.15)+(var_10*0.3)+(var_11*0.4))*var_28)
					else:
						GAP_Analysis_EAPS = (((var_9*0.15)+(var_10*0.3)+(var_11*0.4))*var_28)*0.8
			else:
				GAP_Analysis_EAPS = 0.00
			GAP_Analysis_EAPS = (m.ceil(GAP_Analysis_EAPS ))
	else:
		GAP_Analysis_EAPS = 0.00

	GAP_Analysis = GAP_Analysis_EAPS 

#FAT & SAT Documentation
	FAT_SAT_Documentation1 = 0.00
	FAT_SAT_Documentation2 = 0.00
	FAT_SAT_Documentation = 0.00

	if var_30 == "small":
		FAT_SAT_Documentation1 = 0.50
	elif var_30 == "medium":
		FAT_SAT_Documentation1 = 1.00
	else:
		FAT_SAT_Documentation1 = 2.00

	if var_22 == "Yes via VEP/Remote GES" or var_22 == "Yes no VEP/Remote GES" :
		FAT_SAT_Documentation1 = 8.00 * FAT_SAT_Documentation1
	else :
		FAT_SAT_Documentation1 = 0.00

	if  var_30 == "small":
		FAT_SAT_Documentation2 = 0.60
	elif var_30 == "medium":
		FAT_SAT_Documentation2 = 1.00 
	else:
		FAT_SAT_Documentation2=2

	if var_23 == "Yes":
		FAT_SAT_Documentation2 = 4.00 * FAT_SAT_Documentation2
	else :
		FAT_SAT_Documentation2=0

	FAT_SAT_Documentation = FAT_SAT_Documentation1 + FAT_SAT_Documentation2

#Migration DDS =IF(var_50="Yes",(32*IF(var_30="small",0.6,IF(var_30="medium",1,2))),0)
	Migration_DDS = 0.00
	if var_30 == "small":
		Migration_DDS = 0.60
	elif var_30 == "medium":
		Migration_DDS = 1.00
	else:
		Migration_DDS = 2.00

	if var_50 == "Yes":
		Migration_DDS = 32.00 * Migration_DDS
	else :
		Migration_DDS = 0.00

#Faceplates
	Faceplates = 0.00
	Faceplates_ges_none = m.ceil((((0.70 + 0.40)*(var_37*3.00 + var_38*8.00 + var_39*12.00 + var_40*18.00 + var_41*1.00)))*var_28)
	Faceplates_ges = m.ceil(m.ceil((((0.70 + 0.40)*(var_37*3.00 + var_38*8.00 + var_39*12.00 + var_40*18.00 + var_41*1.00)))*var_28)*1.20)

	if Ges_Location == "None" or Ges_Location == "":
		Faceplates = Faceplates_ges_none
	else:
		Faceplates = Faceplates_ges

	return customer_input_Study, Query_Generation_Clarification, Display_Generation, Safeview_Configuration, Testing_system, SAT_Support, Operator_Training, Project_Close_Out, Shapes, Migration_FDS, FAT_Support, GAP_Analysis, FAT_SAT_Documentation, Migration_DDS, Faceplates

def getCDActuatorLabourHours(Product):
	
	parameters ={"CD_Actuator_IF_Upgrade_General_Info_Cont":{"var_1":"ATT_CD_ACTUATOR_NOZONES","var_2":"CD_Actuator_Actuator_Type","var_3":"CD_Actuator_Interlocks","var_4":"CD_Actuator_QCS_Type","var_5":"CD_Actuator_Lynk_Type"},"CD_Actuator_IF_Upgrade_Services_Cont":{"var_8":"CD_Actuator_SAT_required","var_9":"CD_Actuator_HSE_and_Quality_Plan","var_10":"CD_Actuator_Update_existing_documents"}}
	
	for key in parameters:
		if key == "CD_Actuator_IF_Upgrade_General_Info_Cont":
			var_1 = getFloat(getAttrValue(Product,parameters[key]["var_1"]))
			var_2 = getAttrValue(Product,parameters[key]["var_2"])
			var_3 = getAttrValue(Product,parameters[key]["var_3"])
			var_4 = getAttrValue(Product,parameters[key]["var_4"])
			var_5 = getAttrValue(Product,parameters[key]["var_5"])
		if key == "CD_Actuator_IF_Upgrade_Services_Cont":
			var_8 = getAttrValue(Product,parameters[key]["var_8"])
			var_9 = getAttrValue(Product,parameters[key]["var_9"])
			var_10 = getAttrValue(Product,parameters[key]["var_10"])

	#Additional Docs 
	Additional_Docs = 8.00 if var_9 == "Yes" else 0
	Additional_Docs+= 8.00 if var_10 == "Yes" else 0
	

	#In_house_engineering
	In_house_engineering = 0
	F20 = 8.00
	F21 = 8.00
	F22 = 8.00
	if var_3 == "GE FANUC 90-70" or var_3 == "GE VersaMax" or var_3 == "HC-900":
		In_house_engineering = F20

	if var_4 == "Performance CD Open Version 2 or older" or var_4 == "MXOpen" or var_4 == "Other":
		In_house_engineering += F21

	In_house_engineering += F22 if(var_5 == "MODBUS RTU (Requires Serial Communication Parameters)") else 0
	#Trace.Write( In_house_engineering )

	#Site Installation
	Site_Installation = 0
	if var_2 == "Intelligent Actuator" :
		Site_Installation = 64

	if(var_1 <= 60 and var_2 == "Non-Intelligent Actuator"):
		Site_Installation = 64
	if((var_1 > 60 and var_1 <=100) and var_2 == "Non-Intelligent Actuator"):
		Site_Installation = 80
	if((var_1 > 100 and var_1 <=256) and var_2 == "Non-Intelligent Actuator"):
		 Site_Installation = 100
	#Trace.Write(Site_Installation )

	SAT = 8 if var_8 == "Yes" else 0
	return Additional_Docs,In_house_engineering,Site_Installation,SAT

def getFSCTOSMIOLabourHours(Product):
	
	var_1 = getFloat(getAttrValue(Product,'ATT_FSCtoSMIOMigrationTotalFSC'))
	
	var_2 = 0
	var_3 = 0
	var_8=0
	for16=0
	for4 =0
	for8 =0
	for2 = 0
	for12 = 0
	for10=0
	for3=0
	con1 = getContainer(Product,'FSC_to_SM_IO_Series_1_&_2_FSC_IO_configurations')
	for row in con1.Rows:
		red = getFloat(row['FSC_to_SM_IO_Number_of_IO_Racks'])
		non_red = getFloat(row['NON_RED_FSC_to_SM_IO_Number_of_IO_Racks'])
		var_2 += red
		var_3 += non_red
		no_of_io_racks = red + non_red
		if no_of_io_racks >6:
			var_8 +=1

		for16 += (getFloat(row['FSC_to_SM_IO_DI_24VDC'])+ getFloat(row['NON_RED_FSC_to_SM_IO_DI_24VDC']))
		for16 += (getFloat(row['FSC_to_SM_IO_DI_60VDC'])+ getFloat(row['NON_RED_FSC_to_SM_IO_DI_60VDC']))
		for16 += (getFloat(row['FSC_to_SM_IO_DI_48VDC'])+ getFloat(row['NON_RED_FSC_to_SM_IO_DI_48VDC']))
		for16 += (getFloat(row['FSC_to_SM_IO_DI_24VDC_10104/1/1'])+ getFloat(row['NON_RED_FSC_to_SM_IO_DI_24VDC_10104/1/1']))
		for16 += (getFloat(row['FSC_to_SM_IO_DO_24VDC_10209/1/1'])+ getFloat(row['NON_RED_FSC_to_SM_IO_DO_24VDC_10209/1/1']))
		for16 += (getFloat(row['FSC_to_SM_IO_SDI_24VDC'])+ getFloat(row['NON_RED_FSC_to_SM_IO_SDI_24VDC']))
		for16 += (getFloat(row['FSC_to_SM_IO_SDI_60VDC_10101/2/2'])+ getFloat(row['NON_RED_FSC_to_SM_IO_SDI_60VDC_10101/2/2']))
		for16 += (getFloat(row['FSC_to_SM_IO_SDI_48VDC_10101/2/3'])+ getFloat(row['NON_RED_FSC_to_SM_IO_SDI_48VDC_10101/2/3']))
		for16 += (getFloat(row['FSC_to_SM_IO_DI_24VDC_10104/2/1'])+ getFloat(row['NON_RED_FSC_to_SM_IO_DI_24VDC_10104/2/1']))
		for16 += (getFloat(row['FSC_to_SM_IO_AI_10105/2/1'])+ getFloat(row['NON_RED_FSC_to_SM_IO_AI_10105/2/1']))
		for16 += (getFloat(row['FSC_to_SM_IO_SDIL_10106/2/1'])+ getFloat(row['NON_RED_FSC_to_SM_IO_SDIL_10106/2/1']))
		for16 += (getFloat(row['FSC_to_SM_IO_DO_24VDC_10209/2/1'])+ getFloat(row['NON_RED_FSC_to_SM_IO_DO_24VDC_10209/2/1']))

		for4 += (getFloat(row['FSC_to_SM_IO_AI_4_20mA'])+ getFloat(row['NON_RED_FSC_to_SM_IO_AI_4_20mA']))
		for4 += (getFloat(row['FSC_to_SM_IO_DI_IS_(Eex(i))'])+ getFloat(row['NON_RED_FSC_to_SM_IO_DI_IS_(Eex(i))']))
		for4 += (getFloat(row['FSC_to_SM_IO_DI_IS_(Eex(ii))'])+ getFloat(row['NON_RED_FSC_to_SM_IO_DI_IS_(Eex(ii))']))
		for4 += (getFloat(row['FSC_to_SM_IO_FDO_DS_24VDC_10203/1/1'])+ getFloat(row['NON_RED_FSC_to_SM_IO_FDO_DS_24VDC_10203/1/1']))
		for4 += (getFloat(row['FSC_to_SM_IO_FDO_DS_24VDC_10203/1/2'])+ getFloat(row['NON_RED_FSC_to_SM_IO_FDO_DS_24VDC_10203/1/2']))
		for4 += (getFloat(row['FSC_to_SM_IO_DO_110VDC_10213/1/1'])+ getFloat(row['NON_RED_FSC_to_SM_IO_DO_110VDC_10213/1/1']))
		for4 += (getFloat(row['FSC_to_SM_IO_SDO_60VDC_10213/1/2'])+ getFloat(row['NON_RED_FSC_to_SM_IO_SDO_60VDC_10213/1/2']))
		for4 += (getFloat(row['FSC_to_SM_IO_SD_ 48VDC_10213/1/3'])+ getFloat(row['NON_RED_FSC_to_SM_IO_SD_ 48VDC_10213/1/3']))
		for4 += (getFloat(row['FSC_to_SM_IO_SDO_24VDC_10215/1/1'])+ getFloat(row['NON_RED_FSC_to_SM_IO_SDO_24VDC_10215/1/1']))
		for4 += (getFloat(row['FSC_to_SM_IO_SDOL_24VDC_10216/1/1'])+ getFloat(row['NON_RED_FSC_to_SM_IO_SDOL_24VDC_10216/1/1']))
		for4 += (getFloat(row['FSC_to_SM_IO_SAI_10102/2/1'])+ getFloat(row['NON_RED_FSC_to_SM_IO_SAI_10102/2/1']))
		for4 += (getFloat(row['FSC_to_SM_IO_SDO_110VDC_10213/2/1'])+ getFloat(row['NON_RED_FSC_to_SM_IO_SDO_110VDC_10213/2/1']))
		for4 += (getFloat(row['FSC_to_SM_IO_SDO_60VDC_10213/2/2'])+ getFloat(row['NON_RED_FSC_to_SM_IO_SDO_60VDC_10213/2/2']))
		for4 += (getFloat(row['FSC_to_SM_IO_SDO_48VDC_10213/2/3'])+ getFloat(row['NON_RED_FSC_to_SM_IO_SDO_48VDC_10213/2/3']))
		for4 += (getFloat(row['FSC_to_SM_IO_SDO_24VDC_10215/2/1'])+ getFloat(row['NON_RED_FSC_to_SM_IO_SDO_24VDC_10215/2/1']))
		for4 += (getFloat(row['FSC_to_SM_IO_SDOL_24VDC_10216/2/1'])+ getFloat(row['NON_RED_FSC_to_SM_IO_SDOL_24VDC_10216/2/1']))
		for4 += (getFloat(row['FSC_to_SM_IO_SDOL_48VDC_10216/2/3'])+ getFloat(row['NON_RED_FSC_to_SM_IO_SDOL_48VDC_10216/2/3']))

		for8 += (getFloat(row['FSC_to_SM_IO_DO 24VDC_10201/1/1'])+ getFloat(row['NON_RED_FSC_to_SM_IO_DO 24VDC_10201/1/1']))
		for8 += (getFloat(row['FSC_to_SM_IO_DO_IS_10207/1/1'])+ getFloat(row['NON_RED_FSC_to_SM_IO_DO_IS_10207/1/1']))
		for8 += (getFloat(row['FSC_to_SM_IO_DO_24VDC_10212/1/1'])+ getFloat(row['NON_RED_FSC_to_SM_IO_DO_24VDC_10212/1/1']))
		for8 += (getFloat(row['FSC_to_SM_IO_SDO_24VDC_10201/2/1'])+ getFloat(row['NON_RED_FSC_to_SM_IO_SDO_24VDC_10201/2/1']))

		for2 += (getFloat(row['FSC_to_SM_IO_AO_4-20mA_10205/1/1'])+ getFloat(row['NON_RED_FSC_to_SM_IO_AO_4-20mA_10205/1/1']))
		for2 += (getFloat(row['FSC_to_SM_IO_SAO_10205/2/1'])+ getFloat(row['NON_RED_FSC_to_SM_IO_SAO_10205/2/1']))
		
		for12 += (getFloat(row['FSC_to_SM_IO_DO_24VDC_10206/1/1'])+ getFloat(row['NON_RED_FSC_to_SM_IO_DO_24VDC_10206/1/1']))
		for12 += (getFloat(row['FSC_to_SM_IO_DO_24VDC_10206/2/1'])+ getFloat(row['NON_RED_FSC_to_SM_IO_DO_24VDC_10206/2/1']))
		
		for10 += (getFloat(row['FSC_to_SM_IO_RO_10208/1/1'])+ getFloat(row['NON_RED_FSC_to_SM_IO_RO_10208/1/1']))
		for10 += (getFloat(row['FSC_to_SM_IO_RO_10208/2/1'])+ getFloat(row['NON_RED_FSC_to_SM_IO_RO_10208/2/1']))
		
		for3 += (getFloat(row['FSC_to_SM_IO_SDOL 220VDC_10214/1/2'])+ getFloat(row['NON_RED_FSC_to_SM_IO_SDOL 220VDC_10214/1/2']))
		for3 += (getFloat(row['FSC_to_SM_IO_SDOL_220VDC_10214/2/2'])+ getFloat(row['NON_RED_FSC_to_SM_IO_SDOL_220VDC_10214/2/2']))

	var_5 = ((for16 *16.00)+(for4 *4.00)+(for8 *8.00)+(for2*2.00)+(for12*12.00)+(for10*10.00)+(for3 *3.00))
	Trace.Write("test22::")
	

	#con2 = getContainer(Product,'FSC_to_SM_IO_Services2')
	#con2row = con2.Rows[0]
	var_6 = getFloat(getAttrValue(Product,'ATT_FSC_to_SM_IO_In_Office_Eng_hours'))
	var_7 = getFloat(getAttrValue(Product,'ATT_FSC_to_SM_IO_On_Site_Eng_hours'))
	
	#con3 = getContainer(Product,'FSC_to_SM_IO_Services')
	#con3row = con3.Rows[0]
	var_4 = getAttrValue(Product,'FSC_to_SM_IO_Is_Honeywell_executing_the_field_cros')
	var_12 = getAttrValue(Product,'FSC_to_SM_IO_Software_Factory_Acceptance_Test_Requ')
	ranm = getAttrValue(Product,'FSC_to_SM_IO_Has_the_FSC_IO_Audit_been_performed')
	if ranm == "No":
		var_9 = "Yes"
	else:
		var_9= "No"
	
	#Calculation
	inhouse_prepost_engineering = var_8 * 40.00 + (var_1 - var_8) * 32.00

	safety_audit = (var_8 * 24.00 + (var_1 - var_8) * 16.00) if var_9 == "Yes" else 0

	documentation = var_8 * 40.00 + (var_1 - var_8) * 24.00
	
	inhouse_Eng = m.ceil((32.00 + (var_2 + var_3) * 6.00 + var_5 * 0.40 + var_6)/8.00)
	inhouse_Engineering = inhouse_Eng * 8.00

	software_fat = var_1 * 8.00 + (var_8*32.00) + (var_1 - var_8) * 16.00 if var_12 =="Yes" else 0

	'''onsite_io_migration = 24.00 + (var_2 + var_3) * 4.00
	onsite_io_migration += var_5 * 0.0664 
	onsite_io_migration += var_5 *0.1336 if var_4 == "Yes" else 0
	onsite_io_migration += m.ceil(onsite_io_migration/8.00) * 8.00
	onsite_io_migration += m.ceil(var_7/8.00) * 8.00'''
	
	onsite_io_migration_part1 = (var_5*0.1336) if var_4=="Yes" else 0
	onsite_io_migration_part1 += (var_5*0.0664)
	onsite_io_migration_part1 = (m.ceil(onsite_io_migration_part1/8.00))*8.00
	onsite_io_migration = 24.00+ ((var_2+var_3)*4.00) + onsite_io_migration_part1 + (m.ceil(var_7/8.00))*8

	sat = var_1 * 16.00
	return inhouse_prepost_engineering , safety_audit , documentation , inhouse_Engineering, software_fat ,onsite_io_migration, sat

def getCWSRAEMigrationLabourHours(Product):
	var_1 = Product.Attr('CWS_Mig_Current_Release_on_System').GetValue()
	var_2 = Product.Attr('CWS_Mig_Site_Acceptance_Test_Required').GetValue()
	var_3 = Product.Attr('CWS_Mig_HSE_and_Quality_Plan').GetValue()
	var_4 = Product.Attr('CWS_Mig_Update_existing_documents').GetValue()
	var_5 = getFloat(Product.Attr('CWS_Mig_MXProLine_desktop_server').GetValue())
	var_6 = Product.Attr('CWS_Mig_Migration_performed_by_PEC_using_Honeywell_Migration_Assistant').GetValue()
	var_7 = Product.Attr('CWS_Mig_Customization_to_be_migrated').GetValue()
	var_8 = Product.Attr('CWS_Mig_Is_the_DRG_file_16_DRG_or_earlier').GetValue()
	var_9 = getFloat(Product.Attr('CWS_Mig_Total_number_of_HC900_IO_points').GetValue())
	var_10 = Product.Attr('CWS_Mig_For_MD_CD_work_are_we_doing_installation').GetValue()
	var_11 = getFloat(Product.Attr('CWS_Mig_Number_of_die_bolts').GetValue())
	var_12 = Product.Attr('CWS_Mig_Is_there_existing_Machine_Direction_Contro').GetValue()
	var_13 = Product.Attr('CWS_Mig_Is_there_existing_Cross_Directional_Contro').GetValue()
	F27 = 40.0
	F28 = 40.0
	#Plan_Review_KOM = 8
	#SW_HW order = 4
	#=IF(var_3="Yes",4,0)+IF(var_4="Yes",4,0)
	additional_docs = (4.0 if(var_3 == "Yes") else 0.0) + (4.0 if(var_4 == "Yes") else 0.0)
	#migration_doc = 8
	#F23=IF(var_7="None",0, IF(var_7="Low",24, IF(var_7="Med",40, IF(var_7="High",56))))
	F23= 0.0 if(var_7 == "") else (24.0 if(var_7 =="Low") else (40.0 if(var_7 == "Medium") else (56.0 if(var_7=="High") else 0.0)))
	#F24 =IF(var_7="None",0, IF(var_7="Low",24, IF(var_7="Med",40, IF(var_7="High",56))))+IF(AND(var_1="RAE 2 or Less", var_8="Yes"),40)
	F24 = (0.0 if(var_7 == "") else (24.0 if(var_7 =="Low") else (40.0 if(var_7 == "Medium") else (56.0 if(var_7=="High") else 0.0)))) + (40.0 if(var_1 == "RAE 2 or Less" and var_8 == "Yes") else 0.0)
	F26 = var_5 * 4.0
	#=IF(var_1="RAE 3 or Later",F23,0)+IF(var_1="RAE 2 or Less",F24,0)+(IF(var_6="NO",F26,0))
	in_house_engineering = (F23 if(var_1 == "RAE 3 or Later") else 0.0) + (F24 if(var_1 == "RAE 2 or Less") else 0.0) #+ (F26 if(var_6 == "No") else 0.0)
	site_installation = (3+var_5)*8.0
	if var_9 > 0.0 :
		if var_10 == "Installation Supervision":
			site_installation += (1 * var_9)/3
		else:
			site_installation += (2 * var_9)/3
	else:
		site_installation += 0.0
	if var_11 > 0.0 :
		if var_10 == "Installation Supervision":
			site_installation += (1 * var_11)/3
		else:
			site_installation += (2 * var_11)/3
	else:
		site_installation = 0.0
	Server_Station_Build = var_5 *4.0
	SAT = 8.0 if(var_2 == "Yes") else 0.0
	MD_CD_Configuration = (F27 if(var_12 == "Yes") else 0.0) + (F28 if(var_13 == "Yes") else 0.0)
	return additional_docs, site_installation, SAT, in_house_engineering, Server_Station_Build,MD_CD_Configuration