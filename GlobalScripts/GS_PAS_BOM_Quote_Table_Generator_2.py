salesOrg = Quote.GetCustomField('Sales Area').Content
query = SqlHelper.GetList("Select Part_Number from HPS_LABOR_COST_DATA where Sales_Org='{}' ".format(salesOrg))
labor_parts = [x.Part_Number for x in query]
plc_part_list = []
project = ""

for item in Quote.MainItems:
	if item.PartNumber == 'PRJT':
		project = item
		break
ioSum1=[]
fieldname = []
cg_rg_map = {}
parts_dict = {}
sg_num = 0
names_dict = {}
for x in range(50):
	names_dict["CG_{}".format(x+1)] = row = {}
	row["SG_1"] = row["SG_2"] = row["SG_3"] = row["SG_4"] = row["SG_5"] = row["SG_6"] = row["SG_7"] = row["SG_8"] = row["SG_9"] = row["SG_10"] = "Not Applicable"
	for y in range(16):
		names_dict["CG_{0}_RG_{1}".format(x+1,y+1)] = row = {}
		row["SG_1"] = row["SG_2"] = row["SG_3"] = row["SG_4"] = row["SG_5"] = row["SG_6"] = row["SG_7"] = row["SG_8"] = row["SG_9"] = row["SG_10"] = "Not Applicable"
Trace.Write(str(names_dict))
if project != "":
	for sys_group in project.Children:
		sg_num += 1
		#system_group = parts_dict["{}".format(sg_num)] = {}
		system_group = parts_dict[sg_num] = {}
		system_group["SG_Name"] = sys_group.PartNumber
		for system in sys_group.Children:
			system_items = system_group["{0}".format(system.ProductName)] = {}
			if system.ProductName in ['Experion MX System']:
				cg_num_1 = 0
				cg_num_2 = 20
				for mx_child in system.Children:
					#Trace.Write(mx_child.ProductName)
					if mx_child.ProductName in ['Scanner Group']:
						cg_num_1 += 1
						rg_num = 0
						names_dict["CG_{0}".format(cg_num_1)]["SG_{0}".format(sg_num)] = mx_child.PartNumber
						for control_group_child in mx_child.Children:
							if control_group_child.ProductName in ['Sensor Group']:
								rg_num += 1
								names_dict["CG_{0}_RG_{1}".format(cg_num_1, rg_num)]["SG_{0}".format(sg_num)] = mx_child.PartNumber
								for rg_part in control_group_child.Children:
									if rg_part.PartNumber not in system_items: #New part needs to be added
										part = system_items[rg_part.PartNumber] = {}
										part["Description"] = rg_part.ProductName
										part["Product_Line"] = str(rg_part.QI_PLSG.Value)
										part["Total"] = int(rg_part.Quantity)
										part["CG_{0}_RG_{1}".format(cg_num_1, rg_num)] = str(rg_part.Quantity)
									else: #Product already exists
										part = system_items[rg_part.PartNumber]
										part["Total"] += int(rg_part.Quantity)
										part["CG_{0}_RG_{1}".format(cg_num_1, rg_num)] = str(rg_part.Quantity)
							else: #normal control group parts
								if control_group_child.PartNumber not in system_items: #New part needs to be added
									part = system_items[control_group_child.PartNumber] = {}
									part["Description"] = control_group_child.ProductName
									part["Product_Line"] = str(control_group_child.QI_PLSG.Value)
									part["Total"] = int(control_group_child.Quantity)
									part["CG_{0}".format(cg_num_1)] = str(control_group_child.Quantity)
								else: #Product already exists
									part = system_items[control_group_child.PartNumber]
									part["Total"] += int(control_group_child.Quantity)
									part["CG_{0}".format(cg_num_1)] = str(control_group_child.Quantity)

					elif mx_child.ProductName in ['CD Control Group']:
						cg_num_2 += 1
						names_dict["CG_{0}".format(cg_num_2)]["SG_{0}".format(sg_num)] = mx_child.PartNumber
						for control_group_child in mx_child.Children:
							if control_group_child.PartNumber not in system_items: #New part needs to be added
								part = system_items[control_group_child.PartNumber] = {}
								part["Description"] = control_group_child.ProductName
								part["Product_Line"] = str(control_group_child.QI_PLSG.Value)
								part["Total"] = int(control_group_child.Quantity)
								part["CG_{0}".format(cg_num_2)] = str(control_group_child.Quantity)
							else: #Product already exists
								part = system_items[control_group_child.PartNumber]
								part["Total"] += int(control_group_child.Quantity)
								part["CG_{0}".format(cg_num_2)] = str(control_group_child.Quantity)
					elif mx_child.PartNumber not in labor_parts: #rtu system parts, excluded labor
						if mx_child.PartNumber not in system_items: #New part needs to be added
							part = system_items[mx_child.PartNumber] = {}
							part["Description"] = mx_child.ProductName
							part["Product_Line"] = str(mx_child.QI_PLSG.Value)
							part["Total"] = int(mx_child.Quantity)
							part["System_Items"] = str(mx_child.Quantity)
						else: #Product already exists
							part = system_items[mx_child.PartNumber]
							part["Total"] += int(mx_child.Quantity)
							part["System_Items"] = str(mx_child.Quantity)
			
			if system.ProductName in ['MXProLine System']:
				cg_num_1 = 0
				cg_num_2 = 20
				for mx_child in system.Children:
					#Trace.Write(mx_child.ProductName)
					if mx_child.ProductName in ['MXP Scanner Group']:
						cg_num_1 += 1
						rg_num = 0
						names_dict["CG_{0}".format(cg_num_1)]["SG_{0}".format(sg_num)] = mx_child.PartNumber
						for control_group_child in mx_child.Children:
							if control_group_child.ProductName in ['MXP Sensor Group']:
								rg_num += 1
								names_dict["CG_{0}_RG_{1}".format(cg_num_1, rg_num)]["SG_{0}".format(sg_num)] = mx_child.PartNumber
								for rg_part in control_group_child.Children:
									if rg_part.PartNumber not in system_items: #New part needs to be added
										part = system_items[rg_part.PartNumber] = {}
										part["Description"] = rg_part.ProductName
										part["Product_Line"] = str(rg_part.QI_PLSG.Value)
										part["Total"] = int(rg_part.Quantity)
										part["CG_{0}_RG_{1}".format(cg_num_1, rg_num)] = str(rg_part.Quantity)
									else: #Product already exists
										part = system_items[rg_part.PartNumber]
										part["Total"] += int(rg_part.Quantity)
										part["CG_{0}_RG_{1}".format(cg_num_1, rg_num)] = str(rg_part.Quantity)
							else: #normal control group parts
								if control_group_child.PartNumber not in system_items: #New part needs to be added
									part = system_items[control_group_child.PartNumber] = {}
									part["Description"] = control_group_child.ProductName
									part["Product_Line"] = str(control_group_child.QI_PLSG.Value)
									part["Total"] = int(control_group_child.Quantity)
									part["CG_{0}".format(cg_num_1)] = str(control_group_child.Quantity)
								else: #Product already exists
									part = system_items[control_group_child.PartNumber]
									part["Total"] += int(control_group_child.Quantity)
									part["CG_{0}".format(cg_num_1)] = str(control_group_child.Quantity)

					elif mx_child.ProductName in ['MXP CD Control Group']:
						cg_num_2 += 1
						names_dict["CG_{0}".format(cg_num_2)]["SG_{0}".format(sg_num)] = mx_child.PartNumber
						for control_group_child in mx_child.Children:
							if control_group_child.PartNumber not in system_items: #New part needs to be added
								part = system_items[control_group_child.PartNumber] = {}
								part["Description"] = control_group_child.ProductName
								part["Product_Line"] = str(control_group_child.QI_PLSG.Value)
								part["Total"] = int(control_group_child.Quantity)
								part["CG_{0}".format(cg_num_2)] = str(control_group_child.Quantity)
							else: #Product already exists
								part = system_items[control_group_child.PartNumber]
								part["Total"] += int(control_group_child.Quantity)
								part["CG_{0}".format(cg_num_2)] = str(control_group_child.Quantity)
					elif mx_child.PartNumber not in labor_parts: #rtu system parts, excluded labor
						if mx_child.PartNumber not in system_items: #New part needs to be added
							part = system_items[mx_child.PartNumber] = {}
							part["Description"] = mx_child.ProductName
							part["Product_Line"] = str(mx_child.QI_PLSG.Value)
							part["Total"] = int(mx_child.Quantity)
							part["System_Items"] = str(mx_child.Quantity)
						else: #Product already exists
							part = system_items[mx_child.PartNumber]
							part["Total"] += int(mx_child.Quantity)
							part["System_Items"] = str(mx_child.Quantity)

			if system.ProductName in ['ARO, RESS & ERG System']:
				cg_num = 0
				for rtu_child in system.Children:
					if rtu_child.ProductName in ['Experion ARO, RESS & ERG Group']:
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
					elif rtu_child.PartNumber not in labor_parts: #rtu system parts, excluded labor
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
			if system.ProductName in ['Digital Video Manager']:
				cg_num = 0
				for rtu_child in system.Children:
					if rtu_child.ProductName in ['Digital Video Manager Group']:
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
					elif rtu_child.PartNumber not in labor_parts: #rtu system parts, excluded labor
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
			if system.ProductName in ['Field Device Manager']:
				contr = system.SelectedAttributes.GetContainerByName('FDM_System_Group_Cont')
				if contr:
					for row in contr.Rows:
						control_group_name = row['FDM_System_Group_Name']
						fieldname.append(row['FDM_System_Group_Name'])
						field_name = "|".join(fieldname)
				cg_num = 0
				for rtu_child in system.Children:
					if rtu_child.ProductName in ['FDM System Group']:
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
					elif rtu_child.PartNumber not in labor_parts: #rtu system parts, excluded labor
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
		
			if system.ProductName in ['Electrical Substation Data Collector']:
				cg_num = 0
				for rtu_child in system.Children:
					#commoncode ()
					if rtu_child.ProductName in ["Electrical Substation Data Collector Group"]:
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
					elif rtu_child.PartNumber not in labor_parts: #rtu system parts, excluded labor
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
			if system.ProductName in ['Simulation System']:
				cg_num = 0
				for rtu_child in system.Children:
					#commoncode ()
					if rtu_child.ProductName in ["Simulation System Group"]:
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
					elif rtu_child.PartNumber not in labor_parts: #rtu system parts, excluded labor
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
			if system.ProductName in ['eServer System']:
				contr = system.SelectedAttributes.GetContainerByName('ES_Group')
				if contr:
					for row in contr.Rows:
						control_group_name = row['eServer_System_Group_Name']
						ioSum1.append(row['eServer_System_Group_Name'])
						eserver_name = "|".join(ioSum1)
				cg_num = 0
				for rtu_child in system.Children:
					if rtu_child.ProductName in ["eServer System Group"]:
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
					elif rtu_child.PartNumber not in labor_parts: #rtu system parts, excluded labor
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
Trace.Write("PAS BOM parts: {}".format(parts_dict))
#=============================================================
#Section that loops through dictionary and adds it to the quote table
quoteTable = Quote.QuoteTables["BOM_Table_for_Proposals"]
#quoteTable.Rows.Clear()

experion_num = 0
MXProLine_num = 0
ARORESS_num = 0
DVM_num = 0
FDM_num = 0
ESDC_num = 0
Simulation_num =0
eServer_num =0
for sg_id,sys_group in sorted(parts_dict.items()):
	for system_name in sys_group:
		if system_name == 'SG_Name': #Skips the name, because it isn't a system.
			continue
		system = sys_group[system_name]

		for part_num in system:
			part = system[part_num]
			row = quoteTable.AddNewRow()
			if system_name == 'Experion MX System':
				experion_num += 1
				row['S_Number'] = experion_num
			elif system_name == 'MXProLine System':
				MXProLine_num += 1
				row['S_Number'] = MXProLine_num
			elif system_name == 'ARO, RESS & ERG System':
				ARORESS_num += 1
				row['S_Number'] = ARORESS_num
			elif system_name == 'Digital Video Manager':
				DVM_num += 1
				row['S_Number'] = DVM_num
			elif system_name == 'Field Device Manager':
				FDM_num += 1
				row['S_Number'] = FDM_num
				row['CG_Name'] = field_name
			elif system_name == 'Electrical Substation Data Collector':
				ESDC_num += 1
				row['S_Number'] = ESDC_num
			elif system_name == 'Simulation System':
				Simulation_num += 1
				row['S_Number'] = Simulation_num
			elif system_name == 'eServer System':
				eServer_num += 1
				row['S_Number'] = eServer_num
				row['CG_Name']	= eserver_name
			row['Model_Number'] = part_num
			row['Sys_Name'] = system_name
			row['SG_Name'] = sys_group['SG_Name']
			row['SG_ID'] = sg_id

			for entry in part:
				row[entry] = part.get(entry)

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