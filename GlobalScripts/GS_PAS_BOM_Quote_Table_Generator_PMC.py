salesOrg = Quote.GetCustomField('Sales Area').Content
query = SqlHelper.GetList("Select Part_Number from HPS_LABOR_COST_DATA where Sales_Org='{}' ".format(salesOrg))
labor_parts = [x.Part_Number for x in query]
project = ""

for item in Quote.MainItems:
	if item.PartNumber == 'PRJT':
		project = item
		break

parts_dict = {}
sg_num = 0
names_dict = {}
for x in range(32):
	names_dict["CG_{0}".format(x+1)] = row = {}
	row["SG_1"] = row["SG_2"] = row["SG_3"] = row["SG_4"] = row["SG_5"] = row["SG_6"] = row["SG_7"] = row["SG_8"] = row["SG_9"] = row["SG_10"] = "Not Applicable"
	for y in range(16):
		names_dict["CG_{0}_RG_{1}".format(x+1,y+1)] = row = {}
		row["SG_1"] = row["SG_2"] = row["SG_3"] = row["SG_4"] = row["SG_5"] = row["SG_6"] = row["SG_7"] = row["SG_8"] = row["SG_9"] = row["SG_10"] = "Not Applicable"
area = {}
ioSum1=[]
cg_rg_map = {}
if project != "":
	for sys_group in project.Children:
		sg_num += 1
		gc = 0
		#system_group = parts_dict["{}".format(sg_num)] = {}
		system_group = parts_dict[sg_num] = {}
		system_group["SG_Name"] = sys_group.PartNumber
		for system in sys_group.Children:
			if system.ProductName in ['Variable Frequency Drive System']:
				part1 = area[system.QI_Area.Value] = {}
				part1[sys_group.PartNumber] = []
			if system.ProductName in ["Generic System"]:
				gc += 1
				if gc > 1:
					system_items = sample_dictionary
				else:
					system_items = system_group["{0}".format(system.ProductName)] = {}
			else:
				system_items = system_group["{0}".format(system.ProductName)] = {}
			if system.ProductName in ['Experion HS System']:
				cg_num = 0
				for rtu_child in system.Children:
					if rtu_child.ProductName in ['Experion HS Group']:
						cg_num += 1
						names_dict["CG_{0}".format(cg_num)]["SG_{0}".format(sg_num)] = rtu_child.PartNumber
						for control_group_child in rtu_child.Children:
							if control_group_child.PartNumber not in system_items: #New part needs to be added
								part = system_items[control_group_child.PartNumber] = {}
								part["Description"] = control_group_child.ProductName
								part["Product_Line"] = str(control_group_child.QI_PLSG.Value)
								part["Total"] = int(control_group_child.Quantity)
								part["CG_{0}".format(cg_num)] = str(control_group_child.Quantity)
							else: #Product already exists
								part = system_items[control_group_child.PartNumber]
								part["Total"] += int(control_group_child.Quantity)
								part["CG_{0}".format(cg_num)] = str(control_group_child.Quantity)
			elif system.ProductName in ['HC900 System']:
				cg_num = 0
				for rtu_child in system.Children:
					if rtu_child.ProductName in ['HC900 Group']:
						cg_num += 1
						names_dict["CG_{0}".format(cg_num)]["SG_{0}".format(sg_num)] = rtu_child.PartNumber
						for control_group_child in rtu_child.Children:
							if control_group_child.PartNumber not in system_items: #New part needs to be added
								part = system_items[control_group_child.PartNumber] = {}
								part["Description"] = control_group_child.ProductName
								part["Product_Line"] = str(control_group_child.QI_PLSG.Value)
								part["Total"] = int(control_group_child.Quantity)
								part["CG_{0}".format(cg_num)] = str(control_group_child.Quantity)
							else: #Product already exists
								part = system_items[control_group_child.PartNumber]
								part["Total"] += int(control_group_child.Quantity)
								part["CG_{0}".format(cg_num)] = str(control_group_child.Quantity)   
			elif system.ProductName in ['PlantCruise System']:
				cg_num = 0
				for rtu_child in system.Children:
					if rtu_child.ProductName in ['PlantCruise Group']:
						cg_num += 1
						names_dict["CG_{0}".format(cg_num)]["SG_{0}".format(sg_num)] = rtu_child.PartNumber
						for control_group_child in rtu_child.Children:
							if control_group_child.PartNumber not in system_items: #New part needs to be added
								part = system_items[control_group_child.PartNumber] = {}
								part["Description"] = control_group_child.ProductName
								part["Product_Line"] = str(control_group_child.QI_PLSG.Value)
								part["Total"] = int(control_group_child.Quantity)
								part["CG_{0}".format(cg_num)] = str(control_group_child.Quantity)
							else: #Product already exists
								part = system_items[control_group_child.PartNumber]
								part["Total"] += int(control_group_child.Quantity)
								part["CG_{0}".format(cg_num)] = str(control_group_child.Quantity)   
			elif system.ProductName in ['ControlEdge PCD System']:
				cg_num = 0
				for rtu_child in system.Children:
					if rtu_child.ProductName in ['ControlEdge PCD Group']:
						cg_num += 1
						names_dict["CG_{0}".format(cg_num)]["SG_{0}".format(sg_num)] = rtu_child.PartNumber
						for control_group_child in rtu_child.Children:
							if control_group_child.PartNumber not in system_items: #New part needs to be added
								part = system_items[control_group_child.PartNumber] = {}
								part["Description"] = control_group_child.ProductName
								part["Product_Line"] = str(control_group_child.QI_PLSG.Value)
								part["Total"] = int(control_group_child.Quantity)
								part["CG_{0}".format(cg_num)] = str(control_group_child.Quantity)
							else: #Product already exists
								part = system_items[control_group_child.PartNumber]
								part["Total"] += int(control_group_child.Quantity)
								part["CG_{0}".format(cg_num)] = str(control_group_child.Quantity)
			elif system.ProductName in ['Terminal Manager']:
				cg_num = 0
				for rtu_child in system.Children:
					if rtu_child.PartNumber not in labor_parts: #rtu system parts, excluded labor
						if rtu_child.PartNumber not in system_items: #New part needs to be added
							part = system_items[rtu_child.PartNumber] = {}
							part["Description"] = rtu_child.ProductName
							part["Product_Line"] = str(rtu_child.QI_PLSG.Value)
							part["Total"] = int(rtu_child.Quantity)
							part["System_Items"] = str(rtu_child.Quantity)
						else: #Product already exists
							part = system_items[rtu_child.PartNumber]
							part["Total"] += int(rtu_child.Quantity)
							part["System_Items"] = str(rtu_child.Quantity)
			elif system.ProductName in ['Measurement IQ System']:
				cg_num = 0
				for rtu_child in system.Children:
					if rtu_child.PartNumber not in labor_parts: #rtu system parts, excluded labor
						if rtu_child.PartNumber not in system_items: #New part needs to be added
							part = system_items[rtu_child.PartNumber] = {}
							part["Description"] = rtu_child.ProductName
							part["Product_Line"] = str(rtu_child.QI_PLSG.Value)
							part["Total"] = int(rtu_child.Quantity)
							part["System_Items"] = str(rtu_child.Quantity)
						else: #Product already exists
							part = system_items[rtu_child.PartNumber]
							part["Total"] += int(rtu_child.Quantity)
							part["System_Items"] = str(rtu_child.Quantity)
			elif system.ProductName in ['MasterLogic-50 Generic']:
				cg_num = 0
				for rtu_child in system.Children:
					if rtu_child.PartNumber not in labor_parts: #rtu system parts, excluded labor
						if rtu_child.PartNumber not in system_items: #New part needs to be added
							part = system_items[rtu_child.PartNumber] = {}
							part["Description"] = rtu_child.ProductName
							part["Product_Line"] = str(rtu_child.QI_PLSG.Value)
							part["Total"] = int(rtu_child.Quantity)
							part["System_Items"] = str(rtu_child.Quantity)
						else: #Product already exists
							part = system_items[rtu_child.PartNumber]
							part["Total"] += int(rtu_child.Quantity)
							part["System_Items"] = str(rtu_child.Quantity)
			elif system.ProductName in ['MasterLogic-200 Generic']:
				cg_num = 0
				for rtu_child in system.Children:
					if rtu_child.PartNumber not in labor_parts: #rtu system parts, excluded labor
						if rtu_child.PartNumber not in system_items: #New part needs to be added
							part = system_items[rtu_child.PartNumber] = {}
							part["Description"] = rtu_child.ProductName
							part["Product_Line"] = str(rtu_child.QI_PLSG.Value)
							part["Total"] = int(rtu_child.Quantity)
							part["System_Items"] = str(rtu_child.Quantity)
						else: #Product already exists
							part = system_items[rtu_child.PartNumber]
							part["Total"] += int(rtu_child.Quantity)
							part["System_Items"] = str(rtu_child.Quantity)
			elif system.ProductName in ['Experion LX Generic']:
				cg_num = 0
				for rtu_child in system.Children:
					if rtu_child.PartNumber not in labor_parts: #rtu system parts, excluded labor
						if rtu_child.PartNumber not in system_items: #New part needs to be added
							part = system_items[rtu_child.PartNumber] = {}
							part["Description"] = rtu_child.ProductName
							part["Product_Line"] = str(rtu_child.QI_PLSG.Value)
							part["Total"] = int(rtu_child.Quantity)
							part["System_Items"] = str(rtu_child.Quantity)
						else: #Product already exists
							part = system_items[rtu_child.PartNumber]
							part["Total"] += int(rtu_child.Quantity)
							part["System_Items"] = str(rtu_child.Quantity)
			elif system.ProductName in ['Generic System']:
				cg_num = 0
				for rtu_child in system.Children:
					if rtu_child.PartNumber not in labor_parts: #rtu system parts, excluded labor
						if rtu_child.PartNumber not in system_items: #New part needs to be added
							part = system_items[rtu_child.PartNumber] = {}
							part["Description"] = rtu_child.ProductName
							part["Product_Line"] = str(rtu_child.QI_PLSG.Value)
							part["Total"] = int(rtu_child.Quantity)
							part["System_Items"] = str(rtu_child.Quantity)
						else: #Product already exists
							part = system_items[rtu_child.PartNumber]
							part["Total"] += int(rtu_child.Quantity)
							part["System_Items"] = str(rtu_child.Quantity)
				sample_dictionary = system_items
			elif system.ProductName in ['Virtualization System']:
				cg_num = 0
				for rtu_child in system.Children:
					if rtu_child.PartNumber not in labor_parts: #rtu system parts, excluded labor
						if rtu_child.PartNumber not in system_items: #New part needs to be added
							part = system_items[rtu_child.PartNumber] = {}
							part["Description"] = rtu_child.ProductName
							part["Product_Line"] = str(rtu_child.QI_PLSG.Value)
							part["Total"] = int(rtu_child.Quantity)
							part["System_Items"] = str(rtu_child.Quantity)
						else: #Product already exists
							part = system_items[rtu_child.PartNumber]
							part["Total"] += int(rtu_child.Quantity)
							part["System_Items"] = str(rtu_child.Quantity)
							#Trace.Write('part'+str(part))
			elif system.ProductName in ['C300 System']:
				contr = system.SelectedAttributes.GetContainerByName('Series_C_Control_Groups_Cont')
				if contr:
					for row in contr.Rows:
						control_group_name = row['Series_C_CG_Name']
						ioSum1.append(row['Series_C_CG_Name'])
						control_name = "|".join(ioSum1)
						cg_rg_map[control_group_name] = []

				for item in filter(lambda item: item.ProductName.startswith("Series-C Control Group"), system.Children):
					contr1 = item.SelectedAttributes.GetContainerByName('Series_C_Remote_Groups_Cont')
					if contr1:
						control_group_name = item.PartNumber 
						if control_group_name in cg_rg_map:
							for row in contr1.Rows:
								remote_group_name = row['Series_C_RG_Name']
								cg_rg_map[control_group_name].append(remote_group_name)

				for control_group_name in cg_rg_map:
					while len(cg_rg_map[control_group_name]) < 10:
						cg_rg_map[control_group_name].append("")

				cg_num = 0
				for hipps_child in system.Children:
					if hipps_child.ProductName in ['Series-C Control Group']:
						cg_num += 1
						rg_num = 0
						names_dict["CG_{0}".format(cg_num)]["SG_{0}".format(sg_num)] = hipps_child.PartNumber
						for control_group_child in hipps_child.Children:
							if control_group_child.ProductName in ['Series-C Remote Group']:
								rg_num += 1
								names_dict["CG_{0}_RG_{1}".format(cg_num, rg_num)]["SG_{0}".format(sg_num)] = hipps_child.PartNumber
								for rg_part in control_group_child.Children:
									if rg_part.PartNumber not in system_items: #New part needs to be added
										part = system_items[rg_part.PartNumber] = {}
										part["Description"] = rg_part.ProductName
										part["Product_Line"] = str(rg_part.QI_PLSG.Value)
										part["Total"] = int(rg_part.Quantity)
										part["CG_{0}_RG_{1}".format(cg_num, rg_num)] = str(rg_part.Quantity)
									else: #Product already exists
										part = system_items[rg_part.PartNumber]
										part["Total"] += int(rg_part.Quantity)
										part["CG_{0}_RG_{1}".format(cg_num, rg_num)] = str(rg_part.Quantity)
							else: #normal control group parts
								if control_group_child.PartNumber not in system_items: #New part needs to be added
									part = system_items[control_group_child.PartNumber] = {}
									part["Description"] = control_group_child.ProductName
									part["Product_Line"] = str(control_group_child.QI_PLSG.Value)
									part["Total"] = int(control_group_child.Quantity)
									part["CG_{0}".format(cg_num)] = str(control_group_child.Quantity)
								else: #Product already exists
									part = system_items[control_group_child.PartNumber]
									part["Total"] += int(control_group_child.Quantity)
									part["CG_{0}".format(cg_num)] = str(control_group_child.Quantity)

for item in Quote.MainItems:
	vfdquery = SqlHelper.GetFirst("Select VFD_VC_Model from VFD_VC_Models where VFD_VC_Model = '{}'".format(item.PartNumber))
	vfdsparequery = SqlHelper.GetFirst("Select VFD_VC_Model from VFD_VC_Models where VFD_VC_Model = '{}'".format(item.QI_ParentVcModel.Value))
	if vfdquery is not None or vfdsparequery is not None:
		if area.get(item.QI_Area.Value):
			dict = {}
			dict["Model Number"] = item.PartNumber
			dict["Model Description"] = item.Description
			dict["Product Line"] = item.QI_PLSG.Value
			dict["Quantity"] = str(item.Quantity)

			for key in area[item.QI_Area.Value]:
				area[item.QI_Area.Value][key].append(dict)

Trace.Write("PAS BOM parts: {}".format(parts_dict))
#Trace.Write('sys'+str(system_items))
#=============================================================
#Section that loops through dictionary and adds it to the quote table
quoteTable = Quote.QuoteTables["BOM_Table_for_Proposals"]
#quoteTable.Rows.Clear()
Exp_HS_number = 0
HC900_number = 0
PlantCruise_number = 0
PCD_number = 0
Terminal_number = 0
MIQ_number = 0
Generic50_number = 0
Generic200_number = 0
Exp_LX_number = 0
Generic_number = 0
C300_number= 0
Virtualization = 0
for sg_id,sys_group in sorted(parts_dict.items()):
	for system_name in sys_group:
		if system_name == 'SG_Name': #Skips the name, because it isn't a system.
			continue
		system = sys_group[system_name]

		for part_num in system:
			part = system[part_num]
			row = quoteTable.AddNewRow()
			if system_name == 'Experion HS System':
				Exp_HS_number += 1
				row['S_Number'] = Exp_HS_number
			elif system_name == 'HC900 System':
				HC900_number += 1
				row['S_Number'] = HC900_number
			elif system_name == 'PlantCruise System':
				PlantCruise_number += 1
				row['S_Number'] = PlantCruise_number
			elif system_name == 'ControlEdge PCD System':
				PCD_number += 1
				row['S_Number'] = PCD_number
			elif system_name == 'Terminal Manager':
				Terminal_number += 1
				row['S_Number'] = Terminal_number
			elif system_name == 'Measurement IQ System':
				MIQ_number += 1
				row['S_Number'] = MIQ_number
			elif system_name == 'MasterLogic-50 Generic':
				Generic50_number += 1
				row['S_Number'] = Generic50_number
			elif system_name == 'MasterLogic-200 Generic':
				Generic200_number += 1
				row['S_Number'] = Generic200_number
			elif system_name == 'Experion LX Generic':
				Exp_LX_number += 1
				row['S_Number'] = Exp_LX_number
			elif system_name == 'Generic System':
				Generic_number += 1
				row['S_Number'] = Generic_number
			elif system_name == 'Virtualization System':
				Virtualization += 1
				row['S_Number'] = Virtualization
			elif system_name == 'C300 System':
				C300_number += 1
				row['S_Number'] = C300_number
				row['CG_Name'] = control_name 
				for i, control_group_name in enumerate(ioSum1, start=1):
					cg_name = control_group_name
					rg_name = "|".join(cg_rg_map[control_group_name])
					row["CG_" +str(i) + "_RG_NAME"] = rg_name
			row['Model_Number'] = part_num
			row['Sys_Name'] = system_name
			row['SG_Name'] = sys_group['SG_Name']
			row['SG_ID'] = sg_id

			for entry in part:
				row[entry] = part.get(entry)
sr =0
#Trace.Write(str(area))
if  area != {}:
	for key in area:
		for value in area[key]:
			if area[key][value] !=[]:
				for i in area[key][value]:
					sr+=1
					row = quoteTable.AddNewRow()
					row["S_Number"] = str(sr)
					row["SG_Name"] = str(value)
					row['Sys_Name'] = "Variable Frequency Drive System"
					row["Model_Number"] = str(i["Model Number"])
					row["Description"] = str(i["Model Description"])
					row["Product_Line"] = str(i["Product Line"])
					row["Total"] = str(i["Quantity"])

if Quote.GetCustomField('R2QFlag').Content == 'Yes':
	for item in Quote.MainItems:
		if (item.PartNumber) == "Write-In Third Party Hardware & Software" and (str(item.QI_Area.Value).split("_")[0]) == "DCS":
			row = quoteTable.AddNewRow()
			C300_number += 1
			row['Sys_Name'] = "Write-In Third Party for C300"
			row['S_Number'] = C300_number
			row["Description"] = item.Description
			row["SG_Name"] = "Marshalling - " + str(item.QI_Area.Value)
			row["Model_Number"] = "Write-Ins"
			row["Total"] = item.Quantity


quoteTable.Save()

#Section to update names table
names_table = Quote.QuoteTables["PAS_BOM_Group_Names"]
for col_name, column_dict in sorted(names_dict.items()):
	column_dict = names_dict[col_name]
	test3 = repr(column_dict)
	test4 = col_name
	row = names_table.AddNewRow()
	row['Column_ID'] = col_name

	for entry in column_dict:
		row[entry] = column_dict.get(entry)

names_table.Save()