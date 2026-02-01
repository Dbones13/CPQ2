def getContainer(Product,Name):
	return Product.GetContainerByName(Name)

def getRowData(Product,container,column):
	Container = getContainer(Product,container)
	for row in Container.Rows:
		return row[column]

def getRowDataIndex(Product,container,column,index):
	Container = getContainer(Product,container)
	for row in Container.Rows:
		if row.RowIndex == index:
			return row[column]

def getFloat(Var):
	if Var:
		return float(Var)
	return 0
def getAttrData(Product,Name):
	return Product.Attr(Name).GetValue()
	
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
		Trace.Write("oldCalHrs"+str(oldCalHrs)+"calculated"+str(row["Calculated_Hrs"]))
		return "1"
	else:
		return row["Adjustment_Productivity"]

def getEHPMHARTIOLabourHours(Product,msid_product):

	parameters = {"EHPM_HART_IO_General_Qns_Cont":{"var_1":"Current_Experion_Release","var_3":"Number_of_EHPM_integration_licenses_needed"},"EHPM_HART_IO_Configuration_Cont":{"var_5_1":"Number_of_Non_Redundant_HART_HLAI","var_5_2":"Number_of_Redundant_Hart_HLAI","var_5_3":"Number_of_Non-Red_IOP&Red_FTA_HART_HLA","var_6_1":"Number_of_Non-Redundant_HART_AO_8points","var_6_2":"Number_of_Redundant_HART_AO_8points","var_7_1":"Number_of_Non-Redundan_ HART_AO_16points","var_7_2":"Number_of_Redundant_HART_AO_16points"},"EHPM_HART_IO_Services_Cont":{"var_2":"EHPM_HART_IO_WBI","var_4":"EHPM_HART_IO_Wiring_termination_type","var_9":"EHPM_HART_IO_Will_Honeywell_equipment_activities","var_12":"EHPM_HART_IO_Commissioning_required?","var_13":"EHPM_HART_IO_NES"},"MSID_CommonQuestions":{"var_10":"EHPM_HART_IO_Construction_Work_Package_doc_require"}}

	#var_11
	var_11 = "No"
	selectedDocument=Product.Attr('EHPM_HART_IO_Which_documentation_is_required?').SelectedValues
	for document in selectedDocument:
		if document.UserInput =='Make or update a drawing package required':
			var_11 = "Yes"

	for key in parameters:
		if key == "MSID_CommonQuestions":
			var_10 = getAttrData(msid_product,parameters[key]["var_10"])
		elif key == "EHPM_HART_IO_Services_Cont":
			var_2 = getAttrData(Product,parameters[key]["var_2"])
			var_12 = getAttrData(Product,parameters[key]["var_12"])
			var_4 = getAttrData(Product,parameters[key]["var_4"])
			var_9 = getAttrData(Product,parameters[key]["var_9"])
			var_13 = getAttrData(Product,parameters[key]["var_13"])
		elif key == "EHPM_HART_IO_Configuration_Cont":
			#Total HLAI IOM
			var_5= getFloat(getRowDataIndex(Product,key,parameters[key]["var_5_1"],0)) + getFloat(getRowDataIndex(Product,key,parameters[key]["var_5_1"],2)) + getFloat(getRowDataIndex(Product,key,parameters[key]["var_5_2"],0)) + getFloat(getRowDataIndex(Product,key,parameters[key]["var_5_2"],2)) + getFloat(getRowDataIndex(Product,key,parameters[key]["var_5_3"],0)) + getFloat(getRowDataIndex(Product,key,parameters[key]["var_5_3"],2))
			#Total 8pt
			var_6 = getFloat(getRowDataIndex(Product,key,parameters[key]["var_6_1"],0)) + getFloat(getRowDataIndex(Product,key,parameters[key]["var_6_1"],2)) + getFloat(getRowDataIndex(Product,key,parameters[key]["var_6_2"],0)) + getFloat(getRowDataIndex(Product,key,parameters[key]["var_6_2"],2))
			#Total 16pt
			var_7 = getFloat(getRowDataIndex(Product,key,parameters[key]["var_7_1"],0)) + getFloat(getRowDataIndex(Product,key,parameters[key]["var_7_1"],2)) + getFloat(getRowDataIndex(Product,key,parameters[key]["var_7_2"],0)) + getFloat(getRowDataIndex(Product,key,parameters[key]["var_7_2"],2))
			#Total IOM with licenses
			var_8 = getFloat(getRowDataIndex(Product,key,parameters[key]["var_5_1"],2)) + getFloat(getRowDataIndex(Product,key,parameters[key]["var_5_2"],2)) + getFloat(getRowDataIndex(Product,key,parameters[key]["var_5_3"],2)) + getFloat(getRowDataIndex(Product,key,parameters[key]["var_6_1"],2)) + getFloat(getRowDataIndex(Product,key,parameters[key]["var_6_2"],2)) + getFloat(getRowDataIndex(Product,key,parameters[key]["var_7_1"],2)) + getFloat(getRowDataIndex(Product,key,parameters[key]["var_7_2"],2))
		elif key == "EHPM_HART_IO_General_Qns_Cont":
			var_1 = getRowData(Product,key,parameters[key]["var_1"])
			var_3 = getRowData(Product,key,parameters[key]["var_3"])
	#Documentation Calculation
	documentation = 16 if var_10 == "Yes" else 0
	documentation += getFloat(var_2)* 6 if var_11 == "Yes" else 0

	#Commission Calculation
	commissioning = (var_5 + var_6 + var_7)*0.5 if var_12 == "Yes" else 0

	#site installation Calculation
	#part 1 : IF(var_1="Less than R511.4",1*var_13,0)
	siteInstallation = getFloat(var_13) if (var_1 == "Less_than_R511.4" or var_1 == "") else 0
	#part 2 : +0.05*F39
	siteInstallation += (var_5 + var_6 + var_7)*0.05
	#part 3 : +0.5*var_3
	siteInstallation += getFloat(var_3)*0.5
	#part 4: +0.17*(var_2-var_3)
	siteInstallation += 0.17*(getFloat(var_2) - getFloat(var_3))
	#part 5: +0.12*var_8
	siteInstallation += 0.12*var_8
	#part 6: IF(var_9="Yes",(0.07*F39+0.25*F39+compressionFactor),0)
	#Compression calculation: IF(var_4="Compression",0.17*F39,0.12*((var_5+var_7)*16)+0.12*(var_6*8))
	if var_4 == "Compression" or var_4 == "":
		compressionFactor = 0.17* (var_5 + var_6 + var_7)
	else:
		compressionFactor = 0.12*((var_5+var_7)*16) + 0.12*(var_6*8)
	siteInstallation += (0.07*(var_5 + var_6 + var_7) +0.25* (var_5 + var_6 + var_7) +compressionFactor) if var_9 == "Yes" else 0
	return documentation, commissioning, siteInstallation

def getC200MigrationLabourHours(Product,msid_product):
	migrationScenario = Product.Attr('C200_Select_Migration_Scenario').GetValue()
	#for row in migrationScenarioCon:
		#migrationScenario = row['C200_Select_the_Migration_Scenario']
		#break
	if migrationScenario == 'C200 to ControlEdge UOC':
		try:
			TK_FXX102 = 0
			CC_C8DS01 = 0
			CC_C8SS01 = 0

			c200PartCont = msid_product.GetContainerByName('MSID_C200_Migration_Added_Parts_Common_Container').Rows
			for row in c200PartCont:
				if row['PartNumber']== 'TK-FXX102':
					TK_FXX102 = row['Quantity']
				if row['PartNumber'] == 'CC-C8DS01':
					CC_C8DS01 = row['Quantity']
				if row['PartNumber'] == 'CC-C8SS01':
					CC_C8SS01 = row['Quantity']

		except:
			Trace.Write("Error in C200 Part Container ")

		var_4 = getFloat(TK_FXX102)
		var_9 = getFloat(eval(Product.Attr('Temporary Data').GetValue())['C200_UOC_var_9'])
		#var_9 = 0

		container = Product.GetContainerByName('C200_Migration_Config_Cont')
		count = 0
		peerCount= 0
		for i in container.Rows:
			for j in i.Columns :
				if j.Name=="C200_located_separated_from_0thers_remote_location":
					if j.Value=='Yes':
						count = count +1
				if j.Name=="C200_peer_to_peer_communication":
					p=  j.Value
					if j.Value and j.Value != 'None'   :
						peerCount = peerCount +1
		var_5 =getFloat(count)
		var_7 =getFloat(peerCount)
		var_3 =  0
		var_10 = 0
		var_11 = 0

		parameters = {"C200_Migration_General_Qns_Cont":{"var_1":"C200_How_many_C200s_are_we_migrating","var_2":"C200_How_many_C200s_are_we_migrating","var_6":"C200_Connection _to_Experion_Server", "var_8":"C200_Type_of_downlink_communication_UOC"},"C200_Migration_Config_Cont":{"var_3":"C200_UOC_Number_of_Series_A_IO_Racks","var_10":"C200_Number_of_Serial_Interface_IOMs","var_11":"C200_Number_of_Serial_Interface_points"},"C200_Services_1_Cont":{"var_17":"C200_Documentation_Required","var_12":"C200_additional_hrs_ins","var_16":"C200_Data_Gathering_Required"},"MSID_CommonQuestions":{"var_14":"MSID_Is_Switch_Configuration_in_Honeywell_Scope","var_13":"MSID_Is_FTE_based_System_already_installed_on_Site"},"C200_Services_2_Cont":{"var_18":"C200_Factory_Acceptance_Test_Required","var_15":"C200_Will_Honeywell_perform_equipment_installation"}}



		for key in parameters:
			if key == "C200_Migration_General_Qns_Cont":
				for row in getContainer(Product,key).Rows:
					var_8 =  getRowData(Product,key,parameters[key]["var_8"])
					if var_8=="E/IP" or( not var_8):
						var_8 = "E/IP"
					elif var_8 =="CNET Non-Redundant" or var_8 =="CNET Redundant":
						var_8 = "CNET"
					var_1 = getFloat(getRowData(Product,key,parameters[key]["var_1"]))
					var_2 = getFloat(getRowData(Product,key,parameters[key]["var_2"]))
					var_6 =  getRowData(Product,key,parameters[key]["var_6"])
					if var_6 in [ "Dual Ethernet" , "Single Ethernet","ControlNet"]:
						var_6 = 'CNI'
					elif var_6 == 'FTE' or var_6 == '':
						var_6 = 'FTE'

			if key == "C200_Migration_Config_Cont":
				var_3 = 0
				var_10 = 0
				var_11 = 0
				for row in getContainer(Product,key).Rows:
					var_3 +=   getFloat(getFloat(row[parameters[key]["var_3"]]))
					var_10 +=  getFloat(row[parameters[key]["var_10"]])
					var_11 +=  getFloat(row[parameters[key]["var_11"]])

			if key == "C200_Services_1_Cont":
				var_17=  getAttrData(Product,parameters[key]["var_17"])
				var_12 =  getFloat(getAttrData(Product,parameters[key]["var_12"]))
				var_16 =  getAttrData(Product,parameters[key]["var_16"])

			if key == "MSID_CommonQuestions":
				var_13 =  getAttrData(msid_product,parameters[key]["var_13"]) if getAttrData(msid_product,parameters[key]["var_13"]) else 'Yes'
				var_14 = getAttrData(msid_product,parameters[key]["var_14"]) if getAttrData(msid_product,parameters[key]["var_14"]) else 'Yes'

			if key == "C200_Services_2_Cont":
				var_18 =  getAttrData(Product,parameters[key]["var_18"]) if getAttrData(Product,parameters[key]["var_18"]) else 'No'
				var_15 = getAttrData(Product,parameters[key]["var_15"]) if getAttrData(Product,parameters[key]["var_15"]) else 'No'


		#Calculations
		felSiteDataGathering =  24 if var_16 =='Yes' else 0

		migrationDocumentation = 0 if var_17 =="No" else (24+( var_1 -1)*1)
		migrationDocumentation +=0 if var_17 =="No" else (var_10 *30.00/50.00)
		migrationDocumentation +=0 if var_17 =="No" else (1 if var_8=="CNET" else 0)+ (1 if var_8 =="E/IP" else 0)
		migrationDocumentation +=0 if var_17=="No" else 6
		migrationDocumentation +=40 if var_17=="DDS & Network Drawing" else 0


		inHouseEngineering = 2 if var_18 =="Yes" else 0
		inHouseEngineering += (0 if(var_8)=="CNET" else 15.00/60.00*var_1) if (var_18=="Yes") else 0
		inHouseEngineering += (15.00/60.00*var_1 if (var_8=="E/IP") else 0) if (var_18=="Yes") else 0
		inHouseEngineering += 1*var_1 if (var_18=="Yes") else 0
		inHouseEngineering += (var_7*6.00/60.00) if(var_18=="Yes") else 0
		inHouseEngineering += (var_11*6.00/60.00)if(var_18=="Yes") else 0

		preFAT = (8+(var_1-1)*1) if(var_18=="Yes") else 0
		preFAT += (var_1*4) if(var_18=="Yes") else 0
		preFAT += 8 if(var_18=="Yes") else 0
		preFAT += (var_1*1) if(var_18=="Yes") else 0

		fat = (8+(var_1-1)*2) if(var_18=="Yes") else 0

		siteInstallationEaps = var_10*1
		siteInstallationEaps += var_10*15.00/60.00
		siteInstallationEaps += var_10*15.00/60.00
		siteInstallationEaps +=var_10*1
		siteInstallationEaps += var_10*30.00/60.00
		siteInstallationEaps += var_11*9.00/60.00
		siteInstallationEaps += var_11*15.00/60.00
		siteInstallationEaps += 2
		siteInstallationEaps += var_1*1
		siteInstallationEaps += var_7 *2
		siteInstallationEaps += var_11*6/60
		siteInstallationEaps += 24 if(var_13=="No")else 0
		siteInstallationEaps += 24
		siteInstallationEaps += 24 if(var_6=="CNI") else 0
		siteInstallationEaps += var_12
		siteInstallationEaps += 2 if(var_14=="Yes") else 0

		sat = 8+(var_1-1)*8
		sat += 8 + 4

		siteInstallationEST1 = 1 if(var_15=="No" )else 0
		siteInstallationEST1 += ((var_3+var_4)*15.00/60.00 if(var_8=="E/IP") else 0) if(var_15=="Yes") else 0
		siteInstallationEST1 += ((var_3+var_4)*15.00/60.00 if(var_8=="E/IP") else 0) if(var_15=="Yes" ) else 0
		siteInstallationEST1 += var_1*1 if(var_15=="Yes") else 0
		siteInstallationEST1 += var_2*30.00/60.00 if(var_15=="Yes") else 0
		siteInstallationEST1 += var_2*30/60 if(var_15=="Yes") else 0
		siteInstallationEST1 += ((var_3+var_4)*30.00/60.00 if(var_8)=="CNET" else 0) if(var_15=="Yes") else 0
		siteInstallationEST1 += ((var_3+var_4)*15.00/60.00 if(var_8=="CNET") else 0) if(var_15=="Yes") else 0
		siteInstallationEST1 += ((var_3+var_4)*1 if(var_8=="CNET") else 0) if(var_15=="Yes") else 0
		siteInstallationEST1 += ((var_3+var_4)*30.00/60.00 if(var_8=="CNET") else 0) if(var_15=="Yes") else 0
		siteInstallationEST1 += ((var_3+var_4)*30.00/60.00 if(var_8=="CNET") else 0) if(var_15=="Yes") else 0
		siteInstallationEST1 += var_1*15.00/60.00 if(var_15=="Yes") else 0
		siteInstallationEST1 += var_1*15.00/60.00 if(var_15=="Yes") else 0
		siteInstallationEST1 += (var_1*30.00/60.00 if(var_8=="CNET") else 0) if(var_15=="Yes") else 0
		siteInstallationEST1 += var_4 *2 if(var_15=="Yes" ) else 0
		siteInstallationEST1 += var_9 *4 if(var_15=="Yes") else 0
		siteInstallationEST1 += var_5*30.00/60.00 if(var_15=="Yes") else 0
		siteInstallationEST1 += var_5*30/60 if(var_15=="Yes") else 0
		siteInstallationEST1 += var_5*1 if(var_15=="Yes" )else 0
		siteInstallationEST1 += var_5*30.00/60.00 if(var_15=="Yes") else 0
		siteInstallationEST1 += var_10 *15.00/60.00 if(var_15=="Yes") else 0
		siteInstallationEST1 += var_10*30.00/60.00 if(var_15=="Yes") else 0
		siteInstallationEST1 += var_10*15.00/60.00 if(var_15=="Yes") else 0
		siteInstallationEST1 += var_10*15.00/60.00 if(var_15=="Yes") else 0
		siteInstallationEST1 += var_10*9.00/60.00 if(var_15=="Yes") else 0
		siteInstallationEST1 += var_10*1 if(var_15=="Yes") else 0
		siteInstallationEST1 += var_10*1 if(var_15=="Yes") else 0

		return felSiteDataGathering,migrationDocumentation,inHouseEngineering,preFAT,fat,siteInstallationEaps,sat,siteInstallationEST1

	elif migrationScenario in ('C200 to C300',''):
		try:
			CC_ZHR041 = 0
			TK_FXX102 = 0
			CC_C8DS01 = 0
			CC_C8SS01 = 0
			TK_FTEB01 = 0
			CC_TCF901 = 0
			CC_CBDD01 = 0
			CC_CBDS01 = 0
			c200PartCont = msid_product.GetContainerByName('MSID_C200_Migration_Added_Parts_Common_Container').Rows
			for row in c200PartCont:
				if row['PartNumber']== 'CC-ZHR041':
					CC_ZHR041 = row['Quantity']
				if row['PartNumber'] == 'TK-FXX102':
					TK_FXX102 = row['Quantity']
				if row['PartNumber'] == 'CC-C8DS01':
					CC_C8DS01 = row['Quantity']
				if row['PartNumber'] == 'CC-C8SS01':
					CC_C8SS01 = row['Quantity']
				if row['PartNumber'] == 'TK-FTEB01':
					TK_FTEB01 = row['Quantity']
				if row['PartNumber'] == 'CC-TCF901':
					CC_TCF901 = row['Quantity']
				if row['PartNumber'] == 'CC-CBDD01':
					CC_CBDD01 = row['Quantity']
				if row['PartNumber'] == 'CC-CBDS01':
					CC_CBDS01 = row['Quantity']
		except:
			Trace.Write("Error in C200 Part Container ")
		var_1 = getFloat(CC_ZHR041)
		var_4 = getFloat(TK_FXX102)
		var_5 = getFloat(CC_C8DS01) + getFloat(CC_C8SS01)+ getFloat(CC_CBDD01) + getFloat(CC_CBDS01)
		var_6 = getFloat(TK_FTEB01)
		var_9 = getFloat(CC_TCF901)
		var_11 = eval(Product.Attr('Temporary Data').GetValue())['C300_var_11']
		#var_11 = 0
		var_2 = eval(Product.Attr('Temporary Data').GetValue())['C300_var_2']
		#var_2 = 0

		parameters = {"C200_Migration_General_Qns_Cont":{"var_25":"C200_Number_of_additional_switches","var_2":"C200_How_many_C200s_are_we_migrating","var_3":"C200_How_many_C200s_are_we_migrating","var_8":"C200_Connection _to_Experion_Server"},"C200_Migration_Config_Cont":{"var_16":"C200_C300_Number_of_Pulse_Input_IOMs","var_17_1":"C200_Number_of_Non-Redundant_FIM2_IOMs","var_17_2":"C200_Number_of_Redundant_FIM2_IOMs_to_FIM4_conversion","var_17_3":"C200_Number_of_Redundant_FIM2_IOMs_to_FIM8_conversion","var_18":"C200_Number_of_Profibus_IOMs","var_7":"C200_Number_of_Remote_Series_A_IO_Racks","var_12":"C200_Number_of_Serial_Interface_Allen_Bradley_IOMs","var_13":"C200_Number_of_Serial_Interface_Allen_Bradley_points","var_14":"C200_Number_of_Serial_Interface_Modbus_IOMs","var_15":"C200_Number_of_Serial_Interface_Modbus_points","var_16":"C200_C300_Number_of_Pulse_Input_IOMs","var_18":"C200_Number_of_Profibus_IOMs","":"","":"","":""},"C200_Services_1_Cont":{"var_22":"C200_Data_Gathering_Required","var_23":"C200_Documentation_Required"},"C200_Services_2_Cont":{"var_24":"C200_Factory_Acceptance_Test_Required","var_20":"C200_Will_Honeywell_Perform_Equipment_Installation"},"MSID_CommonQuestions":{"var_21":"MSID_Is_Switch_Configuration_in_Honeywell_Scope","var_19":"MSID_Is_FTE_based_System_already_installed_on_Site"}}

		for key in parameters:

			if key == "C200_Migration_General_Qns_Cont":
				var_3 = 0
				var_8 = 0
				var_25 = 0
				for row in getContainer(Product,key).Rows:
					var_3 = getFloat(getRowData(Product,key,parameters[key]["var_3"]))
					var_8 = getRowData(Product,key,parameters[key]["var_8"])
					var_25 = getFloat(getRowData(Product,key,parameters[key]["var_25"]))


			if key == "C200_Migration_Config_Cont":
				var_16 = 0
				var_17 = 0
				var_18 = 0
				var_12 = 0
				var_14 = 0
				var_7  = 0
				var_15 = 0
				var_13 = 0
				for row in getContainer(Product,key).Rows:
					var_16 +=   getFloat(getFloat(row[parameters[key]["var_16"]]))
					var_17 +=  getFloat(row[parameters[key]["var_17_1"]]) + getFloat(row[parameters[key]["var_17_2"]]) + getFloat(row[parameters[key]["var_17_3"]])
					var_18 +=  getFloat(row[parameters[key]["var_18"]])
					var_12 += getFloat(row[parameters[key]["var_12"]])
					var_14 += getFloat(row[parameters[key]["var_14"]])
					var_7  += getFloat(row[parameters[key]["var_7"]])
					var_15 += getFloat(row[parameters[key]["var_15"]])
					var_13 += getFloat(row[parameters[key]["var_13"]])

			if key == "C200_Services_1_Cont":
				var_22=  getAttrData(Product,parameters[key]["var_22"])
				var_23 =  getAttrData(Product,parameters[key]["var_23"])

			if key == "MSID_CommonQuestions":
				var_19 =  getAttrData(msid_product,parameters[key]["var_19"]) if getAttrData(msid_product,parameters[key]["var_19"]) else 'Yes'
				var_21 = getAttrData(msid_product,parameters[key]["var_21"]) if getAttrData(msid_product,parameters[key]["var_21"]) else 'Yes'

			if key == "C200_Services_2_Cont":
				var_24 =  getAttrData(Product,parameters[key]["var_24"]) if getAttrData(Product,parameters[key]["var_24"]) else 'No'
				var_20 = getAttrData(Product,parameters[key]["var_20"]) if getAttrData(Product,parameters[key]["var_20"]) else 'No'

		#Calculations
		felSiteDataGathering =  24 if var_22 =='Yes' else 0

		inHouseEngineering = 2+(0.3*var_6)
		inHouseEngineering += (4*(var_1+var_2))
		inHouseEngineering += (0.9*var_17)
		inHouseEngineering += (0.75*var_16)
		inHouseEngineering += (3.25*var_18)

		#migrationDDS

		preFat = (21.00+ getFloat(1*((var_1+var_2)-1)) if((var_1+var_2)>1) else 21.00 + 0.00) if var_24 == 'Yes' else 0.00

		if(var_23 !="No"):
			migrationDDS = 70.00
			migrationDDS += ((var_1+var_2)-1 if((var_1+var_2)>1) else 0)
			migrationDDS += 0.50*(var_12+var_14+var_17)
			migrationDDS += (1 if(var_8=="ControlNet" or var_8=="Single Ethernet" or var_8=="Dual Ethernet") else 0.00)
		else:
			migrationDDS = 0.00

		fat =( 8.00 + 2*((var_1+var_2)-1) if((var_1+var_2)>1)else 8.00+ 0) if (var_24=="Yes") else 0

		sat = 20.00
		sat += 8.00 if((var_1+var_2)>1) else 0

		siteInstallation = 2.00
		siteInstallation += ((var_1+var_2)*1.50)
		siteInstallation += (0.50*var_4)
		siteInstallation += (1.00*var_3)
		siteInstallation += (1.00*var_9)
		siteInstallation += (4.25*var_1) if(var_20=="Yes") else(1.75*var_1)
		siteInstallation += (0.50*var_2) if(var_20=="Yes") else 0
		siteInstallation += (1.00*var_11) if(var_11>0) else 0
		siteInstallation += (var_7*2.50) if (var_20=="Yes") else (var_7*1.00)
		siteInstallation += (10.40*var_17) if(var_20=="Yes") else (4.00*var_17)
		siteInstallation += (8.15*var_18) if(var_20=="Yes") else (4.00*var_18)
		siteInstallation += (5.15*var_16) if(var_20=="Yes") else (2.00*var_16)
		siteInstallation += (var_14*3.50) if(var_20=="Yes") else (var_14*2.50)
		siteInstallation += ((var_12+var_14)*1.40) if(var_20=="Yes") else((var_12+var_14)*0.25)
		siteInstallation += (0.50*var_14)
		siteInstallation += (var_15*0.40)
		siteInstallation += (var_12*3.90) if(var_20=="Yes") else (var_12*1.65)
		siteInstallation += (var_13*0.40)
		siteInstallation += (1.00*var_12)
		siteInstallation += (6.25*var_5) if(var_20=="Yes") else(3.25*var_5)
		siteInstallation += (0.50*var_9)
		siteInstallation += (2.00+1.00*var_25) if(var_20=="Yes") else 0
		siteInstallation += (1+0.50*var_25) if(var_21=="Yes" ) else 0
		siteInstallation += 24.00 if(var_19=="Yes") else 72.00

		return felSiteDataGathering,inHouseEngineering,preFat,migrationDDS,fat,sat,siteInstallation

def getCBECLabourHours(Product):
	
	parameters = {"CB_EC_migration_to_C300_UHIO_Configuration_Cont":{"var_1":"CB_EC_How_many_CBs_are_being_migrated","var_2":"CB_EC_How_many_ECs_are_being_migrated","var_4":"CB_EC_Do_you_want_Series_C_RAM_Battery_Backup"},"CB_EC_Services_1_Cont":{"var_16":"ATT_CBECAUXFUN","var_15":"ATT_CBECOMLOOP","var_14":"ATT_CBECASLOOP","var_13":"ATT_CBECHGDCP","var_12":"ATT_CBECHGDOT","var_11":"ATT_CBECHGDIN","var_10":"ATT_CBECHGREG","var_9":"ATT_CBECHGOAT","var_8":"ATT_CBECHGAIN","var_3":"ATT_CBECPSNEDR","var_7":"CB_EC_Is_CB/EC_interfacing_with_DHEB_on_the_system","var_18":"CB_EC_Does_the_Customer_have_all_updated_ILDs","var_19":"CB_EC_Does_the_Customer_validate_ILDs_by_Honeywell"},"CB_EC_Services_2_Cont":{"var_6":"CB_EC_IsCommonPVsharingtwoormorethantwoCB/EC","var_20":"CB_EC_Detailed_DDS_required","var_22":"CB_EC_Is_HotCutover_required","var_5":"CB_ECWillHoneywellperforminstallationactivities","var_17":"CB_EC_Data_Gathering_required"},"MSID_CommonQuestions":{"var_21":"MSID_Acceptance_Test_Required"}}
	
	for key in parameters:
		if key == "MSID_CommonQuestions":
			var_21 = getAttrData(Product,parameters[key]["var_21"])
		if key == "CB_EC_migration_to_C300_UHIO_Configuration_Cont":
			var_1 = getFloat(getRowData(Product,key,parameters[key]["var_1"]))
			var_2 = getFloat(getRowData(Product,key,parameters[key]["var_2"]))
			var_4 = getRowData(Product,key,parameters[key]["var_4"])
		if key == "CB_EC_Services_1_Cont":
			var_3 = getFloat(getAttrData(Product,parameters[key]["var_3"]))
			var_7 = getAttrData(Product,parameters[key]["var_7"])
			var_10 = getFloat(getAttrData(Product,parameters[key]["var_10"]))
			var_9 = getFloat(getAttrData(Product,parameters[key]["var_9"]))
			var_8 = getFloat(getAttrData(Product,parameters[key]["var_8"]))
			var_12 = getFloat(getAttrData(Product,parameters[key]["var_12"]))
			var_13 = getFloat(getAttrData(Product,parameters[key]["var_13"]))
			var_11 = getFloat(getAttrData(Product,parameters[key]["var_11"]))
			var_14 = getFloat(getAttrData(Product,parameters[key]["var_14"]))
			var_15 = getFloat(getAttrData(Product,parameters[key]["var_15"]))
			var_16 = getFloat(getAttrData(Product,parameters[key]["var_16"]))
			var_18 = getAttrData(Product,parameters[key]["var_18"])
			var_19 = getAttrData(Product,parameters[key]["var_19"])
		if key == "CB_EC_Services_2_Cont":
			var_5 = getAttrData(Product,parameters[key]["var_5"])
			var_6 = getAttrData(Product,parameters[key]["var_6"])
			var_17 = getAttrData(Product,parameters[key]["var_17"])
			var_20 = getAttrData(Product,parameters[key]["var_20"])
			var_22 = getAttrData(Product,parameters[key]["var_22"])

	migrationDDS = 0
	inhouseEngineering = 5 + 5*(var_1+var_2)
	felSiteVisitDataGathering = 0
	fat = 0
	siteInstallation = 0
	sat = 0
	
	fat = (24.00 + 8.00*(var_1 + var_2 - 1)) if(var_21 != "SAT") else 0
	sat = (8.00 + 4.00*(var_1 + var_2 - 1)) if(var_21 != "FAT") else 0
	if(var_20 == "No"):
		migrationDDS = (20.00 + 3.00*(var_1 + var_2 -1))
	else:
		migrationDDS = (62.00 + 4.00*(var_1 + var_2 -1))
	if(var_5 == "Yes"):
		siteInstallation += ((160.00/60.00)*(var_1 + var_2) + var_3*2.00)
	else:
		siteInstallation += (0.75*(var_1 + var_2) + var_3*0.50)
	if(var_22 == "No"):
		siteInstallation += 0
	else:
		siteInstallation += ((260.00/60.00)*(var_1 + var_2))
		if(var_6 == "Yes"):
			siteInstallation += (var_1 + var_2)
	if(var_4 == "Yes"):
		siteInstallation += (var_1 + var_2)
	else:
		siteInstallation += 0.25
	siteInstallation += (4.50*(var_1 + var_2) + 16.50)
	if(var_17 == "No"):
		felSiteVisitDataGathering += 0
	else:
		felSiteVisitDataGathering += 8
	if(var_18 == "No"):
		if(var_19 == "Yes"):
			felSiteVisitDataGathering += (var_14*(20.00/60.00) + var_15*0.50 + var_16*(40.00/60.00))
	else:
		if(var_19 == "Yes"):
			felSiteVisitDataGathering += (var_14*(10.00/60.00) + var_15*0.25 + var_16*(20.00/60.00))
	if(var_7 == "Yes"):
		inhouseEngineering += ((var_8 + var_9 + var_10 + var_11 + var_12 + var_13)*(5.00/60.00))+(((var_8 + var_9 + var_11 + var_12)*(10.00/60.00))+((var_10 + var_13)*0.50))+(var_14*1.50 + var_15*2.00 + var_16*(20.00/60.00))
	else:
		inhouseEngineering += ((var_8 + var_9 + var_10 + var_11 + var_12 + var_13)*(5.00/60.00)*0.75)+((((var_8 + var_9 + var_11 + var_12)*(10.00/60.00))+((var_10 + var_13)*0.50))*0.75)+((var_14*1.50 + var_15*2.00 + var_16*(20.00/60.00))*0.80)
	inhouseEngineering += ((var_8 + var_9 + var_10 + var_11 + var_12 + var_13)*(5.00/60.00))

	
	return migrationDDS,inhouseEngineering,felSiteVisitDataGathering,fat,siteInstallation,sat


def getxPMtoC300LabourHours(Product,msid_product):
	try:
		CC_ZHR041 = 0
		CC_C8SS01 = 0
		CC_C8DS01 = 0
		CC_CBDD01 = 0
		CC_CBDS01 = 0
		CC_TCF901 = 0
		_8939_HN = 0
		xpmPartCont = msid_product.GetContainerByName('MSID_xPM_C300_Added_Parts_Common_Container').Rows
		for row in xpmPartCont:
			if row['PartNumber']=='CC-ZHR041':
				CC_ZHR041 = row['Quantity']
			if row['PartNumber']=='CC-C8SS01':
				CC_C8SS01 = row['Quantity']
			if row['PartNumber']=='CC-C8DS01':
				CC_C8DS01 = row['Quantity']
			if row['PartNumber']=='CC-CBDD01':
				CC_CBDD01 = row['Quantity']
			if row['PartNumber']== 'CC-CBDS01':
				CC_CBDS01 = row['Quantity']
			if row['PartNumber']== 'CC-TCF901':
				CC_TCF901 = row['Quantity']
			if row['PartNumber']== '8939-HN':
				_8939_HN = row['Quantity']
	except:
		Trace.Write("Error in xPM Part Container ")
	var_1 = getFloat(CC_ZHR041)
	var_4 = getFloat(CC_C8SS01) + getFloat(CC_C8DS01) + getFloat(CC_CBDD01) + getFloat(CC_CBDS01)
	var_5 = getFloat(CC_TCF901)
	var_41 = getFloat(_8939_HN)

	container = Product.GetContainerByName('xPM_C300_Migration_Configuration_Cont')
	countvar3,countvar2,countvar33 = 0,0,0
	for i in container.Rows:
		if(i["xPM_C300_space_in_the_existing_xPM_cabinet"] !="No" and getFloat(i["xPM_C300_Number_of_Pulse_Input_IOMs"]) == 0):
			countvar3 +=1
		else:
			countvar2 +=1
		if(i["xPM_C300_Power_Supply_Upgrade_Needed"] =="Yes"):
			countvar33+=1
	var_3 = getFloat(countvar3)
	var_2 = getFloat(countvar2)
	var_33 = getFloat(countvar33)

	parameters = {"MSID_CommonQuestions":{"var_35":"MSID_Is_Switch_Configuration_in_Honeywell_Scope" ,"var_36":"MSID_Is_Site_Acceptance_Test_Required"},"xPM_C300_General_Qns_Cont":{"var_6":"ATT_NUMXPMC300"},"xPM_C300_Migration_Configuration_Cont":{"var_7":"xPM_C300_Number_of_xPM_Analog_Input_points" , "var_8":"xPM_C300_Number_of_xPM_Analog_Output_points","var_9":"xPM_C300_Number_of_xPM_Digital_Input_points", "var_10":"xPM_C300_Number_of_xPM_Digital_output_points","var_11":"xPM_C300_Number_of_xPM_Digital_composite_points","var_12":"xPM_C300_Number_of_xPM_Regulatory_CNTL_points", "var_13":"xPM_C300_Number_of_xPM_Regulatory_PV_points","var_14":"xPM_C300_Numer_of_xPM_Flags_Numeric_timer","var_15":"xPM_C300_Number_of_xPM_Logic_points","var_16":"xPM_C300_Number_of_xPM_CL", "var_17":"xPM_C300_Number_of_AM_CL","var_18":"xPM_C300_Number_of_Simple_xPM_CL","var_19":"xPM_C300_Number_of_Complex_xPM_CL","var_20":"xPM_C300_Number_of_Simple_AM_CL","var_21":"xPM_C300_Number_of_medium_AM_CL","var_22":"xPM_C300_Number_of_complex_AM_CL","var_23":"xPM_C300_Number_of_Serial_Interface_modules","var_24":"xPM_C300_Number_of_SI_Modbus_and_Allen_Bradley_Rockwell_Array_points_for_PCDI_conversion","var_26":"xPM_C300_Number_of_Pulse_Input_IOMs","var_27":"xPM_C300_Number_of_LLAI_with_FW_Rev_less_than_6.0","var_28":"xPM_C300_Number_of_LLMUX_with_FW_Rev_less_than_4.1","var_29":"xPM_C300_Number_of_RHMUX_with_FW_Rev_less_than_6.0","var_30":"xPM_C300_Number_of_HLAI_with_FW_Rev_bet_3.4_and_6.0","var_31":"xPM_C300_Number_of_HLAI_with_FW_Rev_GEQ_3.3","var_32":"xPM_C300_Number_of_STI_MV_with_FW_Rev_less_than_6.0","var_33":"xPM_C300_Power_Supply_Upgrade_Needed","var_42":"xPM_C300_Number_of_Serial_Interface_points_for_Scada_conversion","var_43":"xPM_C300_Number_of_devices_connected_to_xPM_SI_for_PCDI_conversion"},"xPM_C300_Services_Cont": {"var_34": "xPM_C300_Will_Honeywell_perform_equipment_installa", "var_37": "xPM_C300_Data_Gathering_required","var_39": "ATT_NUMAMTOACE","var_40":"ATT_NUMAMPTS"}}

	for key in parameters:
		if key == "MSID_CommonQuestions":
			var_35 = getAttrData(msid_product,parameters[key]["var_35"])
			var_36 = getAttrData(msid_product,parameters[key]["var_36"])
		if key == "xPM_C300_General_Qns_Cont":
			var_6 = getFloat(getAttrData(Product,parameters[key]["var_6"]))
		if key == "xPM_C300_Migration_Configuration_Cont":
			dict1= {}
			for items in range(7,33):
				if items == 25:
					continue
				dict1.update({"var_{}".format(items): 0})
			dict1.update({"var_42":0})
			dict1.update({"var_43":0})

			for row in getContainer(Product,key).Rows:
				for item in range(7,33):
					if item == 25:
						continue
					dict1["var_{}".format(item)] += getFloat(row[parameters[key]["var_{}".format(item)]])
				dict1["var_42"] += getFloat(row[parameters[key]["var_42"]])
				dict1["var_43"] += getFloat(row[parameters[key]["var_43"]])
				#from var 7 to 32(except 25) and 42, 43 use dict1 to fetch value

		if key =="xPM_C300_Services_Cont":
			var_34 = getAttrData(Product,parameters[key]["var_34"])
			var_37 = getAttrData(Product,parameters[key]["var_37"])
			var_39 =  getFloat(getAttrData(Product,parameters[key]["var_39"]))
			var_40 =  getFloat(getAttrData(Product,parameters[key]["var_40"]))

	#Calculations

	felSiteVisitDataGathering =  16.00 if (var_37 =='Yes') else 0
	documentationRequired = Product.Attr('xPM_C300_Which_Documentation_Required').GetValue()
	selectedDocumentation = documentationRequired.split(',')
	selectedDocumentation = [x.strip() for x in selectedDocumentation]
	var_44 = "Formal FDS"
	var_45 = "Formal DDS"
	var_46 = "SAMA & Logic Drawings"
	var_47= "New Cabinet drawings"
	var_48 = "Existing system cabinet drawings (if UHIO is used)"
	var_49 = "Network Drawings"
	var_50 = "Power & heat calculation"
	var_51 = "Method statement document"
	migrationDDS = 0 if (var_44  not in selectedDocumentation and var_45 not in selectedDocumentation) else 15.00 
	migrationDDS += (var_1 + var_2 - 1.00)*5.00 if var_44 in selectedDocumentation else 0
	migrationDDS += (var_1 + var_2 - 1.00)*5.00 if var_45 in selectedDocumentation else 0
	migrationDDS += (var_6)* 10.00 if var_46 in selectedDocumentation else 0
	migrationDDS +=  (15.00 + (var_4 -1.00)*10.00 if ( var_4 >0) else 0) if var_47 in selectedDocumentation else 0
	migrationDDS +=  ((12.00 + (var_3-1.00)*8.00) if ( var_3 >0) else 0) if var_48 in selectedDocumentation else 0
	migrationDDS += 4.00 if var_49 in selectedDocumentation else 0
	migrationDDS += (((var_3+var_4)*1.50) if ( (var_3+var_4)<5) else 10.00) if var_50 in selectedDocumentation else 0
	migrationDDS += (15.00 + (var_1+var_2-1.00)*5.00) if var_51 in selectedDocumentation else 0
	

	inHouseEngineering = (10.00 +(var_6-1.00)*5.00 + var_6*2.00 + var_6*1.00 + (dict1["var_7"]+dict1["var_8"]+dict1["var_9"]+dict1["var_10"])*2.00/60.00 +(dict1["var_7"]+dict1["var_8"]+dict1["var_9"]+dict1["var_10"])*4.00/60.00) 
	inHouseEngineering += (dict1["var_12"]*18.00/60.00+dict1["var_13"]*12.00/60.00+(dict1["var_15"]*0.70*12.00/60.00+dict1["var_15"]*0.30*36.00/60.00)*0.90+dict1["var_11"]*18.00/60.00 + 4.00 + dict1["var_15"]*0.10*1.20 + dict1["var_18"]*3.60+dict1["var_19"]*9.60*0.30+dict1["var_19"]*6.00*0.70 + var_39*20.00 + var_40*4.00/60.00 + dict1["var_20"]*5.00 + dict1["var_21"]*7.20 +dict1["var_22"]*12.00)
	inHouseEngineering += (dict1["var_24"])*18.00/60.00   if(dict1["var_43"]>0) else 0
	inHouseEngineering += dict1["var_42"]*2.00/60.00 + dict1["var_26"]*2 + (dict1["var_11"]+dict1["var_12"]+dict1["var_13"]+dict1["var_15"])*5.00/60.00+(dict1["var_18"]+dict1["var_20"])*8.00/60.00+(dict1["var_19"]+dict1["var_20"])*10.00/60.00+dict1["var_21"]*18.00/60.00

	fatProcedure = (16.00 +(var_1+var_2-1.00)*5.00)

	preFAT = (var_1+var_2)*1.00 + (var_1+var_2)*2.50 + (dict1["var_7"]+dict1["var_8"]+ dict1["var_9"]+ dict1["var_10"]+dict1["var_11"]+dict1["var_12"]+dict1["var_13"]+dict1["var_14"]+dict1["var_15"])*2.50/60.00+(dict1["var_18"]+dict1["var_20"])*4.00/60.00+(dict1["var_19"]+dict1["var_20"])*6.00/60+dict1["var_21"]*10/60*0.7+dict1["var_21"]*12/60*0.30 +(dict1["var_24"])*4.00/60.00 + (var_1+var_2)*36.00/60.00 +(var_1+var_2)*1.20

	fat = preFAT *0.60

	siteInstallationEaps = 4.00  if(var_34 =="No") else 0
	siteInstallationEaps += 2.00  if (var_35 =="Yes") else 0
	siteInstallationEaps += (dict1["var_27"]+dict1["var_28"]+dict1["var_29"]+dict1["var_30"]+dict1["var_32"])*15.00/60.00 + dict1["var_31"]*5.00/60.00 + (var_1+var_2)*15.00/60.00 +(var_1+var_2)*1.00 + dict1["var_43"]*30.00/60.00
	siteInstallationEaps += dict1["var_43"]*30.00/60.00 if (var_34 =="Yes") else  dict1["var_43"]*10.00/60.00
	siteInstallationEaps += 30.00/60.00
	siteInstallationEaps += 2.00 if (var_34 =="Yes") else  30.00/60.00
	siteInstallationEaps += (2.00 + 4.00+ (var_39*4.00) + 4.00)

	siteInstallationEST1 = (var_6*1.00+var_6*15.00/60.00+dict1["var_23"]*5.00/60.00+dict1["var_23"]*45.00/60.00+dict1["var_26"]*30.00/60.00+var_4*8.00+var_3*2.00+var_41*1.00+(var_1+var_2)*20.00/60.00+dict1["var_26"]*2.00+var_33*30.00/60.00+(var_1+var_2)*30.00/60.00+var_5*15.00/60.00+dict1["var_23"]*30.00/60.00+dict1["var_23"]*30.00/60.00+dict1["var_23"]*1.00+2.00) if (var_34 =="Yes") else 0

	commisioning = (dict1["var_24"])*2.00/60.00 + (dict1["var_7"]+dict1["var_8"]+dict1["var_9"]+dict1["var_10"])*2.00/60.00+(dict1["var_11"]+dict1["var_12"]+dict1["var_13"]+dict1["var_15"])*4.00/60.00+dict1["var_14"]*1.00/60.00 + var_40*10.00/60.00 + dict1["var_26"]*2.00 + 12.00+(var_1+var_2-1)*8.00

	sat = (16.00+(var_1+var_2-1.00)*4 + 8.00+(var_1+var_2-1.00)*2.00 +4.00 + 8.00+ (var_1+var_2-1.00)*4.00) if(var_36 == "Yes") else 0

	return felSiteVisitDataGathering,migrationDDS,inHouseEngineering,fatProcedure,preFAT,fat,siteInstallationEaps,siteInstallationEST1,commisioning,sat